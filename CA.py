from config import (
    EMPTY, MOORE_NBD, MUSHROOMS, OLDER
)

from utils import Point, convex_hull


class CA:
    def __init__(self, n: int):
        assert n > 0, "Grid size must be positive"
        self.n: int = n
        self.state_grid: dict[tuple[int, int], int] = {}
        self.toxicity_grid: dict[tuple[int, int], float] = {}
        self.time = 0

    def get_grid_representation(
        self,
        min_x: int = 0,
        max_x: int | None = None,
        min_y: int = 0,
        max_y: int | None = None,
        show_toxins: bool = False
    ):
        current_state = self.state_grid

        # Calculate dynamic bounds
        if not current_state:
            # Default to some small area centered at 0 or start at 0 if empty
            xs, ys = [0], [0]
        else:
            xs = [x for _, x in current_state.keys()]
            ys = [y for y, _ in current_state.keys()]

        # Determine viewing window
        min_x, max_x = min(xs), max(xs)
        min_y, max_y = min(ys), max(ys)

        # Add padding
        min_x -= 2
        max_x += 3
        min_y -= 2
        max_y += 3

        message = ""
        for y in range(min_y, max_y):
            for x in range(min_x, max_x):
                if show_toxins:
                    message += str(round(
                        self.toxicity_grid.get((y, x), 0.0), 1
                    )) + " "
                else:
                    message += str(
                        self.state_grid.get((y, x), EMPTY)
                    ) + " "
            message += "\n"
        return message

    def step(self):
        new_state_grid = {}
        current_state = self.state_grid

        # Determine relevant coordinates
        coords_to_check = set(current_state.keys())
        for (y, x) in list(coords_to_check):
            # Add neighbors of active cells
            for dy, dx in MOORE_NBD:
                coords_to_check.add((y + dy, x + dx))

        for (y, x) in coords_to_check:
            new_state = self.state_transition(x, y)
            if new_state != EMPTY:
                new_state_grid[(y, x)] = new_state

        self.state_grid = new_state_grid

        toxicity_grid = self.toxin_transition()
        self.toxicity_grid = toxicity_grid
        self.time += 1

    def reset(self):
        self.state_grid = {}
        self.toxicity_grid = {}
        self.time = 0

    def set_state(self, x: int, y: int, state: int):
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
        assert 0 <= x < self.n, f"x coordinate {x} out of bounds (0-{self.n-1})"
        assert 0 <= y < self.n, f"y coordinate {y} out of bounds (0-{self.n-1})"

        if state == EMPTY:
            if (y, x) in self.state_grid:
                del self.state_grid[(y, x)]
        else:
            self.state_grid[(y, x)] = state

    def set_toxicity(self, x: int, y: int, toxicity: float):
        """
        Set the toxicity of a single cell value

        :param self: Description
        :param x: 0 indexed coordinate
        :type x: int
        :param y: 0 indexed coordinate
        :type y: int
        :param toxicity: Description
        :type toxicity: float
        """
        if toxicity <= 0:
            if (y, x) in self.toxicity_grid:
                del self.toxicity_grid[(y, x)]
        else:
            self.toxicity_grid[(y, x)] = toxicity

    def state_transition(self, x, y) -> int:
        raise NotImplementedError

    def toxin_transition(self) -> dict:
        raise NotImplementedError

    def inner_ring_detector(self) -> tuple | None:
        state_grid = self.state_grid
        mushroom_and_older_coordinates = []
        for (y, x) in state_grid.keys():
            if state_grid[(y, x)] == MUSHROOMS or state_grid[(y, x)] == OLDER:
                mushroom_and_older_coordinates.append(Point(x, y))

        if not mushroom_and_older_coordinates:
            return None

        return convex_hull(mushroom_and_older_coordinates)
