from utils import gkern

# ----- CONSTANTS -----
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

TOXIN_RELEASING_STATES = [MATURING, OLDER, DECAYING]

# ----- VARIABLES -----
sim_parameters = {
    "n": 75,
    "prob_spore_to_hyphae": 1.0,
    "prob_mushroom": 0.7,
    "prob_spread": 0.5,
    "toxin_threshold": 0.3,
    "toxin_decay": 0.05,
    "toxin_convolution": gkern(5, 1, 1),
    "show_toxins": False
}