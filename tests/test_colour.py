import pytest
from unittest.mock import patch
from pyletteyes.colour import Colour


def test_colour_initialization():
    # Test valid initialization
    c = Colour(255, 128, 0)
    assert c.rgb == (255, 128, 0)

    # Test float inputs (should round)
    c = Colour(255.4, 128.6, 0.2)
    assert c.rgb == (255, 129, 0)

    # Test invalid values
    with pytest.raises(ValueError):
        Colour(256, 128, 0)
    with pytest.raises(ValueError):
        Colour(-1, 128, 0)
    with pytest.raises(ValueError):
        Colour(255, 128, 300)


def test_hex_conversion():
    # Test hex to RGB
    c = Colour.from_hex("#FF8000")
    assert c.rgb == (255, 128, 0)

    # Test RGB to hex
    c = Colour(255, 128, 0)
    assert c.to_hex().upper() == "#FF8000"

    # Test hex without #
    c = Colour.from_hex("FF8000")
    assert c.rgb == (255, 128, 0)

    # Test invalid hex
    with pytest.raises(ValueError):
        Colour.from_hex("#FF80")  # Too short
    with pytest.raises(ValueError):
        Colour.from_hex("#GG8000")  # Invalid characters


def test_hsl_conversion():
    # Test pure red
    c = Colour(255, 0, 0)
    h, s, l = c.hsl
    assert pytest.approx(h, abs=0.01) == 0.0  # Red hue
    assert pytest.approx(s, abs=0.01) == 1.0  # Full saturation
    assert pytest.approx(l, abs=0.01) == 0.5  # Mid lightness


def test_from_hsl_valid():
    """Test valid HSL to RGB conversion."""
    test_cases = [
        ((0.0, 0.0, 0.0), (0, 0, 0)),  # Black
        ((0.0, 0.0, 1.0), (255, 255, 255)),  # White
        ((0.0, 1.0, 0.5), (255, 0, 0)),  # Pure red
        ((1 / 3, 1.0, 0.5), (0, 255, 0)),  # Pure green (exactly 1/3)
        ((2 / 3, 1.0, 0.5), (0, 0, 255))  # Pure blue (exactly 2/3) # Blue
    ]

    for hsl, expected_rgb in test_cases:
        colour = Colour.from_hsl(hsl)
        assert (colour._r, colour._g, colour._b) == expected_rgb


def test_from_hsl_out_of_range():
    """Test HSL values outside the valid range."""
    invalid_inputs = [
        (-0.1, 0.5, 0.5),  # Negative hue
        (0.5, -0.1, 0.5),  # Negative saturation
        (0.5, 0.5, -0.1),  # Negative lightness
        (1.1, 0.5, 0.5),  # Hue > 1
        (0.5, 1.1, 0.5),  # Saturation > 1
        (0.5, 0.5, 1.1)  # Lightness > 1
    ]

    for hsl in invalid_inputs:
        with pytest.raises(ValueError, match="HSL values must be within the range of 0.0 to 1.0"):
            Colour.from_hsl(hsl)


# def test_from_hsl_colorsys_error():
#     """Test handling of ValueError from colorsys.hls_to_rgb."""
#     with patch('colorsys.hls_to_rgb') as mock_hls_to_rgb:
#         mock_hls_to_rgb.side_effect = ValueError("Mock colorsys error")
#
#         with pytest.raises(ValueError, match="Invalid HSL value"):
#             Colour.from_hsl((0.5, 0.5, 0.5))


def test_lighten_darken():
    c = Colour(100, 100, 100)

    # Test lightening
    lighter = c.lighten(0.2)
    assert all(x > y for x, y in zip(lighter.rgb, c.rgb))

    # Test darkening
    darker = c.darken(0.2)
    assert all(x < y for x, y in zip(darker.rgb, c.rgb))

    # Test maximum lightness
    white = Colour(255, 255, 255)
    assert white.lighten(0.1).rgb == (255, 255, 255)

    # Test minimum darkness
    black = Colour(0, 0, 0)
    assert black.darken(0.1).rgb == (0, 0, 0)


def test_complementary():
    # Test red -> cyan
    red = Colour(255, 0, 0)
    cyan = red.get_complementary()
    assert pytest.approx(cyan.rgb, abs=1) == (0, 255, 255)

    # Test green -> magenta
    green = Colour(0, 255, 0)
    magenta = green.get_complementary()
    assert pytest.approx(magenta.rgb, abs=1) == (255, 0, 255)


def test_analogous():
    # Test red's analogous colours
    red = Colour(255, 0, 0)
    left, right = red.get_analogous()

    # Check that the analogous colours are different from the original
    assert left.rgb != red.rgb
    assert right.rgb != red.rgb

    # Check that the analogous colours are different from each other
    assert left.rgb != right.rgb

    # Test custom angle
    left, right = red.get_analogous(angle=15)
    left2, right2 = red.get_analogous(angle=45)

    # Wider angle should produce more different colours
    assert sum(abs(a - b) for a, b in zip(left.rgb, right.rgb)) < \
           sum(abs(a - b) for a, b in zip(left2.rgb, right2.rgb))


def test_equality():
    c1 = Colour(255, 128, 0)
    c2 = Colour(255, 128, 0)
    c3 = Colour(0, 128, 255)

    assert c1 == c2
    assert c1 != c3
    assert c1 != "not a colour"


def test_string_representation():
    c = Colour(255, 128, 0)
    assert repr(c) == "rgb(255, 128, 0)"


# Parameterized tests for various colour values
@pytest.mark.parametrize("r,g,b,hex_code", [
    (255, 0, 0, "#FF0000"),
    (0, 255, 0, "#00FF00"),
    (0, 0, 255, "#0000FF"),
    (0, 0, 0, "#000000"),
    (255, 255, 255, "#FFFFFF"),
    (128, 128, 128, "#808080"),
])
def test_colour_values(r, g, b, hex_code):
    c = Colour(r, g, b)
    assert c.to_hex().upper() == hex_code
    assert Colour.from_hex(hex_code).rgb == (r, g, b)


def test_valid_from_string():
    """Test parsing of valid RGB strings."""
    test_cases = [
        ("rgb(255, 0, 0)", (255, 0, 0)),
        ("rgb(0, 255, 0)", (0, 255, 0)),
        ("rgb(0, 0, 255)", (0, 0, 255)),
        ("rgb(128, 128, 128)", (128, 128, 128)),
        ("rgb(0, 0, 0)", (0, 0, 0)),
        ("rgb(255, 255, 255)", (255, 255, 255))
    ]

    for rgb_string, expected in test_cases:
        colour = Colour.from_string(rgb_string)
        assert colour._r == expected[0]
        assert colour._g == expected[1]
        assert colour._b == expected[2]


def test_invalid_from_string():
    """Test that invalid RGB strings raise appropriate errors."""
    invalid_inputs = [
        "rgb(256, 0, 0)",  # Red value too high
        "rgb(-1, 0, 0)",  # Negative value
        "rgb(0, 0",  # Missing closing parenthesis
        "rgb(0, 0, 0, 0)",  # Too many values
        "rgb(a, b, c)",  # Non-numeric values
        "rgb()",  # Empty string
        "rgb(0, 0,)",  # Missing value
        "rgb(255.5, 0, 0)"  # Decimal values
    ]

    for invalid_input in invalid_inputs:
        with pytest.raises(ValueError):
            Colour.from_string(invalid_input)


def test_to_string():
    """Test conversion of Colour instances to RGB strings."""
    test_cases = [
        ((255, 0, 0), "rgb(255, 0, 0)"),
        ((0, 255, 0), "rgb(0, 255, 0)"),
        ((0, 0, 255), "rgb(0, 0, 255)"),
        ((128, 128, 128), "rgb(128, 128, 128)"),
        ((0, 0, 0), "rgb(0, 0, 0)"),
        ((255, 255, 255), "rgb(255, 255, 255)")
    ]

    for rgb_values, expected in test_cases:
        colour = Colour(*rgb_values)
        assert colour.to_string() == expected


def test_roundtrip():
    """Test conversion from string to Colour and back preserves values."""
    test_strings = [
        "rgb(255, 0, 0)",
        "rgb(0, 255, 0)",
        "rgb(0, 0, 255)",
        "rgb(128, 128, 128)",
        "rgb(0, 0, 0)",
        "rgb(255, 255, 255)"
    ]

    for rgb_string in test_strings:
        colour = Colour.from_string(rgb_string)
        assert colour.to_string() == rgb_string


def test_edge_cases():
    """Test edge cases for RGB string parsing."""
    # Extra spaces shouldn't matter
    colour = Colour.from_string("rgb(255, 0, 0)")
    assert colour.to_string() == "rgb(255, 0, 0)"

    # Whitespace at start/end shouldn't matter
    colour = Colour.from_string("  rgb(255, 0, 0)  ")
    assert colour.to_string() == "rgb(255, 0, 0)"