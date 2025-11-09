# Ethanol Plant Model Documentation

**Version:** 0.6.1

Welcome to the comprehensive documentation for the Ethanol Plant Model project. This documentation provides detailed information about installation, usage, API reference, and examples.

## 📋 Table of Contents

1. **[Getting Started](getting-started.md)** - Installation instructions and basic setup
2. **[API Reference](api-reference.md)** - Complete API documentation for all classes and methods
3. **[Process Systems](process-systems.md)** - Detailed guide to process units (Fermentation, Filtration, etc.)
4. **[Connector Systems](connector-systems.md)** - Fluid transport components (Pipes, Bends, Valves)
5. **[Examples](examples.md)** - Practical examples and tutorials

## 🆕 What's New in v0.6.1

### Documentation Enhancements

Version 0.6.1 focuses on comprehensive documentation improvements:

- **Enhanced Docstrings**: All Process and Connector class methods now have detailed docstrings with:
  - Complete parameter descriptions including types and units
  - Detailed return value documentation
  - Exception documentation for error conditions
  - Clear explanations of method functionality

- **Improved Code Clarity**: Added extensive inline comments explaining:
  - Mass to volumetric flow rate conversions
  - Energy and power consumption tracking
  - Cost calculation mechanisms
  - Logging structures and data storage

- **Better Physical Explanations**: Documented the physics behind:
  - Darcy-Weisbach friction losses in pipes
  - Bend losses due to flow direction changes
  - Valve resistance calculations

## 🚀 Quick Navigation

### For New Users
Start with [Getting Started](getting-started.md) to install the package and run your first simulation.

### For Developers
Check out the [API Reference](api-reference.md) for detailed documentation of all classes and methods with comprehensive parameter descriptions and examples.

### For Process Engineers
Review [Process Systems](process-systems.md) and [Connector Systems](connector-systems.md) for detailed information about the physical models and engineering principles.

### For Learning
Explore [Examples](examples.md) for practical tutorials and use cases, now with improved inline documentation for easier understanding.

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
- ✅ **NEW**: Comprehensive documentation with detailed docstrings and inline comments

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

*Last updated: Version 0.6.1 - November 2025*
