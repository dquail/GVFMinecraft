from random import randint
import numpy as np
import random

class BehaviorPolicy:

  def __init__(self):
    self.lastAction = 0
    self.i = 0

    self.ACTIONS = {
      'forward': "move 1",
      'back': "move -1",
      'turn_left': "turn 1",
      'extend_hand':"attack 1",
      'no_action': "move 0"
    }


  def policy(self, state):
    self.i = self.i + 1

    isFacingWall = state[len(state) - 1] == 1 #Last bit in the feature representation represents facing the wall
    if isFacingWall:
      return self.ACTIONS['look_left']
    else:
      return self.ACTIONS['forward']

  def mostlyForwardPolicy(self,state):
    self.i+=1
    if self.i %5 == 0:
      return self.randomPolicy(state)
    else:
      return self.moveForwardPolicy(state)

  def mostlyForwardAndTouchPolicy(self, state):
    self.i +=1
    if self.i % 200 == 0:
      return self.ACTIONS['turn_left']
    elif self.i %2 ==0:
      return self.ACTIONS['extend_hand']
    else:
      return self.moveForwardPolicy(state)

  def extendHandPolicy(self, state):
    return self.ACTIONS['extend_hand']

  def randomPolicy(self, state):
    return self.ACTIONS[random.choice(list(self.ACTIONS.keys()))]

  def moveForwardPolicy(self, state):

    return self.ACTIONS['forward']

  def turnLeftPolicy(self, state):
    self.i = self.i + 1
    return self.ACTIONS['turn_left']

  def epsilonGreedyPolicy(self, state):
    print("Do something here")