from itertools import product
from config import (
    EMPTY, SPORE, YOUNG, MATURING, MUSHROOMS, OLDER, DECAYING, DEAD1, DEAD2,
    INERT
)
import numpy as np


class CA:
    def __init__(self, n: int):
        self.n: int = n
        self.state_grids: list[np.ndarray] = [
            np.zeros((n, n), dtype=np.uint32)]
        self.toxicity_grids: list[np.ndarray] = [
            np.zeros((n, n), dtype=np.float32)]
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
                threshold = 0.3
                if self.toxicity_grids[-1][y, x] > threshold and self.state_grids[-1][y, x] == EMPTY:
                    message += "🟪"
                else:
                    message += state_emojis[self.state_grids[-1][y][x]]
                # message += state_emojis[self.state_grids[-1][y, x]]
            message += "\n"
        return message

    def step(self):
        state_grid = np.zeros((self.n, self.n), dtype=np.uint32)
        for (x, y) in product(range(self.n), repeat=2):
            state_grid[y, x] = self.state_transition(x, y)
        self.state_grids.append(state_grid)

        toxicity_grid = self.toxin_transition()
        self.toxicity_grids.append(toxicity_grid)

    def reset(self):
        self.state_grids: list[np.ndarray] = [
            np.zeros((n, n), dtype=np.uint32)]
        self.toxicity_grids: list[np.ndarray] = [
            np.zeros((n, n), dtype=np.float32)]
        self.time = 0

    def set_state(self, x: int, y: int, state: int, time: int = 0):
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

    def set_toxicity(self, x: int, y: int, toxicity: float, time: int = 0):
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

    def state_transition(self, x, y) -> int:
        raise NotImplementedError

    def toxin_transition(self) -> np.ndarray:
        raise NotImplementedError
