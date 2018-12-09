from requests import get
import json

__all__ = ['hitme',]
__package__ = 'plugins'

def hitme():
  try:
    r=get('http://api.icndb.com/jokes/random')
    q=json.loads(r.text)
    return ''.join(q['value']['joke'])
  except:
    raise
