from triangle import *
import argparse
"""
Emilee Urbanek and Nick Confrey
CMSC 22010: Digital Fabrication
Lab 3
Due: 4/25

---

Parsing functions
"""
def parseInput():
  parser = argparse.ArgumentParser()
  parser.add_argument("path", help="path to the stl file (just the filename if in cwd)")
  # parser.add_argument(
    # "--layer_height", type=float, help="set the layer height; default is 0.19mm", default=0.19)
  # parser.add_argument("--infill", type=int, help="set infill; default is 20%", default=20)
  # parser.add_argument("--infill", help="set infill; default is 20%", action="store_const", const=)
  # parser.add_argument("")
  args = parser.parse_args()

  # do defaults for now, worry about parsing properly later
  infill = 0.20
  layerHeight = 0.19
  filamentThickness = 1.75
  support = False

  return (args.path, infill, layerHeight, filamentThickness, support)


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
  # triangles = parseSTL("samples/3mmBox.stl")
  # temp = map(printFunc, triangles)
  parseInput()

if __name__ == "__main__":
  test()
