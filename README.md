# Notify Send Telegram

![NST Logo](logo-small.jpg)

Send server/desktop notifications to Telegram. Can be used as reminder with cron, log monitor (see `syslog-monitor.sh` for example), update notifier, etc.

## Usage

```
usage: notify-send-telegram.py [options] SUMMARY [BODY]

positional arguments:
  SUMMARY               Notification title, for example 'New mail'
  BODY                  Text of notification, multi-line supported. If BODY
                        isn't set, just the SUMMARY is sent

optional arguments:
  -h, --help            show this help message and exit
  -n, --silent          send notification with no sound
  -r chat_id, --recipient chat_id
                        telegram chat_id (user_id) to send notification
  -t TOKEN, --token TOKEN
                        set telegram bot token to use
```

Example:

`./notify-send-telegram.py -r YOUR_USER_ID -t YOUR_BOT_TOKEN 'New mail' 'Title: Hello world'`

## License

MIT