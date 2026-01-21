import numpy as np
import csv


def gkern(l, sig, multi):
    """
    creates gaussian kernel with side length `l` and a sigma of `sig`
    """
    ax = np.linspace(-(l - 1) / 2., (l - 1) / 2., l)
    gauss = np.exp(-0.5 * np.square(ax) / np.square(sig))
    kernel = np.outer(gauss, gauss)
    return kernel / np.sum(kernel) * multi


def linear_regression(filename="fairy_ring_data.csv") -> tuple:
    '''
    Perform linear regression fairy ring data
    x-values: time in days
    y-values: diameter in meters

    :return: intercept, slope
    :rtype: tuple
    '''

    # Read and parse fairy ring data
    # This currently ignores the type of
    with open(filename, 'r') as f:
        points = []

        reader = csv.reader(f, delimiter=',')
        for row in reader:
            points.append((row[1], row[3]))

    points = np.array(points)

    # Add bias term to x-values
    X_b = np.c_[np.ones((100, 1)), points.T[0]]

    Y_val = points.T[1]

    # Minimize the sum of squared residuals
    res = np.linalg.inv(X_b.T.dot(X_b)).dot(X_b.T).dot(Y_val)

    slope = res[1][0]
    intercept = res[0][0]

    print("slope:", slope, "intercept:", res[0][0])

    return intercept, slope
