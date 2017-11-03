#!/usr/bin/env python3

import argparse
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
        return r.json

    def send_message(self, user_id, text):
        return self.method('sendMessage', {'chat_id': user_id,
                                           'text': text})

