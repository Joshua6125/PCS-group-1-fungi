from constants import *
from transitions import BasicSim
import time


def main():
    # Parameters
    n = 75
    prob_spore_to_hyphae = 0.7
    prob_mushroom = 0.7
    prob_spread = 0.5

    simulation = BasicSim(n, prob_spore_to_hyphae, prob_mushroom, prob_spread)
    simulation.set_state(n//2, n//2, SPORE)

    print(simulation)
    for _ in range(100):
        time.sleep(1)
        simulation.step()
        sim_string = str(simulation)
        print(sim_string)


if __name__ == "__main__":
    main()