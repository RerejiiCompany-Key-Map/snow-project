import sys
import pygame
import Image
import VideoCapture

def image2surface(image):
  mode = image.mode
  size = image.size
  data = image.tostring()

  return pygame.image.fromstring(data, size, mode)

camera = VideoCapture.Device()
camera.displayCapturePinProperties()

pygame.init()

size = width, height = 640, 480

screen = pygame.display.set_mode(size)

BLACK = (0, 0, 0)
ORIGIN = (0, 0)
while 1:
  for event in pygame.event.get():
    if event.type == pygame.QUIT: sys.exit()

  image = camera.getImage()
  surface = image2surface(image)

  screen.fill(BLACK)
  screen.blit(surface, ORIGIN)
  pygame.display.flip()
