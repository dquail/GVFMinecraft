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
from PIL import ImageTk
from PIL import Image

if sys.version_info[0] == 2:
    sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)  # flush print output immediately
else:
    import functools
    print = functools.partial(print, flush=True)

# More interesting generator string: "3;7,44*49,73,35:1,159:4,95:13,35:13,159:11,95:10,159:14,159:6,35:6,95:6;12;"
# Less interesting generator string: "3;7,220*1,5*3,2;3;,biome_1"

missionXML='''<?xml version="1.0" encoding="UTF-8" standalone="no" ?>
            <Mission xmlns="http://ProjectMalmo.microsoft.com" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
            
              <About>
                <Summary>Hello world!</Summary>
              </About>
              
              <ServerSection>
                <ServerInitialConditions>
                    <Time>
                        <StartTime>12000</StartTime>
                        <AllowPassageOfTime>false</AllowPassageOfTime>
                    </Time>
                    <Weather>clear</Weather>
                </ServerInitialConditions>
                <ServerHandlers>
                  <FlatWorldGenerator generatorString="3;7,44*49,73,35:1,159:4,95:13,35:13,159:11,95:10,159:14,159:6,35:6,95:6;12;"/>
                  <DrawingDecorator>
                    <DrawLine x1="20" y1="56" z1="-20" x2="20" y2="56" z2="100" type = "sand"/>
                    <DrawLine x1="20" y1="57" z1="-20" x2="20" y2="57" z2="100" type = "sand"/>
                    <DrawLine x1="20" y1="58" z1="-20" x2="20" y2="58" z2="100" type = "sand"/>
                    <DrawLine x1="20" y1="59" z1="-20" x2="20" y2="59" z2="100" type = "sand"/>
                    
                    <DrawLine x1="11" y1="56" z1="-20" x2="-50" y2="56" z2="-20" type = "gold_block"/>
                    <DrawLine x1="11" y1="57" z1="-20" x2="-50" y2="57" z2="-20" type = "gold_block"/>
                    <DrawLine x1="11" y1="58" z1="-20" x2="-50" y2="58" z2="-20" type = "gold_block"/>
                    <DrawLine x1="11" y1="59" z1="-20" x2="-50" y2="59" z2="-20" type = "gold_block"/>
                    
                    <DrawLine x1="-20" y1="56" z1="-8" x2="-20" y2="56" z2="20" type = "brick_block"/>
                    <DrawLine x1="-20" y1="57" z1="-8" x2="-20" y2="57" z2="20" type = "brick_block"/>
                    <DrawLine x1="-20" y1="58" z1="-8" x2="-20" y2="58" z2="20" type = "brick_block"/>
                    <DrawLine x1="-20" y1="59" z1="-8" x2="-20" y2="59" z2="20" type = "brick_block"/>                    
                                        
                    <DrawLine x1="-10" y1="56" z1="20" x2="9" y2="56" z2="20" type = "diamond_block"/>
                    <DrawLine x1="-10" y1="57" z1="20" x2="9" y2="57" z2="20" type = "diamond_block"/>
                    <DrawLine x1="-10" y1="58" z1="20" x2="9" y2="58" z2="20" type = "diamond_block"/>
                    <DrawLine x1="-10" y1="59" z1="20" x2="9" y2="59" z2="20" type = "diamond_block"/>    
                    
                  </DrawingDecorator>
                  <ServerQuitFromTimeUp timeLimitMs="300000"/>
                  <ServerQuitWhenAnyAgentFinishes/>
                </ServerHandlers>
              </ServerSection>
              
              <AgentSection mode="Survival">
                <Name>MalmoTutorialBot</Name>
                <AgentStart>
                    <Placement x="0.5" y="56" z="0.5" yaw="0"/>
                </AgentStart>
                <AgentHandlers>
                    <VideoProducer want_depth="false">
                        <Width>320</Width>
                        <Height>240</Height>
                    </VideoProducer>
                    <ObservationFromGrid>
                        <Grid name="floor3x3">
                            <min x="-1" y="0" z="-1"/>
                            <max x="1" y="0" z="1"/>
                        </Grid>
                    </ObservationFromGrid>
                    <ObservationFromFullStats/>
                    <DiscreteMovementCommands />
                </AgentHandlers>
              </AgentSection>
            </Mission>'''

# Create default Malmo objects:
#Translates to Move forward, Move back, Turn 90 degrees right, Turn 90 degrees left

actions = ["move 1", "move -1", "turn 1", "turn -1"]

def getRandomAction():
    return actions[np.random.randint(0, len(actions))]

def getPixelIndex(channel, x, y):
    if channel == 'R':
        chan = 0
    elif channel == 'G':
        chan = 1
    elif channel == 'B':
        chan = 2
    else:
        return False

    width = 320
    height = 240
    index = (chan * width * height) + (y * width) + x
    return index

def getRGBPixelFromFrame(frame, x, y):
    """
    rIndex = getPixelIndex('R', x, y)
    gIndex = getPixelIndex('G', x, y)
    bIndex = getPixelIndex('B', x, y)
    rgb = (frame[rIndex], frame[gIndex], frame[bIndex])
    return rgb
    """
    width = 320
    height = 240

    r = frame[3*(x+y*width)]
    g = frame[1+3*(x+y*width)]
    b = frame[2+3*(x+y*width)]
    return (r,g,b)

agent_host = MalmoPython.AgentHost()
agent_host.setObservationsPolicy(MalmoPython.ObservationsPolicy.LATEST_OBSERVATION_ONLY)
agent_host.setVideoPolicy(MalmoPython.VideoPolicy.LATEST_FRAME_ONLY)

try:
    agent_host.parse( sys.argv )
except RuntimeError as e:
    print('ERROR:',e)
    print(agent_host.getUsage())
    exit(1)
if agent_host.receivedArgument("help"):
    print(agent_host.getUsage())
    exit(0)

my_mission = MalmoPython.MissionSpec(missionXML, True)
my_mission_record = MalmoPython.MissionRecordSpec()

# Attempt to start a mission:
max_retries = 3
for retry in range(max_retries):
    try:
        agent_host.startMission( my_mission, my_mission_record )
        break
    except RuntimeError as e:
        if retry == max_retries - 1:
            print("Error starting mission:",e)
            exit(1)
        else:
            time.sleep(2)

# Loop until mission starts:
print("Waiting for the mission to start ", end=' ')
world_state = agent_host.getWorldState()
while not world_state.has_mission_begun:
    print(".", end="")
    time.sleep(0.1)
    world_state = agent_host.getWorldState()
    for error in world_state.errors:
        print("Error:",error.text)

print()
print("Mission running ", end=' ')

actionCount = 0
# Loop until mission ends:
while world_state.is_mission_running:
    actionCount+=1
    print(".", end="")

    #action = getRandomAction()
    action = "move 1"
    print("Action (" + str(actionCount) + "):" + str(action))

    agent_host.sendCommand(action)
    world_state = agent_host.getWorldState()
    time.sleep(1.1)
    for error in world_state.errors:
        print("Error:",error.text)
    if world_state.number_of_observations_since_last_state > 0:  # Have any observations come in?

        msg = world_state.observations[0].text  # Yes, so get the text
        frame = world_state.video_frames[0].pixels
        #cmap = Image.frombytes('RGB', (320, 240), bytes(world_state.video_frames[0].pixels))
        #cmap.show()
        rgb = getRGBPixelFromFrame(frame, int(320/2), int(240/2))

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
