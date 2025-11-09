# API Reference

**Version:** 0.6.1

This document provides comprehensive API documentation for all classes and methods in the Ethanol Plant Model.

## 🆕 Documentation Enhancements (v0.6.1)

All methods now include:
- **Complete parameter descriptions** with types, units, and defaults
- **Detailed return value documentation** with types and explanations
- **Exception documentation** for error conditions
- **Enhanced inline comments** explaining complex calculations
- **Physical principles** documented alongside mathematical operations

## Table of Contents

1. [Process Class](#process-class)
2. [Process Implementations](#process-implementations)
3. [Connector Classes](#connector-classes)

---

## Process Class

The `Process` class is the base class for all processing units in the ethanol plant model. It provides comprehensive functionality for tracking mass flow rates, volumetric flow rates, power consumption, and costs.

### Class: `Process`

**Location:** `systems/process.py`

**Description:** Base class for modeling chemical processing systems with comprehensive logging, conversion utilities, and resource tracking.

### Initialization Parameters

```python
Process(
    name: str = "Process",
    efficiency: float = 1.0,
    massFlowFunction: callable = None,
    power_consumption_rate: float = 0,
    power_consumption_unit: str = "kWh/day",
    cost_per_flow: float = 0
)
```

**Parameters:**
- `name` (str): Name of the process
- `efficiency` (float): Process efficiency (0.0 to 1.0)
- `massFlowFunction` (callable): Custom function for processing mass flows
- `power_consumption_rate` (float): Power consumption rate (default: 0)
- `power_consumption_unit` (str): Unit for power consumption. Options:
  - `"kWh/day"` (default): Kilowatt-hours per day
  - `"kWh/hour"` or `"kW"`: Kilowatts
  - `"W"`: Watts
- `cost_per_flow` (float): Cost per unit volumetric flow rate in $/m³/s (default: 0)

**Attributes:**
- `power_log` (dict): Dictionary tracking power consumption with keys:
  - `power_consumption_rate`: List of power rates (W)
  - `energy_consumed`: List of energy consumed in each interval (J)
  - `interval`: List of time intervals (s)
- `input_log` (dict): Logged input data
- `output_log` (dict): Logged output data

#### consumption_log (dict)
Unified tracking of power, energy, and cost consumption:
- `power_consumption_rate` (list): Power consumption at each time step (W)
- `energy_consumed` (list): Energy consumed in each interval (J)
- `interval` (list): Time interval for each measurement (s)
- `cost_per_unit_flow` (list): Cost per unit flow at each time step ($/m³/s)
- `cost_incurred` (list): Cost incurred for processing each flow ($)

### Methods

#### `processMassFlow()`

**Enhanced Documentation (v0.6.1):** Now includes detailed parameter types, units, and comprehensive return value documentation.

```python
def processMassFlow(self, **kwargs)
```

**Description:** Process mass flow rate inputs through the system's transformation function with flexible input/output formats.

**Parameters:**
- `inputs` (dict): Dictionary of input values. Format depends on input_type:
  - `'amount'`: `{component: value}` in kg/s
  - `'composition'`: `{component: fraction}` (dimensionless, 0-1)
  - `'full'`: `{"amount": {...}, "composition": {...}}`
- `input_type` (str, optional): Format of inputs - `'amount'`, `'composition'`, or `'full'`. Default: `'full'`
- `output_type` (str, optional): Format of outputs - `'amount'`, `'composition'`, or `'full'`. Default: `'full'`
- `total_mass` (float, optional): Total input mass flow rate in kg/s. Required when `input_type='composition'`
- `store_inputs` (bool, optional): Whether to log input values. Default: `False`
- `store_outputs` (bool, optional): Whether to log output values. Default: `False`. Can only be `True` when `output_type='full'`
- `store_cost` (bool, optional): Whether to log cost data. Default: `False`

**Returns:**
- `dict`: Processed outputs in the format specified by output_type:
  - `'amount'`: `{component: value}` in kg/s
  - `'composition'`: `{component: fraction}`
  - `'full'`: `{"amount": {...}, "composition": {...}}`

**Raises:**
- `ValueError`: If inputs are invalid or missing required parameters
- `ValueError`: If attempting to `store_outputs` with non-`'full'` output_type

**Example:**
```python
result = processor.processMassFlow(
    inputs={"ethanol": 0, "water": 100, "sugar": 50, "fiber": 10},
    input_type="amount",
    output_type="full",
    store_outputs=True,
    store_cost=True  # Enable cost tracking
)
```

#### `processVolumetricFlow()`

Process volumetric flow rate inputs through the system.

```python
processVolumetricFlow(
    inputs: dict,
    input_type: str = "amount",
    output_type: str = "amount",
    total_flow: float = None,
    store_inputs: bool = False,
    store_outputs: bool = False,
    store_cost: bool = False
) -> dict
```

**Parameters:**
- `inputs` (dict): Input volumetric flows for each component
- `input_type` (str): Format of inputs - "amount", "composition", or "full"
- `output_type` (str): Format of outputs - "amount", "composition", or "full"
- `total_flow` (float): Total volumetric flow rate (required for composition inputs)
- `store_inputs` (bool): Whether to log input values (default: False)
- `store_outputs` (bool): Whether to log output values (default: False)
- `store_cost` (bool): Whether to log cost data (default: False)

**Returns:**
- dict: Processed volumetric flow outputs in the format specified by output_type

**Example:**
```python
result = processor.processVolumetricFlow(
    inputs={"ethanol": 0, "water": 0.1, "sugar": 0.03, "fiber": 0.008},
    input_type="amount",
    output_type="full",
    store_outputs=True,
    store_cost=True  # Enable cost tracking
)
```

#### `processPowerConsumption()`

**Enhanced Documentation (v0.6.1):** Clear explanation of energy calculation from power and time.

```python
def processPowerConsumption(self, **kwargs)
```

**Description:** Calculate energy consumed over a time interval based on power consumption rate.

**Fundamental Relationship:** Energy = Power × Time (E = P × t)

**Parameters:**
- `store_energy` (bool, optional): Whether to log the power and energy data. Default: `False`
- `interval` (float, optional): Time interval in seconds over which to calculate energy. Default: 1 second

**Returns:**
- `float`: Energy consumed over the interval in Joules (J). Note: 1 J = 1 W·s

**Example:**
```python
# Calculate energy for 10-second interval
energy = process.processPowerConsumption(interval=10, store_energy=True)
print(f"Energy consumed: {energy} J")
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

**Enhanced Documentation (v0.6.1):** Detailed explanation of conversion modes and density-based calculations.

```python
def volumetricToMass(self, **kwargs)
```

**Description:** Convert volumetric flow rates to mass flow rates using component-specific densities. Supports both absolute amounts and compositional fractions.

**Conversion Principle:** Uses `mass_flow = volumetric_flow × density`

**Parameters:**
- `inputs` (dict): Dictionary of component volumetric flow rates or fractions. Keys should be component names from `self.components`
- `mode` (str, optional): Conversion mode - either `'amount'` or `'composition'`. Default: `'amount'`
- `total_flow` (float, optional): Total volumetric flow rate in m³/s. Required when `mode='composition'`

**Returns:**
- `dict`: Dictionary of mass flow rates for each component in kg/s. Does not include a 'total' key

**Raises:**
- `ValueError`: If mode is not `'amount'` or `'composition'`
- `ValueError`: If no inputs are provided
- `ValueError`: If `total_flow` is not provided when `mode='composition'`
- `ValueError`: If an unknown component is encountered

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

**Enhanced Documentation (v0.6.1):** Step-by-step explanation of flow rate calculation after power losses.

```python
def processFlow(self, **kwargs)
```

**Description:** Calculate output volumetric flow rate after power losses in the connector.

**Process Steps:**
1. Calculates flow velocity from volumetric flow and cross-sectional area
2. Computes input kinetic power using velocity and mass flow
3. Determines output power after losses using `processPower()`
4. Calculates resulting output volumetric flow rate

**Parameters:**
- `input_volumetric_flow` (float, optional): Input volumetric flow rate in m³/s. Default: 0
- `input_mass_flow` (float, optional): Input mass flow rate in kg/s. Default: 0

**Returns:**
- `float`: Output volumetric flow rate in m³/s after accounting for power losses

**Physical Principle:** Derives from kinetic energy conservation and continuity equation:
- Input power: P_in = (1/2) × m_dot × v²
- Output power: P_out = P_in - P_loss
- Output flow calculated from P_out using inverse kinetic power formula

---

## Code Quality Features (v0.6.1)

### Comprehensive Docstrings
All methods now include:
- **Args section**: Complete parameter documentation with types, units, and defaults
- **Returns section**: Type information and detailed descriptions
- **Raises section**: Exception types and conditions
- **Examples**: Practical usage demonstrations where applicable

### Inline Comments
Enhanced comments explain:
- **Conversion calculations**: Step-by-step mass/volumetric conversions
- **Energy tracking**: Power and energy logging mechanisms
- **Cost calculations**: Economic tracking methods
- **Physical principles**: Engineering equations and their applications

### Type Information
All parameters and returns documented with:
- Python types (dict, float, str, bool, list)
- Units (kg/s, m³/s, W, J, $)
- Dimensionality (mass flow, volumetric flow, composition fractions)

---

## Usage Examples

See [examples.md](examples.md) for comprehensive tutorials and use cases demonstrating these enhanced features.

## Related Documentation

- [Process Systems](process-systems.md) - Detailed process unit documentation
- [Connector Systems](connector-systems.md) - Fluid transport documentation
- [Examples](examples.md) - Practical usage examples

---

*Last updated: Version 0.6.1 - November 2025*
