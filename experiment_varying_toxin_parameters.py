import numpy as np
from matplotlib import pyplot as plt
from concurrent.futures import ProcessPoolExecutor
from config import SPORE, sim_parameters
from transitions import ProbToxinSim
from utils import gkern
import itertools

def run_single_simulation(kernel_variance, decay, params, num_iterations):
    params["toxin_convolution_variance"] = kernel_variance
    params["toxin_decay"] = decay
    simulation = ProbToxinSim(params)
    simulation.set_state(params["n"] // 2, params["n"] // 2, SPORE)

    for _ in range(num_iterations):
        simulation.step()

    detect = simulation.inner_ring_detector()
    if detect == None:
        return 0
    return simulation.inner_ring_detector()[0]

def main():
    variances = np.arange(0.01, .6, 0.1)
    decays = np.arange(0, .1, 0.01)
    num_simulations = 20
    num_iterations = 50

    fairy_ring_vars = []
    fairy_ring_decays = []

    with ProcessPoolExecutor() as executor:
        for var, decay in itertools.product(variances, decays):
            print(f"calculating variance: {var}, decay: {decay}")

            futures = [executor.submit(run_single_simulation, var, decay, sim_parameters, num_iterations)
                       for _ in range(num_simulations)]

            vals = [f.result() for f in futures]

            fairy_rings = [val >= 0.9 for val in vals]
            fairy_ring_amt = fairy_rings.count(True)
            fairy_ring_ratio = fairy_ring_amt/num_simulations
            print(fairy_ring_ratio)
            if fairy_ring_ratio >= 0.5:
                print(f"FAIRY RING DETECTED")
                fairy_ring_vars.append(var)
                fairy_ring_decays.append(decay)
            else:
                print("no fairy ring detected")

    print(fairy_ring_vars, fairy_ring_decays)
    plt.scatter(fairy_ring_vars, fairy_ring_decays)
    plt.title("Do fairy rings show for toxic parameters")
    plt.xlabel("Variance")
    plt.ylabel("Decay")
    plt.legend()
    plt.savefig("./plots/experiment_varying_toxin_parameters.png")
    plt.show()

if __name__ == "__main__":
    main()