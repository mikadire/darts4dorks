import numpy as np


class StdDev:
    def __init__(self):
        self.values = []

    def step(self, value):
        self.values.append(value)

    def finalize(self):
        stddev = float(np.std(self.values, ddof=1))
        return stddev if not np.isnan(stddev) else 0
