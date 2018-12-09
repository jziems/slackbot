#!/usr/bin/env python

import os
import sys
from slackbot import slackbot
import logging

def main():

    logging.basicConfig(filename=os.path.basename(sys.argv[0]).split('.')[0] + '.log', level=logging.DEBUG, format='(%(message)s', )

    try:
      bot = slackbot()
      bot.read()
    except Exception as e:
      logging.exception(str(e))

if __name__ == '__main__':
  try:
      main()
  except KeyboardInterrupt:
    sys.exit(0)
