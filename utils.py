import numpy as np
import csv

from config import EVALUATED_FUNGI_DATASET

from scipy import stats


def gkern(l: int, sig: float) -> np.ndarray:
    """
    creates 2d gaussian kernel with side length `l` and a sigma of `sig`
    """
    ax = np.linspace(-(l - 1) / 2., (l - 1) / 2., l)
    gauss = np.exp(-0.5 * np.square(ax) / np.square(sig))
    kernel = np.outer(gauss, gauss)
    return kernel / np.sum(kernel)


def gkern_1d(l: int, sig: float) -> np.ndarray:
    """
    creates 1d gaussian kernel with side length `l` and a sigma of `sig`
    """
    ax = np.linspace(-(l - 1) / 2., (l - 1) / 2., l)
    gauss = np.exp(-0.25 * np.square(ax) / np.square(sig))
    return gauss / np.sum(gauss)


def apply_diffusion(source: dict, conv_size: int, conv_var: float) -> dict:
    """
    Apply toxin diffusion convolution directions

    :param source: Coordinates to be evaluated with toxicity level
    :type source: dict
    :param conv_size: width of convolution
    :type conv_size: int
    :param conv_var: variance of convolution
    :type conv_var: float
    :return: Returns a new set of coordinates with toxicity level
    :rtype: dict[Any, Any]
    """
    kernel_1d = gkern_1d(conv_size, conv_var)
    k = len(kernel_1d)
    c = k // 2

    target = {}
    for (y, x), val in source.items():
        for d in range(k):
            kv = kernel_1d[d]
            if kv == 0:
                continue

            t1 = y
            t2 = x + (d - c)

            target[(t1, t2)] = (
                target.get((t1, t2), 0.0) + val * kv
            )

    next_target = {}
    for (y, x), val in target.items():
        for d in range(k):
            kv = kernel_1d[d]
            if kv == 0:
                continue

            t1 = y + (d - c)
            t2 = x
            next_target[(t1, t2)] = (
                next_target.get((t1, t2), 0.0) + val * kv
            )

    return next_target


def read_fairy_data(filename="fairy_ring_data.csv") -> np.ndarray:
    """
    Reads fairy ring data from saved csv and parses it.

    :param filename: Filename of file containing data
    :return: Returns a numpy array with coordinate tuples
    :rtype: ndarray[_AnyShape, dtype[Any]]
    """
    with open(filename, 'r') as f:
        points = []

        reader = csv.reader(f, delimiter=',')
        for i, (n, d, g, a, y) in enumerate(reader):
            # Not interested in column names
            if not i: continue

            # These types don't fit our dataset, lol
            if n not in EVALUATED_FUNGI_DATASET: continue

            diameter = int(d)
            age = int(a)
            points.append((diameter, age))

    return np.array(points)


def linear_regression(points: np.ndarray | None = None) -> tuple:
    '''
    Perform linear regression
    x-values: time in days
    y-values: diameter in metersparam

    :param points: List of coordinates
    :type points: ndarray
    :return: intercept, slope
    :rtype: tuple
    '''

    # Read and parse fairy ring data if no points were given
    if points is None:
        points = read_fairy_data()

    # Should be a list of points
    assert points.shape[1] == 2

    # Add bias term to x-values
    X_b = np.c_[np.ones((len(points), 1)), points.T[0]]

    Y_val = points.T[1]

    # Minimize the sum of squared residuals
    try:
        res = np.linalg.inv(X_b.T.dot(X_b)).dot(X_b.T).dot(Y_val)
    except Exception as E:
        print(E)
        return None, None

    slope = res[1]
    intercept = res[0]

    return intercept, slope


def regression_ci(points, confidence=0.95):
    x = points[:, 0]
    y = points[:, 1]

    n = len(x)
    dof = n - 2 # degrees of freedom

    slope, intercept = np.polyfit(x, y, 1)
    y_fit = intercept + slope * x

    sigma2_hat = np.sum((y - y_fit)**2) / dof
    x_mean = np.mean(x)
    Sxx = np.sum((x - x_mean)**2)

    se_slope = np.sqrt(sigma2_hat / Sxx)
    se_intercept = se_slope * np.sqrt(np.sum(x**2) / n)

    t_val = stats.t.ppf((1 + confidence) / 2, dof)

    slope_ci = (
        slope - t_val * se_slope,
        slope + t_val * se_slope,
    )

    intercept_ci = (
        intercept - t_val * se_intercept,
        intercept + t_val * se_intercept,
    )

    return intercept_ci, slope_ci


class Point():
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)

    def norm(self) -> float:
        return (self.x**2 + self.y**2)**(0.5)

    def __repr__(self):
        return f"{self.x} {self.y}"

    def dist(self, other) -> float:
        return abs(self.x - other.x) + abs(self.y - other.y)


def on_the_left_or_line(p1: Point, p2: Point, p3: Point) -> bool:
    b1 = p2 - p1
    b2 = p3 - p2
    val = b1.x*b2.y - b1.y*b2.x
    return val > 0


def convex_hull(points: list[Point]) -> tuple[float, list[Point]]:
    points.sort(key=lambda p: (p.x, p.y))
    upper_hull: list[Point] = []
    for i in range(len(points)):
        upper_hull.append(points[i])
        while len(upper_hull) > 2:
            if on_the_left_or_line(upper_hull[-3], upper_hull[-2], upper_hull[-1]):
                upper_hull.pop(-2)
                continue
            break
    lower_hull: list[Point] = []
    for i in range(len(points) - 1, -1, -1):
        lower_hull.append(points[i])
        while len(lower_hull) > 2:
            if on_the_left_or_line(lower_hull[-3], lower_hull[-2], lower_hull[-1]):
                lower_hull.pop(-2)
                continue
            break
    if lower_hull:
        lower_hull.pop(0)
    if lower_hull:
        lower_hull.pop(-1)

    hull = upper_hull + lower_hull

    ring_count = 0
    for point in points:
        min_dist = 13
        for other_point in hull:
            if point.dist(other_point) < min_dist:
                min_dist = point.dist(other_point)
        if min_dist <= 12:
            ring_count += 1

    return ring_count/len(points), hull


def area_polygon(points: list[Point]) -> float:
    """
    Calculates the area of a convex polygon

    :param points: list of coordinate tuples
    :type points: list[Point]
    :return: area of polygon
    :rtype: float
    """
    n = len(points)

    if n <= 2:
        return 0

    area = 0
    for i in range(n):
        area += points[i].x * points[(i + 1)%n].y
        area -= points[i].y * points[(i + 1)%n].x

    return -area/2
