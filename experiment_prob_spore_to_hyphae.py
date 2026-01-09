import numpy as np
from transitions import BasicSim
from utils import gkern
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
sim_parameters = {
        "n": 75,
        "prob_spore_to_hyphae": 1.0,
        "prob_mushroom": 0.7,
        "prob_spread": 0.5,
        "toxin_threshold": 0.3,
        "toxin_decay": 0.05,
        "toxin_convolution": gkern(5, 1, 1)
}

num_iterations = 25

colors = [(0, 1, 0), (0, 0.5, 0.5), (0, 0, 0.5), (0, 0, 1), (1, 0, 0), (0.5, 0.5, 0), (0, 0, 0), (0, 0, 0), (1, 1, 1)]

# Main code
probabilities = np.linspace(0.1, 1, 10)
for probability in probabilities:
    sim_parameters["prob_spread"] = probability
    simulation = BasicSim(sim_parameters)
    simulation.set_state(sim_parameters["n"]//2, sim_parameters["n"]//2, SPORE)
    for _ in range(num_iterations):
        simulation.step()
    cmap = LinearSegmentedColormap.from_list("cmap_name", colors, N=10)

    fig, ax = plt.subplots()
    ax.imshow(simulation.state_grids[-1], origin='lower', cmap=cmap)

    plt.title(f"Fairy rings ater {num_iterations} steps with spread probability {round(probability, 1)}")
    plt.savefig(f"./plots/experiment_prob_spread/{num_iterations}_{round(probability, 1)}.png")
