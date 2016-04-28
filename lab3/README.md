# Lab 3 - THE SLICER

We created a slicer that reads in stl geometry files and outputs gcode suitable for running on a 3D printer. Although its not perfect

### Usage:

- run `python slicer.py [stl file name]`
- Some good choices are in the samples folder, namely `samples/sphere.stl` or `samples/cube.stl`
- Output will be the stl file name in the samples folder. So `sphere.stl` becomes `sphere.gcode`.
- Use http://gcode.ws to view the gcode

## Accomplishments

- Created a geometry filestructure infrastructure to hold all data in software. This included writing `point3D.py`, `triangle.py`, `plane.py`. (Emilee)
- Parsed STL triangles into memory and organized them for easy computation (Emilee)
- Defined a cutting plane and an intersection function for triangles to determine if and when a triangle intersects the cutting plane (Nick)
- Wrote a naive algorithm for turning the line segments into a perimeter per z slice (Nick)
- Wrote GCode to turn perimeters into actual printer moves. This included writing a preamble and cleanup code on top of parsing incoming perimeters to move the print head. Calculations were also done to determine how much filament to extrude per segment (Emilee)
- Created an infill algorithm to determine when perimeters should be filled. This involved defining a scan line segment and checking line segment intersection along each section of the perimeter (Nick)
- Handled edge case of a triangle parallel to the cutting plane: Raster fill it completely (Nick). Write gcode to handle this different fill path (Emilee)
- Handled wall thickness contraints. This meant creating a slightly smaller perimeter around the object so the walls have thickness more than a single extrude line (Emilee)

## Improvements

1. **How to increase or decrease the extrusion width**. As far as I know, the width is determined by how much material flows out of the nozzle. If it's exactly the distance travelled * nozzlehead thickness, then extrusion should be the thickness of the nozzlehead (we've been working with 0.4mm). This didn't seem to change anything in the [web gcode viewer](http://gcode.ws). I tried increasing my extrude amount by a factor of 100, and that didn't change anything in the web viewer. It's most likely that I don't understand how to increase the extrusion amount in gcode, though it's also possible that the gcode viewer [only renders this option for gcode generated either by known slicers](https://github.com/hudbrog/gCodeViewer/blob/bd4a9add067a080faad0af556e0c34b1d3619a67/js/gCodeReader.js). If you have any thoughts on this, please let us know. Since it's likely my calculations may be wrong, I still didn't want to chance running this on our printers, but I guess that's half the fun in hacking so we may just be doing it wrong.
2. **Smoothing of perimeters**. Sometimes the intersection points of two different triangles lie on the same line. A form of optimization would be to condense these lines into one line. This would also fix the problem we see with the naive perimeterResize function used to generate the inner perimeter walls, as seen here: TODO INSERT LINK TO PICTURE.
3. **Make resizePerimeters() less naive**. Right now, `resizePerimeters()` is incredibly naive. It trusts that the user gives enough space for the inside walls, but sometimes that simply isn't the case. We'd have to create an intersection detection algorithm to use while generating the inner walls to make sure that the inner walls don't intersect (again, see picture above).
4. **Optimize "Connecting the Dots"**
5. **Improve infill**. Right now our line intersection algorithm for determining infill is a bit wonky and often skips lines. If we had time, we would go back and tighten this up.