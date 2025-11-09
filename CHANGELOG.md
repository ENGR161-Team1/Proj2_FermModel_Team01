# Changelog

All notable changes to the Ethanol Plant Model project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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

## [0.3.x and earlier]

Earlier versions focused on initial development of the ethanol plant model with basic process systems and connector implementations.

---

**Note:** Dates marked with XX indicate approximate timeframes. See git commit history for exact dates.
