#!/usr/bin/env python3

##
# Notify Send Telegram (github.com/MikeWent/notify-send-telegram)
# Released under the MIT license
##

# SETTINGS
# ~ stands for user homedir
CONFIG_PATH = '~/.config/notify-send-telegram/'
CONFIG_FILE = 'config'

import html
import_errors = 0
try:
    import requests
except ImportError:
    print("Module 'requests' isn't installed")
    import_errors += 1
try:
    import configparser
except ImportError:
    print("Module 'configparser' isn't installed")
    import_errors += 1
if import_errors > 0:
    exit(1)

class Telegram(object):
    def __init__(self, api_token):
        self.api_url = "https://api.telegram.org/bot{}/".format(api_token)
    
    def method(self, method_name, data):
        r = requests.post(self.api_url + method_name, data=data)
        return r.json()

    def send_message(self, user_id, text, disable_notification=False):
        return self.method("sendMessage", {"chat_id": user_id,
                                           "text": text,
                                           "disable_notification": disable_notification,
                                           "parse_mode": "HTML"})

if not __name__ == "__main__":
    exit("notify-send-telegram.py can only run as a standalone script")

from os.path import expanduser
from os import makedirs
import argparse

parser = argparse.ArgumentParser(usage="%(prog)s [options] SUMMARY [BODY]")
parser.add_argument("SUMMARY", help="Notification title, for example 'New mail'")
parser.add_argument("BODY", help="Text of notification, multi-line supported. If BODY isn't set, just the SUMMARY is sent", default="", nargs="?")
parser.add_argument("-n", "--silent", help="send notification with no sound", default=False, action="store_true")
parser.add_argument("-r", "--recipient", metavar="chat_id", help="telegram chat_id (user_id) to send notification", type=int)
parser.add_argument("-t", "--token", help="set telegram bot token to use", type=str)
parser.add_argument("-s", "--stdin", help="read notification BODY from stdin", action="store_true")
parser.add_argument("-z", "--save", help="save recipient & token to config file and use them as defaults in future", action="store_true")
parser.add_argument("-w", "--raw", help="do not escape HTML tags in body (use with caution)", action="store_true")
options = parser.parse_args()

config_full_path = expanduser(CONFIG_PATH) + CONFIG_FILE
config = configparser.ConfigParser()
config.read(config_full_path)
if len(config.sections()) == 0:
    # default values if config file was empty
    config["default"] = {"token": "", "recipient": ""}
    config_was_empty = True
else:
    config_was_empty = False

if options.token:
    token_to_use = options.token
    config["default"]["token"] = options.token
elif config["default"]["token"]:
    token_to_use = config["default"]["token"]
else:
    print("No token specified. Set it via -t,--token or in config file")
    exit(1)    

if options.recipient:
    recipient_to_use = options.recipient
    config["default"]["recipient"] = str(options.recipient)
elif config["default"]["recipient"]:
    recipient_to_use = config["default"]["recipient"]
else:
    print("No recipient specified. Set it via -r,--recipient or in config file")
    exit(1)

if options.stdin:
    from sys import stdin
    body = stdin.read()
else:
    body = options.BODY

# init bot
bot = Telegram(token_to_use)

summary = html.escape(options.SUMMARY).replace("\\n", "\n")
if options.raw:
    # do not escape, just replace newlines
    body = body.replace("\\n", "\n")
else:
    body = html.escape(body).replace("\\n", "\n")

# construct message
text = "<b>{}</b>\n{}".format(summary, body)

request_result = bot.send_message(recipient_to_use, text, options.silent)
if not request_result["ok"]:
    print("Telegram API returned an error!")
    print(request_result["error_code"], request_result["description"])
    exit(1)

if options.save or config_was_empty:
    # create directory for user config
    makedirs(config_full_path[0:-len(CONFIG_FILE)])
    with open(config_full_path, "w") as f:
        config.write(f)
        print("Current configuration saved in", config_full_path)
