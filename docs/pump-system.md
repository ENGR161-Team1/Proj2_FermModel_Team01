# Pump System Documentation

The Pump class models fluid pumping operations with efficiency-based energy calculations and realistic flow dynamics.

## Overview

The Pump class simulates the operation of a pump that increases fluid pressure and velocity. It calculates:
- Output flow rates based on pump efficiency
- Power consumption for pumping operations
- Energy balance considering fluid properties

## Table of Contents

- [Class Initialization](#class-initialization)
- [Methods](#methods)
- [Physical Principles](#physical-principles)
- [Usage Examples](#usage-examples)
- [Best Practices](#best-practices)

## Class Initialization

### `Pump(**kwargs)`

Creates a new Pump instance with configurable parameters.

**Parameters:**

| Parameter | Type | Default | Unit | Description |
|-----------|------|---------|------|-------------|
| `name` | str | "Pump" | - | Pump identifier |
| `performance_rating` | float | 0 | m | Pump head rating |
| `cost` | float | 0 | USD/(m³/s) | Cost per unit flow rate |
| `efficiency` | float | 1.0 | - | Pump efficiency (0-1) |
| `opening_diameter` | float | 0.1 | m | Inlet/outlet diameter |

**Example:**

```python
from systems.pump import Pump

# High-efficiency industrial pump
pump = Pump(
    name="Main Feed Pump",
    performance_rating=50,  # 50 m head
    efficiency=0.85,        # 85% efficient
    opening_diameter=0.15,  # 15 cm diameter
    cost=5000              # $5000 per m³/s
)
```

## Methods

### `pump_process(**kwargs)`

Processes fluid through the pump, calculating output flows and power consumption.

**Parameters:**

| Parameter | Type | Required | Unit | Description |
|-----------|------|----------|------|-------------|
| `input_volume_flow` | float | Yes | m³/s | Inlet volumetric flow rate |
| `input_composition` | dict | Yes | - | Component volume fractions |

**Input Composition Keys:**
- `"ethanol"` - Ethanol volume fraction (0-1)
- `"water"` - Water volume fraction (0-1)
- `"sugar"` - Sugar volume fraction (0-1)
- `"fiber"` - Fiber volume fraction (0-1)

**Returns:**

`tuple`: (output_mass_flow, output_volumetric_flow, power_consumed)
- `output_mass_flow` (float): Mass flow rate at outlet in kg/s
- `output_volumetric_flow` (float): Volumetric flow rate at outlet in m³/s
- `power_consumed` (float): Mechanical power consumed in Watts

**Example:**

```python
# Process flow through pump
mass_flow, vol_flow, power = pump.pump_process(
    input_volume_flow=0.001,  # 1 L/s
    input_composition={
        "water": 0.7,
        "ethanol": 0.2,
        "sugar": 0.1
    }
)

print(f"Output flow: {vol_flow*1000:.2f} L/s")
print(f"Power consumed: {power:.2f} W")
```

## Physical Principles

### Energy Balance

The pump process is based on energy balance principles:

1. **Input Kinetic Energy:**
   ```
   KE_in = ½ × mass_flow × velocity²
   velocity = volumetric_flow / cross_sectional_area
   ```

2. **Energy Added by Pump:**
   ```
   E_added = KE_in × efficiency
   ```

3. **Total Power Consumed:**
   ```
   P_consumed = KE_in + E_added
   ```

4. **Output Flow Calculation:**
   ```
   Q_out = (2 × E_added × A² / ρ)^(1/3)
   ```
   where A is cross-sectional area and ρ is fluid density

### Density Calculation

Fluid density is calculated as a weighted average of component densities:

```python
ρ_mixture = Σ(fraction_i × density_i)
```

Component densities:
- Water: 1000 kg/m³
- Ethanol: 789 kg/m³
- Sugar: 1590 kg/m³
- Fiber: 1500 kg/m³

### Efficiency Impact

Pump efficiency directly affects:
- Energy transfer to fluid
- Output flow rate
- Power consumption

Higher efficiency → More energy transferred → Higher output flow

## Usage Examples

### Example 1: Basic Pump Operation

```python
from systems.pump import Pump

# Create pump with 85% efficiency
pump = Pump(
    efficiency=0.85,
    opening_diameter=0.1
)

# Pump water
mass_flow, vol_flow, power = pump.pump_process(
    input_volume_flow=0.001,  # 1 L/s
    input_composition={"water": 1.0}
)

print(f"Input: 1.00 L/s")
print(f"Output: {vol_flow*1000:.2f} L/s")
print(f"Flow increase: {(vol_flow/0.001 - 1)*100:.1f}%")
print(f"Power: {power:.2f} W")
```

### Example 2: Comparing Pump Efficiencies

```python
efficiencies = [0.6, 0.7, 0.8, 0.9]
input_flow = 0.001  # 1 L/s
composition = {"water": 0.7, "ethanol": 0.3}

print("Efficiency Comparison:")
print("-" * 50)

for eff in efficiencies:
    pump = Pump(efficiency=eff)
    _, vol_flow, power = pump.pump_process(
        input_volume_flow=input_flow,
        input_composition=composition
    )
    
    print(f"η = {eff:.0%}: Output = {vol_flow*1000:.3f} L/s, "
          f"Power = {power:.1f} W")
```

### Example 3: Pump with Different Fluids

```python
from systems.pump import Pump

pump = Pump(efficiency=0.85, opening_diameter=0.12)

fluids = {
    "Pure Water": {"water": 1.0},
    "Pure Ethanol": {"ethanol": 1.0},
    "70/30 Mix": {"water": 0.7, "ethanol": 0.3},
    "Sugar Solution": {"water": 0.8, "sugar": 0.2}
}

print("Fluid Comparison (1 L/s input):")
print("-" * 60)

for name, composition in fluids.items():
    mass, vol, power = pump.pump_process(
        input_volume_flow=0.001,
        input_composition=composition
    )
    
    print(f"{name:15} | Output: {vol*1000:.3f} L/s | "
          f"Power: {power:.1f} W | Mass: {mass:.3f} kg/s")
```

### Example 4: Economic Analysis

```python
from systems.pump import Pump

# Pump specifications
pump = Pump(
    efficiency=0.85,
    cost=5000,  # $5000 per m³/s
    opening_diameter=0.15
)

# Operating conditions
input_flow = 0.002  # 2 L/s
composition = {"water": 0.625, "sugar": 0.3125, "fiber": 0.0625}
hours_per_day = 20
days_per_year = 350

# Calculate pump operation
_, vol_flow, power = pump.pump_process(
    input_volume_flow=input_flow,
    input_composition=composition
)

# Economic calculations
capital_cost = pump.cost * input_flow
annual_operating_hours = hours_per_day * days_per_year
annual_energy = power * annual_operating_hours / 1000  # kWh
energy_cost = 0.10  # $0.10 per kWh
annual_energy_cost = annual_energy * energy_cost

print("Economic Analysis:")
print(f"Capital Cost: ${capital_cost:,.2f}")
print(f"Annual Operating Hours: {annual_operating_hours:,} hours")
print(f"Annual Energy Consumption: {annual_energy:,.1f} kWh")
print(f"Annual Energy Cost: ${annual_energy_cost:,.2f}")
print(f"3-Year Total Cost: ${capital_cost + 3*annual_energy_cost:,.2f}")
```

## Best Practices

### Efficiency Selection

**Typical pump efficiencies:**
- Small pumps (< 10 HP): 60-70%
- Medium pumps (10-100 HP): 70-85%
- Large pumps (> 100 HP): 85-95%

**Choose efficiency based on:**
- Pump type and size
- Operating conditions
- Maintenance quality
- Age of equipment

### Diameter Sizing

**Guidelines:**
```python
# For flow rates (L/s) → diameter (m)
flow_lps = 1.0  # L/s
velocity_target = 2.0  # m/s (typical)

# Calculate required diameter
import math
flow_m3s = flow_lps / 1000
area = flow_m3s / velocity_target
diameter = math.sqrt(4 * area / math.pi)
```

**Typical velocities:**
- Suction lines: 1-2 m/s
- Discharge lines: 2-3 m/s
- High-pressure lines: 3-5 m/s

### Performance Monitoring

```python
# Track pump performance over time
pump_log = []

for hour in range(24):
    mass, vol, power = pump.pump_process(
        input_volume_flow=input_flow,
        input_composition=composition
    )
    
    pump_log.append({
        'hour': hour,
        'output_flow': vol,
        'power': power,
        'efficiency_actual': vol / input_flow - 1
    })

# Analyze performance
import numpy as np
avg_power = np.mean([log['power'] for log in pump_log])
max_power = np.max([log['power'] for log in pump_log])
```

### Integration with Facility

```python
from systems.facility import Facility
from systems.processors import Fermentation

# Create integrated system
pump = Pump(efficiency=0.85, opening_diameter=0.15)
fermenter = Fermentation(efficiency=0.95)

facility = Facility(
    pump=pump,
    components=[fermenter]
)

# Process through complete facility
result = facility.facility_process(
    input_volume_composition={"water": 0.7, "sugar": 0.3},
    input_volumetric_flow=0.001
)

print(f"Total power (including pump): {result['total_power_consumed']:.2f} W")
```

## Troubleshooting

### Common Issues

**1. Zero or very low output flow**
- Check input flow is not zero
- Verify composition fractions sum to reasonable value
- Ensure density calculation is not zero

**2. Unrealistic power consumption**
- Review efficiency setting (should be 0-1)
- Check input flow rate magnitude
- Verify diameter is appropriate for flow rate

**3. Mass flow doesn't match expectations**
- Check composition fractions are correct
- Verify density calculations
- Review unit conversions (m³/s vs L/s)

## See Also

- [Facility System](facility-system.md) - Integrating pumps with processes
- [Connector Systems](connector-systems.md) - Downstream flow components
- [Examples](examples.md) - More pump examples
- [API Reference](api-reference.md#pump-class) - Complete API documentation
