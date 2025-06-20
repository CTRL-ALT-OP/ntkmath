# ntkmath

A collection of mathematical utility functions and classes for Python.

## Features

## Installation

### Development Installation
```bash
# Install in development mode
pip install -e .

# Or install with development dependencies
pip install -e ".[dev]"
```

## Usage

The package is designed to allow direct imports of functions and classes:

```python
# Import what you need directly from ntkmath
from ntkmath import 

```

## Available Functions and Classes

## Project Structure

```
ntkmath/
├── ntkmath/
│   └── __init__.py      # Main package file with imports
├── example.py           # Usage examples
├── setup.py            # Package setup
└── README.md           # This file
```

## Adding New Functions

1. Add your function/class to the appropriate module (or create a new one)
2. Import it in `ntkmath/__init__.py`
3. Add it to the `__all__` list in `ntkmath/__init__.py`
4. Update this README

## Example

Run the example script to see all features in action:

```bash
python example.py
```

## Development

Install development dependencies:
```bash
pip install -e ".[dev]"
```

Run tests:
```bash
pytest  # (when tests are added)
```

## License

MIT License 