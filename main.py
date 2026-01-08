from constants import *
from transitions import BasicSim
import time
import numpy as np


def main():
    # Parameters
    n = 75
    prob_spore_to_hyphae = 0.3
    prob_mushroom = 0.7
    prob_spread = 0.5

    prob_spore = 0.05

    simulation = BasicSim(n, prob_spore_to_hyphae, prob_mushroom, prob_spread)
    for i in range(n):
        for j in range(n):
            if np.random.random() <= prob_spore:
                simulation.set_state(i, j, SPORE)

    print(simulation)
    for _ in range(100):
        time.sleep(1)
        simulation.step()
        sim_string = str(simulation)
        print(sim_string)


if __name__ == "__main__":
    main()