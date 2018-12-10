import dropbox
import os
import json
import logging
import time

__all__ = ['__init__', 'upload']
__package__ = 'slackbot.plugins'
logger = logging.getLogger('slackbot')

class MyStr(unicode):
  binary = False

def __init__():
  try:
    homedir = os.path.expanduser('~')
    with open(homedir + '/.dropbox_api', 'r') as fin:
      cfg = json.load(fin)
      for k, v in cfg.items():
        cfg[k] = v
    return (dropbox.Dropbox(cfg['DROPBOX_TOKEN']),None,None)
  except Exception as e:
    logger.exception(e)
    raise e

def upload(dbx=None, filepath=None, remotepath=None):
  try:
    logger.debug("Args dbx: %s filepath: %s remotepath: %s" % (dbx,filepath,remotepath))
    if not filepath:
      raise Exception("Need file path to upload.")
    if remotepath:
      with open(filepath, 'rb') as fin:
        dbx.files_upload(fin.read(), path=remotepath, mode=dropbox.files.WriteMode.add, autorename=False, client_modified=None, mute=True)
        resp = MyStr(dbx.sharing_create_shared_link_with_settings(remotepath).url[0:-1] + '1')
    else:
      remotepath = '/'+str(time.time())+'.jpg'
      with open(filepath, 'rb') as fin:
        dbx.files_upload(fin.read(), path=remotepath, mode=dropbox.files.WriteMode.add, autorename=False, client_modified=None, mute=True)
      resp = MyStr(dbx.sharing_create_shared_link_with_settings(remotepath).url[0:-1]+'1')
    return resp
  except Exception as e:
    logger.exception(e)
    raise e
