import sys
import argparse
import os
import datetime
import csv
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from time import sleep,strftime,gmtime

CURR_DIR = os.path.dirname(os.path.abspath(__file__))

opts = {}

class MessengerBot():
    def __init__(self):
        self.driver = webdriver.Chrome(ChromeDriverManager().install())

    def login(self, username, password):
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

        sleep(3)

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

def create_file(path, data):
    if not os.path.isfile(path):
        with open(path, "w") as f:
            f.write(data)
            f.close()

def append_to_file(path, data):
    with open(path, "a") as f:
        f.write(data)
        f.flush()
        os.fsync(f.fileno())
        f.close()

def write_to_file(path, data):
    with open(path, "w") as f:
        f.write(data)
        f.flush()
        os.fsync(f.fileno())
        f.close()

def ensure_file_exists(path):
    if not os.path.isfile(path):
        raise RuntimeError(os.path.basename(path) + " not found. Run setup?")

def ensure_variable_exists(f, var):
    if (not hasattr(f, var)) or getattr(f, var) == "":
        error = "{0} not found or empty in {1}.py".format(var, f.__name__)
        raise RuntimeError(error)

def setup():
    create_file(os.path.join(CURR_DIR, "subscribers.txt"), "")
    create_file(os.path.join(CURR_DIR, "history.csv"), "")
    append_to_file("history.csv", "users,link,UTC_datetime\n")
    create_file(os.path.join(CURR_DIR, "my_secrets.py"), '')
    append_to_file("my_secrets.py", 'username = ""\npassword = ""')

def add_subscriber(msngr_link):
    ensure_file_exists(os.path.join(CURR_DIR, "subscribers.txt"))
    append_to_file("subscribers.txt", msngr_link + "\n")

def enqueue(track, msg):
    append_to_file("queue.csv", track + "," + msg + "\n")

def dequeue():
    with open("queue.txt", 'r') as fout: 
        head, tail = fout.read().split('\n', 1)
        track, custom_msg = head.split(',', 1)
        # send_track(track, custom_msg)
    write_to_file("queue.txt", tail)

def validate(link):
    with open("history.csv", 'r') as data: 
        reader = csv.DictReader(data)
        for line in reader: 
            track_id = strip_url(line['link'])
            if (("youtube.com" or "youtu.be" or "open.spotify.com") and track_id in link):
                raise RuntimeError("{0} was already sent on {1}".format(line['link'], line['UTC_datetime']))

def strip_url(url):
    if url.startswith("https://www.youtube.com/watch?v="):
        url = url[len("https://www.youtube.com/watch?v="):]
    if url.startswith("https://youtu.be/"):
        url = url[len("https://youtu.be/"):]
    if url.startswith("https://open.spotify.com/track/"):
        url = url[len("https://open.spotify.com/track/"):]
    return url

def update_history(link, subscribers):
    dt_now = strftime("%Y-%m-%dT%H:%M:%S+00:00", gmtime())
    data = str(len(subscribers)) + "," + link + "," + dt_now + "\n"
    append_to_file('history.csv', data)

def start():

    track_link = input("Track link: ")

    validate(track_link)

    custom_msg = input("Custom messеge: ")

    donations = input("Add donations(y/n)?: ")

    unsubscribe = input("Add unsubscribe(y/n)?: ")

    if(donations == "y"): opts['donations'] = True
    if(unsubscribe == "y"): opts['unsubscribe'] = True

    send_track(track_link, custom_msg, opts)


def send_track(track, custom_msg, opts = {}):
    ensure_file_exists(os.path.join(CURR_DIR, "subscribers.txt"))
    ensure_file_exists(os.path.join(CURR_DIR, "my_secrets.py"))

    # Consider better solution
    try:
        import my_secrets
    except ImportError:
        RuntimeError("my_secrets.py not found. Run setup")

    ensure_variable_exists(my_secrets, 'username')
    ensure_variable_exists(my_secrets, 'password')

    with open('subscribers.txt') as f:
        subscribers = f.read().splitlines()

    msg = ["Your daily dose of quality techno.", track, custom_msg]
    
    bot = MessengerBot()
    bot.login(my_secrets.username, my_secrets.password)
    # bot.send_msg("https://www.messenger.com/t/987811307976917", msg, opts)
    bot.send_multiple_msgs(subscribers, msg, opts)
    update_history(track, subscribers)
    bot.quit()

def test():
    print("CHECK")

# CLI
parser = argparse.ArgumentParser(description="Messenger Bot CLI")
parser.add_argument("--setup",
                    action="store_true",
                    help="setup local files")
parser.add_argument("--test",
                    action="store_true",
                    help="test")
parser.add_argument("--add-subscriber",
                    action="store",
                    nargs=1,
                    metavar=("LINK"),
                    help="add new subscriber")
parser.add_argument("--enqueue",
                    action="store",
                    nargs=2,
                    metavar=("TRACK", "MSG"),
                    help="enqueue a track")
parser.add_argument("--dequeue",
                    action="store_true",
                    help="dequeue a track")

if not sys.argv[1:]:    
    start()

args = parser.parse_args()
args = list(filter(lambda i: i[1], vars(args).items()))

for k, v in args:
    {
        "add_subscriber": lambda v: add_subscriber(*v),
        "enqueue": lambda v: enqueue(*v),
        "dequeue": lambda v: dequeue(),
        "test": lambda v: test(),
        "setup": lambda v: setup()
    }[k](v)
