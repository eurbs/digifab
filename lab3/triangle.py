from point3d import *

"""
Emilee Urbanek
CMSC 22010: Digital Fabrication
Lab 3
Due: 4/25

---

The Triangle Class
In-memory representation of the STL triangles.
"""

class Triangle(object):
  def __init__(self, points, normal=[]):
    """
    Keyword arguments:
    points -- array of three point3Ds
    normal -- optional normal. Will calculate if not provided.
    """
    self.points = points
    if normal:
      self.normal = normal
    else:
      self.calculateNormal()
    # Experimental portion below
    # note: in a triangle, will there ever be a z lower or higher than a z
    #       in one of its three points? In other words, will the max z ever
    #       be along one of the line segments?
    #       Right now I'm assuming the min is in the top or bottom
    self.z_min = self._getMinZ()
    self.z_max = self._getMaxZ()

  def calculateNormal(self):
    """Calculates and sets normal of a triangle"""
    raise Exception("Given STL file without normals. Normal calculation not yet supported :(")

    # question: how do i figure out which is the outward facing normal
    # and which is the inside facing normal? Do I need to rely on the normals
    # provided to me? Do I just have to calculate both? how does this work?
    # http://mathworld.wolfram.com/NormalVector.html

  def _getMinZ(self):
    """Returns the minimum z value"""
    min_z = None
    for point in self.points:
      if min_z is None:
        min_z = point.z
      elif point.z < min_z:
        min_z = point.z
    return min_z

  def _getMaxZ(self):
    """Returns the maximum z value"""
    max_z = None
    for point in self.points:
      if max_z is None:
        max_z = point.z
      elif point.z > max_z:
        max_z = point.z
    return max_z

# NEXT UP -- LINE SEGMENT INTERSECTION FORMULA