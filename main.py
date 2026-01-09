from constants import SPORE
from transitions import BasicSim, BasicToxinSim
from utils import gkern
import time


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