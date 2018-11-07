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
from BehaviorPolicy import *

from PIL import ImageTk
from PIL import Image

if sys.version_info[0] == 2:
  sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)  # flush print output immediately
else:
  import functools

  print = functools.partial(print, flush=True)

class Foreground:

  def __init__(self):
    self.agent_host = MalmoPython.AgentHost()
    self.agent_host.setObservationsPolicy(MalmoPython.ObservationsPolicy.LATEST_OBSERVATION_ONLY)
    self.agent_host.setVideoPolicy(MalmoPython.VideoPolicy.LATEST_FRAME_ONLY)
    self.behaviorPolicy = BehaviorPolicy()
    self.stateRepresentation = StateRepresentation()

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
    self.world_state = self.agent_host.getWorldState()
    while not self.world_state.has_mission_begun:
      print(".", end="")
      time.sleep(0.1)
      self.world_state = self.agent_host.getWorldState()
      for error in self.world_state.errors:
        print("Error:", error.text)

    print()
    print("Mission running ", end=' ')

  def start(self):
    self.start_agent_host()

    actionCount = 0


    # Loop until mission ends:
    while self.world_state.is_mission_running:
      actionCount += 1
      print(".", end="")

      self.world_state = self.agent_host.getWorldState()
      action = self.behaviorPolicy.randomPolicy(self.world_state)
      print("Action (" + str(actionCount) + "):" + str(action))

      self.agent_host.sendCommand(action)

      time.sleep(1.1)
      for error in self.world_state.errors:
        print("Error:", error.text)
      if self.world_state.number_of_observations_since_last_state > 0:  # Have any observations come in?

        msg = self.world_state.observations[0].text  # Yes, so get the text

        frame = self.world_state.video_frames[0].pixels
        voronoi = voronoi_from_pixels(pixels = frame, dimensions = (WIDTH, HEIGHT), pixelsOfInterest = self.stateRepresentation.pointsOfInterest)
        # voronoi_from_pixel_subset(self.world_state.video_frames[0].pixels, (WIDTH,HEIGHT), ramdom_pixels)
        #cmap = Image.frombytes('RGB', (WIDTH, HEIGHT), bytes(self.world_state.video_frames[0].pixels))

        #open_cv_image = np.array(cmap)
        # Convert RGB to BGR

        #open_cv_image = open_cv_image[:,:,::-1].copy()
        cv2.imshow('My Image', voronoi)
        cv2.waitKey(0)
        #cmap.show()

        #rgb = getRGBPixelFromFrame(frame, int(1), int(1))

        print("Obs")
        print(msg)
        observations = json.loads(msg)  # and parse the JSON
        grid = observations.get(u'floor3x3', 0)  # and get the grid we asked for
        yaw = observations.get(u'Yaw', 0)
        """
        The observation returns includes yaw value. That (the direction it is facing) combined with the grid value 
        can be uesd to determine if the agent is at a wall. ie. if the grid contains non air values, you know it's up 
        against a wall. Then you can use the direction (yaw) to determine if it is facing a wall. 
        """
        print()
        print("Grid:")
        print(grid)

    print()
    print("Mission ended")
    # Mission has ended.

fg = Foreground()
fg.start()