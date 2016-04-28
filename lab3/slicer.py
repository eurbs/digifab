from parse import *
from triangle import *
from helpers import *
import gcode
import sys
"""
Emilee Urbanek and Nick Confrey
CMSC 22010: Digital Fabrication
Lab 3

---

The Main File -- slicer.py
This file holds all of the main logic to make the slicer run.
"""

def makePerimeter(segmentsPerLayer):
  if not segmentsPerLayer:
    print "can't make a perimeter without any segments :("
    return None

  #deep copy so we don't mess with the original list
  segments = list(segmentsPerLayer[1:])
  final = [[segmentsPerLayer[0]]]
  search = segmentsPerLayer[0].end
  circuitBreaker = 0
  #stores number of perimeters per layer we've found so far
  perimeterNumber = 0
  while segments:
    found = False
    for seg in segments:
      if seg.start.close(search):
        final[perimeterNumber].append(seg)
        segments.remove(seg)
        search = seg.end
        found = True
        break
      if seg.end.close(search):
        final[perimeterNumber].append(Segment(seg.end, seg.start, seg.perpIn))
        segments.remove(seg)
        search = seg.start
        found = True
        break
    if not found:
      perimeterNumber += 1
      final.append(segments[0])
      search = segments[0].end
      segments.pop(0)

    #to avoid infinite loops
    circuitBreaker += 1
    if(circuitBreaker > len(segmentsPerLayer)):
      raise Exception("Unable to find match for perimeter")
      break
  return final


def main():
  #Step 0: Parse user input to get constants
  params = parseInput()
  gfile = open(params.gcodefilename, "w")
  thickness = params.thickness
  
  #Step 1: Parse the STL into a list of triangles
  triangles = parseSTL(params.stlfilename)
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

  # GCODE
  gcode.generateSetup(gfile, params)
  while floatLE(layer, top):
    print "Layer #{:3.4}".format(layer)

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

    #Step 6: Arrange the line segments so they are contiguous, that one ends where the other begins
    perimeters = makePerimeter(segmentsPerLayer)

    #Step 7: Loop over all line segments in data structure, output print head moves in gcode
    #Step 8: Output gcode raise head by layer thickness
    print "generating gcode for layer {!s} perimeters".format(layer) # DEBUG
    gcode.generateGCode(gfile, params, layer, perimeters)

    print "generating gcode for case2 (parallel to cutting plane) triangles" # DEBUG
    gcode.generateGCodeParallel(gfile, params, layer, parallelTrianglesInLayer)

    #Loop until top
    layer += params.layerHeight
    cuttingPlane.up(layer)
  
  # Cleanup 
  gcode.generateCleanup(gfile) 
  gfile.close()

if __name__ == "__main__":
  main()