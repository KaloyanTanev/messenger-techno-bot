import sys
import argparse
import os
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from time import sleep

from secrets import username, password

with open('subscribers.txt') as f:
    subscribers = f.read().splitlines()

opts = {}

class MessengerBot():
    def __init__(self):
        self.driver = webdriver.Chrome(ChromeDriverManager().install())

    def login(self):
        self.driver.get('https://www.messenger.com/')

        sleep(2)

        email_in = self.driver.find_element_by_xpath('//*[@id="email"]')
        email_in.send_keys(username)

        pw_in = self.driver.find_element_by_xpath('//*[@id="pass"]')
        pw_in.send_keys(password)

        login_btn = self.driver.find_element_by_xpath('//*[@id="loginbutton"]')
        login_btn.click()

    def send_msg(self, url, msg, opts = {}):
        self.driver.get(url)

        sleep(1)

        msg_in = self.driver.switch_to.active_element
        for line in msg:
            msg_in.send_keys(line)
            msg_in.send_keys(Keys.SHIFT, Keys.ENTER)
            msg_in.send_keys(Keys.SHIFT, Keys.ENTER)
        
        if(opts.get('donations')): self.add_donations(msg_in)
        if(opts.get('unsubscribe')): self.add_unsubscribe(msg_in)

        msg_in.send_keys(Keys.ENTER)

        sleep(1)

    def send_multiple_msgs(self, subscribers, msg, opts = {}):
        print(subscribers)
        for subscriber in subscribers:
            self.send_msg(subscriber, msg, opts)

    def add_donations(self, msg_in):
        msg_in.send_keys("-----------------")
        msg_in.send_keys(Keys.SHIFT, Keys.ENTER)
        msg_in.send_keys("For donations:")
        msg_in.send_keys(Keys.SHIFT, Keys.ENTER)
        msg_in.send_keys("EUR: NL47ABNA0826676685")
        msg_in.send_keys(Keys.SHIFT, Keys.ENTER)
        msg_in.send_keys("BGN: BG97RZBB91551005263064")
        msg_in.send_keys(Keys.SHIFT, Keys.ENTER)
        msg_in.send_keys("All other fiat: GB17REVO00997059115935")
        msg_in.send_keys(Keys.SHIFT, Keys.ENTER)
        msg_in.send_keys("BTC: 157vHYi4WnUQVpT2rDqQgBJeidLjjUn8Lf")
        msg_in.send_keys(Keys.SHIFT, Keys.ENTER)
        msg_in.send_keys("ETH: 0x4D23936374036f1b459D4090C9D89f504809E04d")
        msg_in.send_keys(Keys.SHIFT, Keys.ENTER)

    def add_unsubscribe(self, msg_in):
        msg_in.send_keys("-----------------")
        msg_in.send_keys(Keys.SHIFT, Keys.ENTER)
        msg_in.send_keys("To unsubscribe, react with (n) on the messege:")

    def quit(self):
        self.driver.quit()

def add_subscriber(msngr_link):
    to_write = "\n" + msngr_link
    with open('subscribers.txt', "a") as f:
        f.write(to_write)
        f.flush()
        os.fsync(f.fileno())
        f.close()

# Actual bot

track_link = input("Track link: ")

custom_msg = input("Custom messеge: ")

donations = input("Add donations(y/n)?: ")

unsubscribe = input("Add unsubscribe(y/n)?: ")

if(donations == "y"): opts['donations'] = True
if(unsubscribe == "y"): opts['unsubscribe'] = True

msg = ["Your daily dose of quality techno.", track_link, custom_msg]

bot = MessengerBot()
bot.login()
# bot.send_msg("https://www.messenger.com/t/987811307976917", msg, opts)
bot.send_multiple_msgs(subscribers, msg, opts)
bot.quit()