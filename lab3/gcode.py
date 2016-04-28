import math
from point3d import Point3D
from parse import Parameters # this will probs be circular, put Parametes in parse.py
import sys
from helpers import *
from segment import *
"""
Emilee Urbanek and Nick Confrey
CMSC 22010: Digital Fabrication
Lab 3

---

The GCode file
This is supposed to generate GCode given perimeters......
I'm not even sure if it's going to be a class or not....
Handles layers and stuff and also setup and cleanup
"""

# ==============================================================================
# =============================== GCODE HELPERS ================================
# ==============================================================================

extruded = 0.0

def updateExtruded(increment):
  global extruded
  extruded += increment

def calculateExtrudeAmount(x1, y1, x2, y2, thickness):
  """Calculates the extrude amount moving from (x1, y1) to (x2, y2)"""
  dist = math.sqrt(math.pow(x2-x1, 2) + math.pow(y2-y1, 2))
  amt = thickness * dist / 1.75 # note: hard coded, todo: make thickness just be params
  return amt

def makeInfill(perimeters, infill, direction):
  """Returns a list of lists of points by either x or y coordinate from min to max"""
  # TODO: Support direction
  if(not perimeters):
    return None
  if(infill == 0):
    return None
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
  
  #increment = (1-infill)*((abs(maxY) - abs(minY))) + infill*layerThickness
  increment = layerThickness / infill

  if(increment < 0):
    raise Exception("increment is negative")
  #increment = 1

  scan = minY + increment

  while(scan <= maxY):
    scanLine = Segment(Point3D(minX, scan, 0), Point3D(maxX, scan, 0), None) # note: probably dangerous to have none
    lineHits = []
    for seggy in allSegments:
      intersect = scanLine.intersect2D(seggy)
      if intersect:
        lineHits.append(intersect)
    # final.append(list(deleteDuplicates(lineHits)))
    sortedLineHits = sorted(lineHits, key=lambda x: x.x)
    final.append(sortedLineHits)
    scan += increment
  return final

def resizePerimeters(params, perimeters, brim=False, raft=False):
  """Resizes perimeters using params.thickness toward the inside of that perimeter
  using the perpIn(dicular) unit vector to each segment in the perimeter.

  If brim or raft is specified, this will generate a brim or raft (cool right?)
  Note: brim and raft not yet functional (less cool)
  """
  if brim:
    raise Exception("brim not yet supported") # TODO
  if raft:
    raise Exception("raft not yet supported") # TODO

  thickness = params.thickness / 2.0
  new_perimeters = []
  for perimeter in perimeters:
    new_seggies = []
    for seggy in perimeter: # Make copies to populate  
      new_seggies.append(Segment(None, None, seggy.perpIn))

    for i in xrange(len(perimeter)): # Start point translation algorithm
      seggy1 = perimeter[i]
      seggy2 = perimeter[(i+1)%len(perimeter)]
      new_seggy1 = new_seggies[i]
      new_seggy2 = new_seggies[(i+1)%len(new_seggies)] # len perimeter and new_seggies should be same
      # if seggy1.end != seggy2.start:
        # raise Exception("Found neighboring segments in perimeter which don't share a point")
        # print seggy1.end
        # print seggy2.start
        # Considering the float imperfections and the imperfections in perimeter handling
        # we ignore this error. We'll consider the end point of the first segment. If the
        # points printed are really different though, that indicates a bigger problem.
      point2d = [seggy1.end.x, seggy1.end.y]  # is the same as seggy2.y
      # Find unit vector of distance thickness from the origin in direction of perpendicular
      trans_end1 = map(lambda x: x * thickness, seggy1.perpIn)
      trans_start2 = map(lambda x: x * thickness, seggy2.perpIn)
      trans_amt = map(lambda x, y: x + y, trans_end1, trans_start2)
      new_point2d = map(lambda x, y: x + y, point2d, trans_amt)
      # Populate the new segments with translated point
      new_seggy1.end = Point3D(new_point2d[0], new_point2d[1], float(0))
      new_seggy2.start = Point3D(new_point2d[0], new_point2d[1], float(0))
    new_perimeters.append(new_seggies)
  return new_perimeters

# ==============================================================================
# ========================= GCODE GENERATION FUNCTIONS =========================
# ==============================================================================

# TODO: FORMAT ALL X AND Y CODES TO {:3.3f} and E CODES TO {:3.5f}.

def generateSetup(gfile, params):
  """Generates the setup GCode preceeding all of the printing

  Keyword arguments:
  gfile -- A file already open for writing the gcode to
  params -- a Parameters class filled with the parameters specified by user
  """
  gfile.write("; Generated by Nick&Em's Slycer at 'I'm too lazy to import datetime'C\n")
  gfile.write("\n")

  gfile.write("; Perimeter Layers: {}\n".format(params.perimeterLayers))
  gfile.write("; Infill: {}%%\n".format(params.infill * 100))
  gfile.write("; Layer Height: {}mm\n".format(params.layerHeight))
  gfile.write("; Nozzle Size: {}mm\n".format(params.thickness))
  gfile.write("; Support {}\n".format("On" if params.support else "Off"))
  gfile.write("; Temperature {} degrees C\n".format(params.temperature))
  gfile.write("\n")

  gfile.write("; SETUP\n")
  lines = [
    "M107 ; fan off",
    "M104 S{} ; set temperature".format(params.temperature),
    "G28 X0 Y0 Z0 ; home all axes",
    "G1 Z5 F5000 ; lift nozzle",
    "",
    "M109 S{} ; wait for temperature to be reached".format(params.temperature),
    "G21 ; set units to millimeters",
    "G90 ; use absolute coordinates",
    "M82 ; use absolute distances for extrusion",
    "G1 Z{:1.3f} F2400 ; put printhead at good distance from bed".format(params.thickness),
    "G92 E0",
    "G29 ; idk but cura does this to touch the corners",
    # right here, we want to find an appropriate place to set the 0 for x and y
    # we want to move there (G1) and then set it as 0 (G92 X0 Y0 Z0)
    ""
  ]
  gfile.write("\n".join(lines))

def generateGCodePerim(gfile, params, perimeter):
  lines = []
  first_point =  perimeter[0].start
  lines.append("G1 X{:3.6f} Y{:3.6f}".format(first_point.x, first_point.y)) # move no extrude
  for seggy in perimeter:
    point_start = seggy.start
    point_end = seggy.end
    extrude_amount = calculateExtrudeAmount(
      point_start.x, point_start.y, point_end.x, point_end.y, params.thickness)
    updateExtruded(extrude_amount)
    # move with extrude
    lines.append("G1 X{:3.6f} Y{:3.6f} E{:3.6f}".format(point_end.x, point_end.y, extruded))
  lines.append("")
  gfile.write("\n".join(lines)) 

def generateGCodeInfill(gfile, params, layerZ, perimeters):
  """Given a gfile, parameters, and a list of perimeters, generate gcode for infill"""
  # Determine if horizontal or vertical infill
  if isclose(layerZ % params.layerHeight, 0.0):
    direction = "horizontal"
  else:
    direction = "vertical"

  # Generate the GCode for the infill
  lines = []
  lines.append("; INFILL")
  infill = makeInfill(perimeters, params.infill, direction)
  for points in infill:
    lines.append("; NEW INFILL LINE")
    if not points:
      continue
    # move to start point
    lines.append("G1 X{:3.6f} Y{:3.6f}".format(points[0].x, points[0].y))
    for i in xrange(len(points)-1):
      start = points[i]
      end = points[i+1]
      if i % 2 == 0: # We're inside, so extrude
        extrude_amount = calculateExtrudeAmount(start.x, start.y, end.x, end.y, params.thickness)
        updateExtruded(extrude_amount)
        lines.append("G1 X{:3.3f} Y{:3.3f} E{:3.5f}".format(end.x, end.y, extruded))
      else: # We're outside, so don't extrude
        lines.append("G1 X{:3.3f} Y{:3.3f}".format(end.x, end.y))
  lines.append("")
  gfile.write("\n".join(lines))

def generateGCode(gfile, params, layerZ, perimeters):
  """Generates the setup GCode preceeding all of the printing

  Keyword arguments:
  gfile -- A file already open for writing the gcode to
  params -- a Parameters class filled with the parameters specified by user
  layerZ -- The Z height of the current layer (relative to origin)
  perimeters -- A list of lists of segments represeting perimeters passed in by slicer.py 
  """
  if not perimeters:
    print "warn: No perimeters passed at layer Z={}. GCode not generated.".format(layerZ)
    return

  gfile.write("; LAYER Z={:3.6f}\n".format(layerZ))
  gfile.write("G1 Z{:3.6f} ; raise print head\n".format(layerZ))

  # --- Generate List of concentric perimeters ---
  concentricPerimeters = []
  concentricPerimeters.append(perimeters)
  for i in xrange(params.perimeterLayers):
    # This includes appending an extra perimeter to be passed to the infill generator
    concentricPerimeters.append(resizePerimeters(params, concentricPerimeters[i]))

  # We're iterating down the columns of concentric perimeters
  for j in xrange(len(concentricPerimeters[0])):
    # We're not going to do the infill perimeter until after all perimeters are done
    gfile.write("; PERIMETER {}\n".format(j))
    for i in xrange(len(concentricPerimeters)-1):
      generateGCodePerim(gfile, params, concentricPerimeters[i][j])

  # --- Generate the code for the infill ---
  if params.infill*100 != 0:
    infill_perimeters = concentricPerimeters.pop() # Pops off last element
    generateGCodeInfill(gfile, params, layerZ, infill_perimeters)
  return

def generateGCodeParallel(gfile, params, layerZ, parallelTriangleSegments):
  """Generates the GCode for triangles that were found that are parallel to
     the cutting plane. This is only ever called AFTER generateGCode as it
     handles an edge case

  Keyword arguments:
  gfile -- A file already open for writing the gcode to
  params -- a Parameters class filled with the parameters specified by user
  layerZ -- The Z height of the current layer (relative to origin)
  parallelTriangleSegments -- A list of lists of line segments represeting the rasterized 
                              area of a triangle parallel to the cutting plane
  """
  # TODO: handle parallel these areas as arbitrarily filled polygons rather than
  #       as raster filled triangles.
  if not parallelTriangleSegments:
    return

  lines = []
  for segments in parallelTriangleSegments:
    lines.append("; Parallel rasterized triangle on layer {}".format(layerZ))
    for seggy in segments:
      # move to start point
      lines.append("G1 X{:3.6f} Y{:3.6f}".format(seggy.start.x, seggy.start.y)) 
      # update extrude amount according to the move we're about to make
      extrude_amount = calculateExtrudeAmount(
        seggy.start.x, seggy.start.y, seggy.end.x, seggy.end.y, params.thickness)
      updateExtruded(extrude_amount)
      # extrude to end point
      lines.append("G1 X{:3.6f} Y{:3.6f} E{:3.6f}".format(seggy.end.x, seggy.end.y, extruded))
  lines.append("")
  gfile.write("\n".join(lines))
  return

def generateCleanup(gfile):
  lines = [
    "; CLEANUP",
    "M104 S0 ; turn off heat",
    "G91 ; relative positioning",
    "G1 E-1 F300 ; retract the filament before lifting nozzle",
    "G1 Z+0.5 E-3 X-20 Y-20 F4200 ;move Z up a bit and retract filament more",
    "G28 X0 Y0 ; move X/Y to min endstops, moving head out of the way",
    "M84 ; disable motors",
    "G90 ; absolute positioning",
    ""
  ]
  gfile.write("\n".join(lines))

def test():
  """Because we're not using a real testing framework"""
  params = Parameters(filename="notused", perimeterLayers=3, infill=.20,
                      layerHeight=.19, thickness=0.4, support=False)

  # Test data from layer 0.19 of the 3mmBox
  perimeter = [
    Segment(Point3D(.19, 0.0, .19), Point3D(0.0, 0.0, .19), [0.0, 1.0]),
    Segment(Point3D(0.0, 0.0, 0.19), Point3D(0.0, 0.19, .19), [1.0, 0.0]),
    Segment(Point3D(0.0, .19, .19), Point3D(0.0, 15.0, .19), [1.0, 0.0]),
    Segment(Point3D(0.0, 15.0, .19), Point3D(14.810, 15.0, .19), [0.0, -1.0]),
    Segment(Point3D(14.810, 15.0, .19), Point3D(15.0, 15.0, .19), [0, -1.0]),
    Segment(Point3D(15.0, 15.0, .19), Point3D(15.0, 14.81, .19), [-1.0, 0.0]),
    Segment(Point3D(15.0, 14.81, .19), Point3D(15.0, 0.0, .19), [-1.0, 0.0]),
    Segment(Point3D(15.0, 0.0, .19), Point3D(0.19, 0.0, .19), [0.0, 1.0])
  ]
  perimeters = [perimeter]
  print "=============== testing perimeter resizing ==============="
  map(printFunc, resizePerimeters(params, perimeters)[0])

  print "=============== TEsting gcode Generation ==============="
  with open("test_gcode.gcode", "w") as gfile:
    generateSetup(gfile, params)
    generateGCode(gfile, params, 0.19, perimeters)
    generateCleanup(gfile)

  print "success"

if __name__ == "__main__":
  test()