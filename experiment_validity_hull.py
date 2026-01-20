import numpy as np
from matplotlib import pyplot as plt
from concurrent.futures import ProcessPoolExecutor
from config import SPORE
from transitions import BasicToxinSim
from utils import gkern

def run_single_simulation(rate, params):
    params["toxin_decay"] = rate
    simulation = BasicToxinSim(params)
    simulation.set_state(params["n"] // 2, params["n"] // 2, SPORE)

    for _ in range(params["iterations"]):
        simulation.step()

    return simulation.inner_ring_detector()

def main():
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

    decay_rates = np.linspace(0, 0.1, 25)
    num_simulations = 60

    val_per_rate = []
    val_per_rate_lower = []
    val_per_rate_upper = []

    with ProcessPoolExecutor() as executor:
        for rate in decay_rates:
            print(f"Processing decay rate: {rate}")

            futures = [executor.submit(run_single_simulation, rate, sim_parameters)
                       for _ in range(num_simulations)]

            vals = [f.result() for f in futures]

            mean_val = np.mean(vals)
            std_val = np.std(vals)
            val_per_rate.append(mean_val)
            val_per_rate_lower.append(mean_val - std_val)
            val_per_rate_upper.append(mean_val + std_val)

    plt.fill_between(decay_rates, val_per_rate_lower, val_per_rate_upper, alpha=0.2, label="std dev")
    plt.plot(decay_rates, val_per_rate, label="mean", marker='o')
    plt.title("Relative Size Inner Rings per Decay Rate")
    plt.xlabel("Decay Rate")
    plt.ylabel("Size Convex Hull divided by Total")
    plt.legend()
    plt.savefig("./results_distance_test.png")
    plt.show()

if __name__ == "__main__":
    main()