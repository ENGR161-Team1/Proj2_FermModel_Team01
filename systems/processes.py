import matplotlib
import matplotlib.pyplot as plt
# matplotlib.use("gtk4agg") --- IGNORE ---

class System:
    def __init__(self, **kwargs):
        self.name = kwargs.get("name", "System")
        self.input_log = {
            "mass": {
                "amount": {
                    "ethanol": [],
                    "water": [],
                    "sugar": [],
                    "fiber": [],
                    "total": []
                },
                "composition": {
                    "ethanol": [],
                    "water": [],
                    "sugar": [],
                    "fiber": []
                }
            },
            "flow": {
                "amount": {
                    "ethanol": [],
                    "water": [],
                    "sugar": [],
                    "fiber": [],
                    "total": []
                },
                "composition": {
                    "ethanol": [],
                    "water": [],
                    "sugar": [],
                    "fiber": []
                }
            }
        }
        self.output_log = {
            "mass": {
                "amount": {
                    "ethanol": [],
                    "water": [],
                    "sugar": [],
                    "fiber": [],
                    "total": []
                },
                "composition": {
                    "ethanol": [],
                    "water": [],
                    "sugar": [],
                    "fiber": []
                },
            },
            "flow": {
                "amount": {
                    "ethanol": [],
                    "water": [],
                    "sugar": [],
                    "fiber": [],
                    "total": []
                },
                "composition": {
                    "ethanol": [],
                    "water": [],
                    "sugar": [],
                    "fiber": []
                },
            }
        }
        self.efficiency = kwargs.get("efficiency", 1.0)
        self.massFunction = kwargs.get("massFunction", None)
        self.densityWater = 997  # kg/m^3
        self.densityEthanol = 789  # kg/m^3
        self.densitySugar = 1590  # kg/m^3
        self.densityFiber = 1311  # kg/m^3

    def flowToMass(self, **kwargs):
        inputs = kwargs.get("inputs", dict())
        mode = kwargs.get("mode", "amount")
        total_flow = kwargs.get("total_flow", None)
        if mode not in ["amount", "composition"]:
            raise ValueError("mode must be either 'amount' or 'composition'")
        if not inputs:
            raise ValueError("No inputs provided for conversion")
        if mode == "amount":
            mass_inputs = dict()
            for component in inputs:
                if component == "ethanol":
                    mass_inputs[component] = inputs[component] * self.densityEthanol
                elif component == "water":
                    mass_inputs[component] = inputs[component] * self.densityWater
                elif component == "sugar":
                    mass_inputs[component] = inputs[component] * self.densitySugar
                elif component == "fiber":
                    mass_inputs[component] = inputs[component] * self.densityFiber
                elif component == "total":
                    # Skip total here, calculate it after processing other components
                    pass
                else:
                    raise ValueError(f"Unknown component: {component}")
            # Calculate total after all components are processed
            if "total" in inputs:
                mass_inputs["total"] = sum(mass_inputs[comp] for comp in mass_inputs)
            return mass_inputs
        else:  # composition
            if total_flow is None:
                raise ValueError("total_flow must be provided when mode is 'composition'")
            mass_inputs = dict()
            for component in inputs:
                if component == "ethanol":
                    mass_inputs[component] = inputs[component] * total_flow * self.densityEthanol
                elif component == "water":
                    mass_inputs[component] = inputs[component] * total_flow * self.densityWater
                elif component == "sugar":
                    mass_inputs[component] = inputs[component] * total_flow * self.densitySugar
                elif component == "fiber":
                    mass_inputs[component] = inputs[component] * total_flow * self.densityFiber
                else:
                    raise ValueError(f"Unknown component: {component}")
            mass_inputs["total"] = sum(mass_inputs[component] for component in mass_inputs)
            return mass_inputs
            
    
    def massToFlow(self, **kwargs):
        inputs = kwargs.get("inputs", dict())
        mode = kwargs.get("mode", "amount")
        total_mass = kwargs.get("total_mass", None)
        if mode not in ["amount", "composition"]:
            raise ValueError("mode must be either 'amount' or 'composition'")
        if not inputs:
            raise ValueError("No inputs provided for conversion")
        if mode == "amount":
            flow_inputs = dict()
            for component in inputs:
                if component == "ethanol":
                    flow_inputs[component] = inputs[component] / self.densityEthanol
                elif component == "water":
                    flow_inputs[component] = inputs[component] / self.densityWater
                elif component == "sugar":
                    flow_inputs[component] = inputs[component] / self.densitySugar
                elif component == "fiber":
                    flow_inputs[component] = inputs[component] / self.densityFiber
                elif component == "total":
                    # Skip total here, calculate it after processing other components
                    pass
                else:
                    raise ValueError(f"Unknown component: {component}")
            # Calculate total after all components are processed
            if "total" in inputs:
                flow_inputs["total"] = sum(flow_inputs[key] for key in flow_inputs)
            return flow_inputs
        else:  # composition
            if total_mass is None:
                raise ValueError("total_mass must be provided when mode is 'composition'")
            flow_inputs = dict()
            for component in inputs:
                if component == "ethanol":
                    flow_inputs[component] = inputs[component] * total_mass / self.densityEthanol
                elif component == "water":
                    flow_inputs[component] = inputs[component] * total_mass / self.densityWater
                elif component == "sugar":
                    flow_inputs[component] = inputs[component] * total_mass / self.densitySugar
                elif component == "fiber":
                    flow_inputs[component] = inputs[component] * total_mass / self.densityFiber
                else:
                    raise ValueError(f"Unknown component: {component}")
            flow_inputs["total"] = sum(flow_inputs[component] for component in flow_inputs)
            return flow_inputs

    
    def processMass(self, **kwargs):
        # Process mass inputs and return outputs based on specified types
        # Extract parameters from kwargs
        inputs = kwargs.get("inputs", dict())
        input_type = kwargs.get("input_type", "full")
        output_type = kwargs.get("output_type", "full")
        total_mass = kwargs.get("total_mass", None)

        # Asking whether to store inputs and outputs into the system logs
        store_inputs = kwargs.get("store_inputs", False)
        store_outputs = kwargs.get("store_outputs", False)
        
        # Validate inputs
        if not inputs:
            raise ValueError("No inputs provided for processing")
        elif input_type not in ["amount", "composition", "full"] or output_type not in ["amount", "composition", "full"]:
            raise ValueError("input_type and output_type must be either 'amount', 'composition', or 'full'")
        elif store_outputs and not output_type == "full":
            raise ValueError("store_outputs can only be True when output_type is 'full'")
        elif input_type == "composition" and any(key not in inputs for key in ["ethanol", "water", "sugar", "fiber"]):
            raise ValueError("All components must be provided when input_type is 'composition'")
        
        # Convert inputs to amounts based on input_type
        if input_type == "composition":
            if total_mass is None:
                raise ValueError("total_mass must be provided when input_type is 'composition'")
            input_amounts = {key: inputs[key] * total_mass for key in inputs}
            input_amounts["total"] = total_mass
            input_composition = inputs
        elif input_type == "amount":
            input_amounts = inputs.copy()
            if input_amounts.get("total") is None:
                input_amounts["total"] = sum(v for k, v in input_amounts.items() if k != "total")
            input_total = total_mass if total_mass is not None else input_amounts["total"]
            if input_total <= 0:
                raise ValueError("Total input amount must be greater than zero to calculate composition")
            input_composition = {key: input_amounts[key] / input_total for key in input_amounts if key != "total"}
        else:  # full
            if any(key not in inputs["amount"] for key in ["ethanol", "water", "sugar", "fiber"]):
                raise ValueError("All components must be provided in 'amount' when input_type is 'full'")
            if any(key not in inputs["composition"] for key in ["ethanol", "water", "sugar", "fiber"]):
                raise ValueError("All components must be provided in 'composition' when input_type is 'full'")
            input_amounts = inputs["amount"].copy()
            input_amounts["total"] = sum(v for k, v in input_amounts.items() if k != "total")
            input_composition = inputs["composition"]

        # Store inputs if requested
        if store_inputs:
            for key in ["ethanol", "water", "sugar", "fiber"]:
                self.input_log["mass"]["amount"][key].append(input_amounts[key])
                self.input_log["mass"]["composition"][key].append(input_composition[key])
            self.input_log["mass"]["amount"]["total"].append(input_amounts["total"])

        # Process inputs through massFunction
        output_amounts = self.massFunction(input_amounts) if self.massFunction else input_amounts

        # Filter out None values and calculate total output
        filtered_output = {k: v for k, v in output_amounts.items() if v is not None}
        output_total = sum(filtered_output.values())
        
        if output_type == "amount":
            filtered_output["total"] = output_total
            return filtered_output
        else: 
            if output_total <= 0:
                raise ValueError("Total output amount must be greater than zero to calculate composition")
            output_composition = {key: filtered_output[key] / output_total for key in filtered_output}
            if output_type == "composition":
                return output_composition
            else:  # full
                if store_outputs:
                    for key in filtered_output:
                        self.output_log["mass"]["amount"][key].append(filtered_output[key])
                        self.output_log["mass"]["composition"][key].append(output_composition[key])
                    self.output_log["mass"]["amount"]["total"].append(output_total)
                filtered_output["total"] = output_total
                outputs = {
                    "amount": filtered_output,
                    "composition": output_composition
                }
                return outputs
    

    def processFlow(self, **kwargs):
        # Convert flow inputs to mass, process them, and convert outputs back to flow
        inputs = kwargs.get("inputs", dict())
        input_type = kwargs.get("input_type", "full")
        output_type = kwargs.get("output_type", "full")
        total_flow = kwargs.get("total_flow", None)
        store_inputs = kwargs.get("store_inputs", False)
        store_outputs = kwargs.get("store_outputs", False)

        # Convert flow inputs to mass inputs
        if input_type == "full":
            mass_inputs = {
                "amount": self.flowToMass(inputs=inputs["amount"], mode="amount"),
                "composition": inputs["composition"]  # Composition is dimensionless
            }
            mass_input_type = "full"
            total_mass = mass_inputs["amount"].get("total", None)
        elif input_type == "amount":
            mass_inputs = self.flowToMass(inputs=inputs, mode="amount")
            mass_input_type = "amount"
            total_mass = mass_inputs.get("total", None)
        elif input_type == "composition":
            if total_flow is None:
                raise ValueError("total_flow must be provided when input_type is 'composition'")
            mass_inputs = self.flowToMass(inputs=inputs, mode="composition", total_flow=total_flow)
            mass_input_type = "amount"
            total_mass = mass_inputs.get("total", None)
        else:
            raise ValueError("input_type must be either 'amount', 'composition', or 'full'")

        # Process mass inputs (store mass data as well)
        mass_outputs = self.processMass(
            inputs=mass_inputs,
            input_type=mass_input_type,
            output_type="full",
            total_mass=total_mass,
            store_inputs=store_inputs,
            store_outputs=store_outputs
        )

        # Convert mass outputs back to flow outputs
        flow_output_amounts = self.massToFlow(inputs=mass_outputs["amount"], mode="amount")
        
        # Store flow inputs if requested
        if store_inputs:
            if input_type == "full":
                for key in ["ethanol", "water", "sugar", "fiber"]:
                    if key in inputs["amount"]:
                        self.input_log["flow"]["amount"][key].append(inputs["amount"][key])
                    if key in inputs["composition"]:
                        self.input_log["flow"]["composition"][key].append(inputs["composition"][key])
                if total_flow is not None:
                    self.input_log["flow"]["amount"]["total"].append(total_flow)
                else:
                    calc_total = sum(inputs["amount"][k] for k in inputs["amount"] if k != "total")
                    self.input_log["flow"]["amount"]["total"].append(calc_total)
            elif input_type == "amount":
                for key in ["ethanol", "water", "sugar", "fiber"]:
                    if key in inputs:
                        self.input_log["flow"]["amount"][key].append(inputs[key])
                flow_total = inputs.get("total", sum(inputs[k] for k in inputs if k != "total"))
                self.input_log["flow"]["amount"]["total"].append(flow_total)
                for key in ["ethanol", "water", "sugar", "fiber"]:
                    if key in inputs:
                        self.input_log["flow"]["composition"][key].append(inputs[key] / flow_total if flow_total > 0 else 0)
            elif input_type == "composition":
                for key in ["ethanol", "water", "sugar", "fiber"]:
                    if key in inputs:
                        self.input_log["flow"]["composition"][key].append(inputs[key])
                self.input_log["flow"]["amount"]["total"].append(total_flow)

        # Store flow outputs if requested
        if store_outputs:
            for key in ["ethanol", "water", "sugar", "fiber"]:
                if key in flow_output_amounts:
                    self.output_log["flow"]["amount"][key].append(flow_output_amounts[key])
                if key in mass_outputs["composition"]:
                    self.output_log["flow"]["composition"][key].append(mass_outputs["composition"][key])
            if "total" in flow_output_amounts:
                self.output_log["flow"]["amount"]["total"].append(flow_output_amounts["total"])

        # Format output based on output_type
        if output_type == "amount":
            return flow_output_amounts
        elif output_type == "composition":
            return mass_outputs["composition"]  # Composition is the same for mass and flow
        else:  # full
            return {
                "amount": flow_output_amounts,
                "composition": mass_outputs["composition"]
            }
    

    def iterateInputs(self, inputValues=dict(), **kwargs):
        # Appends input values to the inputs dictionary
        for key in inputValues:
            self.input_log[key] += inputValues[key]

        # Process each set of inputs and appends to outputs
        for i in range(len(inputValues["ethanol"])):
            input_dict = {key: inputValues[key][i] for key in inputValues}
            output_dict = self.massFunction(input_dict)
            for key in self.output_log:
                self.output_log[key].append(output_dict[key])

        return self.output_log 
    
    def display(self, input=str, output=str):
        plt.plot(self.input_log[input], self.output_log[output], linestyle='--', marker='o')
        plt.title(f"{self.name} System: {input} vs {output}")
        plt.xlabel(f"Input {input} (units)")
        plt.ylabel(f"Output {output} (units)")
        plt.grid(True)
        plt.show()


class Fermentation(System):
    def __init__(self, efficiency=float):
        super().__init__(name="Fermentation", efficiency=efficiency, massFunction=self.ferment)
        # Additional initialization for Fermenter can go here

    
    def ferment(self, input=dict()):
        return {
            "ethanol": 0.51 * input["sugar"] * self.efficiency if input.get("sugar") is not None else None, 
            "water": input["water"] if input.get("water") is not None and input.get("sugar") is not None else None,
            "sugar": (1 - self.efficiency) * input["sugar"] if input.get("sugar") is not None else None,
            "fiber": input["fiber"] if input.get("fiber") is not None else None
        }
        # pass

class Filtration(System):
    def __init__(self, efficiency=float):
        super().__init__(name="Filtration", efficiency=efficiency, massFunction=self.filter)
        # Additional initialization for Filter can go here

    
    def filter(self, input=dict()):
        return {
            "ethanol": input["ethanol"] if input.get("ethanol") is not None else None, 
            "water": input["water"] if input.get("water") is not None else None,
            "sugar": input["sugar"] if input.get("sugar") is not None else None,
            "fiber": (1 - self.efficiency) * input["fiber"] if input.get("fiber") is not None else None
        }

class Distillation(System):
    def __init__(self, efficiency=float):
        super().__init__(name="Distillation", efficiency=efficiency, massFunction=self.distill)
        # Additional initialization for Distiller can go here

    
    def distill(self, input=dict()):
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

class Dehydration(System):
    def __init__(self, efficiency=float):
        super().__init__(name="Dehydration", efficiency=efficiency, massFunction=self.dehydrate)
        # Additional initialization for Dehydrator can go here

    
    def dehydrate(self, input=dict()):
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