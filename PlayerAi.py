from ABC_Player import Player


class PlayerAi(Player):

    # Class variables
    GHOST_HAND_Y_LOCATION = 650
    GHOST_HAND_LOC_LIST = [(300, GHOST_HAND_Y_LOCATION), 
                           (500, GHOST_HAND_Y_LOCATION)]
    GHOST_OBJ_Card = None # Ghost player on hold; code later

    def __init__(self, window, turnPlayer):
        super().__init__(window, turnPlayer)