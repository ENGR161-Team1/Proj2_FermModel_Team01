# Connector Systems

**Version:** 0.6.1

This document provides detailed information about fluid transport connectors in the Ethanol Plant Model.

## 🆕 Enhanced Documentation (v0.6.1)

All connector classes now include:
- **Detailed physical principles** in docstrings explaining loss mechanisms
- **Mathematical formulas** documented with variable definitions
- **Step-by-step calculation explanations** in inline comments
- **Parameter documentation** with types, units, and physical meaning

## Overview

Connectors represent physical components that transport fluids between process units. They model realistic energy losses while conserving mass.

### Key Principles (Documented in Code)

1. **Mass Conservation** - Input mass flow = Output mass flow
2. **Energy Dissipation** - Kinetic energy lost to friction, turbulence, resistance
3. **Power Loss Mechanisms** - Documented for each connector type

---

## Base Connector Class

### Class: `Connector`

**Enhanced Documentation (v0.6.1):** Complete physics documentation in docstrings.

```python
from systems.connectors import Connector

# Base class with documented parameters
connector = Connector(
    power_consumed=power_function,  # callable: Function to calculate power loss (W)
    diameter=0.1,                   # float: Inner diameter in meters
    cost=100.0                      # float: Component cost in USD
)
```

### Core Methods (Enhanced Documentation)

#### `processDensity()`

**Documented Principle:** Calculate fluid density from flow rates.

```python
def processDensity(self, **kwargs):
    """
    Calculate fluid density from mass and volumetric flow rates.
    
    Uses the relationship: density = mass_flow / volumetric_flow
    
    Args:
        input_volumetric_flow (float, optional): Volumetric flow rate in m³/s. Default: 0
        input_mass_flow (float, optional): Mass flow rate in kg/s. Default: 0
    
    Returns:
        float: Fluid density in kg/m³. Returns 0 if volumetric flow is zero.
    """
```

**Physical Meaning (Documented):**
- Density relates mass to volume: ρ = m/V
- Units: kg/m³ = (kg/s) / (m³/s)
- Zero handling prevents division errors

#### `processPower()`

**Documented Principle:** Calculate output power after losses.

```python
def processPower(self, **kwargs):
    """
    Calculate output kinetic power after accounting for power losses.
    
    The output power is the input power minus the power consumed by the connector
    due to friction, resistance, or other loss mechanisms.
    
    Args:
        input_power (float, optional): Input kinetic power in Watts. Default: 0
    
    Returns:
        float: Output kinetic power in Watts after losses.
    """
```

**Energy Balance (Documented in Code):**
```python
# Energy conservation with losses:
# P_out = P_in - P_loss
# Where P_loss depends on connector type (friction, bend, valve)
```

#### `processFlow()`

**Documented Principle:** Calculate flow rate changes due to energy losses.

```python
def processFlow(self, **kwargs):
    """
    Calculate output volumetric flow rate after power losses in the connector.
    
    This method:
    1. Calculates flow velocity from volumetric flow and cross-sectional area
    2. Computes input kinetic power using velocity and mass flow
    3. Determines output power after losses using processPower()
    4. Calculates resulting output volumetric flow rate
    
    Args:
        input_volumetric_flow (float, optional): Input volumetric flow rate in m³/s. Default: 0
        input_mass_flow (float, optional): Input mass flow rate in kg/s. Default: 0
    
    Returns:
        float: Output volumetric flow rate in m³/s after accounting for power losses.
    """
```

**Step-by-Step Calculation (Documented in Code):**
```python
# Step 1: Calculate velocity
# Q = v × A, so v = Q / A
velocity = volumetric_flow / cross_sectional_area  # m/s

# Step 2: Calculate input kinetic power
# P = (1/2) × m_dot × v²
input_power = mass_flow * (velocity ** 2) / 2  # W

# Step 3: Apply power loss
output_power = self.processPower(input_power=input_power)  # W

# Step 4: Calculate output flow from output power
# Derived from kinetic power formula
output_flow = (2 * output_power * A² / ρ) ^ (1/3)  # m³/s
```

---

## Pipe Connector

### Class: `Pipe`

**Enhanced Documentation (v0.6.1):** Complete Darcy-Weisbach equation documentation.

```python
from systems.connectors import Pipe

# Initialize with documented parameters
pipe = Pipe(
    length=10.0,           # float: Pipe length in meters
    friction_factor=0.02,  # float: Darcy friction factor (dimensionless)
    diameter=0.1,          # float: Inner diameter in meters
    cost=500.0             # float: Pipe cost in USD
)
```

### Physical Principle: Darcy-Weisbach Equation (Fully Documented)

**Pressure Drop Formula:**
```
ΔP = f × (L/D) × (ρv²/2)
```

**Where (All Variables Documented in Code):**
- `ΔP` = Pressure drop (Pa)
- `f` = Darcy friction factor (dimensionless)
- `L` = Pipe length (m)
- `D` = Pipe diameter (m)
- `ρ` = Fluid density (kg/m³)
- `v` = Flow velocity (m/s)

**Power Loss Calculation (Documented):**
```
P_loss = ΔP × Q
```

Where:
- `P_loss` = Power consumed (W)
- `Q` = Volumetric flow rate (m³/s)

### Method: `pipePowerFunction()`

**Complete Documentation:**

```python
def pipePowerFunction(self, **kwargs):
    """
    Calculate power consumed due to friction in the pipe.
    
    Uses the Darcy-Weisbach equation for pressure drop:
    ΔP = f × (L/D) × (ρv²/2)
    Power loss = ΔP × Q
    
    Args:
        input_volumetric_flow (float, optional): Volumetric flow rate in m³/s. Default: 0
        input_mass_flow (float, optional): Mass flow rate in kg/s. Default: 0
    
    Returns:
        float: Power consumed due to frictional losses in Watts.
    """
```

**Inline Comments Explain:**
```python
# Darcy-Weisbach power loss formula
# Derived from: P = ΔP × Q where ΔP = f(L/D)(ρv²/2)
# Simplified to: P = m_dot × (8fLQ²)/(π²D⁵)
return mass_flow * (8 * f * L * Q**2) / (π**2 * D**5)  # Watts
```

### Friction Factor Guide (Documented)

**Typical Values (Commented in Code):**
- Smooth pipes (PVC, drawn tubing): `f ≈ 0.015 - 0.020`
- Commercial steel: `f ≈ 0.020 - 0.025`
- Rough pipes: `f ≈ 0.025 - 0.035`

---

## Bend Connector

### Class: `Bend`

**Enhanced Documentation (v0.6.1):** Secondary flow physics explained.

```python
from systems.connectors import Bend

# Initialize with documented parameters
bend = Bend(
    bend_radius=0.5,      # float: Radius of curvature in meters
    bend_factor=0.9,      # float: Efficiency factor (0-1), where 1.0 = no loss
    diameter=0.1,         # float: Inner diameter in meters
    cost=150.0            # float: Bend cost in USD
)
```

### Physical Principle: Secondary Flows (Fully Documented)

**Loss Mechanisms (Documented in Docstrings):**

1. **Secondary Flows:**
   - Fluid follows curved path
   - Centrifugal forces create transverse circulation
   - Dean vortices form (documented in code comments)

2. **Flow Separation:**
   - High-velocity fluid on outer wall
   - Low-velocity region on inner wall
   - Separation can occur at sharp bends

3. **Increased Turbulence:**
   - Velocity gradients enhanced
   - Energy dissipated to smaller eddies

**Power Loss Model (Documented):**
```
P_loss = (1 - efficiency) × (1/2) × m_dot × v²
```

Where:
- `efficiency` = `bend_factor` (0 to 1)
- `1 - efficiency` = fraction of kinetic energy lost

### Method: `bendPowerFunction()`

**Complete Documentation:**

```python
def bendPowerFunction(self, **kwargs):
    """
    Calculate power consumed in the bend due to flow direction change.
    
    Loss is proportional to the kinetic energy and the inefficiency of the bend.
    Power loss = (1 - efficiency) × (1/2) × m_dot × v²
    
    Args:
        input_volumetric_flow (float, optional): Volumetric flow rate in m³/s. Default: 0
        input_mass_flow (float, optional): Mass flow rate in kg/s. Default: 0
    
    Returns:
        float: Power consumed due to bend losses in Watts.
    """
```

**Inline Comments Explain:**
```python
# Calculate flow velocity
velocity = volumetric_flow / cross_sectional_area  # m/s

# Power loss based on kinetic energy and bend inefficiency
# Formula: P = (1 - η) × (1/2) × m_dot × v²
# Where η is the bend_factor (efficiency)
return mass_flow * (1 - self.bend_factor) * (velocity ** 2) / 2  # W
```

### Bend Factor Guide (Documented)

**Typical Values (Commented in Code):**
- Smooth, gradual bends (R/D > 5): `bend_factor ≈ 0.95 - 0.98`
- Standard 90° elbows (R/D ≈ 2): `bend_factor ≈ 0.85 - 0.90`
- Sharp bends (R/D < 1): `bend_factor ≈ 0.70 - 0.80`

Where `R/D` is radius-to-diameter ratio

---

## Valve Connector

### Class: `Valve`

**Enhanced Documentation (v0.6.1):** Resistance mechanism explained.

```python
from systems.connectors import Valve

# Initialize with documented parameters
valve = Valve(
    resistance_coefficient=1.0,  # float: Flow resistance K (dimensionless)
    diameter=0.1,                # float: Inner diameter in meters
    cost=200.0                   # float: Valve cost in USD
)
```

### Physical Principle: Flow Resistance (Fully Documented)

**Resistance Mechanism (Documented in Docstrings):**

Valves control flow by introducing resistance through:
1. **Partial obstruction** of flow path
2. **Flow contraction** through valve opening
3. **Expansion** after valve exit
4. **Turbulence generation** in wake regions

**Power Loss Model (Documented):**
```
P_loss = K × (1/2) × m_dot × v²
```

Where:
- `K` = `resistance_coefficient` (dimensionless)
- Higher `K` = more resistance = more power loss

### Method: `valvePowerFunction()`

**Complete Documentation:**

```python
def valvePowerFunction(self, **kwargs):
    """
    Calculate power consumed through the valve due to flow resistance.
    
    Loss is based on the kinetic energy and resistance coefficient:
    Power loss = K × (1/2) × m_dot × v²
    where K is the resistance coefficient.
    
    Args:
        input_volumetric_flow (float, optional): Volumetric flow rate in m³/s. Default: 0
        input_mass_flow (float, optional): Mass flow rate in kg/s. Default: 0
    
    Returns:
        float: Power consumed due to valve resistance in Watts.
    """
```

**Inline Comments Explain:**
```python
# Calculate flow velocity
velocity = volumetric_flow / cross_sectional_area  # m/s

# Power loss based on resistance coefficient and kinetic energy
# Formula: P = K × (1/2) × m_dot × v²
# Similar to pressure drop: ΔP = K × (1/2) × ρ × v²
return mass_flow * (velocity ** 2) * self.resistance_coefficient / 2  # W
```

### Resistance Coefficient Guide (Documented)

**Typical Values (Commented in Code):**
- Fully open gate valve: `K ≈ 0.15 - 0.20`
- Fully open globe valve: `K ≈ 5.0 - 10.0`
- Partially open valves: `K` increases significantly
- Flow control applications: Adjust `K` to achieve desired restriction

**Relationship to Valve Position:**
```python
# Documented in code comments:
# K increases as valve closes
# Typical relationship: K = K_min × (1 - position)^n
# Where position = 0 (closed) to 1 (open), n ≈ 2-4
```

---

## Combining Connectors (Enhanced Examples)

### Series Connection (Documented)

```python
# Series connection: output of one feeds input of next
# Total power loss = sum of individual losses (documented in code)

# Pipe power loss
pipe_loss = pipe.powerConsumed(
    input_volumetric_flow=Q1,
    input_mass_flow=m1
)  # W

# Pipe output flow
Q2 = pipe.processFlow(
    input_volumetric_flow=Q1,
    input_mass_flow=m1
)  # m³/s

# Mass conserved (documented principle)
m2 = m1  # kg/s

# Bend power loss
bend_loss = bend.powerConsumed(
    input_volumetric_flow=Q2,
    input_mass_flow=m2
)  # W

# Bend output flow
Q3 = bend.processFlow(
    input_volumetric_flow=Q2,
    input_mass_flow=m2
)  # m³/s

# Total power loss (documented calculation)
total_loss = pipe_loss + bend_loss  # W
```

---

## Engineering Applications (Enhanced Documentation)

### Pressure Drop Calculations (Documented)

```python
# Calculate pressure drop from power loss (documented relationship)
# ΔP = P_loss / Q
# Units: Pa = W / (m³/s)

power_loss = pipe.powerConsumed(
    input_volumetric_flow=flow_rate,
    input_mass_flow=mass_rate
)  # W

pressure_drop = power_loss / flow_rate  # Pa

# Convert to other units (documented conversions)
pressure_drop_psi = pressure_drop * 0.000145038  # psi = Pa × 0.000145038
pressure_drop_bar = pressure_drop * 1e-5  # bar = Pa × 10^-5
```

### Reynolds Number Estimation (Documented)

```python
# Reynolds number determines flow regime (documented in comments)
# Re = ρvD/μ = 4m_dot/(πDμ)

# For water at 20°C
density = 997  # kg/m³ (documented value)
viscosity = 0.001  # Pa·s = kg/(m·s) (documented value)
diameter = 0.1  # m

# Calculate Reynolds number (formula documented)
Re = (4 * mass_flow) / (π * diameter * viscosity)

# Flow regime classification (documented thresholds)
if Re < 2300:
    regime = "Laminar"  # Smooth, layered flow
elif Re < 4000:
    regime = "Transitional"  # Mixed behavior
else:
    regime = "Turbulent"  # Chaotic, well-mixed flow
```

---

## Best Practices (Enhanced for v0.6.1)

### Understanding Physical Principles

1. **Read docstrings for physics:**
   ```python
   help(Pipe.pipePowerFunction)
   # Shows complete Darcy-Weisbach documentation
   ```

2. **Check inline comments for formulas:**
   - Source code includes step-by-step derivations
   - Variable meanings documented
   - Unit conversions explained

3. **Verify parameter units:**
   - All parameters documented with SI units
   - Conversion factors provided where needed

### Debugging Flow Calculations

With enhanced documentation:

```python
# Enable detailed inspection (documented approach)
input_Q = 0.01  # m³/s (documented)
input_m = 10.0  # kg/s (documented)

# Step 1: Check input power (documented calculation)
velocity = input_Q / pipe.cross_sectional_area
input_power = input_m * (velocity ** 2) / 2
print(f"Input power: {input_power} W")  # Documented unit

# Step 2: Check power loss (documented mechanism)
loss = pipe.powerConsumed(
    input_volumetric_flow=input_Q,
    input_mass_flow=input_m
)
print(f"Power loss: {loss} W")  # Darcy-Weisbach loss

# Step 3: Check output power (documented calculation)
output_power = input_power - loss
print(f"Output power: {output_power} W")

# Step 4: Calculate output flow (documented formula)
output_Q = pipe.processFlow(
    input_volumetric_flow=input_Q,
    input_mass_flow=input_m
)
print(f"Output flow: {output_Q} m³/s")
```

---

## Related Documentation

- **[Process Systems](process-systems.md)** - Process unit documentation (also enhanced in v0.6.1)
- **[API Reference](api-reference.md)** - Complete API with enhanced docstrings
- **[Examples](examples.md)** - Practical examples with improved explanations

---

*For complete API details with comprehensive docstrings and physics documentation, see [API Reference](api-reference.md)*

*Last updated: Version 0.6.1 - November 2025*
