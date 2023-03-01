# Retweet Bot filtering module which handles filtering timeline and statuses based on query_objects

import logging
from better_profanity import profanity

profanity.load_censor_words()

def filter_status(tweet, list_of_previous_tweet_ids, max_hashtags, max_urls, filter_mentions, filter_media, filter_profanity, require_media):
    """Performs filtering logic on each tweet being processed"""
    filtered_out = []

    if not tweet.retweeted:

        if filter_profanity and profanity.contains_profanity(tweet.text):
            filtered_out.append('profanity')

        if filter_media and tweet.entities['media'] is not None:
            filtered_out.append('contains media')
        
        if require_media and 'media' in tweet.entities and tweet.entities['media'][0] is None:
            filtered_out.append('no media')

        if filter_mentions and len(tweet.entities['user_mentions']) > 0:
            filtered_out.append('user mention')
            
        if max_hashtags < len(tweet.entities['hashtags']):
            filtered_out.append('too many hashtags')

        if max_urls < len(tweet.entities['urls']):
            filtered_out.append('too many URLs')

    if filtered_out:
        logging.info(f'Filtered tweet (ID {tweet.id}) due to: {", ".join(filtered_out)}\n')
        return False
    
    return True
    
def filter_timeline(timeline, query_object):
    """Performs global filtering on the timeline object returned by Tweepy"""

    timeline = filter(lambda status: not any(word in status.text.split()
                                                for word in query_object['word_blacklist']), timeline)
    timeline = filter(
        lambda status: status.author.screen_name not in query_object['user_blacklist'], timeline)
    
    timeline = list(timeline)
    timeline.reverse()

    return timeline