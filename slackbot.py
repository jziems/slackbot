import os
import time
from slackclient import SlackClient
import json
import logging
import sys
sys.path.append('plugins')
from plugins import plugins

class slackbot:

  def __init__(self, loglevel=None):
    try:
      homedir = os.path.expanduser('~')
      with open(homedir+'/.slackbot', 'r') as fin:
        self.cfg = json.load(fin)
        for k,v in self.cfg.items():
          setattr(self, k, v)
    except:
      raise
    try:
      if loglevel:
        self.setloglevel(loglevel)
      else:
        self.setloglevel(logging.CRITICAL)
      self.slack_client = SlackClient(self.SLACK_BOT_TOKEN)
      self.slack_client.rtm_connect()
    except:
      raise

  def __del__(self):
    self._save()

  def setloglevel(self, loglevel):
    try:
      self.logger = logging.getlogger(self.__name__)
      self.logger.setLevel(loglevel)
      sh = logging.StreamHandler()
      sh.setLevel(loglevel)
      formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
      sh.setFormatter(formatter)
      self.logger.addHandler(sh)
    except:
      raise

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

    typing = 0

    while True:
      try:
        msg = self.slack_client.rtm_read()
        if msg:
          if msg[0]['type'] == 'message':
            if not 'bot_id' in msg[0].keys() or msg[0]['bot_id'] != self.BOT_ID:
              if 'text' in msg[0].keys():
                if msg[0]['text'].split(' ')[0] == '<@' + self.BOT_ID + '>':
                  cmd=msg[0]['text'].split(' ')[1]
                else:
                  cmd=msg[0]['text'].split(' ')[0]
                  if cmd in self.bot_commands():
                    try:
                      command = getattr(self.plugins, cmd)
                      self.post_message(channel=msg[0]['channel'], text=command())
                    except Exception as e:
                      self.logger.debug(str(e))
                  else:
                    self.logger.debug("Not a command: %s" % (cmd))
          elif msg[0]['type'] == 'user_typing':
            if typing == 3:
              self.post_message(channel=msg[0]['channel'], text='Shhh... <@'+msg[0]['user']+'> is typing something...')
              typing=0
            else:
              typing+=1
          elif msg[0]['type'] == 'presence_change' and msg[0]['presence'] == 'active':
            self.logger.debug("%s is now active." % (msg[0]['user']))

        time.sleep(self.READ_WEBSOCKET_DELAY)

      except:
        raise

  def post_message(self, channel=None, text=None, attachment=None, as_user=True):
    try:
      self.slack_client.api_call("chat.postMessage", channel=channel, text=text, attachments=attachment, as_user=as_user)
    except:
      raise

  def list_channels(self):
    c=[]
    try:
      c=self.slack_client.api_call("channels.list")
      return c['channels']
    except:
      raise
