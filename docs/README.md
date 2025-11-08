# Ethanol Plant Model Documentation

**Version:** 0.3.0

Welcome to the Ethanol Plant Model documentation. This project provides a comprehensive simulation of an ethanol production plant developed for ENGR-16100 coursework.

## 📖 Documentation

### Getting Started
- [Installation and Setup](getting-started.md)
- [Basic Usage Examples](getting-started.md#basic-usage)
- [Your First Simulation](getting-started.md#your-first-simulation)

### Reference Documentation
- [Complete API Reference](api-reference.md)
- [Process Systems Guide](process-systems.md)
- [Connector Systems Guide](connector-systems.md)

### Tutorials and Examples
- [Practical Examples](examples.md)
- [Complete Pipeline Examples](examples.md#complete-pipeline)
- [Batch Processing](examples.md#batch-processing)

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

## Documentation Structure

| Section | Description |
|---------|-------------|
| [Getting Started](getting-started.md) | Installation, setup, and basic usage |
| [API Reference](api-reference.md) | Complete API documentation with all methods |
| [Process Systems](process-systems.md) | Detailed guide to fermentation, filtration, distillation, and dehydration |
| [Connector Systems](connector-systems.md) | Fluid transport components: pipes, bends, and valves |
| [Examples](examples.md) | Practical examples and complete tutorials |

## Support

For questions or issues, please contact the development team:

- **Advay R. Chandra** - chand289@purdue.edu
- **Karley J. Hammond** - hammon88@purdue.edu
- **Samuel M. Razor** - razor@purdue.edu
- **Katherine E. Hampton** - hampto64@purdue.edu

## Contributing

Contributions are welcome! Please see the main [README](../README.md) for contribution guidelines.

## License

MIT License - See [LICENSE](../LICENSE) file for details.

---

**Navigation:** [Home](README.md) | [Getting Started](getting-started.md) | [API Reference](api-reference.md) | [Examples](examples.md)
