from constants import *
from transitions import BasicSim, BasicToxinSim
import time
import numpy as np

def gkern(l, sig, multi):
    """\
    creates gaussian kernel with side length `l` and a sigma of `sig`
    """
    ax = np.linspace(-(l - 1) / 2., (l - 1) / 2., l)
    gauss = np.exp(-0.5 * np.square(ax) / np.square(sig))
    kernel = np.outer(gauss, gauss)
    return kernel / np.sum(kernel) * multi

def main():
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

    print(sim_parameters["toxin_convolution"])

    simulation = BasicToxinSim(sim_parameters)
    simulation.set_state(sim_parameters["n"]//2, sim_parameters["n"]//2, SPORE)

    print(simulation)
    for _ in range(100):
        time.sleep(0.4)
        simulation.step()
        sim_string = str(simulation)
        print(sim_string)


if __name__ == "__main__":
    main()