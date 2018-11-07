from future import standard_library
standard_library.install_aliases()
from builtins import bytes
from builtins import range
from builtins import object
from past.utils import old_div
import MalmoPython
import random
import time
import logging
import struct
import socket
import os
import sys
import errno
import json
import math
import malmoutils

if sys.version_info[0] == 2:
    # Workaround for https://github.com/PythonCharmers/python-future/issues/262
    from Tkinter import *
else:
    from tkinter import *

from PIL import ImageTk
from PIL import Image


class MyFirstGUI:
  def __init__(self, master):
    self.master = master
    master.title("A simple GUI")

    self.label = Label(master, text="This is our first GUI!")
    self.label.pack()

    self.greet_button = Button(master, text="Greet", command=self.greet)
    self.greet_button.pack()

    self.close_button = Button(master, text="Close", command=master.quit)
    self.close_button.pack()

  def greet(self):
    print("Greetings!")


root = Tk()
my_gui = MyFirstGUI(root)
root.mainloop()