# TgFeed

Tired of the endless switching between channels in Telegram? Missing a single common feed? Tired of advertising in channels?

With this simple Telegram Bot, you can combine all your channels into a single feed, and remove advertising posts from it.

Specify the channels you are interested in, and enjoy the feed without ads!


To launch:

1. Get app_id and app_hash using https://core.telegram.org/api/obtaining_api_id

2. Put the received values in .env-heil

3. Create a feed channel and a channel for ads, specify them in the file `config.py`

4. Load the bot using docker-compose: `docker-compose up --build bot`
