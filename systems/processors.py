from .process import Process


class Fermentation(Process):
    """
    Models the fermentation process where sugar is converted to ethanol.
    Conversion efficiency determines the fraction of sugar converted.
    """
    
    def __init__(self, efficiency=float):
        super().__init__(name="Fermentation", efficiency=efficiency, massFlowFunction=self.ferment)
        # Additional initialization for Fermenter can go here

    
    def ferment(self, input=dict()):
        """
        Fermentation process: converts sugar to ethanol with specified efficiency.
        Stoichiometry: 51% of sugar mass becomes ethanol.
        """
        return {
            "ethanol": 0.51 * input["sugar"] * self.efficiency if input.get("sugar") is not None else None, 
            "water": input["water"] if input.get("water") is not None and input.get("sugar") is not None else None,
            "sugar": (1 - self.efficiency) * input["sugar"] if input.get("sugar") is not None else None,
            "fiber": input["fiber"] if input.get("fiber") is not None else None
        }
        # pass


class Filtration(Process):
    """
    Models the filtration process where fiber is removed from the mixture.
    Efficiency determines the fraction of fiber that is successfully filtered out.
    """
    
    def __init__(self, efficiency=float):
        super().__init__(name="Filtration", efficiency=efficiency, massFlowFunction=self.filter)
        # Additional initialization for Filter can go here

    
    def filter(self, input=dict()):
        """
        Filtration process: removes fiber from the mixture based on efficiency.
        Other components pass through unchanged.
        """
        return {
            "ethanol": input["ethanol"] if input.get("ethanol") is not None else None, 
            "water": input["water"] if input.get("water") is not None else None,
            "sugar": input["sugar"] if input.get("sugar") is not None else None,
            "fiber": (1 - self.efficiency) * input["fiber"] if input.get("fiber") is not None else None
        }


class Distillation(Process):
    """
    Models the distillation process for separating ethanol from other components.
    Higher efficiency means better separation (less impurities in ethanol output).
    """
    
    def __init__(self, efficiency=float):
        super().__init__(name="Distillation", efficiency=efficiency, massFlowFunction=self.distill)
        # Additional initialization for Distiller can go here

    
    def distill(self, input=dict()):
        """
        Distillation process: separates ethanol from water, sugar, and fiber.
        Inefficiency causes proportional amounts of impurities to remain with ethanol.
        """
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


class Dehydration(Process):
    """
    Models the dehydration process for removing water from ethanol.
    Efficiency determines the fraction of water successfully removed.
    """
    
    def __init__(self, efficiency=float):
        super().__init__(name="Dehydration", efficiency=efficiency, massFlowFunction=self.dehydrate)
        # Additional initialization for Dehydrator can go here

    
    def dehydrate(self, input=dict()):
        """
        Dehydration process: removes water from the mixture based on efficiency.
        Other components pass through unchanged.
        """
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