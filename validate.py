from config import sim_parameters, SPORE
from transitions import BasicSim, BasicToxinSim, ProbToxinSim, ProbToxinDeathSim
from utils import linear_regression, area_polygon, read_fairy_data, regression_ci

import numpy as np
import matplotlib.pyplot as plt

def estimate_CA_vars(param: dict, iterations: int = 5, steps: int = 100) -> tuple:
    """
    Function that performs iterative estimation of the diameter/time ratio of a CA model

    :param param: simulation parameters
    :type param: dict
    :param iterations: amount of CA model instances
    :type iterations: int
    :param steps: Amount of steps simulated per CA model
    :type steps: int
    :return: Returns average intercept, average slope, and minimum hull ratio
    :rtype: tuple[Any, ...]
    """
    slopes = []
    intercepts = []
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
        intercepts.append(res[0])

    return np.mean(intercepts), np.mean(slopes), np.mean(hull_ratios)


def main():
    HULL_RATIO = 0.9
    STEPS = 50
    ITERS = 100

    # Get real data
    data_points = read_fairy_data()
    n = len(data_points)

    # Select a third of the points
    np.random.shuffle(data_points)
    calibration_points = data_points[:2*n//3]
    validation_points = data_points[2*n//3:]

    # Perform linear regression on points for slope
    intercept_data, slope_data_calibration = linear_regression(calibration_points)
    if slope_data_calibration is None:
        raise Exception("Calibrating failed.")

    # Calculate CA slope for calibration
    intercept_CA, slope_CA, hull_ratio = estimate_CA_vars(sim_parameters, iterations=ITERS, steps=STEPS)
    if hull_ratio < HULL_RATIO:
        print(f"Too many inner rings. Avg ratio: {hull_ratio:.2f}")
        return

    # Scaler for CA to calibrate to real data
    scaler_slope = slope_data_calibration / slope_CA
    scaler_intercept = intercept_data / intercept_CA

    # Calculate CA slope for validation
    intercept_CA, slope_CA, hull_ratio = estimate_CA_vars(sim_parameters, iterations=ITERS, steps=STEPS)
    if hull_ratio < HULL_RATIO:
        print(f"Too many inner rings. Avg ratio: {hull_ratio:.2f}")
        return

    # Calculate confindence interval of remaining points
    intercept_ci, slope_ci = regression_ci(validation_points)

    # Check if model falls inside the confidence interval
    if slope_ci[0] <= scaler_slope*slope_CA <= slope_ci[1] and \
       intercept_ci[0] <= scaler_intercept*intercept_CA <= intercept_ci[1]:
        print("PASSED")
    else:
        print("REJECTED: Model outside confidence interval.")
    print(f"Scaled slope CA: {scaler_slope*slope_CA:.2f}")
    print(f"Confidence interval slope: [{slope_ci[0]:.2f}, {slope_ci[1]:.2f}]")
    print(f"Scaled intercept CA: {scaler_intercept*intercept_CA:.2f}")
    print(f"Confidence interval slope: [{intercept_ci[0]:.2f}, {intercept_ci[1]:.2f}]")

    t = np.linspace(0, 100, 1000)
    plt.plot(t, [k*slope_ci[0] + intercept_ci[0] for k in t], label="low bound ci")
    plt.plot(t, [k*slope_ci[1] + intercept_ci[1] for k in t], label="upp bound ci")
    plt.plot(t, [k*scaler_slope*slope_CA + scaler_intercept*intercept_CA for k in t], label="CA model")
    plt.scatter(calibration_points[:, 0], calibration_points[:, 1], label="cali")
    plt.scatter(validation_points[:, 0], validation_points[:, 1], label="vali")
    plt.legend()
    plt.show()


if __name__ == "__main__":
    main()