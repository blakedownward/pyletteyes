from pyletteyes.colour import Colour

# Create a colour
red = Colour.from_hex("#FF0000")
print(red)

# Lighten it and output as HSL values
light_red = red.lighten(0.1)
print(light_red.hsl)

# Darken it and print as an RGB string
dark_red = red.darken(0.2)
print(dark_red)

# Get complementary colour and output as hex
complement = red.get_complementary()
print(complement.to_hex())

