from __future__ import print_function
# ------------------------------------------------------------------------------------------------
# Copyright (c) 2016 Microsoft Corporation
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and
# associated documentation files (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge, publish, distribute,
# sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or
# substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT
# NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
# DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
# ------------------------------------------------------------------------------------------------

# Tutorial sample #2: Run simple mission using raw XML

from builtins import range
import MalmoPython
import os
import sys
import time
import numpy as np
import json
import cv2
from Voronoi import *
from constants import *
from StateRepresentation import *
from simpleMission import *
import peakAtState as peak
from BehaviorPolicy import *
from display import *
from GVF import *

from PIL import ImageTk
from PIL import Image

if sys.version_info[0] == 2:
  sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)  # flush print output immediately
else:
  import functools

  print = functools.partial(print, flush=True)

def didTouchCumulant(phi):
  return phi[len(phi) - 1]


def didtouchGamma(phi):
  return 0

class Foreground:

  def __init__(self):
    self.agent_host = MalmoPython.AgentHost()
    self.agent_host.setObservationsPolicy(MalmoPython.ObservationsPolicy.LATEST_OBSERVATION_ONLY)
    self.agent_host.setVideoPolicy(MalmoPython.VideoPolicy.LATEST_FRAME_ONLY)
    self.behaviorPolicy = BehaviorPolicy()
    self.stateRepresentation = StateRepresentation()
    self.display = Display()
    self.gvfs = {}
    self.configureGVFs()
    self.state = False
    self.oldState = False
    self.phi = self.stateRepresentation.getEmptyPhi()
    self.oldPhi = self.stateRepresentation.getEmptyPhi()



  def configureGVFs(self):
    touchGVF = GVF(featureVectorLength = TOTAL_FEATURE_LENGTH, alpha = 0.10 /( NUM_IMAGE_TILINGS * NUMBER_OF_PIXEL_SAMPLES), isOffPolicy=True, name="T")
    touchGVF.cumulant = didTouchCumulant
    touchGVF.policy = self.behaviorPolicy.extendHandPolicy
    touchGVF.gamma = didtouchGamma
    self.gvfs[touchGVF.name] = touchGVF

    turnLeftGVF = GVF(featureVectorLength=TOTAL_FEATURE_LENGTH,
                        alpha=0.10 / (NUM_IMAGE_TILINGS * NUMBER_OF_PIXEL_SAMPLES), isOffPolicy=True, name="TL")
    turnLeftGVF.cumulant = self.gvfs['T'].prediction
    turnLeftGVF.policy = self.behaviorPolicy.turnLeftPolicy
    turnLeftGVF.gamma = didtouchGamma
    self.gvfs[turnLeftGVF.name] = turnLeftGVF

    turnRightGVF = GVF(featureVectorLength=TOTAL_FEATURE_LENGTH,
                        alpha=0.10 / (NUM_IMAGE_TILINGS * NUMBER_OF_PIXEL_SAMPLES), isOffPolicy=True, name="TR")
    turnRightGVF.cumulant = self.gvfs['T'].prediction
    turnRightGVF.policy = self.behaviorPolicy.turnRightPolicy
    turnRightGVF.gamma = didtouchGamma
    self.gvfs[turnRightGVF.name] = turnRightGVF

  def start_agent_host(self):
    try:
      self.agent_host.parse(sys.argv)
    except RuntimeError as e:
      print('ERROR:', e)
      print(self.agent_host.getUsage())
      exit(1)
    if self.agent_host.receivedArgument("help"):
      print(self.agent_host.getUsage())
      exit(0)

    #missionXML is from simpleMission.py
    my_mission = MalmoPython.MissionSpec(missionXML, True)
    my_mission_record = MalmoPython.MissionRecordSpec()

    # Attempt to start a mission:
    max_retries = 3
    for retry in range(max_retries):
      try:
        self.agent_host.startMission(my_mission, my_mission_record)
        break
      except RuntimeError as e:
        if retry == max_retries - 1:
          print("Error starting mission:", e)
          exit(1)
        else:
          time.sleep(2)

    # Loop until mission starts:
    print("Waiting for the mission to start ", end=' ')
    self.state = self.agent_host.getWorldState()
    while not self.state.has_mission_begun:
      print(".", end="")
      time.sleep(0.1)
      self.state = self.agent_host.getWorldState()
      for error in self.state.errors:
        print("Error:", error.text)

    print()
    print("Mission running ", end=' ')

  def learn(self):
    #Get the feature representation for the old and new states
    for name, gvf in self.gvfs.items():
      gvf.learn(lastState=self.oldPhi, action=self.action, newState=self.phi)
    #self.touchGVF.learn(lastState = self.oldPhi, action = self.action, newState = self.phi)



  def updateUI(self):
    #Create a voronoi image
    frame = self.state.video_frames[0].pixels
    # rgb = self.stateRepresentation.getRGBPixelFromFrame(frame, int(1), int(1))

    voronoi = voronoi_from_pixels(pixels=frame, dimensions=(WIDTH, HEIGHT),
                                  pixelsOfInterest=self.stateRepresentation.pointsOfInterest)
    # cv2.imshow('My Image', voronoi)
    # cv2.waitKey(0)

    didTouch = self.stateRepresentation.didTouch(previousAction = self.action, currentState = self.oldState)

    inFront = peak.isWallInFront(self.state)
    touchPrediction = self.gvfs['T'].prediction(self.phi)

    onLeft = peak.isWallOnLeft(self.state)
    turnLeftAndTouchPrediction = self.gvfs['TL'].prediction(self.phi)

    onRight = peak.isWallOnRight(self.state)
    turnRightAndtouchPrediction = self.gvfs['TR'].prediction(self.phi)
    self.display.update(image=voronoi,
                        numberOfSteps=self.actionCount,
                        currentTouchPrediction=touchPrediction,
                        wallInFront = inFront,
                        didTouch=didTouch,
                        turnLeftAndTouchPrediction = turnLeftAndTouchPrediction,
                        wallOnLeft = onLeft,
                        turnRightAndTouchPrediction = turnRightAndtouchPrediction,
                        wallOnRight = onRight)
    #time.sleep(1.0)

  def start(self):
    self.start_agent_host()

    self.actionCount = 0

    self.action = self.behaviorPolicy.ACTIONS['no_action']

    # Loop until mission ends:
    while self.state.is_mission_running:
      self.actionCount += 1
      print(".", end="")

      self.oldState = self.state
      self.oldPhi = self.phi

      #Select and send action. Need to sleep to give time for simulator to respond
      self.action = self.behaviorPolicy.mostlyForwardAndTouchPolicy(self.state)
      self.agent_host.sendCommand(self.action)
      time.sleep(0.1)
      self.state = self.agent_host.getWorldState()
      if self.state.number_of_observations_since_last_state > 0:
        for error in self.state.errors:
          print("Error:", error.text)
        self.phi = self.stateRepresentation.getPhi(state=self.state, previousAction=self.action)

        #Do the learning
        self.learn()

        #Update our display (for debugging and progress reporting)
        self.updateUI()


      #Get new state

      """
      - Choose action
      - Take action
      - Get new observe
      - Make previous observe old
      - Learn
      - Update display
      
      """

    print()
    print("Mission ended")
    # Mission has ended.

fg = Foreground()
fg.start()