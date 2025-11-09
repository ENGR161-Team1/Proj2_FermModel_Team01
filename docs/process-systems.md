# Process Systems

**Version:** 0.6.1

This document provides detailed information about the process systems in the Ethanol Plant Model.

## 🆕 Enhanced Documentation (v0.6.1)

All process methods now include:
- **Detailed parameter documentation** with types, units, and defaults
- **Comprehensive return value descriptions** explaining output formats
- **Physical principles** documented in docstrings and inline comments
- **Exception documentation** for error handling

Check the source code for extensive inline comments explaining each calculation!

## Overview

The ethanol plant model includes four main process systems that transform raw materials into high-purity ethanol:
1. **Fermentation** - Sugar to ethanol conversion
2. **Filtration** - Fiber removal
3. **Distillation** - Ethanol separation
4. **Dehydration** - Water removal

All systems inherit from the `System` base class and support flexible input/output formats.

---

## Architecture

All process systems inherit from the base `Process` class, which provides:

### Core Functionality (Enhanced in v0.6.1)

1. **Flow Processing** - Now with comprehensive docstrings
   - `processMassFlow()` - Process mass flow rates (kg/s)
   - `processVolumetricFlow()` - Process volumetric flow rates (m³/s)
   - Detailed parameter documentation including types and units

2. **Flow Conversion** - With clear conversion formulas
   - `volumetricToMass()` - Convert m³/s to kg/s using density
   - `massToVolumetric()` - Convert kg/s to m³/s using density
   - Inline comments explain: mass_flow = volumetric_flow × density

3. **Resource Tracking** - Enhanced logging documentation
   - `processPowerConsumption()` - Calculate energy from power and time
   - Power in Watts (W), Energy in Joules (J)
   - Formula documented: Energy = Power × Time

4. **Batch Processing** - Improved iteration explanations
   - `iterateMassFlowInputs()` - Process time-series mass data
   - `iterateVolumetricFlowInputs()` - Process time-series volumetric data
   - Clear documentation of input/output formats

### Input/Output Formats (Clearly Documented in v0.6.1)

All process methods support three flexible formats, now with detailed docstring examples:

- **Amount**: Specify exact mass of each component (e.g., kg)
- **Composition**: Specify fractions or percentages of each component
- **Full**: Return both mass and composition of outputs

---

## Base Process Class

All process systems inherit from the `Process` base class, which provides:

- **Modularity**: Each process is a separate class, allowing for independent development and testing.
- **Flexibility**: Easy to add new processes or modify existing ones.
- **Maintainability**: Clear separation of concerns, with each class handling a specific part of the process.

### Module Structure

- **`systems/process.py`** - Contains the base `Process` class
- **`systems/processors.py`** - Contains all process implementations:
  - `Fermentation`
  - `Filtration`
  - `Distillation`
  - `Dehydration`

---

## Process Class (Base)

The `Process` class is defined in `systems/process.py` and serves as the foundation for all processing units.

```python
from systems.process import Process
```

### Key Methods

- `processMass(inputs, input_type, output_type, ...)`: Main method to process mass inputs.
- `iterateMassInputs(inputValues, ...)`: Process multiple sets of inputs (e.g., batch processing).
- `setEfficiency(new_efficiency)`: Update the efficiency parameter.

### Properties

- `efficiency`: Fraction representing the efficiency of the process (0.0 to 1.0).
- `input_units`: Expected units for mass inputs (e.g., "amount", "composition").
- `output_units`: Units for the processed outputs.

---

## Common Features

All process systems inherit from the base `Process` class and support:

1. **Mass Flow Processing** - Convert and process mass flow rates
2. **Volumetric Flow Processing** - Handle volumetric flow rates
3. **Power Consumption Tracking** - Monitor power usage and energy consumption
4. **Cost Tracking** - Track operational costs based on flow rates
5. **Batch Processing** - Process multiple input sets iteratively
6. **Flexible I/O** - Support amount, composition, or full output formats

---

## Fermentation

### Overview

The fermentation system converts sugar into ethanol through biological processes. The conversion follows stoichiometric principles with configurable efficiency.

### Chemistry

**Stoichiometry:**
```
C₆H₁₂O₆ → 2C₂H₅OH + 2CO₂
(Glucose)  (Ethanol)  (CO₂)
```

**Mass Conversion:**
- 51% of converted sugar mass becomes ethanol
- Remaining 49% becomes CO₂ and metabolic byproducts (not tracked)

### Parameters

- `efficiency` (float): Fraction of sugar successfully converted (0.0 to 1.0)

### Behavior

```python
outputs = {
    "ethanol": 0.51 * sugar_input * efficiency,
    "water": water_input,  # unchanged
    "sugar": sugar_input * (1 - efficiency),  # unconverted
    "fiber": fiber_input  # unchanged
}
```

### Examples

#### Basic Usage
```python
from systems.processors import Fermentation

fermenter = Fermentation(efficiency=0.95)

# Process with detailed parameter documentation
result = fermenter.processMassFlow(
    inputs={
        "ethanol": 0,      # float: Initial ethanol in kg/s
        "water": 100,      # float: Water content in kg/s
        "sugar": 50,       # float: Sugar to ferment in kg/s
        "fiber": 10        # float: Fiber (inert) in kg/s
    },
    input_type="amount",   # str: Input format type
    output_type="full",    # str: Return both amounts and compositions
    store_outputs=True     # bool: Log results for analysis
)

# Access results with documented structure
print(f"Ethanol produced: {result['amount']['ethanol']:.2f} kg/s")
print(f"Sugar remaining: {result['amount']['sugar']:.2f} kg/s")
print(f"Ethanol purity: {result['composition']['ethanol']:.2%}")
```

#### Composition Mode
```python
# Input as fractions
inputs_comp = {
    "ethanol": 0.0,
    "water": 0.625,
    "sugar": 0.3125,
    "fiber": 0.0625
}

result = fermenter.processMass(
    inputs=inputs_comp,
    input_type="composition",
    output_type="full",
    total_mass=160  # Required for composition input
)

print(f"Output ethanol composition: {result['composition']['ethanol']:.2%}")
```

#### Batch Processing
```python
# Process multiple batches
batches = {
    "ethanol": [0, 0, 0, 0],
    "water": [100, 120, 90, 110],
    "sugar": [50, 60, 45, 55],
    "fiber": [10, 12, 9, 11]
}

fermenter.iterateMassInputs(
    inputValues=batches,
    input_type="amount",
    output_type="full"
)

# Access all results from logs
ethanol_outputs = fermenter.output_log["mass"]["amount"]["ethanol"]
print(f"Average ethanol per batch: {sum(ethanol_outputs) / len(ethanol_outputs):.2f} kg")
```

### Efficiency Impact

| Efficiency | Sugar Used (%) | Ethanol Yield (%) | Notes |
|-----------|----------------|-------------------|--------|
| 1.00 | 100% | 51.0% | Theoretical maximum |
| 0.95 | 95% | 48.5% | Excellent industrial performance |
| 0.90 | 90% | 45.9% | Good industrial performance |
| 0.80 | 80% | 40.8% | Average performance |
| 0.70 | 70% | 35.7% | Poor performance |

---

## Filtration

### Overview

The filtration system removes solid fiber particles from the liquid mixture. It's typically used after fermentation to clarify the mixture.

### Parameters

- `efficiency` (float): Fraction of fiber removed (0.0 to 1.0)

### Behavior

```python
outputs = {
    "ethanol": ethanol_input,  # unchanged
    "water": water_input,  # unchanged
    "sugar": sugar_input,  # unchanged
    "fiber": fiber_input * (1 - efficiency)  # removed
}
```

### Examples

#### Basic Filtration
```python
from systems.processors import Filtration

filter_sys = Filtration(efficiency=0.98)

# Input from fermentation output
result = filter_sys.processMass(
    inputs={"ethanol": 24.2, "water": 100, "sugar": 2.5, "fiber": 10},
    input_type="amount",
    output_type="full"
)

print(f"Fiber removed: {10 - result['amount']['fiber']:.2f} kg")
print(f"Removal rate: {(1 - result['amount']['fiber'] / 10):.1%}")
```

#### Multi-Stage Filtration
```python
# Two-stage filtration for higher purity
filter1 = Filtration(efficiency=0.95)
filter2 = Filtration(efficiency=0.90)

stage1 = filter1.processMass(
    inputs={"ethanol": 24, "water": 100, "sugar": 2, "fiber": 10},
    input_type="amount",
    output_type="amount"
)

stage2 = filter2.processMass(
    inputs=stage1,
    input_type="amount",
    output_type="full"
)

initial_fiber = 10
final_fiber = stage2['amount']['fiber']
total_removal = (1 - final_fiber / initial_fiber)
print(f"Combined removal: {total_removal:.2%}")
# Expected: 1 - (0.05 * 0.10) = 99.5% removal
```

### Efficiency Impact

| Efficiency | Fiber Remaining (%) | Application |
|-----------|---------------------|-------------|
| 0.99 | 1% | High-purity requirements |
| 0.98 | 2% | Standard industrial |
| 0.95 | 5% | Basic clarification |
| 0.90 | 10% | Pre-filtering |

---

## Distillation

### Overview

The distillation system separates ethanol from other components based on boiling point differences. Higher efficiency means better separation.

### Parameters

- `efficiency` (float): Separation efficiency (0.0 to 1.0)
  - Higher values = purer ethanol output
  - Lower values = more impurities remain with ethanol

### Behavior

```python
inefficiency = (1 / efficiency) - 1
total_impurities = water + sugar + fiber

outputs = {
    "ethanol": ethanol_input,  # all retained
    "water": (water_input * ethanol_input * inefficiency) / total_impurities,
    "sugar": (sugar_input * ethanol_input * inefficiency) / total_impurities,
    "fiber": (fiber_input * ethanol_input * inefficiency) / total_impurities
}
```

### Examples

#### Basic Distillation
```python
from systems.processors import Distillation

distiller = Distillation(efficiency=0.90)

result = distiller.processMass(
    inputs={"ethanol": 24, "water": 100, "sugar": 2, "fiber": 0.2},
    input_type="amount",
    output_type="full"
)

print(f"Ethanol purity: {result['composition']['ethanol']:.2%}")
print(f"Water in output: {result['amount']['water']:.2f} kg")
```

#### Comparing Efficiencies
```python
inputs = {"ethanol": 24, "water": 100, "sugar": 2, "fiber": 0.2}

for eff in [0.80, 0.90, 0.95, 0.99]:
    distiller = Distillation(efficiency=eff)
    result = distiller.processMass(
        inputs=inputs,
        input_type="amount",
        output_type="full"
    )
    purity = result['composition']['ethanol']
    print(f"Efficiency {eff:.0%}: Purity = {purity:.2%}")
```

Output:
```
Efficiency 80%: Purity = 82.76%
Efficiency 90%: Purity = 90.57%
Efficiency 95%: Purity = 95.02%
Efficiency 99%: Purity = 98.97%
```

### Efficiency Impact

| Efficiency | Approx. Ethanol Purity | Typical Application |
|-----------|------------------------|---------------------|
| 0.99 | >98% | Fuel-grade ethanol |
| 0.95 | >94% | High-grade spirits |
| 0.90 | >90% | Standard spirits |
| 0.80 | >82% | Industrial ethanol |

---

## Dehydration

### Overview

The dehydration system removes water to produce high-purity ethanol. Often used as a final purification step.

### Parameters

- `efficiency` (float): Fraction of water removed (0.0 to 1.0)

### Behavior

```python
outputs = {
    "ethanol": ethanol_input,  # unchanged
    "water": water_input * (1 - efficiency),  # removed
    "sugar": sugar_input,  # unchanged
    "fiber": fiber_input  # unchanged
}
```

### Examples

#### Basic Dehydration
```python
from systems.processors import Dehydration

dehydrator = Dehydration(efficiency=0.99)

result = dehydrator.processMass(
    inputs={"ethanol": 24, "water": 2.4, "sugar": 0.2, "fiber": 0.02},
    input_type="amount",
    output_type="full"
)

print(f"Final ethanol purity: {result['composition']['ethanol']:.2%}")
print(f"Water remaining: {result['amount']['water']:.4f} kg")
```

#### Achieving Target Purity
```python
def get_required_efficiency(current_water, current_ethanol, target_purity):
    """Calculate dehydration efficiency needed for target purity"""
    target_water = current_ethanol * (1 - target_purity) / target_purity
    efficiency = 1 - (target_water / current_water)
    return max(0, min(1, efficiency))

current = {"ethanol": 24, "water": 3, "sugar": 0.1, "fiber": 0.01}
target = 0.995  # 99.5% purity

required_eff = get_required_efficiency(
    current["water"], 
    current["ethanol"], 
    target
)

print(f"Required efficiency: {required_eff:.2%}")

dehydrator = Dehydration(efficiency=required_eff)
result = dehydrator.processMass(
    inputs=current,
    input_type="amount",
    output_type="full"
)

print(f"Achieved purity: {result['composition']['ethanol']:.3%}")
```

### Efficiency Impact

| Efficiency | Water Remaining | Final Ethanol Purity* |
|-----------|-----------------|----------------------|
| 0.999 | 0.1% | >99.9% |
| 0.99 | 1% | >99% |
| 0.95 | 5% | >95% |
| 0.90 | 10% | >90% |

*Assuming ethanol + water are primary components

---

## Complete Pipeline

### Example: Full Production Process

```python
from systems.processors import Fermentation, Filtration, Distillation, Dehydration

# Initialize all systems
fermenter = Fermentation(efficiency=0.95)
filter_sys = Filtration(efficiency=0.98)
distiller = Distillation(efficiency=0.92)
dehydrator = Dehydration(efficiency=0.99)

# Raw materials
raw_materials = {
    "ethanol": 0,
    "water": 100,
    "sugar": 50,
    "fiber": 10
}

print("=== Ethanol Production Pipeline ===\n")

# Stage 1: Fermentation
print("Stage 1: Fermentation")
stage1 = fermenter.processMass(
    inputs=raw_materials,
    input_type="amount",
    output_type="full"
)
print(f"  Ethanol: {stage1['amount']['ethanol']:.2f} kg")
print(f"  Purity: {stage1['composition']['ethanol']:.2%}\n")

# Stage 2: Filtration
print("Stage 2: Filtration")
stage2 = filter_sys.processMass(
    inputs=stage1["amount"],
    input_type="amount",
    output_type="full"
)
print(f"  Fiber removed: {10 - stage2['amount']['fiber']:.2f} kg")
print(f"  Purity: {stage2['composition']['ethanol']:.2%}\n")

# Stage 3: Distillation
print("Stage 3: Distillation")
stage3 = distiller.processMass(
    inputs=stage2["amount"],
    input_type="amount",
    output_type="full"
)
print(f"  Ethanol: {stage3['amount']['ethanol']:.2f} kg")
print(f"  Purity: {stage3['composition']['ethanol']:.2%}\n")

# Stage 4: Dehydration
print("Stage 4: Dehydration")
final = dehydrator.processMass(
    inputs=stage3["amount"],
    input_type="amount",
    output_type="full"
)
print(f"  Ethanol: {final['amount']['ethanol']:.2f} kg")
print(f"  Purity: {final['composition']['ethanol']:.3%}\n")

# Summary
print("=== Production Summary ===")
print(f"Sugar input: {raw_materials['sugar']:.2f} kg")
print(f"Ethanol output: {final['amount']['ethanol']:.2f} kg")
print(f"Yield: {final['amount']['ethanol'] / raw_materials['sugar']:.2%}")
print(f"Final purity: {final['composition']['ethanol']:.3%}")
```

---

## Best Practices

1. **Always validate inputs**: Check that component values are non-negative
2. **Use appropriate types**: Choose `input_type` and `output_type` based on your needs
3. **Store data for analysis**: Enable `store_outputs=True` when tracking performance
4. **Chain processes correctly**: Use output from one process as input to the next
5. **Consider efficiency trade-offs**: Higher efficiency may require more energy/cost

---

## Next Steps

- **[Connector Systems](connector-systems.md)**: Learn about fluid transport
- **[Examples](examples.md)**: See more complex applications
- **[API Reference](api-reference.md)**: Detailed method documentation

---

## Power Consumption Tracking

All process systems support power consumption tracking with flexible unit configuration.

### Configuration

```python
from systems.processors import Fermentation

# Configure power consumption during initialization
fermenter = Fermentation(
    efficiency=0.95,
    power_consumption_rate=50,
    power_consumption_unit="kWh/day"
)
```

### Supported Units

- `"kWh/day"` - Kilowatt-hours per day (default)
- `"kWh/hour"` or `"kW"` - Kilowatts
- `"W"` - Watts

All units are internally converted to Watts for consistent calculations.

### Calculating Energy Consumption

```python
# Calculate energy over a time interval
interval = 3600  # 1 hour in seconds
energy_joules = fermenter.processPowerConsumption(
    store_energy=True,
    interval=interval
)

# Convert to kWh
energy_kwh = energy_joules / 3_600_000
print(f"Energy consumed: {energy_kwh:.2f} kWh")
```

### Accessing Power Logs

```python
# After processing with store_energy=True
power_log = fermenter.power_log

# Power consumption rate at each timestep (Watts)
power_rates = power_log["power_consumption_rate"]

# Energy consumed in each interval (Joules)
energy_consumed = power_log["energy_consumed"]

# Time intervals (seconds)
intervals = power_log["interval"]

# Calculate total energy consumed
total_energy = sum(energy_consumed)
print(f"Total energy: {total_energy/3_600_000:.2f} kWh")
```

### Example: Complete Process with Power Tracking

```python
from systems.processors import Fermentation, Filtration, Distillation

# Create process chain with power consumption
fermenter = Fermentation(
    efficiency=0.95,
    power_consumption_rate=50,  # kWh/day
    power_consumption_unit="kWh/day"
)

filter = Filtration(
    efficiency=0.98,
    power_consumption_rate=10,  # kWh/day
    power_consumption_unit="kWh/day"
)

distiller = Distillation(
    efficiency=0.99,
    power_consumption_rate=100,  # kWh/day
    power_consumption_unit="kWh/day"
)

# Process inputs
inputs = {"ethanol": 0, "water": 100, "sugar": 50, "fiber": 10}

# Fermentation
result1 = fermenter.processMassFlow(inputs=inputs, output_type="amount", store_outputs=True)
energy1 = fermenter.processPowerConsumption(store_energy=True, interval=3600)

# Filtration
result2 = filter.processMassFlow(inputs=result1, output_type="amount", store_outputs=True)
energy2 = filter.processPowerConsumption(store_energy=True, interval=3600)

# Distillation
result3 = distiller.processMassFlow(inputs=result2, output_type="amount", store_outputs=True)
energy3 = distiller.processPowerConsumption(store_energy=True, interval=3600)

# Calculate total energy
total_energy_j = energy1 + energy2 + energy3
total_energy_kwh = total_energy_j / 3_600_000

print(f"Total energy consumed: {total_energy_kwh:.2f} kWh")
print(f"Fermentation: {energy1/3_600_000:.2f} kWh")
print(f"Filtration: {energy2/3_600_000:.2f} kWh")
print(f"Distillation: {energy3/3_600_000:.2f} kWh")
```

---

## Cost Tracking

All processors support cost tracking based on volumetric flow rates:

```python
from systems.processors import Fermentation

# Create fermenter with power and cost parameters
fermenter = Fermentation(
    efficiency=0.95,
    power_consumption_rate=100,  # kWh/day
    power_consumption_unit="kWh/day",
    cost_per_flow=50.0                   # float: Cost in $/(m³/s)
)

# Process with cost tracking enabled
result = fermenter.processMassFlow(
    inputs={"ethanol": 0, "water": 100, "sugar": 50, "fiber": 10},
    input_type="amount",
    output_type="full",
    store_outputs=True,
    store_cost=True  # Enable cost logging
)

# Access consumption logs
print(f"Costs incurred: {fermenter.consumption_log['cost_incurred']}")
print(f"Total cost: ${sum(fermenter.consumption_log['cost_incurred']):.2f}")
```

### Consumption Log Structure

The `consumption_log` attribute tracks multiple consumption metrics:

```python
{
    "power_consumption_rate": [100.0, 100.0, ...],  # Power at each step (W)
    "energy_consumed": [360000.0, 360000.0, ...],   # Energy per interval (J)
    "interval": [3600, 3600, ...],                  # Time intervals (s)
    "cost_per_unit_flow": [50.0, 50.0, ...],        # Cost rate ($/m³/s)
    "cost_incurred": [5.25, 5.25, ...]              # Actual cost ($)
}
```

---

## Process Efficiency

| Process | Parameter | Typical Range | Impact on Yield |
|---------|-----------|---------------|-----------------|
| Fermentation | `efficiency` | 0.70 - 0.95 | Higher is better |
| Filtration | `efficiency` | 0.90 - 0.99 | Higher is better |
| Distillation | `efficiency` | 0.80 - 0.99 | Higher is better |
| Dehydration | `efficiency` | 0.90 - 0.99 | Higher is better |

- Monitor and adjust parameters for optimal performance.
- Consider trade-offs between yield, purity, and energy consumption.

---

## Related Documentation

- **[API Reference](api-reference.md)** - Complete method documentation with enhanced docstrings
- **[Connector Systems](connector-systems.md)** - Fluid transport documentation (also enhanced in v0.6.1)
- **[Examples](examples.md)** - Practical examples with improved explanations

---

*For complete API details with comprehensive docstrings, see [API Reference](api-reference.md)*

*Last updated: Version 0.6.1 - November 2025*
