from constants import *
import sys
import cv2
if sys.version_info[0] == 2:
  # Workaround for https://github.com/PythonCharmers/python-future/issues/262
  from Tkinter import *
else:
  from tkinter import *

from PIL import ImageTk
from PIL import Image

video_width = 432
video_height = 240

DISPLAY_WIDTH = WIDTH
DISPLAY_HEIGHT = 432 + video_height

class Display(object):
  def __init__(self):
    self.root = Tk()
    self.root.wm_title("GVF Knowledge")
    #self.root_frame = Frame(self.root)
    #self.canvas = Canvas(self.root_frame, borderwidth=0, highlightthickness=0, width=WIDTH, height=HEIGHT, bg="black")
    self.canvas = Canvas(self.root, borderwidth=0, highlightthickness=0, width=WIDTH, height=HEIGHT, bg="black")
    #self.canvas.config(width=WIDTH, height=HEIGHT)
    self.canvas.pack(padx=0, pady=0)
    #self.root_frame.pack()
    self.reset()



  def reset(self):
    self.canvas.delete("all")

    self.image = Image.new('RGB', (WIDTH, HEIGHT))
    self.photoImage = None
    self.image_handle = None
    self.current_frame = 0

  def updateImage(self, image):
    #change from BGR to RGB
    l = len(image)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    # convert the cv2 images to PIL format...
    self.image = Image.fromarray(image)

    # ...and then to ImageTk format
    self.photoImage = ImageTk.PhotoImage(self.image)


    # And update/create the canvas image:
    if self.image_handle is None:
      self.image_handle = self.canvas.create_image(WIDTH/2,HEIGHT/2,
                                               image=self.photoImage)
    else:
      self.canvas.itemconfig(self.image_handle, image=self.photoImage)

    self.root.update()

