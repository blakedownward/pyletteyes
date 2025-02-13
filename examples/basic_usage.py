from pyletteyes.colour import Colour

# Create a colour
red = Colour.from_hex("#FF0000")
print(red)

# Lighten it and output as hex
light_red = red.lighten(0.1)
print(light_red.hsl)

# Darken it and output as HSL values
dark_red = red.darken(0.2)
print(dark_red.hsl)

# Get complementary colour
complement = red.get_complementary()
print(complement)

