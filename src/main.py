#!/usr/bin/env python
# -*- coding: utf-8 -*-

import retweet_core
import hash_management
import follower_management
import config
import logging
import asyncio


async def main():
    CONFIG = config.Config()
    logging.basicConfig(level = logging.getLevelName(CONFIG.general['log_level']))
    logging.info("Bot started")

    API = retweet_core.api_login(CONFIG.twitter_keys)

    hash_management.create_hashes_folder()

    retweet_task = asyncio.create_task(retweet_core.retweet(API, CONFIG.query_objects))
    follower_task = asyncio.create_task(follower_management.manage_followers(API, CONFIG))
    await asyncio.gather(retweet_task, follower_task)

if __name__ == '__main__':
    asyncio.run(main())