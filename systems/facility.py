from .process import Process
from .processors import Fermentation, Distillation, Dehydration, Filtration
from .connectors import Connector, Pipe, Valve, Bend
from .pump import Pump

class Facility():
    """
    Models a facility that contains multiple processes and connectors.
    
    This class orchestrates the flow of material through a series of connected
    processing units and connectors, managing both mass and volumetric representations
    of flow throughout the facility.
    """
    ETHANOL_ENERGY_DENSITY = 28.818e6  # J/kg
    def __init__(self, **kwargs):
        """
        Initialize a Facility with multiple process and connector components.
        
        Args:
            components (list, optional): List of Process and Connector instances to include
                in the facility. Default is empty list.
            pump_performance_rating (float, optional): Pump head rating in meters.
                Default is 0 m.
        """
        self.components = kwargs.get("components", [])
        self.pump = kwargs.get("pump", Pump())

    def add_component(self, component):
        """
        Add a process or connector to the facility.
        
        Args:
            component (Process or Connector): Unit to add to the facility's component list.
        """
        self.components.append(component)
    
    def facility_process(self, **kwargs):
        """
        Process material through all facility components sequentially.
        
        Converts input volumetric composition to mass flow, passes material through
        all configured processes and connectors in order, maintaining both volumetric
        and mass representations throughout. Tracks power consumption from pump,
        processes, and connectors.
        
        Args:
            store_data (bool, optional): Whether to log input/output data in each component.
                Default is False.
            input_volume_composition (dict): Component volumetric fractions (dimensionless, 0-1).
                Keys should be component names (ethanol, water, sugar, fiber).
            input_volumetric_flow (float): Total input volumetric flow rate in m³/s.
            input_power_consumed (float, optional): Power consumed (currently unused).
                Default is 0 W.
        
        Returns:
            tuple: (current_volumetric_flow, current_mass_flow, total_power_consumed)
                - current_volumetric_flow (dict): Output with keys "total_volumetric_flow",
                  "amount" (component flows in m³/s), "composition" (component fractions)
                - current_mass_flow (dict): Output with keys "total_mass_flow",
                  "amount" (component flows in kg/s), "composition" (component fractions)
                - total_power_consumed (float): Total power consumed by all components in Watts
        """
        store_data = kwargs.get("store_data", False)
        input_volume_composition = kwargs.get("input_volume_composition", {})
        input_total_volumetric_flow = kwargs.get("input_volumetric_flow", 0)
        interval = kwargs.get("interval", 1)
        
        # Initialize power consumption accumulator
        total_power_consumed = 0
        
        # Convert input volumetric composition to mass flow representation
        mass_flow_output = Process.volumetricToMass(
            inputs=input_volume_composition, 
            mode="composition", 
            total_flow=input_total_volumetric_flow,
            output_type="full"
        )
        
        # Initialize mass flow state: extract amounts and composition from conversion
        total_mass_flow = sum(mass_flow_output["amount"].values())
        current_mass_flow = {
            "total_mass_flow": total_mass_flow,
            "amount": mass_flow_output["amount"],
            "composition": mass_flow_output["composition"]
        }
        
        # Initialize volumetric flow state: preserve input structure
        current_volumetric_flow = {
            "total_volumetric_flow": input_total_volumetric_flow,
            "amount": {component: input_total_volumetric_flow * frac 
                      for component, frac in input_volume_composition.items()},
            "composition": input_volume_composition
        }
        
        # Process material through pump first
        pump_mass_flow, pump_volumetric_flow, pump_power_consumed = self.pump.pump_process(
            input_volume_flow=current_volumetric_flow["total_volumetric_flow"],
            input_composition=current_volumetric_flow["composition"]
        )
        total_power_consumed += pump_power_consumed
        
        # Update volumetric flow state with pump output
        current_volumetric_flow["total_volumetric_flow"] = pump_volumetric_flow
        current_volumetric_flow["amount"] = {
            component: pump_volumetric_flow * frac 
            for component, frac in current_volumetric_flow["composition"].items()
        }
        
        # Convert pump output to mass representation
        current_mass_flow = Process.volumetricToMass(
            inputs=current_volumetric_flow["amount"],
            mode="amount",
            output_type="full"
        )
        current_mass_flow["total_mass_flow"] = sum(current_mass_flow["amount"].values())
        
        # Process material through each component in sequence
        for component in self.components:
            if isinstance(component, Process):
                # Pass through process unit and get volumetric output
                current_volumetric_flow = component.processVolumetricFlow(
                    inputs=current_volumetric_flow,
                    input_type="full",
                    output_type="full",
                    store_inputs=store_data,
                    store_outputs=store_data,
                    store_cost=store_data
                )
                
                # Ensure total_volumetric_flow is present in output
                if "total_volumetric_flow" not in current_volumetric_flow:
                    current_volumetric_flow["total_volumetric_flow"] = sum(
                        current_volumetric_flow["amount"].values()
                    )
                
                # Convert volumetric output to mass representation for next component
                current_mass_flow = Process.volumetricToMass(
                    inputs=current_volumetric_flow["amount"],
                    mode="amount",
                    output_type="full"
                )
                current_mass_flow["total_mass_flow"] = sum(current_mass_flow["amount"].values())
                
                # Accumulate power consumption from process
                process_power_consumed = component.processPowerConsumption(
                    store_energy=store_data,
                    interval=interval
                )
                total_power_consumed += process_power_consumed
                
            elif isinstance(component, Connector):
                # Get power consumed by connector
                connector_power_consumed = component.powerConsumed(
                    input_volumetric_flow=current_volumetric_flow["total_volumetric_flow"],
                    input_mass_flow=current_mass_flow["total_mass_flow"]
                ) if component.powerConsumed else 0
                total_power_consumed += connector_power_consumed
                
                # Update total flow through connector (accounts for pressure drop, etc.)
                current_volumetric_flow["total_volumetric_flow"] = component.processFlow(
                    input_volumetric_flow=current_volumetric_flow["total_volumetric_flow"],
                    input_mass_flow=current_mass_flow["total_mass_flow"]
                )
                
                # Convert current volumetric state to mass representation
                current_mass_flow = Process.volumetricToMass(
                    inputs=current_volumetric_flow["amount"],
                    mode="amount",
                    output_type="full"
                )
                current_mass_flow["total_mass_flow"] = sum(current_mass_flow["amount"].values())
                
                # Convert mass representation back to volumetric for consistency
                volumetric_output = Process.massToVolumetric(
                    inputs=current_mass_flow["amount"],
                    mode="amount",
                    output_type="full"
                )
                current_volumetric_flow["amount"] = volumetric_output["amount"]
                current_volumetric_flow["composition"] = volumetric_output["composition"]
        
        return current_volumetric_flow, current_mass_flow, total_power_consumed