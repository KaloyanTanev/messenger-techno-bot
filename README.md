# Messenger Techno Bot

Facebook Messenger bot intended to send daily dose of quality techno.

## Prerequisites

_Note: it is assumed you have `pip3` and not `pip` as your python 3.7 package manager._

- Python 3.7
- Google Chrome >81.0
- Selenium (`pip3 install selenium`)
- Chromium Webdriver (`pip3 install webdriver_manager`)

## Build & Run

_Note: it is assumed you have `python3` and not `python` as your python 3.7 interpreter._

1. Navigate to project folder
2. Run `python3 messenger_bot.py --setup`.
3. Fill in your Facebook username (email) and password in `my_secrets.py` file.
4. Run `python3 messenger_bot.py --add-subscriber` to add your subcribers (example subscriber: <https://www.messenger.com/t/example_link>).
5. Run `python3 messenger_bot.py`
