import matplotlib
import matplotlib.pyplot as plt
# matplotlib.use("gtk4agg") --- IGNORE ---


class Process:
    """
    Base class for modeling chemical processing systems.
    Handles mass flow rate and volumetric flow rate conversions, processing, and logging of inputs/outputs.
    """
    
    def __init__(self, **kwargs):
        """
        Initialize a Process with name, efficiency, and optional mass flow rate function.
        Sets up input/output logs for tracking mass flow rate and volumetric flow rate data.
        """
        self.name = kwargs.get("name", "Process")
        
        # New log structure without 'total' in composition and separated amount/composition
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
        self.energy_consumed_log = []
        self.energy_consumption_rate = kwargs.get("energy_consumption_rate", 0)
        energy_consumption_unit = kwargs.get("energy_consumption_unit", "kWh/day")
        if energy_consumption_unit == "kWh/day":
            self.energy_consumption_rate /= 24  # Convert to kW
            self.energy_consumption_rate *= 1000  # Convert to W
        self.components = ["ethanol", "water", "sugar", "fiber"]
        self.efficiency = kwargs.get("efficiency", 1.0)
        self.massFlowFunction = kwargs.get("massFlowFunction", None)
        
        # Density constants for conversion between mass and flow (kg/m^3)
        self.densityWater = 997  # kg/m^3
        self.densityEthanol = 789  # kg/m^3
        self.densitySugar = 1590  # kg/m^3
        self.densityFiber = 1311  # kg/m^3

    def volumetricToMass(self, **kwargs):
        """
        Convert volumetric flow rates to mass flow rates.
        
        Args:
            inputs: Dictionary of component volumetric flow rates
            mode: 'amount' for absolute values or 'composition' for fractional values
            total_volumetric_flow: Total volumetric flow rate (required when mode='composition')
        
        Returns:
            Dictionary of mass flow rates for each component (no total included)
        """
        inputs = kwargs.get("inputs", dict())
        mode = kwargs.get("mode", "amount")
        total_volumetric_flow = kwargs.get("total_flow", None)
        
        if mode not in ["amount", "composition"]:
            raise ValueError("mode must be either 'amount' or 'composition'")
        if not inputs:
            raise ValueError("No inputs provided for conversion")
            
        if mode == "amount":
            # Convert volumetric flow rate amounts to mass flow rate amounts using component densities
            mass_flow_inputs = dict()
            for component in inputs:
                if component == "ethanol":
                    mass_flow_inputs[component] = inputs[component] * self.densityEthanol
                elif component == "water":
                    mass_flow_inputs[component] = inputs[component] * self.densityWater
                elif component == "sugar":
                    mass_flow_inputs[component] = inputs[component] * self.densitySugar
                elif component == "fiber":
                    mass_flow_inputs[component] = inputs[component] * self.densityFiber
                else:
                    raise ValueError(f"Unknown component: {component}")
            return mass_flow_inputs
        else:  # composition
            # Convert volumetric flow rate compositions to mass flow rate amounts using total volumetric flow rate and densities
            if total_volumetric_flow is None:
                raise ValueError("total_volumetric_flow must be provided when mode is 'composition'")
            mass_flow_inputs = dict()
            for component in inputs:
                if component == "ethanol":
                    mass_flow_inputs[component] = inputs[component] * total_volumetric_flow * self.densityEthanol
                elif component == "water":
                    mass_flow_inputs[component] = inputs[component] * total_volumetric_flow * self.densityWater
                elif component == "sugar":
                    mass_flow_inputs[component] = inputs[component] * total_volumetric_flow * self.densitySugar
                elif component == "fiber":
                    mass_flow_inputs[component] = inputs[component] * total_volumetric_flow * self.densityFiber
                else:
                    raise ValueError(f"Unknown component: {component}")
            return mass_flow_inputs
            
    
    def massToVolumetric(self, **kwargs):
        """
        Convert mass flow rates to volumetric flow rates.
        
        Args:
            inputs: Dictionary of component mass flow rates
            mode: 'amount' for absolute values or 'composition' for fractional values
            total_mass_flow: Total mass flow rate (required when mode='composition')
        
        Returns:
            Dictionary of volumetric flow rates for each component (no total included)
        """
        inputs = kwargs.get("inputs", dict())
        mode = kwargs.get("mode", "amount")
        total_mass_flow = kwargs.get("total_mass", None)
        
        if mode not in ["amount", "composition"]:
            raise ValueError("mode must be either 'amount' or 'composition'")
        if not inputs:
            raise ValueError("No inputs provided for conversion")
            
        if mode == "amount":
            # Convert mass flow rate amounts to volumetric flow rate amounts using component densities
            volumetric_flow_inputs = dict()
            for component in inputs:
                if component == "ethanol":
                    volumetric_flow_inputs[component] = inputs[component] / self.densityEthanol
                elif component == "water":
                    volumetric_flow_inputs[component] = inputs[component] / self.densityWater
                elif component == "sugar":
                    volumetric_flow_inputs[component] = inputs[component] / self.densitySugar
                elif component == "fiber":
                    volumetric_flow_inputs[component] = inputs[component] / self.densityFiber
                else:
                    raise ValueError(f"Unknown component: {component}")
            return volumetric_flow_inputs
        else:  # composition
            # Convert mass flow rate compositions to volumetric flow rate amounts using total mass flow rate and densities
            if total_mass_flow is None:
                raise ValueError("total_mass_flow must be provided when mode is 'composition'")
            volumetric_flow_inputs = dict()
            for component in inputs:
                if component == "ethanol":
                    volumetric_flow_inputs[component] = inputs[component] * total_mass_flow / self.densityEthanol
                elif component == "water":
                    volumetric_flow_inputs[component] = inputs[component] * total_mass_flow / self.densityWater
                elif component == "sugar":
                    volumetric_flow_inputs[component] = inputs[component] * total_mass_flow / self.densitySugar
                elif component == "fiber":
                    volumetric_flow_inputs[component] = inputs[component] * total_mass_flow / self.densityFiber
                else:
                    raise ValueError(f"Unknown component: {component}")
            return volumetric_flow_inputs

    
    def processMassFlow(self, **kwargs):
        """
        Process mass flow rate inputs through the system's mass flow rate function.
        Handles conversion between amounts and compositions, applies the mass flow rate function,
        and optionally stores results in logs.
        
        Args:
            inputs: Dictionary of input values (format depends on input_type)
            input_type: 'amount', 'composition', or 'full'
            output_type: 'amount', 'composition', or 'full'
            total_mass_flow: Total input mass flow rate (required for composition inputs)
            store_inputs: Whether to log input values
            store_outputs: Whether to log output values
        
        Returns:
            Processed outputs in the format specified by output_type
        """
        # Extract parameters from kwargs
        inputs = kwargs.get("inputs", dict())
        input_type = kwargs.get("input_type", "full")
        output_type = kwargs.get("output_type", "full")
        total_mass_flow = kwargs.get("total_mass", None) # Required if input_type is 'composition'

        # Determine whether to store inputs and outputs into the system logs
        store_inputs = kwargs.get("store_inputs", False)
        store_outputs = kwargs.get("store_outputs", False)
        
        # Validate inputs
        if not inputs:
            raise ValueError("No inputs provided for processing")
        elif input_type not in ["amount", "composition", "full"] or output_type not in ["amount", "composition", "full"]:
            raise ValueError("input_type and output_type must be either 'amount', 'composition', or 'full'")
        elif store_outputs and not output_type == "full":
            raise ValueError("store_outputs can only be True when output_type is 'full'")
        elif input_type == "composition" and any(key not in inputs for key in self.components):
            raise ValueError("All components must be provided when input_type is 'composition'")
        
        # Convert inputs to amounts based on input_type
        if input_type == "composition":
            # Convert fractional compositions to absolute amounts
            if total_mass_flow is None:
                raise ValueError("total_mass_flow must be provided when input_type is 'composition'")
            input_amounts = {component: inputs[component] * total_mass_flow for component in self.components}
            input_composition = inputs
        elif input_type == "amount":
            # Calculate compositions from amounts
            input_amounts = inputs.copy()
            if total_mass_flow is None:
                total_mass_flow = sum(inputs[component] for component in self.components)
            if total_mass_flow <= 0:
                raise ValueError("Total input amount must be greater than zero to calculate composition")
            input_composition = {component: input_amounts[component] / total_mass_flow for component in self.components}
        else:  # full
            # Both amounts and compositions provided
            if any(key not in inputs["composition"] for key in self.components):
                raise ValueError("All components must be provided in 'composition' when input_type is 'full'")
            input_amounts = inputs["amount"].copy()
            if total_mass_flow is None:
                total_mass_flow = sum(inputs["amount"][component] for component in self.components)
            input_composition = inputs["composition"].copy()

        # Store inputs if requested (stores to total_mass_flow and component amounts/compositions)
        if store_inputs:
            for component in self.components:
                self.input_log["mass_flow"]["amount"][component].append(input_amounts[component])
                self.input_log["mass_flow"]["composition"][component].append(input_composition[component])
            self.input_log["mass_flow"]["total_mass_flow"].append(total_mass_flow)

        # Process inputs through massFlowFunction
        output_amounts = self.massFlowFunction(input_amounts) if self.massFlowFunction else input_amounts

        # Filter out None values and calculate total output
        filtered_output = {k: v for k, v in output_amounts.items() if v is not None}
        output_total = sum(filtered_output.values())
        
        if output_type == "amount":
            # Return only component amounts (no total included)
            return filtered_output
        else: 
            # Calculate compositions for composition or full output
            if output_total <= 0:
                raise ValueError("Total output amount must be greater than zero to calculate composition")
            output_composition = {component: filtered_output[component] / output_total for component in filtered_output}
            if output_type == "composition":
                # Return only component compositions (no total)
                return output_composition
            else:  # full
                # Return both amounts and compositions, store if requested
                if store_outputs:
                    for component in filtered_output:
                        self.output_log["mass_flow"]["amount"][component].append(filtered_output[component])
                        self.output_log["mass_flow"]["composition"][component].append(output_composition[component])
                    self.output_log["mass_flow"]["total_mass_flow"].append(output_total)
                outputs = {
                    "amount": filtered_output,
                    "composition": output_composition
                }
                return outputs
    

    def processVolumetricFlow(self, **kwargs):
        """
        Process volumetric flow rate inputs through the system.
        Converts volumetric flow rate to mass flow rate, processes through mass flow rate function, then converts back to volumetric flow rate.
        
        Args:
            inputs: Dictionary of input volumetric flow rate values (format depends on input_type)
            input_type: 'amount', 'composition', or 'full'
            output_type: 'amount', 'composition', or 'full'
            total_volumetric_flow: Total input volumetric flow rate (required for composition inputs)
            store_inputs: Whether to log input values
            store_outputs: Whether to log output values
        
        Returns:
            Processed volumetric flow rate outputs in the format specified by output_type
        """
        inputs = kwargs.get("inputs", dict())
        input_type = kwargs.get("input_type", "full")
        output_type = kwargs.get("output_type", "full")
        total_volumetric_flow = kwargs.get("total_flow", None)
        store_inputs = kwargs.get("store_inputs", False)
        store_outputs = kwargs.get("store_outputs", False)

        # Convert volumetric flow rate inputs to mass flow rate inputs
        if input_type == "full":
            mass_flow_inputs = {
                "amount": self.volumetricToMass(inputs=inputs["amount"], mode="amount"),
                "composition": inputs["composition"]  # Composition is dimensionless
            }
            mass_flow_input_type = "full"
            total_mass_flow = sum(mass_flow_inputs["amount"][component] for component in self.components)
        elif input_type == "amount":
            mass_flow_inputs = self.volumetricToMass(inputs=inputs, mode="amount")
            mass_flow_input_type = "amount"
            total_mass_flow = sum(mass_flow_inputs[component] for component in self.components if component in mass_flow_inputs)
        elif input_type == "composition":
            if total_volumetric_flow is None:
                raise ValueError("total_volumetric_flow must be provided when input_type is 'composition'")
            mass_flow_inputs = self.volumetricToMass(inputs=inputs, mode="composition", total_flow=total_volumetric_flow)
            mass_flow_input_type = "amount"
            total_mass_flow = sum(mass_flow_inputs[component] for component in self.components if component in mass_flow_inputs)
        else:
            raise ValueError("input_type must be either 'amount', 'composition', or 'full'")

        # Process mass flow rate inputs (store mass flow rate data as well)
        mass_flow_outputs = self.processMassFlow(
            inputs=mass_flow_inputs,
            input_type=mass_flow_input_type,
            output_type="full",
            total_mass=total_mass_flow,
            store_inputs=store_inputs,
            store_outputs=store_outputs
        )

        # Convert mass flow rate outputs back to volumetric flow rate outputs
        volumetric_flow_output_amounts = self.massToVolumetric(inputs=mass_flow_outputs["amount"], mode="amount")
        
        # Calculate total volumetric flow rate for input storage (sum component volumetric flow rates)
        if input_type == "full":
            if total_volumetric_flow is None:
                total_volumetric_flow = sum(inputs["amount"][component] for component in self.components if component in inputs["amount"])
        elif input_type == "amount":
            if total_volumetric_flow is None:
                total_volumetric_flow = sum(inputs[component] for component in self.components if component in inputs)
        
        # Store volumetric flow rate inputs if requested (stores to total_volumetric_flow and component amounts/compositions)
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

        # Calculate total output volumetric flow rate (sum component volumetric flow rates)
        output_total_volumetric_flow = sum(volumetric_flow_output_amounts[component] for component in volumetric_flow_output_amounts)

        # Store volumetric flow rate outputs if requested (stores to total_volumetric_flow and component amounts/compositions)
        if store_outputs:
            for component in self.components:
                if component in volumetric_flow_output_amounts:
                    self.output_log["volumetric_flow"]["amount"][component].append(volumetric_flow_output_amounts[component])
                if component in mass_flow_outputs["composition"]:
                    self.output_log["volumetric_flow"]["composition"][component].append(mass_flow_outputs["composition"][component])
            self.output_log["volumetric_flow"]["total_volumetric_flow"].append(output_total_volumetric_flow)

        # Format output based on output_type
        if output_type == "amount":
            return volumetric_flow_output_amounts
        elif output_type == "composition":
            return mass_flow_outputs["composition"]  # Composition is the same for mass flow rate and volumetric flow rate
        else:  # full
            return {
                "amount": volumetric_flow_output_amounts,
                "composition": mass_flow_outputs["composition"]
            }
    

    def processEnergyConsumption(self, **kwargs):
        """
        Calculate energy consumed over a time interval.
        
        Args:
            store_energy: Whether to log the energy consumed
            interval: Time interval in seconds (default: 1 second)
        
        Returns:
            Energy consumed over the interval in Joules
        """
        store_energy = kwargs.get("store_energy", False)
        interval = kwargs.get("interval", 1)  # Default to 1 second if not specified
        energy_consumed_in_interval = self.energy_consumption_rate * interval  # Energy consumed over the interval in Joules
        if store_energy:
            self.energy_consumed_log.append(energy_consumed_in_interval)
        return energy_consumed_in_interval

    
    def iterateMassFlowInputs(self, inputValues=dict(), **kwargs):
        """
        Process multiple sets of mass flow rate inputs iteratively.
        Processes each input through the mass flow rate function and stores results in logs.
        
        Args:
            inputValues: Dictionary containing input data. Format depends on input_type:
                - For 'amount': {component: [list of values]}
                - For 'composition': {component: [list of fractions]} + total_mass_flow_list
                - For 'full': {"amount": {component: [values]}, "composition": {component: [fractions]}}
            input_type: 'amount', 'composition', or 'full'
            output_type: 'amount', 'composition', or 'full'
            total_mass_flow_list: List of total mass flow rates (required when input_type is 'composition')
        
        Returns:
            Updated output log containing all processed results
        """
        input_type = kwargs.get("input_type", "amount")
        output_type = kwargs.get("output_type", "full")
        total_mass_flow_list = kwargs.get("total_mass_list", None)
        
        # Validate input_type
        if input_type not in ["amount", "composition", "full"]:
            raise ValueError("input_type must be either 'amount', 'composition', or 'full'")
        
        # Determine number of iterations based on input structure
        if input_type == "full":
            num_iterations = len(inputValues["amount"][self.components[0]])
        else:
            num_iterations = len(inputValues[self.components[0]])
        
        # Validate total_mass_flow_list if required
        if input_type == "composition":
            if total_mass_flow_list is None:
                raise ValueError("total_mass_flow_list must be provided when input_type is 'composition'")
            if len(total_mass_flow_list) != num_iterations:
                raise ValueError("Length of total_mass_flow_list must match number of input sets")
        
        # Process each set of inputs
        for i in range(num_iterations):
            # Build input dictionary for this iteration
            if input_type == "amount":
                input_dict = {component: inputValues[component][i] for component in self.components if component in inputValues}
                total_mass_flow = None
            elif input_type == "composition":
                input_dict = {component: inputValues[component][i] for component in self.components if component in inputValues}
                total_mass_flow = total_mass_flow_list[i]
            else:  # full
                input_dict = {
                    "amount": {component: inputValues["amount"][component][i] for component in self.components if component in inputValues["amount"]},
                    "composition": {component: inputValues["composition"][component][i] for component in self.components if component in inputValues["composition"]}
                }
                total_mass_flow = None
            
            # Process this input set
            self.processMassFlow(
                inputs=input_dict,
                input_type=input_type,
                output_type=output_type,
                total_mass=total_mass_flow,
                store_inputs=True,
                store_outputs=True
            )
        
        return self.output_log
    

    def iterateVolumetricFlowInputs(self, inputValues=dict(), **kwargs):
        """
        Process multiple sets of volumetric flow rate inputs iteratively.
        Processes each input through the volumetric flow rate function and stores results in logs.
        
        Args:
            inputValues: Dictionary containing input data. Format depends on input_type:
                - For 'amount': {component: [list of values]}
                - For 'composition': {component: [list of fractions]} + total_volumetric_flow_list
                - For 'full': {"amount": {component: [values]}, "composition": {component: [fractions]}}
            input_type: 'amount', 'composition', or 'full'
            output_type: 'amount', 'composition', or 'full'
            total_volumetric_flow_list: List of total volumetric flow rates (required when input_type is 'composition')
        
        Returns:
            Updated output log containing all processed results
        """        
        input_type = kwargs.get("input_type", "amount")
        output_type = kwargs.get("output_type", "full")
        total_volumetric_flow_list = kwargs.get("total_flow_list", None)
        
        # Validate input_type
        if input_type not in ["amount", "composition", "full"]:
            raise ValueError("input_type must be either 'amount', 'composition', or 'full'")
        
        # Determine number of iterations based on input structure
        if input_type == "full":
            num_iterations = len(inputValues["amount"][self.components[0]])
        else:
            num_iterations = len(inputValues[self.components[0]])
        
        # Validate total_volumetric_flow_list if required
        if input_type == "composition":
            if total_volumetric_flow_list is None:
                raise ValueError("total_volumetric_flow_list must be provided when input_type is 'composition'")
            if len(total_volumetric_flow_list) != num_iterations:
                raise ValueError("Length of total_volumetric_flow_list must match number of input sets")
        
        # Process each set of inputs
        for i in range(num_iterations):
            # Build input dictionary for this iteration
            if input_type == "amount":
                input_dict = {component: inputValues[component][i] for component in self.components if component in inputValues}
                total_volumetric_flow = None
            elif input_type == "composition":
                input_dict = {component: inputValues[component][i] for component in self.components if component in inputValues}
                total_volumetric_flow = total_volumetric_flow_list[i]
            else:  # full
                input_dict = {
                    "amount": {component: inputValues["amount"][component][i] for component in self.components if component in inputValues["amount"]},
                    "composition": {component: inputValues["composition"][component][i] for component in self.components if component in inputValues["composition"]}
                }
                total_volumetric_flow = None
            
            # Process this input set
            self.processVolumetricFlow(
                inputs=input_dict,
                input_type=input_type,
                output_type=output_type,
                total_flow=total_volumetric_flow,
                store_inputs=True,
                store_outputs=True
            )
        
        return self.output_log
        

    def iterateInputs(self, inputValues=dict(), **kwargs):
        """
        Process multiple sets of inputs iteratively.
        Appends each input to the log and processes it through the mass flow rate function.
        
        Args:
            inputValues: Dictionary containing lists of input values for each component
        
        Returns:
            Updated output log containing all processed results
        """
        # Appends input values to the inputs dictionary
        for key in inputValues:
            self.input_log[key] += inputValues[key]

        # Process each set of inputs and appends to outputs
        for i in range(len(inputValues["ethanol"])):
            input_dict = {key: inputValues[key][i] for key in inputValues}
            output_dict = self.massFlowFunction(input_dict)
            for key in self.output_log:
                self.output_log[key].append(output_dict[key])

        return self.output_log 

    
    def display(self, input=str, output=str):
        """
        Display a plot of input vs output relationship.
        
        Args:
            input: Name of the input variable to plot on x-axis
            output: Name of the output variable to plot on y-axis
        """
        plt.plot(self.input_log[input], self.output_log[output], linestyle='--', marker='o')
        plt.title(f"{self.name} System: {input} vs {output}")
        plt.xlabel(f"Input {input} (units)")
        plt.ylabel(f"Output {output} (units)")
        plt.grid(True)
        plt.show()

