from .process import Process


class Fermentation(Process):
    """
    Models the fermentation process where sugar is converted to ethanol.
    Conversion efficiency determines the fraction of sugar converted.
    Stoichiometry: 51% of sugar mass becomes ethanol.
    """
    
    def __init__(self, **kwargs):
        """
        Initialize Fermentation process.
        
        Args:
            efficiency: Conversion efficiency (default: 1.0)
            power_consumption_rate: Power consumed by fermentation (default: 0 W)
            power_consumption_unit: Unit for power consumption (default: "kWh/day")
        """
        super().__init__(
            name=kwargs.get("name", "Fermentation"),
            massFlowFunction=self.ferment,
            **kwargs
        )

    
    def ferment(self, input=dict()):
        """
        Fermentation process: converts sugar to ethanol with specified efficiency.
        
        Outputs:
            - ethanol: 51% of converted sugar mass
            - water: passes through unchanged
            - sugar: unconverted sugar (based on efficiency)
            - fiber: passes through unchanged
        """
        return {
            "ethanol": 0.51 * input["sugar"] * self.efficiency if input.get("sugar") is not None else None, 
            "water": input["water"] if input.get("water") is not None and input.get("sugar") is not None else None,
            "sugar": (1 - self.efficiency) * input["sugar"] if input.get("sugar") is not None else None,
            "fiber": input["fiber"] if input.get("fiber") is not None else None
        }


class Filtration(Process):
    """
    Models the filtration process where fiber is removed from the mixture.
    Efficiency determines the fraction of fiber that is successfully filtered out.
    """
    
    def __init__(self, **kwargs):
        """
        Initialize Filtration process.
        
        Args:
            efficiency: Filtration efficiency (default: 1.0)
            power_consumption_rate: Power consumed by filtration (default: 0 W)
            power_consumption_unit: Unit for power consumption (default: "kWh/day")
        """
        super().__init__(
            name=kwargs.get("name", "Filtration"),
            massFlowFunction=self.filter,
            **kwargs
        )

    
    def filter(self, input=dict()):
        """
        Filtration process: removes fiber from the mixture based on efficiency.
        
        Outputs:
            - ethanol, water, sugar: pass through unchanged
            - fiber: remaining fiber after filtration (based on efficiency)
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
    At perfect efficiency (1.0), all ethanol is separated with no impurities.
    Lower efficiency results in impurities (water, sugar, fiber) being retained
    proportionally with the ethanol output.
    """
    
    def __init__(self, **kwargs):
        """
        Initialize Distillation process.
        
        Args:
            efficiency: Distillation efficiency (default: 1.0)
            power_consumption_rate: Power consumed by distillation (default: 0 W)
            power_consumption_unit: Unit for power consumption (default: "kWh/day")
        """
        super().__init__(
            name=kwargs.get("name", "Distillation"),
            massFlowFunction=self.distill,
            **kwargs
        )

    
    def distill(self, input=dict()):
        """
        Distillation process: separates ethanol from impurities.
        
        At perfect efficiency (1.0): output contains only ethanol, no impurities.
        At lower efficiency: impurities (water, sugar, fiber) appear in the output
        proportional to their input ratios and the inefficiency factor.
        
        Outputs:
            - ethanol: all input ethanol passes through
            - water, sugar, fiber: amounts based on efficiency and input ratios
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
    
    def __init__(self, **kwargs):
        """
        Initialize Dehydration process.
        
        Args:
            efficiency: Dehydration efficiency (default: 1.0)
            power_consumption_rate: Power consumed by dehydration (default: 0 W)
            power_consumption_unit: Unit for power consumption (default: "kWh/day")
        """
        super().__init__(
            name=kwargs.get("name", "Dehydration"),
            massFlowFunction=self.dehydrate,
            **kwargs
        )

    
    def dehydrate(self, input=dict()):
        """
        Dehydration process: removes water from the mixture based on efficiency.
        
        Outputs:
            - ethanol, sugar, fiber: pass through unchanged
            - water: remaining water after dehydration (based on efficiency)
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