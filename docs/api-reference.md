# API Reference

Complete reference for all classes and methods in the Ethanol Plant Model (v0.4.0).

## Table of Contents

- [System Base Class](#system-base-class)
- [Process Systems](#process-systems)
- [Connector Classes](#connector-classes)

---

## System Base Class

The `System` class is the foundation for all process systems.

### `System(**kwargs)`

**Parameters:**
- `name` (str): Name of the system (default: "System")
- `efficiency` (float): System efficiency, 0.0 to 1.0 (default: 1.0)
- `massFunction` (callable): Function to process mass inputs (default: None)

**Attributes:**
- `components` (list): `["ethanol", "water", "sugar", "fiber"]`
- `input_log` (dict): Logs of all inputs (v0.4.0 structure)
- `output_log` (dict): Logs of all outputs (v0.4.0 structure)
- `densityWater` (float): 997 kg/m³
- `densityEthanol` (float): 789 kg/m³
- `densitySugar` (float): 1590 kg/m³
- `densityFiber` (float): 1311 kg/m³

**Log Structure (v0.4.0):**
```python
{
    "mass": {
        "total_mass": [],
        "amount": {"ethanol": [], "water": [], "sugar": [], "fiber": []},
        "composition": {"ethanol": [], "water": [], "sugar": [], "fiber": []}
    },
    "flow": {
        "total_flow": [],
        "amount": {"ethanol": [], "water": [], "sugar": [], "fiber": []},
        "composition": {"ethanol": [], "water": [], "sugar": [], "fiber": []}
    }
}
```

Note: Composition dictionaries no longer include a `"total"` key.

---

### `processMass(**kwargs)`

Process mass inputs through the system's mass function.

**Parameters:**
- `inputs` (dict): Input values (format depends on `input_type`)
- `input_type` (str): `"amount"`, `"composition"`, or `"full"` (default: "full")
- `output_type` (str): `"amount"`, `"composition"`, or `"full"` (default: "full")
- `total_mass` (float): Total mass for composition inputs (required if `input_type="composition"`)
- `store_inputs` (bool): Whether to log inputs (default: False)
- `store_outputs` (bool): Whether to log outputs (default: False)

**Returns:**
- If `output_type="amount"`: `dict` with component amounts (no `"total"` key)
- If `output_type="composition"`: `dict` with component fractions (no `"total"` key)
- If `output_type="full"`: `dict` with `"amount"` and `"composition"` keys

**Examples:**
```python
# Amount input and output
result = system.processMass(
    inputs={"ethanol": 10, "water": 50, "sugar": 20, "fiber": 5},
    input_type="amount",
    output_type="amount"
)
# Returns: {"ethanol": ..., "water": ..., "sugar": ..., "fiber": ...}

# Composition input (requires total_mass)
result = system.processMass(
    inputs={"ethanol": 0.1, "water": 0.6, "sugar": 0.2, "fiber": 0.1},
    input_type="composition",
    output_type="composition",
    total_mass=100
)
# Returns: {"ethanol": ..., "water": ..., "sugar": ..., "fiber": ...}

# Full format (v0.4.0 - no 'total' in composition)
result = system.processMass(
    inputs={
        "amount": {"ethanol": 10, "water": 50, "sugar": 20, "fiber": 5},
        "composition": {"ethanol": 0.118, "water": 0.588, "sugar": 0.235, "fiber": 0.059}
    },
    input_type="full",
    output_type="full",
    store_outputs=True
)
# Returns: {"amount": {...}, "composition": {...}}
```

---

### `processFlow(**kwargs)`

Process volumetric flow inputs through the system.

**Parameters:**
- `inputs` (dict): Input flow values (format depends on `input_type`)
- `input_type` (str): `"amount"`, `"composition"`, or `"full"` (default: "full")
- `output_type` (str): `"amount"`, `"composition"`, or `"full"` (default: "full")
- `total_flow` (float): Total flow for composition inputs (required if `input_type="composition"`)
- `store_inputs` (bool): Whether to log inputs (default: False)
- `store_outputs` (bool): Whether to log outputs (default: False)

**Returns:**
- Same format as `processMass()` but with flow rates instead of masses

**Example:**
```python
result = system.processFlow(
    inputs={"ethanol": 0.01, "water": 0.05, "sugar": 0.02, "fiber": 0.005},
    input_type="amount",
    output_type="full"
)
# Returns: {"amount": {...}, "composition": {...}}
```

---

### `flowToMass(**kwargs)`

Convert volumetric flow rates to mass amounts using component densities.

**Parameters:**
- `inputs` (dict): Flow rates for each component
- `mode` (str): `"amount"` or `"composition"` (default: "amount")
- `total_flow` (float): Total flow (required if `mode="composition"`)

**Returns:**
- `dict`: Mass amounts for each component (no `"total"` key)

**Example:**
```python
mass = system.flowToMass(
    inputs={"ethanol": 0.01, "water": 0.05},
    mode="amount"
)
# Returns: {"ethanol": 7.89, "water": 49.85}
```

---

### `massToFlow(**kwargs)`

Convert mass amounts to volumetric flow rates using component densities.

**Parameters:**
- `inputs` (dict): Mass amounts for each component
- `mode` (str): `"amount"` or `"composition"` (default: "amount")
- `total_mass` (float): Total mass (required if `mode="composition"`)

**Returns:**
- `dict`: Flow rates for each component (no `"total"` key)

**Example:**
```python
flow = system.massToFlow(
    inputs={"ethanol": 7.89, "water": 49.85},
    mode="amount"
)
# Returns: {"ethanol": 0.01, "water": 0.05}
```

---

### `iterateMassInputs(inputValues, **kwargs)`

Process multiple sets of mass inputs iteratively.

**Parameters:**
- `inputValues` (dict): Dictionary of component lists
  - For `input_type="amount"`: `{component: [values]}`
  - For `input_type="composition"`: `{component: [fractions]}`
  - For `input_type="full"`: `{"amount": {component: [values]}, "composition": {component: [fractions]}}`
- `input_type` (str): `"amount"`, `"composition"`, or `"full"` (default: "amount")
- `output_type` (str): `"amount"`, `"composition"`, or `"full"` (default: "full")
- `total_mass_list` (list): List of total masses (required if `input_type="composition"`)

**Returns:**
- `dict`: Updated `output_log` with all processed results

**Example:**
```python
results = system.iterateMassInputs(
    inputValues={
        "ethanol": [0, 0, 0],
        "water": [100, 120, 90],
        "sugar": [50, 60, 45],
        "fiber": [10, 12, 9]
    },
    input_type="amount",
    output_type="full"
)
```

---

### `iterateFlowInputs(inputValues, **kwargs)`

Process multiple sets of flow inputs iteratively.

**Parameters:**
- Same as `iterateMassInputs()` but with `total_flow_list` instead of `total_mass_list`

**Returns:**
- `dict`: Updated `output_log` with all processed results

---

### `display(input, output)`

Display a plot of input vs output relationship.

**Parameters:**
- `input` (str): Name of input variable to plot on x-axis
- `output` (str): Name of output variable to plot on y-axis

**Example:**
```python
system.display(input="sugar", output="ethanol")
```

---

## Process Systems

Module: `systems.process` (base class) and `systems.processors` (implementations)

### Base Class: Process

The `Process` class is the foundation for all process systems in the ethanol plant model.

**Location:** `systems/process.py`

```python
from systems.process import Process
```

#### Constructor

```python
Process(**kwargs)
```

---

### Fermentation

**Location:** `systems/processors.py`

```python
from systems.processors import Fermentation
```

Converts sugar to ethanol through fermentation.

**Parameters:**
- `efficiency` (float): Fraction of sugar converted (0.0 to 1.0)

**Process:**
- 51% of converted sugar becomes ethanol (stoichiometric)
- Unconverted sugar remains in output
- Water and fiber pass through unchanged

**Example:**
```python
fermenter = Fermentation(efficiency=0.95)
result = fermenter.processMass(
    inputs={"ethanol": 0, "water": 100, "sugar": 50, "fiber": 10},
    input_type="amount",
    output_type="full"
)
# Ethanol produced: 50 * 0.95 * 0.51 = 24.225 kg
```

---

### Filtration

**Location:** `systems/processors.py`

```python
from systems.processors import Filtration
```

Removes fiber from the mixture.

**Parameters:**
- `efficiency` (float): Fraction of fiber removed (0.0 to 1.0)

**Process:**
- Removes specified fraction of fiber
- All other components pass through unchanged

**Example:**
```python
filter_sys = Filtration(efficiency=0.98)
result = filter_sys.processMass(
    inputs={"ethanol": 24, "water": 100, "sugar": 2, "fiber": 10},
    input_type="amount",
    output_type="full"
)
# Fiber remaining: 10 * (1 - 0.98) = 0.2 kg
```

---

### Distillation

**Location:** `systems/processors.py`

```python
from systems.processors import Distillation
```

Separates ethanol from impurities.

**Parameters:**
- `efficiency` (float): Separation efficiency (0.0 to 1.0)

**Process:**
- All ethanol is retained
- Impurities proportionally reduced based on efficiency
- Lower efficiency = more impurities with ethanol

**Example:**
```python
distiller = Distillation(efficiency=0.90)
result = distiller.processMass(
    inputs={"ethanol": 24, "water": 100, "sugar": 2, "fiber": 0.2},
    input_type="amount",
    output_type="full"
)
# Impurities reduced, ethanol composition increased
```

---

### Dehydration

**Location:** `systems/processors.py`

```python
from systems.processors import Dehydration
```

Removes water from ethanol.

**Parameters:**
- `efficiency` (float): Fraction of water removed (0.0 to 1.0)

**Process:**
- Removes specified fraction of water
- Ethanol, sugar, and fiber pass through unchanged

**Example:**
```python
dehydrator = Dehydration(efficiency=0.99)
result = dehydrator.processMass(
    inputs={"ethanol": 24, "water": 10, "sugar": 0.2, "fiber": 0.02},
    input_type="amount",
    output_type="full"
)
# Water remaining: 10 * (1 - 0.99) = 0.1 kg
```

---

## Connector Classes

### `Connector(**kwargs)`

Base class for fluid transport components (v0.4.0 kwargs API).

**Parameters:**
- `energy_consumed` (callable): Function to calculate energy loss
- `diameter` (float): Inner diameter in meters (default: 0.1)

**Attributes:**
- `cross_sectional_area` (float): Calculated from diameter

---

### `processDensity(**kwargs)`

Calculate fluid density from mass and flow rates.

**Parameters (v0.4.0):**
- `input_flow` (float): Volumetric flow rate in m³/s (default: 0)
- `input_mass` (float): Mass flow rate in kg/s (default: 0)

**Returns:**
- `float`: Density in kg/m³

**Example:**
```python
density = connector.processDensity(
    input_flow=0.1,
    input_mass=100
)
# Returns: 1000.0 kg/m³
```

---

### `processEnergy(**kwargs)`

Calculate output kinetic energy after losses.

**Parameters:**
- `input_energy` (float): Input energy in Joules

**Returns:**
- `float`: Output energy in Joules

**Example:**
```python
energy = connector.processEnergy(
    input_energy=1000
)
# Returns: 900.0 Joules (assuming 10% loss)
```

---

### `processFlow(**kwargs)`

Calculate output flow rate after energy losses.

**Parameters (v0.4.0):**
- `input_flow` (float): Input volumetric flow rate in m³/s (default: 0)
- `input_mass` (float): Input mass flow rate in kg/s (default: 0)
- `interval` (float): Time interval in seconds (default: 1)

**Returns:**
- `float`: Output volumetric flow rate in m³/s

**Example:**
```python
output = connector.processFlow(
    input_flow=0.1,
    input_mass=100,
    interval=1
)
```

---

### `Pipe(**kwargs)`

Straight pipe segment with friction losses (Darcy-Weisbach equation).

**Parameters:**
- `length` (float): Length in meters (default: 1.0)
- `friction_factor` (float): Darcy friction factor (default: 0.02)
- `diameter` (float): Inner diameter in meters (default: 0.1)

**Energy Function:**
```python
energy_loss = mass * (8 * f * L * Q²) / (π² * D⁵)
```

**Example:**
```python
pipe = Pipe(length=10, diameter=0.15, friction_factor=0.02)
output_flow = pipe.processFlow(
    input_flow=0.1,
    input_mass=100,
    interval=1
)
```

---

### `Bend(**kwargs)`

Pipe bend or elbow with direction change losses.

**Parameters:**
- `bend_radius` (float): Radius of curvature in meters (default: 0.5)
- `bend_factor` (float): Efficiency factor, 1.0 = no loss (default: 0.9)
- `diameter` (float): Inner diameter in meters (default: 0.1)

**Energy Function:**
```python
energy_loss = mass * (1 - bend_factor) * v² / 2
```

**Example:**
```python
bend = Bend(bend_radius=0.5, bend_factor=0.9, diameter=0.1)
output_flow = bend.processFlow(
    input_flow=0.1,
    input_mass=100,
    interval=1
)
```

---

### `Valve(**kwargs)`

Flow control valve with adjustable resistance.

**Parameters:**
- `resistance_coefficient` (float): Flow resistance (default: 1.0)
- `diameter` (float): Inner diameter in meters (default: 0.1)

**Energy Function:**
```python
energy_loss = mass * v² * resistance_coefficient / 2
```

**Example:**
```python
valve = Valve(resistance_coefficient=1.5, diameter=0.1)
output_flow = valve.processFlow(
    input_flow=0.1,
    input_mass=100,
    interval=1
)
```

---

## Error Handling

Common errors and their causes:

**`ValueError: "No inputs provided"`**
- Provide non-empty `inputs` dictionary

**`ValueError: "input_type must be either 'amount', 'composition', or 'full'"`**
- Use only valid input/output types

**`ValueError: "total_mass must be provided when input_type is 'composition'"`**
- Include `total_mass` parameter for composition inputs

**`ValueError: "Total output amount must be greater than zero"`**
- Check that mass function produces non-zero outputs

**`ValueError: "Unknown component"`**
- Use only: ethanol, water, sugar, fiber
