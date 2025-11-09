# Examples

**Version:** 0.7.0

Practical examples and tutorials for using the Ethanol Plant Model.

## 🆕 v0.7.0 Updates

All examples now demonstrate:
- **Static methods** for cleaner conversion code
- **Flexible output types** to choose your output format
- **Class constants** for density values
- **Simplified API** with better performance

## Example 1: Basic Fermentation

### Understanding the Process

Process a sugar-water mixture through fermentation:

```python
from systems.processors import Fermentation

# Initialize fermenter
fermenter = Fermentation(
    efficiency=0.95,
    power_consumption_rate=100,
    power_consumption_unit="kW"
)

# Define inputs (kg/s)
inputs = {
    "ethanol": 0,
    "water": 100,
    "sugar": 50,
    "fiber": 10
}

# Process with full output (v0.7.0: flexible output_type)
result = fermenter.processMassFlow(
    inputs=inputs,
    input_type="amount",
    output_type="full",  # Get both amounts and compositions
    store_outputs=True
)

# Access results
print(f"Ethanol produced: {result['amount']['ethanol']:.2f} kg/s")
print(f"Sugar remaining: {result['amount']['sugar']:.2f} kg/s")
print(f"Ethanol purity: {result['composition']['ethanol']:.2%}")
```

**Output:**
```
Ethanol produced: 24.44 kg/s  # Calculated from stoichiometry (documented)
Sugar remaining: 0.03 kg/s    # Small amount due to 95% efficiency
Ethanol purity: 15.24%        # Mass fraction (documented calculation)
```

**Understanding the Chemistry:**
```python
# Chemical equation (documented in Fermentation docstring):
# C₆H₁₂O₆ → 2 C₂H₅OH + 2 CO₂
# 180 g glucose → 92 g ethanol (theoretical)
# Efficiency factor: 95% × 92/180 = 0.4867 kg ethanol / kg sugar
```

## Example 2: Complete Ethanol Production Pipeline

### Full Process Chain (Enhanced Documentation)

This example demonstrates a complete ethanol plant with enhanced inline documentation:

```python
from systems.processors import Fermentation, Filtration, Distillation, Dehydration

# Step 1: Fermentation
# See docstring for chemical equation and yield calculations
fermenter = Fermentation(efficiency=0.95, power_consumption_rate=100, power_consumption_unit="kW")

# Initial feed (units documented)
feed = {
    "ethanol": 0,    # kg/s
    "water": 1000,   # kg/s
    "sugar": 500,    # kg/s
    "fiber": 100     # kg/s
}

# Process through fermentation (documented stoichiometry)
fermentation_output = fermenter.processMassFlow(
    inputs=feed,
    input_type="amount",
    output_type="full",
    store_outputs=True
)

print("After Fermentation (documented calculations):")
print(f"  Ethanol: {fermentation_output['amount']['ethanol']:.2f} kg/s")
print(f"  Water: {fermentation_output['amount']['water']:.2f} kg/s")
print(f"  Sugar: {fermentation_output['amount']['sugar']:.2f} kg/s")
print(f"  Fiber: {fermentation_output['amount']['fiber']:.2f} kg/s")
print(f"  Ethanol purity: {fermentation_output['composition']['ethanol']:.2%}\n")

# Step 2: Filtration
# See docstring for mechanical separation principles
filter_unit = Filtration(efficiency=0.98, power_consumption_rate=50, power_consumption_unit="kW")

# Process through filtration (fiber removal documented)
filtration_output = filter_unit.processMassFlow(
    inputs=fermentation_output["amount"],
    input_type="amount",
    output_type="full",
    store_outputs=True
)

print("After Filtration (documented fiber removal):")
print(f"  Ethanol: {filtration_output['amount']['ethanol']:.2f} kg/s")
print(f"  Fiber removed: {fermentation_output['amount']['fiber'] - filtration_output['amount']['fiber']:.2f} kg/s")
print(f"  Ethanol purity: {filtration_output['composition']['ethanol']:.2%}\n")

# Step 3: Distillation
# See docstring for vapor-liquid equilibrium principles
distiller = Distillation(efficiency=0.95, power_consumption_rate=200, power_consumption_unit="kW")

# Process through distillation (separation documented)
distillation_output = distiller.processMassFlow(
    inputs=filtration_output["amount"],
    input_type="amount",
    output_type="full",
    store_outputs=True
)

print("After Distillation (documented vapor-liquid separation):")
print(f"  Ethanol: {distillation_output['amount']['ethanol']:.2f} kg/s")
print(f"  Water: {distillation_output['amount']['water']:.2f} kg/s")
print(f"  Ethanol purity: {distillation_output['composition']['ethanol']:.2%}\n")

# Step 4: Dehydration
# See docstring for molecular sieve mechanism
dehydrator = Dehydration(efficiency=0.99, power_consumption_rate=150, power_consumption_unit="kW")

# Process through dehydration (water removal documented)
final_output = dehydrator.processMassFlow(
    inputs=distillation_output["amount"],
    input_type="amount",
    output_type="full",
    store_outputs=True
)

print("After Dehydration (documented molecular sieve adsorption):")
print(f"  Ethanol: {final_output['amount']['ethanol']:.2f} kg/s")
print(f"  Water: {final_output['amount']['water']:.2f} kg/s")
print(f"  Ethanol purity: {final_output['composition']['ethanol']:.2%}\n")

# Final product specifications (industry standards documented)
print("Final Product:")
print(f"  High-purity ethanol: {final_output['amount']['ethanol']:.2f} kg/s")
print(f"  Purity: {final_output['composition']['ethanol']:.2%}")
print(f"  Water content: {final_output['composition']['water']:.4%}")  # Should be < 0.5%
```

## Example 3: Fluid Transport with Connectors

### Understanding Energy Losses (Enhanced Documentation)

This example demonstrates connector physics with comprehensive documentation:

```python
from systems.connectors import Pipe, Bend, Valve

# Create pipe with documented parameters
# help(Pipe.__init__) for full parameter documentation
pipe = Pipe(
    length=10.0,          # float: Length in meters
    friction_factor=0.02, # float: Darcy friction factor (dimensionless)
    diameter=0.1          # float: Inner diameter in meters
)

# Define flow conditions (units documented)
input_flow = 0.01  # m³/s: Volumetric flow rate
input_mass = 10.0  # kg/s: Mass flow rate

# Calculate power loss - see docstring for Darcy-Weisbach equation
power_loss = pipe.powerConsumed(
    input_volumetric_flow=input_flow,
    input_mass_flow=input_mass
)
print(f"Pipe power loss: {power_loss:.2f} W")
print("  (Calculated using Darcy-Weisbach equation - see docstring)\n")

# Calculate output flow - see docstring for derivation
output_flow = pipe.processFlow(
    input_volumetric_flow=input_flow,
    input_mass_flow=input_mass
)
print(f"Input flow: {input_flow:.6f} m³/s")
print(f"Output flow: {output_flow:.6f} m³/s")
print(f"Flow reduction: {(1 - output_flow/input_flow)*100:.2f}%")
print("  (Due to kinetic energy loss from friction)\n")

# Create bend with documented parameters
# help(Bend.__init__) for physical principles
bend = Bend(
    bend_radius=0.5,    # float: Radius of curvature in meters
    bend_factor=0.9,    # float: Efficiency (1.0 = no loss)
    diameter=0.1        # float: Inner diameter in meters
)

# Calculate bend loss - see docstring for secondary flow explanation
bend_loss = bend.powerConsumed(
    input_volumetric_flow=output_flow,
    input_mass_flow=input_mass
)
print(f"Bend power loss: {bend_loss:.2f} W")
print("  (Due to secondary flows and turbulence - see docstring)\n")

# Calculate final output
final_flow = bend.processFlow(
    input_volumetric_flow=output_flow,
    input_mass_flow=input_mass
)
print(f"Flow after bend: {final_flow:.6f} m³/s")
print(f"Total flow reduction: {(1 - final_flow/input_flow)*100:.2f}%\n")

# Total energy analysis (documented principles)
total_loss = power_loss + bend_loss
print(f"Total power dissipated: {total_loss:.2f} W")
print("  (Energy converted to heat via friction and turbulence)")
```

**Physical Understanding (Documented in Code):**
```python
# Power loss mechanisms (all documented in docstrings):
# 1. Pipe: Darcy-Weisbach friction (ΔP = f × L/D × ρv²/2)
# 2. Bend: Secondary flows (P_loss = (1-η) × ½mv²)
# 3. Valve: Flow resistance (P_loss = K × ½mv²)
```

## Example 4: Batch Processing with Time Series

### Iterative Processing (Enhanced Documentation)

Process multiple time points with documented iteration methods:

```python
from systems.processors import Fermentation
import numpy as np

# Create fermenter (documented initialization)
fermenter = Fermentation(efficiency=0.95)

# Generate time-series data (documented format)
num_points = 10
time_steps = np.linspace(0, 100, num_points)  # seconds

# Input data structure (format documented in docstrings)
batch_inputs = {
    "ethanol": [0] * num_points,           # kg/s: No initial ethanol
    "water": [100] * num_points,           # kg/s: Constant water flow
    "sugar": np.linspace(50, 30, num_points).tolist(),  # kg/s: Decreasing sugar
    "fiber": [10] * num_points             # kg/s: Constant fiber
}

# Process batch - see docstring for detailed explanation
# help(fermenter.iterateMassFlowInputs)
outputs = fermenter.iterateMassFlowInputs(
    inputValues=batch_inputs,
    input_type="amount",    # str: Input format (documented)
    output_type="full"      # str: Return format (documented)
)

# Access logged results (structure documented in docstrings)
ethanol_produced = outputs["mass_flow"]["amount"]["ethanol"]
sugar_consumed = [
    batch_inputs["sugar"][i] - outputs["mass_flow"]["amount"]["sugar"][i]
    for i in range(num_points)
]

print("Batch Processing Results (time-series documented):")
for i in range(num_points):
    print(f"  t={time_steps[i]:.1f}s: "
          f"Sugar in={batch_inputs['sugar'][i]:.1f} kg/s, "
          f"Ethanol out={ethanol_produced[i]:.2f} kg/s")
```

**Understanding Batch Processing (Documented):**
```python
# Batch processing (method documented in detail):
# 1. Each time point processed independently
# 2. Results automatically logged
# 3. Access via output_log["mass_flow"]["amount"][component]
# 4. Compositions also available in output_log["mass_flow"]["composition"]
```

## Example 5: Power and Cost Tracking

### Resource Consumption Analysis (Enhanced Documentation)

Track energy consumption and costs with comprehensive documentation:

```python
from systems.processors import Fermentation

# Initialize with power and cost parameters (all documented)
# help(Fermentation.__init__) for parameter details
fermenter = Fermentation(
    efficiency=0.95,
    power_consumption_rate=100,      # float: Power in specified unit
    power_consumption_unit="kW",     # str: "kW", "W", or "kWh/day"
    cost_per_flow=50.0               # float: Cost in $/(m³/s)
)

# Process with tracking enabled (parameters documented)
result = fermenter.processMassFlow(
    inputs={"ethanol": 0, "water": 100, "sugar": 50, "fiber": 10},
    input_type="amount",
    output_type="full",
    store_outputs=True,
    store_cost=True  # bool: Enable cost logging (documented)
)

# Calculate energy consumption over 10 seconds (formula documented)
# help(fermenter.processPowerConsumption) for details
interval = 10  # seconds
energy = fermenter.processPowerConsumption(
    interval=interval,      # float: Time interval in seconds
    store_energy=True       # bool: Log power and energy
)

print("Resource Consumption (all calculations documented):")
print(f"  Power consumption rate: {fermenter.power_consumption_rate} W")
print(f"  Energy consumed (10s): {energy:.2f} J")
print(f"  Energy consumed (10s): {energy/1000:.2f} kJ")
print(f"  Energy consumed (10s): {energy/3.6e6:.6f} kWh\n")

# Access consumption log (structure documented in docstrings)
print("Consumption Log Structure (documented):")
print(f"  Power rates: {fermenter.consumption_log['power_consumption_rate']}")
print(f"  Energy consumed: {fermenter.consumption_log['energy_consumed']}")
print(f"  Intervals: {fermenter.consumption_log['interval']}")
print(f"  Cost per unit flow: {fermenter.consumption_log['cost_per_unit_flow']}")
print(f"  Cost incurred: {fermenter.consumption_log['cost_incurred']}")

# Calculate total cost (documented calculation)
total_cost = sum(fermenter.consumption_log["cost_incurred"])
print(f"\nTotal cost: ${total_cost:.2f}")
print("  (Based on volumetric flow rate × cost_per_flow - see docstring)")
```

**Understanding Energy Calculations (Fully Documented):**
```python
# Energy relationship (documented in processPowerConsumption):
# E = P × t
# Where:
#   E = Energy in Joules (J)
#   P = Power in Watts (W)
#   t = Time in seconds (s)
# Unit conversions (documented):
#   1 kWh = 3.6 × 10⁶ J
#   1 W = 1 J/s
```

## Example 6: Volumetric Flow Processing

### Working with Volumetric Data (Enhanced Documentation)

Process volumetric flow rates with documented conversions:

```python
from systems.processors import Fermentation

# Initialize (documented parameters)
fermenter = Fermentation(efficiency=0.95)

# Define volumetric inputs (units documented)
volumetric_inputs = {
    "ethanol": 0,       # m³/s: No initial ethanol
    "water": 0.1,       # m³/s: Water flow
    "sugar": 0.03,      # m³/s: Sugar flow
    "fiber": 0.008      # m³/s: Fiber flow
}

# Process volumetric flow - see docstring for conversion details
# help(fermenter.processVolumetricFlow)
result = fermenter.processVolumetricFlow(
    inputs=volumetric_inputs,
    input_type="amount",
    output_type="full",
    store_outputs=True
)

print("Volumetric Flow Processing (conversions documented):")
print(f"  Ethanol produced: {result['amount']['ethanol']:.6f} m³/s")
print(f"  Ethanol purity: {result['composition']['ethanol']:.2%}\n")

# Understanding the conversion (documented in code)
print("Internal Conversion Process (see volumetricToMass docstring):")
print("  1. Volumetric → Mass using density:")
print(f"     Water: {volumetric_inputs['water']} m³/s × 997 kg/m³ = "
      f"{volumetric_inputs['water'] * 997:.2f} kg/s")
print("  2. Process mass flows through chemical transformation")
print("  3. Mass → Volumetric using density:")
print("     Ethanol: mass_flow / 789 kg/m³ = volumetric_flow")
```

**Density Values (Documented in Code):**
```python
# Component densities at standard conditions (documented in Process class):
# - Water: 997 kg/m³ (20°C)
# - Ethanol: 789 kg/m³ (20°C)
# - Sugar (sucrose): 1590 kg/m³ (solid density)
# - Fiber (cellulose): 1311 kg/m³ (solid density)
```

## Best Practices (Enhanced for v0.6.1)

### Leveraging Enhanced Documentation

1. **Always check docstrings first:**
   ```python
   help(Fermentation)           # Class overview
   help(fermenter.processMassFlow)  # Method details
   Fermentation.__init__?       # In IPython/Jupyter
   ```

2. **Read inline comments in source:**
   - Step-by-step calculation explanations
   - Physical principles documented
   - Formula derivations included

3. **Understand parameter types and units:**
   - All documented in docstrings
   - SI units used consistently
   - Conversions provided where needed

### Debugging with Documentation

```python
# Use documented structure to debug
result = process.processMassFlow(inputs=data, ...)

# Check intermediate values (structure documented)
print("Input log:", process.input_log)
print("Output log:", process.output_log)
print("Consumption log:", process.consumption_log)

# Verify conversions (formulas documented in docstrings)
mass = process.volumetricToMass(inputs=vol_data, mode="amount")
vol_back = process.massToVolumetric(inputs=mass, mode="amount")
# Should be approximately equal (documented relationship)
```

### Learning from Examples

1. **Start simple** - Example 1 covers basics with full documentation
2. **Build complexity** - Example 2 shows complete pipeline
3. **Understand physics** - Example 3 explains energy losses
4. **Scale up** - Example 4 demonstrates batch processing
5. **Track resources** - Example 5 covers costs and energy
6. **Master conversions** - Example 6 handles volumetric data

## Related Documentation

- **[Getting Started](getting-started.md)** - Installation and setup with v0.6.1 enhancements
- **[API Reference](api-reference.md)** - Complete API with comprehensive docstrings
- **[Process Systems](process-systems.md)** - Process details with enhanced documentation
- **[Connector Systems](connector-systems.md)** - Fluid transport with physics documentation

---

*All examples benefit from comprehensive docstrings and inline comments added in v0.6.1*

*Use `help()` on any class or method to see detailed documentation!*

*Last updated: Version 0.6.1 - November 2025*
