from ABC_Card import Card

class BriscaCard(Card):
    
    # Created defult values in init method to get the ghost player to work    
    def __init__(self, window, suit='Swords', rank='2', rankValue=2, rankPoints=0):
        
        self.suit = suit
        self.rank = rank 
        self.rankValue = rankValue
        self.rankPoints = rankPoints
        briscaCardName = rank + " of " + suit
        super().__init__(window, cardName=briscaCardName)
    
    # Polymorphism section 
    
    def getSuit(self):
        return self.suit
    
    def getRank(self):
        return self.rank

    def getRankValue(self):
        return self.rankValue
    
    def getRankPoints(self):
        return self.rankPoints