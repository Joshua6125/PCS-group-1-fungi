from config import sim_parameters, SPORE
from transitions import BasicSim, BasicToxinSim, ProbToxinSim, ProbToxinDeathSim
from utils import linear_regression, area_polygon, read_fairy_data

import numpy as np

def estimate_CA_vars(param: dict, iterations: int = 5, steps: int = 100) -> tuple:
    """
    Function that performs iterative estimation of the diameter/time ratio of a CA model

    :param param: simulation parameters
    :type param: dict
    :param iterations: amount of CA model instances
    :type iterations: int
    :param steps: Amount of steps simulated per CA model
    :type steps: int
    :return: Returns average slope and minimum hull ratio
    :rtype: tuple[Any, ...]
    """
    slopes = []
    hull_ratios = []
    for t in range(iterations):
        sim = BasicToxinSim(param)
        sim.set_state(param["n"]//2, param["n"]//2, SPORE)

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
        if res[0] is None:
            continue

        slopes.append(res[1])

    return np.mean(slopes), np.min(hull_ratios)


def main():
    # Get real data
    data_points = read_fairy_data()
    n = len(data_points)

    # Select a third of the points
    np.random.shuffle(data_points)
    calibration_points = data_points[:n//3]
    validation_points = data_points[n//3:]

    # Perform linear regression on points for slope
    _, slope_data_calibration = linear_regression(calibration_points)
    _, slope_data_validation = linear_regression(validation_points)
    if slope_data_calibration is None or slope_data_validation is None:
        raise Exception("Calibrating failed.")

    # Caluclate CA slope for calibration
    slope_CA, hull_ratio = estimate_CA_vars(sim_parameters, iterations=2, steps=50)
    if hull_ratio < 0.9:
        print("Too many inner rings. Avg ratio:", hull_ratio)
        return

    # Scaler for CA to calibrate to real data
    scaler = slope_data_calibration / slope_CA

    # Calculate CA slope for validation
    slope_CA, hull_ratio = estimate_CA_vars(sim_parameters, iterations=2, steps=50)
    if hull_ratio < 0.9:
        print("Too many inner rings. Avg ratio:", hull_ratio)
        return

    print("Ratio:  ", scaler * slope_CA/ slope_data_validation)
    if (scaler * slope_CA/ slope_data_validation - 1) > 0.01:
        print("More than 1% deviance,. Invalid!")


if __name__ == "__main__":
    main()