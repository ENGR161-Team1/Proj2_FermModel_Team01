# Getting Started

**Version:** 0.6.1

This guide will help you install and start using the Ethanol Plant Model.

## 🆕 What's New in v0.6.1

Version 0.6.1 includes comprehensive documentation enhancements:
- **Detailed docstrings** for all methods with parameter types, units, and defaults
- **Enhanced inline comments** explaining complex calculations
- **Physical principles** documented alongside mathematical operations
- **Better error documentation** with exception types and conditions

This makes learning and using the API much easier!

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
    inputs={"water": 0.1, "sugar": 0.03, "fiber": 0.008},  # m³/s
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
    energy_consumption_rate=100,  # kWh/day
    energy_consumption_unit="kWh/day"
)

# Calculate energy consumed over 1 hour (3600 seconds)
energy = distiller.processEnergyConsumption(
    interval=3600,
    store_energy=True
)

print(f"Energy consumed: {energy/1000:.2f} kJ")
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

### Output Types

- **`amount`**: Returns only component amounts
- **`composition`**: Returns only component compositions
- **`full`**: Returns both amounts and compositions

## Understanding the Documentation

### Docstring Conventions (v0.6.1)

All methods now follow comprehensive docstring standards:

```python
def processMassFlow(self, **kwargs):
    """
    Process mass flow rate inputs through the system.
    
    Args:
        inputs (dict): Dictionary of input values in kg/s
        input_type (str, optional): Format - 'amount', 'composition', or 'full'. Default: 'full'
        total_mass (float, optional): Total mass flow rate in kg/s. Required for 'composition' mode
        store_outputs (bool, optional): Whether to log outputs. Default: False
    
    Returns:
        dict: Processed outputs with same format as input_type
    
    Raises:
        ValueError: If inputs are invalid or missing required parameters
    """
```

Key features:
- **Type information**: Every parameter includes its Python type
- **Units**: Physical quantities include units (kg/s, m³/s, W, J, $)
- **Defaults**: Optional parameters show their default values
- **Return types**: Clear description of what's returned
- **Exceptions**: Documents error conditions

### Inline Comments (v0.6.1)

Complex calculations now include step-by-step explanations:

```python
# Convert volumetric flow to mass flow using component densities
# Relationship: mass_flow = volumetric_flow × density
mass_flow = volumetric_flow * self.densityWater  # kg/s = m³/s × kg/m³

# Calculate kinetic power from flow velocity
# Formula: P = (1/2) × m × v²
input_power = input_mass_flow * (velocity ** 2) / 2  # Watts
```

## Next Steps

Now that you have the basics:

1. **Explore the API**: Check out [API Reference](api-reference.md) for detailed method documentation with enhanced docstrings
2. **Learn about processes**: Read [Process Systems](process-systems.md) for detailed process information
3. **Understand connectors**: See [Connector Systems](connector-systems.md) for fluid transport physics
4. **Try examples**: Work through [Examples](examples.md) with improved inline documentation
5. **Review source code**: All code now includes comprehensive comments explaining the logic

## Getting Help

### Using Docstrings

In Python, you can access documentation directly:

```python
# View method documentation
help(fermenter.processMassFlow)

# View class documentation
help(Fermentation)

# In IPython/Jupyter
fermenter.processMassFlow?
```

### Understanding Errors

Version 0.6.1 includes improved error messages. When you encounter a `ValueError`:

```python
try:
    result = process.processMassFlow(inputs={}, input_type='composition')
except ValueError as e:
    print(f"Error: {e}")
    # Output: "total_mass must be provided when input_type is 'composition'"
```

The error messages now clearly explain:
- What parameter is missing
- What condition caused the error
- What you need to provide to fix it

---

*For detailed API documentation with comprehensive docstrings, see [API Reference](api-reference.md)*

*Last updated: Version 0.6.1 - November 2025*
