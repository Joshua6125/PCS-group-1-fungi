import numpy as np
from transitions import BasicSim
import time
from matplotlib import pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

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
num_iterations = 50
prob_spore_to_hyphae = 1
prob_mushroom = 0.9

colors = [(0, 1, 0), (0, 0.5, 0.5), (0, 0, 0.5), (0, 0, 1), (1, 0, 0), (0.5, 0.5, 0), (0, 0, 0), (0, 0, 0), (1, 1, 1)]

# Main code
probabilities = np.linspace(0.1, 1, 10)
for probability in probabilities:
    simulation = BasicSim(n, prob_spore_to_hyphae, prob_mushroom, probability)
    simulation.set_state(n//2, n//2, SPORE)
    for _ in range(num_iterations):
        simulation.step()
    cmap = LinearSegmentedColormap.from_list("cmap_name", colors, N=10)
    
    fig, ax = plt.subplots()
    ax.imshow(simulation.grids[-1], origin='lower', cmap=cmap)
    
    plt.title(f"Fairy rings ater {num_iterations} steps with spread probability {probability}")
    plt.show()