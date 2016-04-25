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
def makePerimeter(segmentsPerLayer):
  #What do perimeters look like for parallel layers??

  # COME BACK TO THIS IF THE NAIVE SOLUTION IS TOO SLOW
  # pieceDic = {}
  # puzzlePieces = []
  # final = []
  # for seg in segmentsPerLayer:
  #   if seg.getHashStringStart in pieceDic:
  #     puzzlePieces.append(list(seg.end, seg.start, pieceDic[seg.getHashStringStart]))
  #     del pieceDic[seg.getHashStringStart]
  #     continue
  #   if seg.getHashStringEnd in pieceDic:
  #     puzzlePieces.append(list(seg.start, seg.end, pieceDic[seg.getHashStringEnd]))
  #     del pieceDic[seg.getHashStringEnd]
  #     continue
  #   pieceDic[seg.getHashStringStart] = seg.end

  # for piece in puzzlePieces:

  #This is the slow solution

  #deep copy
  segments = list(segmentsPerLayer[1:])
  final = [segmentsPerLayer[0].start, segmentsPerLayer[0].end]
  search = segmentsPerLayer[0].end
  circuitBreaker = 0
  while segments:
    if(len(segments) == 1):
      break
    #print "Looking for " + str(search)
    for seg in segments:
      #print "Considering: " + str(seg)
      if(str(seg.start) == str(search)):
        #print "Found it! On line " + str(seg)
        #print "Adding " + str(seg.end)
        final.append(seg.end)
        segments.remove(seg)
        search = seg.end
        break
      if(str(seg.end) == str(search)):
        #print "Found it! On line " + str(seg)
        #print "Adding " + str(seg.start)
        final.append(seg.start)
        segments.remove(seg)
        search = seg.start
        break
    circuitBreaker += 1
    if(circuitBreaker > len(segmentsPerLayer)):
      raise Exception("Fucked")
      break
  return final

def main():
  #Step 0: Parse user input to get constants
  filename, infill, layerHeight, thickness, support = parseInput()
  
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
      #testing for the parallel case
      if(cuttingPlane.normal.z == abs(triangle.normal.z) and triangle.normal.x == 0 and triangle.normal.y == 0):
        triangle._parallelIntersection(thickness, triangle.normal.z)
      else:
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
    perimeter = makePerimeter(segmentsPerLayer)
    for boob in perimeter:
      print boob
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