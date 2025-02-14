from colorsys import rgb_to_hls, hls_to_rgb
from typing import Tuple, Union


class Colour:
    """A class representing a colour in RGB space with various transformation capabilities."""

    def __init__(self, r: Union[int, float], g: Union[int, float], b: Union[int, float]):
        """
        Initialize a new Colour instance.

        Args:
            r (int): Red component (0-255)
            g (int): Green component (0-255)
            b (int): Blue component (0-255)

        Raises:
            ValueError: If RGB values are not in valid range
        """
        rounded_r = round(r)
        rounded_g = round(g)
        rounded_b = round(b)

        if not all(isinstance(v, (int, float)) and 0 <= v <= 255 for v in (rounded_r, rounded_g, rounded_b)):
            raise ValueError("RGB values must be between 0 and 255")

        self._r = rounded_r
        self._g = rounded_g
        self._b = rounded_b

    @property
    def rgb(self) -> Tuple[int, int, int]:
        """Get the RGB values as a tuple."""
        return (self._r, self._g, self._b)

    @property
    def hsl(self) -> Tuple[float, float, float]:
        """Get the HSL values as a tuple (Hue: 0-1, Saturation: 0-1, Lightness: 0-1)."""
        hls = rgb_to_hls(self._r / 255, self._g / 255, self._b / 255)
        return hls[0], hls[2], hls[1]  # must rearrange HLS to HSL

    @classmethod
    def from_hsl(cls, hsl: Tuple[float, float, float]) -> 'Colour':
        """
        Create a Colour instance from HSL values.

        Args:
            HSL values (tuple): Hue, Saturation, Lightness (e.g., (0.1, 0.3, 0.5))

        Returns:
            Colour: New Colour instance

        Raises:
            ValueError: If HSL values are invalid
        """
        for i in hsl:
            if i < 0.0 or i > 1.0:
                raise ValueError("HSL values must be within the range of 0.0 to 1.0")

        try:
            r, g, b = hls_to_rgb(h=hsl[0], l=hsl[2], s=hsl[1])
            return cls(int(r * 255), int(g * 255), int(b * 255))
        except ValueError:
            raise ValueError("Invalid HSL value")


    @classmethod
    def from_hex(cls, hex_string: str) -> 'Colour':
        """
        Create a Colour instance from a hex string.

        Args:
            hex_string (str): Hex colour code (e.g., "#FF0000" or "FF0000")

        Returns:
            Colour: New Colour instance

        Raises:
            ValueError: If hex string is invalid
        """
        hex_string = hex_string.lstrip('#')
        if len(hex_string) != 6:
            raise ValueError("Hex colour must be 6 characters long")

        try:
            r, g, b = tuple(int(hex_string[i:i + 2], 16) for i in (0, 2, 4))
            return cls(r, g, b)
        except ValueError:
            raise ValueError("Invalid hex colour string")

    def to_hex(self) -> str:
        """Convert the colour to hex format."""
        return f"#{self._r:02x}{self._g:02x}{self._b:02x}".upper()

    def lighten(self, amount: float = 0.1) -> 'Colour':
        """
        Create a lighter version of the colour.

        Args:
            amount (float): Amount to lighten by (0-1)

        Returns:
            Colour: New lightened Colour instance
        """
        h, s, l = self.hsl
        r, g, b = hls_to_rgb(h, min(1, l + amount), s)
        return Colour(int(r * 255), int(g * 255), int(b * 255))

    def darken(self, amount: float = 0.1) -> 'Colour':
        """
        Create a darker version of the colour.

        Args:
            amount (float): Amount to darken by (0-1)

        Returns:
            Colour: New darkened Colour instance
        """
        h, s, l = self.hsl
        r, g, b = hls_to_rgb(h, max(0, l - amount), s)
        return Colour(int(r * 255), int(g * 255), int(b * 255))

    def get_pastel(self) -> 'Colour':
        """
        Return a more 'pastel' version of the colour.
        Reduces saturation and increases brightness.

        :return:
            Colour: New pastel-ised Colour instance
        """
        h, s, l = self.hsl
        # Reduce saturation and increase lightness
        new_s = max(0.05, (s * 0.5))
        new_l = min(0.95, (l * 1.2))
        r, g, b = hls_to_rgb(h, new_l, new_s)

        return Colour(int(r * 255), int(g * 255), int(b * 255))

    def get_complementary(self) -> 'Colour':
        """
        Get the complementary colour (180 degrees opposite on the colour wheel).

        Returns:
            Colour: New Colour instance of the complementary colour
        """
        h, s, l = self.hsl
        # Add 0.5 to hue to get the opposite colour (180 degrees on the colour wheel)
        new_h = (h + 0.5) % 1.0
        r, g, b = hls_to_rgb(new_h, l, s)
        return Colour(int(r * 255), int(g * 255), int(b * 255))

    def get_analogous(self, angle: float = 30) -> Tuple['Colour', 'Colour']:
        """
        Get analogous colours (adjacent on the colour wheel).

        Args:
            angle (float): Angle of separation in degrees (default 30)

        Returns:
            Tuple[Colour, Colour]: Two new Colour instances
        """
        h, s, l = self.hsl
        angle = angle / 360  # Convert to 0-1 range

        h1 = (h + angle) % 1.0
        h2 = (h - angle) % 1.0

        r1, g1, b1 = hls_to_rgb(h1, l, s)
        r2, g2, b2 = hls_to_rgb(h2, l, s)

        return (
            Colour(int(r1 * 255), int(g1 * 255), int(b1 * 255)),
            Colour(int(r2 * 255), int(g2 * 255), int(b2 * 255))
        )

    def get_triadic(self) -> Tuple['Colour', 'Colour']:
        """
        Get triadic colours (shift hue left and right by 120 degrees).

        Returns:
            Tuple[Colour, Colour]: Two new Colour instances
        """
        return self.get_analogous(angle=120)


    def __eq__(self, other: object) -> bool:
        """Compare two colours for equality."""
        if not isinstance(other, Colour):
            return NotImplemented
        return self.rgb == other.rgb

    def __repr__(self) -> str:
        """String representation of the colour."""
        return f"rgb({self._r}, {self._g}, {self._b})"