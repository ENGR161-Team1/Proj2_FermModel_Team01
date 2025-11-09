# Examples

Practical examples demonstrating the Ethanol Plant Model capabilities.

## Example 1: Basic Fermentation Process

```python
from systems.processors import Fermentation

# Create fermenter with 95% efficiency
fermenter = Fermentation(efficiency=0.95)

# Process inputs
result = fermenter.processMassFlow(
    inputs={"ethanol": 0, "water": 100, "sugar": 50, "fiber": 10},
    input_type="amount",
    output_type="full",
    store_outputs=True
)

print("=== Fermentation Results ===")
print(f"Ethanol produced: {result['amount']['ethanol']:.2f} kg/s")
print(f"Water: {result['amount']['water']:.2f} kg/s")
print(f"Remaining sugar: {result['amount']['sugar']:.2f} kg/s")
print(f"Fiber: {result['amount']['fiber']:.2f} kg/s")
print(f"\nEthanol purity: {result['composition']['ethanol']:.2%}")
```

## Example 2: Complete Production Pipeline

```python
from systems.processors import Fermentation, Filtration, Distillation, Dehydration

# Initialize all processes
fermenter = Fermentation(efficiency=0.95)
filter_system = Filtration(efficiency=0.98)
distiller = Distillation(efficiency=0.90)
dehydrator = Dehydration(efficiency=0.95)

# Initial inputs
initial_inputs = {
    "ethanol": 0,
    "water": 1000,
    "sugar": 500,
    "fiber": 100
}

# Step 1: Fermentation
print("Step 1: Fermentation")
fermentation_output = fermenter.processMassFlow(
    inputs=initial_inputs,
    input_type="amount",
    output_type="full"
)
print(f"Ethanol: {fermentation_output['amount']['ethanol']:.2f} kg/s")

# Step 2: Filtration
print("\nStep 2: Filtration")
filtration_output = filter_system.processMassFlow(
    inputs=fermentation_output['amount'],
    input_type="amount",
    output_type="full"
)
print(f"Fiber removed: {initial_inputs['fiber'] - filtration_output['amount']['fiber']:.2f} kg/s")

# Step 3: Distillation
print("\nStep 3: Distillation")
distillation_output = distiller.processMassFlow(
    inputs=filtration_output['amount'],
    input_type="amount",
    output_type="full"
)
print(f"Ethanol purity: {distillation_output['composition']['ethanol']:.2%}")

# Step 4: Dehydration
print("\nStep 4: Dehydration")
final_output = dehydrator.processMassFlow(
    inputs=distillation_output['amount'],
    input_type="amount",
    output_type="full"
)
print(f"Final ethanol purity: {final_output['composition']['ethanol']:.2%}")
print(f"Final ethanol amount: {final_output['amount']['ethanol']:.2f} kg/s")
```

## Example 3: Volumetric Flow Rate Processing

```python
from systems.processors import Fermentation

fermenter = Fermentation(efficiency=0.95)

# Input volumetric flow rates (m³/s)
volumetric_inputs = {
    "water": 0.100,      # 100 L/s
    "sugar": 0.031,      # 31 L/s
    "fiber": 0.008       # 8 L/s
}

result = fermenter.processVolumetricFlow(
    inputs=volumetric_inputs,
    input_type="amount",
    output_type="full"
)

print("=== Volumetric Flow Results ===")
print(f"Ethanol flow: {result['amount']['ethanol']*1000:.2f} L/s")
print(f"Total output flow: {sum(result['amount'].values())*1000:.2f} L/s")
print(f"Ethanol concentration: {result['composition']['ethanol']:.2%}")
```

## Example 4: Batch Processing

```python
from systems.processors import Fermentation
import matplotlib.pyplot as plt

fermenter = Fermentation(efficiency=0.95)

# Batch inputs with varying sugar concentrations
batch_inputs = {
    "ethanol": [0, 0, 0, 0, 0],
    "water": [100, 100, 100, 100, 100],
    "sugar": [30, 40, 50, 60, 70],
    "fiber": [10, 10, 10, 10, 10]
}

# Process batch
output_log = fermenter.iterateMassFlowInputs(
    inputValues=batch_inputs,
    input_type="amount",
    output_type="full"
)

# Extract results
sugar_inputs = batch_inputs["sugar"]
ethanol_outputs = output_log["mass_flow"]["amount"]["ethanol"]

# Plot results
plt.figure(figsize=(10, 6))
plt.plot(sugar_inputs, ethanol_outputs, marker='o', linewidth=2)
plt.xlabel("Sugar Input (kg/s)")
plt.ylabel("Ethanol Output (kg/s)")
plt.title("Fermentation: Sugar vs Ethanol Production")
plt.grid(True)
plt.show()

print("=== Batch Processing Results ===")
for i, (sugar, ethanol) in enumerate(zip(sugar_inputs, ethanol_outputs)):
    print(f"Batch {i+1}: {sugar} kg/s sugar → {ethanol:.2f} kg/s ethanol")
```

## Example 5: Energy Consumption Tracking

```python
from systems.processors import Distillation

# Create distiller with energy consumption tracking
distiller = Distillation(
    efficiency=0.90,
    energy_consumption_rate=150,  # kWh/day
    energy_consumption_unit="kWh/day"
)

inputs = {"ethanol": 50, "water": 100, "sugar": 5, "fiber": 1}

# Process and track energy
result = distiller.processMassFlow(
    inputs=inputs,
    input_type="amount",
    output_type="full"
)

# Calculate energy for 8-hour operation
energy_8hrs = distiller.processEnergyConsumption(
    interval=8*3600,  # 8 hours in seconds
    store_energy=True
)

print("=== Energy Consumption ===")
print(f"8-hour energy consumption: {energy_8hrs/3.6e6:.2f} kWh")
print(f"Daily energy consumption: {energy_8hrs*3/3.6e6:.2f} kWh")
```

## Example 6: Composition-Based Processing

```python
from systems.processors import Fermentation

fermenter = Fermentation(efficiency=0.95)

# Input as compositions (fractions)
composition_inputs = {
    "ethanol": 0.0,
    "water": 0.625,   # 62.5%
    "sugar": 0.313,   # 31.3%
    "fiber": 0.062    # 6.2%
}

total_mass_flow = 160  # kg/s total flow rate

result = fermenter.processMassFlow(
    inputs=composition_inputs,
    input_type="composition",
    output_type="full",
    total_mass_flow=total_mass_flow
)

print("=== Composition-Based Results ===")
print(f"Input composition: {composition_inputs}")
print(f"Total input flow: {total_mass_flow} kg/s")
print(f"\nOutput amounts:")
for component, amount in result['amount'].items():
    print(f"  {component}: {amount:.2f} kg/s")
print(f"\nOutput composition:")
for component, fraction in result['composition'].items():
    print(f"  {component}: {fraction:.2%}")
```

## Example 7: Iterative Process Optimization

```python
from systems.processors import Fermentation
import numpy as np

# Test different efficiency values
efficiencies = np.linspace(0.80, 0.99, 10)
results = []

for eff in efficiencies:
    fermenter = Fermentation(efficiency=eff)
    result = fermenter.processMassFlow(
        inputs={"ethanol": 0, "water": 100, "sugar": 50, "fiber": 10},
        input_type="amount",
        output_type="amount"
    )
    results.append(result["ethanol"])

# Find optimal efficiency
optimal_idx = np.argmax(results)
optimal_efficiency = efficiencies[optimal_idx]

print("=== Efficiency Optimization ===")
print(f"Optimal efficiency: {optimal_efficiency:.2%}")
print(f"Maximum ethanol production: {results[optimal_idx]:.2f} kg/s")

# Plot
import matplotlib.pyplot as plt
plt.figure(figsize=(10, 6))
plt.plot(efficiencies*100, results, marker='o')
plt.xlabel("Efficiency (%)")
plt.ylabel("Ethanol Production (kg/s)")
plt.title("Fermentation Efficiency vs Ethanol Production")
plt.grid(True)
plt.show()
```

## Example 8: Multi-Stage Processing with Logging

```python
from systems.processors import Fermentation, Filtration

# Create processes
fermenter = Fermentation(efficiency=0.95)
filter_system = Filtration(efficiency=0.98)

# Multiple batches
batch_data = {
    "ethanol": [0]*5,
    "water": [100, 120, 140, 160, 180],
    "sugar": [50, 60, 70, 80, 90],
    "fiber": [10, 12, 14, 16, 18]
}

# Stage 1: Fermentation
print("Stage 1: Fermentation")
ferm_log = fermenter.iterateMassFlowInputs(
    inputValues=batch_data,
    input_type="amount",
    output_type="full"
)

# Stage 2: Filtration (using fermentation outputs)
print("Stage 2: Filtration")
filt_inputs = {
    "ethanol": ferm_log["mass_flow"]["amount"]["ethanol"],
    "water": ferm_log["mass_flow"]["amount"]["water"],
    "sugar": ferm_log["mass_flow"]["amount"]["sugar"],
    "fiber": ferm_log["mass_flow"]["amount"]["fiber"]
}

filt_log = filter_system.iterateMassFlowInputs(
    inputValues=filt_inputs,
    input_type="amount",
    output_type="full"
)

# Compare results
print("\n=== Multi-Stage Results ===")
for i in range(5):
    print(f"\nBatch {i+1}:")
    print(f"  Input sugar: {batch_data['sugar'][i]:.1f} kg/s")
    print(f"  After fermentation - Ethanol: {ferm_log['mass_flow']['amount']['ethanol'][i]:.2f} kg/s")
    print(f"  After filtration - Ethanol: {filt_log['mass_flow']['amount']['ethanol'][i]:.2f} kg/s")
    print(f"  Final purity: {filt_log['mass_flow']['composition']['ethanol'][i]:.2%}")
```

## Power Consumption Tracking

### Example 1: Basic Power Tracking

```python
from systems.processors import Fermentation

# Create fermenter with power consumption
fermenter = Fermentation(
    efficiency=0.95,
    power_consumption_rate=50,  # 50 kWh/day
    power_consumption_unit="kWh/day"
)

# Process inputs
result = fermenter.processMassFlow(
    inputs={"ethanol": 0, "water": 100, "sugar": 50, "fiber": 10},
    output_type="full",
    store_outputs=True
)

# Calculate energy for 1 hour of operation
energy = fermenter.processPowerConsumption(store_energy=True, interval=3600)

print(f"Energy consumed: {energy/3_600_000:.2f} kWh")
print(f"Ethanol produced: {result['amount']['ethanol']:.2f} kg")
```

### Example 2: Multi-Process Energy Analysis

```python
from systems.processors import Fermentation, Filtration, Distillation, Dehydration

# Create complete process chain with power specifications
processes = {
    "Fermentation": Fermentation(efficiency=0.95, power_consumption_rate=50, power_consumption_unit="kWh/day"),
    "Filtration": Filtration(efficiency=0.98, power_consumption_rate=10, power_consumption_unit="kWh/day"),
    "Distillation": Distillation(efficiency=0.99, power_consumption_rate=100, power_consumption_unit="kWh/day"),
    "Dehydration": Dehydration(efficiency=0.95, power_consumption_rate=20, power_consumption_unit="kWh/day")
}

# Initial inputs
inputs = {"ethanol": 0, "water": 100, "sugar": 50, "fiber": 10}
interval = 3600  # 1 hour

# Process through each stage
energy_breakdown = {}
current_output = inputs

for name, process in processes.items():
    # Process the inputs
    current_output = process.processMassFlow(
        inputs=current_output,
        output_type="amount",
        store_outputs=True
    )
    
    # Calculate and store energy
    energy = process.processPowerConsumption(store_energy=True, interval=interval)
    energy_breakdown[name] = energy / 3_600_000  # Convert to kWh

# Print results
print("Energy Consumption Breakdown:")
print("-" * 40)
for name, energy in energy_breakdown.items():
    print(f"{name:15} {energy:>8.2f} kWh")
print("-" * 40)
print(f"{'Total':15} {sum(energy_breakdown.values()):>8.2f} kWh")

# Final product
print(f"\nFinal ethanol: {current_output['ethanol']:.2f} kg")
print(f"Final purity: {current_output['ethanol']/sum(current_output.values()):.2%}")
```

### Example 3: Energy Tracking Over Time

```python
from systems.processors import Fermentation
import numpy as np

# Create fermenter
fermenter = Fermentation(
    efficiency=0.95,
    power_consumption_rate=50,
    power_consumption_unit="kWh/day"
)

# Simulate 24 hours of operation
hours = 24
interval = 3600  # 1 hour in seconds

for hour in range(hours):
    # Process inputs (assuming continuous operation)
    result = fermenter.processMassFlow(
        inputs={"ethanol": 0, "water": 100, "sugar": 50, "fiber": 10},
        output_type="amount",
        store_outputs=True
    )
    
    # Track energy for this hour
    energy = fermenter.processPowerConsumption(store_energy=True, interval=interval)

# Analyze power log
power_log = fermenter.power_log
total_energy_j = sum(power_log["energy_consumed"])
total_energy_kwh = total_energy_j / 3_600_000
avg_power_w = np.mean(power_log["power_consumption_rate"])

print(f"Total energy (24h): {total_energy_kwh:.2f} kWh")
print(f"Average power: {avg_power_w/1000:.2f} kW")
print(f"Total ethanol produced: {sum(fermenter.output_log['mass_flow']['amount']['ethanol']):.2f} kg")
```

### Example 4: Different Power Units

```python
from systems.processors import Fermentation, Filtration, Distillation

# Different unit specifications
fermenter = Fermentation(
    efficiency=0.95,
    power_consumption_rate=50,
    power_consumption_unit="kWh/day"
)

filter = Filtration(
    efficiency=0.98,
    power_consumption_rate=0.417,  # Equivalent to 10 kWh/day
    power_consumption_unit="kW"
)

distiller = Distillation(
    efficiency=0.99,
    power_consumption_rate=4167,  # Equivalent to 100 kWh/day
    power_consumption_unit="W"
)

# All are internally converted to Watts
print(f"Fermenter power: {fermenter.power_consumption_rate:.2f} W")
print(f"Filter power: {filter.power_consumption_rate:.2f} W")
print(f"Distiller power: {distiller.power_consumption_rate:.2f} W")
```

## Batch Processing

```python
from systems.processors import Fermentation
import matplotlib.pyplot as plt

fermenter = Fermentation(efficiency=0.95)

# Batch inputs with varying sugar concentrations
batch_inputs = {
    "ethanol": [0, 0, 0, 0, 0],
    "water": [100, 100, 100, 100, 100],
    "sugar": [30, 40, 50, 60, 70],
    "fiber": [10, 10, 10, 10, 10]
}

# Process batch
output_log = fermenter.iterateMassFlowInputs(
    inputValues=batch_inputs,
    input_type="amount",
    output_type="full"
)

# Extract results
sugar_inputs = batch_inputs["sugar"]
ethanol_outputs = output_log["mass_flow"]["amount"]["ethanol"]

# Plot results
plt.figure(figsize=(10, 6))
plt.plot(sugar_inputs, ethanol_outputs, marker='o', linewidth=2)
plt.xlabel("Sugar Input (kg/s)")
plt.ylabel("Ethanol Output (kg/s)")
plt.title("Fermentation: Sugar vs Ethanol Production")
plt.grid(True)
plt.show()

print("=== Batch Processing Results ===")
for i, (sugar, ethanol) in enumerate(zip(sugar_inputs, ethanol_outputs)):
    print(f"Batch {i+1}: {sugar} kg/s sugar → {ethanol:.2f} kg/s ethanol")
```
