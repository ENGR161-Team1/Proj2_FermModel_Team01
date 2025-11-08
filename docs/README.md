# Documentation

Welcome to the Ethanol Plant Model documentation. This guide will help you understand and use the ethanol production plant simulation system.

## Version

Current version: **0.4.0**

## What's New in v0.4.0

- **Refactored Connector API**: All connector methods now use `**kwargs` for improved flexibility
- **Enhanced Flow Calculations**: Improved cube root calculation for accurate energy balance
- **Updated Logging Structure**: Separated `amount` and `composition` in logs (removed `total` from composition)
- **Better Error Handling**: Comprehensive input validation and error messages
- **Improved Mass/Flow Conversions**: More accurate density-based conversions

## Documentation Structure

### 📖 [Getting Started](getting-started.md)
Learn how to install the package and run your first simulation. Includes:
- Installation instructions for pip and uv
- System dependencies
- Quick start examples
- Basic usage patterns

### 📚 [API Reference](api-reference.md)
Complete reference for all classes and methods. Covers:
- System base class and methods
- Process systems (Fermentation, Filtration, Distillation, Dehydration)
- Connector components (Pipe, Bend, Valve)
- Method signatures and parameters
- Return value formats

### ⚙️ [Process Systems](process-systems.md)
Detailed guide to chemical process systems:
- Fermentation chemistry and efficiency
- Filtration mechanics
- Distillation separation principles
- Dehydration processes
- Configuration and usage examples

### 🔌 [Connector Systems](connector-systems.md)
Guide to fluid transport components:
- Pipe friction calculations (Darcy-Weisbach)
- Bend energy losses
- Valve resistance modeling
- Energy conservation principles
- Practical usage examples

### 💡 [Examples](examples.md)
Practical examples and tutorials:
- Complete ethanol production pipeline
- Batch processing
- Data visualization
- Iterative processing
- Advanced configurations

## Quick Navigation

**New to the project?** Start with [Getting Started](getting-started.md)

**Looking for specific methods?** Check the [API Reference](api-reference.md)

**Need examples?** Browse the [Examples](examples.md) section

**Working with connectors?** See [Connector Systems](connector-systems.md)

## Key Concepts

### Input/Output Types

The system supports three data format types:

- **`amount`**: Absolute quantities (kg for mass, m³/s for flow)
- **`composition`**: Fractional proportions (0-1, sum = 1)
- **`full`**: Both amount and composition dictionaries

### Logging Structure

Version 0.4.0 introduced a new logging structure:

```python
{
    "mass": {
        "total_mass": [],
        "amount": {"ethanol": [], "water": [], "sugar": [], "fiber": []},
        "composition": {"ethanol": [], "water": [], "sugar": [], "fiber": []}
    },
    "flow": {
        "total_flow": [],
        "amount": {"ethanol": [], "water": [], "sugar": [], "fiber": []},
        "composition": {"ethanol": [], "water": [], "sugar": [], "fiber": []}
    }
}
```

Note: `composition` no longer includes a `total` key (compositions must sum to 1).

### Components

The model tracks four components throughout the process:
- **Ethanol**: Product of fermentation
- **Water**: Solvent and fermentation byproduct
- **Sugar**: Raw material for fermentation
- **Fiber**: Solid byproduct removed by filtration

## Support

For issues or questions:
- Check the documentation sections above
- Review the [Examples](examples.md)
- Contact the development team (see README.md)

## Contributing

We welcome contributions! Please:
1. Review the existing documentation
2. Follow the established code patterns
3. Add tests for new features
4. Update documentation as needed
