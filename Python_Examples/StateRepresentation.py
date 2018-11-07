from constants import *

def getRGBPixelFromFrame(frame, x, y):
  length = len(frame)
  r = frame[3 * (x + y * WIDTH)]
  g = frame[1 + 3 * (x + y * WIDTH)]
  b = frame[2 + 3 * (x + y * WIDTH)]
  return (r, g, b)

