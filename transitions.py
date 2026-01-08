from CA import CA
from constants import *
import numpy as np

VON_NEUMANN_NBD = [(1, 0), (-1, 0), (0, 1), (0, -1)]

class BasicSim(CA):
    def __init__(self, n: int, prob_spore_to_hyphae: float, prob_mushroom: float, prob_spread: float):
        super().__init__(n)
        self.prob_spore_to_hyphae = prob_spore_to_hyphae
        self.prob_mushroom = prob_mushroom
        self.prob_spread = prob_spread


    def transition(self, grid: list[np.ndarray], x: int, y: int) -> int:
        state = grid[y][x]

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
            if any(grid[y + dy][x + dx] == YOUNG if 0 <= y + dy < self.n and 0 <= x + dx < self.n else False for (dx, dy) in VON_NEUMANN_NBD):
                if np.random.random() < self.prob_spread:
                    return YOUNG
            return EMPTY

        if state ==  INERT:
            return INERT

        raise ValueError