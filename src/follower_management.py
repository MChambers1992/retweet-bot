# Retweet Bot follower management module

import common_methods
import logging
import datetime

import tweepy

async def manage_followers(api, config):
    """Performs the logic surrounding maintaining active follower using the follower management settings defined in the config file"""

    if (config.follower_management['manage_followers'] and
        common_methods.can_perform_action_today(config.follower_management['days_to_manage']) is True and
        common_methods.can_perform_action_this_month(config.follower_management['months_to_manage']) is True):
        
        followers = set(api.followers_ids(config.twitter_keys['screen_name']))
        following = set(api.friends_ids(config.twitter_keys['screen_name']))
        not_following_back = [item for item in followers if item not in following]
        following_back = [item for item in followers if item in following]

        if config.follower_management['aggressive_management'] is True:
            aggressive_management(api, config)
        else:
            passive_management(api, config, following, following_back)
        
        if config.follower_management['follow_back'] is True:
            follow_back(api, config, not_following_back)


def follow_back(api, config, not_following_list):
    """Follows back any users who you have not have reciprocated a connection with"""

    followed_users = 0
    err_count = 0

    try:
        for user in not_following_list:
            if followed_users < config.follower_management['max_follows']:
                api.create_friendship(user, True)
                followed_users += 1

        logging.info("Finished reciprocated follows. %d users followed." % followed_users)
    except (tweepy.error.TweepError, IndexError) as err:
        err_count += 1
        logging.error(err)   

        if (hasattr(err, 'reason')):
            if err.reason == "[{'message': 'Rate limit exceeded', 'code': 88}]":
                return


def aggressive_management(api, config):
    """Aggressive management unfollows any followers until rate limit is hit that aren't following back"""

    limit_hit = False
    unfollowed_count = 0
    err_count = 0

    try:
        for page in tweepy.Cursor(api.friends, count = 100).pages():  
            if limit_hit is False:      
                user_ids = [user.id for user in page]

                for user in api._lookup_friendships(user_ids):
                    try:
                        if (unfollowed_count > config.follower_management['max_unfollows']):
                            limit_hit = True
                            break

                        if not user.is_followed_by:
                            api.destroy_friendship(user.id)
                            unfollowed_count += 1

                    except (tweepy.error.TweepError, IndexError) as err:
                        err_count += 1
                        logging.error(err)   

                        if (hasattr(err, 'reason')):
                            if err.reason == "[{'message': 'Rate limit exceeded', 'code': 88}]":
                                limit_hit = True
                                break 

                        continue

    except (tweepy.error.TweepError, IndexError) as err:
        err_count += 1
        logging.error(err)   

        if (hasattr(err, 'reason')):
            if err.reason == "[{'message': 'Rate limit exceeded', 'code': 88}]":
                limit_hit = True

    logging.info("Finished. %d unfollowed, %d errors." % (unfollowed_count, err_count))


def passive_management(api, config, following, following_back):
    """Passive management unfollows any followers who haven't tweeted within the inactivity date set in config"""
    """This method also allows prevention of followers being unfollowed via config"""

    unfollowed_count = 0
    err_count = 0

    inactivityDate = datetime.date.today() - datetime.timedelta(days = config.follower_management['inactivity_period'])

    for follower in following:
        try:
            if config.follower_management['remove_followers'] is False and follower in following_back:
                continue

            if (unfollowed_count < config.follower_management['max_unfollows']):
                lastTweet = api.user_timeline(follower, count = 1)
                lastTweetDate = lastTweet[0].created_at.date()

                if lastTweetDate < inactivityDate:                
                        api.destroy_friendship(follower)
                        unfollowed_count += 1
                        logging.info("Unfollowed: %d" % (follower))
                        continue

        except (tweepy.error.TweepError, IndexError) as err:
            err_count += 1
            logging.error(err)   

            if (hasattr(err, 'reason')):
                if err.reason == "[{'message': 'Rate limit exceeded', 'code': 88}]":
                    break 

            continue

    logging.info("Finished. %d unfollowed, %d errors." % (unfollowed_count, err_count))
