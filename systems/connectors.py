import numpy as np
import math

class Connector:
    """
    Base class for all connector types in the ethanol plant model.
    Connectors represent components that transport fluid between systems.
    """
    def __init__(self, **kwargs):
        """
        Initialize a connector with power function and diameter.
        
        Args:
            power_consumed: Function to calculate power consumed by connector (Watts)
            diameter: Inner diameter of the connector in meters (default: 0.1m)
        """
        self.powerConsumed = kwargs.get("power_consumed", None)
        self.diameter = kwargs.get("diameter", 0.1)
        self.cross_sectional_area = math.pi * (self.diameter / 2) ** 2
    
    def processDensity(self, **kwargs):
        """
        Calculate fluid density based on mass and volumetric flow rates.
        
        Args:
            input_volumetric_flow: Volumetric flow rate in m³/s
            input_mass_flow: Mass flow rate in kg/s
        
        Returns:
            Density in kg/m³, or 0 if volumetric flow is zero
        """
        input_volumetric_flow = kwargs.get("input_volumetric_flow", 0)
        input_mass_flow = kwargs.get("input_mass_flow", 0)
        return input_mass_flow / input_volumetric_flow if input_volumetric_flow != 0 else 0
    
    def processPower(self, **kwargs):
        """
        Calculate output kinetic power after power losses.
        
        Args:
            input_power: Input kinetic power in Watts
            
        Returns:
            output_power: Output kinetic power in Watts
        """
        input_power = kwargs.get("input_power", 0)
        return input_power - self.powerConsumed(**kwargs)


    def processFlow(self, **kwargs):
        """
        Calculate output volumetric flow rate after power losses.
        
        Args:
            input_volumetric_flow: Input volumetric flow rate in m³/s
            input_mass_flow: Input mass flow rate in kg/s
        
        Returns:
            float: Output volumetric flow rate in m³/s
        """
        # Extract input parameters from kwargs
        input_volumetric_flow = kwargs.get("input_volumetric_flow", 0)
        input_mass_flow = kwargs.get("input_mass_flow", 0)
        
        # Calculate flow velocity from volumetric flow rate and cross-sectional area
        velocity = input_volumetric_flow / self.cross_sectional_area if self.cross_sectional_area != 0 else 0
        
        # Calculate input kinetic power
        input_power = input_mass_flow * (velocity ** 2) / 2

        # Calculate output power after accounting for power losses
        output_power = self.processPower(input_power=input_power, **kwargs)
        
        # Calculate output flow rate from output power using inverse kinetic power formula
        output_volumetric_flow = (2 * output_power * self.cross_sectional_area**2 / self.processDensity(**kwargs)) ** (1 / 3) if self.processDensity(**kwargs) != 0 else 0
        return output_volumetric_flow


class Pipe(Connector):
    """
    Represents a straight pipe segment with friction losses.
    Power loss is calculated using the Darcy-Weisbach equation.
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
        super().__init__(power_consumed=self.pipePowerFunction, diameter=kwargs.get("diameter", 0.1))
    
    def pipePowerFunction(self, **kwargs):
        """
        Calculate power consumed due to friction in the pipe.
        Uses Darcy-Weisbach equation for pressure drop.
        
        Args:
            input_volumetric_flow: Volumetric flow rate in m³/s
            input_mass_flow: Mass flow rate in kg/s
        
        Returns:
            Power consumed due to friction (Watts)
        """
        input_volumetric_flow = kwargs.get("input_volumetric_flow", 0)
        input_mass_flow = kwargs.get("input_mass_flow", 0)
        
        return input_mass_flow * (8 * self.friction_factor * self.length * input_volumetric_flow**2) / (math.pi**2 * self.diameter**5)


class Bend(Connector):
    """
    Represents a pipe bend or elbow with associated power losses.
    Power loss is proportional to the dynamic pressure and bend geometry.
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
        super().__init__(power_consumed=self.bendPowerFunction, diameter=kwargs.get("diameter", 0.1))
    
    def bendPowerFunction(self, **kwargs):
        """
        Calculate power consumed in the bend due to flow direction change.
        Loss is based on kinetic power and bend efficiency.
        
        Args:
            input_volumetric_flow: Volumetric flow rate in m³/s
            input_mass_flow: Mass flow rate in kg/s
        
        Returns:
            Power consumed due to bend (Watts)
        """
        input_volumetric_flow = kwargs.get("input_volumetric_flow", 0)
        input_mass_flow = kwargs.get("input_mass_flow", 0)

        if input_volumetric_flow == 0 or input_mass_flow == 0:
            return 0

        velocity = input_volumetric_flow / self.cross_sectional_area
        return input_mass_flow * (1 - self.bend_factor) * (velocity ** 2) / 2


class Valve(Connector):
    """
    Represents a valve with adjustable flow resistance.
    Power loss is proportional to the dynamic pressure and resistance coefficient.
    """
    def __init__(self, **kwargs):
        """
        Initialize a valve connector.
        
        Args:
            resistance_coefficient: Flow resistance coefficient (default: 1.0)
            diameter: Inner diameter in meters (default: 0.1m)
        """
        self.resistance_coefficient = kwargs.get("resistance_coefficient", 1.0)
        super().__init__(power_consumed=self.valvePowerFunction, diameter=kwargs.get("diameter", 0.1))
    
    def valvePowerFunction(self, **kwargs):
        """
        Calculate power consumed through the valve.
        Loss is based on kinetic power and resistance coefficient.
        
        Args:
            input_volumetric_flow: Volumetric flow rate in m³/s
            input_mass_flow: Mass flow rate in kg/s
        
        Returns:
            Power consumed due to valve resistance (Watts)
        """
        input_volumetric_flow = kwargs.get("input_volumetric_flow", 0)
        input_mass_flow = kwargs.get("input_mass_flow", 0)
        
        velocity = input_volumetric_flow / self.cross_sectional_area
        return input_mass_flow * (velocity ** 2) * self.resistance_coefficient / 2