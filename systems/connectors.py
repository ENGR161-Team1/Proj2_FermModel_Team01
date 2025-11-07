import numpy as np
import math

class Connector:
    def __init__(self, inputFlow, outputFlow, connectorFunction):
        self.inputFlow = inputFlow
        self.outputFlow = outputFlow
        self.connectorFunction = connectorFunction
    
    def pass_flow(self, **kwargs):
        input_composition = kwargs.get("input_composition", dict())
        total_flow = kwargs.get("total_flow", None)
        return self.connectorFunction(input)

class Pipe(Connector):
    def __init__(self):
        super().__init__("Pipe Input Flow", "Pipe Output Flow", self.pipe_function)
        # Additional initialization for Pipe can go here

    
    def pipe_function(self, input=dict()):
        return input
        # pass

class Bend(Connector):
    def __init__(self):
        super().__init__("Bend Input Flow", "Bend Output Flow", self.bend_function)
        # Additional initialization for Bend can go here

    
    def bend_function(self, input=dict()):
        return input
        # pass

class Valve(Connector):
    def __init__(self):
        super().__init__("Valve Input Flow", "Valve Output Flow", self.valve_function)
        # Additional initialization for Valve can go here

    
    def valve_function(self, input=dict()):
        return input
        # pass