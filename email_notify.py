#!/usr/bin/env python3

from argparse import ArgumentParser
from email.message import EmailMessage
from smtplib import SMTP_SSL

import testflight_watcher


def email_notifier(email: str, password: str, receivers: list[str]):
    def callback(id: str, free_slots: bool, app_name: str):
        print(f"{app_name} ({id}): {free_slots}")

        if not free_slots:
            return

        server = SMTP_SSL("smtp.gmail.com", 465)
        server.ehlo()
        server.login(email, password)

        for receiver in receivers:
            msg = EmailMessage()
            msg["From"] = f"TestFlight Watcher <{email}>"
            msg["Subject"] = f"Beta for {app_name} available!"
            msg.set_content(testflight_watcher.TESTFLIGHT_URL.format(id))
            msg["To"] = receiver
            try:
                server.send_message(msg)
            except Exception as e:
                print("Error sending email:", e)

    return callback


if __name__ == "__main__":
    parser = ArgumentParser()

    parser.add_argument("email", help="the sender email address")
    parser.add_argument("password", help="the password to the email account")
    parser.add_argument(
        "-r",
        dest="receiver",
        metavar="email",
        action="append",
        help="the receivers email address, can be used multiple times (default is same as sender)",
    )
    parser.add_argument("ID", action="extend", nargs="+", help="the IDs to watch")

    args = parser.parse_args()

    if args.receiver is None:
        args.receiver = [args.email]

    testflight_watcher.watch(args.ID, email_notifier(args.email, args.password, args.receiver), notify_full=False, loop=False)
