# Process Systems

Detailed guide to the chemical process systems in the Ethanol Plant Model (v0.4.0).

## Overview

The model includes four main process systems:
1. **Fermentation** - Sugar to ethanol conversion
2. **Filtration** - Fiber removal
3. **Distillation** - Ethanol separation
4. **Dehydration** - Water removal

All systems inherit from the `System` base class and support flexible input/output formats.

---

## Architecture

All process systems inherit from the base `Process` class, which provides:

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

result = fermenter.processMass(
    inputs={"ethanol": 0, "water": 100, "sugar": 50, "fiber": 10},
    input_type="amount",
    output_type="full"
)

print(f"Ethanol produced: {result['amount']['ethanol']:.2f} kg")
print(f"Sugar consumed: {50 - result['amount']['sugar']:.2f} kg")
print(f"Conversion efficiency: {result['amount']['ethanol'] / (50 * 0.51):.1%}")
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

## Process Efficiency

| Process | Parameter | Typical Range | Impact on Yield |
|---------|-----------|---------------|-----------------|
| Fermentation | `efficiency` | 0.70 - 0.95 | Higher is better |
| Filtration | `efficiency` | 0.90 - 0.99 | Higher is better |
| Distillation | `efficiency` | 0.80 - 0.99 | Higher is better |
| Dehydration | `efficiency` | 0.90 - 0.99 | Higher is better |

- Monitor and adjust parameters for optimal performance.
- Consider trade-offs between yield, purity, and energy consumption.
