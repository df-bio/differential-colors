"""
Differential Bio color utilities
================================

Matplotlib / seaborn-friendly helpers for using the Differential color
palette.

Quick start
-----------

import matplotlib.pyplot as plt
import seaborn as sns
import differential_colors as diff

# Categorical palette (for lines, bars, etc.)
sns.set_palette(diff.palette())   # or pass a subset of names

# Sequential cmap from a single brand color
cmap = diff.cmap("Orange", variant="light")   # 'light', 'dark', or 'full'

sns.heatmap(data, cmap=cmap)

Tip: call diff.tooltip() in a notebook to see all color names and hex codes.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterable, List, Optional

from matplotlib.colors import LinearSegmentedColormap, ListedColormap, to_rgb

# ---------------------------------------------------------------------
# Raw brand colors
# ---------------------------------------------------------------------

BRAND_COLORS: Dict[str, str] = {
    # Core neutrals
    "White": "#FFFFFF",
    "Grey": "#727272",
    "Almost Black": "#1E1E1E",

    # Accent trio
    "Orange": "#FA693A",
    "Red": "#891D1A",
    "Lime": "#70F676",

    # Extended palette
    "Blush": "#EAD6CF",
    "Cream": "#EADFCD",
    "Forest Green": "#304937",
    "Mint": "#D9EAD3",
    "Cloud": "#FCFCF8",
    "Peach": "#FBD2AE",
    "Soft Serve": "#FFFAF6",
    "Midnight": "#011F2E",
    "Blue": "#ABC9DB",
    "Baby Blue": "#EEF9FF",
    "Plum": "#362B40",
    "Haze": "#5B5776",
    "Lavendar": "#D6D4E1",
}

# Default categorical ordering (nice mix of contrast & brand feel)
DEFAULT_ORDER: List[str] = [
    "Orange",
    "Forest Green",
    "Blue",
    "Red",
    "Peach",
    "Plum",
    "Mint",
    "Haze",
    "Cream",
    "Baby Blue",
    "Blush",
    "Lime",
    "Midnight",
    "Cloud",
    "Soft Serve",
    "Lavendar",
    "Grey",
    "Almost Black",
    "White",
]


# ---------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------

def palette(names: Optional[Iterable[str]] = None) -> List[str]:
    """
    Return a categorical palette (list of hex strings).

    Parameters
    ----------
    names:
        Iterable of color names from BRAND_COLORS.
        If None, uses DEFAULT_ORDER.

    Examples
    --------
    sns.set_palette(diff.palette())                  # default mix
    sns.set_palette(diff.palette(["Orange", "Blue"]))
    """
    if names is None:
        names = DEFAULT_ORDER
    hexes = []
    for name in names:
        try:
            hexes.append(BRAND_COLORS[name])
        except KeyError as exc:
            raise KeyError(f"Unknown color name '{name}'. "
                           f"Valid names: {sorted(BRAND_COLORS)}") from exc
    return hexes


def listed_cmap(names: Optional[Iterable[str]] = None,
                name: str = "differential_listed") -> ListedColormap:
    """
    Discrete colormap from multiple brand colors.

    Useful for categorical heatmaps.

    Examples
    --------
    cmap = diff.listed_cmap(["Orange", "Blue", "Forest Green"])
    sns.heatmap(data, cmap=cmap)
    """
    return ListedColormap(palette(names), name=name)


def cmap(base: str,
         variant: str = "full",
         n: int = 256,
         name: Optional[str] = None,
         reverse: bool = False) -> LinearSegmentedColormap:
    """
    Continuous colormap based on a single brand color.

    Parameters
    ----------
    base:
        Name of a base color in BRAND_COLORS (e.g. "Orange", "Blue").
    variant:
        - "light":  white → base
        - "dark":   base  → Almost Black
        - "full":   white → base → Almost Black  (default)
    n:
        Number of color levels (default 256).
    name:
        Optional cmap name; if None, one is generated.
    reverse:
        If True, reverse the colormap.

    Examples
    --------
    cmap = diff.cmap("Orange", variant="light")
    plt.imshow(data, cmap=cmap)

    cmap = diff.cmap("Midnight", variant="dark", reverse=True)
    sns.kdeplot(..., fill=True, cmap=cmap)
    """
    if base not in BRAND_COLORS:
        raise KeyError(f"Unknown base color '{base}'. "
                       f"Valid names: {sorted(BRAND_COLORS)}")

    base_hex = BRAND_COLORS[base]
    white = "#FFFFFF"
    almost_black = BRAND_COLORS["Almost Black"]

    if variant == "light":
        colors = [white, base_hex]
    elif variant == "dark":
        colors = [base_hex, almost_black]
    elif variant == "full":
        colors = [white, base_hex, almost_black]
    else:
        raise ValueError("variant must be one of {'light', 'dark', 'full'}")

    if reverse:
        colors = list(reversed(colors))

    if name is None:
        name = f"diff_{base}_{variant}{'_r' if reverse else ''}"

    return LinearSegmentedColormap.from_list(name, colors, N=n)


def register_mpl_colormaps(variants: Iterable[str] = ("light", "dark", "full")):
    """
    Register a family of colormaps with matplotlib.

    After calling this once, you can refer to them by name:

        plt.cm.get_cmap("diff_Orange_full")

    or just

        cmap="diff_Orange_full"

    in many matplotlib / seaborn functions.
    """
    import matplotlib.cm as cm

    for name in BRAND_COLORS:
        if name == "White":  # avoid degenerate full white maps
            continue
        for v in variants:
            cm.register_cmap(cmap=cmap(name, variant=v))


# ---------------------------------------------------------------------
# “Tooltip” helper
# ---------------------------------------------------------------------

_TOOLTIP = """
Differential Bio color helper

Color names and hex codes
-------------------------

{table}

Usage patterns
--------------

1. Categorical plots (lines, bars, scatter)
   >>> import seaborn as sns
   >>> import differential_colors as diff
   >>> sns.set_palette(diff.palette())              # default order
   >>> sns.set_palette(diff.palette(['Orange','Blue','Forest Green']))

2. Sequential / continuous maps
   >>> cmap = diff.cmap('Orange', variant='light')   # white → orange
   >>> sns.heatmap(data, cmap=cmap)

   Variants:
     - 'light' : white → base
     - 'dark'  : base → Almost Black
     - 'full'  : white → base → Almost Black

3. Registered colormaps (optional)
   >>> diff.register_mpl_colormaps()
   >>> plt.imshow(data, cmap='diff_Orange_full')

Tip: spelling matters – use the names exactly as listed above.
"""


def tooltip() -> None:
    """Print a brief usage guide and the available color names."""
    rows = []
    for name in sorted(BRAND_COLORS):
        rows.append(f"  {name:<12} {BRAND_COLORS[name]}")
    print(_TOOLTIP.format(table="\n".join(rows)))


# ---------------------------------------------------------------------
# Tiny internal helper (not currently used but handy for extension)
# ---------------------------------------------------------------------

@dataclass(frozen=True)
class Color:
    """Convenience wrapper if you want to extend the library later."""
    name: str

    @property
    def hex(self) -> str:
        return BRAND_COLORS[self.name]

    @property
    def rgb(self):
        return to_rgb(self.hex)
def main() -> None:
    print("Hello from differential-colors!")

__all__ = [
    "BRAND_COLORS",
    "palette",
    "listed_cmap",
    "cmap",
    "register_mpl_colormaps",
    "tooltip",
]

__version__ = "0.1.0"