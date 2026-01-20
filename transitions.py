from CA import CA
from config import (
    EMPTY, SPORE, YOUNG, MATURING, MUSHROOMS, OLDER, DECAYING, DEAD1, DEAD2,
    INERT, MOORE_NBD, TOXIN_RELEASING_STATES
)
import numpy as np


class BasicSim(CA):
    def __init__(self, parameters):
        super().__init__(parameters["n"])
        self.prob_spore_to_hyphae: float = parameters["prob_spore_to_hyphae"]
        self.prob_mushroom: float = parameters["prob_mushroom"]
        self.prob_spread: float = parameters["prob_spread"]

    def change_parameters(self, parameters):
        self.prob_spore_to_hyphae: float = parameters["prob_spore_to_hyphae"]
        self.prob_mushroom: float = parameters["prob_mushroom"]
        self.prob_spread: float = parameters["prob_spread"]

    def state_transition(self, x: int, y: int) -> int:
        state_grid = self.state_grids[-1]
        state = state_grid.get((y, x), EMPTY)

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
                # No boundary check needed for infinite grid
                if not state_grid.get((y + dy, x + dx), EMPTY) == YOUNG:
                    continue
                if np.random.random() < self.prob_spread/np.linalg.norm((dx, dy)):
                    return YOUNG
            return EMPTY

        if state == INERT:
            return INERT

        raise ValueError

    def toxin_transition(self) -> dict:
        return {}


class BasicToxinSim(CA):
    def __init__(self, parameters):
        super().__init__(parameters["n"])
        self.prob_spore_to_hyphae: float = parameters["prob_spore_to_hyphae"]
        self.prob_mushroom: float = parameters["prob_mushroom"]
        self.prob_spread: float = parameters["prob_spread"]
        self.toxin_threshold: float = parameters["toxin_threshold"]
        self.toxin_decay: float = parameters["toxin_decay"]
        self.toxin_convolution: np.ndarray = parameters["toxin_convolution"]

    def change_parameters(self, parameters):
        self.prob_spore_to_hyphae: float = parameters["prob_spore_to_hyphae"]
        self.prob_mushroom: float = parameters["prob_mushroom"]
        self.prob_spread: float = parameters["prob_spread"]
        self.toxin_threshold: float = parameters["toxin_threshold"]
        self.toxin_decay: float = parameters["toxin_decay"]
        self.toxin_convolution: np.ndarray = parameters["toxin_convolution"]

    def state_transition(self, x: int, y: int) -> int:
        state_grid = self.state_grids[-1]
        toxicity_grid = self.toxicity_grids[-1]

        state = state_grid.get((y, x), EMPTY)

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
                if not state_grid.get((y + dy, x + dx), EMPTY) == YOUNG:
                    continue
                if toxicity_grid.get((y, x), 0.0) > self.toxin_threshold:
                    continue
                if np.random.random() <\
                        self.prob_spread / np.linalg.norm((dx, dy)):
                    return YOUNG
            return EMPTY

        if state == INERT:
            return INERT

        raise ValueError

    def toxin_transition(self) -> dict:
        state_grid = self.state_grids[-1]
        toxicity_grid = self.toxicity_grids[-1]

        source_grid = {}

        # Consider all existing toxicity
        for (y, x), val in toxicity_grid.items():
            state = state_grid.get((y, x), EMPTY)
            if state in TOXIN_RELEASING_STATES:
                source_grid[(y, x)] = 1
            else:
                new_val = max(val - self.toxin_decay, 0)
                if new_val > 0:
                    source_grid[(y, x)] = new_val

        # Consider all toxin releasing states
        for (y, x), state in state_grid.items():
            if state in TOXIN_RELEASING_STATES:
                source_grid[(y, x)] = 1

        # Sparse convolution
        new_toxicity_grid = {}
        kernel = self.toxin_convolution
        ky, kx = kernel.shape
        cy, cx = ky // 2, kx // 2

        for (y, x), val in source_grid.items():
            # Apply kernel
            for dy in range(ky):
                for dx in range(kx):
                    kv = kernel[dy, dx]
                    # Skip zero entries
                    if kv == 0:
                        continue

                    target_y = y + (dy - cy)
                    target_x = x + (dx - cx)

                    # Accumulate
                    new_toxicity_grid[(target_y, target_x)] =\
                        new_toxicity_grid.get((target_y, target_x), 0.0)\
                        + val * kv

        return new_toxicity_grid


class ProbToxinSim(CA):
    def __init__(self, parameters):
        super().__init__(parameters["n"])
        self.prob_spore_to_hyphae: float = parameters["prob_spore_to_hyphae"]
        self.prob_mushroom: float = parameters["prob_mushroom"]
        self.prob_spread: float = parameters["prob_spread"]
        self.toxin_decay: float = parameters["toxin_decay"]
        self.toxin_convolution: np.ndarray = parameters["toxin_convolution"]

    def change_parameters(self, parameters):
        self.prob_spore_to_hyphae: float = parameters["prob_spore_to_hyphae"]
        self.prob_mushroom: float = parameters["prob_mushroom"]
        self.prob_spread: float = parameters["prob_spread"]
        self.toxin_decay: float = parameters["toxin_decay"]
        self.toxin_convolution: np.ndarray = parameters["toxin_convolution"]

    def state_transition(self, x: int, y: int) -> int:
        state_grid = self.state_grids[-1]
        toxicity_grid = self.toxicity_grids[-1]

        state = state_grid.get((y, x), EMPTY)

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
                if not state_grid.get((y + dy, x + dx), EMPTY) == YOUNG:
                    continue
                if np.random.random() < toxicity_grid.get((y, x), 0.0):
                    continue
                if np.random.random() < self.prob_spread/np.linalg.norm((dx, dy)):
                    return YOUNG
            return EMPTY

        if state == INERT:
            return INERT

        raise ValueError

    def toxin_transition(self) -> dict:
        state_grid = self.state_grids[-1]
        toxicity_grid = self.toxicity_grids[-1]

        source_grid = {}

        # Consider all existing toxicity
        for (y, x), val in toxicity_grid.items():
            state = state_grid.get((y, x), EMPTY)
            if state in TOXIN_RELEASING_STATES:
                source_grid[(y, x)] = 1
            else:
                new_val = max(val - self.toxin_decay, 0)
                if new_val > 0:
                    source_grid[(y, x)] = new_val

        # Consider all toxin releasing states
        for (y, x), state in state_grid.items():
            if state in TOXIN_RELEASING_STATES:
                source_grid[(y, x)] = 1

        # Sparse convolution
        new_toxicity_grid = {}
        kernel = self.toxin_convolution
        ky, kx = kernel.shape
        cy, cx = ky // 2, kx // 2

        for (y, x), val in source_grid.items():
            # Apply kernel
            for dy in range(ky):
                for dx in range(kx):
                    kv = kernel[dy, dx]
                    # Skip zero entries
                    if kv == 0:
                        continue

                    target_y = y + (dy - cy)
                    target_x = x + (dx - cx)

                    # Accumulate
                    new_toxicity_grid[(target_y, target_x)] = new_toxicity_grid.get((target_y, target_x), 0.0) + val * kv

        return new_toxicity_grid


class ProbToxinDeathSim(CA):
    def __init__(self, parameters):
        super().__init__(parameters["n"])
        self.prob_spore_to_hyphae: float = parameters["prob_spore_to_hyphae"]
        self.prob_mushroom: float = parameters["prob_mushroom"]
        self.prob_spread: float = parameters["prob_spread"]
        self.toxin_decay: float = parameters["toxin_decay"]
        self.toxin_convolution: np.ndarray = parameters["toxin_convolution"]

    def change_parameters(self, parameters):
        self.prob_spore_to_hyphae: float = parameters["prob_spore_to_hyphae"]
        self.prob_mushroom: float = parameters["prob_mushroom"]
        self.prob_spread: float = parameters["prob_spread"]
        self.toxin_decay: float = parameters["toxin_decay"]
        self.toxin_convolution: np.ndarray = parameters["toxin_convolution"]

    def state_transition(self, x: int, y: int) -> int:
        state_grid = self.state_grids[-1]
        toxicity_grid = self.toxicity_grids[-1]

        state = state_grid.get((y, x), EMPTY)

        if state == SPORE:
            if np.random.random() < toxicity_grid.get((y, x), 0.0):
                return DEAD1
            if np.random.random() < self.prob_spore_to_hyphae:
                return YOUNG
            return SPORE

        if state == YOUNG:
            if np.random.random() < toxicity_grid.get((y, x), 0.0):
                return DEAD1
            return MATURING

        if state == MATURING:
            if np.random.random() < toxicity_grid.get((y, x), 0.0):
                return DEAD1
            if np.random.random() < self.prob_mushroom:
                return MUSHROOMS
            return OLDER

        if state == OLDER:
            if np.random.random() < toxicity_grid.get((y, x), 0.0):
                return DEAD1
            return DECAYING

        if state == MUSHROOMS:
            if np.random.random() < toxicity_grid.get((y, x), 0.0):
                return DEAD1
            return DECAYING

        if state == DECAYING:
            return DEAD1

        if state == DEAD1:
            return DEAD2

        if state == DEAD2:
            return EMPTY

        if state == EMPTY:
            for (dx, dy) in MOORE_NBD:
                if not state_grid.get((y + dy, x + dx), EMPTY) == YOUNG:
                    continue
                if np.random.random() <\
                        self.prob_spread / np.linalg.norm((dx, dy)):
                    return YOUNG
            return EMPTY

        if state == INERT:
            return INERT

        raise ValueError

    def toxin_transition(self) -> dict:
        state_grid = self.state_grids[-1]
        toxicity_grid = self.toxicity_grids[-1]

        source_grid = {}

        # Consider all existing toxicity
        for (y, x), val in toxicity_grid.items():
            state = state_grid.get((y, x), EMPTY)
            if state in TOXIN_RELEASING_STATES:
                source_grid[(y, x)] = 1
            else:
                new_val = max(val - self.toxin_decay, 0)
                if new_val > 0:
                    source_grid[(y, x)] = new_val

        # Consider all toxin releasing states
        for (y, x), state in state_grid.items():
            if state in TOXIN_RELEASING_STATES:
                source_grid[(y, x)] = 1

        # Sparse convolution
        new_toxicity_grid = {}
        kernel = self.toxin_convolution
        ky, kx = kernel.shape
        cy, cx = ky // 2, kx // 2

        for (y, x), val in source_grid.items():
            # Apply kernel
            for dy in range(ky):
                for dx in range(kx):
                    kv = kernel[dy, dx]
                    # Skip zero entries
                    if kv == 0:
                        continue

                    target_y = y + (dy - cy)
                    target_x = x + (dx - cx)

                    # Accumulate
                    new_toxicity_grid[(target_y, target_x)] =\
                        new_toxicity_grid.get((target_y, target_x), 0.0) +\
                        val * kv

        return new_toxicity_grid
