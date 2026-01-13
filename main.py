from config import SPORE, sim_parameters
from transitions import BasicSim, BasicToxinSim
import time


def main():
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
