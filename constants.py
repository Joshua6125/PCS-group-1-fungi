# States
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

# Neighborhoods
VON_NEUMANN_NBD = [(1, 0), (-1, 0), (0, 1), (0, -1)]
MOORE_NBD = [
    (1, 1),  (1, 0),  (1, -1),
    (0, 1),           (0, -1),
    (-1, 1), (-1, 0), (-1, -1)
]
