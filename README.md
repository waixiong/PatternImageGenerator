# Pattern Image Generator

## Use
### Generate image from data
`python3 _encoder.py -d "Hello world, a good day to everyone here, this is pa"`

`python3 -h` for more command

### Extract data from image
`python3 ./_decoder.py -i Output.jpg`

Image format allow, `jpeg`, `png`

### Warning
Currently only 52 characters can be encoded, error will happen if characters more than 52


## Library Used
### Delaunator-Python
Fast Delaunay triangulation of 2D points implemented in Python.

This code was ported from [Mapbox's Delaunator Project](https://github.com/mapbox/delaunator) (JavaScript).

