import dropbox
import os
import json

__all__ = ['__init__', 'upload']
__package__ = 'plugins'

def __init__():
  try:
    homedir = os.path.expanduser('~')
    with open(homedir + '/.dropbox_api', 'r') as fin:
      cfg = json.load(fin)
      for k, v in cfg.items():
        cfg[k] = v
    return (dropbox.Dropbox(cfg['DROPBOX_TOKEN']),None,None)
  except:
    raise

def upload(dbx, filepath, remotepath=None):
  try:
    dbx.files_upload(open(filepath, 'rb'), remotepath, mode=dropbox.files.WriteMode.add, autorename=False, client_modified=None, mute=True)
    return dbx.sharing_create_shared_link_with_settings(remotepath).url[0:-1]+'1'
  except:
    raise
