# Process Systems

Detailed documentation for each process system in the ethanol plant model.

## Overview

The model includes four process systems that simulate the ethanol production pipeline:

1. **Fermentation** - Sugar → Ethanol conversion
2. **Filtration** - Fiber removal
3. **Distillation** - Ethanol concentration
4. **Dehydration** - Water removal

Each system tracks four components:
- **Ethanol** (density: 789 kg/m³)
- **Water** (density: 997 kg/m³)
- **Sugar** (density: 1590 kg/m³)
- **Fiber** (density: 1311 kg/m³)

---

## Fermentation

### Description

Converts sugar into ethanol through biochemical fermentation.

### Stoichiometry

```
Sugar → 0.51 × Sugar mass × Efficiency → Ethanol
```

- Theoretical maximum: 51% of sugar mass becomes ethanol
- Actual conversion depends on efficiency parameter

### Inputs

- **Sugar** - Raw material to be converted
- **Water** - Solvent medium
- **Fiber** - Passes through unchanged
- **Ethanol** - Typically 0 for initial fermentation

### Outputs

- **Ethanol** - Product (0.51 × sugar × efficiency)
- **Sugar** - Unconverted sugar (sugar × (1 - efficiency))
- **Water** - Unchanged
- **Fiber** - Unchanged

### Example

```python
from systems.processes import Fermentation

fermenter = Fermentation(efficiency=0.95)

result = fermenter.processMass(
    inputs={"ethanol": 0, "water": 1000, "sugar": 500, "fiber": 50},
    input_type="amount",
    output_type="full"
)

# Expected ethanol: 500 × 0.51 × 0.95 = 242.25 kg
print(f"Ethanol: {result['amount']['ethanol']:.2f} kg")
# Expected remaining sugar: 500 × (1 - 0.95) = 25 kg
print(f"Sugar: {result['amount']['sugar']:.2f} kg")
```

### Efficiency Effect

- **100% efficiency** - All sugar converted (unrealistic)
- **95% efficiency** - 95% of sugar converted (good performance)
- **85% efficiency** - 85% of sugar converted (moderate performance)
- **70% efficiency** - 70% of sugar converted (poor performance)

---

## Filtration

### Description

Removes solid particles and fiber from the mixture.

### Process

Fiber is removed based on efficiency while other components pass through unchanged.

### Inputs

- **Ethanol** - Passes through
- **Water** - Passes through
- **Sugar** - Passes through
- **Fiber** - Partially removed

### Outputs

- **Ethanol** - Unchanged
- **Water** - Unchanged
- **Sugar** - Unchanged
- **Fiber** - Reduced (fiber × (1 - efficiency))

### Example

```python
from systems.processes import Filtration

filter_sys = Filtration(efficiency=0.90)

result = filter_sys.processMass(
    inputs={"ethanol": 242, "water": 1000, "sugar": 25, "fiber": 50},
    input_type="amount",
    output_type="full"
)

# Expected fiber: 50 × (1 - 0.90) = 5 kg
print(f"Fiber removed: {50 - result['amount']['fiber']:.2f} kg")
```

### Efficiency Effect

- **100% efficiency** - All fiber removed (ideal)
- **90% efficiency** - 90% fiber removed (good)
- **80% efficiency** - 80% fiber removed (moderate)
- **60% efficiency** - 60% fiber removed (poor)

---

## Distillation

### Description

Separates and concentrates ethanol from other components by exploiting differences in boiling points.

### Process

Ethanol is separated with some carry-over of impurities based on efficiency.

### Inputs

- **Ethanol** - Product to be concentrated
- **Water** - Impurity to be removed
- **Sugar** - Impurity to be removed
- **Fiber** - Impurity to be removed

### Outputs

- **Ethanol** - Unchanged amount
- **Water** - Reduced (carries over proportionally)
- **Sugar** - Reduced (carries over proportionally)
- **Fiber** - Reduced (carries over proportionally)

### Math

```python
distill_inefficiency = (1 / efficiency) - 1
total_impurities = water + sugar + fiber
water_out = (water × ethanol × distill_inefficiency) / total_impurities
```

### Example

```python
from systems.processes import Distillation

distiller = Distillation(efficiency=0.98)

result = distiller.processMass(
    inputs={"ethanol": 242, "water": 1000, "sugar": 25, "fiber": 5},
    input_type="amount",
    output_type="full"
)

print(f"Ethanol purity: {result['composition']['ethanol']:.2%}")
```

### Efficiency Effect

- **100% efficiency** - Perfect separation (no impurities)
- **98% efficiency** - ~2% impurities remain
- **95% efficiency** - ~5% impurities remain
- **90% efficiency** - ~10% impurities remain

---

## Dehydration

### Description

Final step to remove remaining water content and produce high-purity ethanol.

### Process

Water is removed based on efficiency while other components pass through.

### Inputs

- **Ethanol** - Product
- **Water** - To be removed
- **Sugar** - Passes through
- **Fiber** - Passes through

### Outputs

- **Ethanol** - Unchanged
- **Water** - Reduced (water × (1 - efficiency))
- **Sugar** - Unchanged
- **Fiber** - Unchanged

### Example

```python
from systems.processes import Dehydration

dehydrator = Dehydration(efficiency=0.99)

result = dehydrator.processMass(
    inputs={"ethanol": 242, "water": 50, "sugar": 5, "fiber": 1},
    input_type="amount",
    output_type="full"
)

# Expected water: 50 × (1 - 0.99) = 0.5 kg
print(f"Water remaining: {result['amount']['water']:.2f} kg")
print(f"Final purity: {result['composition']['ethanol']:.2%}")
```

### Efficiency Effect

- **100% efficiency** - All water removed (ideal)
- **99% efficiency** - 99% water removed (excellent)
- **95% efficiency** - 95% water removed (good)
- **90% efficiency** - 90% water removed (moderate)

---

## Complete Pipeline

### Typical Efficiency Values

| Process | Typical Efficiency | Range |
|---------|-------------------|-------|
| Fermentation | 92-96% | 85-98% |
| Filtration | 88-92% | 80-95% |
| Distillation | 96-99% | 92-99.5% |
| Dehydration | 98-99.5% | 95-99.9% |

### Pipeline Example

```python
from systems.processes import Fermentation, Filtration, Distillation, Dehydration

# Initialize with realistic efficiencies
fermenter = Fermentation(efficiency=0.94)
filter_sys = Filtration(efficiency=0.90)
distiller = Distillation(efficiency=0.97)
dehydrator = Dehydration(efficiency=0.99)

# Raw materials
raw = {"ethanol": 0, "water": 5000, "sugar": 2000, "fiber": 200}

# Process pipeline
step1 = fermenter.processMass(inputs=raw, input_type="amount", output_type="amount")
step2 = filter_sys.processMass(inputs=step1, input_type="amount", output_type="amount")
step3 = distiller.processMass(inputs=step2, input_type="amount", output_type="amount")
final = dehydrator.processMass(inputs=step3, input_type="amount", output_type="full")

print(f"Input sugar: 2000 kg")
print(f"Output ethanol: {final['amount']['ethanol']:.2f} kg")
print(f"Conversion efficiency: {(final['amount']['ethanol']/2000)*100:.1f}%")
print(f"Ethanol purity: {final['composition']['ethanol']:.2%}")
```

---

**Navigation:** [Home](README.md) | [Getting Started](getting-started.md) | [API Reference](api-reference.md) | [Process Systems](process-systems.md) | [Connector Systems](connector-systems.md) | [Examples](examples.md)
