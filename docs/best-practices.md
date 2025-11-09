# Best Practices

Guidelines for effective ethanol plant modeling with best practices, optimization strategies, and common patterns.

## Table of Contents

- [Model Design](#model-design)
- [Performance Optimization](#performance-optimization)
- [Data Management](#data-management)
- [Error Handling](#error-handling)
- [Testing & Validation](#testing--validation)
- [Documentation](#documentation)

## Model Design

### Component Organization

**DO:**
```python
# Organize components logically
facility = Facility(
    pump=Pump(efficiency=0.85),
    components=[
        # Pre-processing
        Fermentation(efficiency=0.95),
        Pipe(length=20),
        
        # Purification
        Filtration(efficiency=0.98),
        Pipe(length=15),
        
        # Concentration
        Distillation(efficiency=0.92),
        Pipe(length=10),
        
        # Final purification
        Dehydration(efficiency=0.99)
    ]
)
```

**DON'T:**
```python
# Avoid disorganized component lists
facility = Facility(components=[
    Distillation(),  # Wrong order
    Pump(),          # Pump should be separate parameter
    Fermentation(),
    Pipe()
])
```

### Efficiency Selection

**Use realistic values:**
```python
# Good: Research-based efficiencies
fermentation = Fermentation(efficiency=0.95)  # 95% is realistic
distillation = Distillation(efficiency=0.92)  # 92% is typical
pump = Pump(efficiency=0.85)  # 85% is achievable

# Bad: Unrealistic or default values
fermentation = Fermentation(efficiency=1.0)   # 100% unrealistic
distillation = Distillation(efficiency=0.5)   # 50% too low
pump = Pump()  # Default 1.0 efficiency unrealistic
```

**Efficiency ranges by process:**
- Fermentation: 90-98%
- Filtration: 95-99%
- Distillation: 85-95%
- Dehydration: 95-99.5%
- Pumps: 60-95% (depending on size)

### Unit Consistency

**Always specify units in comments:**
```python
# Good: Clear units
input_flow = 0.001  # m³/s
length = 50  # meters
diameter = 0.1  # meters
power = 50_000  # Watts

# Bad: Ambiguous units
input_flow = 1  # Is this L/s or m³/s?
length = 50  # Feet? Meters?
power = 50  # kW or W?
```

**Use unit conversion consistently:**
```python
# Convert at input
flow_lps = 1.0  # L/s
flow_m3s = flow_lps / 1000  # m³/s

result = facility.facility_process(
    input_volumetric_flow=flow_m3s,  # Always use SI units
    # ...
)

# Convert at output
ethanol_kgs = result['mass_flow']['amount']['ethanol']  # kg/s
ethanol_kgh = ethanol_kgs * 3600  # kg/hr
```

## Performance Optimization

### Minimize Unnecessary Logging

**DO:**
```python
# Only log when needed
result = facility.facility_process(
    input_volume_composition=composition,
    input_volumetric_flow=flow,
    store_data=False  # Default, fastest
)

# Enable logging for debugging only
result = facility.facility_process(
    input_volume_composition=composition,
    input_volumetric_flow=flow,
    store_data=True  # Only when analyzing
)
```

**DON'T:**
```python
# Always logging (slower)
for _ in range(1000):
    result = facility.facility_process(
        input_volume_composition=composition,
        input_volumetric_flow=flow,
        store_data=True  # Unnecessary for all iterations
    )
```

### Batch Processing Efficiently

**Use iteration methods:**
```python
# Good: Use built-in batch processing
inputs = [
    {"water": 0.6, "sugar": 0.3, "fiber": 0.1},
    {"water": 0.65, "sugar": 0.25, "fiber": 0.1},
    {"water": 0.7, "sugar": 0.2, "fiber": 0.1}
]

# Convert to mass flow for batch processing
mass_inputs = [
    Process.volumetricToMass(inp, mode="composition", total_flow=0.001)
    for inp in inputs
]

results = fermentation.iterateMassFlowInputs(
    inputValues=mass_inputs,
    store_outputs=True
)
```

### Reuse Component Instances

**DO:**
```python
# Create once, use many times
pump = Pump(efficiency=0.85)
fermenter = Fermentation(efficiency=0.95)

facility1 = Facility(pump=pump, components=[fermenter])
facility2 = Facility(pump=pump, components=[fermenter])

# Both facilities use same component instances
```

**DON'T:**
```python
# Creating new instances repeatedly (wasteful)
for _ in range(100):
    facility = Facility(
        pump=Pump(efficiency=0.85),  # New instance each time
        components=[Fermentation(efficiency=0.95)]  # New instance
    )
```

## Data Management

### Structured Output Handling

**Good pattern:**
```python
def analyze_facility_output(result):
    """Extract key metrics from facility result."""
    return {
        'ethanol_production_kgh': result['mass_flow']['amount']['ethanol'] * 3600,
        'ethanol_purity': result['mass_flow']['composition']['ethanol'],
        'power_kw': result['total_power_consumed'] / 1000,
        'net_energy_mj': result['net_power_gained'] / 1e6,
        'is_viable': result['net_power_gained'] > 0
    }

result = facility.facility_process(...)
metrics = analyze_facility_output(result)
print(f"Production: {metrics['ethanol_production_kgh']:.2f} kg/hr")
```

### Logging Strategy

**Organize logs systematically:**
```python
import json
from datetime import datetime

# Create structured log
log_entry = {
    'timestamp': datetime.now().isoformat(),
    'inputs': {
        'composition': input_volume_composition,
        'flow_rate': input_volumetric_flow
    },
    'outputs': {
        'ethanol_kgs': result['mass_flow']['amount']['ethanol'],
        'purity': result['mass_flow']['composition']['ethanol'],
        'power_w': result['total_power_consumed']
    },
    'economics': {
        'net_energy_j': result['net_power_gained'],
        'viable': result['net_power_gained'] > 0
    }
}

# Save to file
with open('facility_log.json', 'a') as f:
    json.dump(log_entry, f)
    f.write('\n')
```

## Error Handling

### Input Validation

**Always validate inputs:**
```python
def validate_composition(composition):
    """Validate composition dictionary."""
    valid_components = {'water', 'ethanol', 'sugar', 'fiber'}
    
    # Check keys
    if not set(composition.keys()).issubset(valid_components):
        invalid = set(composition.keys()) - valid_components
        raise ValueError(f"Invalid components: {invalid}")
    
    # Check fractions
    total = sum(composition.values())
    if not (0.99 <= total <= 1.01):  # Allow small numerical errors
        raise ValueError(f"Composition sum {total:.3f} should be ~1.0")
    
    # Check ranges
    for component, fraction in composition.items():
        if not (0 <= fraction <= 1):
            raise ValueError(f"{component} fraction {fraction} out of range [0,1]")
    
    return True

# Use validation
try:
    validate_composition(input_volume_composition)
    result = facility.facility_process(
        input_volume_composition=input_volume_composition,
        input_volumetric_flow=input_volumetric_flow
    )
except ValueError as e:
    print(f"Invalid input: {e}")
```

### Graceful Degradation

**Handle edge cases:**
```python
def safe_facility_process(facility, **kwargs):
    """Process with error handling."""
    try:
        result = facility.facility_process(**kwargs)
        
        # Check for warnings
        if result['net_power_gained'] < 0:
            print("Warning: Negative net energy - facility consuming more than producing")
        
        if result['mass_flow']['composition']['ethanol'] < 0.85:
            print(f"Warning: Low purity {result['mass_flow']['composition']['ethanol']:.1%}")
        
        return result
        
    except ZeroDivisionError:
        print("Error: Division by zero - check input flow rate")
        return None
    except KeyError as e:
        print(f"Error: Missing composition component {e}")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None
```

## Testing & Validation

### Unit Testing

**Test individual components:**
```python
def test_fermentation_stoichiometry():
    """Test fermentation follows expected stoichiometry."""
    fermenter = Fermentation(efficiency=1.0)  # 100% for testing
    
    # Pure sugar input
    result = fermenter.processMassFlow(
        inputs={"sugar": 100, "water": 0, "ethanol": 0, "fiber": 0},
        input_type="amount",
        output_type="amount"
    )
    
    # Check stoichiometry: 1 kg sugar → 0.51 kg ethanol (theoretical)
    expected_ethanol = 100 * 0.51
    actual_ethanol = result['ethanol']
    
    assert abs(actual_ethanol - expected_ethanol) < 0.1, \
        f"Expected {expected_ethanol:.2f} kg ethanol, got {actual_ethanol:.2f}"
    
    print("✓ Stoichiometry test passed")

test_fermentation_stoichiometry()
```

### Integration Testing

**Test component interactions:**
```python
def test_facility_mass_balance():
    """Verify mass is conserved through facility."""
    facility = Facility(
        pump=Pump(efficiency=0.85),
        components=[Fermentation(efficiency=0.95)]
    )
    
    # Input mass
    input_comp = {"water": 0.7, "sugar": 0.3}
    input_flow = 0.001  # m³/s
    
    input_mass_result = Process.volumetricToMass(
        inputs=input_comp,
        mode="composition",
        total_flow=input_flow,
        output_type="full"
    )
    input_total_mass = sum(input_mass_result['amount'].values())
    
    # Output mass
    result = facility.facility_process(
        input_volume_composition=input_comp,
        input_volumetric_flow=input_flow
    )
    output_total_mass = result['mass_flow']['total_mass_flow']
    
    # Allow small difference for fermentation products
    # (sugar converts to ethanol + CO2, but CO2 leaves system)
    assert output_total_mass <= input_total_mass, \
        "Output mass exceeds input (conservation violated)"
    
    print(f"✓ Mass balance: Input={input_total_mass:.4f} kg/s, "
          f"Output={output_total_mass:.4f} kg/s")

test_facility_mass_balance()
```

### Regression Testing

**Track performance over versions:**
```python
import pickle

def save_baseline(result, filename='baseline.pkl'):
    """Save baseline results."""
    baseline = {
        'ethanol_output': result['mass_flow']['amount']['ethanol'],
        'power_consumed': result['total_power_consumed'],
        'net_energy': result['net_power_gained']
    }
    with open(filename, 'wb') as f:
        pickle.dump(baseline, f)

def check_against_baseline(result, filename='baseline.pkl', tolerance=0.01):
    """Compare against baseline."""
    with open(filename, 'rb') as f:
        baseline = pickle.load(f)
    
    for key in baseline:
        current = result[key] if key in result else result['mass_flow']['amount']['ethanol']
        expected = baseline[key]
        diff = abs(current - expected) / expected
        
        if diff > tolerance:
            print(f"⚠ Regression in {key}: {diff*100:.1f}% difference")
        else:
            print(f"✓ {key} within tolerance")
```

## Documentation

### Code Documentation

**Document key parameters:**
```python
def create_production_facility(
    pump_efficiency=0.85,      # Pump hydraulic efficiency (0-1)
    fermentation_eff=0.95,     # Sugar to ethanol conversion (0-1)
    distillation_eff=0.92,     # Ethanol recovery rate (0-1)
    pipe_length_m=100,         # Total pipe length in meters
    pipe_diameter_m=0.1        # Pipe inner diameter in meters
):
    """
    Create a standard ethanol production facility.
    
    Args:
        pump_efficiency: Pump hydraulic efficiency, typical range 0.7-0.95
        fermentation_eff: Fermentation efficiency, typical range 0.90-0.98
        distillation_eff: Distillation efficiency, typical range 0.85-0.95
        pipe_length_m: Total piping length in meters
        pipe_diameter_m: Pipe inner diameter in meters
    
    Returns:
        Facility: Configured production facility
    """
    # Implementation...
```

### Usage Examples in Code

**Include examples:**
```python
"""
Example usage:

>>> facility = create_production_facility(pump_efficiency=0.85)
>>> result = facility.facility_process(
...     input_volume_composition={"water": 0.7, "sugar": 0.3},
...     input_volumetric_flow=0.001
... )
>>> print(f"Ethanol: {result['mass_flow']['amount']['ethanol']:.4f} kg/s")
Ethanol: 0.0001 kg/s
"""
```

## See Also

- [Examples](examples.md) - Practical implementations
- [Troubleshooting](troubleshooting.md) - Common issues
- [API Reference](api-reference.md) - Complete API
