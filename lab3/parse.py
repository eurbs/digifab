from helpers import *
from triangle import *
import argparse
import sys
"""
Emilee Urbanek and Nick Confrey
CMSC 22010: Digital Fabrication
Lab 3

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
    self.filamentThickness = 1.75


def parseInput():
  parser = argparse.ArgumentParser()
  parser.add_argument("path", action="store",
                      help="path to the stl file")
  parser.add_argument("--perimeterlayers", action="store", type=int, default=2,
                      help="number of perimeter layers, default: 2")
  parser.add_argument("--infill", action="store", type=int, default=20,
                      help="number from 0 to 100 for %%infill, default: 20")
  parser.add_argument("--layerHeight", action="store", type=float, default=0.19,
                      help="layer height in mm, default: 0.19")
  parser.add_argument("--headdiameter", action="store", type=float, default=0.4,
                      help="diameter of print head in mm, default: 0.4")
  parser.add_argument("--support", action="store_true", default=False,
                      help="use this flag if you need support. (not supported)")


  args = parser.parse_args()

  params = Parameters(filename=args.path, 
                      perimeterLayers=args.perimeterlayers,
                      infill=(float(args.infill)/100.0),
                      layerHeight=args.layerHeight,
                      thickness=args.headdiameter,
                      # support=args.support) # note: not supported
                      support=False)

  return params

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
        triangle = Triangle(points, normal)
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
