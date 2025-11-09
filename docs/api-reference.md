# API Reference

Complete API documentation for the Ethanol Plant Model.

## Process Class

Base class for all processing systems.

### Constructor

```python
Process(name="Process", efficiency=1.0, massFlowFunction=None, 
        energy_consumption_rate=0, energy_consumption_unit="kWh/day")
```

**Parameters:**
- `name` (str): Name of the process
- `efficiency` (float): Process efficiency (0-1)
- `massFlowFunction` (callable): Function to process mass flow rates
- `energy_consumption_rate` (float): Energy consumption rate
- `energy_consumption_unit` (str): Unit for energy consumption ("kWh/day")

### Core Methods

#### `processMassFlow(**kwargs)`

Process mass flow rate inputs through the system.

**Parameters:**
- `inputs` (dict): Input values (format depends on input_type)
- `input_type` (str): "amount", "composition", or "full"
- `output_type` (str): "amount", "composition", or "full"
- `total_mass_flow` (float): Total mass flow rate (required for composition inputs)
- `store_inputs` (bool): Whether to log inputs (default: False)
- `store_outputs` (bool): Whether to log outputs (default: False)

**Returns:** Dictionary with processed outputs in specified format

**Example:**
```python
result = processor.processMassFlow(
    inputs={"ethanol": 10, "water": 50, "sugar": 20, "fiber": 5},
    input_type="amount",
    output_type="full",
    store_outputs=True
)
```

#### `processVolumetricFlow(**kwargs)`

Process volumetric flow rate inputs through the system.

**Parameters:**
- `inputs` (dict): Input volumetric flow rates
- `input_type` (str): "amount", "composition", or "full"
- `output_type` (str): "amount", "composition", or "full"
- `total_volumetric_flow` (float): Total volumetric flow rate (required for composition)
- `store_inputs` (bool): Whether to log inputs (default: False)
- `store_outputs` (bool): Whether to log outputs (default: False)

**Returns:** Dictionary with processed volumetric flow rates

**Example:**
```python
result = processor.processVolumetricFlow(
    inputs={"water": 0.05, "sugar": 0.01},
    input_type="amount",
    output_type="full"
)
```

#### `processEnergyConsumption(**kwargs)`

Calculate energy consumed over a time interval.

**Parameters:**
- `interval` (float): Time interval in seconds (default: 1)
- `store_energy` (bool): Whether to log energy consumed (default: False)

**Returns:** Energy consumed in Joules

**Example:**
```python
energy = processor.processEnergyConsumption(
    interval=3600,  # 1 hour
    store_energy=True
)
```

### Conversion Methods

#### `volumetricToMass(**kwargs)`

Convert volumetric flow rates to mass flow rates.

**Parameters:**
- `inputs` (dict): Component volumetric flow rates
- `mode` (str): "amount" or "composition"
- `total_volumetric_flow` (float): Required when mode="composition"

**Returns:** Dictionary of mass flow rates

#### `massToVolumetric(**kwargs)`

Convert mass flow rates to volumetric flow rates.

**Parameters:**
- `inputs` (dict): Component mass flow rates
- `mode` (str): "amount" or "composition"
- `total_mass_flow` (float): Required when mode="composition"

**Returns:** Dictionary of volumetric flow rates

### Batch Processing Methods

#### `iterateMassFlowInputs(inputValues, **kwargs)`

Process multiple sets of mass flow rate inputs iteratively.

**Parameters:**
- `inputValues` (dict): Input data arrays
- `input_type` (str): "amount", "composition", or "full"
- `output_type` (str): "amount", "composition", or "full"
- `total_mass_flow_list` (list): List of total mass flow rates (for composition)

**Returns:** Updated output log

**Example:**
```python
batch_data = {
    "ethanol": [0, 0, 0],
    "water": [100, 150, 200],
    "sugar": [50, 75, 100],
    "fiber": [10, 15, 20]
}

output_log = processor.iterateMassFlowInputs(
    inputValues=batch_data,
    input_type="amount",
    output_type="full"
)
```

#### `iterateVolumetricFlowInputs(inputValues, **kwargs)`

Process multiple sets of volumetric flow rate inputs iteratively.

**Parameters:**
- `inputValues` (dict): Input data arrays
- `input_type` (str): "amount", "composition", or "full"
- `output_type` (str): "amount", "composition", or "full"
- `total_volumetric_flow_list` (list): List of total volumetric flow rates

**Returns:** Updated output log

### Attributes

#### Logs

- `input_log` (dict): Stores input history
  - `mass_flow`: Mass flow rate data
    - `total_mass_flow`: Total mass flow rates
    - `amount`: Component amounts
    - `composition`: Component compositions
  - `volumetric_flow`: Volumetric flow rate data
    - `total_volumetric_flow`: Total volumetric flow rates
    - `amount`: Component amounts
    - `composition`: Component compositions

- `output_log` (dict): Stores output history (same structure as input_log)

- `energy_consumed_log` (list): Energy consumption history

#### Constants

- `densityWater`: 997 kg/m³
- `densityEthanol`: 789 kg/m³
- `densitySugar`: 1590 kg/m³
- `densityFiber`: 1311 kg/m³

## Process Implementations

### Fermentation

Converts sugar to ethanol with 51% theoretical yield.

```python
from systems.processors import Fermentation

fermenter = Fermentation(efficiency=0.95)
result = fermenter.processMassFlow(
    inputs={"ethanol": 0, "water": 100, "sugar": 50, "fiber": 10},
    input_type="amount",
    output_type="full"
)
```

### Filtration

Removes fiber from the mixture.

```python
from systems.processors import Filtration

filter = Filtration(efficiency=0.98)
result = filter.processMassFlow(
    inputs={"ethanol": 25, "water": 50, "sugar": 5, "fiber": 10},
    input_type="amount",
    output_type="full"
)
```

### Distillation

Separates ethanol from impurities.

```python
from systems.processors import Distillation

distiller = Distillation(efficiency=0.90)
result = distiller.processMassFlow(
    inputs={"ethanol": 25, "water": 50, "sugar": 2, "fiber": 0.2},
    input_type="amount",
    output_type="full"
)
```

### Dehydration

Removes water from ethanol mixture.

```python
from systems.processors import Dehydration

dehydrator = Dehydration(efficiency=0.95)
result = dehydrator.processMassFlow(
    inputs={"ethanol": 80, "water": 15, "sugar": 0.5, "fiber": 0.1},
    input_type="amount",
    output_type="full"
)
```

## Migration from v0.4.x

### Method Name Changes

| v0.4.x | v0.5.0 |
|--------|--------|
| `processMass()` | `processMassFlow()` |
| `processFlow()` | `processVolumetricFlow()` |
| `iterateMassInputs()` | `iterateMassFlowInputs()` |
| `iterateFlowInputs()` | `iterateVolumetricFlowInputs()` |
| `flowToMass()` | `volumetricToMass()` |
| `massToFlow()` | `massToVolumetric()` |

### Log Structure Changes

- `input_log["mass"]` → `input_log["mass_flow"]`
- `input_log["flow"]` → `input_log["volumetric_flow"]`
- `total_mass` → `total_mass_flow`
- `total_flow` → `total_volumetric_flow`

### Parameter Changes

- `total_mass` → `total_mass_flow`
- `total_flow` → `total_volumetric_flow`
- `total_mass_list` → `total_mass_flow_list`
- `total_flow_list` → `total_volumetric_flow_list`
