import random
from Card import *

class Deck():
    SUIT_TUPLE = ('Swords', 'Coins', 'Cups', 'Clubs')
    # Example: Ace is rank, value is list [pointsValue, trcikValue]
    BRISCA_DICT = {'2':[0, 2], '3':[0, 13], '4':[0, 4], '5':[0, 5],
                                  '6':[0, 6], '7':[0, 7], 'Jack':[2, 10],
                                  'Knight':[3, 11], 'King':[4, 12], 'Ace':[11, 14]}
    
    def __init__(self, window, rankValueDict=BRISCA_DICT):
        # rankValueDict defaults to STANDARD_DICT
        self.startingDeckList = []
        self.playingDeckList = []

        for suit in Deck.SUIT_TUPLE:
            for rank, value in rankValueDict.items():
                oCard = Card(window, suit, rank, value[0], trickValue=value[1])
                self.startingDeckList.append(oCard)
        
        self.shuffle()
    
    def shuffle(self):
        # Copy the starting deck and save it in the playing deck list
        self.playingDeckList = self.startingDeckList.copy()
        # Conceal all cards before you shuffle
        for oCard in self.playingDeckList:
            oCard.conceal()
        # shuffle using the random module
        random.shuffle(self.playingDeckList)
    
    def returnCardToDeck(self, oCard, loc):
        """conceal card and Put it back into the deck"""
        oCard.conceal()
        oCard.setLoc(loc)
        self.playingDeckList.append(0, oCard)

    def setLoc(self, loc):
        for oCard in self.playingDeckList:
            oCard.setLoc(loc) # call the oCard's setLoc method
    
    def getLoc(self): # get the location from the oCard
        loc = []
        for oCard in self.playingDeckList:
            locXY = self.oCard.getLoc()
            loc.append(f"{oCard.getName()} is loc at {locXY}")
        return loc
    
    def getCard(self):
        # Checks to see if there are any cards
        if len(self.playingDeckList) == 0:
            print('Ha! No more cards, go and get a life!')
            return False
        # Returns one card from the top of the deck
        oCard = self.playingDeckList.pop()
        return oCard

    def getDeck(self):
        return self.playingDeckList.copy()

# Test deck
if __name__ == "__main__":

    WINDOW_WIDTH = 100
    WINDOW_HEIGHT = 100

    pygame.init()
    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

    oDeck = Deck(window)

    for i in range(1, 41):
        oCard = oDeck.getCard()
        print(f"Name: {oCard.getName()}, Value: {oCard.getValue()}, Trick Value: {oCard.getTrickValue()}")