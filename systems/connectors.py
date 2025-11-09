import numpy as np
import math

class Connector:
    """
    Base class for all connector types in the ethanol plant model.
    
    Connectors represent physical components that transport fluid between systems,
    such as pipes, bends, and valves. Each connector can consume power due to
    friction and other flow resistance mechanisms.
    """
    def __init__(self, **kwargs):
        """
        Initialize a connector with configurable parameters.
        
        Args:
            power_consumed (callable, optional): Function to calculate power consumed 
                by the connector in Watts. Should accept **kwargs.
            diameter (float, optional): Inner diameter of the connector in meters. 
                Default is 0.1m.
            cost (float, optional): Cost per unit in USD. Default is 0.
        """
        self.powerConsumed = kwargs.get("power_consumed", None)
        self.diameter = kwargs.get("diameter", 0.1)
        # Calculate cross-sectional area for flow calculations
        self.cross_sectional_area = math.pi * (self.diameter / 2) ** 2
        self.cost = kwargs.get("cost", 0)
    
    @staticmethod
    def processDensity(**kwargs):
        """
        Calculate fluid density from mass and volumetric flow rates.
        
        Uses the relationship: density = mass_flow / volumetric_flow
        
        Args:
            input_volumetric_flow (float, optional): Volumetric flow rate in m³/s. Default is 0.
            input_mass_flow (float, optional): Mass flow rate in kg/s. Default is 0.
        
        Returns:
            float: Fluid density in kg/m³. Returns 0 if volumetric flow is zero.
        """
        input_volumetric_flow = kwargs.get("input_volumetric_flow", 0)
        input_mass_flow = kwargs.get("input_mass_flow", 0)
        return input_mass_flow / input_volumetric_flow if input_volumetric_flow != 0 else 0
    
    def processPower(self, **kwargs):
        """
        Calculate output kinetic power after accounting for power losses.
        
        The output power is the input power minus the power consumed by the connector
        due to friction, resistance, or other loss mechanisms.
        
        Args:
            input_power (float, optional): Input kinetic power in Watts. Default is 0.
            
        Returns:
            float: Output kinetic power in Watts after losses.
        """
        input_power = kwargs.get("input_power", 0)
        return input_power - self.powerConsumed(**kwargs)


    def processFlow(self, **kwargs):
        """
        Calculate output volumetric flow rate after power losses in the connector.
        
        This method:
        1. Calculates flow velocity from volumetric flow and cross-sectional area
        2. Computes input kinetic power using velocity and mass flow
        3. Determines output power after losses using processPower()
        4. Calculates resulting output volumetric flow rate
        
        Args:
            input_volumetric_flow (float, optional): Input volumetric flow rate in m³/s. Default is 0.
            input_mass_flow (float, optional): Input mass flow rate in kg/s. Default is 0.
        
        Returns:
            float: Output volumetric flow rate in m³/s after accounting for power losses.
        """
        input_volumetric_flow = kwargs.get("input_volumetric_flow", 0)
        input_mass_flow = kwargs.get("input_mass_flow", 0)
        
        # Calculate flow velocity: Q = v * A, so v = Q / A
        velocity = input_volumetric_flow / self.cross_sectional_area if self.cross_sectional_area != 0 else 0
        
        # Calculate input kinetic power: P = (1/2) * m * v^2
        input_power = input_mass_flow * (velocity ** 2) / 2

        # Determine output power after accounting for connector losses
        output_power = self.processPower(input_power=input_power, **kwargs)
        
        # Calculate output volumetric flow rate from output power
        # Derived from kinetic power formula and continuity equation
        output_volumetric_flow = (2 * output_power * self.cross_sectional_area**2 / self.processDensity(**kwargs)) ** (1 / 3) if self.processDensity(**kwargs) != 0 else 0
        return output_volumetric_flow


class Pipe(Connector):
    """
    Represents a straight pipe segment with frictional losses.
    
    Power loss is calculated using the Darcy-Weisbach equation, which relates
    pressure drop to friction factor, pipe length, diameter, and flow velocity.
    """
    def __init__(self, **kwargs):
        """
        Initialize a pipe connector with geometric and friction properties.
        
        Args:
            length (float, optional): Length of the pipe in meters. Default is 1.0m.
            friction_factor (float, optional): Darcy friction factor (dimensionless). 
                Default is 0.02 (typical for turbulent flow in smooth pipes).
            diameter (float, optional): Inner diameter in meters. Default is 0.1m.
        """
        self.length = kwargs.get("length", 1.0)
        self.friction_factor = kwargs.get("friction_factor", 0.02)
        super().__init__(power_consumed=self.pipePowerFunction, diameter=kwargs.get("diameter", 0.1))
    
    def pipePowerFunction(self, **kwargs):
        """
        Calculate power consumed due to friction in the pipe.
        
        Uses the Darcy-Weisbach equation for pressure drop:
        ΔP = f * (L/D) * (ρv²/2)
        Power loss = ΔP * Q
        
        Args:
            input_volumetric_flow (float, optional): Volumetric flow rate in m³/s. Default is 0.
            input_mass_flow (float, optional): Mass flow rate in kg/s. Default is 0.
        
        Returns:
            float: Power consumed due to frictional losses in Watts.
        """
        input_volumetric_flow = kwargs.get("input_volumetric_flow", 0)
        input_mass_flow = kwargs.get("input_mass_flow", 0)
        
        # Darcy-Weisbach power loss formula
        return input_mass_flow * (8 * self.friction_factor * self.length * input_volumetric_flow**2) / (math.pi**2 * self.diameter**5)


class Bend(Connector):
    """
    Represents a pipe bend or elbow with losses due to flow direction change.
    
    Power loss occurs when fluid changes direction in a bend due to secondary flows
    and increased turbulence. The loss is proportional to the dynamic pressure and
    depends on the bend geometry and efficiency factor.
    """
    def __init__(self, **kwargs):
        """
        Initialize a bend connector with geometric and efficiency properties.
        
        Args:
            bend_radius (float, optional): Radius of curvature in meters. Default is 0.5m.
            bend_factor (float, optional): Efficiency factor between 0 and 1, where 
                1.0 means no loss and 0.0 means complete loss. Default is 0.9.
            diameter (float, optional): Inner diameter in meters. Default is 0.1m.
        """
        self.bend_radius = kwargs.get("bend_radius", 0.5)
        self.bend_factor = kwargs.get("bend_factor", 0.9)
        super().__init__(power_consumed=self.bendPowerFunction, diameter=kwargs.get("diameter", 0.1))
    
    def bendPowerFunction(self, **kwargs):
        """
        Calculate power consumed in the bend due to flow direction change.
        
        Loss is proportional to the kinetic energy and the inefficiency of the bend.
        Power loss = (1 - efficiency) * (1/2) * m * v²
        
        Args:
            input_volumetric_flow (float, optional): Volumetric flow rate in m³/s. Default is 0.
            input_mass_flow (float, optional): Mass flow rate in kg/s. Default is 0.
        
        Returns:
            float: Power consumed due to bend losses in Watts.
        """
        input_volumetric_flow = kwargs.get("input_volumetric_flow", 0)
        input_mass_flow = kwargs.get("input_mass_flow", 0)

        # Return zero power loss if there is no flow
        if input_volumetric_flow == 0 or input_mass_flow == 0:
            return 0

        # Calculate flow velocity
        velocity = input_volumetric_flow / self.cross_sectional_area
        # Power loss based on kinetic energy and bend inefficiency
        return input_mass_flow * (1 - self.bend_factor) * (velocity ** 2) / 2


class Valve(Connector):
    """
    Represents a valve with adjustable flow resistance.
    
    Valves control flow by introducing resistance. Power loss is proportional to
    the dynamic pressure and the valve's resistance coefficient, which can be
    adjusted based on the valve opening position.
    """
    def __init__(self, **kwargs):
        """
        Initialize a valve connector with resistance properties.
        
        Args:
            resistance_coefficient (float, optional): Flow resistance coefficient 
                (dimensionless). Higher values indicate more resistance. Default is 1.0.
            diameter (float, optional): Inner diameter in meters. Default is 0.1m.
        """
        self.resistance_coefficient = kwargs.get("resistance_coefficient", 1.0)
        super().__init__(power_consumed=self.valvePowerFunction, diameter=kwargs.get("diameter", 0.1))
    
    def valvePowerFunction(self, **kwargs):
        """
        Calculate power consumed through the valve due to flow resistance.
        
        Loss is based on the kinetic energy and resistance coefficient:
        Power loss = K * (1/2) * m_dot * v²
        where K is the resistance coefficient.
        
        Args:
            input_volumetric_flow (float, optional): Volumetric flow rate in m³/s. Default is 0.
            input_mass_flow (float, optional): Mass flow rate in kg/s. Default is 0.
        
        Returns:
            float: Power consumed due to valve resistance in Watts.
        """
        input_volumetric_flow = kwargs.get("input_volumetric_flow", 0)
        input_mass_flow = kwargs.get("input_mass_flow", 0)
        
        # Calculate flow velocity
        velocity = input_volumetric_flow / self.cross_sectional_area
        # Power loss based on resistance coefficient and kinetic energy
        return input_mass_flow * (velocity ** 2) * self.resistance_coefficient / 2