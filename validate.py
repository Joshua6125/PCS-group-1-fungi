from config import sim_parameters, SPORE, CELL_SCALE, TIME_SCALE
from transitions import BasicSim, BasicToxinSim, ProbToxinSim, ProbToxinDeathSim
from utils import linear_regression, area_polygon

import numpy as np
import matplotlib.pyplot as plt

def estimate_CA_vars(iterations: int = 5, steps: int = 100) -> tuple:
    slopes = []
    hull_ratios = []
    for t in range(iterations):
        sim = BasicToxinSim(sim_parameters)
        sim.set_state(sim_parameters["n"]//2, sim_parameters["n"]//2, SPORE)

        points = [(0, 0)]
        for _ in range(steps):
            sim.step()

            hull = sim.inner_ring_detector()
            if hull is None: continue
            hull_ratio, hull_points = hull

            area = area_polygon(hull_points)
            diameter = 2*np.sqrt(area/np.pi)

            points.append((diameter, sim.time))
            hull_ratios.append(hull_ratio)

        points = np.array(points)
        res = linear_regression(points)
        slopes.append(res[1])

        print("case", t+1, "slope:", res[1])

    return np.mean(slopes), np.mean(hull_ratios)


def main():
    intercept_data, slope_data = linear_regression()

    slope_CA, hull_ratio = estimate_CA_vars(iterations=5, steps=150)
    if hull_ratio < 0.9:
        print("Too many inner rings. Avg ratio:", hull_ratio)
        return

    scaled_slope_CA = CELL_SCALE * slope_CA / TIME_SCALE

    print("Slope data:     ", slope_data)
    print("Slope CA:       ", slope_CA)
    print("Hull ratio CA:  ", hull_ratio)
    print("Slope CA scaled:", scaled_slope_CA)
    print("Ratio CA/data:  ", scaled_slope_CA / slope_data)

    t = np.linspace(0, 100, 1000)
    plt.plot(t, slope_data * t, label="data")
    plt.plot(t, scaled_slope_CA * t, label="CA (scaled)")
    plt.legend()
    plt.show()


if __name__ == "__main__":
    main()