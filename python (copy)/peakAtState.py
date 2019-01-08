import json

# For debugging - tells us if there is indeed
def isWallInFront(currentState):
  msg = currentState.observations[0].text
  # print(msg)

  observations = json.loads(msg)  # and parse the JSON
  grid = observations.get(u'floor3x3', 0)  # and get the grid we asked for
  yaw = observations.get(u'Yaw', 0)
  forwardIdx = 1
  isBlock = False
  if (yaw == 0.0):
    # Facing south
    forwardIdx = 7
  elif (yaw == 90.0):
    # Facing west
    forwardIdx = 3
  elif (yaw == 180.0):
    # Facing north
    forwardIdx = 1
  elif (yaw == -90 or yaw == 270):
    # Facing east
    forwardIdx = 5
  if not grid[forwardIdx] == "air":
    isBlock = True

  return isBlock

def isWallOnLeft(currentState):
  msg = currentState.observations[0].text
  # print(msg)

  observations = json.loads(msg)  # and parse the JSON
  grid = observations.get(u'floor3x3', 0)  # and get the grid we asked for
  yaw = observations.get(u'Yaw', 0)
  leftIdx = 1
  isBlock = False
  if (yaw == 0.0):
    # Facing south
    leftIdx = 5
  elif (yaw == 90.0):
    # Facing west
    leftIdx = 7
  elif (yaw == 180.0):
    # Facing north
    leftIdx = 3
  elif (yaw == -90 or yaw == 270):
    # Facing east
    leftIdx = 1
  if not grid[leftIdx] == "air":
    isBlock = True


  return isBlock

def isWallAdjacent(currentState):
  msg = currentState.observations[0].text
  # print(msg)

  observations = json.loads(msg)  # and parse the JSON
  grid = observations.get(u'floor3x3', 0)  # and get the grid we asked for
  yaw = observations.get(u'Yaw', 0)
  isBlock = False

  if not grid[1] == "air":
    isBlock = True
  elif not grid[3] == "air":
    isBlock = True
  elif not grid[5] == "air":
    isBlock = True
  elif not grid[7] == "air":
    isBlock = True

  return isBlock

def isWallOnRight(currentState):
  msg = currentState.observations[0].text
  # print(msg)

  observations = json.loads(msg)  # and parse the JSON
  grid = observations.get(u'floor3x3', 0)  # and get the grid we asked for
  yaw = observations.get(u'Yaw', 0)
  rightIdx = 1
  isBlock = False
  if (yaw == 0.0):
    # Facing south
    rightIdx = 3
  elif (yaw == 90.0):
    # Facing west
    rightIdx = 1
  elif (yaw == 180.0):
    # Facing north
    rightIdx = 5
  elif (yaw == -90 or yaw == 270):
    # Facing east
    rightIdx = 7
  if not grid[rightIdx] == "air":
    isBlock = True


  return isBlock
