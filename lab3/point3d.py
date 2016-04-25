import operator

"""This section is for things that belong in different files"""
# Python 2 equivalent for enums for indexing into arrays of x, y, and z
X = 0
Y = 1
Z = 2

class Point3D(object):
  """Note: Don't know how to make immutable classes, but Point3D's should be
           treated as though they are immutable
  """
  def __init__(self, *args):
    """Either can be constructed with a list of 3 numbers or 3 numbers"""
    if len(args) == 3:
      points = [args[0], args[1], args[2]]
    elif isinstance(args[0], list) and len(args[0]) == 3:
      points = args[0]
    else:
      raise Exception("Unacceptable arguments passed to Point3D constructor")
    
    self.x = float(points[0])
    self.y = float(points[1])
    self.z = float(points[2])
    self.a = [self.x, self.y, self.z]

  def __str__(self):
    return "point: {:.5f} {:.5f} {:.5f}".format(self.x, self.y, self.z)

  def __hash__(self):
    return hash(str(self))

  def __eq__(self, other):
    """Assumes other is a Point3D as well"""
    return (self.x == other.x) and (self.y == other.y) and (self.z == other.z)

  def getArray(self):
    """Returns the array representation of the point with x,y,z respectively"""
    return self.a

  def sub(self, other):
    p3 = map(operator.sub, self.a, other.a)
    return Point3D(p3[0], p3[1], p3[2])


def test():
  """Test function in the case we don't use unittest or mock"""
  point = Point3D(1, 2, 3)
  print "--------------printing type of point--------------"
  print type(point)
  print "--------------printing a Point3D--------------"
  print point
  print "--------------testing hashability--------------"
  point_set = set()
  point_set.add(point)
  point_set.add(Point3D(1, 2, 3))
  print "hashability is good: {}".format(len(point_set) == 1)

if __name__ == "__main__":
  test()
