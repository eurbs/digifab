import math
"""
Emilee Urbanek and Nick Confrey
CMSC 22010: Digital Fabrication
Lab 3

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

def deleteDuplicates(pointsList):
  """Given a list of points, remove duplicate points"""
  deleteDupes = set(pointsList)

  #Sanity check to avoid nan points
  #And near duplicates - points that are episilon from being the same point
  bad = []
  for i,p in enumerate(deleteDupes):
    for coord in p.a:
      if math.isnan(coord):
        bad.append(p)
        break
    for compare in deleteDupes:
      if compare == p or compare in bad:
        continue
      if(isclose(p.x, compare.x, episilon) and
      isclose(p.y, compare.y, episilon) and
      isclose(p.z, compare.z, episilon)):
        bad.append(p)
        break

  for ugly in bad:
    deleteDupes.remove(ugly)
  return deleteDupes
