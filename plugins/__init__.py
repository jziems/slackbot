import sys
import os
import logging

sys.path.append(__name__)
__package__ = 'slackbot.plugins'

class plugins:

  def __init__(self):
    self.__all__ = []
    self.logger = logging.getLogger('slackbot')
    mods = []
    for file in os.listdir(os.path.dirname(__file__)):
      filename, file_extension = os.path.splitext(file)
      if file_extension == '.py' and not filename[:1] == '__':
        mods.append(filename)
    for mod in mods:
      try:
        fx = __import__(mod)
        i = None
        if hasattr(fx, '__all__'):
          attrs = getattr(fx, '__all__')
          if '__init__' in attrs:
            i = fx.__init__()
            self.logger.debug("Module: %s init: %s" % (mod,i))
            attrs.remove('__init__')
          for a in attrs:
            self.__func_init__(getattr(fx, a), ini=i)
      except Exception as e:
        self.logger.exception(e)
        raise e

  def __func_init__(self, fx, ini=None):
    try:
      self.logger.debug("Function: %s ini: %s" % (fx,ini))
      setattr(self, fx.func_name, fx)
      if ini:
        setattr(getattr(self, fx.func_name), 'func_defaults', ini)
      self.__all__.append(fx.func_name)
    except Exception as e:
      self.logger.exception(e)
      raise e