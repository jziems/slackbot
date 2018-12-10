import os
import pygame.camera
import pygame.image
import logging

__all__ = ['__init__', 'snap', '__del__']
__package__ = 'slackbot.plugins'
logger = logging.getLogger('slackbot')

class MySurface(pygame.Surface):
  binary = True

  def __init__(self, img, path):
    pygame.image.save(img, path)
    self.path = os.path.abspath(path)

def __init__(width=1280, height=720, format="RGB"):
  try:
    logger.debug("Width: %s Height: %s" % (width,height))
    pygame.camera.init()
    cams = pygame.camera.list_cameras()
    cam = pygame.camera.Camera(cams[0], (width,height), format)
    return (cam,)
  except Exception as e:
    logger.exception(e)
    raise e

def snap(cam=None):
  try:
    logger.debug("cam: %s" % cam)
    cam.start()
    img = cam.get_image()
    cam.stop()
    return MySurface(img, path='temp.jpg')
  except Exception as e:
    logger.exception(e.args)
    logger.exception(e.message)
    raise e

def __del__():
    pygame.camera.quit()

