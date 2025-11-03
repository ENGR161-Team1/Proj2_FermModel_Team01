class System:
    def __init__(self, name=str, inputs=list(), outputs=list(), efficiency=float, massFunction=None):
        self.name = name
        self.inputs = inputs
        self.outputs = outputs
        self.efficiency = efficiency
        self.massFunction = massFunction
    
    def convertMass(self):
        pass
        # Placeholder for mass conversion logic
    
    def iterateInputs(self, inputValues=dict()):
        # self.inputs[key].append(inputValues[key]) for key in inputValues
        pass
        # Placeholder for iterating over inputs
    
    def display(self):
        pass
        # Placeholder for display logic

class Fermentation(System):
    def __init__(self, efficiency=float):
        inputs = {
            "ethanol": [],
            "water": [],
            "sugar": [],
            "fiber": []
        }
        outputs = {
            "ethanol": [],
            "water": [],
            "sugar": [],
            "fiber": []
        }
        super().__init__("Fermentation", inputs, outputs, efficiency, self.ferment())
        # Additional initialization for Fermenter can go here

    
    def ferment(self, input=dict()):
        return {
            "ethanol": 0.51 * input["sugar"] * self.efficiency if input.get("sugar") is not None else None, 
            "water": input["water"] if input.get("water") is not None and input.get("sugar") is not None else None,
            "sugar": (1 - self.efficiency) * input["sugar"] if input.get("sugar") is not None else None,
            "fiber": input["fiber"] if input.get("fiber") is not None else None
        }
        # pass
        # Placeholder for fermentation logic
