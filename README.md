# Messenger Techno Bot

Facebook Messenger bot intended to send daily dose of quality techno.

## Prerequirements

- Python 3.7
- Google Chrome 81.0
- Chromium Webdriver (<https://chromedriver.chromium.org/downloads>)
- Selenium (install with `pip`)

## Build & Run

1. Navigate to project folder
2. Run `python3 messenger_bot.py --setup`.
3. Fill in your Facebook username (email) and password in `my)secrets.py` file.
4. Run `python3 messenger_bot.py --add-subscriber` to add your subcribers (example subscriber: <https://www.messenger.com/t/example_link>).
5. Run `python3 messenger_bot.py` (in case you have `python3` command as your python 3.7 interpreter)
