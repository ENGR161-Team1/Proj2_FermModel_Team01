# Connector Systems

Documentation for fluid transport connectors that simulate energy losses between process stages.

## Overview

Connectors model the physical transport of fluids through:
- **Pipes** - Straight segments with friction losses
- **Bends** - Elbows with direction change losses  
- **Valves** - Flow control with resistance losses

All connectors:
- Conserve mass (no material loss)
- Calculate energy dissipation
- Use density-based flow calculations

---

## Connector (Base Class)

### Description

Base class providing common functionality for all connector types.

### Constructor

```python
Connector(diameter=0.1, mass_function=None, energy_function=None)
```

**Parameters:**
- `diameter` (float): Inner diameter in meters (default: 0.1m)
- `mass_function` (callable): Function to calculate mass flow
- `energy_function` (callable): Function to calculate energy changes

### Attributes

- `diameter` - Inner diameter (m)
- `cross_sectional_area` - Flow area (m²)

### Methods

#### `processDensity(inputs)`

Calculate fluid density from mass and volumetric flow rates.

**Parameters:**
- `inputs` (dict):
  - `input_flow` - Volumetric flow rate (m³/s)
  - `input_mass` - Mass flow rate (kg/s)

**Returns:** float - Density (kg/m³)

**Example:**
```python
density = connector.processDensity({
    "input_flow": 0.1,   # m³/s
    "input_mass": 78.9   # kg/s
})
# Returns: 789 kg/m³ (ethanol)
```

---

## Pipe

### Description

Models straight pipe segments with frictional energy losses calculated using the Darcy-Weisbach equation.

### Constructor

```python
Pipe(length=1.0, diameter=0.1, friction_factor=0.02)
```

**Parameters:**
- `length` (float): Pipe length in meters
- `diameter` (float): Inner diameter in meters
- `friction_factor` (float): Darcy friction factor (dimensionless)

### Typical Friction Factors

| Pipe Material | Friction Factor |
|--------------|-----------------|
| Smooth pipes (PVC, drawn tubing) | 0.01 - 0.015 |
| Commercial steel | 0.015 - 0.02 |
| Cast iron | 0.02 - 0.03 |
| Rough pipes (old, corroded) | 0.03 - 0.05 |

### Methods

#### `pipeEnergyFunction(**kwargs)`

Calculate energy loss due to friction.

**Formula:**
```
ΔE = ρ × (8 × f × L × Q²) / (π² × d⁵)
```

Where:
- ρ = fluid density (kg/m³)
- f = friction factor
- L = pipe length (m)
- Q = volumetric flow rate (m³/s)
- d = diameter (m)

**Parameters:**
- `input_flow` (float): Volumetric flow rate (m³/s)
- `input_mass` (float): Mass flow rate (kg/s)
- `input_energy` (float): Input energy (J)

**Returns:** float - Output energy after losses (J)

**Example:**
```python
pipe = Pipe(length=10.0, diameter=0.15, friction_factor=0.02)

output_energy = pipe.pipeEnergyFunction(
    input_flow=0.1,      # m³/s
    input_mass=78.9,     # kg/s
    input_energy=1000    # J
)
print(f"Energy loss: {1000 - output_energy:.2f} J")
```

#### `pipeMassFunction(**kwargs)`

Calculate mass flow through pipe (conserved).

**Parameters:**
- `input_mass` (float): Input mass flow rate (kg/s)

**Returns:** float - Output mass flow rate (kg/s, equal to input)

---

## Bend

### Description

Models pipe bends/elbows with energy losses due to flow direction changes.

### Constructor

```python
Bend(bend_radius=0.5, bend_factor=0.9, diameter=0.1)
```

**Parameters:**
- `bend_radius` (float): Radius of curvature in meters
- `bend_factor` (float): Efficiency factor (1.0 = no loss, 0.0 = complete loss)
- `diameter` (float): Inner diameter in meters

### Typical Bend Factors

| Bend Type | Bend Factor |
|-----------|-------------|
| Long radius bend (R > 2d) | 0.95 - 0.98 |
| Standard elbow (R ≈ d) | 0.85 - 0.92 |
| Sharp elbow (R < d) | 0.70 - 0.85 |
| 90° miter bend | 0.60 - 0.75 |

### Methods

#### `bendEnergyFunction(**kwargs)`

Calculate energy loss in bend.

**Formula:**
```
ΔE = ρ × (1 - bend_factor) × v² / 2
```

Where:
- ρ = fluid density (kg/m³)
- v = flow velocity (m/s)
- bend_factor = efficiency (dimensionless)

**Parameters:**
- `input_flow` (float): Volumetric flow rate (m³/s)
- `input_mass` (float): Mass flow rate (kg/s)
- `input_energy` (float): Input energy (J)

**Returns:** float - Output energy after losses (J)

**Example:**
```python
bend = Bend(bend_radius=0.5, bend_factor=0.9, diameter=0.15)

output_energy = bend.bendEnergyFunction(
    input_flow=0.1,
    input_mass=78.9,
    input_energy=1000
)
```

#### `bendMassFunction(**kwargs)`

Calculate mass flow through bend (conserved).

**Parameters:**
- `input_mass` (float): Input mass flow rate (kg/s)

**Returns:** float - Output mass flow rate (kg/s, equal to input)

---

## Valve

### Description

Models flow control valves with adjustable resistance.

### Constructor

```python
Valve(resistance_coefficient=1.0, diameter=0.1)
```

**Parameters:**
- `resistance_coefficient` (float): Flow resistance coefficient (dimensionless)
- `diameter` (float): Inner diameter in meters

### Typical Resistance Coefficients

| Valve Position | Resistance Coefficient |
|----------------|------------------------|
| Fully open | 0.1 - 0.5 |
| 75% open | 1.0 - 2.0 |
| 50% open | 4.0 - 8.0 |
| 25% open | 20 - 50 |
| Nearly closed | 100+ |

### Methods

#### `valveEnergyFunction(**kwargs)`

Calculate energy loss through valve.

**Formula:**
```
ΔE = ρ × v² × K / 2
```

Where:
- ρ = fluid density (kg/m³)
- v = flow velocity (m/s)
- K = resistance coefficient

**Parameters:**
- `input_flow` (float): Volumetric flow rate (m³/s)
- `input_mass` (float): Mass flow rate (kg/s)
- `input_energy` (float): Input energy (J)

**Returns:** float - Output energy after losses (J)

**Example:**
```python
valve = Valve(resistance_coefficient=1.5, diameter=0.15)

output_energy = valve.valveEnergyFunction(
    input_flow=0.1,
    input_mass=78.9,
    input_energy=1000
)
```

#### `valveMassFunction(**kwargs)`

Calculate mass flow through valve (conserved).

**Parameters:**
- `input_mass` (float): Input mass flow rate (kg/s)

**Returns:** float - Output mass flow rate (kg/s, equal to input)

---

## Complete Transport Example

### Pipeline with Multiple Connectors

```python
from systems.connectors import Pipe, Bend, Valve

# Define transport components
pipe1 = Pipe(length=5.0, diameter=0.1, friction_factor=0.02)
bend1 = Bend(bend_radius=0.3, bend_factor=0.9, diameter=0.1)
valve1 = Valve(resistance_coefficient=0.5, diameter=0.1)
pipe2 = Pipe(length=3.0, diameter=0.1, friction_factor=0.02)

# Initial conditions
initial_energy = 10000  # J
flow_rate = 0.05        # m³/s
mass_rate = 39.45       # kg/s (ethanol)

# Transport through pipeline
energy1 = pipe1.pipeEnergyFunction(
    input_flow=flow_rate,
    input_mass=mass_rate,
    input_energy=initial_energy
)

energy2 = bend1.bendEnergyFunction(
    input_flow=flow_rate,
    input_mass=mass_rate,
    input_energy=energy1
)

energy3 = valve1.valveEnergyFunction(
    input_flow=flow_rate,
    input_mass=mass_rate,
    input_energy=energy2
)

final_energy = pipe2.pipeEnergyFunction(
    input_flow=flow_rate,
    input_mass=mass_rate,
    input_energy=energy3
)

# Mass is conserved throughout
final_mass = mass_rate

print(f"Initial energy: {initial_energy} J")
print(f"Final energy: {final_energy:.2f} J")
print(f"Total loss: {initial_energy - final_energy:.2f} J")
print(f"Efficiency: {(final_energy/initial_energy)*100:.1f}%")
```

### Integration with Process Systems

```python
from systems.processes import Fermentation, Filtration
from systems.connectors import Pipe

# Process systems
fermenter = Fermentation(efficiency=0.95)
filter_sys = Filtration(efficiency=0.90)

# Transport connector
transport_pipe = Pipe(length=10.0, diameter=0.15, friction_factor=0.02)

# Process through fermentation
result1 = fermenter.processMass(
    inputs={"ethanol": 0, "water": 1000, "sugar": 500, "fiber": 50},
    input_type="amount",
    output_type="amount"
)

# Transport energy calculation (mass is conserved)
total_mass = sum(result1.values())
output_mass = transport_pipe.pipeMassFunction(input_mass=total_mass)
# Note: In practice, you'd also track energy through the system

# Process through filtration
result2 = filter_sys.processMass(
    inputs=result1,  # Mass is conserved
    input_type="amount",
    output_type="full"
)
```

---

**Navigation:** [Home](index.md) | [Getting Started](getting-started.md) | [API Reference](api-reference.md) | [Process Systems](process-systems.md) | [Connector Systems](connector-systems.md) | [Examples](examples.md)
