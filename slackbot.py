#!/usr/bin/env python

import os
import sys
import time
import json
import logging
import plugins
from dbox import dbox
from slackclient import SlackClient

__package__ = 'slackbot'

class slackbot:

  def __init__(self):
    try:
      homedir = os.path.expanduser('~')
      self.logger = logging.getLogger('slackbot')
      self.plugins = plugins.plugins()
      with open(homedir+'/.slackbot', 'r') as fin:
        self.cfg = json.load(fin)
      for k,v in self.cfg.items():
        setattr(self, k, v)
      if not hasattr(self, 'SLACK_BOT_TOKEN'):
        self.SLACK_BOT_TOKEN = raw_input("Please enter slack bot token: ")
      if not hasattr(self, 'BOT_ID'):
        self.BOT_ID = raw_input("Please enter bot id: ")
      if not hasattr(self, 'READ_WEBSOCKET_DELAY'):
        self.READ_WEBSOCKET_DELAY = 1
      self.slack_client = SlackClient(self.SLACK_BOT_TOKEN)
      self.slack_client.rtm_connect()
    except Exception as e:
      self.logger.exception(e)

  def _parse_exe(self, cmd, args=None):
    pass

  def _presence_change(self):
    pass

  def _dispatch(self, message):
    if message['type'] == 'message':
      if not 'bot_id' in message.keys() or message['bot_id'] != self.BOT_ID:
        if 'text' in message.keys():
          cmd_split = message['text'].split(' ')
          if cmd_split[0] == '<@' + self.BOT_ID + '>':
            cmd = cmd_split[1]
            if len(cmd_split) > 2:
              args = ', '.join(cmd_split[2:])
            else:
              args = None
          else:
            cmd = cmd_split[0]
            if len(cmd_split) > 1:
              args = ', '.join(cmd_split[1:])
            else:
              args = None
            if cmd in self.bot_commands():
              try:
                command = getattr(self.plugins, cmd)
                if args:
                  self.logger.debug("Command: %s args: %s" % (cmd, args))
                  ret = command(filepath=args)
                else:
                  self.logger.debug("Command: %s" % cmd)
                  ret = command()
                if hasattr(ret, 'binary'):
                  if ret.binary:
                    self.logger.debug("path to object: %s" % ret.path)
                    self.upload(channel=message['channel'], filename=ret.path)
                  else:
                    self.post_message(channel=message['channel'], text=ret)
                else:
                  self.post_message(channel=message['channel'], text="Unknown response from plugin.")
              except Exception as e:
                self.logger.exception(e)
                raise e
            else:
              self.logger.debug("Not a command: %s" % (cmd))
              self.post_message(channel=message['channel'], text="I didn't understand %s" % cmd)
    elif message['type'] == 'presence_change' and message['presence'] == 'active':
      self.logger.debug("%s is now active." % (message['user']))

  def __del__(self):
    self._save()

  def setloglevel(self, loglevel):
    try:
      self.logger.setLevel(loglevel)
    except Exception as e:
      self.logger.exception(e)

  def _save(self):
    config = dict()
    for x in dir(self):
      y = getattr(self, x)
      if isinstance(y, basestring):
        self.logger.debug("Attribute: {0} Value: {1}".format(x,y))
        config[x] = y
        with open('/home/joe/.slackbot', 'w') as fout:
          json.dump(config, fout, indent=4)
 
  def bot_commands(self):
    return self.plugins.__all__

  def read(self):

    while True:
      try:
        msg = self.slack_client.rtm_read()
        if len(msg) > 0:
          self.logger.debug("Message: %s" % msg)
          for message in msg:
            self._dispatch(message)
          time.sleep(self.READ_WEBSOCKET_DELAY)
      except Exception as e:
        self.logger.exception(e)

  def post_message(self, channel=None, text=None, attachment=None, as_user=True):
    try:
      self.slack_client.api_call('chat.postMessage', channel=channel, text=text, attachments=attachment, as_user=as_user)
    except Exception as e:
      self.logger.exception(e)

  def upload(self, channel=None, filename=None):
    try:
      name = os.path.basename(filename)
      with open(filename, 'rb') as fh:
        resp = self.slack_client.api_call('files.upload', channel=channel, title=name, filename=name, file=fh, as_user=True)
      self.logger.debug("Response from upload: %s" % resp)
      self.post_message(channel=channel, text=resp['file']['permalink'], as_user=True)
      if not resp['ok']:
        self.logger.debug("Response from upload: %s" % resp['error'])
    except Exception as e:
      self.logger.exception(e)

  def list_channels(self):
    try:
      c=self.slack_client.api_call("channels.list")
      return c['channels']
    except Exception as e:
      self.logger.exception(e)

def main():

  logger = logging.getLogger('slackbot')
  sh = logging.FileHandler(filename=os.path.basename(sys.argv[0]).split('.')[0] + '.log')
  logger.setLevel(logging.DEBUG)
  sh.setLevel(logging.DEBUG)
  formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
  sh.setFormatter(formatter)
  logger.addHandler(sh)

  try:
    bot = slackbot()
    bot.read()
  except Exception as e:
    logging.exception(e)

if __name__ == '__main__':
  try:
      main()
  except KeyboardInterrupt:
    sys.exit(0)
