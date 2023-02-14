import pygwidgets
from Deck import *
from Card import *
from Player import *

class Game():
    # Class Variables
    HAND_CARD_OFFSET = 20 # player's cards buffer between each other
    PLAYER2_HAND_CARDS_TOP = 400 # Y coordinate
    PLAYER1_HAND_CARDS_BOTTOM = 100 # Y coordinate
    CARDS_LEFT = 75 # X coordinate
    DISPLAY_STARTING_HANDS = 3
    MAX_HAND = 3
    
    def __init__(self, window):
        """Initisialize attributes."""
        self.window = window
        self.oDeck = Deck(self.window)
        self.trumpCard = None
        self.dealerPot = []
        self.oPlayer1 = Player(1)
        self.oPlayer2 = Player(0)
        self.playerList = [self.oPlayer1, self.oPlayer2]
        self.potScore = 0
        self.potScoreText = pygwidgets.DisplayText(window, (450, 164),
                                        f'Pot Score: {self.potScore}',
                                        fontSize=36, textColor=(255, 255, 255))
        
        self.messageText = pygwidgets.DisplayText(window, (50, 460),
                                        f'', width=900, justified='center',
                                        fontSize=36, textColor=(255, 255, 255))
        
        # Card shuffle sound
        self.cardShuffleSound = pygame.mixer.Sound("sounds/cardShuffle.wav")
        # Win sound
        self.winnerSound = pygame.mixer.Sound("sounds/ding.wav")
        # Lost sound
        self.loserSound = pygame.mixer.Sound("sounds/loser.wav")
        
        # Calculating Players card positions within the player's hand
        self.cardXPositionList = []
        thisLeft = Game.CARDS_LEFT # Starting card to the left of hand

        # Calculate the x positions of all cards, once 
        for cardNum in range(Game.DISPLAY_STARTING_HANDS): # 3 cards
            self.cardXPositionList.append(thisLeft)
            thisLeft += Game.HAND_CARD_OFFSET # Space between cards
        # Both players can share X position
        self.player1CardXPositionList = self.cardXPositionList.copy()
        self.player2CardXPositionList = self.cardXPositionList.copy()
        
        # Game decides who goes first at random before game starts
        self.highestCardWinds()
        
    def reset(self):
        """This method is called when a new round starts"""
        # play shuffle sound
        oDeck.shuffle() # shuffle deck

        # Pick a Trump card
        oCard = oDeck.getCard()
        self.trumpCard = oCard
        
        # deal cards to players
        for i in range(Game.MAX_HAND): # Players draw up to 3 cards
            for oPlayer in self.playerList:

                # take one card from deck
                oCard = self.oDeck.getCard()

                # set card coordinates per player hand location is...
                if oPlayer.getTurnPlayer:  # If player is turnPlayer do or die!
                    oPlayer.setHand(oCard) # Set card in oPlayer's hand

                    if oPlayer.getPlayerId() == 0: # Set card coordinates for oPlayer1
                        cardLocX = self.player1CardXPositionList.pop(0) # Add x-coordinates
                        oCard.setLoc(cardLocX, Game.PLAYER1_HAND_CARDS_BOTTOM) # Add coordinates
                        oCard.reveal() # show player card running the software

                    else:                          # Set card coordinates for oPlayer2
                        cardLocX = self.player2CardXPositionList.pop(0)
                        oCard.setLoc(cardLocX, Game.PLAYER2_HAND_CARDS_TOP)

    def highestCardWinds(self):
        """Player with the highest card value wins to be turnPlayer."""
        
        for oPlayer in self.playerList: # Players draw one card each
            oCard = self.oDeck.getCard() # player draws
            oPlayer.setHand(oCard) # player puts card in their hand

        # Players compare cards and decide who will be turn player   
        if self.oPlayer1.hand[0].getTrickValue() > self.oPlayer2.hand[0].getTrickValue(): # If player 1 wins and set as turn player
                print("-------Player 1 wins")
                self.oPlayer1.setTurnPlayer(True) # Player1 is turnPlayer, player 2 is false by defult
                self.playerList = [self.oPlayer1, self.oPlayer2] # Player arrangement decides who draws first
                # Remove the 1st card from each player's hand
                for oPlayer in self.playerList:
                    oCard = oPlayer.removeCard(0) # Remove card from player's hand
                    oDeck.returnCardToDeck(oCard) # Card returns to deck
           
        elif oPlayer.hand[0].getTrickValue() < oPlayer2.hand[0].getTrickValue():  # if player 2 wins and set as turn player
                print("-------Player 2 wins")
                self.oPlayer2.setTurnPlayer(True) # Player2 is turnPlayer, player 1 is false by defult
                self.playerList = [self.oPlayer2, self.oPlayer1] # Player arrangement decides who draws first
                # Remove the 1st card from each player's hand
                for oPlayer in self.playerList:
                    oCard = oPlayer.removeCard(0) # Remove card from player's hand
                    oDeck.returnCardToDeck(oCard) # Card returns to deck
            
        else: # If players end in a tie, repeat process above
            for oPlayer in self.playerList:
                oCard = oPlayer.removeCard(0) # Remove card from player's hand
                oDeck.returnCardToDeck(oCard) # Card returns to deck
            oDeck.shuffle()

            tie = True
            while tie:
                # Players draw one card each
                for oPlayer in self.playerList: # Loop player list
                    oCard = self.oDeck.getCard() # player draws
                    oPlayer.setHand(oCard) # player puts card in their hand

                # Players compare cards    
                if self.oPlayer1.hand[0].getTrickValue() > self.oPlayer2.hand[0].getTrickValue(): # If player 1 wins and set as turn player
                    print("-------Player 1 wins")
                    self.oPlayer1.setTurnPlayer(True) # Player1 is turnPlayer, player 2 is false by defult
                    self.playerList = [self.oPlayer1, self.oPlayer2] # Player arrangement decides who draws first
                    tie = False # Exit loop
                    # Remove the 1st card from each player's hand
                    for oPlayer in self.playerList:
                        oCard = oPlayer.removeCard(0) # Remove card from player's hand
                        oDeck.returnCardToDeck(oCard) # Card returns to deck
           
                elif oPlayer.hand[0].getTrickValue() < oPlayer2.hand[0].getTrickValue():  # if player 2 wins and set as turn player
                    print("-------Player 2 wins")
                    self.oPlayer2.setTurnPlayer(True) # Player2 is turnPlayer, player 1 is false by defult
                    self.playerList = [self.oPlayer2, self.oPlayer1] # Player arrangement decides who draws first
                    tie = False # Exit loop
                    # Remove the 1st card from each player's hand
                    for oPlayer in self.playerList:
                        oCard = oPlayer.removeCard(0) # Remove card from player's hand
                        oDeck.returnCardToDeck(oCard) # Card returns to deck
                
                else: # If tie again repeat while loop
                    for oPlayer in self.playerList:
                        oCard = oPlayer.removeCard(0) # Remove card from player's hand
                        oDeck.returnCardToDeck(oCard) # Card returns to deck
                    oDeck.shuffle()

        self.reset()# start a round of the game

        """
        Which sections of the method can be their own little methods?
        """
    
    def setDealerPot(self, oCards):
        """Appends object Cards to dealerPot list after a trick tie."""
        for oCard in oCards.copy():
            self.dealerPot.append(oCard)
    
    def getDealerPot(self):
        """This method is used by setPot Transfer """
        return self.dealerPot
    
    def setDealerPotTransfer(self, player):
        """The dealerPot gives all it's cards to a player's pot."""
        dealerPot = self.getDealerPot.copy() # Itterate using a copy of the list
        for card in dealerPot:
            card = self.dealerPot.pop(0) # Remove items using real list
            player.setPot(card)  

    def trick(self, playersAndCards):
        """
        Players have chosen their cards for battle; now they fight for supremacy, but mostly points.
        If tie, cards are placed with the dealer pot; after a tie, which ever player wins the following trick
        gains all the dealer pot cards, uuh nice!
        """
        # playersAndCards is a dictionary with the player's iD and corresponding cards
        # Create local variables to identify players (playeriDs) and their cards (oCards)????

        # Compare player's trump cards to the main trump card
        isPlayer1Trump = playersAndCards[0].getSuit() == self.trumpCard.getSuit()
        isPlayer2Trump = playersAndCards[1].getSuit() == self.trumpCard.getSuit()

        if isPlayer1Trump and isPlayer2Trump: # Both players have a trump card
            # Compares player's cards; the higest value card wins and gets the spoils of war!
            if (playersAndCards[0].getTrickValue() > playersAndCards[1].getTrickValue()):
                print("-------Player 1 wins")
                # Place the cards in a list
                potCards = [playersAndCards[0], playersAndCards[1]]
                # Add cards into player pot
                for card in potCards.copy():
                    card = potCards.pop(0)
                    self.oPlayer1.setPot(card)

                if self.dealerPot: # If there are cards in the dealer list, give them all to player1
                    self.setDealerPotTransfer(self.oPlayer1) # Player1 has all the dealer cards in their pot
            
            elif playersAndCards[0].getTrickValue() < playersAndCards[1].getTrickValue():
                print("-------Player 2 wins")
                # Place the cards in a list
                potCards = [playersAndCards[0], playersAndCards[1]]
                # Add cards into player pot
                for card in potCards.copy():
                    card = potCards.pop(0)
                    self.oPlayer2.setPot(card)
                
                if self.dealerPot: # If there are cards in the dealer list, give them all to player2
                        self.setDealerPotTransfer(self.oPlayer2) # Player2 has all the dealer cards in their pot         
            
            else: # Tie
                print("-------ITS A TIE! T.T")
                potCards = [playersAndCards[0], playersAndCards[1]]
                self.setDealerPot(potCards) # Trick cards are set to dealerPot  
        
        elif isPlayer1Trump or isPlayer2Trump: # A player has a trump card
            if isPlayer1Trump:
                print("-------Player 1 wins")
                # Place the cards in a list
                potCards = [playersAndCards[0], playersAndCards[1]]
                # Add cards into player pot
                for card in potCards.copy():
                    card = potCards.pop(0)
                    self.oPlayer1.setPot(card)

                if self.dealerPot: # If there are cards in the dealer list, give them all to player1
                    self.setDealerPotTransfer(self.oPlayer1)
            else:
                print("-------Player 2 wins")
                # Place the cards in a list
                potCards = [playersAndCards[0], playersAndCards[1]]
                # Add cards into player pot
                for card in potCards.copy():
                    card = potCards.pop(0)
                    self.oPlayer2.setPot(card)

                if self.dealerPot: # If there are cards in the dealer list, give them all to player2
                    self.setDealerPotTransfer(self.oPlayer2)
        
        # Are there any cards left in the deck?
