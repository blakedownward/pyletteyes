from pyletteyes import Colour
from pyletteyes import Palette

# Create a colour and print RGB string
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

# make a pastel of the complementary colour
pastel = complement.get_pastel()
print(pastel)

# make a palette of colours
palette = Palette([pastel, dark_red, red])

# output as a list of rgb strings
string_list = palette.to_string_list()
print(string_list)

# or a list of hex codes
hex_list = palette.to_hex_list()
print(hex_list)

# import as a list of rgb strings
from_string_list = Palette.from_string_list(string_list)
print(from_string_list.to_string_list())

# import as a list of hex strings
from_hex_list = Palette.from_hex_list(hex_list)
print(from_hex_list.to_hex_list())

