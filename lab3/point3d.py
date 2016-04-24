import operator

"""This section is for things that belong in different files"""
# Python 2 equivalent for enums for indexing into arrays of x, y, and z
X = 0
Y = 1
Z = 2

class Point3D(object):
  def __init__(self, x, y, z):
    self.x = x
    self.y = y
    self.z = z

    self.a = [self.x, self.y, self.z]

  def getArray(self):
    """Returns the array representation of the point with x,y,z respectively"""
    return self.a

  def sub(self, other):
    p3 = map(operator.sub, self.a, other.a)
    return Point3D(p3[0], p3[1], p3[2])