import math
"""
Emilee Urbanek and Nick Confrey
CMSC 22010: Digital Fabrication
Lab 3
Due: 4/25

---

All the random helpers that everyone needs
"""
#Don't push this any lower or the sphere will break
episilon = .001

def isclose(a, b, rel_tol=1e-09, abs_tol=0.0):
	return abs(a-b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)

def floatGE(a, b):
  """Returns whether or not a >= b"""
  return a > b or isclose(a, b)

def floatLE(a, b):
  """Returns whether or not a <= b"""
  return a < b or isclose(a, b)

def floatGT(a, b):
  """Returns whether or not a > b"""
  return (a > b) and (not isclose(a, b))

def floatLT(a, b):
  """Returns whether or not a < b"""
  return (a < b) and (not isclose(a, b))

def printFunc(x):
  """Since Python2 doesn't have a print function"""
  print x

def normalize2DVec(v):
  """Normalizes a 2D vector represented as a list [x,y]"""
  x = v[0]
  y = v[1]
  magnitude = math.sqrt(x*x + y*y)
  return [x/magnitude, y/magnitude]