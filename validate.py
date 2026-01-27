from config import sim_parameters, SPORE
from transitions import BasicSim, BasicToxinSim, ProbToxinSim, ProbToxinDeathSim
import utils

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

            area = utils.area_polygon(hull_points)
            diameter = 2*np.sqrt(area/np.pi)

            points.append((diameter, sim.time))
            hull_ratios.append(hull_ratio)

        points = np.array(points)
        res = utils.linear_regression(points)
        if res[0] is None:
            continue

        slopes.append(res[1])
        intercepts.append(res[0])

    return intercepts, slopes, hull_ratios


def main():
    # Validation parameters
    HULL_RATIO = 0.9
    STEPS = 50
    ITERS = 200
    PLOT_TYPE = 3

    np.random.seed(42)

    # Get real data
    data_points = utils.read_fairy_data()
    n = len(data_points)

    # Select a third of the points
    np.random.shuffle(data_points)
    calibration_points = data_points[:n//3]
    validation_points = data_points[n//3:]

    # Perform linear regression on points for slope
    intercept_data, slope_data_calibration = utils.linear_regression(calibration_points)
    if slope_data_calibration is None:
        raise Exception("Calibrating failed.")

    # Calculate CA slope for calibration
    intercept_CA_arr, slope_CA_arr, hull_ratio_arr = estimate_CA_vars(sim_parameters, iterations=ITERS, steps=STEPS)

    intercept_CA = np.mean(intercept_CA_arr)
    slope_CA = np.mean(slope_CA_arr)
    hull_ratio = np.mean(hull_ratio_arr)

    if hull_ratio < HULL_RATIO:
        print(f"Too many inner rings. Avg ratio: {hull_ratio:.2f}")
        return

    # Scaler for CA to calibrate to real data
    scaler_slope = slope_data_calibration / slope_CA
    scaler_intercept = intercept_data / intercept_CA

    # Calculate confindence interval of remaining points
    intercept_ci, slope_ci = utils.regression_ci(validation_points)

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

    if PLOT_TYPE == 0:
        slope_ref = 0.5 * (slope_ci[0] + slope_ci[1])
        intercept_ref = 0.5 * (intercept_ci[0] + intercept_ci[1])

        residual_CA = (scaler_slope * slope_CA * t + scaler_intercept * intercept_CA) - (slope_ref * t + intercept_ref)

        residual_lower = (slope_ci[0] - slope_ref) * t + (intercept_ci[0] - intercept_ref)
        residual_upper = (slope_ci[1] - slope_ref) * t + (intercept_ci[1] - intercept_ref)

        plt.fill_between(t, residual_lower, residual_upper, alpha=0.3, label="residual 95% confidence band")
        plt.plot(t, residual_CA, linewidth=2, label="Residual scaled CA model")
        plt.xlabel("Time")
        plt.ylabel("Residual Diameter")
    elif PLOT_TYPE == 1:
        CA_val = scaler_slope*slope_CA*t + scaler_intercept*intercept_CA

        lower = slope_ci[0] * t + intercept_ci[0]
        upper = slope_ci[1] * t + intercept_ci[1]

        plt.fill_between(t, lower, upper, alpha=0.3, label="residual 95% confidence band")
        plt.plot(t, CA_val, linewidth=1, label="Residual scaled CA model")
        plt.xlabel("Time")
        plt.ylabel("Diameter")
    elif PLOT_TYPE == 2:
        scaled_ca_slopes = scaler_slope * np.array(slope_CA_arr)

        plt.hist(scaled_ca_slopes, bins=30, density=True, alpha=0.6, label="CA slope distribution")
        plt.axvspan(slope_ci[0], slope_ci[1], alpha=0.3, label="95% empirical CI")
        plt.axvline(slope_data_calibration, linestyle="--", linewidth=2, label="Empirical slope")
        plt.xlabel("Radial growth rate")
        plt.ylabel("Density")
    elif PLOT_TYPE == 3:
        bootstrap_ci = utils.bootstrap_slope_ci(validation_points)
        scaled_ca_slopes = scaler_slope * np.array(slope_CA_arr)
        plt.hist(scaled_ca_slopes, bins=30, density=True, alpha=0.6, label="CA slope distribution")
        plt.axvspan(bootstrap_ci[0], bootstrap_ci[1], alpha=0.3, label="95% emprical percentile")
        plt.axvline(slope_data_calibration, linestyle="--", linewidth=2, label="Empirical slope")
        plt.xlabel("Radial growth rate")
        plt.ylabel("Density")

    plt.legend()
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()