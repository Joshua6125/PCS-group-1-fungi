import numpy as np
from transitions import BasicSim
import time

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
n = 75
prob_spore_to_hyphae = 1
prob_mushroom = 0.9
prob_spread = 0.7

# Main code
simulation = BasicSim(n, prob_spore_to_hyphae, prob_mushroom, prob_spread)
simulation.set_state(n//2, n//2, SPORE)
print(simulation)
for _ in range(100):
    time.sleep(1)
    simulation.step()
    sim_string = str(simulation)
    print(sim_string)