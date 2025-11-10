# Changelog

All notable changes to the Ethanol Plant Model project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.1] - 2025-11-09

### 🔧 Patch Release - Analysis Improvements

This patch release enhances the decision matrix analysis model with improved testing coverage and data export capabilities.

### Added

- **Comprehensive visualization suite** for decision matrix analysis
  - Multi-panel visualization with 17 charts across 4 analysis categories
  - Build cost analysis by component (pump, fermenter, filtration, distillation, dehydration)
  - Operational cost analysis with diameter and friction factor impacts
  - Power return analysis across all configuration parameters
  - Composite score breakdown for top configurations
- **Enhanced data export capabilities**
  - Full results export to CSV with all configurations and scores
  - Top 10 configurations export for quick reference
  - Summary statistics export with key metrics
  - All exports saved to dedicated `data/` folder
- **Duplicate configuration detection and removal**
  - Automatic deduplication of test configurations
  - Tracking of tested configurations to prevent redundant testing
  - Detailed reporting of duplicates found and removed

### Improved

- **Testing workflow optimization**
  - Progress indicators during extensive testing phases
  - Better flow threshold analysis with comprehensive test ranges
  - More robust error handling during facility testing
- **Results presentation**
  - Enhanced console output formatting with clear section headers
  - Improved top 10 displays across all categories
  - Better visualization of score components and weights

### Fixed

- Duplicate configuration testing that was inflating result counts
- Data folder creation to ensure export paths exist
- Visualization sizing and layout for better readability

### Documentation

- Updated all documentation files to reflect v1.0.1
- Enhanced inline comments in analysis notebook

## [1.0.0] - 2025-11-09

### 🎉 Full Release - Production Ready

This major release marks the completion of the Ethanol Plant Model as a fully functional, production-ready simulation system for ethanol production facilities.

### Highlights

- **Stable API:** All core interfaces finalized and guaranteed backward compatible
- **Complete feature set:** Full simulation capabilities from raw materials to high-purity ethanol
- **Production validated:** Extensively tested across realistic operating conditions
- **Professional documentation:** Comprehensive guides, API reference, and examples

### Core Capabilities

- **Process Modeling:** Complete simulation of Fermentation, Filtration, Distillation, and Dehydration
- **Fluid Dynamics:** Accurate modeling of pumps, pipes, bends, and valves with realistic energy losses
- **Economic Analysis:** Integrated cost tracking and power consumption monitoring
- **Facility Management:** Seamless orchestration of complete process chains
- **Flexible Architecture:** Static methods, configurable parameters, and extensible design

### System Features

- Mass and volumetric flow rate calculations with automatic conversions
- Energy balance tracking with power consumption and generation analysis
- Cost tracking for comprehensive economic analysis
- Configurable efficiency parameters across all process units
- Batch processing capabilities for time-series analysis
- Comprehensive logging systems for data management
- Built-in visualization support

### Quality Assurance

- Validated against industry-standard process models
- Comprehensive error handling and input validation
- Extensive inline documentation and docstrings
- Complete test coverage of core functionality

### Migration Notes

This release maintains full backward compatibility with v0.8.x. No breaking changes.

## [0.8.1] - 2025-11-09

### Added
- **Cost tracking in Facility class:**
  - New `cost` attribute to track total facility cost across all components
  - `add_component()` method now updates facility cost when components are added
  - Cost accumulation from pump, processes, and connectors

- **Cost consumption tracking in facility_process():**
  - New `total_cost_consumed` field returned in facility_process() output
  - Cost calculation for pump operations based on volumetric flow
  - Cost calculation for processes using `cost_per_flow` multiplied by volumetric flow
  - Cost calculation for connectors using fixed cost per connector
  - Enhanced docstring for facility_process() to document cost tracking

### Changed
- **Updated Facility initialization:**
  - Constructor now initializes facility cost from all components and pump
  - Improved cost accumulation tracking throughout the facility

- **Enhanced Process batch processing methods:**
  - Added `store_cost` parameter to `iterateMassFlowInputs()` method
  - Added `store_cost` parameter to `iterateVolumetricFlowInputs()` method
  - Both methods now support cost logging when enabled

### Improved
- **Processor class initialization:**
  - Simplified Fermentation, Filtration, Distillation, and Dehydration class constructors
  - Used `setdefault()` pattern for cleaner default parameter handling
  - Reduced constructor complexity while maintaining all functionality

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

## [0.5.4] - 2025-11-09

### Added
- **Cost tracking integrated into consumption logs:**
  - Added `cost_per_unit_flow` and `cost_incurred` fields to `consumption_log`
  - Cost tracking now integrated alongside power and energy consumption
  - Enhanced logging structure to capture economic metrics

### Changed
- **Refactored consumption tracking:**
  - Enhanced `consumption_log` to include cost data alongside power/energy metrics
  - Updated logging methods to handle cost calculations
  - Improved parameter handling for cost tracking in Process class

### Improved
- **Enhanced documentation:**
  - Added examples for power consumption tracking configuration
  - Updated Process systems documentation with power consumption parameter details
  - Better explanation of consumption tracking capabilities

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

## [0.2.4] - 2025-11-07

### Improved
- **Enhanced documentation:**
  - Updated README.md with clearer explanations of processing methods
  - Added comprehensive examples for mass and flow input processing
  - Improved clarity on single batch vs iterative processing workflows
  - Enhanced feature descriptions with better formatting

## [0.2.3] - 2025-11-07

### Added
- **Batch processing capabilities:**
  - New `iterateMassInputs()` method for processing multiple sets of mass inputs iteratively
  - New `iterateFlowInputs()` method for processing multiple sets of flow inputs iteratively
  - Support for multiple input formats: 'amount', 'composition', or 'full'
  - Automatic storage of all processed results in input/output logs
  - Comprehensive validation of input data structures

### Improved
- **Enhanced data processing workflow:**
  - Methods handle variable-length input arrays automatically
  - Support for total_mass_list when using composition-based inputs
  - Better error handling for mismatched array lengths
  - Improved documentation with detailed parameter descriptions

## [0.2.2] - 2025-11-07

### Changed
- **Refactored input/output log structure:**
  - Removed 'total' from composition dictionaries for cleaner data organization
  - Separated 'total_mass' and 'total_flow' as dedicated fields in logs
  - Enhanced clarity by distinguishing between component amounts/compositions and totals
  - Improved data structure for better analysis and visualization

### Improved
- **Code organization:**
  - Cleaner log structure with separated amount/composition/total tracking
  - Removed redundant total calculations in composition dictionaries
  - Better separation of concerns in data tracking
  - Optimized code for improved readability and maintainability

## [0.2.1] - 2025-11-07

### Fixed
- Fixed object attribute error in System class initialization
- Corrected components list initialization from `self.components = self.components` to proper list: `["ethanol", "water", "sugar", "fiber"]`

### Improved
- Enhanced code documentation with better inline comments
- Consolidated copyright notices in LICENSE file

## [0.2.0] - 2025-11-06

### Added
- **Flow-based processing logic:**
  - New `processFlow()` method for handling volumetric flow rate inputs (m³)
  - Comprehensive flow rate tracking in input/output logs
  - Support for flow-based composition and amount calculations
  - Automatic conversions between mass and flow representations

### Changed
- **Enhanced input/output logging structure:**
  - Added separate 'flow' section to input_log and output_log
  - Parallel tracking for both mass (kg) and flow (m³) representations
  - Unified data structure supporting both mass-based and flow-based calculations
  - Improved log organization with amount/composition separation

### Improved
- **Enhanced project documentation:**
  - Updated README.md with comprehensive project description
  - Added detailed feature list
  - Improved process stage descriptions with technical details
  - Enhanced usage examples for both mass and flow processing
  - Better formatting and organization throughout documentation

## [0.1.0] - 2025-11-05

### Added
- **Visualization capabilities:**
  - New `display()` method in System class for plotting input/output relationships
  - Matplotlib integration with GTK4 backend support
  - Ability to visualize relationships between specific input and output components
  - Enhanced data visualization for process analysis

### Changed
- **Improved GTK4 integration:**
  - Fixed GTK dependency configuration issues
  - Updated pyproject.toml to include proper GTK4 dependencies
  - Better handling of PyGObject integration
  - Removed unnecessary libgirepository1.0-dev requirement from documentation

### Improved
- **Enhanced documentation:**
  - Updated README.md with detailed installation instructions for GTK4
  - Added usage examples demonstrating visualization capabilities
  - Improved descriptions of the four-stage ethanol production process
  - Added testing and contributing guidelines
  - Better organization of installation steps

### Fixed
- Removed debug print statements from processes.py for cleaner output
- Fixed input iteration logic in `iterateInputs()` method
- Improved massFunction reference handling

## [0.0.5] - 2025-11-XX

### Added
- **Batch input processing:**
  - Implemented `iterateInputs()` method for processing multiple input sets
  - Support for iterating through time-series or batch data
  - Automatic output generation for each input set
  - Enhanced input/output logging for batch processing

### Changed
- **Refactored System class initialization:**
  - Removed redundant inputs and outputs parameters
  - Streamlined constructor for better clarity
  - Improved parameter handling in subclasses

### Fixed
- Fixed input processing logic in `iterateInputs()` method
- Corrected massFunction references throughout the codebase
- Removed debugging print statements for production readiness

## [0.0.4] - 2025-11-XX

### Added
- **Dehydration process:**
  - New `Dehydration` class for water removal stage
  - `dehydrate()` method for processing inputs through dehydration
  - Support for efficiency-based water removal calculations
  - Completes the four-stage ethanol production pipeline

### Improved
- **Enhanced project documentation:**
  - Updated README.md with detailed project overview
  - Added comprehensive installation instructions
  - Included usage examples for all four process stages
  - Improved project metadata in pyproject.toml

## [0.0.3] - 2025-11-XX

### Added
- **Distillation process:**
  - New `Distillation` class for ethanol-water separation
  - `distill()` method for processing inputs through distillation
  - Efficiency-based separation calculations
  - Input validation for distillation parameters

### Improved
- **Project setup and documentation:**
  - Added comprehensive README.md with project overview
  - Enhanced LICENSE file with proper author attribution
  - Updated author information in pyproject.toml
  - Better project structure documentation

### Fixed
- Fixed project version naming inconsistencies
- Corrected author name formatting in configuration files

## [0.0.2] - 2025-11-XX

### Added
- **Filtration process:**
  - New `Filtration` class for fiber removal
  - `filter()` method for processing inputs through filtration
  - Efficiency-based fiber removal calculations
  - Support for configurable filtration efficiency

### Changed
- **System class improvements:**
  - Refined constructor implementation
  - Better parameter handling
  - Improved internal structure

## [0.0.1] - 2025-11-XX

### Added
- **Core System class:**
  - Base `System` class with mass conversion placeholder
  - Input/output logging structure
  - Component tracking for ethanol, water, sugar, and fiber

- **Fermentation process:**
  - `Fermentation` class as first process implementation
  - `ferment()` method for sugar-to-ethanol conversion
  - Configurable efficiency parameters
  - Stoichiometric calculations based on biochemical conversion

- **Project infrastructure:**
  - Initial project structure with pyproject.toml
  - Basic README.md (initially blank)
  - MIT License file
  - Git repository initialization with .gitignore

### Fixed
- Fixed efficiency calculation errors in Fermentation class
- Removed placeholder comments after implementation

---

**Note:** Dates marked with XX indicate approximate timeframes. See git commit history for exact dates.
