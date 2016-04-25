from parse import *
from triangle import *
import sys
"""
Emilee Urbanek and Nick Confrey
CMSC 22010: Digital Fabrication
Lab 3
Due: 4/25

---

The Main File -- slicer.py
This file holds all of the main logic to make the slicer run.
"""
class Parameters(object):
  """Class used to pass parameters to gcode parsing functions"""
  def __init__(self, filename, perimeterLayers, infill, layerHeight, thickness, support):
    self.stlfilename = filename
    self.gcodefilename = filename.split(".")[0] + ".gcode"
    self.perimeterLayers = perimeterLayers
    self.infill = infill
    self.layerHeight = layerHeight
    self.thickness = thickness
    self.support = support
    self.temperature = 210


def main():
  #Step 0: Parse user input to get constants
  filename, perimeterLayers, infill, layerHeight, thickness, support = parseInput()
  params = Parameters(filename, perimeterLayers, infill, layerHeight, thickness, support)
  
  #Step 1: Parse the STL into a list of triangles
  # TODO: force z's into multiples of the layerHeight
  triangles = parseSTL(filename)

  #Step 2: Sort the list of triangles by minZ
  triangles.sort(key=lambda x: x.z_min)

  # Find top of object (largest maxZ of triangles)
  top = max(triangles, key=lambda x: x.z_max).z_max

  #Step 3: Define a cutting plane (start at z = 0, increment by layer thickness)
  cuttingPlane = Plane()
  layer = 0.0
  # Iterate increasing the z value of the plane by layer thickness until = top

  trianglesConsidered = []
  # """Testing Data"""
  # p1 = Point3D(-1,3,0)
  # p2 = Point3D(1,5,0)
  # p3 = Point3D(0,0,0)
  # trianglesConsidered.append(Triangle([p1,p2,p3],Point3D([0,0,1])))

  while(layer <= top):
    #Step 4: Determine subset of triangles within cutting plane, throw rest away
    trianglesConsidered = filter(lambda x: (x.z_min <= layer) and (x.z_max >= layer), triangles)

    #Step 5: Run plane intersection test on each triangle, return a line segment
    segmentsPerLayer = []
    for triangle in trianglesConsidered:
      segmentsPerLayer.extend(triangle.intersectPlane(cuttingPlane, thickness))
    # What if the triangle is paralell to the plane??
      #Run special function to create line segments based on filament width
    # What if the triangle intersects at only one point??
      #line segment with start and end are the same
    # What if a triangle lies between two cutting planes?
      # check for intersections on the (previous, current] cutting planes interval
    # Store line segment x,y in a data structure (list?)
    print
    print "Layer #" + str(layer)
    for seggy in segmentsPerLayer:
        print str(seggy)
    #sorted insertion?
    #sort into different perimeters
    #Step 6: Arrange the line segments so they are contiguous, that one ends where the other begins
    #Step 7: Loop over all line segments in data structure, output print head moves in gcode
    # What about when there are multiple perameters per layer??
    # How to optimize non-printing head moves??
    #Step 8: Output gcode raise head by layer thickness

    #Loop until top
    layer += layerHeight
    cuttingPlane.up(layer)
  
  

  #others:
  # infill
  # supports
  # centering the object for gcode
  # different speeds for extrude/non-extrude moves
  # draw the circle around the object to get the extrusion going
  # support zhops on non-extrusion moves

if __name__ == "__main__":
  main()