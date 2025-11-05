# Ethanol Plant Model

## Overview
This project contains a model of an ethanol production plant, developed as part of ENGR-161 coursework.

## Description
The model simulates various processes involved in ethanol production from raw materials to final product. It implements four key stages of production:

1. **Fermentation**: Converts sugar into ethanol using a biochemical process, with a theoretical maximum conversion rate of 51% and configurable efficiency.
2. **Filtration**: Removes solid particles and fiber content from the fermented mixture to prepare for distillation.
3. **Distillation**: Separates and concentrates ethanol from the mixture by exploiting differences in boiling points.
4. **Dehydration**: Removes remaining water content to produce high-purity ethanol.

The model tracks mass balances throughout the process, considering the following components:
- Ethanol concentration
- Water content
- Residual sugar
- Fiber content

Each process stage can be configured with different efficiency parameters to simulate real-world conditions and equipment limitations.

## Dependencies
- Python >= 3.10
- NumPy
- Matplotlib
- PyGObject

## Installation

### Using pip
```bash
# Clone the repository
git clone https://github.com/ENGR161-Team1/EthanolPlantModel.git

# Install necessary packages
sudo apt install libgirepository2.0-dev libgirepository1.0-dev libcairo2-dev pkg-config python3-dev python3-gi python3-gi-cairo gir1.2-gtk-4.0 gobject-introspection

# Install using pip
cd EthanolPlantModel
pip install .
```

### Using uv (Faster Alternative)
```bash
# Install uv if you haven't already
curl -LsSf https://astral.sh/uv/install.sh | sh

# Clone the repository
git clone https://github.com/ENGR161-Team1/EthanolPlantModel.git

# Install necessary packages
sudo apt install libgirepository2.0-dev libgirepository1.0-dev libcairo2-dev pkg-config python3-dev python3-gi python3-gi-cairo gir1.2-gtk-4.0 gobject-introspection

# Install using uv
cd EthanolPlantModel
uv pip install .
```

## Usage
```python
from systems.processes import Fermentation, Filtration, Distillation, Dehydration

# Initialize systems with efficiency values
fermenter = Fermentation(0.85)  # 85% conversion efficiency
filter = Filtration(0.90)       # 90% filtering efficiency
distiller = Distillation(0.80)  # 80% distillation efficiency
dehydrator = Dehydration(0.95)  # 95% dehydration efficiency

# Configure input parameters
input_values = {
    "ethanol": [0],     # Initial ethanol content in kg
    "water": [3000],    # Water content in liters/kg
    "sugar": [1000],    # Sugar content in kg
    "fiber": [100]      # Fiber content in kg
}

# Process the materials through each system
fermented = fermenter.iterateInputs(input_values)
filtered = filter.iterateInputs(fermented)
distilled = distiller.iterateInputs(filtered)
dehydrated = dehydrator.iterateInputs(distilled)

# Access the output values
final_ethanol = dehydrated["ethanol"][-1]
final_water = dehydrated["water"][-1]
print(f"Final ethanol: {final_ethanol:.2f} units")
print(f"Remaining water: {final_water:.2f} units")
```

## System Components

### Fermentation
Converts sugar to ethanol with the given efficiency. The theoretical maximum conversion rate is 51% of sugar mass to ethanol.

### Filtration
Removes fiber content from the mixture based on the efficiency rate.

### Distillation
Separates ethanol from the mixture, with some carry-over of other components based on efficiency.

### Dehydration
Removes water from the ethanol mixture to achieve higher purity, based on the given efficiency.

## Project Structure
```
EthanolPlantModel/
├── systems/
│   └── processes.py    # Core system components
├── LICENSE
├── README.md
└── pyproject.toml
```

## Testing
```bash
# Run unit tests
python -m pytest tests/

# Run specific test file
python -m pytest tests/test_fermentation.py
```

## Contributing
1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Contact
- Advay R. Chandra - chand289@purdue.edu
- Karley J. Hammond - hammon88@purdue.edu
- Samuel M. Razor - razor@purdue.edu
- Katherine E. Hampton - hampto64@purdue.edu

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
