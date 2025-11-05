import numpy as np
import math

class Connector:
    def __init__(self, inputFlow, outputFlow, connectorFunction):
        self.inputFlow = inputFlow
        self.outputFlow = outputFlow
        self.connectorFunction = connectorFunction