# Ethanol Plant Model

**Version:** 1.0.1

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
from systems.facility import Facility
from systems.pump import Pump
from systems.connectors import Pipe

# Create a complete facility with pump and processes
pump = Pump(efficiency=0.85, opening_diameter=0.15)
fermenter = Fermentation(efficiency=0.95)
pipe = Pipe(length=10, diameter=0.1)

facility = Facility(pump=pump, components=[fermenter, pipe])

# Process material through the facility
result = facility.facility_process(
    input_volume_composition={"water": 0.625, "sugar": 0.3125, "fiber": 0.0625},
    input_volumetric_flow=0.001,  # 1 L/s
    interval=1,
    store_data=True
)

print(f"Total power consumed: {result['total_power_consumed']:.2f} W")
print(f"Total cost consumed: {result['total_cost_consumed']:.2f} USD")
print(f"Energy generated: {result['power_generated']:.2f} J")
print(f"Net power gain: {result['net_power_gained']:.2f} J")
print(f"Ethanol produced: {result['mass_flow']['amount']['ethanol']:.4f} kg/s")
```

## Features

- ✅ Mass flow rate and volumetric flow rate balance calculations
- ✅ Power consumption tracking with configurable rates and units
- ✅ Energy consumption tracking for all processes with detailed logging
- ✅ Cost tracking for process economics with configurable rates
- ✅ **Pump modeling with efficiency-based energy calculations**
- ✅ **Integrated facility management for complete process chains**
- ✅ **Net power gain analysis for ethanol production systems**
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
- Power consumption tracking via `processPowerConsumption()`
- Batch processing via `iterateMassFlowInputs()` and `iterateVolumetricFlowInputs()`

### Fluid Transport Components

- **Pipe** - Straight segments with friction losses (Darcy-Weisbach equation)
- **Bend** - Elbows with direction change losses based on bend geometry
- **Valve** - Flow control with adjustable resistance coefficients
- **Pump** - Increases fluid pressure/velocity with efficiency-based power consumption

All connectors conserve mass while calculating realistic energy dissipation based on fluid dynamics principles. The connectors use a dedicated `processEnergy` method to calculate output kinetic energy after accounting for energy losses, which is then used to determine output flow rates.

### Facility Management

- **Facility** - Orchestrates complete process chains with integrated power tracking
  - Sequential processing through pumps, processes, and connectors
  - Automatic flow state management (mass and volumetric)
  - Total power consumption tracking across all components
  - Energy generation calculations from ethanol production
  - Net power gain analysis for economic viability assessment

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
│   ├── connectors.py   # Fluid transport connectors (Pipe, Bend, Valve)
│   ├── pump.py         # Pump class for fluid dynamics
│   └── facility.py     # Facility class for system integration
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

## Recent Updates (v1.0.0) - Full Release

### Production Ready
- **Stable API:** All core features finalized and production-ready
- **Comprehensive testing:** Extensive validation across all components
- **Complete documentation:** Full API reference, examples, and guides
- **Performance optimized:** Enhanced efficiency and reliability

### Key Features
- **Complete process simulation:** Fermentation, Filtration, Distillation, and Dehydration with realistic efficiency modeling
- **Integrated facility management:** Seamless orchestration of pumps, processes, and connectors
- **Economic analysis:** Full cost tracking and power consumption monitoring
- **Flexible architecture:** Static methods, configurable parameters, and extensible design

### v1.0.0 Highlights
This release marks the completion of the Ethanol Plant Model with a fully integrated simulation system featuring:
- Validated mass and energy balance calculations
- Accurate fluid dynamics modeling
- Comprehensive economic tracking
- Production-grade code quality and documentation

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
