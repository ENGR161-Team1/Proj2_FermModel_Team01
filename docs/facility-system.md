# Facility System Documentation

The Facility class orchestrates complete process chains, integrating pumps, processes, and connectors with comprehensive power tracking and energy analysis.

## Overview

The Facility class provides high-level system integration that:
- Manages sequential processing through multiple components
- Automatically handles flow state conversions (mass ↔ volumetric)
- Tracks total power consumption across all equipment
- Calculates energy generation from ethanol production
- Analyzes net energy gain for economic viability

## Table of Contents

- [Class Initialization](#class-initialization)
- [Methods](#methods)
- [Flow Management](#flow-management)
- [Power Tracking](#power-tracking)
- [Usage Examples](#usage-examples)
- [Best Practices](#best-practices)

## Class Initialization

### `Facility(**kwargs)`

Creates a new Facility instance with integrated components.

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `components` | list | [] | List of Process and Connector instances |
| `pump` | Pump | Pump() | Pump instance for the facility |

**Example:**

```python
from systems.facility import Facility
from systems.pump import Pump
from systems.processors import Fermentation, Distillation
from systems.connectors import Pipe

# Create facility with all components
facility = Facility(
    pump=Pump(efficiency=0.85),
    components=[
        Fermentation(efficiency=0.95),
        Pipe(length=50, diameter=0.1),
        Distillation(efficiency=0.92)
    ]
)
```

## Methods

### `add_component(component)`

Adds a process or connector to the facility's component chain.

**Parameters:**
- `component` (Process or Connector): Component to add

**Example:**

```python
facility = Facility()
facility.add_component(Fermentation(efficiency=0.95))
facility.add_component(Pipe(length=10))
facility.add_component(Distillation(efficiency=0.90))
```

### `facility_process(**kwargs)`

Processes material through all facility components sequentially.

**Parameters:**

| Parameter | Type | Required | Default | Unit | Description |
|-----------|------|----------|---------|------|-------------|
| `input_volume_composition` | dict | Yes | - | - | Component volume fractions |
| `input_volumetric_flow` | float | Yes | - | m³/s | Total input flow rate |
| `store_data` | bool | No | False | - | Log input/output data |
| `interval` | float | No | 1 | s | Time interval for energy calcs |

**Returns:**

`dict` with keys:
- `"volumetric_flow"` (dict): Output volumetric flow data
  - `"total_volumetric_flow"` (float): Total flow in m³/s
  - `"amount"` (dict): Component flows in m³/s
  - `"composition"` (dict): Component fractions
- `"mass_flow"` (dict): Output mass flow data
  - `"total_mass_flow"` (float): Total flow in kg/s
  - `"amount"` (dict): Component flows in kg/s
  - `"composition"` (dict): Component fractions
- `"total_power_consumed"` (float): Total power in Watts
- `"power_generated"` (float): Energy from ethanol in Joules
- `"net_power_gained"` (float): Net energy (generated - consumed) in Joules

**Example:**

```python
result = facility.facility_process(
    input_volume_composition={
        "water": 0.625,
        "sugar": 0.3125,
        "fiber": 0.0625
    },
    input_volumetric_flow=0.001,  # 1 L/s
    interval=3600,  # 1 hour
    store_data=True
)

print(f"Power consumed: {result['total_power_consumed']/1000:.2f} kW")
print(f"Energy generated: {result['power_generated']/1e6:.2f} MJ")
print(f"Net gain: {result['net_power_gained']/1e6:.2f} MJ")
```

## Flow Management

### Automatic State Conversions

The facility automatically manages flow representations:

```
Input (volumetric) → Pump → Process 1 → Connector 1 → Process 2 → ... → Output
         ↓              ↓         ↓            ↓            ↓              ↓
    Composition     Mass flow  Vol flow    Mass flow    Vol flow    Both formats
```

**Conversion points:**
1. **Input** → Converted to both mass and volumetric representations
2. **After pump** → Volumetric flow updated, converted to mass
3. **After each process** → Volumetric output converted to mass
4. **After each connector** → Mass flow converted back to volumetric
5. **Output** → Both representations provided

### Component Processing Order

```python
# Processing sequence:
1. Convert input composition to mass/volumetric flows
2. Process through pump (update both representations)
3. For each component in components list:
   a. If Process: 
      - Process volumetric flow
      - Track power consumption
      - Convert output to mass
   b. If Connector:
      - Calculate power consumed
      - Process flow (apply losses)
      - Convert mass to volumetric
4. Calculate energy generated from ethanol
5. Return complete results
```

## Power Tracking

### Total Power Consumption

Power is accumulated from three sources:

```python
total_power = pump_power + process_powers + connector_powers
```

**Pump Power:**
```python
pump_power = input_kinetic_energy + energy_added
```

**Process Power:**
```python
process_power = power_consumption_rate  # Configured for each process
```

**Connector Power:**
```python
connector_power = energy_lost_to_friction  # From Darcy-Weisbach, etc.
```

### Energy Generation

Energy from ethanol production:

```python
E_generated = ethanol_mass_flow × ETHANOL_ENERGY_DENSITY × interval
```

Where:
- `ETHANOL_ENERGY_DENSITY` = 28.818 MJ/kg
- `ethanol_mass_flow` = Final ethanol output in kg/s
- `interval` = Time period in seconds

### Net Energy Gain

```python
net_energy = energy_generated - total_power_consumed
```

**Positive net energy** → Economically viable
**Negative net energy** → Energy input exceeds output

## Usage Examples

### Example 1: Simple Facility

```python
from systems.facility import Facility
from systems.pump import Pump
from systems.processors import Fermentation

# Create simple facility
facility = Facility(
    pump=Pump(efficiency=0.85),
    components=[Fermentation(efficiency=0.95)]
)

# Process material
result = facility.facility_process(
    input_volume_composition={"water": 0.7, "sugar": 0.3},
    input_volumetric_flow=0.001
)

print(f"Ethanol produced: {result['mass_flow']['amount']['ethanol']:.4f} kg/s")
print(f"Net energy: {result['net_power_gained']:.2f} J")
```

### Example 2: Complete Production Line

```python
from systems.facility import Facility
from systems.pump import Pump
from systems.processors import Fermentation, Filtration, Distillation, Dehydration
from systems.connectors import Pipe, Bend, Valve

# Build complete facility
pump = Pump(efficiency=0.85, opening_diameter=0.15)

components = [
    Fermentation(efficiency=0.95, power_consumption_rate=50, power_consumption_unit="kW"),
    Pipe(length=20, diameter=0.1),
    Filtration(efficiency=0.98, power_consumption_rate=20, power_consumption_unit="kW"),
    Bend(angle=90, diameter=0.1),
    Distillation(efficiency=0.92, power_consumption_rate=100, power_consumption_unit="kW"),
    Valve(diameter=0.1, resistance_coefficient=2.0),
    Dehydration(efficiency=0.99, power_consumption_rate=30, power_consumption_unit="kW"),
    Pipe(length=10, diameter=0.1)
]

facility = Facility(pump=pump, components=components)

# Process with detailed logging
result = facility.facility_process(
    input_volume_composition={"water": 0.625, "sugar": 0.3125, "fiber": 0.0625},
    input_volumetric_flow=0.002,  # 2 L/s
    interval=3600,  # 1 hour
    store_data=True
)

# Analyze results
print("=== Facility Performance ===")
print(f"Total Power: {result['total_power_consumed']/1000:.2f} kW")
print(f"Energy Generated: {result['power_generated']/1e6:.2f} MJ")
print(f"Net Energy: {result['net_power_gained']/1e6:.2f} MJ")
print(f"Ethanol Output: {result['mass_flow']['amount']['ethanol']*3600:.2f} kg/hr")
print(f"Purity: {result['mass_flow']['composition']['ethanol']:.2%}")
```

### Example 3: Economic Analysis

```python
# Calculate economics
energy_cost = 0.10  # $/kWh
ethanol_price = 2.50  # $/kg
operating_hours = 8000  # hours/year

# Process for 1 hour
result = facility.facility_process(
    input_volume_composition={"water": 0.625, "sugar": 0.3125, "fiber": 0.0625},
    input_volumetric_flow=0.002,
    interval=3600,
    store_data=False
)

# Annual calculations
annual_power_kwh = (result['total_power_consumed'] / 1000) * operating_hours
annual_power_cost = annual_power_kwh * energy_cost

annual_ethanol_kg = result['mass_flow']['amount']['ethanol'] * 3600 * operating_hours
annual_revenue = annual_ethanol_kg * ethanol_price

annual_profit = annual_revenue - annual_power_cost

print("=== Economic Analysis ===")
print(f"Annual Power Cost: ${annual_power_cost:,.2f}")
print(f"Annual Ethanol Production: {annual_ethanol_kg:,.0f} kg")
print(f"Annual Revenue: ${annual_revenue:,.2f}")
print(f"Annual Profit: ${annual_profit:,.2f}")
print(f"Energy ROI: {(annual_revenue/annual_power_cost - 1)*100:.1f}%")
```

### Example 4: Optimization Study

```python
import numpy as np

# Test different pump efficiencies
efficiencies = np.linspace(0.6, 0.95, 8)
results = []

components = [Fermentation(efficiency=0.95), Distillation(efficiency=0.92)]

for eff in efficiencies:
    facility = Facility(
        pump=Pump(efficiency=eff),
        components=components
    )
    
    result = facility.facility_process(
        input_volume_composition={"water": 0.7, "sugar": 0.3},
        input_volumetric_flow=0.001,
        interval=3600
    )
    
    results.append({
        'efficiency': eff,
        'power_consumed': result['total_power_consumed'],
        'net_gain': result['net_power_gained'],
        'ethanol_output': result['mass_flow']['amount']['ethanol']
    })

# Find optimal efficiency
best = max(results, key=lambda x: x['net_gain'])
print(f"Optimal pump efficiency: {best['efficiency']:.2%}")
print(f"Net energy gain: {best['net_gain']/1e6:.2f} MJ")
```

### Example 5: Batch Processing

```python
# Process multiple batches
batch_compositions = [
    {"water": 0.6, "sugar": 0.35, "fiber": 0.05},
    {"water": 0.65, "sugar": 0.30, "fiber": 0.05},
    {"water": 0.7, "sugar": 0.25, "fiber": 0.05}
]

batch_results = []

for i, composition in enumerate(batch_compositions):
    result = facility.facility_process(
        input_volume_composition=composition,
        input_volumetric_flow=0.001,
        interval=3600
    )
    
    batch_results.append(result)
    
    print(f"Batch {i+1}:")
    print(f"  Ethanol: {result['mass_flow']['amount']['ethanol']*3600:.2f} kg")
    print(f"  Net energy: {result['net_power_gained']/1e6:.2f} MJ")

# Aggregate statistics
total_ethanol = sum(r['mass_flow']['amount']['ethanol'] for r in batch_results) * 3600
avg_power = np.mean([r['total_power_consumed'] for r in batch_results])

print(f"\nTotal ethanol (3 batches): {total_ethanol:.2f} kg")
print(f"Average power: {avg_power/1000:.2f} kW")
```

## Best Practices

### Component Ordering

**Recommended sequence:**
1. Pump (always first)
2. Fermentation
3. Pipe/connectors
4. Filtration
5. Pipe/connectors
6. Distillation
7. Pipe/connectors
8. Dehydration
9. Final pipes

### Power Optimization

```python
# Compare configurations
configs = [
    {"name": "Base", "pump_eff": 0.75, "ferm_eff": 0.90},
    {"name": "Mid", "pump_eff": 0.85, "ferm_eff": 0.95},
    {"name": "High", "pump_eff": 0.95, "ferm_eff": 0.98}
]

for config in configs:
    facility = Facility(
        pump=Pump(efficiency=config["pump_eff"]),
        components=[Fermentation(efficiency=config["ferm_eff"])]
    )
    
    result = facility.facility_process(
        input_volume_composition={"water": 0.7, "sugar": 0.3},
        input_volumetric_flow=0.001
    )
    
    print(f"{config['name']}: Net = {result['net_power_gained']:.2f} J")
```

### Data Logging

```python
# Enable comprehensive logging
result = facility.facility_process(
    input_volume_composition=composition,
    input_volumetric_flow=flow,
    interval=interval,
    store_data=True  # Enable logging
)

# Access component logs
for component in facility.components:
    if isinstance(component, Process):
        print(f"{component.name} inputs:", component.inputs_log)
        print(f"{component.name} outputs:", component.outputs_log)
        print(f"{component.name} power:", component.consumption_log)
```

### Error Handling

```python
try:
    result = facility.facility_process(
        input_volume_composition=composition,
        input_volumetric_flow=flow
    )
    
    if result['net_power_gained'] < 0:
        print("Warning: Negative net energy gain!")
    
    if result['mass_flow']['composition']['ethanol'] < 0.9:
        print("Warning: Low ethanol purity!")
        
except Exception as e:
    print(f"Processing error: {e}")
```

## Troubleshooting

### Common Issues

**1. Unexpected zero outputs**
- Check all components are initialized correctly
- Verify input composition sums to reasonable value
- Ensure flow rate is not zero

**2. Negative net energy**
- Review pump and process efficiencies
- Check power consumption rates are realistic
- Verify interval parameter is correct

**3. Component order errors**
- Ensure pump is first (or use default)
- Check connector placement between processes
- Verify flow compatibility between components

## See Also

- [Pump System](pump-system.md) - Pump integration details
- [Process Systems](process-systems.md) - Individual process documentation
- [Connector Systems](connector-systems.md) - Connector integration
- [Examples](examples.md) - More facility examples
- [API Reference](api-reference.md#facility-class) - Complete API
