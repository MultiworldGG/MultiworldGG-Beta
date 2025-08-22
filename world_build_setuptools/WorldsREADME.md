# Worlds Namespace Package

This is a pure namespace package for MultiWorld Games. It provides the base namespace structure for individual game worlds.

## Purpose

This package serves as a namespace container for MultiWorld game implementations. Individual game worlds are installed as separate packages that extend this namespace.

## Installation

This package is installed as a dependency of the main MultiWorld application.

## Usage

Individual game worlds can be installed separately and will automatically be available under the `worlds` namespace:

```python
import worlds.kh1  # Kingdom Hearts 1 world
import worlds.oot  # Ocarina of Time world
# etc.
```

## Development

This is a pure namespace package that should not contain any game-specific code. All game implementations should be in separate packages.
