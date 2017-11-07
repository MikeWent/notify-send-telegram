#!/usr/bin/env python3

# SETTINGS
CONFIG_FILE = "notify-send-telegram.ini"

import html # for escaping html codes

try:
    import requests
except ImportError:
    print("Module 'requests' isn't installed")
    exit(1)

try:
    import configparser
except ImportError:
    print("Module 'configparser' isn't installed")
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

if __name__ == "__main__":
    import argparse
    """
        Args parser
    """
    parser = argparse.ArgumentParser(usage="%(prog)s [options] SUMMARY [BODY]")
    
    parser.add_argument("SUMMARY", help="Notification title, for example 'New mail'")
    parser.add_argument("BODY", help="Text of notification, multi-line supported. If BODY isn't set, just the SUMMARY is sent", default="", nargs="?")
    parser.add_argument("-n", "--silent", help="send notification with no sound", default=False, action="store_true")
    parser.add_argument("-r", "--recipient", metavar="chat_id", help="telegram chat_id (user_id) to send notification", type=int)
    parser.add_argument("-t", "--token", help="set telegram bot token to use", type=str)
    parser.add_argument("-z", "--save", help="save recipient & token to config file and use them as defaults in future", action="store_true")
    options = parser.parse_args()

    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)
    if len(config.sections()) == 0:
        # if empty config
        config["default"] = {"token": "",
                             "recipient": ""}
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

    # init bot
    bot = Telegram(token_to_use)
    # construct message
    summary = html.escape(options.SUMMARY).replace("\\n", "\n")
    body = html.escape(options.BODY).replace("\\n", "\n")
    text = "<b>"+summary+"</b>\n"+body
    request_result = bot.send_message(recipient_to_use, text, options.silent)
    if not request_result["ok"]:
        print("Telegram API returned an error!")
        print(request_result["error_code"], request_result["description"])
    
    if options.save or config_was_empty:
        with open(CONFIG_FILE, "w") as f:
            config.write(f)
            print("Current configuration saved in", CONFIG_FILE)
