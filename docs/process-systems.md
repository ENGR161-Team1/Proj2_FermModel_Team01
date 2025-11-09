# Process Systems Guide

Detailed documentation of the process units (Fermentation, Filtration, Distillation, Dehydration) and their capabilities.

## Overview

Process systems model the core transformation steps in an ethanol production plant. Each process unit handles:
- Mass and volumetric flow rate balancing
- Component stoichiometry and efficiency
- Power consumption tracking
- Cost accounting
- Comprehensive logging of inputs, outputs, and resources

## Core Processing Methods

### Static Conversion Methods (v0.7.0+)

**NEW in v0.7.0**: Conversion methods are now static, eliminating instance dependencies.

```python
# Using static methods directly on the class
from systems.process import Process

mass_flows = Process.volumetricToMass(
    inputs={"ethanol": 0.1, "water": 0.2},
    mode="amount"
)

volumetric_flows = Process.massToVolumetric(
    inputs=mass_flows,
    mode="amount"
)
```

### Input Type Modes

All processing methods support three input modes:

#### 1. 'amount' Mode
Absolute values for each component.

```python
process.processMassFlow(
    inputs={"ethanol": 100, "water": 500, "sugar": 50, "fiber": 10},
    input_type="amount"
)
```

#### 2. 'composition' Mode
Normalized fractions (must sum to approximately 1.0).

```python
process.processMassFlow(
    inputs={"ethanol": 0.1, "water": 0.7, "sugar": 0.1, "fiber": 0.1},
    input_type="composition",
    total_mass=1000  # Required for composition mode
)
```

#### 3. 'full' Mode
Both amounts and compositions together.

```python
process.processMassFlow(
    inputs={
        "amount": {"ethanol": 100, "water": 500, "sugar": 50, "fiber": 10},
        "composition": {"ethanol": 0.1, "water": 0.7, "sugar": 0.1, "fiber": 0.1}
    },
    input_type="full"
)
```

### Output Type Options (v0.7.0+)

**NEW in v0.7.0**: Flexible output formatting with `output_type` parameter.

#### 'amount' Output
Returns only component amounts:
```python
{"ethanol": 100, "water": 500, "sugar": 50, "fiber": 10}
```

#### 'composition' Output
Returns only normalized fractions:
```python
{"ethanol": 0.1, "water": 0.7, "sugar": 0.1, "fiber": 0.1}
```

#### 'full' Output (Default)
Returns both amounts and compositions:
```python
{
    "amount": {"ethanol": 100, "water": 500, "sugar": 50, "fiber": 10},
    "composition": {"ethanol": 0.1, "water": 0.7, "sugar": 0.1, "fiber": 0.1}
}
```

## Processor Classes

### Fermentation

Models the ethanol fermentation process where sugars are converted to ethanol.

```python
from systems.processors import Fermentation

fermenter = Fermentation(
    name="Main Fermenter",
    efficiency=0.85,
    power_consumption_rate=20,
    power_consumption_unit="kW",
    cost=1000,
    cost_per_flow=50
)

# Process inputs
output = fermenter.processMassFlow(
    inputs={"ethanol": 10, "water": 100, "sugar": 50, "fiber": 5},
    input_type="amount",
    store_inputs=True,
    store_outputs=True,
    store_cost=True
)
```

### Filtration

Separates solids from liquids in the ethanol production process.

```python
from systems.processors import Filtration

filter_unit = Filtration(
    name="Main Filter",
    efficiency=0.90,
    power_consumption_rate=15,
    power_consumption_unit="kW"
)

output = filter_unit.processVolumetricFlow(
    inputs={
        "amount": {"ethanol": 0.1, "water": 0.5, "sugar": 0.05, "fiber": 0.01},
        "composition": {"ethanol": 0.1, "water": 0.6, "sugar": 0.2, "fiber": 0.1}
    },
    input_type="full",
    store_outputs=True
)
```

### Distillation

Separates ethanol from water based on boiling points.

```python
from systems.processors import Distillation

distiller = Distillation(
    name="Main Still",
    efficiency=0.75,
    power_consumption_rate=50,
    power_consumption_unit="kW"
)
```

### Dehydration

Removes remaining water to produce fuel-grade ethanol.

```python
from systems.processors import Dehydration

dehydrator = Dehydration(
    name="Dehydration Unit",
    efficiency=0.80,
    power_consumption_rate=25,
    power_consumption_unit="kW"
)
```

## Batch Processing

Process multiple inputs iteratively using `iterateMassFlowInputs()` or `iterateVolumetricFlowInputs()`.

```python
# Process time-series data
time_series_data = {
    "ethanol": [100, 105, 110, 108, 112],
    "water": [500, 510, 520, 515, 525],
    "sugar": [50, 52, 55, 53, 56],
    "fiber": [10, 11, 12, 11, 13]
}

results = process.iterateMassFlowInputs(
    inputValues=time_series_data,
    input_type="amount",
    output_type="full"
)

# Results are automatically logged to process.output_log
print(f"Processed {len(results['mass_flow']['total_mass_flow'])} time steps")
```

## Power Consumption Tracking

Track instantaneous power consumption and cumulative energy usage.

```python
# Calculate energy consumed over 1 hour (3600 seconds)
energy = process.processPowerConsumption(
    store_energy=True,
    interval=3600
)

# Access consumption logs
power_rates = process.consumption_log["power_consumption_rate"]
energy_values = process.consumption_log["energy_consumed"]
intervals = process.consumption_log["interval"]

# Calculate total energy
total_energy = sum(process.consumption_log["energy_consumed"])
print(f"Total energy consumed: {total_energy} J ({total_energy/3.6e6} kWh)")
```

## Cost Tracking

Track variable and fixed costs during processing.

```python
process = Process(
    name="Cost Tracking Example",
    cost=1000,              # Fixed cost per operation
    cost_per_flow=50        # Variable cost per m³/s
)

# Costs are logged during processing
output = process.processMassFlow(
    inputs={"ethanol": 100, "water": 500, "sugar": 50, "fiber": 10},
    input_type="amount",
    store_cost=True
)

# Access cost logs
costs_per_unit = process.consumption_log["cost_per_unit_flow"]
total_costs = process.consumption_log["cost_incurred"]
print(f"Total cost incurred: ${sum(total_costs)}")
```

## Logging and Data Retrieval

### Accessing Logged Data

All processing methods automatically log data when `store_inputs` or `store_outputs` flags are True.

```python
# After processing
input_mass_flows = process.input_log["mass_flow"]["amount"]["ethanol"]
output_compositions = process.output_log["volumetric_flow"]["composition"]
power_data = process.consumption_log["power_consumption_rate"]
```

### Log Structure

Each process maintains three logs:

1. **input_log**: Stores all input data (mass and volumetric)
2. **output_log**: Stores all output data (mass and volumetric)
3. **consumption_log**: Stores power, energy, and cost data

## Best Practices

### 1. Use Static Methods for Conversions

**v0.7.0+**: Always use static methods for density conversions:

```python
# ✓ Correct (v0.7.0+)
mass = Process.volumetricToMass(inputs=volumetric, mode="amount")

# ✗ Avoid (older style)
mass = process.volumetricToMass(inputs=volumetric, mode="amount")
```

### 2. Choose Appropriate Output Types

Use `output_type` parameter for cleaner code:

```python
# Get only amounts
amounts = process.processMassFlow(
    inputs=data,
    output_type="amount"  # Returns dict of amounts only
)

# Get only compositions
compositions = process.processMassFlow(
    inputs=data,
    output_type="composition"  # Returns dict of fractions only
)

# Get both (for logging)
full = process.processMassFlow(
    inputs=data,
    output_type="full"  # Returns {"amount": {...}, "composition": {...}}
)
```

### 3. Enable Logging Strategically

```python
# Logging adds overhead - only enable when needed
output = process.processMassFlow(
    inputs=data,
    store_inputs=True,    # Only if you need input history
    store_outputs=True,   # Only if you need output history
    store_cost=True       # Only if tracking costs
)
```

### 4. Batch Processing for Time-Series

Use iteration methods for time-series data:

```python
# More efficient than individual calls
results = process.iterateMassFlowInputs(
    inputValues=time_series,
    input_type="amount"
)
```

## Component Constants

The Process class uses class-level density constants (v0.7.0+):

```python
Process.DENSITY_WATER = 997      # kg/m³
Process.DENSITY_ETHANOL = 789    # kg/m³
Process.DENSITY_SUGAR = 1590     # kg/m³
Process.DENSITY_FIBER = 1311     # kg/m³
```

These constants are used automatically in all conversion calculations.

---

For more examples, see [Examples](examples.md).
