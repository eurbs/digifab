import math
from point3d import Point3D
from parse import Parameters # this will probs be circular, put Parametes in parse.py
"""
Emilee Urbanek and Nick Confrey
CMSC 22010: Digital Fabrication
Lab 3
Due: 4/25

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
  # TODO: this is messed up somehow
  dist = math.sqrt(math.pow(x2-x1, 2) + math.pow(y2-y1, 2))
  amt = thickness * dist
  return amt



# ==============================================================================
# ========================= GCODE GENERATION FUNCTIONS =========================
# ==============================================================================

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


def generateGCode(gfile, params, layerZ, perimeters):
  """Generates the setup GCode preceeding all of the printing

  Keyword arguments:
  gfile -- A file already open for writing the gcode to
  params -- a Parameters class filled with the parameters specified by user
  layerZ -- The Z height of the current layer (relative to origin)
  perimeters -- A list of lists of points represeting perimeters passed in by slicer.py 
  """

  gfile.write("; LAYER Z={:3.3f}\n".format(layerZ))
  gfile.write("G1 Z{:3.3f} ; raise print head\n".format(layerZ))
  lines = []
  # TODO: handle parallel "perimeters" (actually areas)
  for i, perim in enumerate(perimeters):
    lines.append("; PERIMETER {}".format(i))
    first_point =  perim[0]
    lines.append("G1 X{:3.3f} Y{:3.3f}".format(first_point.x, first_point.y)) # move no extrude
    for j in xrange(len(perim)-1):
      point_start = perim[j]
      point_end = perim[j+1]
      extrude_amount = calculateExtrudeAmount(
        point_start.x, point_start.y, point_end.x, point_end.y, params.thickness)
      updateExtruded(extrude_amount)
      # move with extrude
      lines.append("G1 X{:3.3f} Y{:3.3f} E{:3.3f}".format(point_end.x, point_end.y, extruded)) 

  lines.append("")
  gfile.write("\n".join(lines))
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
  if not parallelTriangleSegments:
    return

  lines = []
  for segments in parallelTriangleSegments:
    lines.append("; Parallel rasterized triangle on layer {}".format(layerZ))
    for seggy in segments:
      # note: not yet optimized, this raster scans, but doesn't alternate
      # note: also doesn't print a perimeter around this, but that's handled elsewhere
      # TODO: make sure the start and end points are +thickness and -thickness respectively to fit
      #       within the perimeters

      # move to start point
      lines.append("G1 X{:3.3f} Y{:3.3f}".format(seggy.start.x, seggy.start.y)) 
      # update extrude amount according to the move we're about to make
      extrude_amount = calculateExtrudeAmount(
        seggy.start.x, seggy.start.y, seggy.end.x, seggy.end.y, params.thickness)
      updateExtruded(extrude_amount)
      # extrude to end point
      lines.append("G1 X{:3.3f} Y{:3.3f} E{:3.3f}".format(seggy.end.x, seggy.end.y, extruded))
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
  params = Parameters(filename="notused", perimeterLayers=1, infill=.20,
                      layerHeight=.19, thickness=0.4, support=False)

  # Test data from layer 0.19 of the 3mmBox
  perimeter = [
    Point3D(10, 15, .19),
    Point3D(10, 5.6333, .19), # where does this number come from??? (5.6333)
    Point3D(10, 5, .19),
    Point3D(10, -4.3667, .19),
    Point3D(10, -5, .19),
    Point3D(19.36667, -5, .19),
    Point3D(20, -5, .19),
    Point3D(29.36667, -5, .19),
    Point3D(30, -5, .19),
    Point3D(30, 4.36667, .19),
    Point3D(30, 5, .19),
    Point3D(30, 14.36667, .19),
    Point3D(30, 15, .19),
    Point3D(20.63333, 15, .19),
    Point3D(20, 15, .19),
    Point3D(10.63333, 15, .19),
    Point3D(10, 15, .19),       # return to first point
  ]
  perimeters = [perimeter]
  with open("test_gcode.gcode", "w") as gfile:
    generateSetup(gfile, params)
    generateGCode(gfile, params, 0.0, perimeters)
    generateGCode(gfile, params, 0.19, perimeters)
    generateGCode(gfile, params, 0.38, perimeters)
    generateCleanup(gfile)

  print "success"

if __name__ == "__main__":
  test()