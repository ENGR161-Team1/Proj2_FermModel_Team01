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

class Filtration(System):
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
        super().__init__("Filtration", inputs, outputs, efficiency, self.filter())
        # Additional initialization for Filter can go here

    
    def filter(self, input=dict()):
        return {
            "ethanol": input["ethanol"] if input.get("ethanol") is not None else None, 
            "water": input["water"] if input.get("water") is not None else None,
            "sugar": input["sugar"] if input.get("sugar") is not None else None,
            "fiber": (1 - self.efficiency) * input["fiber"] if input.get("fiber") is not None else None
        }

class Distillation(System):
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
        super().__init__("Distillation", inputs, outputs, efficiency, self.distill())
        # Additional initialization for Distiller can go here

    
    def distill(self, input=dict()):
        if None in [input.get("ethanol"), input.get("water"), input.get("sugar"), input.get("fiber")]:
            return {
                "ethanol": None,
                "water": None,
                "sugar": None,
                "fiber": None
            }
        distill_inefficiency = (1 / self.efficiency) - 1
        in_nonEthanol = input["water"] + input["sugar"] + input["fiber"]
        return {
            "ethanol": input["ethanol"],
            "water": (input["water"] * input["ethanol"] * distill_inefficiency) / in_nonEthanol, 
            "sugar": (input["sugar"] * input["ethanol"] * distill_inefficiency) / in_nonEthanol,
            "fiber": (input["fiber"] * input["ethanol"] * distill_inefficiency) / in_nonEthanol
        }

class Dehydration(System):
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
        super().__init__("Dehydration", inputs, outputs, efficiency, self.dehydrate())
        # Additional initialization for Dehydrator can go here

    
    def dehydrate(self, input=dict()):
        if None in [input.get("ethanol"), input.get("water"), input.get("sugar"), input.get("fiber")]:
            return {
                "ethanol": None,
                "water": None,
                "sugar": None,
                "fiber": None
            }
        return {
            "ethanol": input["ethanol"], 
            "water": input["water"] * (1 - self.efficiency),
            "sugar": input["sugar"],
            "fiber": input["fiber"],
        }