# Ethanol Plant Model Documentation

**Version:** 0.7.0

Welcome to the comprehensive documentation for the Ethanol Plant Model project. This documentation provides detailed information about installation, usage, API reference, and examples.

## 📋 Table of Contents

1. **[Getting Started](getting-started.md)** - Installation instructions and basic setup
2. **[API Reference](api-reference.md)** - Complete API documentation for all classes and methods
3. **[Process Systems](process-systems.md)** - Detailed guide to process units (Fermentation, Filtration, etc.)
4. **[Connector Systems](connector-systems.md)** - Fluid transport components (Pipes, Bends, Valves)
5. **[Examples](examples.md)** - Practical examples and tutorials

## 🆕 What's New in v0.7.0

### Major Refactoring for Improved Design

Version 0.7.0 focuses on architectural improvements and API enhancements:

- **Static Methods for Core Conversions**: 
  - `processDensity()`, `volumetricToMass()`, and `massToVolumetric()` are now static methods
  - Eliminates unnecessary instance state dependencies
  - Improves performance for repeated conversions
  - Better adherence to Python best practices

- **Class-Level Density Constants**:
  - Density constants moved from instance variables to class constants
  - More efficient memory usage and cleaner code organization
  - Constants: `DENSITY_WATER`, `DENSITY_ETHANOL`, `DENSITY_SUGAR`, `DENSITY_FIBER`

- **Enhanced Output Flexibility**:
  - New `output_type` parameter in conversion methods
  - Three output formats: 'amount' (values), 'composition' (fractions), or 'full' (both)
  - Provides cleaner API for different use cases

- **Streamlined Documentation**:
  - Simplified docstrings without sacrificing clarity
  - Better focused parameter descriptions
  - Improved code organization and readability

- **Performance Improvements**:
  - Static methods reduce method lookup overhead
  - Class constants improve memory efficiency
  - Cleaner code flow with fewer state dependencies

## 🚀 Quick Navigation

### For New Users
Start with [Getting Started](getting-started.md) to install the package and run your first simulation.

### For Developers
Check out the [API Reference](api-reference.md) for detailed documentation of all classes and methods with comprehensive parameter descriptions and examples.

### For Process Engineers
Review [Process Systems](process-systems.md) and [Connector Systems](connector-systems.md) for detailed information about the physical models and engineering principles.

### For Learning
Explore [Examples](examples.md) for practical tutorials and use cases with clear, concise inline documentation.

## 📊 Project Features

- ✅ Mass flow rate and volumetric flow rate balance calculations
- ✅ Power consumption tracking with configurable rates and units
- ✅ Energy consumption tracking with detailed logging
- ✅ Cost tracking for process economics
- ✅ Energy loss modeling for fluid transport
- ✅ Configurable efficiency parameters
- ✅ Flexible input/output formats
- ✅ Comprehensive logging system
- ✅ Built-in visualization capabilities
- ✅ Batch processing with iterative methods
- ✅ **NEW v0.7.0**: Static methods and class constants for better design
- ✅ **NEW v0.7.0**: Flexible output type options for conversions

## 💡 Documentation Conventions

Throughout this documentation:
- **Parameters** are documented with types, units, and default values
- **Returns** include type information and explanations
- **Raises** sections document exceptions and error conditions
- **Examples** demonstrate practical usage patterns
- **Physical principles** are explained alongside calculations

## 🔗 Additional Resources

- [Main README](../README.md) - Project overview and quick start
- [CHANGELOG](../CHANGELOG.md) - Version history and updates
- [GitHub Repository](https://github.com/ENGR161-Team1/EthanolPlantModel) - Source code and issues
- [License](../LICENSE) - MIT License details

## 📝 Contributing to Documentation

If you find areas where documentation could be improved:
1. Check the source code for inline comments and docstrings
2. Review existing documentation files
3. Submit issues or pull requests with suggestions

All documentation follows [NumPy docstring conventions](https://numpydoc.readthedocs.io/en/latest/format.html) for consistency.

---

*Last updated: Version 0.7.0 - November 2025*
