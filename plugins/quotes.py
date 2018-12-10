from requests import get
import json
import logging

__all__ = ['hitme',]
__package__ = 'slackbot.plugins'
logger = logging.getLogger('slackbot')

class MyStr(unicode):
  binary = False

def hitme():
  try:
    r=get('http://api.icndb.com/jokes/random')
    q=json.loads(r.text)
    resp = MyStr(''.join(q['value']['joke']))
    return resp
  except Exception as e:
    logger.exception(e)
    raise e
