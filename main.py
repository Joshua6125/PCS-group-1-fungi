from config import SPORE, sim_parameters
from transitions import BasicToxinSim
import time


def main():
    sim_parameters["n"] = 20
    sim_parameters["show_toxins"] = True
    simulation = BasicToxinSim(sim_parameters)
    simulation.set_state(sim_parameters["n"]//2, sim_parameters["n"]//2, SPORE)

    print(simulation.get_grid_representation(
        show_toxins=sim_parameters["show_toxins"]))
    for _ in range(100):
        time.sleep(0.4)
        simulation.step()
        sim_string = simulation.get_grid_representation(
            show_toxins=sim_parameters["show_toxins"])
        print(sim_string)


if __name__ == "__main__":
    main()
