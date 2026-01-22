from config import sim_parameters, SPORE
from transitions import BasicSim, BasicToxinSim, ProbToxinSim, ProbToxinDeathSim
from utils import linear_regression, area_polygon

import numpy as np

def main():
    iterations = 1
    steps = 100

    bi, si = linear_regression()

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

            # Add extra unit of time to make 1-indexed
            points.append((diameter, sim.time))

        points = np.array(points)
        res = linear_regression(points)
        slopes.append(res[1])

        print("t", t, "slope:", res[1])

    print(bi/np.mean(slopes), bi, np.mean(slopes))


if __name__ == "__main__":
    main()