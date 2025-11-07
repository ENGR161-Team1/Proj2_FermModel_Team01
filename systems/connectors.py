import numpy as np
import math

class Connector:
    """
    Base class for all connector types in the ethanol plant model.
    Connectors represent components that transport fluid between systems.
    """
    def __init__(self, **kwargs):
        """
        Initialize a connector with mass and energy functions.
        
        Args:
            mass_function: Function to calculate mass flow through connector
            energy_function: Function to calculate energy changes in connector
            diameter: Inner diameter of the connector in meters (default: 0.1m)
        """
        self.mass_function = kwargs.get("mass_function", None)
        self.energy_function = kwargs.get("energy_function", None)
        self.diameter = kwargs.get("diameter", 0.1)  # default diameter in meters
        # Calculate cross-sectional area for flow calculations
        self.cross_sectional_area = math.pi * (self.diameter / 2) ** 2
    
    def processDensity(self, inputs=dict()):
        """
        Calculate fluid density based on mass and volumetric flow rates.
        
        Args:
            inputs: Dictionary containing:
                - input_flow: Volumetric flow rate in m³/h
                - input_mass: Mass flow rate in kg/h
        
        Returns:
            Density in kg/m³, or 0 if volumetric flow is zero
        """
        input_flow = inputs.get("input_flow", 0) # input volumetric flow rate in m3/h
        input_mass = inputs.get("input_mass", 0) # input mass flow rate in kg/h
        return input_mass / input_flow if input_flow != 0 else 0

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
        self.length = kwargs.get("length", 1.0)      # default length in meters
        self.friction_factor = kwargs.get("friction_factor", 0.02)  # default friction factor

        super().__init__(mass_function=self.pipeMassFunction, energy_function=self.pipeEnergyFunction, diameter=kwargs.get("diameter", 0.1))
    
    def pipeEnergyFunction(self, **kwargs):
        """
        Calculate energy loss due to friction in the pipe.
        Uses simplified Darcy-Weisbach equation for pressure drop.
        
        Args:
            input_flow: Volumetric flow rate in m³/h
            input_mass: Mass flow rate in kg/h
            input_energy: Input energy in Joules
        
        Returns:
            Output energy after friction losses (Joules)
        """
        input_flow = kwargs.get("input_flow", 0)
        input_mass = kwargs.get("input_mass", 0)
        input_energy = kwargs.get("input_energy", 0)
        
        # Calculate energy loss due to friction using Darcy-Weisbach
        energy_change = input_mass * (8 * self.friction_factor * input_flow**2) / (math.pi**2 * self.diameter**5)
        return input_energy - energy_change
    
    def pipeMassFunction(self, **kwargs):
        """
        Calculate mass flow through the pipe.
        Assumes no mass loss (conservation of mass).
        
        Args:
            input_mass: Input mass flow rate in kg/h
        
        Returns:
            Output mass flow rate in kg/h (equal to input)
        """
        input_mass = kwargs.get("input_mass", 0)
        return input_mass  # No mass loss in the pipe

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
        self.bend_radius = kwargs.get("bend_radius", 0.5)  # default bend radius in meters
        self.bend_factor = kwargs.get("bend_factor", 0.9)  # default bend factor

        super().__init__(mass_function=self.bendMassFunction, energy_function=self.bendEnergyFunction, diameter=kwargs.get("diameter", 0.1))

    
    def bendEnergyFunction(self, **kwargs):
        """
        Calculate energy loss in the bend due to flow direction change.
        Loss is based on kinetic energy and bend efficiency.
        
        Args:
            input_flow: Volumetric flow rate in m³/h
            input_mass: Mass flow rate in kg/h
            input_energy: Input energy in Joules
        
        Returns:
            Output energy after bend losses (Joules)
        """
        input_flow = kwargs.get("input_flow", 0)
        input_mass = kwargs.get("input_mass", 0)
        input_energy = kwargs.get("input_energy", 0)

        # Return input energy if no flow or mass
        if input_flow == 0 or input_mass == 0:
            return input_energy

        # Calculate flow velocity
        velocity = input_flow / (self.cross_sectional_area)
        # Energy loss is proportional to kinetic energy and bend inefficiency
        energy_change = input_mass * (1 - self.bend_factor) * (velocity ** 2) / 2
        return input_energy - energy_change
    
    def bendMassFunction(self, **kwargs):
        """
        Calculate mass flow through the bend.
        Assumes no mass loss (conservation of mass).
        
        Args:
            input_mass: Input mass flow rate in kg/h
        
        Returns:
            Output mass flow rate in kg/h (equal to input)
        """
        input_mass = kwargs.get("input_mass", 0)
        return input_mass  # No mass loss in the bend
    

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
        self.resistance_coefficient = kwargs.get("resistance_coefficient", 1.0)  # default resistance coefficient
        super().__init__(mass_function=self.valveMassFunction, energy_function=self.valveEnergyFunction)
    
    def valveEnergyFunction(self, **kwargs):
        """
        Calculate energy loss through the valve.
        Loss is based on kinetic energy and resistance coefficient.
        
        Args:
            input_flow: Volumetric flow rate in m³/h
            input_mass: Mass flow rate in kg/h
            input_energy: Input energy in Joules
        
        Returns:
            Output energy after valve losses (Joules)
        """
        input_flow = kwargs.get("input_flow", 0)
        input_mass = kwargs.get("input_mass", 0)
        input_energy = kwargs.get("input_energy", 0)
        
        # Calculate flow velocity
        velocity = input_flow / (self.cross_sectional_area)
        # Energy loss is proportional to kinetic energy and resistance
        energy_change = input_mass * (velocity ** 2) * self.resistance_coefficient / 2

        return input_energy - energy_change

    def valveMassFunction(self, **kwargs):
        """
        Calculate mass flow through the valve.
        Assumes no mass loss (conservation of mass).
        
        Args:
            input_mass: Input mass flow rate in kg/h
        
        Returns:
            Output mass flow rate in kg/h (equal to input)
        """
        input_mass = kwargs.get("input_mass", 0)
        return input_mass  # No mass loss in the valve