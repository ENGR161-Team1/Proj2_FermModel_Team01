# Ethanol Plant Model

## Overview
This project contains a model of an ethanol production plant, developed as part of ENGR-16100 coursework. The model simulates the complete production pipeline from raw materials to high-purity ethanol through mass balance calculations, process efficiency modeling, and fluid transport dynamics.

## Description
The model simulates four key stages of ethanol production:

1. **Fermentation**: Converts sugar into ethanol using a biochemical process
   - Theoretical maximum conversion: 51% of sugar mass to ethanol
   - Configurable efficiency parameter (0.0 to 1.0)
   - Preserves water and fiber content through the process

2. **Filtration**: Removes solid particles and fiber content
   - Efficiency-based fiber removal
   - Passes ethanol, water, and sugar through unchanged

3. **Distillation**: Separates and concentrates ethanol
   - Exploits differences in boiling points
   - Some carry-over of non-ethanol components based on efficiency

4. **Dehydration**: Removes remaining water content
   - Produces high-purity ethanol
   - Efficiency-based water removal

### Fluid Transport Components
The model includes connector components that simulate fluid transport between process stages:

- **Pipe**: Straight pipe segments with friction losses calculated using the Darcy-Weisbach equation
- **Bend**: Pipe bends/elbows with energy losses proportional to flow velocity and bend geometry
- **Valve**: Flow control valves with adjustable resistance coefficients

These connectors handle:
- Mass conservation (no mass loss during transport)
- Energy dissipation due to friction, turbulence, and flow resistance
- Density-based flow calculations

### Mass Balance Tracking
The model tracks four components throughout the process:
- **Ethanol**: Product concentration
- **Water**: Solvent and byproduct
- **Sugar**: Raw material and residual
- **Fiber**: Solid waste material

Each `System` class maintains input and output histories for all components, enabling detailed analysis and visualization of the production process. The system supports both mass-based (kg) and flow-based (m³) calculations with automatic conversions using component densities.

## Features
- Mass and volumetric flow balance calculations for each process stage
- Energy loss calculations for fluid transport (friction, bends, valves)
- Configurable efficiency parameters for realistic simulations
- Flexible input/output formats: amounts, compositions, or full data
- Built-in visualization using Matplotlib
- Iterative processing of multiple input batches
- Component tracking across the entire production pipeline
- Automatic unit conversions between mass and flow

## Dependencies
- Python >= 3.10
- NumPy
- Matplotlib
- PyGObject (GTK4 bindings)

## Installation

### Using pip
```bash
# Clone the repository
git clone https://github.com/ENGR161-Team1/EthanolPlantModel.git
cd EthanolPlantModel

# Install system dependencies (Ubuntu/Debian)
sudo apt install libgirepository2.0-dev libcairo2-dev libgtk-4-dev \
    pkg-config python3-dev python3-gi python3-gi-cairo \
    gir1.2-gtk-4.0 gobject-introspection

# Install Python package
pip install .
```

### Using uv (Faster Alternative)
```bash
# Install uv if you haven't already
curl -LsSf https://astral.sh/uv/install.sh | sh

# Clone the repository
git clone https://github.com/ENGR161-Team1/EthanolPlantModel.git
cd EthanolPlantModel

# Install system dependencies (Ubuntu/Debian)
sudo apt install libgirepository2.0-dev libcairo2-dev libgtk-4-dev \
    pkg-config python3-dev python3-gi python3-gi-cairo \
    gir1.2-gtk-4.0 gobject-introspection

# Install using uv
uv pip install .
```

## Usage

### Basic Example - Single Batch Processing
```python
from systems.processes import Fermentation, Filtration, Distillation, Dehydration

# Initialize systems with efficiency values (0.0 to 1.0)
fermenter = Fermentation(efficiency=0.95)
filter_system = Filtration(efficiency=0.90)
distiller = Distillation(efficiency=0.98)
dehydrator = Dehydration(efficiency=0.99)

# Define input masses (kg)
mass_input = {
    "ethanol": 0,
    "water": 100,
    "sugar": 50,
    "fiber": 10
}

# Process through fermentation
fermented = fermenter.processMass(
    inputs=mass_input,
    input_type="amount",
    output_type="full",
    store_inputs=True,
    store_outputs=True
)

print(f"Ethanol produced: {fermented['amount']['ethanol']:.2f} kg")
print(f"Ethanol composition: {fermented['composition']['ethanol']:.2%}")
```

### Flow-Based Processing
```python
# Define input flows (m³)
flow_input = {
    "ethanol": 0.1,
    "water": 0.5,
    "sugar": 0.05,
    "fiber": 0.02
}

# Process volumetric flow
filtered = filter_system.processFlow(
    inputs=flow_input,
    input_type="amount",
    output_type="full",
    store_inputs=True,
    store_outputs=True
)

print(f"Output flow - Fiber: {filtered['amount']['fiber']:.4f} m³")
print(f"Total output flow: {sum(filtered['amount'].values()):.3f} m³")
```

### Composition-Based Input
```python
# Define input composition (fractions must sum to 1.0)
composition_input = {
    "ethanol": 0.15,
    "water": 0.80,
    "sugar": 0.03,
    "fiber": 0.02
}

# Process with total mass specified
distilled = distiller.processMass(
    inputs=composition_input,
    input_type="composition",
    output_type="full",
    total_mass=100  # 100 kg total
)

print(f"Output composition - Ethanol: {distilled['composition']['ethanol']:.2%}")
```

### Multiple Batch Processing - Mass
```python
# Define multiple batches
mass_batches = {
    "ethanol": [0, 0, 0, 0],
    "water": [100, 120, 90, 110],
    "sugar": [50, 60, 45, 55],
    "fiber": [10, 12, 9, 11]
}

# Process all batches iteratively
fermenter.iterateMassInputs(
    inputValues=mass_batches,
    input_type="amount",
    output_type="full"
)

# Access results from logs
print(f"Input sugars: {fermenter.input_log['mass']['amount']['sugar']}")
print(f"Output ethanols: {fermenter.output_log['mass']['amount']['ethanol']}")
```

### Multiple Batch Processing - Flow with Compositions
```python
# Define composition batches
flow_compositions = {
    "ethanol": [0.813, 0.820, 0.805, 0.815],
    "water": [0.163, 0.155, 0.170, 0.160],
    "sugar": [0.016, 0.017, 0.016, 0.017],
    "fiber": [0.008, 0.008, 0.009, 0.008]
}

total_flows = [1.0, 1.2, 1.1, 1.15]  # m³

# Process all flow batches
dehydrator.iterateFlowInputs(
    inputValues=flow_compositions,
    input_type="composition",
    output_type="full",
    total_flow_list=total_flows
)

print(f"Output water compositions: {dehydrator.output_log['flow']['composition']['water']}")
```

### Using Connectors for Fluid Transport
```python
from systems.connectors import Pipe, Bend, Valve

# Initialize a pipe with specific properties
pipe = Pipe(
    length=10.0,          # 10 meters
    diameter=0.15,        # 15 cm diameter
    friction_factor=0.02  # Darcy friction factor
)

# Calculate energy loss through the pipe
input_energy = 1000  # Joules
input_flow = 0.1     # m³/s
input_mass = 78.9    # kg/s (ethanol at ~789 kg/m³)

output_energy = pipe.pipeEnergyFunction(
    input_flow=input_flow,
    input_mass=input_mass,
    input_energy=input_energy
)

print(f"Energy lost to friction: {input_energy - output_energy:.2f} J")

# Initialize a bend
bend = Bend(
    bend_radius=0.5,    # 50 cm radius
    bend_factor=0.9,    # 90% efficiency (10% energy loss)
    diameter=0.15
)

# Calculate energy loss through the bend
output_energy = bend.bendEnergyFunction(
    input_flow=input_flow,
    input_mass=input_mass,
    input_energy=input_energy
)

# Initialize a valve
valve = Valve(
    resistance_coefficient=1.5,  # Partially closed valve
    diameter=0.15
)

# Calculate energy loss through the valve
output_energy = valve.valveEnergyFunction(
    input_flow=input_flow,
    input_mass=input_mass,
    input_energy=input_energy
)
```

### Complete Pipeline Example with Transport
```python
from systems.processes import Fermentation, Filtration, Distillation, Dehydration
from systems.connectors import Pipe, Bend

# Initialize process systems
fermenter = Fermentation(efficiency=0.95)
filter_system = Filtration(efficiency=0.90)
distiller = Distillation(efficiency=0.98)
dehydrator = Dehydration(efficiency=0.99)

# Initialize connectors
pipe1 = Pipe(length=5.0, diameter=0.1)
bend1 = Bend(bend_radius=0.5, bend_factor=0.9, diameter=0.1)

# Process through pipeline
input_data = {"ethanol": 0, "water": 3000, "sugar": 1000, "fiber": 100}

# Fermentation
result1 = fermenter.processMass(inputs=input_data, input_type="amount", output_type="amount")

# Transport through pipe (energy calculation)
# Note: Connectors handle energy, mass is conserved
pipe_output_mass = pipe1.pipeMassFunction(input_mass=sum(result1.values()))

# Filtration
result2 = filter_system.processMass(inputs=result1, input_type="amount", output_type="amount")

# Transport through bend
bend_output_mass = bend1.bendMassFunction(input_mass=sum(result2.values()))

# Distillation
result3 = distiller.processMass(inputs=result2, input_type="amount", output_type="amount")

# Dehydration
final = dehydrator.processMass(inputs=result3, input_type="amount", output_type="full")

print(f"Final ethanol: {final['amount']['ethanol']:.2f} kg")
print(f"Final purity: {final['composition']['ethanol']:.2%}")
```

## System Components

### System (Base Class)
The base class for all process systems, providing:
- Input/output tracking for mass and flow data
- Conversion between mass and volumetric flow
- Mass function execution via `processMass()` and `processFlow()`
- Batch iteration capabilities with `iterateMassInputs()` and `iterateFlowInputs()`
- Visualization with `display()`

### Process Systems

#### Fermentation
- **Input**: Sugar, water, fiber
- **Output**: Ethanol (51% × sugar × efficiency), unconverted sugar, water, fiber
- **Efficiency effect**: Determines sugar conversion rate

#### Filtration
- **Input**: All components from fermentation
- **Output**: Ethanol, water, sugar pass through; fiber reduced by efficiency
- **Efficiency effect**: Determines fiber removal rate

#### Distillation
- **Input**: All components from filtration
- **Output**: Concentrated ethanol with some carry-over impurities
- **Efficiency effect**: Determines purity of separation

#### Dehydration
- **Input**: All components from distillation
- **Output**: High-purity ethanol with reduced water content
- **Efficiency effect**: Determines water removal rate

### Connector Components

#### Connector (Base Class)
Base class for all fluid transport connectors, providing:
- Density calculation from mass and flow rates
- Configurable diameter and cross-sectional area
- Mass and energy function interfaces

#### Pipe
Represents straight pipe segments with friction losses.
- **Parameters**: length, diameter, friction_factor
- **Energy Loss**: Calculated using Darcy-Weisbach equation
- **Mass**: Conserved (no mass loss)

#### Bend
Represents pipe bends/elbows with direction change losses.
- **Parameters**: bend_radius, bend_factor, diameter
- **Energy Loss**: Based on kinetic energy and bend inefficiency
- **Mass**: Conserved (no mass loss)

#### Valve
Represents flow control valves with resistance.
- **Parameters**: resistance_coefficient, diameter
- **Energy Loss**: Proportional to dynamic pressure and resistance
- **Mass**: Conserved (no mass loss)

## Project Structure
```
EthanolPlantModel/
├── systems/
│   ├── processes.py    # Core process systems
│   └── connectors.py   # Fluid transport connectors
├── LICENSE
├── README.md
└── pyproject.toml
```

## API Reference

### Core Processing Methods

#### `processMass(**kwargs)`
Process mass inputs through the system.

**Arguments:**
- `inputs` (dict): Input values (format depends on `input_type`)
- `input_type` (str): `'amount'`, `'composition'`, or `'full'`
- `output_type` (str): `'amount'`, `'composition'`, or `'full'`
- `total_mass` (float): Total mass (required for composition inputs)
- `store_inputs` (bool): Whether to log inputs
- `store_outputs` (bool): Whether to log outputs

**Returns:** Processed outputs in specified format

#### `processFlow(**kwargs)`
Process volumetric flow inputs through the system.

**Arguments:**
- `inputs` (dict): Input flow values (format depends on `input_type`)
- `input_type` (str): `'amount'`, `'composition'`, or `'full'`
- `output_type` (str): `'amount'`, `'composition'`, or `'full'`
- `total_flow` (float): Total flow rate in m³ (required for composition inputs)
- `store_inputs` (bool): Whether to log inputs
- `store_outputs` (bool): Whether to log outputs

**Returns:** Processed flow outputs in specified format

#### `iterateMassInputs(inputValues, **kwargs)`
Process multiple sets of mass inputs iteratively.

**Arguments:**
- `inputValues` (dict): Component lists (format depends on `input_type`)
- `input_type` (str): `'amount'`, `'composition'`, or `'full'`
- `output_type` (str): `'amount'`, `'composition'`, or `'full'`
- `total_mass_list` (list): List of total masses (required for composition inputs)

**Returns:** Updated output log

#### `iterateFlowInputs(inputValues, **kwargs)`
Process multiple sets of flow inputs iteratively.

**Arguments:**
- `inputValues` (dict): Component flow lists (format depends on `input_type`)
- `input_type` (str): `'amount'`, `'composition'`, or `'full'`
- `output_type` (str): `'amount'`, `'composition'`, or `'full'`
- `total_flow_list` (list): List of total flows (required for composition inputs)

**Returns:** Updated output log

#### `display(input, output)`
Visualize input vs output relationship from stored logs.

**Arguments:**
- `input` (str): Input variable name
- `output` (str): Output variable name

### Conversion Methods

#### `flowToMass(**kwargs)`
Convert volumetric flow to mass.

**Arguments:**
- `inputs` (dict): Flow values
- `mode` (str): `'amount'` or `'composition'`
- `total_flow` (float): Required for composition mode

#### `massToFlow(**kwargs)`
Convert mass to volumetric flow.

**Arguments:**
- `inputs` (dict): Mass values
- `mode` (str): `'amount'` or `'composition'`
- `total_mass` (float): Required for composition mode

### Connector Methods

#### Connector Base Class

##### `processDensity(**kwargs)`
Calculate fluid density from mass and volumetric flow rates.

**Arguments:**
- `input_flow` (float): Volumetric flow rate in m³/s
- `input_mass` (float): Mass flow rate in kg/s

**Returns:** Density in kg/m³

#### Pipe Class

##### `pipeEnergyFunction(**kwargs)`
Calculate energy loss due to friction in a straight pipe.

**Arguments:**
- `input_flow` (float): Volumetric flow rate in m³/s
- `input_mass` (float): Mass flow rate in kg/s
- `input_energy` (float): Input energy in Joules

**Returns:** Output energy after friction losses (Joules)

##### `pipeMassFunction(**kwargs)`
Calculate mass flow through the pipe (conserved).

**Arguments:**
- `input_mass` (float): Input mass flow rate in kg/s

**Returns:** Output mass flow rate in kg/s

#### Bend Class

##### `bendEnergyFunction(**kwargs)`
Calculate energy loss in a pipe bend due to flow direction change.

**Arguments:**
- `input_flow` (float): Volumetric flow rate in m³/s
- `input_mass` (float): Mass flow rate in kg/s
- `input_energy` (float): Input energy in Joules

**Returns:** Output energy after bend losses (Joules)

##### `bendMassFunction(**kwargs)`
Calculate mass flow through the bend (conserved).

**Arguments:**
- `input_mass` (float): Input mass flow rate in kg/s

**Returns:** Output mass flow rate in kg/s

#### Valve Class

##### `valveEnergyFunction(**kwargs)`
Calculate energy loss through a valve.

**Arguments:**
- `input_flow` (float): Volumetric flow rate in m³/s
- `input_mass` (float): Mass flow rate in kg/s
- `input_energy` (float): Input energy in Joules

**Returns:** Output energy after valve losses (Joules)

##### `valveMassFunction(**kwargs)`
Calculate mass flow through the valve (conserved).

**Arguments:**
- `input_mass` (float): Input mass flow rate in kg/s

**Returns:** Output mass flow rate in kg/s

### Process-Specific Methods
- `Fermentation.ferment(input: dict) -> dict`: Execute fermentation mass balance
- `Filtration.filter(input: dict) -> dict`: Execute filtration mass balance
- `Distillation.distill(input: dict) -> dict`: Execute distillation mass balance
- `Dehydration.dehydrate(input: dict) -> dict`: Execute dehydration mass balance

## Contributing
1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Team Members
- **Advay R. Chandra** - chand289@purdue.edu
- **Karley J. Hammond** - hammon88@purdue.edu
- **Samuel M. Razor** - razor@purdue.edu
- **Katherine E. Hampton** - hampto64@purdue.edu

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments
Developed as part of ENGR-16100 coursework at Purdue University.
