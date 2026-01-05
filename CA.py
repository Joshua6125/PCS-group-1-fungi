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
    def __init__(self, x: int, y: int, type: int):
        self.x: int = x
        self.y: int = y
        self.type: int = type
        
    def transition():
        return

class CA_Grid():
    def __init__(self, n: int):
        self.n: int = n
        self.grid: np.array = np.zeros((n, n))