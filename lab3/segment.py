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
