# Connector Systems

Comprehensive guide to fluid transport components in the Ethanol Plant Model (v0.4.0).

## Overview

Connectors model the physical components that transport fluids between process systems. They calculate energy losses due to friction, direction changes, and flow resistance.

### Key Features (v0.4.0)

- **Kwargs-based API**: All methods use `**kwargs` for flexibility
- **Energy conservation**: Mass is conserved, energy is dissipated
- **Realistic physics**: Based on fluid dynamics equations
- **Flexible parameters**: Configurable dimensions and properties

### Available Connectors

1. **Pipe** - Straight segments with friction losses
2. **Bend** - Elbows with direction change losses
3. **Valve** - Flow control with adjustable resistance

---

## Base Connector Class

The `Connector` class provides the foundation for all fluid transport components.

### Methods

#### `__init__(**kwargs)`
Initialize a connector with energy function and diameter.

**Parameters:**
- `energy_consumed`: Function to calculate energy consumed by connector
- `diameter`: Inner diameter of the connector in meters (default: 0.1m)

#### `processDensity(**kwargs)`
Calculate fluid density based on mass and volumetric flow rates.

**Parameters:**
- `input_flow`: Volumetric flow rate in m³/s
- `input_mass`: Mass flow rate in kg/s

**Returns:** Density in kg/m³, or 0 if volumetric flow is zero

#### `processEnergy(**kwargs)`
Calculate output kinetic energy after energy losses.

**Parameters:**
- `input_energy`: Input kinetic energy in Joules

**Returns:** Output kinetic energy in Joules after subtracting energy losses

**Note:** This method calls the connector's `energyConsumed` function to determine losses.

#### `processFlow(**kwargs)`
Calculate output volumetric flow rate after energy losses.

**Parameters:**
- `input_flow`: Input volumetric flow rate in m³/s
- `input_mass`: Mass flow rate in kg/s
- `interval`: Time interval in seconds (default: 1s)

**Returns:** Output volumetric flow rate in m³/s

**Process:**
1. Calculates flow velocity from input flow and cross-sectional area
2. Computes input kinetic energy over the time interval
3. Uses `processEnergy` to determine output energy after losses
4. Calculates output flow rate using inverse kinetic energy formula with cube root

### Energy Balance

The connector calculates energy dissipation:

```python
# Input kinetic energy
velocity = flow / cross_sectional_area
input_energy = interval * mass * (velocity² / 2)

# Energy loss (calculated by specific connector)
energy_loss = energyConsumed(input_flow, input_mass)

# Output energy and flow
output_energy = input_energy - energy_loss
output_flow = ((output_energy * area) / (density * interval)) ^ (1/3)
```

---

## Pipe

Models straight pipe segments using the Darcy-Weisbach equation for friction losses.

### Physics

**Darcy-Weisbach Equation:**
```
ΔP = f * (L/D) * (ρv²/2)
Energy loss = mass * (8fLQ²) / (π²D⁵)
```

Where:
- `f` = Darcy friction factor
- `L` = pipe length
- `D` = pipe diameter
- `Q` = volumetric flow rate
- `ρ` = fluid density

### Initialization

```python
from systems.connectors import Pipe

pipe = Pipe(
    length=10.0,           # meters
    diameter=0.15,         # meters
    friction_factor=0.02   # dimensionless
)
```

### Parameters

- `length` (float): Pipe length in meters (default: 1.0)
- `diameter` (float): Inner diameter in meters (default: 0.1)
- `friction_factor` (float): Darcy friction factor (default: 0.02)

### Examples

#### Basic Usage
```python
pipe = Pipe(length=10, diameter=0.1, friction_factor=0.02)

output_flow = pipe.processFlow(
    input_flow=0.05,   # 0.05 m³/s input
    input_mass=50,     # 50 kg/s
    interval=1
)

print(f"Input flow: 0.05 m³/s")
print(f"Output flow: {output_flow:.4f} m³/s")
print(f"Flow reduction: {(0.05 - output_flow) / 0.05:.1%}")
```

#### Comparing Pipe Lengths
```python
for length in [1, 5, 10, 20]:
    pipe = Pipe(length=length, diameter=0.1, friction_factor=0.02)
    output = pipe.processFlow(
        input_flow=0.05,
        input_mass=50,
        interval=1
    )
    loss = (0.05 - output) / 0.05
    print(f"Length {length}m: {loss:.1%} flow loss")
```

#### Diameter Effect
```python
input_flow = 0.05
input_mass = 50

for diameter in [0.05, 0.10, 0.15, 0.20]:
    pipe = Pipe(length=10, diameter=diameter, friction_factor=0.02)
    output = pipe.processFlow(
        input_flow=input_flow,
        input_mass=input_mass,
        interval=1
    )
    loss = (input_flow - output) / input_flow
    print(f"Diameter {diameter}m: {loss:.1%} flow loss")
```

### Friction Factor Selection

| Surface Type | Friction Factor (f) | Notes |
|-------------|---------------------|--------|
| Smooth (drawn tubing) | 0.01-0.015 | PVC, glass |
| Commercial steel | 0.02-0.025 | New pipes |
| Galvanized iron | 0.02-0.03 | Standard industrial |
| Cast iron | 0.025-0.035 | Older pipes |
| Rough/corroded | 0.04-0.10 | Poor condition |

---

## Bend

Models pipe bends or elbows where flow direction changes, causing energy loss.

### Physics

Energy is lost due to:
- Flow separation
- Secondary flows
- Direction change

```
Energy loss = mass * (1 - bend_factor) * (v²/2)
```

Where:
- `bend_factor` = efficiency (1.0 = no loss, lower = more loss)
- `v` = flow velocity

### Initialization

```python
from systems.connectors import Bend

bend = Bend(
    bend_radius=0.5,    # meters
    bend_factor=0.9,    # efficiency (0-1)
    diameter=0.1        # meters
)
```

### Parameters

- `bend_radius` (float): Radius of curvature in meters (default: 0.5)
- `bend_factor` (float): Efficiency factor, 1.0 = no loss (default: 0.9)
- `diameter` (float): Inner diameter in meters (default: 0.1)

### Examples

#### Basic Usage
```python
bend = Bend(bend_radius=0.5, bend_factor=0.9, diameter=0.1)

output_flow = bend.processFlow(
    input_flow=0.05,
    input_mass=50,
    interval=1
)

print(f"Input flow: 0.05 m³/s")
print(f"Output flow: {output_flow:.4f} m³/s")
```

#### Bend Sharpness Effect
```python
input_flow = 0.05
input_mass = 50

# Sharp bend (low efficiency)
sharp_bend = Bend(bend_radius=0.2, bend_factor=0.70, diameter=0.1)
output_sharp = sharp_bend.processFlow(
    input_flow=input_flow, input_mass=input_mass, interval=1
)

# Gentle bend (high efficiency)
gentle_bend = Bend(bend_radius=1.0, bend_factor=0.95, diameter=0.1)
output_gentle = gentle_bend.processFlow(
    input_flow=input_flow, input_mass=input_mass, interval=1
)

print(f"Sharp bend loss: {(input_flow - output_sharp) / input_flow:.1%}")
print(f"Gentle bend loss: {(input_flow - output_gentle) / input_flow:.1%}")
```

#### Multiple Bends
```python
# Pipeline with 4 bends
input_flow = 0.05
input_mass = 50

current_flow = input_flow
current_mass = input_mass

for i in range(4):
    bend = Bend(bend_radius=0.5, bend_factor=0.9, diameter=0.1)
    current_flow = bend.processFlow(
        input_flow=current_flow,
        input_mass=current_mass,
        interval=1
    )
    # Mass is conserved
    print(f"After bend {i+1}: flow = {current_flow:.4f} m³/s")

total_loss = (input_flow - current_flow) / input_flow
print(f"\nTotal loss through 4 bends: {total_loss:.1%}")
```

### Bend Factor Guidelines

| Bend Type | Radius/Diameter | Bend Factor | Typical Loss |
|-----------|-----------------|-------------|--------------|
| Very sharp (90°) | R/D < 1 | 0.60-0.70 | 30-40% |
| Sharp (90°) | R/D = 1-2 | 0.75-0.85 | 15-25% |
| Standard (90°) | R/D = 3-5 | 0.85-0.90 | 10-15% |
| Gentle (90°) | R/D > 5 | 0.90-0.95 | 5-10% |
| Swept (45°) | Any | 0.95-0.98 | 2-5% |

---

## Valve

Models flow control valves with adjustable resistance.

### Physics

Energy loss proportional to dynamic pressure:

```
Energy loss = mass * (v²/2) * resistance_coefficient
```

Where:
- `resistance_coefficient` = valve-specific loss coefficient

### Initialization

```python
from systems.connectors import Valve

valve = Valve(
    resistance_coefficient=1.0,  # dimensionless
    diameter=0.1                 # meters
)
```

### Parameters

- `resistance_coefficient` (float): Flow resistance (default: 1.0)
- `diameter` (float): Inner diameter in meters (default: 0.1)

### Examples

#### Basic Usage
```python
valve = Valve(resistance_coefficient=1.5, diameter=0.1)

output_flow = valve.processFlow(
    input_flow=0.05,
    input_mass=50,
    interval=1
)

print(f"Flow reduction: {(0.05 - output_flow) / 0.05:.1%}")
```

#### Valve Opening Simulation
```python
# Simulate different valve positions
input_flow = 0.05
input_mass = 50

positions = {
    "Fully open": 0.5,
    "75% open": 1.0,
    "50% open": 2.5,
    "25% open": 8.0,
    "Nearly closed": 20.0
}

for position, resistance in positions.items():
    valve = Valve(resistance_coefficient=resistance, diameter=0.1)
    output = valve.processFlow(
        input_flow=input_flow,
        input_mass=input_mass,
        interval=1
    )
    reduction = (input_flow - output) / input_flow
    print(f"{position:15s}: {reduction:5.1%} flow reduction")
```

#### Flow Control System
```python
import numpy as np

def adjust_valve_to_target_flow(target_flow, input_flow, input_mass):
    """Find valve resistance to achieve target flow"""
    for resistance in np.linspace(0.1, 10, 100):
        valve = Valve(resistance_coefficient=resistance, diameter=0.1)
        output = valve.processFlow(
            input_flow=input_flow,
            input_mass=input_mass,
            interval=1
        )
        if abs(output - target_flow) < 0.001:
            return resistance, output
    return None, None

target = 0.03  # Want 0.03 m³/s output
resistance, actual = adjust_valve_to_target_flow(
    target, 
    input_flow=0.05, 
    input_mass=50
)

print(f"Target flow: {target} m³/s")
print(f"Required resistance: {resistance:.2f}")
print(f"Actual output: {actual:.4f} m³/s")
```

### Resistance Coefficient Guidelines

| Valve Type | Position | Resistance Coefficient |
|-----------|----------|----------------------|
| Gate valve | Fully open | 0.1-0.2 |
| Gate valve | 75% open | 0.5-1.0 |
| Gate valve | 50% open | 2.0-4.0 |
| Globe valve | Fully open | 4.0-10.0 |
| Ball valve | Fully open | 0.05-0.1 |
| Butterfly valve | Fully open | 0.2-0.5 |
| Check valve | Open | 2.0-4.0 |

---

## Combined Systems

### Complete Pipeline Example

```python
from systems.connectors import Pipe, Bend, Valve

# Define pipeline components
components = [
    Pipe(length=5, diameter=0.1, friction_factor=0.02),
    Bend(bend_radius=0.5, bend_factor=0.9, diameter=0.1),
    Pipe(length=10, diameter=0.1, friction_factor=0.02),
    Bend(bend_radius=0.5, bend_factor=0.9, diameter=0.1),
    Valve(resistance_coefficient=1.5, diameter=0.1),
    Pipe(length=5, diameter=0.1, friction_factor=0.02)
]

# Initial conditions
current_flow = 0.1  # m³/s
current_mass = 100  # kg/s

print("=== Pipeline Flow Analysis ===\n")
print(f"Initial flow: {current_flow:.4f} m³/s")

# Process through each component
for i, component in enumerate(components):
    component_type = type(component).__name__
    
    output_flow = component.processFlow(
        input_flow=current_flow,
        input_mass=current_mass,
        interval=1
    )
    
    loss = (current_flow - output_flow) / current_flow
    print(f"{i+1}. {component_type:10s}: "
          f"flow = {output_flow:.4f} m³/s, "
          f"loss = {loss:.2%}")
    
    current_flow = output_flow

total_loss = (0.1 - current_flow) / 0.1
print(f"\nTotal pipeline loss: {total_loss:.1%}")
print(f"Final flow: {current_flow:.4f} m³/s")
```

### Optimization Example

```python
import numpy as np

def optimize_pipeline(target_flow, initial_flow, initial_mass):
    """Find optimal pipe diameter to achieve target flow"""
    best_diameter = None
    best_output = None
    
    for diameter in np.linspace(0.05, 0.3, 50):
        # Test pipeline with this diameter
        pipeline = [
            Pipe(length=20, diameter=diameter, friction_factor=0.02),
            Bend(bend_radius=diameter*5, bend_factor=0.9, diameter=diameter),
            Pipe(length=10, diameter=diameter, friction_factor=0.02)
        ]
        
        current_flow = initial_flow
        current_mass = initial_mass
        
        for component in pipeline:
            current_flow = component.processFlow(
                input_flow=current_flow,
                input_mass=current_mass,
                interval=1
            )
        
        if best_output is None or abs(current_flow - target_flow) < abs(best_output - target_flow):
            best_diameter = diameter
            best_output = current_flow
    
    return best_diameter, best_output

optimal_d, output = optimize_pipeline(
    target_flow=0.08,
    initial_flow=0.1,
    initial_mass=100
)

print(f"Optimal diameter: {optimal_d:.3f} m")
print(f"Achieved flow: {output:.4f} m³/s")
```

---

## Integration with Process Systems

### Connecting Processes with Pipes

```python
from systems.processes import Fermentation, Filtration
from systems.connectors import Pipe

# Create process systems
fermenter = Fermentation(efficiency=0.95)
filter_sys = Filtration(efficiency=0.98)

# Create transport pipe
transfer_pipe = Pipe(length=15, diameter=0.2, friction_factor=0.02)

# Initial inputs
inputs = {"ethanol": 0, "water": 100, "sugar": 50, "fiber": 10}

# Process through fermenter
fermentation_output = fermenter.processMass(
    inputs=inputs,
    input_type="amount",
    output_type="full"
)

print("After fermentation:")
print(f"  Ethanol: {fermentation_output['amount']['ethanol']:.2f} kg")

# Convert to flow rate (assume 1 hour transfer time = 3600s)
transfer_time = 3600  # seconds
flow_inputs = {
    comp: fermentation_output['amount'][comp] / transfer_time 
    for comp in fermenter.components
}

# Calculate mass flow rate
total_mass_flow = sum(fermentation_output['amount'].values()) / transfer_time

# Transport through pipe
output_flow = transfer_pipe.processFlow(
    input_flow=sum(flow_inputs.values()),
    input_mass=total_mass_flow,
    interval=1
)

# Scale back to total amounts after transfer
flow_ratio = output_flow / sum(flow_inputs.values())
filtration_inputs = {
    comp: fermentation_output['amount'][comp] * flow_ratio
    for comp in fermenter.components
}

# Process through filtration
final_output = filter_sys.processMass(
    inputs=filtration_inputs,
    input_type="amount",
    output_type="full"
)

print("\nAfter transport and filtration:")
print(f"  Ethanol: {final_output['amount']['ethanol']:.2f} kg")
print(f"  Transport losses: {(1 - flow_ratio) * 100:.1f}%")
```

---

## Best Practices

1. **Mass Conservation**: Mass flow rate remains constant through connectors
2. **Sequential Processing**: Chain connectors by using output of one as input to next
3. **Realistic Parameters**: Use typical values for friction factors and resistances
4. **Energy Losses**: Remember that flow rate decreases due to energy dissipation
5. **Diameter Selection**: Larger diameters = less friction but higher material cost
6. **Interval Consistency**: Use consistent time intervals when chaining connectors
7. **Zero Flow Handling**: Methods return 0 when input flow or mass is zero

---

## Common Applications

### Pressure Drop Calculation

```python
def calculate_pressure_drop(components, flow_rate, density=1000):
    """Calculate total pressure drop through system"""
    total_energy_loss = 0
    current_flow = flow_rate
    mass_flow = flow_rate * density
    
    for component in components:
        # Energy loss for this component
        energy_loss = component.energyConsumed(
            input_flow=current_flow,
            input_mass=mass_flow
        )
        total_energy_loss += energy_loss
        
        # Update flow for next component
        current_flow = component.processFlow(
            input_flow=current_flow,
            input_mass=mass_flow,
            interval=1
        )
    
    # Convert energy loss to pressure drop
    # ΔP = ΔE / Volume = ΔE * density / mass
    pressure_drop = total_energy_loss * density / (mass_flow if mass_flow > 0 else 1)
    
    return pressure drop, current_flow

# Example usage
pipeline = [
    Pipe(length=20, diameter=0.1, friction_factor=0.02),
    Bend(bend_radius=0.5, bend_factor=0.9, diameter=0.1),
    Valve(resistance_coefficient=2.0, diameter=0.1)
]

pressure_drop, final_flow = calculate_pressure_drop(
    pipeline,
    flow_rate=0.05,
    density=1000
)

print(f"Total pressure drop: {pressure_drop:.2f} Pa")
print(f"Final flow rate: {final_flow:.4f} m³/s")
```

### System Sizing

```python
def size_system_for_capacity(target_capacity, max_pressure_drop):
    """
    Determine pipe diameter needed for target capacity
    
    Args:
        target_capacity: Required flow rate (m³/s)
        max_pressure_drop: Maximum allowable pressure drop (Pa)
    
    Returns:
        Recommended diameter (m)
    """
    density = 1000  # kg/m³
    length = 50  # Total pipeline length
    friction_factor = 0.02
    
    for diameter in np.linspace(0.05, 0.5, 100):
        pipe = Pipe(
            length=length,
            diameter=diameter,
            friction_factor=friction_factor
        )
        
        output_flow = pipe.processFlow(
            input_flow=target_capacity,
            input_mass=target_capacity * density,
            interval=1
        )
        
        # Calculate pressure drop
        energy_loss = pipe.energyConsumed(
            input_flow=target_capacity,
            input_mass=target_capacity * density
        )
        pressure_drop = energy_loss * density / (target_capacity * density)
        
        if pressure_drop <= max_pressure_drop:
            return diameter
    
    return None  # No suitable diameter found

# Example
recommended_diameter = size_system_for_capacity(
    target_capacity=0.1,  # 0.1 m³/s
    max_pressure_drop=50000  # 50 kPa
)

if recommended_diameter:
    print(f"Recommended diameter: {recommended_diameter:.3f} m")
else:
    print("No suitable diameter found within constraints")
```

---

## Troubleshooting

### Common Issues

**Issue: Output flow is zero**
- Check that `input_flow` and `input_mass` are non-zero
- Verify that energy loss isn't exceeding input energy
- Consider increasing diameter or reducing length

**Issue: Unrealistic energy losses**
- Check friction factor values (should be 0.01-0.10)
- Verify bend_factor is between 0 and 1
- Ensure resistance coefficients are reasonable

**Issue: Mass flow seems to change**
- Mass is conserved through connectors
- Only volumetric flow rate changes due to energy loss
- Density remains constant in each connector

---

## Next Steps

- **[Process Systems](process-systems.md)**: Learn about chemical processing
- **[Examples](examples.md)**: See complete system integrations
- **[API Reference](api-reference.md)**: Detailed method documentation
