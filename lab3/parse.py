from helpers import *
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
class Parameters(object):
  """Class used to pass parameters to gcode parsing functions"""
  def __init__(self, filename, perimeterLayers, infill, layerHeight, thickness, support):
    # TODO: should handle defaults here instead of in parse.py
    self.stlfilename = filename
    self.gcodefilename = filename.split(".")[0] + ".gcode"
    self.perimeterLayers = perimeterLayers
    self.infill = infill
    self.layerHeight = layerHeight
    self.thickness = thickness
    self.support = support
    self.temperature = 210


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
  # TODO: properly parse options
  perimeterLayers = 2
  infill = 0.20
  layerHeight = 0.19
  thickness = 0.4     # thickness of the filament when extruded (size of nozzle)
  support = False

  return (args.path, perimeterLayers, infill, layerHeight, thickness, support)

def round3Decimal(f):
  """Rounds to 3 decimal places"""
  # return float("{:.3f}".format(f))
  # TODO: allow truncation. right not too tired and too afraid that it will mess nick's thing up
  return float(f)

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
        vertex = Point3D(round3Decimal(float(contents[1])),
                         round3Decimal(float(contents[2])), 
                         round3Decimal(float(contents[3])))
        points.append(vertex)
      elif contents[0] == "facet":
        normal = Point3D(round3Decimal(float(contents[2])),
                         round3Decimal(float(contents[3])),
                         round3Decimal(float(contents[4])))
      elif contents[0] == "endfacet":
        triangle = Triangle(points, normal)
        # TODO: analyze the triangle and move things to cutting plane
        triangles.append(Triangle(points, normal))
        # Reset for next iteration
        points = []   # Can't wait to move to python 3.3, points.clear() would work
        normal = None
  return triangles

def test():
  print "--------------parsing stl--------------"
  triangles = parseSTL("samples/3mmBox.stl")
  print "--------------printing parsed stl--------------"
  temp = map(printFunc, triangles)
  print "--------------parsing commandline args--------------"
  filename, infill, layerHeight, filamentThickness, support = parseInput()
  print "filename: {}".format(filename)
  print "infill: {}".format(infill)
  print "layer height: {}mm".format(layerHeight)
  print "filament thickness: {}mm".format(filamentThickness)
  print "support: {}".format(support)

if __name__ == "__main__":
  test()
