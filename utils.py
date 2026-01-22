import numpy as np
import csv

from config import EVALUATED_FUNGI_DATASET


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
    gauss = np.exp(-0.5 * np.square(ax) / np.square(sig))
    return gauss / np.sum(gauss)


def apply_diffusion(source: dict, conv_size: int, conv_var: float) -> dict:
    """
    Used to apply one of two toxin diffusion convolution directions

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
        for dy in range(k):
            kv = kernel_1d[dy]
            if kv == 0:
                continue

            ty = y + (dy - c)
            target[(ty, x)] = (
                target.get((ty, x), 0.0) + val * kv
            )

    return target


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
