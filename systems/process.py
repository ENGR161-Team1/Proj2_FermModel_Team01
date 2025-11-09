import matplotlib
import matplotlib.pyplot as plt


class Process:
    """
    Base class for modeling chemical processing systems in an ethanol plant.
    
    This class provides comprehensive functionality for:
    - Tracking and logging mass flow rates and volumetric flow rates
    - Converting between mass and volumetric flow representations
    - Processing chemical component flows through custom transformation functions
    - Monitoring power consumption and associated costs
    - Handling compositional analysis of multi-component mixtures
    
    The class maintains detailed logs of inputs, outputs, and resource consumption
    for process analysis and optimization.
    """
    
    # Density constants for component conversion between mass and volume (kg/m³)
    # These values are at standard conditions (typically 20°C, 1 atm)
    DENSITY_WATER = 997    # Water density (kg/m³)
    DENSITY_ETHANOL = 789  # Ethanol density (kg/m³)
    DENSITY_SUGAR = 1590   # Sugar (sucrose) density (kg/m³)
    DENSITY_FIBER = 1311   # Fiber (cellulose) density (kg/m³)
    
    def __init__(self, **kwargs):
        """
        Initialize a Process with configuration parameters and logging structures.
        
        Sets up comprehensive tracking for mass flow, volumetric flow, power consumption,
        and cost data. Initializes density constants for common ethanol plant components.
        
        Args:
            name (str, optional): Descriptive name for this process unit. Default is "Process".
            efficiency (float, optional): Process efficiency factor between 0 and 1. Default is 1.0.
            massFlowFunction (callable, optional): Custom function to transform input mass flows
                to output mass flows. Should accept a dict of component mass flows and return
                a dict of output mass flows. If None, acts as a pass-through.
            power_consumption_rate (float, optional): Power consumption rate. Default is 0.
                Units depend on power_consumption_unit parameter.
            power_consumption_unit (str, optional): Unit for power consumption rate.
                Options: "kWh/day", "kWh/hour"/"kW", or "W". Default is "kWh/day".
            cost (float, optional): Fixed cost per unit in USD. Default is 0.
            cost_per_flow (float, optional): Variable cost per m³/s of flow processed in USD. Default is 0.
        """
        self.name = kwargs.get("name", "Process")
        
        # Initialize input log structure for tracking all input data
        # Separates mass flow and volumetric flow measurements
        # For each flow type, tracks total flow, individual component amounts, and compositions
        self.input_log = {
            "mass_flow": {
                "total_mass_flow": [],  # Total mass flow rate at each time step (kg/s)
                "amount": {
                    "ethanol": [],  # Ethanol mass flow rate (kg/s)
                    "water": [],    # Water mass flow rate (kg/s)
                    "sugar": [],    # Sugar mass flow rate (kg/s)
                    "fiber": []     # Fiber mass flow rate (kg/s)
                }, 
                "composition": {
                    "ethanol": [],  # Ethanol mass fraction (dimensionless, 0-1)
                    "water": [],    # Water mass fraction (dimensionless, 0-1)
                    "sugar": [],    # Sugar mass fraction (dimensionless, 0-1)
                    "fiber": []     # Fiber mass fraction (dimensionless, 0-1)
                }
            },
            "volumetric_flow": {
                "total_volumetric_flow": [],  # Total volumetric flow rate at each time step (m³/s)
                "amount": {
                    "ethanol": [],  # Ethanol volumetric flow rate (m³/s)
                    "water": [],    # Water volumetric flow rate (m³/s)
                    "sugar": [],    # Sugar volumetric flow rate (m³/s)
                    "fiber": []     # Fiber volumetric flow rate (m³/s)
                }, 
                "composition": {
                    "ethanol": [],  # Ethanol volumetric fraction (dimensionless, 0-1)
                    "water": [],    # Water volumetric fraction (dimensionless, 0-1)
                    "sugar": [],    # Sugar volumetric fraction (dimensionless, 0-1)
                    "fiber": []     # Fiber volumetric fraction (dimensionless, 0-1)
                }
            },
        }
        
        # Initialize output log with same structure as input log
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
        
        # Initialize consumption log for tracking power, energy, and cost
        self.consumption_log = {
            "power_consumption_rate": [],  # Instantaneous power consumption at each time step (W)
            "energy_consumed": [],         # Energy consumed in each time interval (J)
            "interval": [],                # Duration of each time interval (s)
            "cost_per_unit_flow": [],      # Cost per unit volumetric flow at each time step ($/m³/s)
            "cost_incurred": []            # Total cost incurred for processing this flow ($)
        }
        
        # Set up power consumption with automatic unit conversion to Watts
        self.power_consumption_rate = kwargs.get("power_consumption_rate", 0)
        power_consumption_unit = kwargs.get("power_consumption_unit", "kWh/day")
        
        # Convert all power consumption rates to Watts for internal calculations
        if power_consumption_unit == "kWh/day":
            self.power_consumption_rate /= 24  # Convert kWh/day to kWh/hour (kW)
            self.power_consumption_rate *= 1000  # Convert kW to W
        if power_consumption_unit == "kWh/hour" or power_consumption_unit == "kW":
            self.power_consumption_rate *= 1000  # Convert kW to W
        # If already in W, no conversion needed
        
        # Cost parameters for economic analysis
        self.cost = kwargs.get("cost", 0)  # Fixed cost per unit operation (USD)
        self.cost_per_flow = kwargs.get("cost_per_flow", 0)  # Variable cost per unit flow (USD/(m³/s))

        # List of all chemical components tracked in this process
        self.components = ["ethanol", "water", "sugar", "fiber"]
        
        # Process efficiency factor (0 to 1, where 1 is 100% efficient)
        self.efficiency = kwargs.get("efficiency", 1.0)
        
        # Custom transformation function for mass flow processing
        # If None, process acts as a pass-through (output = input)
        self.massFlowFunction = kwargs.get("massFlowFunction", None)

    def volumetricToMass(self, **kwargs):
        """
        Convert volumetric flow rates to mass flow rates using component densities.
        
        This method handles two modes of operation:
        1. 'amount' mode: Converts absolute volumetric flow rates to mass flow rates
        2. 'composition' mode: Converts volumetric fractions with total flow to mass flow rates
        
        The conversion uses the relationship: mass_flow = volumetric_flow × density
        
        Args:
            inputs (dict): Dictionary of component volumetric flow rates or fractions.
                Keys should be component names from self.components.
            mode (str, optional): Conversion mode - either 'amount' or 'composition'. Default is 'amount'.
            total_flow (float, optional): Total volumetric flow rate in m³/s.
                Required when mode='composition'.
        
        Returns:
            dict: Dictionary of mass flow rates for each component in kg/s.
                Does not include a 'total' key.
        
        Raises:
            ValueError: If mode is not 'amount' or 'composition'.
            ValueError: If no inputs are provided.
            ValueError: If total_flow is not provided when mode='composition'.
            ValueError: If an unknown component is encountered.
        """
        inputs = kwargs.get("inputs", dict())
        mode = kwargs.get("mode", "amount")
        total_volumetric_flow = kwargs.get("total_flow", None)
        
        if mode not in ["amount", "composition"]:
            raise ValueError("mode must be either 'amount' or 'composition'")
        if not inputs:
            raise ValueError("No inputs provided for conversion")
            
        if mode == "amount":
            # Direct conversion: mass_flow = volumetric_flow × density
            mass_flow_inputs = dict()
            for component in inputs:
                if component == "ethanol":
                    mass_flow_inputs[component] = inputs[component] * self.DENSITY_ETHANOL
                elif component == "water":
                    mass_flow_inputs[component] = inputs[component] * self.DENSITY_WATER
                elif component == "sugar":
                    mass_flow_inputs[component] = inputs[component] * self.DENSITY_SUGAR
                elif component == "fiber":
                    mass_flow_inputs[component] = inputs[component] * self.DENSITY_FIBER
                else:
                    raise ValueError(f"Unknown component: {component}")
            return mass_flow_inputs
        else:  # composition mode
            # Convert fractions to amounts: mass_flow = fraction × total_flow × density
            if total_volumetric_flow is None:
                raise ValueError("total_volumetric_flow must be provided when mode is 'composition'")
            mass_flow_inputs = dict()
            for component in inputs:
                if component == "ethanol":
                    mass_flow_inputs[component] = inputs[component] * total_volumetric_flow * self.DENSITY_ETHANOL
                elif component == "water":
                    mass_flow_inputs[component] = inputs[component] * total_volumetric_flow * self.DENSITY_WATER
                elif component == "sugar":
                    mass_flow_inputs[component] = inputs[component] * total_volumetric_flow * self.DENSITY_SUGAR
                elif component == "fiber":
                    mass_flow_inputs[component] = inputs[component] * total_volumetric_flow * self.DENSITY_FIBER
                else:
                    raise ValueError(f"Unknown component: {component}")
            return mass_flow_inputs
    
    def massToVolumetric(self, **kwargs):
        """
        Convert mass flow rates to volumetric flow rates using component densities.
        
        This method handles two modes of operation:
        1. 'amount' mode: Converts absolute mass flow rates to volumetric flow rates
        2. 'composition' mode: Converts mass fractions with total mass flow to volumetric flow rates
        
        The conversion uses the relationship: volumetric_flow = mass_flow / density
        
        Args:
            inputs (dict): Dictionary of component mass flow rates or fractions.
                Keys should be component names from self.components.
            mode (str, optional): Conversion mode - either 'amount' or 'composition'. Default is 'amount'.
            total_mass (float, optional): Total mass flow rate in kg/s.
                Required when mode='composition'.
        
        Returns:
            dict: Dictionary of volumetric flow rates for each component in m³/s.
                Does not include a 'total' key.
        
        Raises:
            ValueError: If mode is not 'amount' or 'composition'.
            ValueError: If no inputs are provided.
            ValueError: If total_mass is not provided when mode='composition'.
            ValueError: If an unknown component is encountered.
        """
        inputs = kwargs.get("inputs", dict())
        mode = kwargs.get("mode", "amount")
        total_mass_flow = kwargs.get("total_mass", None)
        
        if mode not in ["amount", "composition"]:
            raise ValueError("mode must be either 'amount' or 'composition'")
        if not inputs:
            raise ValueError("No inputs provided for conversion")
            
        if mode == "amount":
            # Direct conversion: volumetric_flow = mass_flow / density
            volumetric_flow_inputs = dict()
            for component in inputs:
                if component == "ethanol":
                    volumetric_flow_inputs[component] = inputs[component] / self.DENSITY_ETHANOL
                elif component == "water":
                    volumetric_flow_inputs[component] = inputs[component] / self.DENSITY_WATER
                elif component == "sugar":
                    volumetric_flow_inputs[component] = inputs[component] / self.DENSITY_SUGAR
                elif component == "fiber":
                    volumetric_flow_inputs[component] = inputs[component] / self.DENSITY_FIBER
                else:
                    raise ValueError(f"Unknown component: {component}")
            return volumetric_flow_inputs
        else:  # composition mode
            # Convert fractions to amounts: volumetric_flow = fraction × total_mass / density
            if total_mass_flow is None:
                raise ValueError("total_mass_flow must be provided when mode is 'composition'")
            volumetric_flow_inputs = dict()
            for component in inputs:
                if component == "ethanol":
                    volumetric_flow_inputs[component] = inputs[component] * total_mass_flow / self.DENSITY_ETHANOL
                elif component == "water":
                    volumetric_flow_inputs[component] = inputs[component] * total_mass_flow / self.DENSITY_WATER
                elif component == "sugar":
                    volumetric_flow_inputs[component] = inputs[component] * total_mass_flow / self.DENSITY_SUGAR
                elif component == "fiber":
                    volumetric_flow_inputs[component] = inputs[component] * total_mass_flow / self.DENSITY_FIBER
                else:
                    raise ValueError(f"Unknown component: {component}")
            return volumetric_flow_inputs

    
    def processMassFlow(self, **kwargs):
        """
        Process mass flow rate inputs through the system's transformation function.
        
        This is the core processing method for mass flow operations. It:
        1. Normalizes inputs to both amounts and compositions
        2. Applies the custom massFlowFunction to transform inputs
        3. Calculates output totals and compositions
        4. Optionally logs inputs, outputs, and costs
        
        Supports flexible input/output formats: amounts only, compositions only, or both.
        
        Args:
            inputs (dict): Dictionary of input values. Format depends on input_type:
                - 'amount': {component: value} for each component
                - 'composition': {component: fraction} for each component (must sum to 1)
                - 'full': {"amount": {...}, "composition": {...}}
            input_type (str, optional): Format of inputs - 'amount', 'composition', or 'full'.
                Default is 'full'.
            output_type (str, optional): Format of outputs - 'amount', 'composition', or 'full'.
                Default is 'full'.
            total_mass (float, optional): Total input mass flow rate in kg/s.
                Required when input_type='composition'.
            store_inputs (bool, optional): Whether to log input values. Default is False.
            store_outputs (bool, optional): Whether to log output values. Default is False.
                Can only be True when output_type='full'.
            store_cost (bool, optional): Whether to log cost data. Default is False.
        
        Returns:
            dict: Processed outputs in the format specified by output_type:
                - 'amount': {component: value}
                - 'composition': {component: fraction}
                - 'full': {"amount": {...}, "composition": {...}}
        
        Raises:
            ValueError: If inputs are invalid or missing required parameters.
            ValueError: If attempting to store_outputs with non-'full' output_type.
        """
        # Extract parameters from kwargs
        inputs = kwargs.get("inputs", dict())
        input_type = kwargs.get("input_type", "full")
        output_type = kwargs.get("output_type", "full")
        total_mass_flow = kwargs.get("total_mass", None) # Required if input_type is 'composition'

        # Determine whether to store inputs and outputs into the system logs
        store_inputs = kwargs.get("store_inputs", False)
        store_outputs = kwargs.get("store_outputs", False)
        store_cost = kwargs.get("store_cost", False)
        
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
            # Multiply each composition fraction by total flow to get absolute amounts
            input_amounts = {component: inputs[component] * total_mass_flow for component in self.components}
            input_composition = inputs
        elif input_type == "amount":
            # Calculate compositions from amounts
            input_amounts = inputs.copy()
            # Calculate total if not provided
            if total_mass_flow is None:
                total_mass_flow = sum(inputs[component] for component in self.components)
            if total_mass_flow <= 0:
                raise ValueError("Total input amount must be greater than zero to calculate composition")
            # Calculate fractional composition of each component
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

        # Calculate and store cost if requested
        if store_cost:
            # Convert mass flow to volumetric flow for cost calculation (cost is per volume)
            volumetric_flow_for_cost = self.massToVolumetric(inputs=input_amounts, mode="amount")
            total_volumetric_flow = sum(volumetric_flow_for_cost.values())
            cost_incurred = self.cost_per_flow * total_volumetric_flow
            
            self.consumption_log["cost_per_unit_flow"].append(self.cost_per_flow)
            self.consumption_log["cost_incurred"].append(cost_incurred)

        # Apply the mass flow transformation function (or pass-through if None)
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
            # Calculate fractional composition of each output component
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
        
        This method provides a volumetric interface to the mass-based processing system:
        1. Converts volumetric inputs to mass flow rates
        2. Processes through processMassFlow()
        3. Converts mass outputs back to volumetric flow rates
        4. Handles logging for both volumetric and mass representations
        
        This allows the system to work with volumetric measurements while maintaining
        mass-based transformations internally.
        
        Args:
            inputs (dict): Dictionary of input volumetric flow rates. Format depends on input_type:
                - 'amount': {component: value} in m³/s
                - 'composition': {component: fraction} (dimensionless)
                - 'full': {"amount": {...}, "composition": {...}}
            input_type (str, optional): Format of inputs - 'amount', 'composition', or 'full'.
                Default is 'full'.
            output_type (str, optional): Format of outputs - 'amount', 'composition', or 'full'.
                Default is 'full'.
            total_flow (float, optional): Total input volumetric flow rate in m³/s.
                Required when input_type='composition'.
            store_inputs (bool, optional): Whether to log input values. Default is False.
            store_outputs (bool, optional): Whether to log output values. Default is False.
            store_cost (bool, optional): Whether to log cost data. Default is False.
        
        Returns:
            dict: Processed volumetric flow rate outputs in the format specified by output_type:
                - 'amount': {component: value} in m³/s
                - 'composition': {component: fraction}
                - 'full': {"amount": {...}, "composition": {...}}
        
        Raises:
            ValueError: If input_type is not valid.
            ValueError: If total_flow is not provided when input_type='composition'.
        """
        inputs = kwargs.get("inputs", dict())
        input_type = kwargs.get("input_type", "full")
        output_type = kwargs.get("output_type", "full")
        total_volumetric_flow = kwargs.get("total_flow", None)
        store_inputs = kwargs.get("store_inputs", False)
        store_outputs = kwargs.get("store_outputs", False)
        store_cost = kwargs.get("store_cost", False)

        # Convert volumetric flow rate inputs to mass flow rate inputs
        if input_type == "full":
            # Convert volumetric amounts to mass amounts, keep compositions unchanged
            mass_flow_inputs = {
                "amount": self.volumetricToMass(inputs=inputs["amount"], mode="amount"),
                "composition": inputs["composition"]  # Composition is dimensionless
            }
            mass_flow_input_type = "full"
            total_mass_flow = sum(mass_flow_inputs["amount"][component] for component in self.components)
        elif input_type == "amount":
            # Convert volumetric amounts to mass amounts
            mass_flow_inputs = self.volumetricToMass(inputs=inputs, mode="amount")
            mass_flow_input_type = "amount"
            total_mass_flow = sum(mass_flow_inputs[component] for component in self.components if component in mass_flow_inputs)
        elif input_type == "composition":
            if total_volumetric_flow is None:
                raise ValueError("total_volumetric_flow must be provided when input_type is 'composition'")
            # Convert volumetric compositions to mass amounts
            mass_flow_inputs = self.volumetricToMass(inputs=inputs, mode="composition", total_flow=total_volumetric_flow)
            mass_flow_input_type = "amount"
            total_mass_flow = sum(mass_flow_inputs[component] for component in self.components if component in mass_flow_inputs)
        else:
            raise ValueError("input_type must be either 'amount', 'composition', or 'full'")

        # Process mass flow rate inputs (store mass flow rate data as well)
        mass_flow_outputs = self.processMassFlow(
            inputs=mass_flow_inputs,
            input_type=mass_flow_input_type,
            output_type="full",  # Always get full output for conversion back to volumetric
            total_mass=total_mass_flow,
            store_inputs=store_inputs,
            store_outputs=store_outputs,
            store_cost=False  # Cost handling done separately in this method
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
                # Store both amounts and compositions from full input
                for component in self.components:
                    if component in inputs["amount"]:
                        self.input_log["volumetric_flow"]["amount"][component].append(inputs["amount"][component])
                    if component in inputs["composition"]:
                        self.input_log["volumetric_flow"]["composition"][component].append(inputs["composition"][component])
                self.input_log["volumetric_flow"]["total_volumetric_flow"].append(total_volumetric_flow)
            elif input_type == "amount":
                # Store amounts and calculate compositions from amounts
                for component in self.components:
                    if component in inputs:
                        self.input_log["volumetric_flow"]["amount"][component].append(inputs[component])
                        self.input_log["volumetric_flow"]["composition"][component].append(inputs[component] / total_volumetric_flow if total_volumetric_flow > 0 else 0)
                self.input_log["volumetric_flow"]["total_volumetric_flow"].append(total_volumetric_flow)
            elif input_type == "composition":
                # Store compositions and calculate amounts from compositions
                for component in self.components:
                    if component in inputs:
                        self.input_log["volumetric_flow"]["composition"][component].append(inputs[component])
                        self.input_log["volumetric_flow"]["amount"][component].append(inputs[component] * total_volumetric_flow)
                self.input_log["volumetric_flow"]["total_volumetric_flow"].append(total_volumetric_flow)

        # Calculate and store cost if requested (based on volumetric flow)
        if store_cost:
            cost_incurred = self.cost_per_flow * total_volumetric_flow
            
            self.consumption_log["cost_per_unit_flow"].append(self.cost_per_flow)
            self.consumption_log["cost_incurred"].append(cost_incurred)

        # Calculate total output volumetric flow rate (sum component volumetric flow rates)
        output_total_volumetric_flow = sum(volumetric_flow_output_amounts[component] for component in volumetric_flow_output_amounts)

        # Store volumetric flow rate outputs if requested (stores to total_volumetric_flow and component amounts/compositions)
        if store_outputs:
            for component in self.components:
                if component in volumetric_flow_output_amounts:
                    self.output_log["volumetric_flow"]["amount"][component].append(volumetric_flow_output_amounts[component])
                if component in mass_flow_outputs["composition"]:
                    # Composition is the same for mass and volumetric flow
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
    

    def processPowerConsumption(self, **kwargs):
        """
        Calculate energy consumed over a time interval based on power consumption rate.
        
        Uses the fundamental relationship: Energy = Power × Time
        This allows tracking of cumulative energy consumption over process operation.
        
        Args:
            store_energy (bool, optional): Whether to log the power and energy data. Default is False.
            interval (float, optional): Time interval in seconds over which to calculate energy.
                Default is 1 second.
        
        Returns:
            float: Energy consumed over the interval in Joules (J).
                Note: 1 J = 1 W·s
        """
        store_energy = kwargs.get("store_energy", False)
        interval = kwargs.get("interval", 1)  # Default interval of 1 second
        
        # Calculate energy: E (J) = P (W) × t (s)
        energy_consumed_in_interval = self.power_consumption_rate * interval
        
        if store_energy:
            # Log instantaneous power consumption rate (W)
            self.consumption_log["power_consumption_rate"].append(self.power_consumption_rate)
            
            # Log energy consumed during this specific interval (J)
            self.consumption_log["energy_consumed"].append(energy_consumed_in_interval)
            
            # Log the duration of this time interval (s)
            self.consumption_log["interval"].append(interval)
        
        return energy_consumed_in_interval

    
    def iterateMassFlowInputs(self, inputValues=dict(), **kwargs):
        """
        Process multiple sets of mass flow rate inputs iteratively over time.
        
        This method enables batch processing of time-series or parametric study data.
        Each set of inputs is processed sequentially through the mass flow function,
        with all results automatically logged for analysis.
        
        Useful for:
        - Simulating process operation over time
        - Conducting parametric sensitivity studies
        - Analyzing batch operations
        
        Args:
            inputValues (dict): Dictionary containing lists of input data. Format depends on input_type:
                - 'amount': {component: [value1, value2, ...]} for each component
                - 'composition': {component: [fraction1, fraction2, ...]} for each component
                - 'full': {"amount": {component: [values]}, "composition": {component: [fractions]}}
            input_type (str, optional): Format of inputs - 'amount', 'composition', or 'full'.
                Default is 'amount'.
            output_type (str, optional): Format of outputs - 'amount', 'composition', or 'full'.
                Default is 'full'.
            total_mass_list (list, optional): List of total mass flow rates in kg/s.
                Required when input_type='composition'. Length must match number of input sets.
        
        Returns:
            dict: Updated output_log containing all processed results with same structure as self.output_log.
        
        Raises:
            ValueError: If input_type is not valid.
            ValueError: If total_mass_list is missing when required.
            ValueError: If total_mass_list length doesn't match input length.
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
        
        # Process each set of inputs sequentially
        for i in range(num_iterations):
            # Build input dictionary for this iteration
            if input_type == "amount":
                # Extract amounts for each component at index i
                input_dict = {component: inputValues[component][i] for component in self.components if component in inputValues}
                total_mass_flow = None
            elif input_type == "composition":
                # Extract compositions for each component at index i
                input_dict = {component: inputValues[component][i] for component in self.components if component in inputValues}
                total_mass_flow = total_mass_flow_list[i]
            else:  # full
                # Extract both amounts and compositions at index i
                input_dict = {
                    "amount": {component: inputValues["amount"][component][i] for component in self.components if component in inputValues["amount"]},
                    "composition": {component: inputValues["composition"][component][i] for component in self.components if component in inputValues["composition"]}
                }
                total_mass_flow = None
            
            # Process this input set and automatically store results in logs
            self.processMassFlow(
                inputs=input_dict,
                input_type=input_type,
                output_type=output_type,
                total_mass=total_mass_flow,
                store_inputs=True,   # Always store for iteration methods
                store_outputs=True   # Always store for iteration methods
            )
        
        return self.output_log
    

    def iterateVolumetricFlowInputs(self, inputValues=dict(), **kwargs):
        """
        Process multiple sets of volumetric flow rate inputs iteratively over time.
        
        Similar to iterateMassFlowInputs but for volumetric data. Each set of volumetric
        inputs is converted to mass, processed, and converted back, with both mass and
        volumetric representations logged.
        
        Useful for:
        - Processing field measurement data (often volumetric)
        - Time-series simulation with volumetric meters
        - Parametric studies with volumetric constraints
        
        Args:
            inputValues (dict): Dictionary containing lists of input data. Format depends on input_type:
                - 'amount': {component: [value1, value2, ...]} in m³/s
                - 'composition': {component: [fraction1, fraction2, ...]} (dimensionless)
                - 'full': {"amount": {component: [values]}, "composition": {component: [fractions]}}
            input_type (str, optional): Format of inputs - 'amount', 'composition', or 'full'.
                Default is 'amount'.
            output_type (str, optional): Format of outputs - 'amount', 'composition', or 'full'.
                Default is 'full'.
            total_flow_list (list, optional): List of total volumetric flow rates in m³/s.
                Required when input_type='composition'. Length must match number of input sets.
        
        Returns:
            dict: Updated output_log containing all processed results with same structure as self.output_log.
        
        Raises:
            ValueError: If input_type is not valid.
            ValueError: If total_flow_list is missing when required.
            ValueError: If total_flow_list length doesn't match input length.
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
        
        # Process each set of inputs sequentially
        for i in range(num_iterations):
            # Build input dictionary for this iteration
            if input_type == "amount":
                # Extract amounts for each component at index i
                input_dict = {component: inputValues[component][i] for component in self.components if component in inputValues}
                total_volumetric_flow = None
            elif input_type == "composition":
                # Extract compositions for each component at index i
                input_dict = {component: inputValues[component][i] for component in self.components if component in inputValues}
                total_volumetric_flow = total_volumetric_flow_list[i]
            else:  # full
                # Extract both amounts and compositions at index i
                input_dict = {
                    "amount": {component: inputValues["amount"][component][i] for component in self.components if component in inputValues["amount"]},
                    "composition": {component: inputValues["composition"][component][i] for component in self.components if component in inputValues["composition"]}
                }
                total_volumetric_flow = None
            
            # Process this input set and automatically store results in logs
            self.processVolumetricFlow(
                inputs=input_dict,
                input_type=input_type,
                output_type=output_type,
                total_flow=total_volumetric_flow,
                store_inputs=True,   # Always store for iteration methods
                store_outputs=True   # Always store for iteration methods
            )
        
        return self.output_log
        

    def iterateInputs(self, inputValues=dict(), **kwargs):
        """
        Legacy method for processing multiple sets of inputs iteratively.
        
        Note: This is a simplified legacy interface. For new code, prefer using
        iterateMassFlowInputs() or iterateVolumetricFlowInputs() which provide
        more flexible input/output formats and better logging capabilities.
        
        Args:
            inputValues (dict): Dictionary containing lists of input values for each component.
                Format: {component: [value1, value2, ...]}
        
        Returns:
            dict: Updated output_log containing all processed results.
        """
        # Append all input values to the input log
        for key in inputValues:
            self.input_log[key] += inputValues[key]

        # Process each set of inputs through the mass flow function
        for i in range(len(inputValues["ethanol"])):
            # Extract inputs for this iteration
            input_dict = {key: inputValues[key][i] for key in inputValues}
            
            # Apply mass flow transformation function
            output_dict = self.massFlowFunction(input_dict)
            
            # Append outputs to output log
            for key in self.output_log:
                self.output_log[key].append(output_dict[key])

        return self.output_log 

    
    def display(self, input=str, output=str):
        """
        Display a scatter plot showing the relationship between input and output variables.
        
        This visualization method helps analyze:
        - Input-output relationships
        - Process linearity or non-linearity
        - Process trends over time
        
        Args:
            input (str): Name of the input variable to plot on x-axis.
                Must be a key in self.input_log.
            output (str): Name of the output variable to plot on y-axis.
                Must be a key in self.output_log.
        
        Note:
            Creates a matplotlib plot with grid and displays it. The plot style uses
            dashed lines with circle markers for clear visualization of discrete data points.
        """
        # Create scatter plot with line connecting points
        plt.plot(self.input_log[input], self.output_log[output], linestyle='--', marker='o')
        
        # Set descriptive title and axis labels
        plt.title(f"{self.name} System: {input} vs {output}")
        plt.xlabel(f"Input {input} (units)")
        plt.ylabel(f"Output {output} (units)")
        
        # Add grid for easier reading of values
        plt.grid(True)
        
        # Display the plot
        plt.show()

