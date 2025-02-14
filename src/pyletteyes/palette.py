from typing import List, Optional, Tuple
from .colour import Colour
import numpy as np


class Palette:
    """A class representing a collection of colours with analysis capabilities."""

    def __init__(self, colours: List[Colour]):
        """
        Initialize a new Palette instance.

        Args:
            colours (List[Colour]): List of Colour objects

        Raises:
            ValueError: If palette is empty
        """
        if not colours:
            raise ValueError("Palette must contain at least one colour")
        self._colours = colours.copy()  # Create a copy to prevent external modification

    @property
    def colours(self) -> List[Colour]:
        """Get the list of colours in the palette."""
        return self._colours.copy()  # Return a copy to prevent external modification

    @property
    def size(self) -> int:
        """Get the number of colours in the palette."""
        return len(self._colours)

    def score_contrast(self) -> float:
        """
        Calculate the overall contrast score of the palette.
        Higher scores indicate more contrast between colours.

        Returns:
            float: Contrast score between 0 and 1
        """
        if self.size < 2:
            return 1.0  # Single colour has no contrast

        contrasts = []
        for i, c1 in enumerate(self._colours):
            for c2 in self._colours[i + 1:]:
                # Calculate contrast using luminance difference
                # Convert RGB to luminance using standard coefficients
                l1 = 0.299 * c1.rgb[0] + 0.587 * c1.rgb[1] + 0.114 * c1.rgb[2]
                l2 = 0.299 * c2.rgb[0] + 0.587 * c2.rgb[1] + 0.114 * c2.rgb[2]

                # Normalize luminance difference
                contrast = abs(l1 - l2) / 255
                contrasts.append(contrast)

        return sum(contrasts) / len(contrasts)


    def score_uniqueness(self) -> float:
        """
        Score the palette based on how distinct colours are from one another.
        Higher scores indicate greater uniqueness.
        :return:
            float: Uniqueness score between 0 and 1
        """
        if self.size < 2:
            return 1.0

        rgb_values = np.array([
            [int(c.rgb[0]), int(c.rgb[1]), int(c.rgb[2])]
            for c in self._colours
        ], dtype=np.int32)

        similarities = []
        for i in range(len(rgb_values)):
            for j in range(i + 1, len(rgb_values)):
                # Max possible distance in RGB space is sqrt(255^2 * 3) ≈ 441.67
                distance = np.sqrt(np.sum((rgb_values[i].astype(float) - rgb_values[j].astype(float)) ** 2))
                similarity = 1 - (distance / 441.67)
                similarities.append(similarity)

        return float(1 - np.mean(similarities))


    def score_harmony(self) -> float:
        """
        Calculate the colour harmony score of the palette.
        Based on hue differences and standard colour theory principles.
        Higher scores indicate more harmonious combinations.

        Returns:
            float: Harmony score between 0 and 1
        """
        if self.size < 2:
            return 1.0

        # Get all HSL values
        hsls = [c.hsl for c in self._colours]

        # Calculate hue differences
        harmony_scores = []
        for i, (h1, _, _) in enumerate(hsls):
            for h2, _, _ in hsls[i + 1:]:
                # Calculate the smallest hue difference accounting for circular nature
                hue_diff = min(abs(h1 - h2), 1 - abs(h1 - h2))

                # Score based on common harmony principles
                # Perfect harmony at:
                # - 0 (same hue/monochromatic) = 1.0
                # - 1/6 (30° analogous) = 0.8
                # - 1/3 (120° triadic) = 0.9
                # - 1/2 (180° complementary) = 0.85
                harmony = max(
                    1.0 if hue_diff < 0.01 else 0,  # Monochromatic
                    0.8 if abs(hue_diff - 1 / 6) < 0.1 else 0,  # Analogous
                    0.9 if abs(hue_diff - 1 / 3) < 0.1 else 0,  # Triadic
                    0.85 if abs(hue_diff - 1 / 2) < 0.1 else 0,  # Complementary
                    # Base score for other relationships
                    0.5 - min(abs(hue_diff - 0), abs(hue_diff - 1 / 6),
                              abs(hue_diff - 1 / 3), abs(hue_diff - 1 / 2))
                )
                harmony_scores.append(harmony)

        return sum(harmony_scores) / len(harmony_scores)

    def score_saturation_variation(self) -> float:
        """
        Calculate a score based on variation in saturation levels.
        :return:
            float: Saturation variation score between 0 and 1
        """
        if self.size < 2:
            return 1.0

        saturations = [c.hsl[1] for c in self._colours]
        return float(np.std(saturations))


    def score_temperature_variation(self) -> float:
        """
        Calculate a score based on the mix of warm and cool colours.
        :return:
            float: Temperature variation score between 0 and 1
        """
        if self.size < 2:
            return 1.0

        hues = [c.hsl[0] for c in self._colours]
        warm_colors = sum(1 for h in hues if h <= 0.167 or h >= 0.833)
        cool_colors = len(hues) - warm_colors
        return float(1 - abs(warm_colors - cool_colors) / len(hues))


    def score_brightness(self) -> float:
        """
        Calculate the overall brightness score of the palette.

        Returns:
            float: Brightness score between 0 and 1
        """
        brightnesses = []
        for colour in self._colours:
            # Use the lightness component from HSL
            _, _, lightness = colour.hsl
            brightnesses.append(lightness)

        return sum(brightnesses) / len(brightnesses)


    def score_brightness_balance(self) -> float:
        """
        Calculate a score based on the balance of light and dark colours.
        :return:
            float: Brightness (lightness) balance score between 0 and 1
        """
        if self.size < 2:
            return 1.0

        values = [c.hsl[2] for c in self._colours]

        return float(1 - abs(np.mean(values) - 0.5) * 2)


    def get_dominant_colour(self) -> Colour:
        """
        Get the most dominant colour in the palette.
        Currently returns the first colour, but could be enhanced with
        clustering or frequency analysis.

        Returns:
            Colour: The dominant colour
        """
        return self._colours[0]


    def add_colour(self, colour: Colour) -> None:
        """
        Add a new colour to the palette.

        Args:
            colour (Colour): Colour to add
        """
        self._colours.append(colour)

    def remove_colour(self, colour: Colour) -> None:
        """
        Remove a colour from the palette.

        Args:
            colour (Colour): Colour to remove

        Raises:
            ValueError: If colour not in palette or would make palette empty
        """
        if colour not in self._colours:
            raise ValueError("Colour not in palette")
        if self.size <= 1:
            raise ValueError("Cannot remove last colour from palette")
        self._colours.remove(colour)


    @classmethod
    def from_hex_list(cls, hex_colours: List[str]) -> 'Palette':
        """
        Create a palette from a list of hex colour strings.

        Args:
            hex_colours (List[str]): List of hex colour codes

        Returns:
            Palette: New Palette instance
        """
        colours = [Colour.from_hex(hex_str) for hex_str in hex_colours]
        return cls(colours)

    def to_hex_list(self) -> List[str]:
        """
        Convert the palette to a list of hex colour strings.

        Returns:
            List[str]: List of hex colour codes
        """
        return [c.to_hex() for c in self._colours]

    @classmethod
    def from_string_list(cls, rgb_colours: List[str]) -> 'Palette':
        """
        Create a palette from a list of rgb colour strings.

        Args:
            rgb_colours (List[str]): List of rgb colour strings

        Returns:
            Palette: New Palette instance
        """
        colours = [Colour.from_string(rgb_str) for rgb_str in rgb_colours]
        return cls(colours)


    def to_string_list(self) -> List[str]:
        """
        Convert the palette to a list of rgb colour strings.

        Returns:
            List[str]: List of rgb colour strings
        """
        return [c.to_string() for c in self._colours]

    def __len__(self) -> int:
        """Get the number of colours in the palette."""
        return self.size

    def __getitem__(self, index: int) -> Colour:
        """Get a colour by index."""
        return self._colours[index]

    def __iter__(self):
        """Iterate over colours in the palette."""
        return iter(self._colours)

    def __repr__(self) -> str:
        """String representation of the palette."""
        hex_colours = [c.to_hex() for c in self._colours]
        return f"Palette(colours={hex_colours})"
