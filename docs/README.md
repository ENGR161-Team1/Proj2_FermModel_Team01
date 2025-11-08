# Ethanol Plant Model Documentation

**Version:** 0.3.0

Welcome to the Ethanol Plant Model documentation. This project provides a comprehensive simulation of an ethanol production plant developed for ENGR-16100 coursework.

---

## 📖 Quick Navigation

| Section | Description |
|---------|-------------|
| [Getting Started](getting-started.md) | Installation, setup, and basic usage |
| [API Reference](api-reference.md) | Complete API documentation |
| [Process Systems](process-systems.md) | Fermentation, filtration, distillation, dehydration |
| [Connector Systems](connector-systems.md) | Pipes, bends, and valves |
| [Examples](examples.md) | Practical examples and tutorials |

---

## What is the Ethanol Plant Model?

The Ethanol Plant Model simulates a complete ethanol production pipeline through four key stages:

1. **Fermentation** - Converts sugar into ethanol
2. **Filtration** - Removes solid particles and fiber
3. **Distillation** - Separates and concentrates ethanol
4. **Dehydration** - Removes remaining water content

Additionally, the model includes fluid transport components (pipes, bends, valves) that simulate realistic energy losses during transport between process stages.

## Key Features

- ✅ Mass and volumetric flow balance calculations
- ✅ Energy loss modeling for fluid transport
- ✅ Configurable efficiency parameters
- ✅ Flexible input/output formats
- ✅ Built-in visualization
- ✅ Batch processing capabilities
- ✅ Component tracking across the pipeline

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

## Installation

See the [Getting Started Guide](getting-started.md) for detailed installation instructions.

### Quick Install

```bash
git clone https://github.com/ENGR161-Team1/EthanolPlantModel.git
cd EthanolPlantModel
pip install .
```

## Documentation Sections

### [Getting Started](getting-started.md)
Learn how to install and start using the Ethanol Plant Model. Includes:
- System requirements and dependencies
- Installation steps (pip and uv)
- Your first simulation
- Understanding input/output types
- Complete pipeline example

### [API Reference](api-reference.md)
Complete API documentation for all classes and methods:
- System base class with core processing methods
- Process systems (Fermentation, Filtration, Distillation, Dehydration)
- Connector systems (Pipe, Bend, Valve)
- All methods with parameters, return types, and examples

### [Process Systems](process-systems.md)
Detailed documentation for each process stage:
- Process descriptions and stoichiometry
- Input/output specifications
- Efficiency effects and typical values
- Examples with expected results
- Complete pipeline configuration

### [Connector Systems](connector-systems.md)
Fluid transport component documentation:
- Energy loss calculations and formulas
- Typical parameter values for different configurations
- Integration with process systems
- Complete transport pipeline examples

### [Examples](examples.md)
Practical tutorials and examples:
- Basic single process operations
- Complete production pipeline
- Batch processing with multiple inputs
- Flow-based processing
- Transport with energy loss connectors
- Logging and visualization techniques

## Component Tracking

The model tracks four components throughout the production process:

| Component | Density (kg/m³) | Role |
|-----------|-----------------|------|
| **Ethanol** | 789 | Product concentration |
| **Water** | 997 | Solvent and byproduct |
| **Sugar** | 1590 | Raw material and residual |
| **Fiber** | 1311 | Solid waste material |

Each `System` maintains detailed input/output histories enabling comprehensive analysis and visualization.

## Support

For questions or issues, please contact the development team:

- **Advay R. Chandra** - chand289@purdue.edu
- **Karley J. Hammond** - hammon88@purdue.edu
- **Samuel M. Razor** - razor@purdue.edu
- **Katherine E. Hampton** - hampto64@purdue.edu

## Contributing

Contributions are welcome! Please see the main [README](../README.md) for contribution guidelines:

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

MIT License - See [LICENSE](../LICENSE) file for details.

## Acknowledgments

Developed as part of ENGR-16100 coursework at Purdue University.

---

**Navigation:** [Home](README.md) | [Getting Started](getting-started.md) | [API Reference](api-reference.md) | [Process Systems](process-systems.md) | [Connector Systems](connector-systems.md) | [Examples](examples.md)
