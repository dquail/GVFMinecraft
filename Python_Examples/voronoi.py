#!/usr/bin/python

import cv2
import numpy as np
import random


# Check if a point is inside a rectangle
def rect_contains(rect, point):
  if point[0] < rect[0]:
    return False
  elif point[1] < rect[1]:
    return False
  elif point[0] > rect[2]:
    return False
  elif point[1] > rect[3]:
    return False
  return True


# Draw a point
def draw_point(img, p, color):
  cv2.circle(img, p, 2, color, 2, cv2.LINE_AA, 0)


# Draw delaunay triangles
def draw_delaunay(img, subdiv, delaunay_color):
  triangleList = subdiv.getTriangleList();
  size = img.shape
  r = (0, 0, size[1], size[0])

  for t in triangleList:

    pt1 = (t[0], t[1])
    pt2 = (t[2], t[3])
    pt3 = (t[4], t[5])

    if rect_contains(r, pt1) and rect_contains(r, pt2) and rect_contains(r, pt3):
      cv2.line(img, pt1, pt2, delaunay_color, 1, cv2.LINE_AA, 0)
      cv2.line(img, pt2, pt3, delaunay_color, 1, cv2.LINE_AA, 0)
      cv2.line(img, pt3, pt1, delaunay_color, 1, cv2.LINE_AA, 0)


# Draw voronoi diagram
def draw_voronoi(original, img, subdiv):
  (facets, centers) = subdiv.getVoronoiFacetList([])
  facetCount = len(facets)
  for i in range(0, len(facets)):
    ifacet_arr = []
    for f in facets[i]:
      ifacet_arr.append(f)

    ifacet = np.array(ifacet_arr, np.int)
    #color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    p = centers[i]
    x = int(p[1])
    y = int(p[0])
    originalPixel = original[x,y]

    color = originalPixel.tolist()

    cv2.fillConvexPoly(img, ifacet, color, cv2.LINE_AA, 0);
    ifacets = np.array([ifacet])
    cv2.polylines(img, ifacets, True, (0, 0, 0), 1, cv2.LINE_AA, 0)
    #cv2.circle(img, (centers[i][0], centers[i][1]), 3, (0, 0, 0), 2, cv2.LINE_AA, 0)


if __name__ == '__main__':

  # Define window names
  win_delaunay = "Delaunay Triangulation"
  win_voronoi = "Voronoi Diagram"

  # Turn on animation while drawing triangles
  animate = True

  # Define colors for drawing.
  delaunay_color = (255, 255, 255)
  points_color = (0, 0, 255)

  # Read in the image.
  #1920X1080
  img = cv2.imread("christmastree.jpg");
  #cv2.imshow('image', img)
  #cv2.waitKey(0)
  # Keep a copy around
  img_orig = img.copy();

  # Rectangle to be used with Subdiv2D
  #(1080, 1920, 3)
  size = img.shape
  rect = (0, 0, size[1], size[0])

  # Create an instance of Subdiv2D
  subdiv = cv2.Subdiv2D(rect);

  # Create an array of points.
  points = [];
  numberOfRandomPoints = 1500
  #TODO - remove afte rtesting

  #randomYs = np.random.choice(size[0], numberOfRandomPoints, replace=True)
  width = size[1]
  height = size[0]
  smallest = min(width, height)
  randomYs = np.random.choice(height, numberOfRandomPoints, replace=True)
  randomXs = np.random.choice(width, numberOfRandomPoints, replace=True)
  for i in range(numberOfRandomPoints):
    point = int(randomXs[i]), int(randomYs[i])
    points.append(point)

  """
  # Read in the points from a text file
  with open("points.txt") as file:
    for line in file:
      x, y = line.split()
      points.append((int(x), int(y)))
  """
  # Insert points into subdiv
  for p in points:
    subdiv.insert(p)

    """
    # Show animation
    if animate:
      img_copy = img_orig.copy()
      # Draw delaunay triangles
      draw_delaunay(img_copy, subdiv, (255, 255, 255));
      cv2.imshow(win_delaunay, img_copy)
      cv2.waitKey(100)
    """
  # Draw delaunay triangles
  #draw_delaunay(img, subdiv, (255, 255, 255));

  # Draw points
  """
  for p in points:
    draw_point(img, p, (0, 0, 255))
  """
  # Allocate space for Voronoi Diagram
  img_voronoi = np.zeros(img.shape, dtype=img.dtype)

  # Draw Voronoi diagram
  draw_voronoi(img, img_voronoi, subdiv)

  # Show results
  #cv2.imshow(win_delaunay, img)
  cv2.imshow(win_voronoi, img_voronoi)

  cv2.waitKey(0)
