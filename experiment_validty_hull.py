from constants import SPORE
from transitions import BasicSim, BasicToxinSim
from matplotlib import pyplot as plt
from utils import gkern


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

    num_simulations = 100
    vals = []
    for i in range(num_simulations):
        print(i)
        simulation = BasicToxinSim(sim_parameters)
        simulation.set_state(sim_parameters["n"]//2, sim_parameters["n"]//2, SPORE)

        for _ in range(sim_parameters["iterations"]):
            simulation.step()
        vals.append(simulation.inner_ring_detector())

    plt.hist(vals)
    plt.savefig("result_medium_toxin_decay.png")


if __name__ == "__main__":
    main()