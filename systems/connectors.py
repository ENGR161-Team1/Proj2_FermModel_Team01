import numpy as np
import math

class Connector:
    """
    Base class for all connector types in the ethanol plant model.
    Connectors represent components that transport fluid between systems.
    """
    def __init__(self, **kwargs):
        """
        Initialize a connector with energy function and diameter.
        
        Args:
            energy_consumed: Function to calculate energy consumed by connector
            diameter: Inner diameter of the connector in meters (default: 0.1m)
        """
        self.energyConsumed = kwargs.get("energy_consumed", None)
        self.diameter = kwargs.get("diameter", 0.1)
        self.cross_sectional_area = math.pi * (self.diameter / 2) ** 2
    
    def processDensity(self, **kwargs):
        """
        Calculate fluid density based on mass and volumetric flow rates.
        
        Args:
            inputs: Dictionary containing:
                - input_flow: Volumetric flow rate in m³/s
                - input_mass: Mass flow rate in kg/s
        
        Returns:
            Density in kg/m³, or 0 if volumetric flow is zero
        """
        input_flow = kwargs.get("input_flow", 0)
        input_mass = kwargs.get("input_mass", 0)
        return input_mass / input_flow if input_flow != 0 else 0

    def processFlow(self, **kwargs):
        """
        Calculate output volumetric flow rate after energy losses.
        
        Args:
            input_flow: Input volumetric flow rate in m³/s
            input_mass: Input mass flow rate in kg/s
            interval: Time interval in seconds (default: 1s)
        
        Returns:
            float: Output volumetric flow rate in m³/s
        """
        input_flow = kwargs.get("input_flow", 0)
        input_mass = kwargs.get("input_mass", 0)
        interval = kwargs.get("interval", 1)
        
        velocity = input_flow / self.cross_sectional_area if self.cross_sectional_area != 0 else 0
        input_energy = interval * input_mass * (velocity ** 2) / 2
        output_energy = input_energy - self.energyConsumed(**kwargs)

        output_flow = ((output_energy * self.cross_sectional_area) / (self.processDensity(**kwargs) * interval)) ** (float(1) / 3) if self.processDensity(**kwargs) != 0 else 0
        return output_flow


class Pipe(Connector):
    """
    Represents a straight pipe segment with friction losses.
    Energy loss is calculated using the Darcy-Weisbach equation.
    """
    def __init__(self, **kwargs):
        """
        Initialize a pipe connector.
        
        Args:
            length: Length of the pipe in meters (default: 1.0m)
            friction_factor: Darcy friction factor (default: 0.02)
            diameter: Inner diameter in meters (default: 0.1m)
        """
        self.length = kwargs.get("length", 1.0)
        self.friction_factor = kwargs.get("friction_factor", 0.02)
        super().__init__(energy_consumed=self.pipeEnergyFunction, diameter=kwargs.get("diameter", 0.1))
    
    def pipeEnergyFunction(self, **kwargs):
        """
        Calculate energy consumed due to friction in the pipe.
        Uses Darcy-Weisbach equation for pressure drop.
        
        Args:
            input_flow: Volumetric flow rate in m³/s
            input_mass: Mass flow rate in kg/s
        
        Returns:
            Energy consumed due to friction (Joules)
        """
        input_flow = kwargs.get("input_flow", 0)
        input_mass = kwargs.get("input_mass", 0)
        
        return input_mass * (8 * self.friction_factor * self.length * input_flow**2) / (math.pi**2 * self.diameter**5)


class Bend(Connector):
    """
    Represents a pipe bend or elbow with associated energy losses.
    Energy loss is proportional to the dynamic pressure and bend geometry.
    """
    def __init__(self, **kwargs):
        """
        Initialize a bend connector.
        
        Args:
            bend_radius: Radius of curvature in meters (default: 0.5m)
            bend_factor: Efficiency factor, 1.0 = no loss (default: 0.9)
            diameter: Inner diameter in meters (default: 0.1m)
        """
        self.bend_radius = kwargs.get("bend_radius", 0.5)
        self.bend_factor = kwargs.get("bend_factor", 0.9)
        super().__init__(energy_consumed=self.bendEnergyFunction, diameter=kwargs.get("diameter", 0.1))
    
    def bendEnergyFunction(self, **kwargs):
        """
        Calculate energy consumed in the bend due to flow direction change.
        Loss is based on kinetic energy and bend efficiency.
        
        Args:
            input_flow: Volumetric flow rate in m³/s
            input_mass: Mass flow rate in kg/s
        
        Returns:
            Energy consumed due to bend (Joules)
        """
        input_flow = kwargs.get("input_flow", 0)
        input_mass = kwargs.get("input_mass", 0)

        if input_flow == 0 or input_mass == 0:
            return 0

        velocity = input_flow / self.cross_sectional_area
        return input_mass * (1 - self.bend_factor) * (velocity ** 2) / 2


class Valve(Connector):
    """
    Represents a valve with adjustable flow resistance.
    Energy loss is proportional to the dynamic pressure and resistance coefficient.
    """
    def __init__(self, **kwargs):
        """
        Initialize a valve connector.
        
        Args:
            resistance_coefficient: Flow resistance coefficient (default: 1.0)
            diameter: Inner diameter in meters (default: 0.1m)
        """
        self.resistance_coefficient = kwargs.get("resistance_coefficient", 1.0)
        super().__init__(energy_consumed=self.valveEnergyFunction, diameter=kwargs.get("diameter", 0.1))
    
    def valveEnergyFunction(self, **kwargs):
        """
        Calculate energy consumed through the valve.
        Loss is based on kinetic energy and resistance coefficient.
        
        Args:
            input_flow: Volumetric flow rate in m³/s
            input_mass: Mass flow rate in kg/s
        
        Returns:
            Energy consumed due to valve resistance (Joules)
        """
        input_flow = kwargs.get("input_flow", 0)
        input_mass = kwargs.get("input_mass", 0)
        
        velocity = input_flow / self.cross_sectional_area
        return input_mass * (velocity ** 2) * self.resistance_coefficient / 2