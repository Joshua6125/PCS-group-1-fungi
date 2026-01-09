from itertools import product
from scipy.signal import convolve2d
from CA import CA
from constants import (
    EMPTY, SPORE, YOUNG, MATURING, MUSHROOMS, OLDER, DECAYING, DEAD1, DEAD2,
    INERT, MOORE_NBD, TOXIN_RELEASING_STATES
)
import numpy as np

class BasicSim(CA):
    def __init__(self, n: int, prob_spore_to_hyphae: float, prob_mushroom: float, prob_spread: float):
        super().__init__(n)
        self.prob_spore_to_hyphae = prob_spore_to_hyphae
        self.prob_mushroom = prob_mushroom
        self.prob_spread = prob_spread

    def state_transition(self, state_grid: np.ndarray, toxicity_grid: np.ndarray, x: int, y: int) -> int:
        state = state_grid[y][x]

        if state == SPORE:
            if np.random.random() < self.prob_spore_to_hyphae:
                return YOUNG
            return SPORE

        if state == YOUNG:
            return MATURING

        if state == MATURING:
            if np.random.random() < self.prob_mushroom:
                return MUSHROOMS
            return OLDER

        if state == OLDER:
            return DECAYING

        if state == MUSHROOMS:
            return DECAYING

        if state == DECAYING:
            return DEAD1

        if state == DEAD1:
            return DEAD2

        if state == DEAD2:
            return EMPTY

        if state == EMPTY:
            for (dx, dy) in MOORE_NBD:
                if not (0 <= y + dy < self.n and 0 <= x + dx < self.n):
                    continue
                if not state_grid[y + dy][x + dx] == YOUNG:
                    continue
                if np.random.random() < self.prob_spread/np.linalg.norm((dx, dy)):
                    return YOUNG
            return EMPTY

        if state ==  INERT:
            return INERT

        raise ValueError

    def toxin_transition(self, state_grid: np.ndarray, toxicity_grid: np.ndarray) -> np.ndarray:
        return np.zeros((self.n, self.n), dtype=np.uint32)


class BasicToxinSim(CA):
    def __init__(self, parameters):
        super().__init__(parameters["n"])
        self.prob_spore_to_hyphae: float = parameters["prob_spore_to_hyphae"]
        self.prob_mushroom: float = parameters["prob_mushroom"]
        self.prob_spread: float = parameters["prob_spread"]
        self.toxin_threshold: float = parameters["toxin_threshold"]
        self.toxin_decay : float = parameters["toxin_decay"]
        self.toxin_convolution: np.ndarray = parameters["toxin_convolution"]

    def state_transition(self, state_grid: np.ndarray, toxicity_grid: np.ndarray, x: int, y: int) -> int:
        state = state_grid[y][x]

        if state == SPORE:
            if np.random.random() < self.prob_spore_to_hyphae:
                return YOUNG
            return SPORE

        if state == YOUNG:
            return MATURING

        if state == MATURING:
            if np.random.random() < self.prob_mushroom:
                return MUSHROOMS
            return OLDER

        if state == OLDER:
            return DECAYING

        if state == MUSHROOMS:
            return DECAYING

        if state == DECAYING:
            return DEAD1

        if state == DEAD1:
            return DEAD2

        if state == DEAD2:
            return EMPTY

        if state == EMPTY:
            for (dx, dy) in MOORE_NBD:
                if not (0 <= y + dy < self.n and 0 <= x + dx < self.n):
                    continue
                if not state_grid[y + dy, x + dx] == YOUNG:
                    continue
                if toxicity_grid[y, x] > self.toxin_threshold:
                    continue
                if np.random.random() < self.prob_spread/np.linalg.norm((dx, dy)):
                    return YOUNG
            return EMPTY

        if state ==  INERT:
            return INERT

        raise ValueError

    def toxin_transition(self, state_grid: np.ndarray, toxicity_grid: np.ndarray) -> np.ndarray:
        for x, y in product(range(self.n), range(self.n)):
            if state_grid[y, x] in TOXIN_RELEASING_STATES:
                toxicity_grid[y, x] = 1
            else:
                toxicity_grid[y, x] = max(toxicity_grid[y][x] - self.toxin_decay, 0)

        return convolve2d(toxicity_grid, self.toxin_convolution, mode="same", boundary="fill", fillvalue=0)
