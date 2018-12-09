import os
import pygame.camera
import pygame.image

__all__ = ['__init__', 'snap', '__del__']
__package__ = 'plugins'

def __init__(width=1600, height=900, format="RGB"):
  try:
    pygame.camera.init()
    cams = pygame.camera.list_cameras()
    cam = pygame.camera.Camera(cams[0], (width,height), format)
    cam.start()
    return (cam,)
  except:
    raise

def snap(cam=None, name='test.jpg'):
  try:
    img = cam.get_image()
    pygame.image.save(img, name)
    return os.path.abspath(name)
  except:
    raise

def __del__(cam=None):
    cam.stop()
    pygame.camera.quit()

