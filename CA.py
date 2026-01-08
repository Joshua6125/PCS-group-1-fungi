from itertools import product
from constants import *
import numpy as np


class CA:
    def __init__(self, n: int):
        self.n: int = n
        self.grids: list[np.ndarray] = [np.zeros((n, n), dtype=np.uint32)]
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
                message += state_emojis[self.grids[-1][y][x]]
            message += "\n"
        return message

    def step(self):
        grid = np.zeros((self.n, self.n), dtype=np.uint32)
        for (x, y) in product(range(self.n), repeat=2):
            grid[y][x] = self.transition(self.grids[-1], x, y)
        self.grids.append(grid)

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
        self.grids[time][y][x] = state

    def transition(self, grid, x, y):
        raise NotImplementedError
