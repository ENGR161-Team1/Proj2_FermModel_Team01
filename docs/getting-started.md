# Getting Started

**Version:** 0.7.0

This guide will help you install and start using the Ethanol Plant Model.

## 🆕 What's New in v0.7.0

Version 0.7.0 includes major architectural improvements:
- **Static methods** for core conversions - cleaner API and better performance
- **Class-level density constants** - improved code organization and efficiency
- **Flexible output types** - choose between amounts, compositions, or both
- **Streamlined docstrings** - easier to read while maintaining clarity

See [API Reference](api-reference.md) for v0.7.0 migration guide!

## Installation

### Prerequisites

- Python >= 3.10
- System dependencies (Ubuntu/Debian):
  ```bash
  sudo apt install libgirepository2.0-dev libcairo2-dev libgtk-4-dev \
      pkg-config python3-dev python3-gi python3-gi-cairo \
      gir1.2-gtk-4.0 gobject-introspection
  ```

### Using pip

```bash
git clone https://github.com/ENGR161-Team1/EthanolPlantModel.git
cd EthanolPlantModel
pip install .
```

### Using uv (Recommended)

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
git clone https://github.com/ENGR161-Team1/EthanolPlantModel.git
cd EthanolPlantModel
uv pip install .
```

## Key Features

- ✅ **Mass and Volumetric Flow Processing** - Handle both mass and volumetric flow rates
- ✅ **Power Consumption Tracking** - Monitor energy usage with configurable rates
- ✅ **Cost Tracking** - Track operational costs based on volumetric flow rates
- ✅ **Flexible I/O Formats** - Support amount, composition, or full output formats
- ✅ **Comprehensive Logging** - Track inputs, outputs, power, energy, and costs
- ✅ **Batch Processing** - Process multiple input sets efficiently
- ✅ **Process Efficiency Modeling** - Configure efficiency parameters for each unit
- ✅ **Fluid Transport Dynamics** - Model energy losses in pipes, bends, and valves
- ✅ **v0.7.0: Static Methods** - Cleaner API for conversion functions
- ✅ **v0.7.0: Flexible Output Types** - Choose output format that fits your needs

## Basic Usage

### Simple Example

```python
from systems.processors import Fermentation

# Create a fermentation system with efficiency and cost parameters
fermenter = Fermentation(
    efficiency=0.95,
    power_consumption_rate=100,
    power_consumption_unit="kWh/day",
    cost_per_flow=25.0  # $25 per m³/s of flow
)

# Process mass flow inputs with cost tracking
result = fermenter.processMassFlow(
    inputs={"ethanol": 0, "water": 100, "sugar": 50, "fiber": 10},
    input_type="amount",
    output_type="full",
    store_outputs=True,
    store_cost=True  # Track costs
)

# Access results
print(f"Ethanol produced: {result['amount']['ethanol']:.2f} kg")
print(f"Ethanol purity: {result['composition']['ethanol']:.2%}")

# Check consumption data
print(f"Cost incurred: ${fermenter.consumption_log['cost_incurred'][-1]:.2f}")
```

### Processing Mass Flow Rates

```python
# Process mass flow rate inputs
result = fermenter.processMassFlow(
    inputs={"ethanol": 0, "water": 100, "sugar": 50, "fiber": 10},
    input_type="amount",
    output_type="full",
    store_outputs=True
)

print(f"Ethanol produced: {result['amount']['ethanol']:.2f} kg/s")
print(f"Ethanol purity: {result['composition']['ethanol']:.2%}")
```

### Processing Volumetric Flow Rates

```python
# Process volumetric flow rate inputs
result = fermenter.processVolumetricFlow(
    inputs={"water": 0.1, "sugar": 0.03, "fiber": 0.01},  # m³/s
    input_type="amount",
    output_type="full",
    store_outputs=True
)

print(f"Total output flow: {sum(result['amount'].values()):.4f} m³/s")
```

### Energy Consumption Tracking

```python
# Create a process with energy consumption
from systems.processors import Distillation

distiller = Distillation(
    efficiency=0.90,
    power_consumption_rate=100,
    power_consumption_unit="kW"
)

# Calculate energy consumed over 1 hour (3600 seconds)
energy = distiller.processPowerConsumption(
    interval=3600,
    store_energy=True
)

print(f"Energy consumed: {energy/3.6e6:.2f} kWh")
```

### Batch Processing

```python
# Process multiple input sets
batch_inputs = {
    "ethanol": [0, 0, 0],
    "water": [100, 150, 200],
    "sugar": [50, 75, 100],
    "fiber": [10, 15, 20]
}

output_log = fermenter.iterateMassFlowInputs(
    inputValues=batch_inputs,
    input_type="amount",
    output_type="full"
)

# Access results
ethanol_outputs = output_log["mass_flow"]["amount"]["ethanol"]
print(f"Ethanol production: {ethanol_outputs}")
```

## Understanding Input/Output Types

### Input Types

- **`amount`**: Absolute mass flow rates (kg/s) or volumetric flow rates (m³/s)
- **`composition`**: Fractional compositions (0-1) + total flow rate
- **`full`**: Both amounts and compositions provided

### Output Types (v0.7.0+)

- **`amount`**: Returns only component amounts - lightweight output
- **`composition`**: Returns only component fractions - minimal data
- **`full`**: Returns both amounts and compositions - complete data

**Example:**
```python
# Get only amounts (lightweight)
amounts = fermenter.processMassFlow(inputs=data, output_type="amount")
# Returns: {"ethanol": 24.44, "water": 89.5, ...}

# Get only compositions (normalized fractions)
comps = fermenter.processMassFlow(inputs=data, output_type="composition")
# Returns: {"ethanol": 0.152, "water": 0.558, ...}

# Get both (complete)
full = fermenter.processMassFlow(inputs=data, output_type="full")
# Returns: {"amount": {...}, "composition": {...}}
```

## Static Methods (v0.7.0+)

**NEW**: Core conversion methods are now static - call them directly on the class!

### Using Static Conversion Methods

```python
from systems.process import Process

# Convert volumetric to mass using static method
mass_flows = Process.volumetricToMass(
    inputs={"ethanol": 0.05, "water": 0.25},
    mode="amount"
)

# Convert mass to volumetric using static method
volumetric_flows = Process.massToVolumetric(
    inputs=mass_flows,
    mode="amount"
)

# Calculate density using static method
density = Process.processDensity(mass_flow=100, volumetric_flow=0.1)
```

### Class-Level Density Constants (v0.7.0+)

Access component densities directly from the class:

```python
print(f"Water density: {Process.DENSITY_WATER} kg/m³")
print(f"Ethanol density: {Process.DENSITY_ETHANOL} kg/m³")
print(f"Sugar density: {Process.DENSITY_SUGAR} kg/m³")
print(f"Fiber density: {Process.DENSITY_FIBER} kg/m³")

# Used automatically in all conversions
```

## Migration from v0.6.x to v0.7.0

### Static Method Changes

```python
# ❌ v0.6.x style (instance method)
mass = process.volumetricToMass(inputs=data, mode="amount")

# ✅ v0.7.0 style (static method)
mass = Process.volumetricToMass(inputs=data, mode="amount")

# Both work, but v0.7.0 is cleaner and faster
```

### Output Type Parameter

```python
# v0.7.0: Choose what you want back
amounts_only = process.processMassFlow(
    inputs=data,
    output_type="amount"  # Just amounts
)

comps_only = process.processMassFlow(
    inputs=data,
    output_type="composition"  # Just compositions
)

full_data = process.processMassFlow(
    inputs=data,
    output_type="full"  # Both (default)
)
```

## Next Steps

Now that you have the basics:

1. **Explore the API**: Check out [API Reference](api-reference.md) for complete method documentation
2. **Learn about processes**: Read [Process Systems](process-systems.md) for detailed process information
3. **Understand connectors**: See [Connector Systems](connector-systems.md) for fluid transport physics
4. **Try examples**: Work through [Examples](examples.md) with practical tutorials
5. **Review source code**: All code includes comprehensive inline comments

## Getting Help

### Using Built-in Help

In Python, you can access documentation directly:

```python
# View class documentation
help(Fermentation)

# View method documentation
help(fermenter.processMassFlow)

# In IPython/Jupyter
Fermentation?
fermenter.processMassFlow?
```

### Understanding Errors

v0.7.0 maintains clear error messages. When you encounter a `ValueError`:

```python
try:
    result = process.processMassFlow(inputs={}, input_type='composition')
except ValueError as e:
    print(f"Error: {e}")
    # Output: Error clearly states what's missing and why
```

### Common Issues

**Issue**: `AttributeError: 'Process' object has no attribute 'volumetricToMass'`
```python
# ❌ Wrong: Using as instance method
mass = process.volumetricToMass(inputs=data)

# ✅ Correct: Use static method on class
mass = Process.volumetricToMass(inputs=data)
```

**Issue**: `KeyError` when accessing results
```python
# Check what output_type you requested
result = process.processMassFlow(inputs=data, output_type="amount")
# Returns: dict of amounts only, no 'composition' key

# Use output_type="full" to get both
result = process.processMassFlow(inputs=data, output_type="full")
# Returns: {"amount": {...}, "composition": {...}}
```

---

*For detailed API documentation, see [API Reference](api-reference.md)*

*For practical examples, see [Examples](examples.md)*

*Last updated: Version 0.7.0 - November 2025*
