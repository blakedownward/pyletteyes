import pytest
import numpy as np
from pyletteyes.palette import Palette
from pyletteyes.colour import Colour


@pytest.fixture
def basic_palette():
    """Create a basic palette with three colours."""
    return Palette([
        Colour(255, 0, 0),  # Red
        Colour(0, 255, 0),  # Green
        Colour(0, 0, 255)  # Blue
    ])


@pytest.fixture
def monochrome_palette():
    """Create a monochrome palette with three shades of blue."""
    return Palette([
        Colour(0, 0, 255),  # Blue
        Colour(0, 0, 192),  # Darker blue
        Colour(0, 0, 128)  # Even darker blue
    ])


def test_palette_initialization():
    # Test valid initialization
    colours = [Colour(255, 0, 0), Colour(0, 255, 0)]
    palette = Palette(colours)
    assert len(palette) == 2

    # Test empty palette
    with pytest.raises(ValueError):
        Palette([])

    # Test that palette makes a copy of the input list
    colours.append(Colour(0, 0, 255))
    assert len(palette) == 2


def test_palette_properties(basic_palette):
    assert basic_palette.size == 3
    assert len(basic_palette.colours) == 3

    # Test that colours property returns a copy
    colours = basic_palette.colours
    colours.append(Colour(0, 0, 0))
    assert len(basic_palette) == 3


def test_add_remove_colour(basic_palette):
    new_colour = Colour(255, 255, 0)  # Yellow
    initial_size = len(basic_palette)

    # Test adding
    basic_palette.add_colour(new_colour)
    assert len(basic_palette) == initial_size + 1
    assert new_colour in basic_palette.colours

    # Test removing
    basic_palette.remove_colour(new_colour)
    assert len(basic_palette) == initial_size
    assert new_colour not in basic_palette.colours

    # Test removing non-existent colour
    with pytest.raises(ValueError):
        basic_palette.remove_colour(Colour(128, 128, 128))

    # Test removing last colour
    while len(basic_palette) > 1:
        basic_palette.remove_colour(basic_palette[0])
    with pytest.raises(ValueError):
        basic_palette.remove_colour(basic_palette[0])


def test_hex_conversion():
    hex_colours = ["#FF0000", "#00FF00", "#0000FF"]
    palette = Palette.from_hex_list(hex_colours)

    assert len(palette) == 3
    assert palette.to_hex_list() == hex_colours


def test_contrast_score(basic_palette, monochrome_palette):
    # High contrast palette should have higher score
    high_contrast = basic_palette.score_contrast()

    # Low contrast (monochrome) palette should have lower score
    low_contrast = monochrome_palette.score_contrast()

    assert 0 <= high_contrast <= 1
    assert 0 <= low_contrast <= 1
    assert high_contrast > low_contrast


def test_harmony_score(basic_palette, monochrome_palette):
    # Test that scores are in valid range
    assert 0 <= basic_palette.score_harmony() <= 1
    assert 0 <= monochrome_palette.score_harmony() <= 1

    # Monochrome palette should be more harmonious
    assert monochrome_palette.score_harmony() > basic_palette.score_harmony()


def test_brightness_score():
    # Test white palette
    white_palette = Palette([Colour(255, 255, 255)])
    assert pytest.approx(white_palette.score_brightness(), abs=0.01) == 1.0

    # Test black palette
    black_palette = Palette([Colour(0, 0, 0)])
    assert pytest.approx(black_palette.score_brightness(), abs=0.01) == 0.0

    # Test mixed palette
    mixed_palette = Palette([
        Colour(255, 255, 255),  # White
        Colour(0, 0, 0)  # Black
    ])
    assert pytest.approx(mixed_palette.score_brightness(), abs=0.01) == 0.5


def test_dominant_colour(basic_palette):
    dominant = basic_palette.get_dominant_colour()
    assert isinstance(dominant, Colour)
    assert dominant == basic_palette[0]


def test_iteration(basic_palette):
    # Test that palette is iterable
    colours = list(basic_palette)
    assert len(colours) == 3
    assert all(isinstance(c, Colour) for c in colours)


def test_indexing(basic_palette):
    # Test positive indexing
    assert isinstance(basic_palette[0], Colour)
    assert basic_palette[0].rgb == (255, 0, 0)

    # Test negative indexing
    assert basic_palette[-1].rgb == (0, 0, 255)

    # Test index out of range
    with pytest.raises(IndexError):
        _ = basic_palette[len(basic_palette)]


def test_representation(basic_palette):
    repr_str = repr(basic_palette)
    assert repr_str.startswith("Palette(colours=[")
    for colour in basic_palette.colours:
        assert colour.to_hex() in repr_str
    assert repr_str.endswith("])")


def test_uniqueness_score(basic_palette, monochrome_palette):
    # Test that scores are in valid range
    assert 0 <= basic_palette.score_uniqueness() <= 1
    assert 0 <= monochrome_palette.score_uniqueness() <= 1

    # Basic palette (Red, Green, Blue) should have high uniqueness
    high_uniqueness = basic_palette.score_uniqueness()

    # Monochrome palette should have low uniqueness
    low_uniqueness = monochrome_palette.score_uniqueness()

    assert high_uniqueness > low_uniqueness
    assert high_uniqueness > 0.8  # RGB colours should be very unique
    assert low_uniqueness < 0.5  # Similar blues should have low uniqueness


def test_uniqueness_score_single_colour():
    # Single colour palette should have perfect uniqueness
    palette = Palette([Colour(255, 0, 0)])  # Single red
    assert pytest.approx(palette.score_uniqueness(), abs=0.01) == 1.0


def test_uniqueness_score_identical_colours():
    # Palette with identical colours should have minimum uniqueness
    palette = Palette([
        Colour(255, 0, 0),  # Red
        Colour(255, 0, 0)  # Same red
    ])
    assert pytest.approx(palette.score_uniqueness(), abs=0.01) == 0.0


def test_uniqueness_score_similar_colours():
    # Test with very similar but not identical colours
    palette = Palette([
        Colour(255, 0, 0),  # Red
        Colour(250, 5, 5)  # Very similar red
    ])
    score = palette.score_uniqueness()
    assert score < 0.2  # Should have low uniqueness score


def test_brightness_balance_score_perfect_balance():
    palette = Palette([
        Colour.from_hsl((0, 0, 0.3)),
        Colour.from_hsl((0, 0, 0.7))
    ])
    assert pytest.approx(palette.score_brightness_balance(), abs=0.01) == 1


def test_brightness_balance_score_all_dark():
    palette = Palette([
        Colour.from_hsl((0, 0, 0.1)),
        Colour.from_hsl((0, 0, 0.2)),
        Colour.from_hsl((0, 0, 0.1))
    ])

    # calculate the mean lightness as an expected low score
    mean_lightness = np.mean([0.1, 0.2, 0.1])

    expected = 1 - abs(mean_lightness - 0.5) * 2
    assert pytest.approx(palette.score_brightness_balance(), abs(0.01)) == expected


def test_brightness_balance_score_all_light():
    palette = Palette([
        Colour.from_hsl((0, 0, 0.8)),
        Colour.from_hsl((0, 0, 0.9)),
        Colour.from_hsl((0, 0, 0.8))
    ])

    # calculate the mean lightness as an expected low score
    mean_lightness = np.mean([0.8, 0.9, 0.8])

    expected = 1 - abs(mean_lightness - 0.5) * 2
    assert pytest.approx(palette.score_brightness_balance(), abs(0.01)) == expected


def test_brightness_balance_score_mixed_colours():
    palette = Palette([
        Colour.from_hsl((0, 0, 0.2)),
        Colour.from_hsl((0, 0, 0.4)),
        Colour.from_hsl((0, 0, 0.6)),
        Colour.from_hsl((0, 0, 0.8))
    ])

    # calculate the mean lightness as an expected low score
    mean_lightness = np.mean([0.2, 0.4, 0.6, 0.8])

    expected = 1 - abs(mean_lightness - 0.5) * 2
    assert pytest.approx(palette.score_brightness_balance(), abs(0.01)) == expected