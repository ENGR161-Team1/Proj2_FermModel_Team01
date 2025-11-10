# API Reference

Complete API documentation for all classes and methods in the Ethanol Plant Model.

## Table of Contents
- [Process Class](#process-class)
- [Processor Classes](#processor-classes)
- [Connector Classes](#connector-classes)
- [Pump Class](#pump-class)
- [Facility Class](#facility-class)

---

## Process Class

Base class for modeling chemical processing systems.

### Class Constants

```python
DENSITY_WATER = 997      # kg/m³
DENSITY_ETHANOL = 789    # kg/m³
DENSITY_SUGAR = 1590     # kg/m³
DENSITY_FIBER = 1311     # kg/m³
```

### `__init__(**kwargs)`

Initialize a Process with configuration parameters.

**Parameters:**
- `name` (str): Descriptive name for this process unit. Default: "Process"
- `efficiency` (float): Process efficiency factor (0-1). Default: 1.0
- `massFlowFunction` (callable): Custom function to transform mass flows. If None, acts as pass-through
- `power_consumption_rate` (float): Power consumption rate. Default: 0
- `power_consumption_unit` (str): Unit for power - "kWh/day", "kW"/"kWh/hour", or "W". Default: "kWh/day"
- `cost` (float): Fixed cost per unit operation (USD). Default: 0
- `cost_per_flow` (float): Variable cost per m³/s of flow (USD). Default: 0

**Example:**
```python
from systems.process import Process

process = Process(
    name="Fermentation Tank",
    efficiency=0.95,
    power_consumption_rate=10,
    power_consumption_unit="kW"
)
```

### `volumetricToMass(**kwargs)` (Static Method)

**NEW in v0.7.0**: Now a static method with flexible output options.

Convert volumetric flow rates to mass flow rates using component densities.

**Parameters:**
- `inputs` (dict): Component volumetric flow rates or fractions
- `mode` (str): 'amount' or 'composition'. Default: 'amount'
- `total_flow` (float): Total volumetric flow (m³/s). Required for 'composition' mode
- `output_type` (str): 'amount', 'composition', or 'full'. Default: 'amount'

**Returns:** dict - Mass flow rates (kg/s) or formatted output per output_type

**Raises:** ValueError - For invalid modes, missing inputs, or unknown components

**Example:**
```python
# Direct conversion (amount to amount)
mass_flows = Process.volumetricToMass(
    inputs={"ethanol": 0.1, "water": 0.2},
    mode="amount"
)

# Composition conversion with full output
result = Process.volumetricToMass(
    inputs={"ethanol": 0.3, "water": 0.7},
    mode="composition",
    total_flow=0.5,
    output_type="full"
)
# Returns: {"amount": {...}, "composition": {...}}
```

### `massToVolumetric(**kwargs)` (Static Method)

**NEW in v0.7.0**: Now a static method with flexible output options.

Convert mass flow rates to volumetric flow rates using component densities.

**Parameters:**
- `inputs` (dict): Component mass flow rates or fractions
- `mode` (str): 'amount' or 'composition'. Default: 'amount'
- `total_mass` (float): Total mass flow (kg/s). Required for 'composition' mode
- `output_type` (str): 'amount', 'composition', or 'full'. Default: 'amount'

**Returns:** dict - Volumetric flow rates (m³/s) or formatted output per output_type

**Raises:** ValueError - For invalid modes, missing inputs, or unknown components

**Example:**
```python
# Direct conversion
volumetric_flows = Process.massToVolumetric(
    inputs={"ethanol": 100, "water": 500},
    mode="amount"
)

# Composition-based conversion
result = Process.massToVolumetric(
    inputs={"ethanol": 0.15, "water": 0.85},
    mode="composition",
    total_mass=1000,
    output_type="composition"
)
```

### `processMassFlow(**kwargs)`

Process mass flow rate inputs through the system's transformation function.

**Parameters:**
- `inputs` (dict): Input values per input_type format
- `input_type` (str): 'amount', 'composition', or 'full'. Default: 'full'
- `output_type` (str): 'amount', 'composition', or 'full'. Default: 'full'
- `total_mass` (float): Total mass flow (kg/s). Required for 'composition' input_type
- `store_inputs` (bool): Whether to log input values. Default: False
- `store_outputs` (bool): Whether to log output values. Default: False (only valid with 'full' output_type)
- `store_cost` (bool): Whether to log cost data. Default: False

**Returns:** dict - Processed outputs in format specified by output_type

**Raises:** ValueError - For invalid inputs or incompatible parameters

**Example:**
```python
# Process with amount input
output = process.processMassFlow(
    inputs={"ethanol": 100, "water": 500, "sugar": 50, "fiber": 10},
    input_type="amount",
    output_type="full",
    store_inputs=True,
    store_outputs=True,
    store_cost=True
)
# Returns: {"amount": {...}, "composition": {...}}
```

### `processVolumetricFlow(**kwargs)`

Process volumetric flow rate inputs through the system.

**Parameters:**
- `inputs` (dict): Component volumetric flow rates per input_type format (m³/s)
- `input_type` (str): 'amount', 'composition', or 'full'. Default: 'full'
- `output_type` (str): 'amount', 'composition', or 'full'. Default: 'full'
- `total_flow` (float): Total volumetric flow (m³/s). Required for 'composition' input_type
- `store_inputs` (bool): Whether to log input values. Default: False
- `store_outputs` (bool): Whether to log output values. Default: False
- `store_cost` (bool): Whether to log cost data. Default: False

**Returns:** dict - Processed volumetric flow outputs in specified format (m³/s)

**Raises:** ValueError - For invalid input_type or missing required parameters

**Example:**
```python
output = process.processVolumetricFlow(
    inputs={
        "amount": {"ethanol": 0.05, "water": 0.25, "sugar": 0.03, "fiber": 0.01},
        "composition": {"ethanol": 0.1, "water": 0.5, "sugar": 0.2, "fiber": 0.2}
    },
    input_type="full",
    output_type="full",
    store_inputs=True,
    store_outputs=True
)
```

### `processPowerConsumption(**kwargs)`

Calculate energy consumed over a time interval based on power consumption rate.

**Parameters:**
- `store_energy` (bool): Whether to log power and energy data. Default: False
- `interval` (float): Time interval in seconds. Default: 1

**Returns:** float - Energy consumed in Joules (J)

**Example:**
```python
# Calculate energy for 1 hour (3600 seconds)
energy = process.processPowerConsumption(
    store_energy=True,
    interval=3600
)
print(f"Energy consumed: {energy} J")
```

### `iterateMassFlowInputs(inputValues=dict(), **kwargs)`

Process multiple sets of mass flow rate inputs iteratively over time.

**Parameters:**
- `inputValues` (dict): Dictionary of input lists per input_type format
- `input_type` (str): 'amount', 'composition', or 'full'. Default: 'amount'
- `output_type` (str): 'amount', 'composition', or 'full'. Default: 'full'
- `total_mass_list` (list): List of total mass flows (kg/s). Required when input_type='composition'

**Returns:** dict - Updated output_log with all processed results

**Raises:** ValueError - For invalid input_type or mismatched total_mass_list

**Example:**
```python
# Batch process time-series data
results = process.iterateMassFlowInputs(
    inputValues={
        "ethanol": [100, 110, 105, 115],
        "water": [500, 520, 510, 530],
        "sugar": [50, 55, 52, 58],
        "fiber": [10, 11, 10, 12]
    },
    input_type="amount",
    output_type="full"
)
```

### `iterateVolumetricFlowInputs(inputValues=dict(), **kwargs)`

Process multiple sets of volumetric flow rate inputs iteratively over time.

**Parameters:**
- `inputValues` (dict): Dictionary of input lists per input_type format (m³/s)
- `input_type` (str): 'amount', 'composition', or 'full'. Default: 'amount'
- `output_type` (str): 'amount', 'composition', or 'full'. Default: 'full'
- `total_flow_list` (list): List of total volumetric flows (m³/s). Required when input_type='composition'

**Returns:** dict - Updated output_log with all processed results

**Raises:** ValueError - For invalid input_type or mismatched total_flow_list

**Example:**
```python
# Process volumetric measurements
results = process.iterateVolumetricFlowInputs(
    inputValues={
        "ethanol": [0.05, 0.055, 0.052, 0.058],
        "water": [0.25, 0.26, 0.255, 0.265],
        "sugar": [0.03, 0.0275, 0.026, 0.029],
        "fiber": [0.005, 0.0055, 0.005, 0.006]
    },
    input_type="amount",
    output_type="full"
)
```

### Logging Structures

#### `input_log`
```python
{
    "mass_flow": {
        "total_mass_flow": [list],
        "amount": {"ethanol": [], "water": [], "sugar": [], "fiber": []},
        "composition": {"ethanol": [], "water": [], "sugar": [], "fiber": []}
    },
    "volumetric_flow": {
        "total_volumetric_flow": [list],
        "amount": {"ethanol": [], "water": [], "sugar": [], "fiber": []},
        "composition": {"ethanol": [], "water": [], "sugar": [], "fiber": []}
    }
}
```

#### `output_log`
Same structure as `input_log`

#### `consumption_log`
```python
{
    "power_consumption_rate": [],  # W
    "energy_consumed": [],         # J
    "interval": [],                # s
    "cost_per_unit_flow": [],      # $/m³/s
    "cost_incurred": []            # $
}
```

---

## Processor Classes

### Fermentation, Filtration, Distillation, Dehydration

All processor classes inherit from `Process` and implement specific stoichiometry and efficiency models.

**NEW in v0.7.0**: All conversion methods are now static and use class constants for densities.

```python
from systems.processors import Fermentation, Filtration, Distillation, Dehydration

fermentation = Fermentation(
    name="Main Fermenter",
    efficiency=0.90,
    power_consumption_rate=15,
    power_consumption_unit="kW"
)
```

---

## Connector Classes

### Connector (Base Class)

Base class for fluid transport components.

### `processDensity(**kwargs)` (Static Method)

**NEW in v0.7.0**: Now a static method.

Calculate fluid density from mass and volumetric flow rates.

**Parameters:**
- `mass_flow` (float): Mass flow rate (kg/s)
- `volumetric_flow` (float): Volumetric flow rate (m³/s)

**Returns:** float - Fluid density (kg/m³)

**Example:**
```python
density = Connector.processDensity(mass_flow=100, volumetric_flow=0.1)
print(f"Fluid density: {density} kg/m³")
```

### Pipe, Bend, Valve

Specialized connector classes with specific energy loss calculations.

```python
from systems.connectors import Pipe, Bend, Valve

pipe = Pipe(
    name="Main Pipeline",
    diameter=0.1,
    length=50,
    friction_factor=0.03,
    power_consumption_rate=5
)

bend = Bend(
    name="Flow Direction Change",
    diameter=0.1,
    bend_angle=90,
    efficiency_factor=0.95,
    power_consumption_rate=2
)

valve = Valve(
    name="Flow Control Valve",
    diameter=0.1,
    resistance_coefficient=0.5,
    power_consumption_rate=1
)
```

---

## Pump Class

### `Pump(**kwargs)`

Models a pump for increasing fluid pressure and velocity.

**Parameters:**
- `name` (str): Pump identifier. Default: "Pump"
- `performance_rating` (float): Pump head rating in meters. Default: 0
- `cost` (float): Cost in USD per m³/s of flow rate. Default: 0
- `efficiency` (float): Pump efficiency as fraction (0-1). Default: 1.0
- `opening_diameter` (float): Inlet/outlet diameter in meters. Default: 0.1

### `pump_process(**kwargs)`

Calculates output flow rates and power consumption based on pump efficiency.

**Parameters:**
- `input_volume_flow` (float): Inlet volumetric flow rate in m³/s
- `input_composition` (dict): Component volume fractions with keys: "ethanol", "water", "sugar", "fiber"

**Returns:**
- `tuple`: (output_mass_flow, output_volumetric_flow, power_consumed)
  - `output_mass_flow` (float): Mass flow rate at outlet in kg/s
  - `output_volumetric_flow` (float): Volumetric flow rate at outlet in m³/s
  - `power_consumed` (float): Mechanical power consumed in Watts

**Example:**
```python
from systems.pump import Pump

pump = Pump(efficiency=0.85, opening_diameter=0.15)
mass_flow, vol_flow, power = pump.pump_process(
    input_volume_flow=0.001,
    input_composition={"water": 0.7, "ethanol": 0.2, "sugar": 0.1}
)
```

---

## Facility Class

### `Facility(**kwargs)`

Orchestrates material flow through multiple processes and connectors with integrated power and cost tracking.

**Parameters:**
- `components` (list): List of Process and Connector instances. Default: []
- `pump` (Pump): Pump instance for the facility. Default: Pump()

**Attributes:**
- `cost` (float): Total facility cost (USD) - sum of all component costs and pump cost

### `add_component(component)`

Adds a process or connector to the facility and updates facility cost.

**Parameters:**
- `component` (Process or Connector): Component to add

**Example:**
```python
facility = Facility()
facility.add_component(Fermentation(efficiency=0.95, cost_per_flow=0.5))
facility.add_component(Pipe(length=10, cost=100))
```

### `facility_process(**kwargs)`

Processes material through all facility components sequentially with power and cost tracking.

**Parameters:**
- `store_data` (bool): Whether to log input/output data. Default: False
- `input_volume_composition` (dict): Component volumetric fractions (0-1)
- `input_volumetric_flow` (float): Total input volumetric flow rate in m³/s
- `interval` (float): Time interval in seconds for energy calculations. Default: 1

**Returns:**
- `dict`: Facility output with keys:
  - `"volumetric_flow"` (dict): Output volumetric flow data
  - `"mass_flow"` (dict): Output mass flow data
  - `"total_power_consumed"` (float): Total power consumed in Watts
  - `"total_cost_consumed"` (float): Total cost consumed in USD
  - `"power_generated"` (float): Energy generated from ethanol in Joules
  - `"net_power_gained"` (float): Net power gain (generated - consumed) in Joules

**Example:**
```python
from systems.facility import Facility
from systems.pump import Pump
from systems.processors import Fermentation

facility = Facility(
    pump=Pump(efficiency=0.85, cost=10),
    components=[Fermentation(efficiency=0.95, cost_per_flow=0.5)]
)

result = facility.facility_process(
    input_volume_composition={"water": 0.625, "sugar": 0.3125, "fiber": 0.0625},
    input_volumetric_flow=0.001,
    interval=1,
    store_data=True
)

print(f"Net power: {result['net_power_gained']:.2f} J")
print(f"Total cost: ${result['total_cost_consumed']:.2f}")
```

---

## Version History

**v1.0.1 - Patch Release:**
- 🔧 Enhanced decision matrix analysis with comprehensive visualizations
- Added duplicate configuration detection and removal
- Improved data export capabilities with dedicated data folder
- Better testing workflow with progress indicators
- Updated all documentation

**v1.0.0 - Full Release:**
- 🎉 Production-ready stable release
- Complete feature set with validated simulation capabilities
- Finalized API with backward compatibility guarantee
- Comprehensive documentation and professional code quality
- Extensive testing and validation
- All systems integrated and production-validated

**v0.8.1 Changes:**
- Added `cost` attribute to Facility class
- `add_component()` now updates facility cost
- `facility_process()` returns `total_cost_consumed` in output
- Cost tracking for pump, processes, and connectors
- Added `store_cost` parameter to batch processing methods

**v0.7.0 Changes:**
- Conversion methods (`volumetricToMass`, `massToVolumetric`, `processDensity`) now static
- Density constants moved to class level
- Added `output_type` parameter for flexible output formatting
- Streamlined docstrings for improved clarity

**Earlier versions:** See [CHANGELOG](../CHANGELOG.md) for complete version history.
