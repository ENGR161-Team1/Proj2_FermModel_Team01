# Ethanol Plant Model

## Overview
This project contains a model of an ethanol production plant, developed as part of ENGR-161 coursework.

## Description
The model simulates various processes involved in ethanol production from raw materials to final product.

## Dependencies
- Python >= 3.10
- NumPy
- Matplotlib

## Installation
```bash
# Clone the repository
git clone https://github.com/ENGR161-Team1/EthanolPlantModel.git
```

## Usage
```python
from systems.processes import Fermentation, Filtration, Distillation

# Initialize systems with efficiency values
fermenter = Fermentation(0.85)
filter = Filtration(0.90)
distiller = Distillation(0.80)

# Process configuration and simulation code goes here
```

## Project Structure
```
EthanolPlantModel/
├── systems/
│   └── processes.py    # Core system components
├── LICENSE
├── README.md
└── pyproject.toml
```

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.