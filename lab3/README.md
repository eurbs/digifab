# Lab 3 - THE SLICER

We created a slicer that reads in stl geometry files and outputs gcode suitable for running on a 3D printer. Although it's not perfect

### Usage:

- run `python slicer.py [stl file path]`
- for more options, run `python slicer.py -h` (Perimeter layers, layer height, etc)
- Some good choices are in the samples folder, namely `samples/sphere.stl` or `samples/cube.stl`
- Output will be the stl file name in the same directory as the stl file. So `sphere.stl` becomes `sphere.gcode`.
- Use [http://gcode.ws](http://gcode.ws) to view the gcode

## Accomplishments

- Created a geometry filestructure infrastructure to hold all data in software. This included writing `point3D.py`, `triangle.py`, `plane.py`. (Emilee)
- Parsed STL triangles into memory and organized them for easy computation (Emilee)
- Argument parsing and parameters data structure (Emilee)
- Defined a cutting plane and an intersection function for triangles to determine if and when a triangle intersects the cutting plane (Nick)
- Wrote a naive algorithm for turning the line segments into a perimeter per z slice (Nick)
- Wrote GCode to turn perimeters into actual printer moves. This included writing a preamble and cleanup code on top of parsing incoming perimeters to move the print head. Calculations were also done to determine how much filament to extrude per segment (Emilee)
- Created an infill algorithm to determine when perimeters should be filled. This involved defining a scan line segment and checking line segment intersection along each section of the perimeter (Nick). Fixed the segment intersection by adding bound checking and found that floating points can't be compared using the regular comparison operators -- what a bug (Emilee).
- Handled edge case of a triangle parallel to the cutting plane: Raster fill it completely (Nick). Write gcode to handle this different fill path (Emilee)
- Handled wall thickness contraints. This meant creating a slightly smaller perimeter around the object so the walls have thickness more than a single extrude line (Emilee)

## Improvements

1. **Better handling of perimeters parallel to cutting plane**. As we have it, the code currently raster scans and fills each individual triangle that is parallel to the cutting plane inside of [`_parallelIntersection()`](https://github.com/eurbs/digifab/blob/master/lab3/triangle.py). This isn't optimal, however changing it would involve a whole lot of refactoring (which at this point is trivial work, but would take hours to do.. nobody likes to refactor). The plan for refactoring is as follows: Change the return type of `intersectPlane()` from a list of lists of segments to a tuple consisting of a type of perimeter ("area" or "perim") and a list of lists of segments. Then we un-expose `_parallelIntersection()` (by calling it from `intersectPlane()` as is the intended use) which *should* be treated as a private function but alas is called explicitly in [`slicer.py:main()`](https://github.com/eurbs/digifab/blob/master/lab3/slicer.py). We'd then adapt all of the functions in [`gcode.py`](https://github.com/eurbs/digifab/blob/master/lab3/gcode.py) to understand this new return value. When the tuple given indicates that a perimeter is an *area*, then we would simply call `makeInfill()` with the infill at 100%, and this would make the flat tops look much nicer than they currently do. 
2. **Smoothing of perimeters**. Sometimes the intersection points of two different triangles lie on the same line. A form of optimization would be to condense these lines into one line. This would also fix the problem we see with the naive perimeterResize function used to generate the inner perimeter walls.
3. **Make resizePerimeters() less naive**. Right now, `resizePerimeters()` is incredibly naive. It trusts that the user gives enough space for the inside walls, but sometimes that simply isn't the case. We'd have to create an intersection detection algorithm to use while generating the inner walls to make sure that the inner walls don't intersect (again, see picture above).
4. **Optimize "Connecting the Dots"**. Right now, this is an `O(n^2)` algorithm. We were going to do a game of hash and find, but the float values weren't cooperating and we'd need to ensure all line segments had the start and end in the right direction, and we couldn't quite figure out a rule for that.
5. **Improve infill**. Right now our line intersection algorithm for determining infill is a bit wonky and often skips lines. If we had time, we would go back and tighten this up. Additionally, infill raster scans and fills only in the -x to +x direction. We would like to, at the very least, snake the raster filling and alternate on every layer whether the infill is horizontal or vertical. We'd then follow a very simple checkerboard infill pattern. 
6. **Use a testing framework** This lab turned out to be a full fledged project. Though we have some primative unit tests setup in each file, they're not really understandable by anyone except for us, and much of the intersection and perimeter functionalities do not have unit tests, which led to exceptionally difficult debug sessions. If we had unit tests, we'd probably be able to figure out why infill infills sporadically as well.
7. **Create supports**. Though this was initially part of the assignment, we didn't manage to get around to it :(
8. **Center the object on the printbed**
9. **Draw circle around object before printing** this gets the extrusion going for better sticking
10. **Option for output directory** And default to a gcode directory.
11. **Support Brims**. `resizePerimeters()` already does this for wall heights, but unfortunately we have a bug for our bottom layer perimeter. With a little bit of bug hunting and some repurposing of code, brims would be supported.
12. **Log Level Option**. We'd like to keep our print statements and debug logs, but have the option to run our program without forcing users to see those logs. Lesson learned for all future projects.

## Summary

This lab turned out to be a full fledged project. At every step we hit walls, did research, and tried to come up with solutions to the problems we were facing. It was incredibly rewarding though and it would be cool to continue building on this.
