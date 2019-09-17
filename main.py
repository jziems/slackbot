#!/usr/bin/env python

import os,sys
from slackbot.slackbot import Slackbot
import logging
# import threading
from time import sleep

def main():

    homedir = os.path.expanduser('~')
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    try:
        bot = Slackbot(homedir+'/.slackbot')
        # thr = threading.Thread(target=bot.read_forever)
        # thr.setDaemon(True)
        # thr.start()
        print("Channels: {}".format(bot.list_channels()))
        bot.post_message(text='hello', channel='bot_debug')
        while True:
            sleep(1)
    except Exception as e:
        logging.exception(e)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)
