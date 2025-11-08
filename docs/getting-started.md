# Getting Started

This guide will help you install and start using the Ethanol Plant Model.

## Installation

### System Requirements

- Python >= 3.10
- GTK4 development libraries
- GObject introspection

### Install Dependencies (Ubuntu/Debian)

```bash
sudo apt install libgirepository2.0-dev libcairo2-dev libgtk-4-dev \
    pkg-config python3-dev python3-gi python3-gi-cairo \
    gir1.2-gtk-4.0 gobject-introspection
```

### Install Using pip

```bash
git clone https://github.com/ENGR161-Team1/EthanolPlantModel.git
cd EthanolPlantModel
pip install .
```

### Install Using uv (Faster)

```bash
# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Clone and install
git clone https://github.com/ENGR161-Team1/EthanolPlantModel.git
cd EthanolPlantModel
uv pip install .
```

## Basic Usage

### Your First Simulation

```python
from systems.processes import Fermentation

# Create a fermentation system
fermenter = Fermentation(efficiency=0.95)

# Define input materials (in kg)
inputs = {
    "ethanol": 0,      # No ethanol initially
    "water": 100,      # 100 kg water
    "sugar": 50,       # 50 kg sugar
    "fiber": 10        # 10 kg fiber
}

# Process through fermentation
output = fermenter.processMass(
    inputs=inputs,
    input_type="amount",
    output_type="full"
)

# View results
print(f"Ethanol: {output['amount']['ethanol']:.2f} kg")
print(f"Purity: {output['composition']['ethanol']:.2%}")
```

### Understanding Input/Output Types

The model supports three data formats:

**1. Amount** - Absolute quantities
```python
{"ethanol": 25.5, "water": 80.0, "sugar": 5.0, "fiber": 1.0}
```

**2. Composition** - Fractional values (must sum to 1.0)
```python
{"ethanol": 0.23, "water": 0.72, "sugar": 0.04, "fiber": 0.01}
```

**3. Full** - Both amounts and compositions
```python
{
    "amount": {"ethanol": 25.5, "water": 80.0, ...},
    "composition": {"ethanol": 0.23, "water": 0.72, ...}
}
```

### Complete Pipeline Example

```python
from systems.processes import Fermentation, Filtration, Distillation, Dehydration

# Initialize all systems
fermenter = Fermentation(efficiency=0.95)
filter_sys = Filtration(efficiency=0.90)
distiller = Distillation(efficiency=0.98)
dehydrator = Dehydration(efficiency=0.99)

# Input materials
raw_input = {"ethanol": 0, "water": 3000, "sugar": 1000, "fiber": 100}

# Process through pipeline
step1 = fermenter.processMass(inputs=raw_input, input_type="amount", output_type="amount")
step2 = filter_sys.processMass(inputs=step1, input_type="amount", output_type="amount")
step3 = distiller.processMass(inputs=step2, input_type="amount", output_type="amount")
final = dehydrator.processMass(inputs=step3, input_type="amount", output_type="full")

print(f"Final ethanol: {final['amount']['ethanol']:.2f} kg")
print(f"Final purity: {final['composition']['ethanol']:.2%}")
```

## Next Steps

- [API Reference](api-reference.md) - Explore all available methods
- [Process Systems](process-systems.md) - Learn about each process stage
- [Examples](examples.md) - See more practical examples

---

**Navigation:** [Home](README.md) | [Getting Started](getting-started.md) | [API Reference](api-reference.md) | [Process Systems](process-systems.md) | [Examples](examples.md)
