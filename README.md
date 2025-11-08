# Ethanol Plant Model

**Version:** 0.3.0

[![Documentation](https://img.shields.io/badge/docs-latest-blue.svg)](docs/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

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
from systems.processes import Fermentation

# Create a fermentation system with 95% efficiency
fermenter = Fermentation(efficiency=0.95)

# Process inputs
result = fermenter.processMass(
    inputs={"ethanol": 0, "water": 100, "sugar": 50, "fiber": 10},
    input_type="amount",
    output_type="full"
)

print(f"Ethanol produced: {result['amount']['ethanol']:.2f} kg")
print(f"Purity: {result['composition']['ethanol']:.2%}")
```

## Features

- ✅ Mass and volumetric flow balance calculations
- ✅ Energy loss modeling for fluid transport
- ✅ Configurable efficiency parameters
- ✅ Flexible input/output formats
- ✅ Built-in visualization
- ✅ Batch processing capabilities
- ✅ Component tracking across the pipeline

## System Components

### Process Systems

1. **Fermentation** - Converts sugar into ethanol (51% theoretical yield)
2. **Filtration** - Removes solid particles and fiber content
3. **Distillation** - Separates and concentrates ethanol
4. **Dehydration** - Removes remaining water content

### Fluid Transport Components

- **Pipe** - Straight segments with friction losses (Darcy-Weisbach equation)
- **Bend** - Elbows with direction change losses
- **Valve** - Flow control with adjustable resistance

All connectors conserve mass while calculating realistic energy dissipation.

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
- NumPy
- Matplotlib
- PyGObject (GTK4 bindings)

## Project Structure

```
EthanolPlantModel/
├── systems/
│   ├── processes.py    # Core process systems
│   └── connectors.py   # Fluid transport connectors
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
