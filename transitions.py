from CA import CA
from constants import *
import numpy as np

class BasicSim(CA):
    def __init__(self, n: int, prob_spore_to_hyphae: float, prob_mushroom: float, prob_spread: float):
        super().__init__(n)
        self.prob_spore_to_hyphae = prob_spore_to_hyphae
        self.prob_mushroom = prob_mushroom
        self.prob_spread = prob_spread

    def transition(self, state_grid: list[np.ndarray], toxicity_grid: list[np.ndarray], x: int, y: int) -> int:
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