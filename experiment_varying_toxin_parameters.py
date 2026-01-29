import numpy as np
from matplotlib import pyplot as plt
import matplotlib.ticker as ticker
from concurrent.futures import ProcessPoolExecutor
from config import SPORE, sim_parameters
from transitions import ProbToxinSim
from utils import gkern
import itertools


def run_single_simulation(
        kernel_variance: float,
        decay: float,
        params,
        num_iterations: int) -> float:
    params["toxin_convolution_variance"] = kernel_variance
    params["toxin_decay"] = decay
    simulation = ProbToxinSim(params)
    simulation.set_state(params["n"] // 2, params["n"] // 2, SPORE)

    for _ in range(num_iterations):
        simulation.step()

    detect = simulation.inner_ring_detector()
    if detect is None:
        return 0
    return detect[0]


def main():
    variances = np.arange(0.01, 1.2, 0.05)
    decays = np.arange(0, .1, 0.005)
    num_simulations = 50
    num_iterations = 50

    calculate = False

    # Only calculate if calculate == True
    if calculate:
        heatmap_data = np.zeros((len(variances), len(decays)))

        with ProcessPoolExecutor() as executor:
            for (n, var), (m, decay) in itertools.product(
                    enumerate(variances),
                    enumerate(decays)):
                print(f"calculating variance: {var}, decay: {decay}")

                # Use executor for parallelizing the workload
                futures = [executor.submit(
                    run_single_simulation,
                    var,
                    decay,
                    sim_parameters,
                    num_iterations) for _ in range(num_simulations)]

                vals = [f.result() for f in futures]

                fairy_rings = [val >= 0.9 for val in vals]
                fairy_ring_amt = fairy_rings.count(True)
                fairy_ring_ratio = fairy_ring_amt/num_simulations
                heatmap_data[n][m] = fairy_ring_ratio
                print(fairy_ring_ratio)

        with open("data/fairy_ring_prevalance.data", "w") as fr_p_file:
            fr_p_file.write(str([[float(j) for j in i] for i in heatmap_data]))
    else:
        # Else read from file
        with open("data/fairy_ring_prevalance.data", "r") as fr_p_file:
            heatmap_data = eval(fr_p_file.read())
    heatmap_data = [[100 * j for j in i] for i in heatmap_data]
    im = plt.imshow(heatmap_data, cmap="vanimo")
    cbar = plt.colorbar(im, orientation="vertical",
                 label="% of simulations forming FFR without inner ring")
    cbar.ax.yaxis.set_major_formatter(ticker.PercentFormatter())

    plt.title("FFR prevalence for varying kernel variance and decay values.")
    plt.ylabel("Variance")
    plt.yticks(range(0, len(variances), 2), labels=[
               f"{x:.2f}" for x in variances[::2]])
    plt.xlabel("Decay")
    plt.xticks(range(0, len(decays), 2), labels=[
               f"{x:.2f}" for x in decays[::2]], rotation=45)
    plt.savefig("./plots/experiment_varying_toxin_parameters.png")
    plt.show()


if __name__ == "__main__":
    main()
