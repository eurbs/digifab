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

def main():
  #Step 0: Parse user input to get constants
  filename, infill, layerHeight, filamentThickness, support = parseInput()
  
  #Step 1: Parse the STL into a list of triangles
  triangles = parseSTL(filename)

  #Step 2: Sort the list of triangles by minZ
  triangles.sort(key=lambda x: x.z_min)

  # Find top of object (largest maxZ of triangles)
  triangles_dup = list(triangles)
  triangles_dup.sort(key=lambda x: x.z_max, reverse=True)
  top = triangles[0].z_max

  #Step 3: Define a cutting plane (start at z = 0, increment by layer thickness)
  cuttingPlane = Plane()
  layer = 0
  # Iterate increasing the z value of the plane by layer thickness until = top
  trianglesConsidered = []
  """Testing Data"""
  p1 = Point3D(-1,0,0)
  p2 = Point3D(1,0,0)
  p3 = Point3D(0,0,2)
  trianglesConsidered.append(Triangle([p1,p2,p3],Point3D([0,1,0])))
  while(layer <= top):
    #Step 4: Determine subset of triangles within cutting plane, throw rest away
    # TODO

    #Step 5: Run plane intersection test on each triangle, return a line segment
    for triangle in trianglesConsidered:
      print triangle.intersectPlane(cuttingPlane)
    # What if the triangle is paralell to the plane??
      #Run special function to create line segments based on filament width
    # What if the triangle intersects at only one point??
      #line segment with start and end are the same
    # What if a triangle lies between two cutting planes?
      # check for intersections on the (previous, current] cutting planes interval
    # Store line segment x,y in a data structure (list?)
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

if __name__ == "__main__":
  main()
