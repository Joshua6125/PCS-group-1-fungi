from constants import SPORE
from transitions import BasicSim, BasicToxinSim
from matplotlib import pyplot as plt
from utils import gkern
import numpy as np


def main():
    # Parameters
    sim_parameters = {
        "n": 150,
        "prob_spore_to_hyphae": 1.0,
        "prob_mushroom": 0.7,
        "prob_spread": 0.5,
        "toxin_threshold": 0.3,
        "toxin_decay": 0.5,
        "toxin_convolution": gkern(5, 1, 1),
        "iterations": 50
    }

    decay_rates = np.linspace(0, 0.1, 40)
    num_simulations = 40
    val_per_rate = []
    val_per_rate_lower = []
    val_per_rate_upper = []

    for i, rate in enumerate(decay_rates):
        print(i)
        sim_parameters["toxin_decay"] = rate
        vals = []
        for _ in range(num_simulations):
            simulation = BasicToxinSim(sim_parameters)
            simulation.set_state(sim_parameters["n"]//2, sim_parameters["n"]//2, SPORE)

            for _ in range(sim_parameters["iterations"]):
                simulation.step()
            vals.append(simulation.inner_ring_detector())

        mean_val = np.mean(vals)
        std_val = np.std(vals)
        val_per_rate.append(mean_val)
        val_per_rate_lower.append(mean_val - std_val)
        val_per_rate_upper.append(mean_val + std_val)
    plt.plot(decay_rates, val_per_rate, )
    plt.plot(decay_rates, val_per_rate_lower)
    plt.plot(decay_rates, val_per_rate_upper)
    plt.title("relative size inner rings per decay rate")
    plt.xlabel("decay rate")
    plt.ylabel("size convex hull divided by total")
    plt.legend(["mean", "lower", "upper"])
    plt.savefig("results_10_simulations.png")


if __name__ == "__main__":
    main()