# Ethanol Plant Model

**Version:** 0.5.2

[![Documentation](https://img.shields.io/badge/docs-latest-blue.svg)](docs/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Changelog](https://img.shields.io/badge/changelog-latest-orange.svg)](CHANGELOG.md)

## Overview
This project contains a model of an ethanol production plant, developed as part of ENGR-16100 coursework. The model simulates the complete production pipeline from raw materials to high-purity ethanol through mass balance calculations, process efficiency modeling, and fluid transport dynamics.

## 📚 Documentation

Full documentation is available in the [docs](docs/) folder:

- **[Getting Started](docs/getting-started.md)** - Installation and basic usage
- **[API Reference](docs/api-reference.md)** - Complete API documentation
- **[Process Systems](docs/process-systems.md)** - Detailed guide to process systems
- **[Connector Systems](docs/connector-systems.md)** - Fluid transport components
- **[Examples](docs/examples.md)** - Practical examples and tutorials

## Quick Start

```python
from systems.processors import Fermentation

# Create a fermentation system with 95% efficiency
fermenter = Fermentation(efficiency=0.95)

# Process mass flow rate inputs
result = fermenter.processMassFlow(
    inputs={"ethanol": 0, "water": 100, "sugar": 50, "fiber": 10},
    input_type="amount",
    output_type="full",
    store_outputs=True
)

print(f"Ethanol produced: {result['amount']['ethanol']:.2f} kg")
print(f"Water remaining: {result['amount']['water']:.2f} kg")
print(f"Ethanol purity: {result['composition']['ethanol']:.2%}")
```

## Features

- ✅ Mass flow rate and volumetric flow rate balance calculations
- ✅ Energy consumption tracking for all processes
- ✅ Energy loss modeling for fluid transport (Darcy-Weisbach, bend losses)
- ✅ Configurable efficiency parameters for all process units
- ✅ Flexible input/output formats (amount, composition, or full)
- ✅ Comprehensive logging system for process tracking
- ✅ Built-in visualization capabilities
- ✅ Batch processing with iterative methods
- ✅ Component tracking across the entire pipeline

## System Components

### Process Systems

1. **Fermentation** - Converts sugar into ethanol (51% theoretical yield)
2. **Filtration** - Removes solid particles and fiber content
3. **Distillation** - Separates and concentrates ethanol from impurities
4. **Dehydration** - Removes remaining water content for high-purity ethanol

All processes support:
- Mass flow rate processing via `processMassFlow()`
- Volumetric flow rate processing via `processVolumetricFlow()`
- Energy consumption tracking via `processEnergyConsumption()`
- Batch processing via `iterateMassFlowInputs()` and `iterateVolumetricFlowInputs()`

### Fluid Transport Components

- **Pipe** - Straight segments with friction losses (Darcy-Weisbach equation)
- **Bend** - Elbows with direction change losses based on bend geometry
- **Valve** - Flow control with adjustable resistance coefficients

All connectors conserve mass while calculating realistic energy dissipation based on fluid dynamics principles. The connectors use a dedicated `processEnergy` method to calculate output kinetic energy after accounting for energy losses, which is then used to determine output flow rates.

## Installation

### Using pip
```bash
git clone https://github.com/ENGR161-Team1/EthanolPlantModel.git
cd EthanolPlantModel

# Install system dependencies (Ubuntu/Debian)
sudo apt install libgirepository2.0-dev libcairo2-dev libgtk-4-dev \
    pkg-config python3-dev python3-gi python3-gi-cairo \
    gir1.2-gtk-4.0 gobject-introspection

pip install .
```

### Using uv (Faster)
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
git clone https://github.com/ENGR161-Team1/EthanolPlantModel.git
cd EthanolPlantModel

# Install system dependencies (Ubuntu/Debian)
sudo apt install libgirepository2.0-dev libcairo2-dev libgtk-4-dev \
    pkg-config python3-dev python3-gi python3-gi-cairo \
    gir1.2-gtk-4.0 gobject-introspection

uv pip install .
```

## Dependencies

- Python >= 3.10
- NumPy - Numerical computations
- Matplotlib - Visualization
- PyGObject - GTK4 bindings for GUI support

## Project Structure

```
EthanolPlantModel/
├── systems/
│   ├── process.py      # Base Process class for all systems
│   ├── processors.py   # Process implementations (Fermentation, Filtration, etc.)
│   └── connectors.py   # Fluid transport connectors (Pipe, Bend, Valve)
├── docs/               # Documentation
│   ├── README.md
│   ├── getting-started.md
│   ├── api-reference.md
│   ├── process-systems.md
│   ├── connector-systems.md
│   └── examples.md
├── LICENSE
├── README.md
└── pyproject.toml
```

## Recent Updates (v0.5.2)

### Bug Fixes
- **Refactored Connector class to use power terminology:**
  - Updated parameter names and calculations to use "power" instead of "energy" for improved clarity
  - Renamed methods and attributes to reflect instantaneous power consumption rather than total energy
  - Better aligns with the physical concepts being modeled (power dissipation in fluid flow)

See [CHANGELOG.md](CHANGELOG.md) for complete version history and previous updates.

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Team Members

- **Advay R. Chandra** - chand289@purdue.edu
- **Karley J. Hammond** - hammon88@purdue.edu
- **Samuel M. Razor** - razor@purdue.edu
- **Katherine E. Hampton** - hampto64@purdue.edu

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

Developed as part of ENGR-16100 coursework at Purdue University.
