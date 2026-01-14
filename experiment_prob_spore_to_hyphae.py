import numpy as np
from transitions import BasicSim
from config import SPORE, sim_parameters
from matplotlib import pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import os


num_iterations = 25

colors = [(0, 1, 0), (0, 0.5, 0.5), (0, 0, 0.5), (0, 0, 1),
          (1, 0, 0), (0.5, 0.5, 0), (0, 0, 0), (0, 0, 0), (1, 1, 1)]

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

    plt.title(
        f"Fairy rings ater {num_iterations} steps with spread probability {round(probability, 1)}")
    if not os.path.exists('./plots/experiment_prob_spread/'):
        os.makedirs('./plots/experiment_prob_spread')
    plt.savefig(
        f"./plots/experiment_prob_spread/{num_iterations}_{round(probability, 1)}.png")
