import matplotlib
import matplotlib.pyplot as plt


class Process:
    """
    Base class for modeling chemical processing systems in an ethanol plant.
    
    Provides functionality for tracking mass/volumetric flow rates, converting between
    representations, processing chemical components, monitoring power consumption and costs,
    and handling compositional analysis of multi-component mixtures.
    """
    
    # Density constants (kg/m³) at standard conditions (20°C, 1 atm)
    DENSITY_WATER = 997
    DENSITY_ETHANOL = 789
    DENSITY_SUGAR = 1590
    DENSITY_FIBER = 1311
    
    def __init__(self, **kwargs):
        """
        Initialize a Process with configuration parameters and logging structures.
        
        Args:
            name (str): Descriptive name for this process unit. Default: "Process".
            efficiency (float): Process efficiency factor (0-1). Default: 1.0.
            massFlowFunction (callable): Custom function to transform input mass flows
                to output mass flows. If None, acts as pass-through.
            power_consumption_rate (float): Power consumption rate. Default: 0.
            power_consumption_unit (str): Unit for power - "kWh/day", "kW"/"kWh/hour", or "W".
                Default: "kWh/day".
            cost (float): Fixed cost per unit operation (USD). Default: 0.
            cost_per_flow (float): Variable cost per m³/s of flow (USD). Default: 0.
        """
        self.name = kwargs.get("name", "Process")
        
        self.input_log = {
            "mass_flow": {
                "total_mass_flow": [],
                "amount": {
                    "ethanol": [],
                    "water": [],
                    "sugar": [],
                    "fiber": []
                }, 
                "composition": {
                    "ethanol": [],
                    "water": [],
                    "sugar": [],
                    "fiber": []
                }
            },
            "volumetric_flow": {
                "total_volumetric_flow": [],
                "amount": {
                    "ethanol": [],
                    "water": [],
                    "sugar": [],
                    "fiber": []
                }, 
                "composition": {
                    "ethanol": [],
                    "water": [],
                    "sugar": [],
                    "fiber": []
                }
            },
        }
        
        self.output_log = {
            "mass_flow": {
                "total_mass_flow": [],
                "amount": {
                    "ethanol": [], 
                    "water": [], 
                    "sugar": [], 
                    "fiber": []
                }, 
                "composition": {
                    "ethanol": [], 
                    "water": [], 
                    "sugar": [], 
                    "fiber": []
                }
            },
            "volumetric_flow": {
                "total_volumetric_flow": [],
                "amount": {
                    "ethanol": [], 
                    "water": [], 
                    "sugar": [], 
                    "fiber": []
                }, 
                "composition": {
                    "ethanol": [], 
                    "water": [], 
                    "sugar": [], 
                    "fiber": []
                }
            },
        }
        
        self.consumption_log = {
            "power_consumption_rate": [],
            "energy_consumed": [],
            "interval": [],
            "cost_per_unit_flow": [],
            "cost_incurred": []
        }
        
        # Convert power consumption to Watts
        self.power_consumption_rate = kwargs.get("power_consumption_rate", 0)
        power_consumption_unit = kwargs.get("power_consumption_unit", "kWh/day")
        
        if power_consumption_unit == "kWh/day":
            self.power_consumption_rate = self.power_consumption_rate / 24 * 1000
        elif power_consumption_unit == "kWh/hour" or power_consumption_unit == "kW":
            self.power_consumption_rate *= 1000
        
        self.cost = kwargs.get("cost", 0)
        self.cost_per_flow = kwargs.get("cost_per_flow", 0)
        self.components = ["ethanol", "water", "sugar", "fiber"]
        self.efficiency = kwargs.get("efficiency", 1.0)
        self.massFlowFunction = kwargs.get("massFlowFunction", None)

    @staticmethod
    def volumetricToMass(**kwargs):
        """
        Convert volumetric flow rates to mass flow rates using component densities.
        
        Supports two modes:
        - 'amount': Direct volumetric to mass conversion
        - 'composition': Converts fractional compositions with total flow to mass rates
        
        Args:
            inputs (dict): Component volumetric flow rates or fractions.
            mode (str): 'amount' or 'composition'. Default: 'amount'.
            total_flow (float): Total volumetric flow (m³/s). Required for 'composition' mode.
            output_type (str): 'amount', 'composition', or 'full'. Default: 'amount'.
        
        Returns:
            dict: Mass flow rates (kg/s) or formatted output per output_type.
        
        Raises:
            ValueError: For invalid modes, missing inputs, or unknown components.
        """
        inputs = kwargs.get("inputs", dict())
        mode = kwargs.get("mode", "amount")
        total_volumetric_flow = kwargs.get("total_flow", None)
        output_type = kwargs.get("output_type", "amount")
        
        if mode not in ["amount", "composition"]:
            raise ValueError("mode must be either 'amount' or 'composition'")
        if not inputs:
            raise ValueError("No inputs provided for conversion")
        if output_type not in ["amount", "composition", "full"]:
            raise ValueError("output_type must be either 'amount', 'composition', or 'full'")
            
        if mode == "amount":
            mass_flow_inputs = dict()
            for component in inputs:
                if component == "ethanol":
                    mass_flow_inputs[component] = inputs[component] * Process.DENSITY_ETHANOL
                elif component == "water":
                    mass_flow_inputs[component] = inputs[component] * Process.DENSITY_WATER
                elif component == "sugar":
                    mass_flow_inputs[component] = inputs[component] * Process.DENSITY_SUGAR
                elif component == "fiber":
                    mass_flow_inputs[component] = inputs[component] * Process.DENSITY_FIBER
                else:
                    raise ValueError(f"Unknown component: {component}")
            
            if output_type == "amount":
                return mass_flow_inputs
            else:
                total_mass = sum(mass_flow_inputs.values())
                if total_mass <= 0:
                    raise ValueError("Total mass flow must be greater than zero to calculate composition")
                mass_composition = {component: mass_flow_inputs[component] / total_mass for component in mass_flow_inputs}
                
                return mass_composition if output_type == "composition" else {
                    "amount": mass_flow_inputs,
                    "composition": mass_composition
                }
        else:
            if total_volumetric_flow is None:
                raise ValueError("total_volumetric_flow must be provided when mode is 'composition'")
            mass_flow_inputs = dict()
            for component in inputs:
                if component == "ethanol":
                    mass_flow_inputs[component] = inputs[component] * total_volumetric_flow * Process.DENSITY_ETHANOL
                elif component == "water":
                    mass_flow_inputs[component] = inputs[component] * total_volumetric_flow * Process.DENSITY_WATER
                elif component == "sugar":
                    mass_flow_inputs[component] = inputs[component] * total_volumetric_flow * Process.DENSITY_SUGAR
                elif component == "fiber":
                    mass_flow_inputs[component] = inputs[component] * total_volumetric_flow * Process.DENSITY_FIBER
                else:
                    raise ValueError(f"Unknown component: {component}")
            
            if output_type == "amount":
                return mass_flow_inputs
            else:
                mass_composition = inputs
                return mass_composition if output_type == "composition" else {
                    "amount": mass_flow_inputs,
                    "composition": mass_composition
                }
    
    @staticmethod
    def massToVolumetric(**kwargs):
        """
        Convert mass flow rates to volumetric flow rates using component densities.
        
        Supports two modes:
        - 'amount': Direct mass to volumetric conversion
        - 'composition': Converts fractional compositions with total mass flow to volumetric rates
        
        Args:
            inputs (dict): Component mass flow rates or fractions.
            mode (str): 'amount' or 'composition'. Default: 'amount'.
            total_mass (float): Total mass flow (kg/s). Required for 'composition' mode.
            output_type (str): 'amount', 'composition', or 'full'. Default: 'amount'.
        
        Returns:
            dict: Volumetric flow rates (m³/s) or formatted output per output_type.
        
        Raises:
            ValueError: For invalid modes, missing inputs, or unknown components.
        """
        inputs = kwargs.get("inputs", dict())
        mode = kwargs.get("mode", "amount")
        total_mass_flow = kwargs.get("total_mass", None)
        output_type = kwargs.get("output_type", "amount")
        
        if mode not in ["amount", "composition"]:
            raise ValueError("mode must be either 'amount' or 'composition'")
        if not inputs:
            raise ValueError("No inputs provided for conversion")
        if output_type not in ["amount", "composition", "full"]:
            raise ValueError("output_type must be either 'amount', 'composition', or 'full'")
            
        if mode == "amount":
            volumetric_flow_inputs = dict()
            for component in inputs:
                if component == "ethanol":
                    volumetric_flow_inputs[component] = inputs[component] / Process.DENSITY_ETHANOL
                elif component == "water":
                    volumetric_flow_inputs[component] = inputs[component] / Process.DENSITY_WATER
                elif component == "sugar":
                    volumetric_flow_inputs[component] = inputs[component] / Process.DENSITY_SUGAR
                elif component == "fiber":
                    volumetric_flow_inputs[component] = inputs[component] / Process.DENSITY_FIBER
                else:
                    raise ValueError(f"Unknown component: {component}")
            
            if output_type == "amount":
                return volumetric_flow_inputs
            else:
                total_volumetric = sum(volumetric_flow_inputs.values())
                if total_volumetric <= 0:
                    raise ValueError("Total volumetric flow must be greater than zero to calculate composition")
                volumetric_composition = {component: volumetric_flow_inputs[component] / total_volumetric for component in volumetric_flow_inputs}
                
                return volumetric_composition if output_type == "composition" else {
                    "amount": volumetric_flow_inputs,
                    "composition": volumetric_composition
                }
        else:
            if total_mass_flow is None:
                raise ValueError("total_mass_flow must be provided when mode is 'composition'")
            volumetric_flow_inputs = dict()
            for component in inputs:
                if component == "ethanol":
                    volumetric_flow_inputs[component] = inputs[component] * total_mass_flow / Process.DENSITY_ETHANOL
                elif component == "water":
                    volumetric_flow_inputs[component] = inputs[component] * total_mass_flow / Process.DENSITY_WATER
                elif component == "sugar":
                    volumetric_flow_inputs[component] = inputs[component] * total_mass_flow / Process.DENSITY_SUGAR
                elif component == "fiber":
                    volumetric_flow_inputs[component] = inputs[component] * total_mass_flow / Process.DENSITY_FIBER
                else:
                    raise ValueError(f"Unknown component: {component}")
            
            if output_type == "amount":
                return volumetric_flow_inputs
            else:
                volumetric_composition = inputs
                return volumetric_composition if output_type == "composition" else {
                    "amount": volumetric_flow_inputs,
                    "composition": volumetric_composition
                }
    
    def processMassFlow(self, **kwargs):
        """
        Process mass flow rate inputs through the system's transformation function.
        
        Core processing method that:
        1. Normalizes inputs to amounts and compositions
        2. Applies custom massFlowFunction transformation
        3. Calculates outputs and compositions
        4. Optionally logs inputs, outputs, and costs
        
        Args:
            inputs (dict): Input values per input_type format.
            input_type (str): 'amount', 'composition', or 'full'. Default: 'full'.
            output_type (str): 'amount', 'composition', or 'full'. Default: 'full'.
            total_mass (float): Total mass flow (kg/s). Required for 'composition' input_type.
            store_inputs (bool): Whether to log input values. Default: False.
            store_outputs (bool): Whether to log output values. Default: False.
                Only valid with output_type='full'.
            store_cost (bool): Whether to log cost data. Default: False.
        
        Returns:
            dict: Processed outputs in format specified by output_type.
        
        Raises:
            ValueError: For invalid inputs or incompatible parameters.
        """
        inputs = kwargs.get("inputs", dict())
        input_type = kwargs.get("input_type", "full")
        output_type = kwargs.get("output_type", "full")
        total_mass_flow = kwargs.get("total_mass", None)
        store_inputs = kwargs.get("store_inputs", False)
        store_outputs = kwargs.get("store_outputs", False)
        store_cost = kwargs.get("store_cost", False)
        
        if not inputs:
            raise ValueError("No inputs provided for processing")
        if input_type not in ["amount", "composition", "full"] or output_type not in ["amount", "composition", "full"]:
            raise ValueError("input_type and output_type must be either 'amount', 'composition', or 'full'")
        if store_outputs and not output_type == "full":
            raise ValueError("store_outputs can only be True when output_type is 'full'")
        if input_type == "composition" and any(key not in inputs for key in self.components):
            raise ValueError("All components must be provided when input_type is 'composition'")
        
        # Normalize inputs
        if input_type == "composition":
            if total_mass_flow is None:
                raise ValueError("total_mass_flow must be provided when input_type is 'composition'")
            input_amounts = {component: inputs[component] * total_mass_flow for component in self.components}
            input_composition = inputs
        elif input_type == "amount":
            input_amounts = inputs.copy()
            if total_mass_flow is None:
                total_mass_flow = sum(inputs[component] for component in self.components)
            if total_mass_flow <= 0:
                raise ValueError("Total input amount must be greater than zero to calculate composition")
            input_composition = {component: input_amounts[component] / total_mass_flow for component in self.components}
        else:
            if any(key not in inputs["composition"] for key in self.components):
                raise ValueError("All components must be provided in 'composition' when input_type is 'full'")
            input_amounts = inputs["amount"].copy()
            if total_mass_flow is None:
                total_mass_flow = sum(inputs["amount"][component] for component in self.components)
            input_composition = inputs["composition"].copy()

        if store_inputs:
            for component in self.components:
                self.input_log["mass_flow"]["amount"][component].append(input_amounts[component])
                self.input_log["mass_flow"]["composition"][component].append(input_composition[component])
            self.input_log["mass_flow"]["total_mass_flow"].append(total_mass_flow)

        if store_cost:
            volumetric_flow_for_cost = Process.massToVolumetric(inputs=input_amounts, mode="amount")
            total_volumetric_flow = sum(volumetric_flow_for_cost.values())
            cost_incurred = self.cost_per_flow * total_volumetric_flow
            
            self.consumption_log["cost_per_unit_flow"].append(self.cost_per_flow)
            self.consumption_log["cost_incurred"].append(cost_incurred)

        output_amounts = self.massFlowFunction(input_amounts) if self.massFlowFunction else input_amounts
        filtered_output = {k: v for k, v in output_amounts.items() if v is not None}
        output_total = sum(filtered_output.values())
        
        if output_type == "amount":
            return filtered_output
        else:
            if output_total <= 0:
                raise ValueError("Total output amount must be greater than zero to calculate composition")
            output_composition = {component: filtered_output[component] / output_total for component in filtered_output}
            
            if output_type == "composition":
                return output_composition
            else:
                if store_outputs:
                    for component in filtered_output:
                        self.output_log["mass_flow"]["amount"][component].append(filtered_output[component])
                        self.output_log["mass_flow"]["composition"][component].append(output_composition[component])
                    self.output_log["mass_flow"]["total_mass_flow"].append(output_total)
                
                return {
                    "amount": filtered_output,
                    "composition": output_composition
                }

    def processVolumetricFlow(self, **kwargs):
        """
        Process volumetric flow rate inputs through the system.
        
        Provides a volumetric interface to mass-based processing:
        1. Converts volumetric inputs to mass flow rates
        2. Processes through processMassFlow()
        3. Converts mass outputs back to volumetric flow rates
        4. Logs both volumetric and mass representations
        
        Args:
            inputs (dict): Component volumetric flow rates per input_type format (m³/s).
            input_type (str): 'amount', 'composition', or 'full'. Default: 'full'.
            output_type (str): 'amount', 'composition', or 'full'. Default: 'full'.
            total_flow (float): Total volumetric flow (m³/s). Required for 'composition' input_type.
            store_inputs (bool): Whether to log input values. Default: False.
            store_outputs (bool): Whether to log output values. Default: False.
            store_cost (bool): Whether to log cost data. Default: False.
        
        Returns:
            dict: Processed volumetric flow outputs in format specified by output_type (m³/s).
        
        Raises:
            ValueError: For invalid input_type or missing required parameters.
        """
        inputs = kwargs.get("inputs", dict())
        input_type = kwargs.get("input_type", "full")
        output_type = kwargs.get("output_type", "full")
        total_volumetric_flow = kwargs.get("total_flow", None)
        store_inputs = kwargs.get("store_inputs", False)
        store_outputs = kwargs.get("store_outputs", False)
        store_cost = kwargs.get("store_cost", False)

        # Convert volumetric inputs to mass
        if input_type == "full":
            mass_flow_inputs = {
                "amount": Process.volumetricToMass(inputs=inputs["amount"], mode="amount"),
                "composition": inputs["composition"]
            }
            mass_flow_input_type = "full"
            total_mass_flow = sum(mass_flow_inputs["amount"][component] for component in self.components)
        elif input_type == "amount":
            mass_flow_inputs = Process.volumetricToMass(inputs=inputs, mode="amount")
            mass_flow_input_type = "amount"
            total_mass_flow = sum(mass_flow_inputs[component] for component in self.components if component in mass_flow_inputs)
        elif input_type == "composition":
            if total_volumetric_flow is None:
                raise ValueError("total_volumetric_flow must be provided when input_type is 'composition'")
            mass_flow_inputs = Process.volumetricToMass(inputs=inputs, mode="composition", total_flow=total_volumetric_flow)
            mass_flow_input_type = "amount"
            total_mass_flow = sum(mass_flow_inputs[component] for component in self.components if component in mass_flow_inputs)
        else:
            raise ValueError("input_type must be either 'amount', 'composition', or 'full'")

        mass_flow_outputs = self.processMassFlow(
            inputs=mass_flow_inputs,
            input_type=mass_flow_input_type,
            output_type="full",
            total_mass=total_mass_flow,
            store_inputs=store_inputs,
            store_outputs=store_outputs,
            store_cost=False
        )

        volumetric_flow_output_amounts = Process.massToVolumetric(inputs=mass_flow_outputs["amount"], mode="amount")
        
        # Calculate total volumetric flow
        if input_type == "full":
            if total_volumetric_flow is None:
                total_volumetric_flow = sum(inputs["amount"][component] for component in self.components if component in inputs["amount"])
        elif input_type == "amount":
            if total_volumetric_flow is None:
                total_volumetric_flow = sum(inputs[component] for component in self.components if component in inputs)
        
        # Store volumetric inputs if requested
        if store_inputs:
            if input_type == "full":
                for component in self.components:
                    if component in inputs["amount"]:
                        self.input_log["volumetric_flow"]["amount"][component].append(inputs["amount"][component])
                    if component in inputs["composition"]:
                        self.input_log["volumetric_flow"]["composition"][component].append(inputs["composition"][component])
                self.input_log["volumetric_flow"]["total_volumetric_flow"].append(total_volumetric_flow)
            elif input_type == "amount":
                for component in self.components:
                    if component in inputs:
                        self.input_log["volumetric_flow"]["amount"][component].append(inputs[component])
                        self.input_log["volumetric_flow"]["composition"][component].append(inputs[component] / total_volumetric_flow if total_volumetric_flow > 0 else 0)
                self.input_log["volumetric_flow"]["total_volumetric_flow"].append(total_volumetric_flow)
            elif input_type == "composition":
                for component in self.components:
                    if component in inputs:
                        self.input_log["volumetric_flow"]["composition"][component].append(inputs[component])
                        self.input_log["volumetric_flow"]["amount"][component].append(inputs[component] * total_volumetric_flow)
                self.input_log["volumetric_flow"]["total_volumetric_flow"].append(total_volumetric_flow)

        if store_cost:
            cost_incurred = self.cost_per_flow * total_volumetric_flow
            self.consumption_log["cost_per_unit_flow"].append(self.cost_per_flow)
            self.consumption_log["cost_incurred"].append(cost_incurred)

        output_total_volumetric_flow = sum(volumetric_flow_output_amounts[component] for component in volumetric_flow_output_amounts)

        if store_outputs:
            for component in self.components:
                if component in volumetric_flow_output_amounts:
                    self.output_log["volumetric_flow"]["amount"][component].append(volumetric_flow_output_amounts[component])
                if component in mass_flow_outputs["composition"]:
                    self.output_log["volumetric_flow"]["composition"][component].append(mass_flow_outputs["composition"][component])
            self.output_log["volumetric_flow"]["total_volumetric_flow"].append(output_total_volumetric_flow)

        if output_type == "amount":
            return volumetric_flow_output_amounts
        elif output_type == "composition":
            return mass_flow_outputs["composition"]
        else:
            return {
                "amount": volumetric_flow_output_amounts,
                "composition": mass_flow_outputs["composition"]
            }

    def processPowerConsumption(self, **kwargs):
        """
        Get the power consumption rate of the process.
        
        Args:
            store_energy (bool): Whether to log power and energy data. Default: False.
            interval (float): Time interval in seconds for energy calculation. Default: 1.
        
        Returns:
            float: Power consumption rate in Watts (W).
        """
        store_energy = kwargs.get("store_energy", False)
        interval = kwargs.get("interval", 1)
        
        energy_consumed_in_interval = self.power_consumption_rate * interval
        
        if store_energy:
            self.consumption_log["power_consumption_rate"].append(self.power_consumption_rate)
            self.consumption_log["energy_consumed"].append(energy_consumed_in_interval)
            self.consumption_log["interval"].append(interval)
        
        return self.power_consumption_rate

    def iterateMassFlowInputs(self, inputValues=dict(), **kwargs):
        """
        Process multiple sets of mass flow rate inputs iteratively over time.
        
        Enables batch processing of time-series or parametric study data with automatic logging.
        
        Args:
            inputValues (dict): Dictionary of input lists per input_type format.
            input_type (str): 'amount', 'composition', or 'full'. Default: 'amount'.
            output_type (str): 'amount', 'composition', or 'full'. Default: 'full'.
            total_mass_list (list): List of total mass flows (kg/s).
                Required when input_type='composition'. Length must match input sets.
            store_cost (bool): Whether to log cost data. Default: False.
        
        Returns:
            dict: Updated output_log with all processed results.
        
        Raises:
            ValueError: For invalid input_type or mismatched total_mass_list.
        """
        input_type = kwargs.get("input_type", "amount")
        output_type = kwargs.get("output_type", "full")
        total_mass_flow_list = kwargs.get("total_mass_list", None)
        store_cost = kwargs.get("store_cost", False)
        
        if input_type not in ["amount", "composition", "full"]:
            raise ValueError("input_type must be either 'amount', 'composition', or 'full'")
        
        if input_type == "full":
            num_iterations = len(inputValues["amount"][self.components[0]])
        else:
            num_iterations = len(inputValues[self.components[0]])
        
        if input_type == "composition":
            if total_mass_flow_list is None:
                raise ValueError("total_mass_flow_list must be provided when input_type is 'composition'")
            if len(total_mass_flow_list) != num_iterations:
                raise ValueError("Length of total_mass_flow_list must match number of input sets")
        
        for i in range(num_iterations):
            if input_type == "amount":
                input_dict = {component: inputValues[component][i] for component in self.components if component in inputValues}
                total_mass_flow = None
            elif input_type == "composition":
                input_dict = {component: inputValues[component][i] for component in self.components if component in inputValues}
                total_mass_flow = total_mass_flow_list[i]
            else:
                input_dict = {
                    "amount": {component: inputValues["amount"][component][i] for component in self.components if component in inputValues["amount"]},
                    "composition": {component: inputValues["composition"][component][i] for component in self.components if component in inputValues["composition"]}
                }
                total_mass_flow = None
            
            self.processMassFlow(
                inputs=input_dict,
                input_type=input_type,
                output_type=output_type,
                total_mass=total_mass_flow,
                store_inputs=True,
                store_outputs=True,
                store_cost=store_cost
            )
        
        return self.output_log

    def iterateVolumetricFlowInputs(self, inputValues=dict(), **kwargs):
        """
        Process multiple sets of volumetric flow rate inputs iteratively over time.
        
        Similar to iterateMassFlowInputs but for volumetric data. Converts to mass,
        processes, and converts back with both representations logged.
        
        Args:
            inputValues (dict): Dictionary of input lists per input_type format (m³/s).
            input_type (str): 'amount', 'composition', or 'full'. Default: 'amount'.
            output_type (str): 'amount', 'composition', or 'full'. Default: 'full'.
            total_flow_list (list): List of total volumetric flows (m³/s).
                Required when input_type='composition'. Length must match input sets.
            store_cost (bool): Whether to log cost data. Default: False.
        
        Returns:
            dict: Updated output_log with all processed results.
        
        Raises:
            ValueError: For invalid input_type or mismatched total_flow_list.
        """        
        input_type = kwargs.get("input_type", "amount")
        output_type = kwargs.get("output_type", "full")
        total_volumetric_flow_list = kwargs.get("total_flow_list", None)
        store_cost = kwargs.get("store_cost", False)
        
        if input_type not in ["amount", "composition", "full"]:
            raise ValueError("input_type must be either 'amount', 'composition', or 'full'")
        
        if input_type == "full":
            num_iterations = len(inputValues["amount"][self.components[0]])
        else:
            num_iterations = len(inputValues[self.components[0]])
        
        if input_type == "composition":
            if total_volumetric_flow_list is None:
                raise ValueError("total_volumetric_flow_list must be provided when input_type is 'composition'")
            if len(total_volumetric_flow_list) != num_iterations:
                raise ValueError("Length of total_volumetric_flow_list must match number of input sets")
        
        for i in range(num_iterations):
            if input_type == "amount":
                input_dict = {component: inputValues[component][i] for component in self.components if component in inputValues}
                total_volumetric_flow = None
            elif input_type == "composition":
                input_dict = {component: inputValues[component][i] for component in self.components if component in inputValues}
                total_volumetric_flow = total_volumetric_flow_list[i]
            else:
                input_dict = {
                    "amount": {component: inputValues["amount"][component][i] for component in self.components if component in inputValues["amount"]},
                    "composition": {component: inputValues["composition"][component][i] for component in self.components if component in inputValues["composition"]}
                }
                total_volumetric_flow = None
            
            self.processVolumetricFlow(
                inputs=input_dict,
                input_type=input_type,
                output_type=output_type,
                total_flow=total_volumetric_flow,
                store_inputs=True,
                store_outputs=True,
                store_cost=store_cost
            )
        
        return self.output_log

    def iterateInputs(self, inputValues=dict(), **kwargs):
        """
        Legacy method for processing multiple sets of inputs iteratively.
        
        Note: Prefer iterateMassFlowInputs() or iterateVolumetricFlowInputs() for new code.
        These provide more flexible input/output formats and better logging.
        
        Args:
            inputValues (dict): Dictionary of input value lists per component.
        
        Returns:
            dict: Updated output_log with all processed results.
        """
        for key in inputValues:
            self.input_log[key] += inputValues[key]

        for i in range(len(inputValues["ethanol"])):
            input_dict = {key: inputValues[key][i] for key in inputValues}
            output_dict = self.massFlowFunction(input_dict)
            
            for key in self.output_log:
                self.output_log[key].append(output_dict[key])

        return self.output_log