# Retweet Bot try/except logic decorator to gracefully handle rate limit errors

import tweepy
import logging

def log_errors(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except tweepy.RateLimitError as e:
            logging.error("Hit rate limit, breaking out of current process.")
            raise e
        except Exception as e:
            logging.exception(e)
    return wrapper