# API Reference

This document provides detailed API documentation for all classes and methods in the Ethanol Plant Model.

## Process Class

The base class for all process systems.

### Initialization Parameters

```python
Process(
    name: str = "Process",
    efficiency: float = 1.0,
    massFlowFunction: callable = None,
    power_consumption_rate: float = 0,
    power_consumption_unit: str = "kWh/day"
)
```

**Parameters:**
- `name` (str): Name identifier for the process
- `efficiency` (float): Process efficiency between 0 and 1 (default: 1.0)
- `massFlowFunction` (callable): Function to transform mass flow inputs to outputs
- `power_consumption_rate` (float): Power consumption rate (default: 0)
- `power_consumption_unit` (str): Unit for power consumption. Options:
  - `"kWh/day"` (default): Kilowatt-hours per day
  - `"kWh/hour"` or `"kW"`: Kilowatts
  - `"W"`: Watts

**Attributes:**
- `power_log` (dict): Dictionary tracking power consumption with keys:
  - `power_consumption_rate`: List of power rates (W)
  - `energy_consumed`: List of energy consumed in each interval (J)
  - `interval`: List of time intervals (s)
- `input_log` (dict): Logged input data
- `output_log` (dict): Logged output data

### Methods

#### `processMassFlow()`

Process mass flow rate inputs through the system.

```python
processMassFlow(
    inputs: dict,
    input_type: str = "amount",
    output_type: str = "amount",
    total_mass_flow: float = None,
    store_inputs: bool = False,
    store_outputs: bool = False
) -> dict
```

**Parameters:**
- `inputs` (dict): Input amounts, compositions, or both
- `input_type` (str): Type of input data
  - `"amount"`: Absolute amounts (kg/s or kg/hr)
  - `"composition"`: Fractional compositions (requires `total_mass_flow`)
  - `"full"`: Both amounts and compositions
- `output_type` (str): Type of output data
  - `"amount"`: Returns only amounts
  - `"composition"`: Returns only compositions
  - `"full"`: Returns both amounts and compositions
- `total_mass_flow` (float): Total mass flow rate (required for composition inputs)
- `store_inputs` (bool): Whether to log inputs (default: False)
- `store_outputs` (bool): Whether to log outputs (default: False)

**Returns:**
- dict: Processed output in the requested format

#### `processVolumetricFlow()`

Process volumetric flow rate inputs through the system.

```python
processVolumetricFlow(
    inputs: dict,
    input_type: str = "amount",
    output_type: str = "amount",
    total_volumetric_flow: float = None,
    store_inputs: bool = False,
    store_outputs: bool = False
) -> dict
```

**Parameters:** Same as `processMassFlow()` but for volumetric flow rates (m³/s or m³/hr)

**Returns:**
- dict: Processed output in the requested format

#### `processPowerConsumption()`

Calculate energy consumed over a time interval based on power consumption rate.

```python
processPowerConsumption(
    store_energy: bool = False,
    interval: float = 1
) -> float
```

**Parameters:**
- `store_energy` (bool): Whether to log power and energy data (default: False)
- `interval` (float): Time interval in seconds (default: 1)

**Returns:**
- float: Energy consumed in the interval (Joules)

**Example:**
```python
# Calculate energy over 60 seconds and log it
energy = processor.processPowerConsumption(store_energy=True, interval=60)
print(f"Energy consumed: {energy} J")

# Access logged data
print(f"Power rate: {processor.power_log['power_consumption_rate'][-1]} W")
print(f"Energy: {processor.power_log['energy_consumed'][-1]} J")
print(f"Interval: {processor.power_log['interval'][-1]} s")
```

#### `iterateMassFlowInputs()`

Process multiple sets of mass flow rate inputs in batch.

```python
iterateMassFlowInputs(
    inputValues: dict,
    input_type: str = "amount",
    output_type: str = "amount",
    total_mass_flow_list: list = None
) -> None
```

**Parameters:**
- `inputValues` (dict): Dictionary of component lists
- `input_type` (str): Input data type ("amount", "composition", or "full")
- `output_type` (str): Output data type ("amount", "composition", or "full")
- `total_mass_flow_list` (list): List of total mass flows (for composition inputs)

**Note:** Results are automatically stored in logs

#### `iterateVolumetricFlowInputs()`

Process multiple sets of volumetric flow rate inputs in batch.

```python
iterateVolumetricFlowInputs(
    inputValues: dict,
    input_type: str = "amount",
    output_type: str = "amount",
    total_volumetric_flow_list: list = None
) -> None
```

**Parameters:** Same as `iterateMassFlowInputs()` but for volumetric flow rates

#### `volumetricToMass()`

Convert volumetric flow rates to mass flow rates.

```python
volumetricToMass(
    inputs: dict,
    mode: str = "amount",
    total_flow: float = None
) -> dict
```

#### `massToVolumetric()`

Convert mass flow rates to volumetric flow rates.

```python
massToVolumetric(
    inputs: dict,
    mode: str = "amount",
    total_mass: float = None
) -> dict
```

## Processor Classes

All processor classes inherit from `Process` and accept the same initialization parameters.

### Fermentation

Converts sugar to ethanol (51% stoichiometric yield).

```python
Fermentation(
    efficiency: float = 1.0,
    power_consumption_rate: float = 0,
    power_consumption_unit: str = "kWh/day",
    name: str = "Fermentation"
)
```

**Process:** `sugar → ethanol (51%) + unconverted sugar`

### Filtration

Removes fiber from the mixture.

```python
Filtration(
    efficiency: float = 1.0,
    power_consumption_rate: float = 0,
    power_consumption_unit: str = "kWh/day",
    name: str = "Filtration"
)
```

**Process:** `fiber → removed fiber + remaining fiber`

### Distillation

Separates ethanol from impurities.

```python
Distillation(
    efficiency: float = 1.0,
    power_consumption_rate: float = 0,
    power_consumption_unit: str = "kWh/day",
    name: str = "Distillation"
)
```

**Process:** At perfect efficiency (1.0), outputs pure ethanol. Lower efficiency adds proportional impurities.

### Dehydration

Removes water from the mixture.

```python
Dehydration(
    efficiency: float = 1.0,
    power_consumption_rate: float = 0,
    power_consumption_unit: str = "kWh/day",
    name: str = "Dehydration"
)
```

**Process:** `water → removed water + remaining water`

## Connector Class

Base class for fluid transport components.

### Initialization Parameters

```python
Connector(
    name: str = "Connector",
    length: float = 1.0,
    diameter: float = 0.1,
    roughness: float = 0.0001,
    bend_angle: float = 0,
    bend_radius: float = None,
    resistance_coefficient: float = 0
)
```

### Connector Types

#### Pipe

Straight pipe with friction losses.

```python
Pipe(length: float, diameter: float, roughness: float = 0.0001)
```

#### Bend

Pipe bend with direction change losses.

```python
Bend(
    diameter: float,
    bend_angle: float,
    bend_radius: float = None,
    roughness: float = 0.0001
)
```

#### Valve

Flow control valve with adjustable resistance.

```python
Valve(diameter: float, resistance_coefficient: float)
```

### Methods

#### `processFlow()`

Calculate output flow considering energy losses.

```python
processFlow(inputs: dict, store_inputs: bool = False, store_outputs: bool = False) -> dict
```

**Parameters:**
- `inputs` (dict): Input flow rates and compositions
- `store_inputs` (bool): Whether to log inputs
- `store_outputs` (bool): Whether to log outputs

**Returns:**
- dict: Output flow rates and compositions after energy losses

---

## Complete Example

```python
from systems.processors import Fermentation, Filtration

# Create processes with power consumption
fermenter = Fermentation(
    efficiency=0.95,
    power_consumption_rate=50,  # 50 kWh/day
    power_consumption_unit="kWh/day"
)

filter = Filtration(
    efficiency=0.98,
    power_consumption_rate=2,  # 2 kW
    power_consumption_unit="kW"
)

# Process with logging
result = fermenter.processMassFlow(
    inputs={"ethanol": 0, "water": 100, "sugar": 50, "fiber": 10},
    input_type="amount",
    output_type="full",
    store_outputs=True
)

# Track energy consumption
energy = fermenter.processPowerConsumption(store_energy=True, interval=3600)  # 1 hour
print(f"Energy consumed: {energy/3600000:.2f} kWh")
```
