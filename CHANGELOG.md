# Changelog

All notable changes to the Ethanol Plant Model project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.8.0] - 2025-11-09

### Added
- **Pump class for fluid dynamics:**
  - New `Pump` class in `systems/pump.py` for modeling pumping operations
  - Configurable pump parameters: performance rating, efficiency, cost, and opening diameter
  - `pump_process()` method calculates output flow rates and power consumption
  - Energy balance calculations based on inlet velocity and pump efficiency
  - Cross-sectional area calculations for accurate flow velocity modeling

- **Facility class for system integration:**
  - New `Facility` class in `systems/facility.py` for orchestrating multiple processes
  - Sequential processing through pumps, processes, and connectors
  - Integrated power consumption tracking across all components
  - Energy generation calculations from ethanol production
  - Net power gain analysis (energy generated - energy consumed)
  - Automatic flow state management (volumetric and mass representations)

### Changed
- **Enhanced `processPowerConsumption()` method:**
  - Changed return value from energy consumed to power consumption rate
  - Method now returns instantaneous power in Watts instead of energy in Joules
  - Still logs energy consumed when `store_energy=True` for tracking purposes
  - Updated docstring to clarify power rate vs energy distinction

### Improved
- **Comprehensive system integration:**
  - Facility class seamlessly integrates Process, Connector, and Pump components
  - Automatic conversion between mass and volumetric flow representations
  - Unified power tracking methodology across all system components
  - Enhanced energy balance calculations considering ethanol energy density (28.818 MJ/kg)

## [0.7.0] - 2025-11-09

### Changed
- **Refactored core conversion and utility methods to static methods:**
  - Changed `processDensity()` from instance method to `@staticmethod` for improved clarity
  - Converted `volumetricToMass()` to static method - no longer requires instance state
  - Converted `massToVolumetric()` to static method - no longer requires instance state
  - Updated all internal calls to use `Process.methodName()` for static method invocation

- **Optimized density constant management:**
  - Moved density constants from instance variables (`self.densityWater`, etc.) to class constants (`DENSITY_WATER`, etc.)
  - Density constants now defined at class level for better performance and clarity
  - Constants: `DENSITY_WATER`, `DENSITY_ETHANOL`, `DENSITY_SUGAR`, `DENSITY_FIBER` (all in kg/m³)

- **Enhanced API flexibility with output_type parameter:**
  - Added `output_type` parameter to `volumetricToMass()` and `massToVolumetric()` methods
  - Supports three output formats: 'amount', 'composition', or 'full'
  - 'amount': Returns component amounts only
  - 'composition': Returns normalized component fractions
  - 'full': Returns both amounts and compositions in nested structure

- **Simplified and improved docstrings:**
  - Condensed verbose class and method docstrings for better readability
  - Maintained essential information while removing redundancy
  - Improved parameter descriptions with focus on practical usage
  - Better organization of Args, Returns, and Raises sections

- **Streamlined initialization and internal structure:**
  - Removed redundant comments from `__init__` method
  - Cleaned up log structure initialization
  - Improved power consumption unit conversion logic
  - Removed commented-out code (`# matplotlib.use("gtk4agg")`)

### Improved
- **Code clarity and performance:**
  - Static methods eliminate unnecessary instance state lookups
  - Class constants provide better encapsulation
  - Reduced memory footprint for repeated method calls
  - More consistent with Python best practices

- **Better error handling:**
  - Maintained validation for all input modes
  - Clear error messages for invalid parameters
  - Comprehensive Raises documentation

## [0.6.1] - 2025-11-09

### Improved
- **Comprehensive documentation enhancements:**
  - Added detailed docstrings for all Process class methods with complete parameter descriptions
  - Enhanced Connector class documentation with clear explanations of power loss mechanisms
  - Improved method documentation across all classes with:
    - Type hints and units for all parameters
    - Detailed descriptions of return values
    - Documentation of exceptions and error conditions
    - Clear explanations of method functionality and use cases
  - Added extensive inline comments explaining:
    - Conversion calculations between mass and volumetric flow rates
    - Energy and power consumption tracking mechanisms
    - Cost calculation methods
    - Logging structures and data storage patterns
  - Enhanced code readability with better variable naming and calculation explanations
  - Documented physical principles behind connector power loss calculations (Darcy-Weisbach, bend losses, valve resistance)

## [0.6.0] - 2025-11-09

### Added
- **Cost tracking system:**
  - Added `cost_per_flow` parameter to track cost per unit volumetric flow rate ($/m³/s)
  - New `cost_per_unit_flow` and `cost_incurred` fields in `consumption_log` for tracking costs
  - Cost calculations in both `processMassFlow()` and `processVolumetricFlow()` methods
  - Optional `store_cost` parameter to enable/disable cost logging

### Changed
- **Refactored consumption tracking:**
  - Renamed `power_log` → `consumption_log` to encompass power, energy, and cost tracking
  - Enhanced `consumption_log` dictionary with integrated cost tracking alongside power/energy data
  - Unified tracking structure for all consumption-related metrics (power, energy, cost)

### Improved
- **Enhanced project metadata:**
  - Updated project description with comprehensive feature list
  - Added keywords for better project discoverability
  - Added additional project URLs (Repository, Documentation, Changelog, Issues)
  - Updated license field in pyproject.toml

## [0.5.3] - 2025-11-09

### Added
- **Power consumption tracking system:**
  - Added `power_log` dictionary to track power consumption rate, energy consumed, and time intervals
  - New `processPowerConsumption()` method for calculating energy consumption based on power rate
  - Comprehensive power/energy logging with separate tracking for power (W), energy (J), and intervals (s)

### Changed
- **Refactored energy consumption to power-based model:**
  - Renamed `energy_consumption_rate` → `power_consumption_rate` for accurate physical representation
  - Renamed `energy_consumption_unit` → `power_consumption_unit` (supports "kWh/day", "kWh/hour", "kW", "W")
  - Renamed `processEnergyConsumption()` → `processPowerConsumption()` to reflect instantaneous power calculation
  - Replaced `energy_consumed_log` list with structured `power_log` dictionary containing:
    - `power_consumption_rate`: Power consumption at each time step (W)
    - `energy_consumed`: Energy consumed in each interval (J)
    - `interval`: Time interval for each measurement (s)
  - Enhanced all processor classes (Fermentation, Filtration, Distillation, Dehydration) to accept power consumption parameters in initialization

### Improved
- **Enhanced documentation:**
  - Updated docstrings for all processor classes with detailed parameter descriptions
  - Added comprehensive output descriptions for each process step
  - Improved clarity of stoichiometry and efficiency explanations
  - Better code comments explaining conversion calculations and logging behavior

## [0.5.2] - 2025-11-08

### Changed
- **Refactored Connector class to use power terminology:**
  - Updated parameter names from energy-based to power-based terminology for improved accuracy and clarity
  - Renamed methods and calculations to reflect instantaneous power consumption rather than total energy
  - Better alignment with the physical concepts being modeled (power dissipation in fluid flow systems)
  - This change improves code readability and maintains consistency with engineering terminology

## [0.5.1] - 2025-11-08

### Fixed
- Fixed parameter name in Process class initialization: corrected `massFunction` → `massFlowFunction` in kwargs.get() call to ensure proper initialization of mass flow processing functions
- Fixed Connector energy calculation: removed redundant `self` reference in `processEnergy()` call, correcting method invocation in `processFlow()` method
- Fixed output flow calculation in Connector class: replaced `math.root()` with exponentiation operator `** (1/3)` to improve compatibility and calculation accuracy for cube root operations

## [0.5.0] - 2025-11-08

### Changed - Major API Improvements
- **Renamed methods for clarity:**
  - `processMass()` → `processMassFlow()` - Process mass flow rate inputs
  - `processFlow()` → `processVolumetricFlow()` - Process volumetric flow rate inputs
  - `iterateMassInputs()` → `iterateMassFlowInputs()` - Batch process mass flow rates
  - `iterateFlowInputs()` → `iterateVolumetricFlowInputs()` - Batch process volumetric flow rates
  - `flowToMass()` → `volumetricToMass()` - Convert volumetric to mass flow rates
  - `massToFlow()` → `massToVolumetric()` - Convert mass to volumetric flow rates

- **Updated internal attribute names:**
  - `massFunction` → `massFlowFunction` - Process-specific mass flow rate function
  - Log structure keys updated: `mass` → `mass_flow`, `flow` → `volumetric_flow`
  - `total_mass` → `total_mass_flow`, `total_flow` → `total_volumetric_flow`

### Added
- **Energy consumption tracking:**
  - Added `energy_consumed_log` to track energy usage over time
  - New `processEnergyConsumption()` method for calculating energy consumption
  - Configurable `energy_consumption_rate` with unit conversion support

### Breaking Changes
⚠️ **This version introduces breaking changes to the API.** Code using v0.4.x will need updates:

```python
# Old (v0.4.x)
result = processor.processMass(inputs=data)
processor.iterateMassInputs(inputValues=batch_data)

# New (v0.5.0)
result = processor.processMassFlow(inputs=data)
processor.iterateMassFlowInputs(inputValues=batch_data)
```

## [0.4.2] - 2025-11-08

### Added
- Added `processEnergy` method to Connector class for improved energy calculations
- Enhanced energy loss calculations with better separation of concerns

### Changed
- Refactored `processFlow` to use the new `processEnergy` method for cleaner code organization

### Fixed
- Fixed cube root calculation using `math.root` for accurate flow rate determination

## [0.4.1] - 2025-11-08

### Changed
- Restructured codebase: renamed `System` to `Process` and split into separate files
- `process.py` now contains the base `Process` class
- `processors.py` contains all process implementations (Fermentation, Filtration, Distillation, Dehydration)
- Improved code organization and modularity
- Updated import statements to use relative imports

## [0.4.0] - 2025-11-07

### Changed
- Refactored connector API to use kwargs for improved flexibility
- Enhanced flow calculation using cube root for accurate energy balance
- Improved logging structure with separated amount/composition tracking
- Updated density-based mass/flow conversions for accuracy

### Added
- Comprehensive error handling and input validation

## [0.3.5] - 2025-11-07

### Changed
- **Refactored Connector class architecture:**
  - Removed `mass_function` parameter - mass is now always conserved (no mass loss in connectors)
  - Renamed `energy_function` → `energy_consumed` to better reflect consumption calculation
  - Streamlined initialization to focus on energy consumption modeling

### Added
- **New `processFlow()` method in Connector class:**
  - Calculates output volumetric flow rate after energy losses
  - Uses energy balance to determine flow reduction due to friction/resistance
  - Implements cube root calculation for accurate flow rate determination from energy

### Removed
- **Removed redundant mass functions from all connector classes:**
  - Removed `pipeMassFunction()` - mass conservation is implicit
  - Removed `bendMassFunction()` - mass conservation is implicit
  - Removed `valveMassFunction()` - mass conservation is implicit

### Improved
- **Enhanced energy calculation methods:**
  - `pipeEnergyFunction()` now returns energy consumed (not remaining energy)
  - `bendEnergyFunction()` now returns energy consumed (not remaining energy)
  - `valveEnergyFunction()` now returns energy consumed (not remaining energy)
  - Cleaner separation of concerns between energy dissipation and flow calculation

## [0.3.0] - 2025-11-07

### Added
- **Complete connector system implementation:**
  - Implemented `Bend` class with energy loss calculations for flow direction changes
  - Implemented `Valve` class with resistance-based energy loss modeling
  - Added `pipeMassFunction()`, `bendMassFunction()`, and `valveMassFunction()` to all connector classes
  - Added cross-sectional area calculations for all connectors based on diameter

### Improved
- **Enhanced connector documentation:**
  - Added comprehensive docstrings for all Connector, Pipe, Bend, and Valve classes
  - Documented all methods with detailed parameter descriptions and return types
  - Added clear explanations of physical principles (Darcy-Weisbach equation, bend losses, valve resistance)
  - Included unit specifications for all flow rates and energy calculations

### Changed
- **Refined energy loss calculations:**
  - Updated Pipe energy loss to properly include length parameter in Darcy-Weisbach equation
  - Improved Bend energy loss calculation using kinetic energy and bend efficiency factor
  - Added Valve energy loss calculation based on resistance coefficient and dynamic pressure
  - Standardized flow rate units to m³/s and kg/s across all connector classes

### Fixed
- Fixed `components` initialization in System class (changed from `self.components = self.components` to proper list initialization)

## [0.2.x and earlier]

Earlier versions focused on initial development of the ethanol plant model with basic process systems and connector implementations.

---

**Note:** Dates marked with XX indicate approximate timeframes. See git commit history for exact dates.
