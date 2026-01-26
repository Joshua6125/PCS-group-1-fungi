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
    variances = np.arange(0.01, 1.2, 0.05)
    decays = np.arange(0, .1, 0.005)
    num_simulations = 50
    num_iterations = 50

    calculate = False

    if calculate:
        fairy_ring_vars = []
        fairy_ring_decays = []
        heatmap_data = np.zeros((len(variances), len(decays)))

        with ProcessPoolExecutor() as executor:
            for (n, var), (m, decay) in itertools.product(enumerate(variances), enumerate(decays)):
                print(f"calculating variance: {var}, decay: {decay}")

                futures = [executor.submit(run_single_simulation, var, decay, sim_parameters, num_iterations)
                        for _ in range(num_simulations)]

                vals = [f.result() for f in futures]

                fairy_rings = [val >= 0.9 for val in vals]
                fairy_ring_amt = fairy_rings.count(True)
                fairy_ring_ratio = fairy_ring_amt/num_simulations
                heatmap_data[n][m] = fairy_ring_ratio
                print(fairy_ring_ratio)
                if fairy_ring_ratio >= 0.5:
                    print(f"FAIRY RING DETECTED")
                    fairy_ring_vars.append(var)
                    fairy_ring_decays.append(decay)
                else:
                    print("no fairy ring detected")

    if calculate:
        with open("fairy_ring_prevalance.data", "w") as fr_p_file:
            fr_p_file.write(str([[float(j) for j in i] for i in heatmap_data]))
    else:
        with open("fairy_ring_prevalance.data", "r") as fr_p_file:
            heatmap_data = eval(fr_p_file.read())
    heatmap_data = [[100 * j for j in i] for i in heatmap_data]
    im = plt.imshow(heatmap_data, cmap="vanimo")
    plt.colorbar(im, orientation="vertical", label="% of simulations forming FFR without inner ring")
    plt.title("FFR prevalence for varying kernel variance and decay values.")
    plt.ylabel("Variance")
    plt.yticks(range(0, len(variances), 2), labels=[f"{x:.2f}" for x in variances[::2]])
    plt.xlabel("Decay")
    plt.xticks(range(0, len(decays), 2), labels=[f"{x:.2f}" for x in decays[::2]], rotation=45)
    plt.savefig("./plots/experiment_varying_toxin_parameters.png")
    plt.show()

if __name__ == "__main__":
    main()