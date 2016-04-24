from triangle import *
"""
Emilee Urbanek and Nick Confrey
CMSC 22010: Digital Fabrication
Lab 3
Due: 4/25

---

Parsing functions
"""

def parseSTL(filename):
  """Given a filename in the cwd, opens file and parses STL.
  Currently, we only support ASCII STL files with proper normals.
  The ASCII STL file may have either decimal or scientific notation style.
  Assumes well formatted STL files.

  returns: list of Triangles.
  """
  triangles = []
  points = []
  normal = None
  with open(filename, 'r') as f:
    for line in f:
      contents = line.split()
      if contents[0] == "vertex":
        vertex = Point3D(float(contents[1]), float(contents[2]), float(contents[3]))
        points.append(vertex)
      elif contents[0] == "facet":
        normal = Point3D(float(contents[2]), float(contents[3]), float(contents[4]))
      elif contents[0] == "endfacet":
        triangles.append(Triangle(points, normal))
        # Reset for next iteration
        points = []   # Can't wait to move to python 3.3, points.clear() would work
        normal = None
  return triangles

def printFunc(x):
  """Since Python2 doesn't have a print function"""
  print x

def test():
  triangles = parseSTL("samples/3mmBox.stl")
  temp = map(printFunc, triangles)

if __name__ == "__main__":
  test()
