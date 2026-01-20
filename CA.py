from config import (
    EMPTY, MOORE_NBD, MUSHROOMS, OLDER
)

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

    def dist(self, other):
        return abs(self.x - other.x) + abs(self.y - other.y)

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
        self.state_grids: list[dict[tuple[int, int], int]] = [{}]
        self.toxicity_grids: list[dict[tuple[int, int], float]] = [{}]
        self.time = 0

    def get_grid_representation(
        self,
        min_x: int = 0,
        max_x: int | None = None,
        min_y: int = 0,
        max_y: int | None = None,
        show_toxins: bool = False
    ):
        current_state = self.state_grids[-1]

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
                        self.toxicity_grids[-1].get((y, x), 0.0), 1
                    )) + " "
                else:
                    message += str(
                        self.state_grids[-1].get((y, x), EMPTY)
                    ) + " "
            message += "\n"
        return message

    def step(self):
        new_state_grid = {}
        current_state = self.state_grids[-1]

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

        self.state_grids.append(new_state_grid)

        toxicity_grid = self.toxin_transition()
        self.toxicity_grids.append(toxicity_grid)
        self.time += 1

    def reset(self):
        self.state_grids = [{}]
        self.toxicity_grids = [{}]
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
        if state == EMPTY:
            if (y, x) in self.state_grids[time]:
                del self.state_grids[time][(y, x)]
        else:
            self.state_grids[time][(y, x)] = state

    def set_toxicity(self, x: int, y: int, toxicity: float, time: int = 0):
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
            if (y, x) in self.toxicity_grids[time]:
                del self.toxicity_grids[time][(y, x)]
        else:
            self.toxicity_grids[time][(y, x)] = toxicity

    def state_transition(self, x, y) -> int:
        raise NotImplementedError

    def toxin_transition(self) -> dict:
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

        ring_count = 0
        for fungus in mushroom_and_older_coordinates:
            min_dist = 5
            for point in hull:
                if fungus.dist(point) < min_dist:
                    min_dist = fungus.dist(point)
            if min_dist <= 3:
                ring_count += 1


        return ring_count/len(mushroom_and_older_coordinates)