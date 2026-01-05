from itertools import product
import numpy as np

# State Names
EMPTY = 0
SPORE = 1
YOUNG = 2
MATURING = 3
MUSHROOMS = 4
OLDER = 5
DECAYING = 6
DEAD1 = 7
DEAD2 = 8
INERT = 9
        
class CA():
    def __init__(self, n: int):
        self.n: int = n
        self.grids: list[np.array] = [np.zeros((n, n), dtype=np.uint32)]
        self.time = 0
        
    def __repr__(self):
        message = ""
        for y in range(self.n):
            for x in range(self.n):
                message += str(self.grids[-1][y][x]) + " "
            message += "\n"
        return message
        
    def step(self):
        grid = np.zeros((self.n, self.n), dtype=np.uint32)
        for (x, y) in product(range(self.n), repeat=2):
            grid[y][x] = self.transition(self.grids[-1][y][x])
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
        
    def transition(self, state):
        if state ==  SPORE:
            return YOUNG
        elif state ==   YOUNG:
            return MATURING
        elif state ==  MATURING:
            return MUSHROOMS
        elif state ==  OLDER:
            return DECAYING
        elif state ==  MUSHROOMS:
            return DECAYING
        elif state ==  DECAYING:
            return DEAD1
        elif state ==  DEAD1:
            return DEAD2
        elif state ==  DEAD2:
            return EMPTY
        elif state ==  EMPTY:
            return YOUNG
        elif state ==  INERT:
            return INERT
        else:
            raise ValueError