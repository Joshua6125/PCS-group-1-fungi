from config import sim_parameters, SPORE
from transitions import BasicSim, BasicToxinSim, ProbToxinSim, ProbToxinDeathSim
from utils import linear_regression, area_polygon

import numpy as np
import matplotlib.pyplot as plt

def estimate_CA_slope(iterations=5, steps=100):
    slopes = []
    for t in range(iterations):
        sim = BasicToxinSim(sim_parameters)
        sim.set_state(sim_parameters["n"]//2, sim_parameters["n"]//2, SPORE)

        points = [(0, 0)]
        for _ in range(steps):
            sim.step()

            hull = sim.inner_ring_detector()
            if hull is None: continue
            _, hull_points = hull

            area = area_polygon(hull_points)
            diameter = 2*np.sqrt(area/np.pi)

            points.append((diameter, sim.time))

        points = np.array(points)
        res = linear_regression(points)
        slopes.append(res[1])

        print("t", t, "slope:", res[1])

    return np.mean(slopes)


def main():
    _, slope_data = linear_regression()

    slope_CA = estimate_CA_slope(iterations=5)

    slope_ratio = slope_data/slope_CA

    print("Slope data:", slope_data)
    print("Slope CA:  ", slope_CA)
    print("ratio s_data/s_CA:", slope_ratio)






if __name__ == "__main__":
    main()