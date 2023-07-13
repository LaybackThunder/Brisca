from abc import ABC, abstractmethod

class Deck(ABC):
    
    @abstractmethod
    def __init__(self):
        raise NotImplementedError

    @abstractmethod
    def shuffle(self):
        raise NotImplementedError

    @abstractmethod
    def drawCard(self):
        raise NotImplementedError
    
    @abstractmethod
    def addCardToDeck(self, oCard, loc):
        raise NotImplementedError

    @abstractmethod
    def draw(self):
        raise NotImplementedError


