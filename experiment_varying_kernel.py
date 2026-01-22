import numpy as np
from matplotlib import pyplot as plt
from concurrent.futures import ProcessPoolExecutor
from config import SPORE, sim_parameters
from transitions import ProbToxinSim
from utils import gkern
import itertools

def run_single_simulation(variance, kernel_size, params, num_iterations):
    params["toxin_convolution_variance"] = variance
    params["toxin_convolution_size"] = kernel_size
    simulation = ProbToxinSim(params)
    simulation.set_state(params["n"] // 2, params["n"] // 2, SPORE)

    for _ in range(num_iterations):
        simulation.step()

    detect = simulation.inner_ring_detector()
    if detect == None:
        return 0
    return simulation.inner_ring_detector()[0]

def main():
    variances = np.arange(0.1, 2, 0.1)
    kernel_sizes = np.arange(1, 12, 2)
    num_simulations = 10
    num_iterations = 50

    fairy_ring_vars = []
    fairy_ring_kern_sizes = []

    with ProcessPoolExecutor() as executor:
        for var, kern_size in itertools.product(variances, kernel_sizes):
            print(f"calculating var: {var}, kern_size: {kern_size}")

            futures = [executor.submit(run_single_simulation, var, kern_size, sim_parameters, num_iterations)
                       for _ in range(num_simulations)]

            vals = [f.result() for f in futures]

            mean_val = np.mean(vals)
            if mean_val >= 0.8:
                print(f"var: {var}, kern_size: {kern_size} → mean: {mean_val}")
                np.append(fairy_ring_kern_sizes, kern_size)
                fairy_ring_vars.append(var)
                fairy_ring_kern_sizes.append(kern_size)

    print(fairy_ring_vars, fairy_ring_kern_sizes)
    plt.scatter(fairy_ring_vars, fairy_ring_kern_sizes)
    plt.title("Relative Size Inner Rings for diffusion parameters")
    plt.xlabel("Variance")
    plt.ylabel("Kernel Size")
    plt.legend()
    plt.savefig("./plots/experiment_varying_kernel.png")
    plt.show()

if __name__ == "__main__":
    main()