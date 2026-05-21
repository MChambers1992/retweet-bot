# Retweet Bot

> **This project is no longer maintained and has been archived.**
>
> Following Elon Musk's acquisition of Twitter (now rebranded as X) in October 2022, the platform introduced severe restrictions to its developer API. The free tier was effectively rendered non-functional for automation use cases, requiring a paid subscription for any meaningful API access. As a result, this project has not been in active development since the acquisition and is unlikely to work for the vast majority of users without a paid X API plan.
>
> The repository is left here for historical reference only. No further updates, bug fixes, or support will be provided.

---

![Python 3.6](https://img.shields.io/badge/python-3.6-green.svg "Python 3.6")
![Archived](https://img.shields.io/badge/status-archived-red.svg)

This script retweets certain tweets with a specific search query and can use parameters defined in the config file to perform additional actions. To limit Twitter API requests it uses a savepoint for each configured query object, tracking the last retweeted tweet ID per search query.

Originally built against Twitter API v1.1.

## Why this project was archived

When Elon Musk acquired Twitter in October 2022 and rebranded it to X, the platform's developer API underwent significant changes:

- **Free tier restrictions**: The free API tier was stripped of nearly all functionality, making read/write automation effectively impossible without payment.
- **Paid tier costs**: Basic API access sufficient for a bot like this requires a paid subscription, pricing out hobbyist and open-source use cases.
- **Policy changes**: Automated posting and retweet behaviour became subject to increasingly strict and unpredictable enforcement.

This project was built for the original Twitter developer ecosystem and is not worth maintaining under the current X API model.

---

## Legacy documentation

The following is preserved for historical reference.

### Requirements

Python 3.4 or later. Packages available at http://www.python.org/getit/

### Dependencies

```
pip install -r requirements.txt
```

### Quick start

Create a copy of `config/config.SAMPLE.json` and rename it to `config.json`, then:

- Define your `query_objects` in `config.json`
- Add your `twitter_keys` to `config.json` — credentials were obtained from https://apps.twitter.com/

Run with:

```
python src/main.py
```

### Cron job

```
30 * * * * [your-user-here] cd ~/retweet-bot/src/ && python3 main.py >> ~/retweet-bot/twitter_bot.txt
```

See https://crontab.guru for cron interval syntax.

### Compatibility

Compatible with Python 3.x, tested on Python 3.6.
