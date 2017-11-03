#!/usr/bin/env python3

import html # for escaping html codes

try:
    import requests
except ImportError:
    print("Module 'requests' isn't installed")
    exit(1)

class Telegram(object):
    def __init__(self, api_token):
        self.api_url = 'https://api.telegram.org/bot{}/'.format(api_token)
    
    def method(self, method_name, data):
        r = requests.post(self.api_url + method_name, data=data)
        return r

    def send_message(self, user_id, text, disable_notification=False):
        return self.method('sendMessage', {'chat_id': user_id,
                                           'text': text,
                                           'disable_notification': disable_notification,
                                           'parse_mode': 'HTML'})

if __name__ == '__main__':
    import argparse
    '''
        Args parser
    '''
    parser = argparse.ArgumentParser(usage='%(prog)s [options] SUMMARY [BODY]')
    
    parser.add_argument("SUMMARY", help="Notification title, for example 'New mail'")
    parser.add_argument("BODY", help="Text of notification, multi-line supported. If BODY isn't set, just the SUMMARY is sent", default="", nargs='?')
    
    parser.add_argument("-n", "--silent", help="send notification with no sound", default=False, action='store_true')
    parser.add_argument("-r", "--recipient", metavar='chat_id', help="telegram chat_id (user_id) to send notification", type=int, required=True)
    parser.add_argument("-t", "--token", help="set telegram bot token to use", type=str, required=True)
    options = parser.parse_args()
    
    sender = Telegram(options.token)
    summary = html.escape(options.SUMMARY).replace('\\n', '\n')
    body = html.escape(options.BODY).replace('\\n', '\n')
    text = '<b>'+summary+'</b>\n'+body
    sender.send_message(options.recipient, text, options.silent)
