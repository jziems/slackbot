#!/usr/bin/env python

import os
import slackbot
import logging

if __name__ == '__main__':
    try:
        bot = slackbot.Slackbot(os.path.expanduser('~') + '/.slackbot')
        bot.setloglevel(logging.DEBUG)
        bot.start()
    except KeyboardInterrupt:
        exit(0)
