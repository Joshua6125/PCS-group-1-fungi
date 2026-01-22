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

EVALUATED_FUNGI_DATASET = [
    "Agaricus aff. lilaceps", "Bovista plumbea", "Calvatia spp",
    "Disciseda candida", "Marasmius oreades"
]

# scale of CA
CELL_SCALE = 3.7299489928772203 # meters per cell
TIME_SCALE = 1                  # years per time step

# ----- VARIABLES -----
sim_parameters = {
    "n": 75,
    "prob_spore_to_hyphae": 1.0,
    "prob_mushroom": 0.7,
    "prob_spread": 0.5,
    "toxin_threshold": 0.3,
    "toxin_decay": 0.05,
    "toxin_convolution_size": 5,
    "toxin_convolution_variance": 1.0,
    "show_toxins": False
}

colors = [(0, 0.4, 0), (1, 1, 1), (1, .8, .8), (1, .4, .4),
          (.8, 0, 0), (0.4, 0.2, 0), (.4, .4, 0), (.1, .2, 0), (.1, .2, 0)]
state_names = [
    'Empty', 'Spore', 'Young', 'Maturing', 'Mushrooms', 'Older', 'Decaying',
    'Dead',
]
