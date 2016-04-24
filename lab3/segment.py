from point3d import *
import numpy

"""
Emilee Urbanek and Nick Confrey
CMSC 22010: Digital Fabrication
Lab 3
Due: 4/25

---

The line segment class
"""

class segment(object):
  def __init__(self, start, end):
  	self.start = start
  	self.end = end