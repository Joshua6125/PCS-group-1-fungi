import numpy as np
from CA import CA

# State names
EMPTY = 0
SPORE = 1
YOUNG = 2
MATURING = 3
MUSHROOMS = 4
OLDER = 5
DECAYING = 6
DEAD1 = 7
DEAD2 = 8
INERT = 9

# Parameters
n = 20
prob_spore_to_hyphae = 0.2
prob_mushroom = 0.5
prob_spread = 0.5

# Main code
simulation = CA(n, prob_spore_to_hyphae, prob_mushroom, prob_spread)
print(simulation)
for _ in range(10):
    simulation.step()
    sim_string = str(simulation)
    print(sim_string)