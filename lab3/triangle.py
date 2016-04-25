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

    self.z_min = self._getMinZ()
    self.z_max = self._getMaxZ()

  def __str__(self):
    return "triangle:\n\tnormal: {!s}\n vertices:\n\t{!s}\n\t{!s}\n\t{!s}".format(
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

  def _getMinY(self):
    """Returns the minimum y value"""
    min_y = None
    for point in self.points:
      if min_y is None:
        min_y = point.y
      elif point.y < min_y:
        min_y = point.y
    return min_y

  def _getMaxY(self):
    """Returns the maximum y value"""
    max_y = None
    for point in self.points:
      if max_y is None:
        max_y = point.y
      elif point.y > max_y:
        max_y = point.z
    return max_y

  def _segmentPlaneIntersection(self, p1, p2, plane):
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
      #print "Both on plane error"
      return pointsOnPlane

    #if the points are on the same side of the plane, there can be no intersection
    #print "d1 is " + str(d1) + " d2 is " + str(d2)
    if(d1*d2 > espilon):
      #print "Same side of plane error"
      return pointsOnPlane

    place = d1 / (d1 - d2)
    # P1 + place * (P2 - P1)
    temp1 = numpy.subtract(p2.a, p1.a)
    temp2 = numpy.multiply(temp1, place)
    pointsOnPlane.append(Point3D(list(numpy.add(p1.a, temp2))))
    return pointsOnPlane

  def _fillBottomFlatTriangle(self, v1, v2, v3, z, thickness):
    lineSeggies = []
    inverseSlope1 = (v2.x - v1.x) / (v2.y - v1.y)
    inverseSlope2 = (v3.x - v1.x) / (v3.y - v1.y)

    countingX1 = v1.x
    countingX2 = v1.x
    scanLineY = v1.y
    #print "v1 " + str(v1.y) + " v2 " + str(v2.y)
    while(scanLineY >= v2.y): # emilee: flipped sign? more bugs? i told you so.
      start = Point3D(countingX1, scanLineY, z)
      end = Point3D(countingX2, scanLineY, z)
      #print "start: " + str(start) + "end: " + str(end)
      lineSeggies.append(Segment(start, end))

      countingX1 += inverseSlope1
      countingX2 += inverseSlope2
      #This might be broken here... good place to come back to
      #Do i need to multiply the slope by thickness? does each step step enough
      scanLineY -= thickness  # emilee: i told you so
    return lineSeggies

  def _fillTopFlatTriangle(self, v1, v2, v3, z, thickness):
    lineSeggies = []
    inverseSlope1 = (v3.x - v1.x) / (v3.y - v1.y)
    inverseSlope2 = (v3.x - v2.x) / (v3.y - v2.y)

    countingX1 = v3.x
    countingX2 = v3.x
    scanLineY = v3.y
    while(scanLineY < v1.y):
      start = Point3D(countingX1, scanLineY, z)
      end = Point3D(countingX2, scanLineY, z)
      lineSeggies.append(Segment(start, end))

      countingX1 -= inverseSlope1
      countingX2 -= inverseSlope2
      #This might be broken here... good place to come back to
      #Do i need to multiply the slope by thickness? does each step step enough
      scanLineY += thickness
    return lineSeggies

  def _parallelIntersection(self, thickness, z):
    """
    Create line segments across the entire triangle.
    All line segments start from negative x and end from a more positive x
    Raster up y
    """
    #Sort by assending y coordinates so v1 is the top
    self.points.sort(key=lambda p: p.y, reverse=True)

    #check for trivial case of flat bottom triangle
    if(self.points[1].y == self.points[2].y):
      return self._fillBottomFlatTriangle(self.points[0], self.points[1], self.points[2], z, thickness)
    if(self.points[0].y == self.points[1].y):
      return self._fillTopFlatTriangle(self.points[0], self.points[1], self.points[2], z, thickness)

    #Else for the general case need to split the triangle into a topper and a bottomer
    v4x = (self.points[0].x + ((float)(self.points[1].y - self.points[0].y) / (self.points[2].y - self.points[0].y)) * (self.points[2].x - self.points[0].x))
    v4 = Point3D(v4x, self.points[1].y, z)
    lineSeggies = self._fillBottomFlatTriangle(self.points[0], self.points[1], v4, z, thickness)
    lineSeggies.extend(self._fillTopFlatTriangle(self.points[1], v4, self.points[2], z, thickness))
    return lineSeggies

  def intersectPlane(self, plane, thickness):
    if(plane.normal.z == self.normal.z and self.normal.x == 0 and self.normal.y == 0):
      return self._parallelIntersection(thickness, self.normal.z)

    pointsOnPlane = []
    #print "Points 1 and 2:"
    pointsOnPlane.extend(self._segmentPlaneIntersection(self.points[0], self.points[1], plane))
    #print "Points 2 and 3:"
    pointsOnPlane.extend(self._segmentPlaneIntersection(self.points[1], self.points[2], plane))
    #print "Points 3 and 0:"
    pointsOnPlane.extend(self._segmentPlaneIntersection(self.points[2], self.points[0], plane))
    deleteDupes = set(pointsOnPlane)
    #print pointsOnPlane
    if(len(deleteDupes) > 2):
      raise Exception("Too many points to define a line segment in triangle: " + str(self.points))
    seggy = list(deleteDupes)
    if(len(seggy) == 0):
      # triangle does not intersect plane
      return None
    if(len(seggy) == 1):
      # triangle intersects plane at single point
      return [Segment(seggy[0], seggy[0])]
    return [Segment(seggy[0], seggy[1])]


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
