import numpy as np
import csv
import matplotlib.pyplot as plt


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
        for i, (n, d, g, a, y) in enumerate(reader):
            if not i: continue
            if n == "A. argenteus" or n == "Geastrum sp.": continue
            diameter = int(d)
            age = int(a)
            points.append((diameter, age))

    points = np.array(points)

    print(points.T)

    # Add bias term to x-values
    X_b = np.c_[np.ones((len(points), 1)), points.T[0]]

    Y_val = points.T[1]

    # Minimize the sum of squared residuals
    res = np.linalg.inv(X_b.T.dot(X_b)).dot(X_b.T).dot(Y_val)

    print(res)

    slope = res[1]
    intercept = res[0]

    print("slope:", slope, "intercept:", intercept)

    return intercept, slope, points.T


# i, s, p = linear_regression()

# t = np.linspace(0, max(p[0]), 1000)
# plt.scatter(*p)
# plt.plot(t, [i + s*k for k in t])
# plt.show()