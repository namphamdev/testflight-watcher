#!/usr/bin/env python3

import testflight_watcher
import requests
import sys
import os


CHAT_ID = os.environ['CHAT_ID']
TRACKERS = os.environ['TRACKERS']
BOT_TOKEN = os.environ['BOT_TOKEN']
BOT_URL = "https://api.telegram.org/bot{}/sendMessage".format(BOT_TOKEN)
MSG_NO_FULL = "TestFlight slots for <b>{}</b> beta are now available! \
<a href='{}'>Download now</a>"
MSG_FULL = "<b>{}</b> beta program on TestFlight is now full"

def send_notification(tf_id, free_slots, title):
    dl_url = testflight_watcher.TESTFLIGHT_URL.format(tf_id)
    if free_slots:
        message = MSG_NO_FULL.format(title, dl_url)
    else:
        message = MSG_FULL.format(title)
    requests.get(
        BOT_URL, params={"chat_id": CHAT_ID, "text": message, "parse_mode": "html", "disable_web_page_preview": "true"}
    )


testflight_watcher.watch(TRACKERS.split(","), send_notification)
