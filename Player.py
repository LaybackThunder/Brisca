from ABC_Player import Player
from Hand import *

class Player(Player):

    def __init__(self, window):
        super().__init__(window)
        self.humanPlayer = True
        self.oHand = Hand(window) # Id draw (display imgs) doesn't work check classes for fidelity.
