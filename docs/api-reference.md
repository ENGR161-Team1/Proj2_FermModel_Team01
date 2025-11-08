# API Reference

Complete API documentation for the Ethanol Plant Model.

## System (Base Class)

Base class for all process systems. Provides core functionality for mass/flow processing and logging.

### Constructor

```python
System(name="System", efficiency=1.0, massFunction=None)
```

**Parameters:**
- `name` (str): System name for identification
- `efficiency` (float): Process efficiency (0.0 to 1.0)
- `massFunction` (callable): Function to process mass inputs

### Core Methods

#### `processMass(**kwargs)`

Process mass inputs through the system.

**Parameters:**
- `inputs` (dict): Input values
- `input_type` (str): `'amount'`, `'composition'`, or `'full'`
- `output_type` (str): `'amount'`, `'composition'`, or `'full'`
- `total_mass` (float, optional): Total mass for composition inputs
- `store_inputs` (bool): Store in input log (default: False)
- `store_outputs` (bool): Store in output log (default: False)

**Returns:** dict - Processed outputs in specified format

**Example:**
```python
result = system.processMass(
    inputs={"ethanol": 0, "water": 100, "sugar": 50, "fiber": 10},
    input_type="amount",
    output_type="full",
    store_inputs=True,
    store_outputs=True
)
```

---

#### `processFlow(**kwargs)`

Process volumetric flow inputs through the system.

**Parameters:**
- `inputs` (dict): Input flow values
- `input_type` (str): `'amount'`, `'composition'`, or `'full'`
- `output_type` (str): `'amount'`, `'composition'`, or `'full'`
- `total_flow` (float, optional): Total flow for composition inputs
- `store_inputs` (bool): Store in input log (default: False)
- `store_outputs` (bool): Store in output log (default: False)

**Returns:** dict - Processed flow outputs in specified format

**Example:**
```python
result = system.processFlow(
    inputs={"ethanol": 0.1, "water": 0.5, "sugar": 0.05, "fiber": 0.02},
    input_type="amount",
    output_type="full"
)
```

---

#### `iterateMassInputs(inputValues, **kwargs)`

Process multiple sets of mass inputs iteratively.

**Parameters:**
- `inputValues` (dict): Component lists
- `input_type` (str): `'amount'`, `'composition'`, or `'full'`
- `output_type` (str): `'amount'`, `'composition'`, or `'full'`
- `total_mass_list` (list, optional): List of total masses

**Returns:** dict - Updated output log

**Example:**
```python
batches = {
    "ethanol": [0, 0, 0],
    "water": [100, 120, 90],
    "sugar": [50, 60, 45],
    "fiber": [10, 12, 9]
}
system.iterateMassInputs(inputValues=batches, input_type="amount")
```

---

#### `iterateFlowInputs(inputValues, **kwargs)`

Process multiple sets of flow inputs iteratively.

**Parameters:**
- `inputValues` (dict): Component flow lists
- `input_type` (str): `'amount'`, `'composition'`, or `'full'`
- `output_type` (str): `'amount'`, `'composition'`, or `'full'`
- `total_flow_list` (list, optional): List of total flows

**Returns:** dict - Updated output log

---

#### `display(input, output)`

Visualize input vs output relationship.

**Parameters:**
- `input` (str): Input variable name
- `output` (str): Output variable name

**Example:**
```python
system.display(input="sugar", output="ethanol")
```

### Conversion Methods

#### `flowToMass(**kwargs)`

Convert volumetric flow to mass.

**Parameters:**
- `inputs` (dict): Flow values
- `mode` (str): `'amount'` or `'composition'`
- `total_flow` (float, optional): Required for composition mode

**Returns:** dict - Mass values

---

#### `massToFlow(**kwargs)`

Convert mass to volumetric flow.

**Parameters:**
- `inputs` (dict): Mass values
- `mode` (str): `'amount'` or `'composition'`
- `total_mass` (float, optional): Required for composition mode

**Returns:** dict - Flow values

---

## Process Systems

### Fermentation

Converts sugar to ethanol using biochemical process.

```python
Fermentation(efficiency=0.95)
```

**Stoichiometry:** 51% of sugar mass → ethanol

**Process Method:**
```python
ferment(input: dict) -> dict
```

---

### Filtration

Removes solid particles and fiber content.

```python
Filtration(efficiency=0.90)
```

**Process Method:**
```python
filter(input: dict) -> dict
```

---

### Distillation

Separates and concentrates ethanol.

```python
Distillation(efficiency=0.98)
```

**Process Method:**
```python
distill(input: dict) -> dict
```

---

### Dehydration

Removes remaining water content.

```python
Dehydration(efficiency=0.99)
```

**Process Method:**
```python
dehydrate(input: dict) -> dict
```

---

## Connector Systems

### Connector (Base Class)

Base class for fluid transport connectors.

```python
Connector(diameter=0.1)
```

**Methods:**
- `processDensity(inputs)` - Calculate fluid density

---

### Pipe

Straight pipe segment with friction losses.

```python
Pipe(length=10.0, diameter=0.15, friction_factor=0.02)
```

**Parameters:**
- `length` (float): Pipe length in meters
- `diameter` (float): Inner diameter in meters
- `friction_factor` (float): Darcy friction factor

**Methods:**
- `pipeEnergyFunction(input_flow, input_mass, input_energy)` - Calculate energy loss
- `pipeMassFunction(input_mass)` - Calculate mass flow (conserved)

---

### Bend

Pipe bend/elbow with direction change losses.

```python
Bend(bend_radius=0.5, bend_factor=0.9, diameter=0.15)
```

**Parameters:**
- `bend_radius` (float): Radius of curvature in meters
- `bend_factor` (float): Efficiency factor (1.0 = no loss)
- `diameter` (float): Inner diameter in meters

**Methods:**
- `bendEnergyFunction(input_flow, input_mass, input_energy)` - Calculate energy loss
- `bendMassFunction(input_mass)` - Calculate mass flow (conserved)

---

### Valve

Flow control valve with resistance.

```python
Valve(resistance_coefficient=1.5, diameter=0.15)
```

**Parameters:**
- `resistance_coefficient` (float): Flow resistance coefficient
- `diameter` (float): Inner diameter in meters

**Methods:**
- `valveEnergyFunction(input_flow, input_mass, input_energy)` - Calculate energy loss
- `valveMassFunction(input_mass)` - Calculate mass flow (conserved)

---

**Navigation:** [Home](README.md) | [Getting Started](getting-started.md) | [API Reference](api-reference.md) | [Process Systems](process-systems.md) | [Connector Systems](connector-systems.md) | [Examples](examples.md)
