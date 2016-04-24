from point3d import *
from segment import *
from plane import *

"""
Emilee Urbanek and Nick Confrey
CMSC 22010: Digital Fabrication
Lab 3
Due: 4/25

---

The Triangle Class
In-memory representation of the STL triangles.
"""

class Triangle(object):
  def __init__(self, points, normal=None):
    """
    Keyword arguments:
    points -- array of three point3Ds
    normal -- optional normal (point3D type).
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

  def __str__(self):
    return "normal: {!s}\n vertices:\n\t{!s}\n\t{!s}\n\t{!s}".format(
      self.normal, self.points[0], self.points[1], self.points[2])

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

  def _segmentPlaneIntersection(p1, p2, plane):
    """ Used as a helper in plane triangle intersection """
    #an arbitrary small number to deal with numerical percision issues
    espilon = 0.001
    pointsOnPlane = []

    d1 = plane.distanceFrom(p1)
    d2 = plane.distanceFrom(p2)
    d1OnPlane = abs(d1) < espilon
    d2OnPlane = abs(d2) < espilon

    if(d1OnPlane):
      pointsOnPlane.append(p1)
    if(d2OnPlane):
      pointsOnPlane.append(p2)
    if(d2OnPlane and d1OnPlane):
      return pointsOnPlane

    #if the points are on the same side of the plane, there can be no intersection
    if(d1*d2 > espilon):
      return pointsOnPlane

    place = d1 / (d1 - d2)
    pointsOnPlane.append(P1 + place * (p2 - p1))
    return pointsOnPlane

  def intersectPlane(self, plane):
    pointsOnPlane = []
    pointsOnPlane.extend(_segmentPlaneIntersection(self.points[0], self.points[1]))
    pointsOnPlane.extend(_segmentPlaneIntersection(self.points[1], self.points[2]))
    pointsOnPlane.extend(_segmentPlaneIntersection(self.points[2], self.points[0]))
    deleteDupes = set(pointsOnPlane)
    if(len(deleteDupes) > 2):
      raise Exception("Too many points to define a line segment in triangle: " + self.points)
    return segment(deleteDupes[0], deleteDupes[1])


def test():
  """Test function in the case we don't use unittest or mock"""
  normal = Point3D(0, 0, 1)
  points = [Point3D(1, 1, 0), Point3D(1, 2, 0), Point3D(2, 1, 0)]
  triangle = Triangle(points, normal)
  print "--------------printing type of triangle object--------------"
  print type(triangle)
  print "--------------printing triangle--------------"
  print triangle
  print "--------------trying to initialize with no normal--------------"
  triangle2 = Triangle(points) # should throw exception

if __name__ == "__main__":
  test()