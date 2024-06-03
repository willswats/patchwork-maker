# Patchwork Maker

Display multiple patterns and interactively overwrite them.

## Controls

### Selection mode

- Click on patches to select or deselect them.
- Click `OK` to enter edit mode.
- Click `CLOSE` to close the program.

### Edit Mode

- s - enter selection mode.
- d - deselect all patches.
- p - change all selected patches to the penultimate digit design.
- f - change all selected patches to the final digit design.
- q - change all selected patches to be plain.
- The initial letter of any valid colour (r, g, b, m, o, y or c) - change all selected patches to that colour, keeping their designs the same.
- x - change all selected patches to a 4x4 grid of random colours.

## Setup

### Pre-requisites

[Poetry](https://python-poetry.org/) needs to be installed.

### Install

Install the dependencies:

```bash
poetry install --no-root
```

### Run

Run the program:

```bash
poetry run python3 ./main.py
```
