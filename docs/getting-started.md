# Getting Started

This guide will help you install and start using the Ethanol Plant Model.

## Installation

### Prerequisites

**Python Version**: Python 3.10 or higher is required.

**System Dependencies** (Ubuntu/Debian):
```bash
sudo apt install libgirepository2.0-dev libcairo2-dev libgtk-4-dev \
    pkg-config python3-dev python3-gi python3-gi-cairo \
    gir1.2-gtk-4.0 gobject-introspection
```

### Option 1: Install with pip

```bash
git clone https://github.com/ENGR161-Team1/EthanolPlantModel.git
cd EthanolPlantModel
pip install .
```

### Option 2: Install with uv (Recommended - Faster)

```bash
# Install uv if you haven't already
curl -LsSf https://astral.sh/uv/install.sh | sh

# Clone and install
git clone https://github.com/ENGR161-Team1/EthanolPlantModel.git
cd EthanolPlantModel
uv pip install .
```

## Basic Usage

### Importing Components

```python
# Import process systems
from systems.processors import Fermentation, Filtration, Distillation, Dehydration

# Import the base Process class if needed
from systems.process import Process

# Import connector systems
from systems.connectors import Pipe, Bend, Valve
```

### Simple Fermentation Example

```python
from systems.processes import Fermentation

# Create a fermentation system with 95% efficiency
fermenter = Fermentation(efficiency=0.95)

# Define inputs (mass in kg)
inputs = {
    "ethanol": 0,      # Starting with no ethanol
    "water": 100,      # 100 kg of water
    "sugar": 50,       # 50 kg of sugar
    "fiber": 10        # 10 kg of fiber
}

# Process the inputs
result = fermenter.processMass(
    inputs=inputs,
    input_type="amount",
    output_type="full",
    store_outputs=False
)

# Display results
print(f"Ethanol produced: {result['amount']['ethanol']:.2f} kg")
print(f"Sugar remaining: {result['amount']['sugar']:.2f} kg")
print(f"Ethanol purity: {result['composition']['ethanol']:.2%}")
```

### Understanding Input/Output Types

The system supports three format types:

#### 1. Amount (Absolute Quantities)
```python
# Input as absolute amounts
inputs = {"ethanol": 10, "water": 50, "sugar": 20, "fiber": 5}

result = fermenter.processMass(
    inputs=inputs,
    input_type="amount",
    output_type="amount"
)
# Returns: {"ethanol": 19.95, "water": 50.0, "sugar": 1.0, "fiber": 5.0}
```

#### 2. Composition (Fractional)
```python
# Input as fractions (must sum to 1.0)
inputs = {"ethanol": 0.1, "water": 0.5, "sugar": 0.3, "fiber": 0.1}

result = fermenter.processMass(
    inputs=inputs,
    input_type="composition",
    output_type="composition",
    total_mass=100  # Required for composition input
)
# Returns: {"ethanol": 0.261, "water": 0.654, "sugar": 0.013, "fiber": 0.065}
```

#### 3. Full (Both Amount and Composition)
```python
# Most comprehensive format - v0.4.0 structure
inputs = {
    "amount": {"ethanol": 10, "water": 50, "sugar": 20, "fiber": 5},
    "composition": {"ethanol": 0.118, "water": 0.588, "sugar": 0.235, "fiber": 0.059}
}

result = fermenter.processMass(
    inputs=inputs,
    input_type="full",
    output_type="full"
)
# Returns both amount and composition dictionaries
# Note: composition no longer includes 'total' key
```

### Working with Flow Rates

```python
# Using volumetric flow rates (m³/s)
flow_inputs = {
    "ethanol": 0,
    "water": 0.1,      # 0.1 m³/s
    "sugar": 0.03,
    "fiber": 0.008
}

result = fermenter.processFlow(
    inputs=flow_inputs,
    input_type="amount",
    output_type="full"
)

print(f"Output ethanol flow: {result['amount']['ethanol']:.4f} m³/s")
print(f"Ethanol composition: {result['composition']['ethanol']:.2%}")
```

### Using Connectors (v0.4.0 API)

```python
from systems.connectors import Pipe

# Create a pipe with specific parameters
pipe = Pipe(
    length=10.0,           # 10 meters long
    diameter=0.15,         # 0.15 m diameter
    friction_factor=0.02   # Friction factor
)

# Calculate output flow after energy losses (new kwargs API)
output_flow = pipe.processFlow(
    input_flow=0.1,    # m³/s
    input_mass=100,    # kg/s
    interval=1         # 1 second
)

print(f"Output flow rate: {output_flow:.4f} m³/s")
```

### Complete Pipeline Example

```python
from systems.processes import Fermentation, Filtration, Distillation, Dehydration

# Create all process systems
fermenter = Fermentation(efficiency=0.95)
filter_system = Filtration(efficiency=0.98)
distiller = Distillation(efficiency=0.90)
dehydrator = Dehydration(efficiency=0.99)

# Initial inputs
inputs = {"ethanol": 0, "water": 100, "sugar": 50, "fiber": 10}

# Stage 1: Fermentation
stage1 = fermenter.processMass(
    inputs=inputs,
    input_type="amount",
    output_type="full"
)

# Stage 2: Filtration
stage2 = filter_system.processMass(
    inputs=stage1["amount"],
    input_type="amount",
    output_type="full"
)

# Stage 3: Distillation
stage3 = distiller.processMass(
    inputs=stage2["amount"],
    input_type="amount",
    output_type="full"
)

# Stage 4: Dehydration
final = dehydrator.processMass(
    inputs=stage3["amount"],
    input_type="amount",
    output_type="full"
)

# Results
print("\n=== Final Product ===")
print(f"Ethanol: {final['amount']['ethanol']:.2f} kg")
print(f"Purity: {final['composition']['ethanol']:.2%}")
```

## Logging and Tracking

### Enabling Storage

```python
# Store inputs and outputs for later analysis
result = fermenter.processMass(
    inputs=inputs,
    input_type="amount",
    output_type="full",
    store_inputs=True,    # Log input values
    store_outputs=True    # Log output values
)

# Access logs (v0.4.0 structure)
print("Input total mass:", fermenter.input_log["mass"]["total_mass"])
print("Output ethanol amounts:", fermenter.output_log["mass"]["amount"]["ethanol"])
print("Output compositions:", fermenter.output_log["mass"]["composition"]["ethanol"])
```

### Batch Processing

```python
# Process multiple batches
input_data = {
    "ethanol": [0, 0, 0],
    "water": [100, 120, 90],
    "sugar": [50, 60, 45],
    "fiber": [10, 12, 9]
}

fermenter.iterateMassInputs(
    inputValues=input_data,
    input_type="amount",
    output_type="full"
)

# All results are now in the output log
print("All ethanol outputs:", fermenter.output_log["mass"]["amount"]["ethanol"])
```

## Next Steps

- **[API Reference](api-reference.md)**: Detailed documentation of all methods
- **[Process Systems](process-systems.md)**: In-depth guide to each process
- **[Connector Systems](connector-systems.md)**: Fluid transport components
- **[Examples](examples.md)**: More complex examples and use cases

## Common Issues

### Import Errors
Make sure you've installed the package: `pip install .` or `uv pip install .`

### System Dependencies Missing
Install GTK4 and related libraries (see Prerequisites section)

### ValueError: "total_mass must be provided"
When using `input_type="composition"`, you must provide the `total_mass` parameter

### Composition doesn't sum to 1.0
Ensure all component fractions add up to exactly 1.0 when using composition mode
