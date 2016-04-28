from point3d import *
from helpers import *
import numpy

"""
Emilee Urbanek and Nick Confrey
CMSC 22010: Digital Fabrication
Lab 3
Due: 4/25

---

The line segment class
"""

class Segment(object):
  def __init__(self, start, end):
    self.start = start
    self.end = end

  def __str__(self):
    return "segment:\n\tstart {!s}\n\t  end {!s}".format(self.start, self.end)

  def getHashStringStart(self):
  	return "X" + str(self.start.x) + "Y" + str(self.start.y)

  def getHashStringEnd(self):
  	return "X" + str(self.end.x) + "Y" + str(self.end.y)

  	#s = self, o = other, both segment objects
  def intersect2D(s, o):
  	"""Check if the two lines intersect, only considering x and y coords"""
  	#https://en.wikipedia.org/wiki/Line%E2%80%93line_intersection
  	#Using determinants, as we only have two points on each line
  	x1 = s.start.x
  	y1 = s.start.y
  	x2 = s.end.x
  	y2 = s.end.y
  	x3 = o.start.x
  	y3 = o.start.y
  	x4 = o.end.x
  	y4 = o.end.y

  	pXTop = (x1*y2 - y1*x2) * (x3 - x4) - (x1 - x2)*(x3*y4 - y3*x4)
  	pButt = (x1 - x2)*(y3 - y4) - (y1 - y2)*(x3 - x4)
  	pYTop = (x1*y2 - y1*x2) * (y3 - y4) - (y1 - y2)*(x3*y4 - y3*x4)

  	if(isclose(pButt, 0)):
  		return None
  	Px = pXTop / pButt
  	Py = pYTop / pButt
  	if(Px < x1 or Px > x2):
  		return None
  	if(Py < y1 or Py > y2):
  		return None

  	return Point3D(Px, Py, 0)
