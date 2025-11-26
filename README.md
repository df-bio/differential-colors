[project]
name = "differential-colors"
version = "0.1.0"
description = "Differential Bio color utilities for matplotlib & seaborn."
readme = "README.md"
requires-python = ">=3.9"
license = { text = "MIT" }  # or whatever license you prefer
authors = [
  { name = "Your Name", email = "you@example.com" },
]

dependencies = [
  "matplotlib>=3.7",
  "seaborn>=0.13",   # optional but handy, leave out if you want zero deps
]

[tool.uv]
# lets uv know this is a managed project
