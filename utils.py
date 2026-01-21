import numpy as np

import matplotlib.pyplot as plt


def gkern(l: int, sig: float, multi: float) -> np.ndarray:
    """
    creates gaussian kernel with side length `l` and a sigma of `sig`
    """
    ax = np.linspace(-(l - 1) / 2., (l - 1) / 2., l)
    gauss = np.exp(-0.5 * np.square(ax) / np.square(sig))
    kernel = np.outer(gauss, gauss)
    return kernel / np.sum(kernel) * multi

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
