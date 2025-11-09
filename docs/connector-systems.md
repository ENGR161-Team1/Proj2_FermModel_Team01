# Connector Systems Guide

Documentation for fluid transport components (pipes, bends, valves) and their energy loss calculations.

## Overview

Connector systems model the transport of fluid through pipes and connections, accounting for energy losses due to friction and resistance. Each connector type handles:
- Volumetric flow rate tracking
- Energy loss calculations based on fluid dynamics
- Power consumption from flow resistance
- Mass conservation (mass in = mass out)

## Core Concepts

### Energy Loss Mechanisms

Connectors lose energy (and thus reduce flow rate) through different mechanisms:

#### 1. Pipe Friction (Darcy-Weisbach)
Energy loss due to friction between fluid and pipe wall:
```
ΔP = f × (L/D) × (ρv²/2)
```

#### 2. Bend Losses (Secondary Flows)
Energy loss in bends due to secondary flows and turbulence:
```
P_loss = (1 - efficiency) × (1/2) × m_dot × v²
```

#### 3. Valve Resistance
Energy loss through valves due to flow resistance:
```
P_loss = K × (1/2) × m_dot × v²
```

Where:
- `ΔP` = Pressure drop (Pa)
- `P_loss` = Power consumed (W)
- `f` = Darcy friction factor (dimensionless)
- `L` = Pipe length (m)
- `D` = Pipe diameter (m)
- `ρ` = Fluid density (kg/m³)
- `v` = Flow velocity (m/s)
- `efficiency` = bend_factor (0 to 1)
- `K` = resistance_coefficient (dimensionless)

## Connector Classes

### Pipe Connector

**Class:** `Pipe`

Models straight pipe sections.

#### Key Parameters
- `length`: Pipe length (m)
- `friction_factor`: Darcy friction factor (dimensionless)
- `diameter`: Inner diameter (m)
- `cost`: Component cost (USD)

#### Core Methods
- `pipePowerFunction()`: Calculates power consumed due to friction using the Darcy-Weisbach equation.

### Bend Connector

**Class:** `Bend`

Models pipe bends.

#### Key Parameters
- `bend_radius`: Radius of curvature (m)
- `bend_factor`: Efficiency factor (0-1)
- `diameter`: Inner diameter (m)
- `cost`: Component cost (USD)

#### Core Methods
- `bendPowerFunction()`: Calculates power consumed in the bend due to flow direction change.

### Valve Connector

**Class:** `Valve`

Models flow control valves.

#### Key Parameters
- `resistance_coefficient`: Flow resistance (dimensionless)
- `diameter`: Inner diameter (m)
- `cost`: Component cost (USD)

#### Core Methods
- `valvePowerFunction()`: Calculates power consumed through the valve due to flow resistance.

## Best Practices

- **Understand physical principles:** Read docstrings and check inline comments for formulas and variable meanings.
- **Verify parameter units:** All parameters are documented with SI units. Conversion factors are provided where needed.
- **Debugging flow calculations:** Enhanced documentation provides detailed inspection steps for troubleshooting.

## Related Documentation

- **[Process Systems](process-systems.md)** - Process unit documentation
- **[API Reference](api-reference.md)** - Complete API with enhanced docstrings
- **[Examples](examples.md)** - Practical examples with improved explanations

*For complete API details with comprehensive docstrings and physics documentation, see [API Reference](api-reference.md)*

*Last updated: Version 0.6.1 - November 2025*
