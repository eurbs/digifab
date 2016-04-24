from point3d import *
import numpy

"""
Emilee Urbanek and Nick Confrey
CMSC 22010: Digital Fabrication
Lab 3
Due: 4/25

---

The Plane Class
Used to define the cutting Plane
"""

class Plane(object):
  def __init__(self):
  	self.normal = point3d(0,0,1)
  	self.distance = 0

  def distanceFrom(self, point):
  	""" returns the distance of a point from this plane """
  	return dot(self.normal,point) + self.distance