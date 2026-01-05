import numpy as np
from CA import CA_Grid

# Parameters
n = 4

# Main code
simulation = CA_Grid(n)
print(simulation)
simulation.step()
print(simulation)