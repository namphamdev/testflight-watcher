#!/usr/bin/env python3

import requests
from lxml import html
import re
from time import sleep


XPATH_STATUS = '//*[@class="beta-status"]/span/text()'
XPATH_TITLE = "/html/head/title/text()"
TITLE_REGEX = r"Join the (.+) beta - TestFlight - Apple"
TESTFLIGHT_URL = "https://testflight.apple.com/join/{}"
FULL_TEXT = "This beta is full."


def watch(watch_ids: list[str], callback, notify_full=True, loop=True, sleep_time=900):
    while True:
        for id in watch_ids:

            # get state
            try:
                req = requests.get(TESTFLIGHT_URL.format(id), headers={"Accept-Language": "en-us"})
                page = html.fromstring(req.text)
                free_slots = page.xpath(XPATH_STATUS)[0] != FULL_TEXT
                if free_slots or notify_full:
                    app_name = re.findall(TITLE_REGEX, page.xpath(XPATH_TITLE)[0])[0]
                    callback(id, free_slots, app_name)

            except Exception as e:
                print("An error occured:", e)

        if not loop:
            break
        sleep(sleep_time)

