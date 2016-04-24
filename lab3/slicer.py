from triangle import *
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
  print "Nothing is done yet"

if __name__ == "__main__":
  main()


#Step 1: Parse the STL into a list of triangles

#Step 2: Sort the list of triangles by minZ
# Find top of object (largest maxZ of triangles)

#Step 3: Define a cutting plane (start at z = 0, increment by layer thickness)
# Iterate increasing the z value of the plane by layer thickness until = top

#Loop until top:
	#Step 4: Determine subset of triangles within cutting plane, throw rest away
	#Step 5: Run plane intersection test on each triangle, return a line segment
		# What if the triangle is paralell to the plane??
			#Run special function to create line segments based on filament width
		# What if the triangle intersects at only one point??
			#line segment with start and end are the same
	# Store line segment x,y in a data structure (list?)
		#sorted insertion?
		#sort into different perimeters
	#Step 6: Arrange the line segments so they are contiguous, that one ends where the other begins
	#Step 7: Loop over all line segments in data structure, output print head moves in gcode
		# What about when there are multiple perameters per layer??
		# How to optimize non-printing head moves??
	#Step 8: Output gcode raise head by layer thickness

#others:
# infill
# supports