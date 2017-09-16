#!/usr/bin/python

import os, sys, time
import datetime
from slackclient import SlackClient
import pygame.camera
import pygame.image
import dropbox
from PIL import Image
import requests
import json

class logger:

  def __init__(self):
    self.logfile="pythonbot.log"
    self.log=open(self.logfile, 'a')
    return None

  def write(self, message=None):
    self.log.write(str(datetime.datetime.now()) + ': ' + message + '\n')
    self.log.flush()

class pythonbot:

  def __init__(self):
    try:
      self.slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))
      self.BOT_ID=os.environ.get('BOT_ID')
      self.BOT_NAME = 'pythonbot'
      self.slack_client.rtm_connect()
      self._bot_commands=['take_upload_pic', 'hitme']
    except Exception, e:
      raise e
    return None

  def bot_commands(self):
    return self._bot_commands

  def read(self):
    try:
      return self.slack_client.rtm_read()
    except Exception, e:
      raise e

  def post_message(self, channel=None, text=None, attachment=None, as_user=True):
    try:
      self.slack_client.api_call("chat.postMessage", channel=channel, text=text, attachments=attachment, as_user=as_user)
    except Exception, e:
      raise e

  def list_channels(self):
    c=[]
    try:
      c=self.slack_client.api_call("channels.list")
    except Exception, e:
      raise e
    return c['channels']

  def db(self, filepath=None):
    try:
      db_token=os.environ.get('DROPBOX_TOKEN')
      dbx = dropbox.Dropbox(db_token)
      remotepath='/bmps/' + str(filepath.split("/")[-1])
      dbx.files_upload(open(filepath, 'rb'), remotepath, mode=dropbox.files.WriteMode.add, autorename=False, client_modified=None, mute=True)
      return dbx.sharing_create_shared_link(remotepath).url[0:-1]+'1'
    except Exception, e:
      raise e
    return None

  def snap(self, filepath=None):
    try:
      pygame.camera.init()
      cam = pygame.camera.Camera(pygame.camera.list_cameras()[0])
      cam.start()
      img = cam.get_image()
      cam.stop()
      pygame.image.save(img, filepath + ".bmp")
      pygame.camera.quit()
      im=Image.open(filepath + ".bmp")
      new_im=im.convert()
      new_im.save(filepath + ".jpg")
    except Exception, e:
      raise e
    return True

  def take_upload_pic(self, channel=None, text='An Image'):
    f="/tmp/photo-" + str(int(time.time()))
    try:
      self.snap(filepath=f)
      url=self.db(filepath=f + ".jpg")
      at=[]
      d={}
      d['title']="An Image"
      d['image_url']=url
      at.append(d)
      self.post_message(channel=channel, text=text, attachment=at)
    except Exception, e:
      raise e
    return None

  def hitme(self, channel=None):
    try:
      r=requests.get('http://api.icndb.com/jokes/random')
      q=json.loads(r.text)
      self.post_message(channel=channel, text=''.join(q['value']['joke']))
    except Exception, e:
      raise e
    return None

def daemonize():
  try:
    pid = os.fork()
    if pid > 0:
      # exit first parent
      sys.exit(0)
  except OSError as err:
    sys.stderr.write('_Fork #1 failed: {0}\n'.format(err))
    sys.exit(1)
  # decouple from parent environment
  os.chdir('/')
  os.setsid()
  os.umask(0)
  # do second fork
  try:
    pid = os.fork()
    if pid > 0:
      # exit from second parent
      sys.exit(0)
  except OSError as err:
    sys.stderr.write('_Fork #2 failed: {0}\n'.format(err))
    sys.exit(1)

  # redirect standard file descriptors
  sys.stdout.flush()
  sys.stderr.flush()
  si = open(os.devnull, 'r')
  so = open(os.devnull, 'w')
  se = open(os.devnull, 'w')
  os.dup2(si.fileno(), sys.stdin.fileno())
  os.dup2(so.fileno(), sys.stdout.fileno())
  os.dup2(se.fileno(), sys.stderr.fileno())
  main(os.getpid())

def main(pid=None):

  if pid == None:
    daemonize()
  else:
    with open("pythonbot.pid", 'w') as pidfile:
      pidfile.write(str(pid))
    log=logger()
    log.write("Starting....")

    READ_WEBSOCKET_DELAY = 1
    typing=0
    try:
      pb = pythonbot()
      log.write("Started.")

      log.write("Channel List:")
      for channel in pb.list_channels():
        log.write('\t' + channel['name'])

      while True:
        msg = pb.read()
  
        if msg:
          if msg[0]['type'] == 'message':
            if not 'bot_id' in msg[0].keys() or msg[0]['bot_id'] != pb.BOT_ID:
              if 'text' in msg[0].keys():
                if msg[0]['text'].split(' ')[0] == '<@' + pb.BOT_ID + '>':
                  cmd=msg[0]['text'].split(' ')[1]
                else:
                  cmd=msg[0]['text'].split(' ')[0]
                if cmd in pb.bot_commands():
                  try:
                    ret=eval('pb.' + cmd)(channel=msg[0]['channel'])
                  except Exception, e:
                    log.write(str(e))
                else:
                  log.write("Not a command: %s" % (cmd))
          elif msg[0]['type'] == 'user_typing':
            if typing == 3:
              pb.post_message(channel=msg[0]['channel'], text='Shhh... <@'+msg[0]['user']+'> is typing something...')
              typing=0
            else:
              typing+=1
          elif msg[0]['type'] == 'presence_change' and msg[0]['presence'] == 'active':
            log.write("%s is now active." % (msg[0]['user']))

        time.sleep(READ_WEBSOCKET_DELAY)
    except Exception, e:
      log.write(str(e))
      pass

if __name__ == 'main':
  main()
