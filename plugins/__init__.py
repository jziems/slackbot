import sys
import os

sys.path.append(__name__)

class plugin:

  def __init__(self, mods):
    self.__all__ = []
    for mod in mods:
      fx = __import__(mod)
      i = None
      if hasattr(fx, '__all__'):
        attrs = getattr(fx, '__all__')
        if '__init__' in attrs:
          i = fx.__init__()
          attrs.remove('__init__')
        for a in attrs:
          self.__func_init__(getattr(fx, a), ini=i)

  def __func_init__(self, fx, ini=None):
    setattr(self, fx.func_name, fx)
    if ini:
      setattr(getattr(self, fx.func_name), 'func_defaults', ini)
    self.__all__.append(fx.func_name)

mods = []

for file in os.listdir(os.path.dirname(__file__)):
  filename, file_extension = os.path.splitext(file)
  if file_extension == '.py':
    mods.append(filename)

plugins = plugin(mods)

del file
del filename
del file_extension
del mods