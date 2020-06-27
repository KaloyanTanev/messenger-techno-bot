import sys
import argparse
import os
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from time import sleep

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

def create_file(path, data):
    if not os.path.isfile(path):
        with open(path, "w") as f:
            f.write(data)
            f.close()

def ensure_file_exists(path):
    if not os.path.isfile(path):
        raise RuntimeError(os.path.basename(path) + " not found. Run setup?")

def ensure_variable_exists(f, var):
    if (not hasattr(f, var)) or getattr(f, var) == "":
        raise RuntimeError("{0} not found or empty in {1}.py".format(var, f.__name__))

def add_option(opt):
    print ("opa")
    opts[opt] = True


def setup():
    create_file(os.path.join(CURR_DIR, "subscribers.txt"), "")
    create_file(os.path.join(CURR_DIR, "my_secrets.py"), 'username = ""\npassword = ""')

def add_subscriber(msngr_link):
    ensure_file_exists(os.path.join(CURR_DIR, "subscribers.txt"))
    to_write = msngr_link + "\n"
    with open('subscribers.txt', "a") as f:
        f.write(to_write)
        f.flush()
        os.fsync(f.fileno())
        f.close()

def start():
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

    track_link = input("Track link: ")

    custom_msg = input("Custom messеge: ")

    donations = input("Add donations(y/n)?: ")

    unsubscribe = input("Add unsubscribe(y/n)?: ")

    if(donations == "y"): opts['donations'] = True
    if(unsubscribe == "y"): opts['unsubscribe'] = True

    msg = ["Your daily dose of quality techno.", track_link, custom_msg]

    bot = MessengerBot()
    bot.login(my_secrets.username, my_secrets.password)
    # bot.send_msg("https://www.messenger.com/t/987811307976917", msg, opts)
    bot.send_multiple_msgs(subscribers, msg, opts)
    bot.quit()

# CLI
parser = argparse.ArgumentParser(description="Messenger Bot CLI")
parser.add_argument("run",
                    action="store_true",
                    help="run the bot")
parser.add_argument("--setup",
                    action="store_true",
                    help="setup local files")
parser.add_argument("--add-subscriber",
                    action="store",
                    nargs=1,
                    metavar=("LINK"),
                    help="add new subscriber")
parser.add_argument("-d", "--donations",
                    action="store_true",
                    help="setup local files")
parser.add_argument("-u", "--unsubscribe",
                    action="store_true",
                    help="setup local files")

if not sys.argv[1:]:
    # os.path.dirname(os.path.abspath(__file__))
    start()

args = parser.parse_args()
args = list(filter(lambda i: i[1], vars(args).items()))

for k, v in args:
    {
        "add_subscriber": lambda v: add_subscriber(*v),
        "setup": lambda v: setup(),
        "donations": lambda v: add_option('donations'),
        "unsubscribe": lambda v: add_option('unsubscribe'),
        "run": lambda v: start(),
    }[k](v)
