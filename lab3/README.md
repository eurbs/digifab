# Lab 3 - THE SLICER

Welcome to what seems like the most painful lab yet. I'll be parsing .stl files and transferring geometry made entirely of triangles to the G-Code representation of "beautiful" 3D objects. Who knows if this will actually work, but we embark on a journey that should surely be an interesting one.

## Improvements


## Things to figure out

1. **How to increase or decrease the extrusion width**. As far as I know, the width is determined by how much material flows out of the nozzle. If it's exactly the distance travelled * nozzlehead thickness, then extrusion should be the thickness of the nozzlehead (we've been working with 0.4mm). This didn't seem to change anything in the [web gcode viewer](http://gcode.ws). I tried increasing my extrude amount by a factor of 100, and that didn't change anything in the web viewer. It's most likely that I don't understand how to increase the extrusion amount in gcode, though it's also possible that the gcode viewer [only renders this option for gcode generated either by known slicers](https://github.com/hudbrog/gCodeViewer/blob/bd4a9add067a080faad0af556e0c34b1d3619a67/js/gCodeReader.js). If you have any thoughts on this, please let us know. Since it's likely my calculations may be wrong, I still didn't want to chance running this on our printers, but I guess that's half the fun in hacking so we may just be doing it wrong.
2. **Smoothing of perimeters**. Sometimes the intersection points of two different triangles lie on the same line. A form of optimization would be to condense these lines into one line. This would also fix the problem we see with the naive perimeterResize function used to generate the inner perimeter walls, as seen here: TODO INSERT LINK TO PICTURE.
3. **Make resizePerimeters() less naive**. Right now, `resizePerimeters()` is incredibly naive. It trusts that the user gives enough space for the inside walls, but sometimes that simply isn't the case. We'd have to create an intersection detection algorithm to use while generating the inner walls to make sure that the inner walls don't intersect (again, see picture above).
4. **Optimize "Connecting the Dots"**