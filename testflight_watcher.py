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
FULL_TEXT_VN = "Bản beta này đã đầy."


def watch(watch_ids: list[str], callback, notify_full=False, loop=True, sleep_time=300):
    while True:
        for id in watch_ids:
            # get state
            try:
                req = requests.get(TESTFLIGHT_URL.format(id), headers={"Accept-Language": "en,en-us"})
                page = html.fromstring(req.text)
                if len(page.xpath(XPATH_STATUS)) == 0:
                    print("Invalid ID:", id)
                    continue
                free_slots = page.xpath(XPATH_STATUS)[0] != FULL_TEXT
                if free_slots or notify_full:
                    if len(re.findall(TITLE_REGEX, page.xpath(XPATH_TITLE)[0])) > 0:
                        app_name = re.findall(TITLE_REGEX, page.xpath(XPATH_TITLE)[0])[0]
                    else:
                        app_name = page.xpath(XPATH_TITLE)[0]
                    callback(id, free_slots, app_name)

            except Exception as e:
                print("An error occured:", e)

        if not loop:
            break
        sleep(sleep_time)

