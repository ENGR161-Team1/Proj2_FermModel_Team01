# Examples

Practical examples demonstrating common use cases for the Ethanol Plant Model.

## Table of Contents

1. [Basic Single Process](#basic-single-process)
2. [Complete Pipeline](#complete-pipeline)
3. [Batch Processing](#batch-processing)
4. [Working with Compositions](#working-with-compositions)
5. [Flow-Based Processing](#flow-based-processing)
6. [Transport with Connectors](#transport-with-connectors)
7. [Logging and Visualization](#logging-and-visualization)

---

## Basic Single Process

Process a single batch through fermentation.

```python
from systems.processes import Fermentation

# Create system
fermenter = Fermentation(efficiency=0.95)

# Define inputs
inputs = {
    "ethanol": 0,
    "water": 1000,
    "sugar": 500,
    "fiber": 50
}

# Process
result = fermenter.processMass(
    inputs=inputs,
    input_type="amount",
    output_type="full"
)

# Display results
print("=== Fermentation Results ===")
print(f"Ethanol produced: {result['amount']['ethanol']:.2f} kg")
print(f"Sugar remaining: {result['amount']['sugar']:.2f} kg")
print(f"Ethanol composition: {result['composition']['ethanol']:.2%}")
```

---

## Complete Pipeline

Process materials through all four stages.

```python
from systems.processes import Fermentation, Filtration, Distillation, Dehydration

# Initialize systems
fermenter = Fermentation(efficiency=0.94)
filter_sys = Filtration(efficiency=0.90)
distiller = Distillation(efficiency=0.97)
dehydrator = Dehydration(efficiency=0.99)

# Raw materials
raw_materials = {
    "ethanol": 0,
    "water": 5000,
    "sugar": 2000,
    "fiber": 200
}

print("=== Ethanol Production Pipeline ===\n")
print(f"Input: {sum(raw_materials.values())} kg total")

# Step 1: Fermentation
step1 = fermenter.processMass(
    inputs=raw_materials,
    input_type="amount",
    output_type="full"
)
print(f"\nAfter Fermentation:")
print(f"  Ethanol: {step1['amount']['ethanol']:.2f} kg")
print(f"  Purity: {step1['composition']['ethanol']:.2%}")

# Step 2: Filtration
step2 = filter_sys.processMass(
    inputs=step1['amount'],
    input_type="amount",
    output_type="full"
)
print(f"\nAfter Filtration:")
print(f"  Ethanol: {step2['amount']['ethanol']:.2f} kg")
print(f"  Fiber: {step2['amount']['fiber']:.2f} kg")

# Step 3: Distillation
step3 = distiller.processMass(
    inputs=step2['amount'],
    input_type="amount",
    output_type="full"
)
print(f"\nAfter Distillation:")
print(f"  Ethanol: {step3['amount']['ethanol']:.2f} kg")
print(f"  Purity: {step3['composition']['ethanol']:.2%}")

# Step 4: Dehydration
final = dehydrator.processMass(
    inputs=step3['amount'],
    input_type="amount",
    output_type="full"
)
print(f"\nFinal Product:")
print(f"  Ethanol: {final['amount']['ethanol']:.2f} kg")
print(f"  Purity: {final['composition']['ethanol']:.3%}")
print(f"  Water: {final['amount']['water']:.2f} kg")

# Overall efficiency
overall_efficiency = final['amount']['ethanol'] / (raw_materials['sugar'] * 0.51) * 100
print(f"\nOverall Efficiency: {overall_efficiency:.1f}%")
```

---

## Batch Processing

Process multiple batches and track results.

```python
from systems.processes import Fermentation

fermenter = Fermentation(efficiency=0.95)

# Define multiple batches
batches = {
    "ethanol": [0, 0, 0, 0, 0],
    "water": [1000, 1200, 900, 1100, 1000],
    "sugar": [500, 600, 450, 550, 500],
    "fiber": [50, 60, 45, 55, 50]
}

# Process all batches
fermenter.iterateMassInputs(
    inputValues=batches,
    input_type="amount",
    output_type="full"
)

# Analyze results
print("=== Batch Processing Results ===\n")
print("Batch | Input Sugar | Output Ethanol | Conversion")
print("------|-------------|----------------|------------")

for i in range(len(batches['sugar'])):
    input_sugar = fermenter.input_log['mass']['amount']['sugar'][i]
    output_ethanol = fermenter.output_log['mass']['amount']['ethanol'][i]
    conversion = (output_ethanol / input_sugar) * 100
    print(f"  {i+1}   |   {input_sugar:6.1f} kg |   {output_ethanol:7.2f} kg |  {conversion:5.2f}%")

# Calculate statistics
import statistics
ethanol_outputs = fermenter.output_log['mass']['amount']['ethanol']
print(f"\nStatistics:")
print(f"  Mean ethanol: {statistics.mean(ethanol_outputs):.2f} kg")
print(f"  Std dev: {statistics.stdev(ethanol_outputs):.2f} kg")
print(f"  Total: {sum(ethanol_outputs):.2f} kg")
```

---

## Working with Compositions

Use fractional compositions instead of absolute amounts.

```python
from systems.processes import Distillation

distiller = Distillation(efficiency=0.98)

# Define input as composition (fractions must sum to 1.0)
composition = {
    "ethanol": 0.50,
    "water": 0.45,
    "sugar": 0.04,
    "fiber": 0.01
}

# Process with total mass specified
result = distiller.processMass(
    inputs=composition,
    input_type="composition",
    output_type="full",
    total_mass=1000  # 1000 kg total
)

print("=== Distillation with Composition Input ===\n")
print("Input Composition:")
for comp, frac in composition.items():
    print(f"  {comp:8s}: {frac:.2%}")

print(f"\nOutput Amounts:")
for comp, amount in result['amount'].items():
    print(f"  {comp:8s}: {amount:7.2f} kg")

print(f"\nOutput Composition:")
for comp, frac in result['composition'].items():
    print(f"  {comp:8s}: {frac:.3%}")

# Calculate purification factor
purity_increase = result['composition']['ethanol'] / composition['ethanol']
print(f"\nPurity increase: {purity_increase:.2f}x")
```

---

## Flow-Based Processing

Work with volumetric flow rates instead of masses.

```python
from systems.processes import Fermentation

fermenter = Fermentation(efficiency=0.95)

# Define inputs as volumetric flows (m³)
flow_inputs = {
    "ethanol": 0.0,
    "water": 1.0,    # 1 m³ water ≈ 997 kg
    "sugar": 0.314,  # 0.314 m³ sugar ≈ 500 kg
    "fiber": 0.038   # 0.038 m³ fiber ≈ 50 kg
}

# Process flows
result = fermenter.processFlow(
    inputs=flow_inputs,
    input_type="amount",
    output_type="full"
)

print("=== Flow-Based Processing ===\n")
print("Input Flows:")
for comp, flow in flow_inputs.items():
    print(f"  {comp:8s}: {flow:.3f} m³")

print(f"\nOutput Flows:")
for comp, flow in result['amount'].items():
    print(f"  {comp:8s}: {flow:.3f} m³")

print(f"\nTotal volume change:")
total_in = sum(flow_inputs.values())
total_out = sum(result['amount'].values())
print(f"  Input: {total_in:.3f} m³")
print(f"  Output: {total_out:.3f} m³")
print(f"  Change: {total_out - total_in:.3f} m³ ({((total_out/total_in)-1)*100:+.1f}%)")
```

---

## Transport with Connectors

Model energy losses during fluid transport.

```python
from systems.processes import Fermentation, Filtration
from systems.connectors import Pipe, Bend, Valve

# Process systems
fermenter = Fermentation(efficiency=0.95)
filter_sys = Filtration(efficiency=0.90)

# Transport components
pipe1 = Pipe(length=10.0, diameter=0.2, friction_factor=0.02)
bend1 = Bend(bend_radius=0.5, bend_factor=0.92, diameter=0.2)
valve1 = Valve(resistance_coefficient=0.8, diameter=0.2)

# Initial conditions
initial_energy = 50000  # Joules
flow_rate = 0.2         # m³/s
mass_rate = 160         # kg/s (approximate for mixed stream)

print("=== Transport Energy Losses ===\n")

# Fermentation
result1 = fermenter.processMass(
    inputs={"ethanol": 0, "water": 1000, "sugar": 500, "fiber": 50},
    input_type="amount",
    output_type="amount"
)

# Transport step 1: Pipe
energy_after_pipe = pipe1.pipeEnergyFunction(
    input_flow=flow_rate,
    input_mass=mass_rate,
    input_energy=initial_energy
)
loss_pipe = initial_energy - energy_after_pipe
print(f"After 10m pipe:")
print(f"  Energy: {energy_after_pipe:.0f} J")
print(f"  Loss: {loss_pipe:.0f} J ({(loss_pipe/initial_energy)*100:.1f}%)")

# Transport step 2: Bend
energy_after_bend = bend1.bendEnergyFunction(
    input_flow=flow_rate,
    input_mass=mass_rate,
    input_energy=energy_after_pipe
)
loss_bend = energy_after_pipe - energy_after_bend
print(f"\nAfter bend:")
print(f"  Energy: {energy_after_bend:.0f} J")
print(f"  Loss: {loss_bend:.0f} J ({(loss_bend/energy_after_pipe)*100:.1f}%)")

# Transport step 3: Valve
energy_after_valve = valve1.valveEnergyFunction(
    input_flow=flow_rate,
    input_mass=mass_rate,
    input_energy=energy_after_bend
)
loss_valve = energy_after_bend - energy_after_valve
print(f"\nAfter valve:")
print(f"  Energy: {energy_after_valve:.0f} J")
print(f"  Loss: {loss_valve:.0f} J ({(loss_valve/energy_after_bend)*100:.1f}%)")

# Filtration (mass is conserved through transport)
result2 = filter_sys.processMass(
    inputs=result1,
    input_type="amount",
    output_type="full"
)

# Summary
total_loss = initial_energy - energy_after_valve
print(f"\n=== Summary ===")
print(f"Initial energy: {initial_energy} J")
print(f"Final energy: {energy_after_valve:.0f} J")
print(f"Total loss: {total_loss:.0f} J ({(total_loss/initial_energy)*100:.1f}%)")
print(f"Transport efficiency: {(energy_after_valve/initial_energy)*100:.1f}%")
```

---

## Logging and Visualization

Track and visualize process data over multiple runs.

```python
from systems.processes import Fermentation
import matplotlib.pyplot as plt

fermenter = Fermentation(efficiency=0.95)

# Process multiple batches with varying sugar inputs
sugar_inputs = range(300, 701, 50)  # 300 to 700 kg
batches = {
    "ethanol": [0] * len(sugar_inputs),
    "water": [1000] * len(sugar_inputs),
    "sugar": list(sugar_inputs),
    "fiber": [50] * len(sugar_inputs)
}

# Process all batches
fermenter.iterateMassInputs(
    inputValues=batches,
    input_type="amount",
    output_type="full"
)

# Extract data from logs
input_sugar = fermenter.input_log['mass']['amount']['sugar']
output_ethanol = fermenter.output_log['mass']['amount']['ethanol']
output_composition = fermenter.output_log['mass']['composition']['ethanol']

# Create visualizations
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

# Plot 1: Sugar vs Ethanol
ax1.plot(input_sugar, output_ethanol, 'o-', linewidth=2, markersize=8)
ax1.set_xlabel('Input Sugar (kg)', fontsize=12)
ax1.set_ylabel('Output Ethanol (kg)', fontsize=12)
ax1.set_title('Sugar to Ethanol Conversion', fontsize=14)
ax1.grid(True, alpha=0.3)

# Plot 2: Sugar vs Ethanol Composition
ax2.plot(input_sugar, [c*100 for c in output_composition], 'o-', 
         linewidth=2, markersize=8, color='orange')
ax2.set_xlabel('Input Sugar (kg)', fontsize=12)
ax2.set_ylabel('Ethanol Composition (%)', fontsize=12)
ax2.set_title('Output Ethanol Purity', fontsize=14)
ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('fermentation_analysis.png', dpi=150)
print("Plots saved to 'fermentation_analysis.png'")

# Statistical summary
print("\n=== Statistical Summary ===")
print(f"Batches processed: {len(input_sugar)}")
print(f"Sugar range: {min(input_sugar):.0f} - {max(input_sugar):.0f} kg")
print(f"Ethanol range: {min(output_ethanol):.2f} - {max(output_ethanol):.2f} kg")
print(f"Average conversion: {(sum(output_ethanol)/sum(input_sugar)):.3f} kg ethanol/kg sugar")
```

---

## Tips and Best Practices

### 1. Choose Appropriate Input Types

- Use `"amount"` for absolute quantities
- Use `"composition"` when working with fractional data
- Use `"full"` when you need both for analysis

### 2. Enable Logging for Analysis

```python
result = system.processMass(
    inputs=data,
    input_type="amount",
    output_type="full",
    store_inputs=True,   # Enable input logging
    store_outputs=True   # Enable output logging
)
```

### 3. Handle Edge Cases

```python
# Check for zero total before calculating composition
total = sum(amounts.values())
if total > 0:
    composition = {k: v/total for k, v in amounts.items()}
else:
    composition = {k: 0 for k in amounts.keys()}
```

### 4. Validate Efficiency Parameters

```python
def create_system(efficiency):
    if not 0 <= efficiency <= 1:
        raise ValueError("Efficiency must be between 0 and 1")
    return Fermentation(efficiency=efficiency)
```

### 5. Use Flow Processing for Continuous Operations

```python
# For continuous flow operations, use processFlow
result = system.processFlow(
    inputs=flow_rates,
    input_type="amount",
    output_type="full"
)
```

---

**Navigation:** [Home](README.md) | [Getting Started](getting-started.md) | [API Reference](api-reference.md) | [Process Systems](process-systems.md) | [Connector Systems](connector-systems.md) | [Examples](examples.md)
