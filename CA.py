from itertools import product
from constants import (
    EMPTY, SPORE, YOUNG, MATURING, MUSHROOMS, OLDER, DECAYING, DEAD1, DEAD2,
    INERT
)
import numpy as np

class Point():
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)

    def norm(self):
        return (self.x**2 + self.y**2)**(0.5)

    def __repr__(self):
        return f"{self.x} {self.y}"

def on_the_left_or_line(p1, p2, p3):
    b1 = p2 - p1
    b2 = p3 - p2
    val = b1.x*b2.y - b1.y*b2.x
    return val >= 0

def convex_hull(points):
    points.sort(key=lambda p: (p.x, p.y))
    upper_hull = []
    for i in range(len(points)):
        upper_hull.append(points[i])
        while len(upper_hull) > 2:
            if on_the_left_or_line(upper_hull[-3], upper_hull[-2], upper_hull[-1]):
                upper_hull.pop(-2)
                continue
            break
    lower_hull = []
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
    return upper_hull + lower_hull


class CA:
    def __init__(self, n: int):
        self.n: int = n
        self.state_grids: list[np.ndarray] = [np.zeros((n, n), dtype=np.uint32)]
        self.toxicity_grids: list[np.ndarray] = [np.zeros((n, n), dtype=np.float32)]
        self.time = 0

    def __repr__(self):
        state_emojis = {
            EMPTY: "⬛",
            SPORE: "✨",
            YOUNG: "👶",
            MATURING: "👦",
            MUSHROOMS: "🍄",
            OLDER: "🧑",
            DECAYING: "👴",
            DEAD1: "💀",
            DEAD2: "💀️",
            INERT: "🟥"
        }

        message = ""
        for y in range(self.n):
            for x in range(self.n):
                # Uncomment for hacky visualization of toxicity.
                # threshold = 0.3
                # if self.toxicity_grids[-1][y, x] > threshold and self.state_grids[-1][y, x] == EMPTY:
                #     message += "🟪"
                # else:
                #     message += state_emojis[self.state_grids[-1][y][x]]
                message += state_emojis[self.state_grids[-1][y, x]]
            message += "\n"
        return message

    def step(self):
        state_grid = np.zeros((self.n, self.n), dtype=np.uint32)
        for (x, y) in product(range(self.n), repeat=2):
            state_grid[y, x] = self.state_transition(self.state_grids[-1], self.toxicity_grids[-1], x, y)
        self.state_grids.append(state_grid)

        toxicity_grid =  self.toxin_transition(self.state_grids[-1], self.toxicity_grids[-1]);
        self.toxicity_grids.append(toxicity_grid)

    def set_state(self, x: int, y: int, state: int, time: int=0):
        """
        Set the state of a single cell value

        :param self: Description
        :param x: 0 indexed coordinate
        :type x: int
        :param y: 0 indexed coordinate
        :type y: int
        :param state: Description
        :type state: int
        """
        self.state_grids[time][y, x] = state

    def set_toxicity(self, x: int, y: int, toxicity: float, time: int=0):
        """
        Set the state of a single cell value

        :param self: Description
        :param x: 0 indexed coordinate
        :type x: int
        :param y: 0 indexed coordinate
        :type y: int
        :param state: Description
        :type state: int
        """
        self.toxicity_grids[time][y, x] = toxicity

    def state_transition(self, state_grid: np.ndarray, toxicity_grid: np.ndarray, x, y) -> int:
        raise NotImplementedError

    def toxin_transition(self, state_grid: np.ndarray, toxicity_grid: np.ndarray) -> np.ndarray:
        raise NotImplementedError

    def inner_ring_detector(self):
        state_grid = self.state_grids[-1]
        mushroom_and_older_coordinates = []
        for (x, y) in product(range(self.n), repeat=2):
            if state_grid[y, x] == MUSHROOMS or state_grid[y, x] == OLDER:
                mushroom_and_older_coordinates.append(Point(x, y))

        if not mushroom_and_older_coordinates:
            return 0
        hull = convex_hull(mushroom_and_older_coordinates)
        perimiter_hull = 0
        for i in range(1, len(hull)):
            perimiter_hull += (hull[i] - hull[i - 1]).norm()

        return len(hull)/len(mushroom_and_older_coordinates)