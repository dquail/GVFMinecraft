from constants import *



#!/usr/bin/env python

"""Uses tilecoding to create state.

"""
import numpy as np
from tiles import *
import json
import time
from BehaviorPolicy import *

# image tiles
NUMBER_OF_PIXEL_SAMPLES = 100
CHANNELS = 4
NUM_IMAGE_TILINGS = 4
NUM_IMAGE_INTERVALS = 4
SCALE_RGB = NUM_IMAGE_INTERVALS / 256.0

IMAGE_START_INDEX = 0

# constants relating to image size recieved
IMAGE_HEIGHT = HEIGHT  # rows
IMAGE_WIDTH = WIDTH  # columns

NUMBER_OF_COLOR_CHANNELS = 3 #red, blue, green
PIXEL_FEATURE_LENGTH = np.power(NUM_IMAGE_INTERVALS, NUMBER_OF_COLOR_CHANNELS) * NUM_IMAGE_TILINGS
DID_TOUCH_FEATURE_LENGTH = 1
TOTAL_FEATURE_LENGTH = PIXEL_FEATURE_LENGTH * NUMBER_OF_PIXEL_SAMPLES + DID_TOUCH_FEATURE_LENGTH

# Channels
RED_CHANNEL = 0
GREEN_CHANNEL = 1
BLUE_CHANNEL = 2
DEPTH_CHANNEL = 3

WALL_THRESHOLD = 0.2 #If the prediction is greater than this, the pavlov agent will avert

class StateRepresentation(object):
  def __init__(self):
    self.behaviorPolicy = BehaviorPolicy()
    self.pointsOfInterest = []
    self.numberOfTimesBumping = 0
    self.randomYs = np.random.choice(HEIGHT, NUMBER_OF_PIXEL_SAMPLES, replace=True)
    self.randomXs = np.random.choice(WIDTH, NUMBER_OF_PIXEL_SAMPLES, replace=True)

    for i in range(NUMBER_OF_PIXEL_SAMPLES):
      point = self.randomXs[i], self.randomYs[i]
      self.pointsOfInterest.append(point)

  def getRGBPixelFromFrame(self, frame, x, y):
    length = len(frame)
    r = frame[3 * (x + y * WIDTH)]
    g = frame[1 + 3 * (x + y * WIDTH)]
    b = frame[2 + 3 * (x + y * WIDTH)]
    return (r, g, b)

  def didTouch(self, previousAction, currentState):
    # Determine if if touch was obtained last time step
    if not len(currentState.observations) > 0:
      return False

    didTouch = False

    if previousAction == self.behaviorPolicy.ACTIONS['extend_hand']:
      msg = currentState.observations[0].text
      #print(msg)

      observations = json.loads(msg)  # and parse the JSON
      grid = observations.get(u'floor3x3', 0)  # and get the grid we asked for
      yaw = observations.get(u'Yaw', 0)
      facingIdx = 1
      if (yaw == 0.0):
        # Facing south
        facingIdx = 7
      elif (yaw == 90.0):
        # Facing west
        facingIdx = 3
      elif (yaw == 180.0):
        # Facing north
        facingIdx = 1
      elif (yaw == -90):
        # Facing east
        facingIdx = 5
      if not grid[facingIdx] == "air":
        didTouch = True
      """
      print()
      print("Grid:")
      print(grid)
      """

    return didTouch

  def getEmptyPhi(self):
    return np.zeros(TOTAL_FEATURE_LENGTH)

  """
  Name: getPhi
  Description: Creates the feature representation (phi) for a given observation. The representation
    created by individually tile coding each NUMBER_OF_PIXEL_SAMPLES rgb values together, and then assembling them. 
    Finally, the didBump value is added to the end of the representation. didBump is determined to be true if
    the closest pixel in view is less than PIXEL_DISTANCE_CONSIDERED_BUMP
  Input: the observation. This is the full pixel rgbd values for each of the IMAGE_WIDTH X IMAGE_HEIGHT pixels in view
  Output: The feature vector
  """
  def getPhi(self, state, previousAction):
    if not state:
      return None
    if len(state.video_frames) < 0:
      return self.getEmptyPhi()
    frame = state.video_frames[0].pixels

    phi = []

    for point in self.pointsOfInterest:
      #Get the pixel value at that point
      x = point[0]
      y = point[1]
      red, green, blue = self.getRGBPixelFromFrame(frame, x, y)
      red = red / 256.0
      green = green / 256.0
      blue = blue / 256.0

      pixelRep = np.zeros(PIXEL_FEATURE_LENGTH)
      #Tile code these 3 values together
      indexes = tiles(NUM_IMAGE_TILINGS, PIXEL_FEATURE_LENGTH, [red, green, blue])
      for index in indexes:
        pixelRep[index] = 1.0

      #Assemble with other pixels
      phi.extend(pixelRep)

    didTouch = self.didTouch(previousAction = previousAction, currentState = state)
    phi.append(int(didTouch))

    return np.array(phi)


