# Pyletteyes

A comprehensive Python library for colour manipulation and evaluation.

Easily create Colour objects to manipulate or transform as required. Palette objects 
offer a convenient methods for storing, accessing and scoring collections of Colour objects.

## Features

- Colour space conversions (Hex, RGB, HSL)
- Colour manipulation (lighten, darken, complementary colours)
- Palette generation and analysis
- Image colour extraction

## Installation

```bash
pip install pyletteyes
```

## Basic Usage Example

```python
from pyletteyes import Colour
from pyletteyes import Palette

# Create a colour and print RGB string
red = Colour.from_hex("#FF0000")
print(red) # outputs: rgb(255, 0, 0)

# Lighten it and output as HSL values
light_red = red.lighten(0.1)
print(light_red.hsl) # outputs: (0.0, 0.5980392156862745, 1.0)

# Darken it and print as an RGB string
dark_red = red.darken(0.2)
print(dark_red) # outputs: rgb(153, 0, 0)

# Get complementary colour and output as hex
complement = red.get_complementary()
print(complement.to_hex()) # outputs: #00feff

# Get a pastel from the complementary colour
pastel = complement.get_pastel()
print(pastel) # outputs: rgb(101, 203, 204)
```
