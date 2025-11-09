# Troubleshooting Guide

This guide provides troubleshooting tips and solutions for common issues encountered when using the Ethanol Plant Model. If you experience problems, follow these steps to diagnose and resolve them.

## Debugging Tips

### Enable Detailed Logging

```python
# Enable all logging
result = facility.facility_process(
    input_volume_composition=composition,
    input_volumetric_flow=flow,
    interval=3600,
    store_data=True  # Enable comprehensive logging
)

# Inspect each component
for i, component in enumerate(facility.components):
    print(f"\n=== Component {i}: {component.name if hasattr(component, 'name') else type(component).__name__} ===")
    
    if hasattr(component, 'inputs_log'):
        print("Inputs:", component.inputs_log)
    if hasattr(component, 'outputs_log'):
        print("Outputs:", component.outputs_log)
    if hasattr(component, 'consumption_log'):
        print("Power/Energy:", component.consumption_log)
```

### Print Intermediate States

```python
# Monitor flow through facility
def debug_facility_process(facility, **kwargs):
    """Process with detailed debugging output."""
    print("=== Starting Facility Process ===")
    print(f"Input composition: {kwargs.get('input_volume_composition')}")
    print(f"Input flow: {kwargs.get('input_volumetric_flow')} m³/s")
    
    result = facility.facility_process(**kwargs)
    
    print("\n=== Final Results ===")
    print(f"Output composition: {result['mass_flow']['composition']}")
    print(f"Output flow: {result['volumetric_flow']['total_volumetric_flow']} m³/s")
    print(f"Power consumed: {result['total_power_consumed']} W")
    print(f"Net energy: {result['net_power_gained']} J")
    
    return result

# Use debug wrapper
result = debug_facility_process(
    facility,
    input_volume_composition={"water": 0.7, "sugar": 0.3},
    input_volumetric_flow=0.001,
    store_data=True
)
```

### Validate at Each Step

```python
def validate_flow_state(flow_state, step_name):
    """Validate flow state is reasonable."""
    issues = []
    
    # Check for negative values
    for component, amount in flow_state.get('amount', {}).items():
        if amount < 0:
            issues.append(f"{step_name}: Negative {component} amount: {amount}")
    
    # Check composition sums to ~1.0
    comp_sum = sum(flow_state.get('composition', {}).values())
    if not (0.99 <= comp_sum <= 1.01):
        issues.append(f"{step_name}: Composition sum {comp_sum:.3f} != 1.0")
    
    # Check total flow matches sum of amounts
    total = flow_state.get('total_volumetric_flow', 0) or flow_state.get('total_mass_flow', 0)
    amount_sum = sum(flow_state.get('amount', {}).values())
    if abs(total - amount_sum) > 0.001:
        issues.append(f"{step_name}: Total {total} != sum {amount_sum}")
    
    if issues:
        for issue in issues:
            print(f"⚠ {issue}")
        return False
    return True

# Use in processing
result = facility.facility_process(...)
validate_flow_state(result['mass_flow'], "Final output")
```

### Use Assertions for Critical Values

```python
def safe_pump_process(pump, **kwargs):
    """Pump process with assertions."""
    input_flow = kwargs.get('input_volume_flow', 0)
    composition = kwargs.get('input_composition', {})
    
    # Pre-conditions
    assert input_flow > 0, "Input flow must be positive"
    assert 0 < pump.efficiency <= 1, "Efficiency must be in (0, 1]"
    assert sum(composition.values()) > 0, "Composition cannot be all zeros"
    
    # Process
    mass_flow, vol_flow, power = pump.pump_process(**kwargs)
    
    # Post-conditions
    assert vol_flow >= 0, "Output flow cannot be negative"
    assert power >= 0, "Power cannot be negative"
    assert vol_flow >= input_flow, "Output should be >= input for pump"
    
    return mass_flow, vol_flow, power
```

## Performance Profiling

### Timing Individual Components

```python
import time

def profile_facility(facility, **kwargs):
    """Profile each component's execution time."""
    timings = {'pump': 0, 'processes': {}, 'connectors': {}}
    
    # Time pump
    start = time.time()
    # Pump processing happens in facility_process
    # We'll time the full facility process
    result = facility.facility_process(**kwargs)
    total_time = time.time() - start
    
    print(f"Total processing time: {total_time*1000:.2f} ms")
    
    # For detailed profiling, time each component individually
    for i, component in enumerate(facility.components):
        comp_name = component.name if hasattr(component, 'name') else f"{type(component).__name__}_{i}"
        
        if isinstance(component, Process):
            start = time.time()
            # Simulate processing
            _ = component.processVolumetricFlow(
                inputs={"water": 0.7, "sugar": 0.3},
                input_type="composition"
            )
            elapsed = time.time() - start
            timings['processes'][comp_name] = elapsed
            print(f"  {comp_name}: {elapsed*1000:.2f} ms")

profile_facility(facility, input_volume_composition={"water": 0.7, "sugar": 0.3}, input_volumetric_flow=0.001)
```

### Memory Profiling

```python
import sys

def check_memory_usage(facility):
    """Check memory usage of facility components."""
    total_size = sys.getsizeof(facility)
    
    print(f"Facility object: {total_size} bytes")
    
    for i, component in enumerate(facility.components):
        comp_size = sys.getsizeof(component)
        print(f"  Component {i}: {comp_size} bytes")
        
        if hasattr(component, 'outputs_log'):
            log_size = sys.getsizeof(component.outputs_log)
            print(f"    Outputs log: {log_size} bytes")
        
        if hasattr(component, 'consumption_log'):
            log_size = sys.getsizeof(component.consumption_log)
            print(f"    Consumption log: {log_size} bytes")

check_memory_usage(facility)
```

## Getting Help

### Before Asking for Help

1. **Check this troubleshooting guide**
2. **Review the relevant documentation:**
   - [API Reference](api-reference.md)
   - [Examples](examples.md)
   - [Process Systems](process-systems.md)
3. **Search existing issues:** [GitHub Issues](https://github.com/ENGR161-Team1/EthanolPlantModel/issues)
4. **Create a minimal reproducible example**

### Minimal Reproducible Example Template

```python
"""
Describe the issue: [Brief description]

Expected behavior: [What you expect to happen]
Actual behavior: [What actually happens]
Error message (if any): [Full error traceback]
"""

from systems.facility import Facility
from systems.pump import Pump
from systems.processors import Fermentation

# Minimal code that reproduces the issue
pump = Pump(efficiency=0.85)
fermenter = Fermentation(efficiency=0.95)
facility = Facility(pump=pump, components=[fermenter])

result = facility.facility_process(
    input_volume_composition={"water": 0.7, "sugar": 0.3},
    input_volumetric_flow=0.001
)

print(result)  # Issue appears here
```

### Reporting Bugs

When reporting bugs, include:

1. **Version information:**
```python
import systems
print(f"Version: 0.8.0")  # From pyproject.toml
```

2. **System information:**
```python
import platform
print(f"Python: {platform.python_version()}")
print(f"OS: {platform.system()} {platform.release()}")
```

3. **Full error traceback**
4. **Minimal reproducible example**
5. **Expected vs. actual behavior**

### Contact Information

- **GitHub Issues:** https://github.com/ENGR161-Team1/EthanolPlantModel/issues
- **Team Members:** See [README](../README.md#team-members)

## See Also

- [Best Practices](best-practices.md) - Avoid common pitfalls
- [Examples](examples.md) - Working examples
- [API Reference](api-reference.md) - Complete API documentation
- [Getting Started](getting-started.md) - Basic setup and usage