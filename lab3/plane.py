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
  	self.normal = Point3D(0,0,1)
  	self.distance = 0

  def distanceFrom(self, point):
  	""" returns the distance of a point from this plane """
  	return numpy.dot(self.normal.getArray(),point.getArray()) + self.distance

  def up(self, increment):
  	self.normal.z = increment