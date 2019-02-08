from builtins import range
import MalmoPython
import os
import sys
import time
import numpy as np
import json
import pickle
import cv2
from PIL import ImageTk
from PIL import Image
from constants import *

from simpleMission import *

if sys.version_info[0] == 2:
  sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)  # flush print output immediately
else:
  import functools

  print = functools.partial(print, flush=True)

class CreateModel:

  def __init__(self):
    #Initialize the game engine
    self.agent_host = MalmoPython.AgentHost()
    self.agent_host.setObservationsPolicy(MalmoPython.ObservationsPolicy.LATEST_OBSERVATION_ONLY)
    self.agent_host.setVideoPolicy(MalmoPython.VideoPolicy.LATEST_FRAME_ONLY)

    self.ACTIONS = {
      'e': "move 1",
      's': "turn -1",
      'f': "turn 1",
      'b':"move -1"
    }

    self.grids = {}
    self.currentX = 0
    self.currentY = 0
    print("Initializing")

    #Set currentX and currentY based on the observation from the game.

  def startAgentHost(self):
    try:
      self.agent_host.parse(sys.argv)
    except RuntimeError as e:
      print('ERROR:', e)
      print(self.agent_host.getUsage())
      exit(1)
      exit(1)
    if self.agent_host.receivedArgument("help"):
      print(self.agent_host.getUsage())
      exit(0)

    # missionXML is from simpleMission.py
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


  def updateStateDictionaryWithState(self, state):
    print("Creating grid object from state.")
    #Get the object from dictionary for given x,y
    if state.number_of_observations_since_last_state > 0:
      for observation in state.observations:
        msg = observation.text
        obs = json.loads(msg)  # and parse the JSON
        yaw = int(obs.get(u'Yaw', 0))
        xPos = int(obs.get(u'XPos', 0) + 4.5)
        zPos = int(obs.get(u'ZPos', 0) + 4.5)
        videoFrame = state.video_frames[0]
        #cmap = Image.frombytes('RGB', (WIDTH, HEIGHT), bytes(videoFrame.pixels))
        #imageName = "model/x=" + str(xPos) + "y=" + str(zPos) + "yaw=" + str(yaw) + ".png"
        #cmap.save(imageName, "PNG")

        pos = str(xPos) + "," + str(zPos)
        if pos not in self.grids:
          self.grids[pos] = {}
        self.grids[pos]['x'] = xPos
        self.grids[pos]['y'] = zPos
        #fileName = "image" + str(yaw)
        #self.grids[pos][fileName] = imageName
        self.grids[pos][str(yaw)] = videoFrame.pixels

        print("To observation: (" + str(xPos) + ", " + str(zPos) + "), yaw:" + str(yaw))

  def takeAction(self, action):
    print("Taking action: " + str(action))
    model.agent_host.sendCommand(model.ACTIONS[action])
    time.sleep(0.20)
    state = model.agent_host.getWorldState()
    self.updateStateDictionaryWithState(state)



  def writeFile(self):
    print("Writing to file")
    """
    with open('model/model.json', 'w') as outfile:
      json.dump(self.grids, outfile)
    """
    pickleFile = "grids"
    with open('model/grids', 'wb') as outfile:
      pickle.dump(self.grids, outfile)


################################
#Main
################################

model = CreateModel()
model.startAgentHost()

writeToFile = False
while not writeToFile:
  action = input("Type command. {s:turn left, f:turn right, e: move forward, q: Write contents to file}: ")
  if action in ['s', 'e', 'f']:
    print("Take action")
    # Select and send action. Need to sleep to give time for simulator to respond
    model.takeAction(action)
    for i in range(4):
      #Turn 4 times to capture all four views from grid
      model.takeAction('s')

  elif action == 'q':
    print("Write the models grids to file")
    model.writeFile()
    writeToFile = True
  else:
    print("")
    print("Error. Command " + str(action) + " not recognized.")
    print("")
