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
  def __init__(self, start, end, perpIn):
    self.start = start
    self.end = end
    self.perpIn = perpIn  # This is set after the initialization of a segment
    # perpIn stands for perpendicular unit vector pointing inward

  def __str__(self):
    return "segment:\n\tstart {!s}\n\t  end {!s}".format(self.start, self.end)

  def getHashStringStart(self):
  	return "X" + str(self.start.x) + "Y" + str(self.start.y)

  def getHashStringEnd(self):
  	return "X" + str(self.end.x) + "Y" + str(self.end.y)
