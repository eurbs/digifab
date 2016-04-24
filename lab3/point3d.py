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

  def getArray(self):
    """Returns the array representation of the point with x,y,z respectively"""
    return [self.x, self.y, self.z]
