from itertools import product
from constants import (
    EMPTY, SPORE, YOUNG, MATURING, MUSHROOMS, OLDER, DECAYING, DEAD1, DEAD2,
    INERT
)
import numpy as np


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
                message += state_emojis[self.state_grids[-1][y][x]]
            message += "\n"
        return message

    def step(self):
        state_grid = np.zeros((self.n, self.n), dtype=np.uint32)
        toxicity_grid = np.zeros((self.n, self.n), dtype=np.uint32)

        for (x, y) in product(range(self.n), repeat=2):
            state, toxicity = self.transition(self.state_grids[-1], self.toxicity_grids[-1], x, y)
            state_grid[y][x] = state
            toxicity_grid[y][x] = toxicity

        self.state_grids.append(state_grid)
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
        self.state_grids[time][y][x] = state

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
        self.toxicity_grids[time][y][x] = toxicity

    def transition(self, state_grid, toxicity_grid, x, y):
        raise NotImplementedError
