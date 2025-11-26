# differential-colors

**Brand-aligned color utilities for plotting with matplotlib & seaborn**

`differential-colors` provides a clean, Pythonic interface for using the Differential Bio color palette in scientific figures, dashboards, and reports. It includes:

* ✔ A curated **categorical palette**
* ✔ High-quality **sequential colormaps** (light, dark, full variants)
* ✔ Ready-to-use **matplotlib** and **seaborn** integrations
* ✔ A built-in **tooltip** showing all colors and hex codes
* ✔ Optional registration of named colormaps with matplotlib

Designed for internal research projects, this package ensures consistent visualization aesthetics across notebooks, figures, and presentations.

---

## 🚀 Installation

You can install directly from GitHub using **uv** (recommended):

```bash
uv add "git+https://github.com/YOURUSER/differential-colors.git"
```

or with **pip**:

```bash
pip install "git+https://github.com/YOURUSER/differential-colors.git"
```

> Replace `YOURUSER` with your GitHub username or organization.

---

## 📦 Usage

### Import the library

```python
import differential_colors as diff
import matplotlib.pyplot as plt
import seaborn as sns
```

---

## 🎨 1. Categorical Palette

Set the seaborn/matplotlib palette using the branded categorical color order:

```python
sns.set_palette(diff.palette())
sns.barplot(data=df, x="variable", y="value")
```

Or specify certain colors:

```python
sns.set_palette(diff.palette(["Orange", "Blue", "Forest Green"]))
```

---

## 🌈 2. Sequential Colormaps

Generate continuous colormaps for heatmaps, KDE plots, etc.

### Available variants:

* `"light"` — white → base color
* `"dark"` — base color → almost black
* `"full"` — white → base → almost black

```python
cmap = diff.cmap("Orange", variant="full")
sns.heatmap(data, cmap=cmap)
```

Reverse direction:

```python
cmap = diff.cmap("Blue", variant="light", reverse=True)
```

---

## 🗂 3. Discrete Colormaps (ListedColormap)

Useful for categorical heatmaps or annotated blocks:

```python
cmap = diff.listed_cmap(["Peach", "Plum", "Mint"])
plt.imshow(matrix, cmap=cmap)
```

---

## 📚 4. Register all colormaps with matplotlib (optional)

This allows you to reference them by name in any plotting function:

```python
diff.register_mpl_colormaps()

plt.imshow(data, cmap="diff_Orange_full")
```

---

## 💡 Tooltip of all color names + hex values

For quick reference in notebooks:

```python
diff.tooltip()
```

Outputs something like:

```
Differential Bio color helper
-----------------------------
Orange         #FA693A
Forest Green   #304937
Blue           #ABC9DB
...
```

---

## 🧩 API Summary

| Function                       | Description                                     |
| ------------------------------ | ----------------------------------------------- |
| `palette(names=None)`          | Returns a list of hex codes for categorical use |
| `listed_cmap(names)`           | Discrete matplotlib colormap                    |
| `cmap(base, variant, reverse)` | Continuous colormap generator                   |
| `register_mpl_colormaps()`     | Registers all colormaps globally                |
| `tooltip()`                    | Prints all colors + usage tips                  |

---

## 📁 Project Structure

```text
differential-colors/
  pyproject.toml
  README.md
  src/
    differential_colors/
      __init__.py
```

---

## 🛠 Development

Install dev environment:

```bash
uv sync
uv run python
```

Run tests (if you add them later):

```bash
uv run pytest
```

---

## 📄 License

MIT License — feel free to modify for your own team’s needs.

---