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
        self.oPlayer1 = Player(1) # Instantiate only one player
        self.oPlayer2 = Player(0) # When testing the class I'll create more players
        self.playerList = [self.oPlayer1, self.oPlayer2] # Leave this list empty
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
        self.highestCardWins()
        
    def draw(self):
        """Tell each card to draw an image of itself"""
        for oCard in self.cardList:
            oCard.draw()

        self.potScoreText.draw()
        self.messageText.draw()

    def setDealerPot(self, oCards):
        """Appends object Cards to dealerPot list after a trick tie."""
        for oCard in oCards.copy():
            self.dealerPot.append(oCard)
    
    def getDealerPot(self):
        """This method is used by setPot Transfer """
        return self.dealerPot
    
    def setDealerPotTransfer(self, player): # Change the name to "DealerPotTransfer" or whatever lol
        """The dealerPot gives all it's cards to tie breaker, player's pot."""
        dealerPot = self.getDealerPot.copy() # Itterate using a copy of the list
        for card in dealerPot:
            card = self.dealerPot.pop(0) # Remove items using real list
            player.setPot(card)  

    def showTrumpCard(self, oCard):
        oCard.reveal()

    def setTrump(self, oCard):
        self.trumpCard = oCard

    def highestCardWins(self):
        """
        When players enter the game room the dealer gives each player a card.
        Player with the highest card value wins to be turnPlayer.
        Player's turnPlayer var is set to True or keps False.
        """
        
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

    def reset(self):
        """This method is called when a new round starts. 
        Resets and sets; deck, pots, points
        """
        # Reset Player's pot points

        # Remove any cards in any player's pot

        self.cardShuffleSound.play() # play shuffle sound
        self.oDeck.shuffle() # shuffle deck a new deck

        # Pick a Trump card
        oCard = oDeck.getCard() 
        self.setTrump(oCard)
        # Trump location under the deck
        self.trumpCard.setLoc((600, 500))
        self.trumpCard.setRotate(90) # 90 degrees rotation
        # Reveal trump card
        self.showTrumpCard(self.trumpCard)  

        # Deck's location
        self.oDeck.setLoc((600, 500))
                
        # Deal cards to players before the game starts
        for i in range(Game.MAX_HAND): # Players draw up to 3 cards
                
            didTurnPlayerDraw = False # Tells none turn player to avoid drawing till turn player has drawn
            keepDrawing = True # Keep drawing till all players have drawn
            while keepDrawing:
                
                for player in self.playerList: 

                    # set card coordinates per player hand location is...
                    if player.getTurnPlayer and not didTurnPlayerDraw:  # If player is turnPlayer draw!
                        oCard = self.oDeck.getCard() # take one card from the top of the deck
                        player.setHand(oCard) # Set card in oPlayer's hand

                        # Set card coordinates for oPlayer1
                        if player.getPlayerId() == 0: 
                            cardLocX = self.player1CardXPositionList.pop(0) # Add x-coordinates
                            oCard.setLoc(cardLocX, Game.PLAYER1_HAND_CARDS_BOTTOM) # Add coordinates
                            oCard.reveal() # show player card running the software
                            didTurnPlayerDraw = True

                        # Set card coordinates for oPlayer2 -------------CHECK HERE
                        else: 
                            """PLACE HOLDERS ARE EMPTY CARDS? with a back image?"""
                            cardLocX = self.player2CardXPositionList.pop(0)
                            oCard.setLoc(cardLocX, Game.PLAYER2_HAND_CARDS_TOP)
                            didTurnPlayerDraw = True
                    
                    elif didTurnPlayerDraw: # player draw if turnPlayer drew first!
                        oCard = self.oDeck.getCard() # take one card from the top of the deck
                        player.setHand(oCard) # Set card in oPlayer's hand

                        # Set card coordinates for oPlayer1
                        if player.getPlayerId() == 0: 
                            cardLocX = self.player1CardXPositionList.pop(0) # Add x-coordinates
                            oCard.setLoc(cardLocX, Game.PLAYER1_HAND_CARDS_BOTTOM) # Add coordinates
                            oCard.reveal() # show player card running the software
                            keepDrawing = False # Exit while loop

                        # Set card coordinates for oPlayer2 -------------CHECK HERE
                        else: 
                            """PLACE HOLDERS ARE EMPTY CARDS? with a back image?"""
                            cardLocX = self.player2CardXPositionList.pop(0)
                            oCard.setLoc(cardLocX, Game.PLAYER2_HAND_CARDS_TOP)
                            keepDrawing = False # Exit while loop

        # Start game
        self._briscaGame()

    def playersDrawACard(self):
        """Players draw a card."""
        # Can you draw a card?
        # yes?
        # no?
        pass

    def selectCard(self):
        """
        Players can select to enter a trick session or if applicable, a trump swap
        """
        pass

    def trumpHandSwap(self):
        """Swap one card in the player's hand for the trump card."""
        pass

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

    def _briscaGame(self):
        """The logic of the game loop"""
        pass

"""
Todo list: 
1) Check local variables that are named 'oPlayer' and change them to 'player'.
2) Re-check writen methods one more time for logoc consistency.
3) Work on the players drawn a card method
4) Check to see if players draw a card method can be used across the class to sub stitudes other code. 
5) Create place holders for client's opponent. 
6) Figure the other empty methods out.
7) Whatever needs to happen next lol!
"""