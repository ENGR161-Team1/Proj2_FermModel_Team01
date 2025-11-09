# Ethanol Plant Model Documentation

Welcome to the Ethanol Plant Model documentation! This guide will help you understand and use the ethanol production simulation system.

## 📖 Table of Contents

### Getting Started
- **[Installation & Setup](getting-started.md)** - Install the package and verify your setup
- **[Quick Start Guide](getting-started.md#quick-start)** - Get running in minutes
- **[Basic Concepts](getting-started.md#basic-concepts)** - Core concepts and terminology

### Core Documentation
- **[API Reference](api-reference.md)** - Complete API documentation for all classes and methods
- **[Process Systems](process-systems.md)** - Fermentation, Filtration, Distillation, and Dehydration
- **[Connector Systems](connector-systems.md)** - Pipes, Bends, Valves, and fluid transport
- **[Pump System](pump-system.md)** - Pump modeling and fluid dynamics
- **[Facility System](facility-system.md)** - Integrated facility management and orchestration

### Practical Guides
- **[Examples & Tutorials](examples.md)** - Step-by-step examples and common use cases
- **[Best Practices](best-practices.md)** - Tips for effective modeling
- **[Troubleshooting](troubleshooting.md)** - Common issues and solutions

## 🚀 Quick Navigation

### By Use Case

**I want to...**
- **Model a single process** → [Process Systems](process-systems.md)
- **Connect multiple components** → [Connector Systems](connector-systems.md)
- **Add pumping capability** → [Pump System](pump-system.md)
- **Build a complete facility** → [Facility System](facility-system.md)
- **Track power consumption** → [API Reference - Power Tracking](api-reference.md#power-consumption-tracking)
- **Calculate costs** → [API Reference - Cost Tracking](api-reference.md#cost-tracking)
- **See working examples** → [Examples](examples.md)

### By Component Type

- **[Base Process Class](api-reference.md#process-class)** - Foundation for all processes
- **[Fermentation](process-systems.md#fermentation)** - Sugar to ethanol conversion
- **[Filtration](process-systems.md#filtration)** - Solid particle removal
- **[Distillation](process-systems.md#distillation)** - Ethanol concentration
- **[Dehydration](process-systems.md#dehydration)** - Water removal for high purity
- **[Pipe](connector-systems.md#pipe)** - Straight segment transport
- **[Bend](connector-systems.md#bend)** - Direction change with losses
- **[Valve](connector-systems.md#valve)** - Flow control
- **[Pump](pump-system.md)** - Pressure/velocity increase
- **[Facility](facility-system.md)** - Complete system integration

## 📊 Model Capabilities

### Flow Calculations
- Mass flow rate processing
- Volumetric flow rate processing
- Automatic unit conversions
- Component tracking (ethanol, water, sugar, fiber)

### Energy & Power
- Power consumption tracking
- Energy balance calculations
- Pump efficiency modeling
- Net energy gain analysis

### Economic Analysis
- Cost tracking per flow rate
- Economic viability assessment
- Power cost calculations
- Revenue projections

### Data Management
- Comprehensive logging systems
- Batch processing capabilities
- Visualization support
- Multiple output formats

## 🎯 Learning Path

### Beginner
1. Read [Getting Started](getting-started.md)
2. Review [Basic Concepts](getting-started.md#basic-concepts)
3. Try [Example 1: Simple Fermentation](examples.md#example-1-simple-fermentation)
4. Explore [Process Systems](process-systems.md)

### Intermediate
1. Study [Connector Systems](connector-systems.md)
2. Learn about [Pump System](pump-system.md)
3. Work through [Example 3: Complete Pipeline](examples.md#example-3-complete-process-pipeline)
4. Review [Power Tracking](api-reference.md#power-consumption-tracking)

### Advanced
1. Master [Facility System](facility-system.md)
2. Implement [Example 6: Complete Facility](examples.md#example-6-complete-facility-with-pump-and-power-analysis)
3. Study [Best Practices](best-practices.md)
4. Explore economic optimization

## 🔧 Technical Reference

### Key Classes
- `Process` - Base class for all processes
- `Fermentation`, `Filtration`, `Distillation`, `Dehydration` - Processor implementations
- `Connector`, `Pipe`, `Bend`, `Valve` - Fluid transport components
- `Pump` - Pumping operations
- `Facility` - System integration

### Key Methods
- `processMassFlow()` - Process mass flow rates
- `processVolumetricFlow()` - Process volumetric flow rates
- `processPowerConsumption()` - Track power usage
- `pump_process()` - Pump operations
- `facility_process()` - Complete facility processing

### Physical Constants
- Water density: 1000 kg/m³
- Ethanol density: 789 kg/m³
- Sugar density: 1590 kg/m³
- Fiber density: 1500 kg/m³
- Ethanol energy density: 28.818 MJ/kg

## 📝 Additional Resources

- **[CHANGELOG](../CHANGELOG.md)** - Version history and updates
- **[README](../README.md)** - Project overview
- **[GitHub Repository](https://github.com/ENGR161-Team1/EthanolPlantModel)** - Source code
- **[Issue Tracker](https://github.com/ENGR161-Team1/EthanolPlantModel/issues)** - Report bugs

## 🤝 Contributing

We welcome contributions! Please see the main [README](../README.md#contributing) for guidelines.

## 📧 Support

For questions or issues:
- Check [Troubleshooting](troubleshooting.md)
- Search existing [Issues](https://github.com/ENGR161-Team1/EthanolPlantModel/issues)
- Contact the team (see [README](../README.md#team-members))

---

**Version:** 0.8.0 | **Last Updated:** November 2025
