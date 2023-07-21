from abc import ABC, abstractmethod



"""Currently:
I am reading OOPython's inheritance chapter to refresh my knowledge 
on the subject. I am currently creating a Hand abstract class. 
The purpuse is to give players and AI functionality that do the same thing,
but implemented differently.   
"""

class ABC_Hand(ABC):
    """Currently:
    All methods meet the needs of a human player's hand.
    """

    def __init__(self, window, HAND_LOCATION_DICT):
        self.window = window
        self.cardList = [] # Holds all the cards on hand
        self.iDCardSlots = [] # Remembers where cards are on hand; holds location ids
        self.oCard = None
        self.clickableHand = True
        self.oCardClicked = False # Used in parallel with oCard's self.oCardClicked.
        self.HAND_LOCATION_DICT = HAND_LOCATION_DICT


    def disableAllCardsOnHand(self):
        """Disables all cards on hand to avoid being click able.""" 
        self.clickableHand = False
    
    def enableAllCardsOnHand(self):
        """Enables all cards on hand to be click able.""" 
        self.clickableHand = True

    def getCardClick(self):
        """Returns a bool of card's click status."""
        return self.oCardClicked

    def _popCardFromHand(self):
        """
        This method retrives a card from the hand and returns the selected card 
        as the new trump card or for selcted card to enter a trick.
        """
        try: 
            oCardIndex = self.cardList.index(self.oCard) # Identify card's index.
            selectedCard = self.cardList.pop(oCardIndex) # Use index to pop oCard from the hand

            self.enableAllCardsOnHand() # Enables other cards on hand to be selected
            self.setCardClickedToFalse(selectedCard) # Selected card is set to unclickled, a.k.a False
            self.retriveCardId(selectedCard) # Obtain selected card's iD; Id is reassiged to a drawn or swaped card.
            
            return selectedCard # Card left the hand; (ﾉ◕ヮ◕)ﾉ*:･ﾟ✧ peace the fuck out!

        except:
            if self.oCard is None:
                print("Object is None Type.")
    
    def enterTrick(self):
        """
            Take card from hand. 
            Returns an oCard to be a trick card; a card that will battle. 
        """
        oTrickCard = self._popCardFromHand()
        self.oCard = None

        return oTrickCard

    def getLengthCardsOnHand(self):
        """Returns the total number of cards on hand."""
        return len(self.cardList)

    def getCardsOnHand(self):
        """Returns a list of cards on hand."""
        # NOTE: This method is connected to Player class,
        # but Game cass is not using it.
        return self.cardList

    def getSelectedCardfromHand(self):
        """This method tells us which card did the player select."""
        try:
            selectedCard = self.oCard
            return selectedCard
        except:
            if self.oCard is None:
                print("Object is None Type.")
            else:
                 print("Unknown error: Check logic and/or syntax.")

    def retriveCardId(self, oCard):
            """
            Get the oCard's iD and assigns it to self.iDCardSlots.
            By re assigning old iDs we can tell new card where to go in the hand.
            iDCardSlots is sorted by numercial order to avoid erros.
            """
            self.iDCardSlots.append(oCard.getCardId())
            self.iDCardSlots.sort() 

    def _trumpSwap(self, oCard):
        """Takes trump card and adds it to the hand."""
            
        self.setCardId(oCard) # Set id cordinates for the swaped trump card  
        self.addCardToHand(oCard) # Add swaped trump card to hand
        oCard.setRotation(90) # Rotate trump card upside-up to match the other cards in hand
        self.setHandCorrdinatesForDisplay(oCard) # Give card display coordinates mapped by card iD
        self.enableAllCardsOnHand() # After card is swapped, make all cards in hand clickable
        self.setCardClickedToFalse(oCard) # The oCard place holder, has been unclicked
        self.oCard = None # Empty place holder       

    def setCardClickedToFalse(self, selectedCard):
            """Card set to not selected; GUI buttons do not interact with card no more."""
            #NOTE: self.oCardClicked is ued to tell the handleEvent how to haddle button configurations.

            selectedCard.setCardClickedToFalse() # Tells oCard that it is false
            self.oCardClicked = False # Tells hand that oCard has been set to false        

    def addCardToHand(self, oCard):
         self.cardList.insert(oCard.getCardId(), oCard)

    @abstractmethod
    def setHandCorrdinatesForDisplay(self, oCard):
        raise NotImplementedError

    @abstractmethod
    def setCardId(self, oCard):
        raise NotImplementedError

    @abstractmethod
    def _drawCard(self, oCard):
        raise NotImplementedError

    @abstractmethod
    def draw(self):
         raise NotImplementedError

    @abstractmethod
    def handleEvent(self, event): 
        raise NotImplementedError
    