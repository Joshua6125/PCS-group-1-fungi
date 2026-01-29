We are fun guys studying fungi! 🍄

Fairy ring data from (Miller & Gongloff, 2023).

## Overview

This project simulates fungal growth and the formation of fairy rings using Cellular Automata (CA). It includes various simulation models that incorporate factors like toxin diffusion and stochastic state transitions.

### Python Files

- **`CA.py`**: Defines the base CA class, managing the grid state, toxicity levels, and basic visualization logic.
- **`config.py`**: Stores configuration constants, simulation parameters (probabilities and thresholds), state definitions and color schemes.
- **`transitions.py`**: Implements simulation logic:
  - `BasicSim`: Simple lifecycle transitions.
  - `BasicToxinSim`, `ProbToxinSim`, `ProbToxinDeathSim`: toxin diffusion models with extra goodies
- **`gui.py`**: A GUI to visualize and control the simulations.
- **`utils.py`**: Utility functions.
- **`validate.py`**: Validates the model by comparing to real world data.
- **`experiment_validity_hull.py`**: Runs batch simulations to analyze the "validity hull" metric across different toxin decay rates.
- **`experiment_varying_kernel.py`**: Experiments with different convolution kernel sizes and variances to detect fairy ring formation.

## Usage

First install the uv python package manager (written in Rust!)
```bash
https://docs.astral.sh/uv/
```

Then install all the required packages
```bash
uv sync
```

To run the main simulation with the GUI:
```bash
uv run main.py
```

To run specific experiments:
```bash
uv run experiment_validity_hull.py
# or
uv run experiment_varying_kernel.py
```

## References
- Miller, S. L., & Gongloff, A. (2023). Size, age, and insights into establishment, dynamics and persistence of fairy rings in the Laramie Basin, Wyoming. Fungal Ecology, 65, 101272. https://doi.org/10.1016/j.funeco.2023.101272