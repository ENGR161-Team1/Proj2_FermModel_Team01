# Getting Started

Welcome to the Ethanol Plant Model! This guide will help you install and start using the package.

## Table of Contents

- [Installation](#installation)
- [Quick Start](#quick-start)
- [Basic Concepts](#basic-concepts)
- [Your First Model](#your-first-model)
- [Next Steps](#next-steps)

## Installation

### Prerequisites

- Python >= 3.10
- pip or uv package manager
- System dependencies (for PyGObject)

### System Dependencies

**Ubuntu/Debian:**
```bash
sudo apt install libgirepository2.0-dev libcairo2-dev libgtk-4-dev \
    pkg-config python3-dev python3-gi python3-gi-cairo \
    gir1.2-gtk-4.0 gobject-introspection
```

**Fedora:**
```bash
sudo dnf install cairo-gobject-devel gobject-introspection-devel \
    gtk4-devel python3-devel
```

**macOS:**
```bash
brew install pygobject3 gtk4
```

### Install with pip

```bash
# Clone the repository
git clone https://github.com/ENGR161-Team1/EthanolPlantModel.git
cd EthanolPlantModel

# Install the package
pip install .
```

### Install with uv (Faster)

```bash
# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Clone and install
git clone https://github.com/ENGR161-Team1/EthanolPlantModel.git
cd EthanolPlantModel
uv pip install .
```

### Verify Installation

```python
# Test import
from systems.processors import Fermentation
from systems.pump import Pump
from systems.facility import Facility

print("✓ Installation successful!")
```

## Quick Start

### Example 1: Simple Fermentation

```python
from systems.processors import Fermentation

# Create a fermentation system
fermenter = Fermentation(efficiency=0.95)

# Process sugar solution
result = fermenter.processMassFlow(
    inputs={
        "ethanol": 0,
        "water": 100,    # 100 kg water
        "sugar": 50,     # 50 kg sugar
        "fiber": 10      # 10 kg fiber
    },
    input_type="amount",
    output_type="full"
)

# View results
print(f"Ethanol produced: {result['amount']['ethanol']:.2f} kg")
print(f"Ethanol composition: {result['composition']['ethanol']:.2%}")
```

### Example 2: Complete Facility

```python
from systems.facility import Facility
from systems.pump import Pump
from systems.processors import Fermentation, Distillation

# Create facility components
pump = Pump(efficiency=0.85)
fermenter = Fermentation(efficiency=0.95)
distiller = Distillation(efficiency=0.92)

# Build facility
facility = Facility(
    pump=pump,
    components=[fermenter, distiller]
)

# Process material
result = facility.facility_process(
    input_volume_composition={
        "water": 0.7,
        "sugar": 0.3
    },
    input_volumetric_flow=0.001,  # 1 L/s
    interval=3600  # 1 hour
)

# Analyze results
print(f"Power consumed: {result['total_power_consumed']/1000:.2f} kW")
print(f"Net energy: {result['net_power_gained']/1e6:.2f} MJ")
print(f"Ethanol output: {result['mass_flow']['amount']['ethanol']*3600:.2f} kg/hr")
```

## Basic Concepts

### Flow Representations

The model uses two flow representations:

**1. Mass Flow (kg/s):**
```python
mass_flow = {
    "ethanol": 0.1,   # 0.1 kg/s
    "water": 0.5,     # 0.5 kg/s
    "sugar": 0.2,     # 0.2 kg/s
    "fiber": 0.05     # 0.05 kg/s
}
```

**2. Volumetric Flow (m³/s):**
```python
volumetric_flow = {
    "ethanol": 0.0001,  # 0.1 L/s
    "water": 0.0005,    # 0.5 L/s
    "sugar": 0.0001,    # 0.1 L/s
    "fiber": 0.00003    # 0.03 L/s
}
```

### Component Tracking

The model tracks four components:
- **Ethanol** - Product of fermentation
- **Water** - Solvent and process medium
- **Sugar** - Fermentation feedstock
- **Fiber** - Solid impurities

### Input/Output Modes

**Amount Mode:** Absolute quantities
```python
inputs = {"water": 100, "sugar": 50}  # kg or m³/s
```

**Composition Mode:** Fractions (sum to 1.0)
```python
inputs = {"water": 0.67, "sugar": 0.33}  # fractions
```

**Full Mode:** Both amount and composition
```python
result = {
    "amount": {"water": 100, "sugar": 50},
    "composition": {"water": 0.67, "sugar": 0.33}
}
```

### Efficiency

All processes have configurable efficiency (0-1):
- **1.0** = 100% efficient (theoretical maximum)
- **0.95** = 95% efficient (realistic)
- **< 0.9** = Inefficient process

```python
fermenter = Fermentation(efficiency=0.95)  # 95% efficient
```

## Your First Model

Let's build a complete ethanol production model step by step.

### Step 1: Import Components

```python
from systems.facility import Facility
from systems.pump import Pump
from systems.processors import Fermentation, Filtration, Distillation, Dehydration
from systems.connectors import Pipe
```

### Step 2: Create Components

```python
# Pump
pump = Pump(
    name="Feed Pump",
    efficiency=0.85,
    opening_diameter=0.15  # 15 cm
)

# Processes
fermentation = Fermentation(
    efficiency=0.95,
    power_consumption_rate=50,
    power_consumption_unit="kW"
)

filtration = Filtration(
    efficiency=0.98,
    power_consumption_rate=20,
    power_consumption_unit="kW"
)

distillation = Distillation(
    efficiency=0.92,
    power_consumption_rate=100,
    power_consumption_unit="kW"
)

dehydration = Dehydration(
    efficiency=0.99,
    power_consumption_rate=30,
    power_consumption_unit="kW"
)

# Connectors
pipe1 = Pipe(length=20, diameter=0.1)
pipe2 = Pipe(length=15, diameter=0.1)
pipe3 = Pipe(length=10, diameter=0.1)
```

### Step 3: Build Facility

```python
facility = Facility(
    pump=pump,
    components=[
        fermentation,
        pipe1,
        filtration,
        pipe2,
        distillation,
        pipe3,
        dehydration
    ]
)
```

### Step 4: Process Material

```python
result = facility.facility_process(
    input_volume_composition={
        "water": 0.625,    # 62.5%
        "sugar": 0.3125,   # 31.25%
        "fiber": 0.0625    # 6.25%
    },
    input_volumetric_flow=0.002,  # 2 L/s
    interval=3600,  # 1 hour
    store_data=True
)
```

### Step 5: Analyze Results

```python
# Extract key metrics
ethanol_output_kgh = result['mass_flow']['amount']['ethanol'] * 3600
ethanol_purity = result['mass_flow']['composition']['ethanol']
power_kw = result['total_power_consumed'] / 1000
net_energy_mj = result['net_power_gained'] / 1e6

# Print summary
print("=== Production Summary ===")
print(f"Ethanol Production: {ethanol_output_kgh:.2f} kg/hr")
print(f"Ethanol Purity: {ethanol_purity:.2%}")
print(f"Power Consumed: {power_kw:.2f} kW")
print(f"Net Energy Gain: {net_energy_mj:.2f} MJ")

# Economic analysis
energy_cost = 0.10  # $/kWh
ethanol_price = 2.50  # $/kg

hourly_power_cost = power_kw * energy_cost
hourly_revenue = ethanol_output_kgh * ethanol_price
hourly_profit = hourly_revenue - hourly_power_cost

print("\n=== Economics ===")
print(f"Power Cost: ${hourly_power_cost:.2f}/hr")
print(f"Revenue: ${hourly_revenue:.2f}/hr")
print(f"Profit: ${hourly_profit:.2f}/hr")
```

## Next Steps

### Learn More

- **[Process Systems](process-systems.md)** - Detailed process documentation
- **[Connector Systems](connector-systems.md)** - Fluid transport components
- **[Pump System](pump-system.md)** - Pump modeling
- **[Facility System](facility-system.md)** - System integration
- **[Examples](examples.md)** - More examples and tutorials

### Common Tasks

**Track power consumption:**
```python
power = process.processPowerConsumption(
    store_energy=True,
    interval=3600
)
```

**Batch processing:**
```python
results = process.iterateMassFlowInputs(
    inputValues=[input1, input2, input3]
)
```

**Convert between flow types:**
```python
mass_flow = Process.volumetricToMass(
    inputs=volumetric_flow,
    mode="amount"
)
```

### Get Help

- **[Troubleshooting](troubleshooting.md)** - Common issues
- **[Best Practices](best-practices.md)** - Tips and patterns
- **[API Reference](api-reference.md)** - Complete documentation
- **[GitHub Issues](https://github.com/ENGR161-Team1/EthanolPlantModel/issues)** - Report bugs

## See Also

- [API Reference](api-reference.md) - Complete API documentation
- [Examples](examples.md) - Practical examples
- [Best Practices](best-practices.md) - Recommended patterns
