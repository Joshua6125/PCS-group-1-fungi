from itertools import product

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
    def __init__(self, x: int, y: int, state: int):
        self.x: int = x
        self.y: int = y
        self.state: int = state
        
    def transition(self):
        if self.state == SPORE:
            self.state = YOUNG
        elif self.state ==  YOUNG:
            self.state = MATURING
        elif self.state == MATURING:
            self.state = MUSHROOMS
        elif self.state == OLDER:
            self.state = DECAYING
        elif self.state == MUSHROOMS:
            self.state = DECAYING
        elif self.state == DECAYING:
            self.state = DEAD1
        elif self.state == DEAD1:
            self.state = DEAD2
        elif self.state == DEAD2:
            self.state = EMPTY
        elif self.state == EMPTY:
            self.state = YOUNG
        elif self.state == INERT:
            self.state = INERT
        else:
            raise ValueError
    
    def __repr__(self):
        return str(self.state)
        

class CA_Grid():
    def __init__(self, n: int):
        self.n: int = n
        self.grid: list[list[CA]] = [[CA(x, y, 0) for x in range(n)] for y in range(self.n)]
        
    def __repr__(self):
        message = ""
        for y in range(self.n):
            for x in range(self.n):
                message += str(self.grid[y][x]) + " "
            message += "\n"
        return message
        
    def step(self):
        for (x, y) in product(range(self.n), repeat=2):
            self.grid[y][x].transition()