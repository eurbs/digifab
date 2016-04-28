from parse import *
from triangle import *
from helpers import *
import gcode
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

  if(not segmentsPerLayer):
    print "FUUUUCK"
    return None

  #deep copy so we don't mess with the original list
  segments = list(segmentsPerLayer[1:])
  final = [[segmentsPerLayer[0]]]
  search = segmentsPerLayer[0].end
  circuitBreaker = 0
  #stores number of perimeters per layer we've found so far
  perimeterNumber = 0
  while segments:
    #print "Looking for " + str(search)
    found = False
    for seg in segments:
      #print "Considering: " + str(seg)
      if(seg.start.close(search)):
        #print "Found it! On line " + str(seg)
        #print "Adding " + str(seg.end)
        final[perimeterNumber].append(seg)
        segments.remove(seg)
        search = seg.end
        found = True
        break
      if(seg.end.close(search)):
        #print "Found it! On line " + str(seg)
        #print "Adding " + str(seg.start)
        final[perimeterNumber].append(Segment(seg.end, seg.start))
        segments.remove(seg)
        search = seg.start
        found = True
        break
    if(not found):
      perimeterNumber += 1
      final.append(segments[0])
      search = segments[0].end
      segments.pop(0)

    #to avoid infinite loops
    circuitBreaker += 1
    if(circuitBreaker > len(segmentsPerLayer)):
      raise Exception("Unable to find match for perimeter")
      break

  # append first point of each perimeter to end of list
  # for each perimeter, make sure that the start and end point are the same
  #for i in xrange(len(final)):
  #  final[i].append(final[i][0])

  return final

def pointsToSegments(perimeter):
  segments = []
  for i, point in enumerate(perimeter[:-1]):
    segments.append(Segment(point, perimeter[i+1]))
  return segments

#return type: list of lists of points by either x or y coordinate
#from min to max y
def makeInfill(perimeters, infill, direction):
  final = []
  allSegments = []
  maxY = perimeters[0][0].start.y
  minY = perimeters[0][0].start.y 
  maxX = perimeters[0][0].start.x
  minX = perimeters[0][0].start.x
  for perimeter in perimeters:
    for segment in perimeter:
      maxY = max(maxY, max(segment.start.y, segment.end.y))
      minY = min(minY, min(segment.start.y, segment.end.y))
      maxX = max(maxX, max(segment.start.x, segment.end.x))
      minX = min(minX, min(segment.start.x, segment.end.x))
      allSegments.append(segment)

  #linear interpolation between 0-100% infill
  layerThickness = .4
  increment = layerThickness + infill*(layerThickness - (maxY - minY))
  increment = 1
  print "increment is: " + str(increment)
  #Optimize: is there a pretty way to get both of these in one pass?
  # maxY = max(perm, key=lambda seg: max(seg.start.y, seg.end.y))
  # minY = min(perm, key=lambda seg: min(seg.start.y, seg.end.y))
  # maxX = max(perm, key=lambda seg: max(seg.start.x, seg.end.x))
  # minX = min(perm, key=lambda seg: min(seg.start.x, seg.end.x))

  scan = minY + increment
  print "starting at y = " + str(minY)
  #segmentsConsidered = []
  while(scan <= maxY):
    scanLine = Segment(Point3D(minX, scan, 0), Point3D(maxX, scan, 0))
    #segmentsConsidered = filter(lambda x: floatLE(x.start.y, scanLine) and floatGE(x.z_max, scanLine), perm)
    lineHits = []
    for seggy in allSegments:
      intersect = scanLine.intersect2D(seggy)
      if(intersect):
        lineHits.append(intersect)
    if(not lineHits):
      print "Y value failure: " + str(scan)
      raise Exception("Uhoh! The infill finder did not find a inside part.")
    final.append(lineHits)
    scan += increment
  return final

def main():
  #Step 0: Parse user input to get constants
  filename, perimeterLayers, infill, layerHeight, thickness, support = parseInput()
  params = Parameters(filename, perimeterLayers, infill, layerHeight, thickness, support)
  gfile = open(params.gcodefilename, "w") # note: this is NOT good. should open and close each time I want to write to it. to do this, we open in "a" or append mode rather than "w" or write mode
  
  #Step 1: Parse the STL into a list of triangles
  triangles = parseSTL(filename)

  # TODO: force z's into multiples of the layerHeight
  # note: below should solve the todo.
  for triangle in triangles:
    triangle.adjustToCuttingPlane(params.layerHeight)

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

  gcode.generateSetup(gfile, params)
  while floatLE(layer, top):
    print
    print "Layer #" + str(layer)
    #Step 4: Determine subset of triangles within cutting plane, throw rest away
    trianglesConsidered = filter(
      lambda x: floatLE(x.z_min, layer) and floatGE(x.z_max, layer), triangles)

    #Step 5: Run plane intersection test on each triangle, return a line segment
    segmentsPerLayer = []
    parallelTrianglesInLayer = [] # list of lists of segments
    for triangle in trianglesConsidered:
      #testing for the parallel case
      if(cuttingPlane.normal.z == abs(triangle.normal.z) and triangle.normal.x == 0 and triangle.normal.y == 0):
        # THIS IS WHERE YOU WOULD DO SOMETHING WITH THE RASTER LAYER
        parallelTrianglesInLayer.append(
          triangle._parallelIntersection(thickness, triangle.normal.z))
      else:
        segmentsPerLayer.extend(triangle.intersectPlane(cuttingPlane, thickness))
    # What if the triangle is paralell to the plane??
      #Run special function to create line segments based on filament width
    # What if the triangle intersects at only one point??
      #line segment with start and end are the same
      #note: nick says he got rid of the handling of single points. emilee gave the example of the tip of a triangle. If we want this to be complete, we should fix this. (falls into group 3 of the triangle intersection examples)
    # What if a triangle lies between two cutting planes?
      # check for intersections on the (previous, current] cutting planes interval
    # Store line segment x,y in a data structure (list?)

    # for seggy in segmentsPerLayer:
    #     print str(seggy)
    #sorted insertion?
    #sort into different perimeters

    #Step 6: Arrange the line segments so they are contiguous, that one ends where the other begins
    # note: RUNNING INTO PROBLEMS WITH THE SPHERE
    perimeters = makePerimeter(segmentsPerLayer)
    # if(perimeters == None):
    #   layer += layerHeight
    #   cuttingPlane.up(layer)
    #   continue # there's a magical floating object!
    if perimeters:
      for i,perm in enumerate(perimeters): # DEBUG (for loop)
        print "Perimeter #" + str(i)
        for per in perm:
          print "\t " + str(per)

    infillList = makeInfill(perimeters, .50, "blah")
    for i,fill in enumerate(infillList):
      print "Layer #" + str(i)
      for point in fill:
        print "\t" + str(point)
    break
    print "generating gcode for layer {!s} perimeters".format(layer) # DEBUG
    gcode.generateGCode(gfile, params, layer, perimeters)
    #makeInfill(perimeters)

    print "generating gcode for case2 (parallel to cutting plane) triangles" # DEBUG
    gcode.generateGCodeParallel(gfile, params, layer, parallelTrianglesInLayer)



    #Step 7: Loop over all line segments in data structure, output print head moves in gcode
    # What about when there are multiple perameters per layer??
    # How to optimize non-printing head moves??
    #Step 8: Output gcode raise head by layer thickness

    #Loop until top
    layer += layerHeight
    cuttingPlane.up(layer)
  
  # Cleanup 
  gcode.generateCleanup(gfile) 
  gfile.close()

  #others:
  # infill
  # supports
  # centering the object for gcode
  # different speeds for extrude/non-extrude moves
  # draw the circle around the object to get the extrusion going
  # support zhops on non-extrusion moves
  # avoid overlaps in perimeters (when drawing, the final point is shorter by .4mm)

if __name__ == "__main__":
  main()