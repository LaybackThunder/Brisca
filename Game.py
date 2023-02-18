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
        self.oPlayer1 = Player(1) # Instantiate for testing
        self.oPlayer2 = Player(0) # Instantiate for testing
        self.playerList = [self.oPlayer1, self.oPlayer2] # Leave this list empty when test run good
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
        thisLeft = Game.CARDS_LEFT # Starting card to the left of the player's hand

        # Calculate the x positions of all cards, once 
        for i in range(Game.DISPLAY_STARTING_HANDS): # 3 cards
            self.cardXPositionList.append(thisLeft)
            thisLeft += Game.HAND_CARD_OFFSET # Space between cards in the player's hand
        # Both players can share X position
        self.player1CardXPositionList = self.cardXPositionList.copy()
        self.player2CardXPositionList = self.cardXPositionList.copy()
        
        # Game decides who goes first at random before game starts
        self.highestCardWins()
        
    def draw(self): # draw image to screen.
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
    
    def DealerPotTransfer(self, player=None): # Change the name to "DealerPotTransfer" or whatever lol
        """The dealerPot gives all it's cards to the player's pot or to the deck."""
        if player != None: # Give cards to player
            dealerPot = self.getDealerPot.copy() # Itterate using a copy of the list
            for card in dealerPot:
                card = self.dealerPot.pop(0) # Remove items using real list
                player.setPot(card)

        else: # Return cards to deck
            dealerPot = self.getDealerPot.copy() # Itterate using a copy of the list
            for card in dealerPot:
                card = self.dealerPot.pop(0) # Remove items using real list
                self.oDeck.returnCardToDeck(card)

    def showTrumpCard(self, oCard):
        oCard.reveal()

    def setTrump(self, oCard):
        self.trumpCard = oCard

    def compareCards(self, playerList):
        """
        Sets a turnPlayer by comparing the highest value card.
        Returns True or False for tie.
        """
        if playerList[0].hand[0].getTrickValue() > playerList[1].hand[0].getTrickValue():
            print("-------You WIN!")
            playerList[0].setTurnPlayer(True) # Player1 is turnPlayer, player 2 is false by defult
            self.playerList = [playerList[0], playerList[1]] # Player arrangement decides who draws first
            tie = False
        
        elif playerList[0].hand[0].getTrickValue() < playerList[1].hand[0].getTrickValue():
            print("-------You WIN!")
            playerList[1].setTurnPlayer(True) # Player1 is turnPlayer, player 2 is false by defult
            self.playerList = [playerList[1], playerList[0]] # Player arrangement decides who draws first
            tie = False

        else: # If players end in a tie: cards return to deck
            print("Tie")
            tie = True

        return tie # Return the value of Tie

    def highestCardWins(self):
        """
        When players enter the game room the dealer gives each player a card.
        Player with the highest card value wins to be turnPlayer=True.
        Player's var turnPlayer is set to False by defult.
        """
        tie = False
        
        if not tie: 
            # Add cards to player's hand
            for player in self.playerList: # Players draw one card each
                oCard = self.oDeck.getCard() # draw a card
                player.setHand(oCard) # player puts card in their hand

            # Players compare cards and decide who will be turn player   
            tie = self.compareCards(self.playerList) # Check for tie

            # Remove the 1st card from each player's hand
            for player in self.playerList:
                oCard = player.removeCardFromHand(0) # Remove card from player's hand
                self.oDeck.returnCardToDeck(oCard) # Card returns to deck

        while tie:
            # Add cards to player's hand
            for player in self.playerList: # Players draw one card each
                oCard = self.oDeck.getCard() # player draws
                player.setHand(oCard) # player puts card in their hand

            # Players compare cards and decide who will be turn player   
            tie = self.compareCards(self.playerList) # Check for tie

            # Remove the 1st card from each player's hand
            for player in self.playerList:
                oCard = player.removeCardFromHand(0) # Remove card from player's hand
                self.oDeck.returnCardToDeck(oCard) # Card returns to deck

            # If true shuffle deck after cards return deck after
            if tie:
                self.oDeck.shuffle() 

    def reset(self):
        """This method is called when a new round starts. 
        Resets and sets; deck, pots, points
        """
        # Reset every Player's pot points

        # Remove any cards in every player's pot and put it back int the deck
        for player in self.playerList:
            for card in range(len(player.getPot().copy())): # Number iteration
                  discard = player.removeCardFromPot(card) # Pop using the index
                  self.oDeck.returnCardToDeck(discard) # The resturned value is placed back in the deck

        # Remove any cards in dealer's pot
        if self.getDealerPot(): # is it true that there are cards?
            for card in range(len(self.getDealerPot.copy())): # Number iteration
                discard = player.removeCardFromPot(card) # Pop using the index
                self.oDeck.returnCardToDeck(discard) # The resturned value is placed back at the bottom of the deck

        self.cardShuffleSound.play() # play shuffle sound
        self.oDeck.shuffle() # shuffle new deck

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

        # Decide which player becomes turnPlayer
        self.highestCardWins()
                
        # Deal cards to players before the game starts
        for i in range(Game.MAX_HAND): # Players draw up to 3 cards
                
            didTurnPlayerDraw = False # Tells none turn player to avoid drawing till turn player has drawn
            keepDrawing = True # Keep drawing till all players have drawn
            while keepDrawing:
                
                for player in self.playerList: 

                    # set card coordinates per player hand location is...
                    if player.getTurnPlayer and not didTurnPlayerDraw:  # If player is turnPlayer draw!
                        oCard = self.oDeck.getCard() # take one card from the top of the deck
                        player.setHand(oCard) # Set card in player's hand

                        # Set card coordinates for oPlayer1
                        if player.getPlayerId() == 0: 
                            cardLocX = self.player1CardXPositionList.pop(0) # Add x-coordinates
                            oCard.setLoc(cardLocX, Game.PLAYER1_HAND_CARDS_BOTTOM) # Add coordinates
                            oCard.reveal() # show player card running the software
                            didTurnPlayerDraw = True

                        # Set card coordinates for oPlayer2
                        else: 
                            """PLACE HOLDERS ARE EMPTY CARDS? with a back image?"""
                            cardLocX = self.player2CardXPositionList.pop(0)
                            oCard.setLoc(cardLocX, Game.PLAYER2_HAND_CARDS_TOP)
                            didTurnPlayerDraw = True
                    
                    elif didTurnPlayerDraw: # player draw if turnPlayer drew first!
                        oCard = self.oDeck.getCard() # take one card from the top of the deck
                        player.setHand(oCard) # Set card in player's hand

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
                    self.DealerPotTransfer(self.oPlayer1) # Player1 has all the dealer cards in their pot
            
            elif playersAndCards[0].getTrickValue() < playersAndCards[1].getTrickValue():
                print("-------Player 2 wins")
                # Place the cards in a list
                potCards = [playersAndCards[0], playersAndCards[1]]
                # Add cards into player pot
                for card in potCards.copy():
                    card = potCards.pop(0)
                    self.oPlayer2.setPot(card)
                
                if self.dealerPot: # If there are cards in the dealer list, give them all to player2
                        self.DealerPotTransfer(self.oPlayer2) # Player2 has all the dealer cards in their pot         
            
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
                    self.DealerPotTransfer(self.oPlayer1)
            else:
                print("-------Player 2 wins")
                # Place the cards in a list
                potCards = [playersAndCards[0], playersAndCards[1]]
                # Add cards into player pot
                for card in potCards.copy():
                    card = potCards.pop(0)
                    self.oPlayer2.setPot(card)

                if self.dealerPot: # If there are cards in the dealer list, give them all to player2
                    self.DealerPotTransfer(self.oPlayer2)
        
        # Are there any cards left in the deck?

    def _briscaGame(self):
        """The logic of the game loop"""
        pass

"""
Todo list: 
2) Re-check writen methods one more time for logoc consistency.
    - Modified highestCardWins, creat compareCards method
    - Add comments in the reset() and arrange highestCardWins() in the reset method
    - Left OFF --> Cehck Reset method
3) Work on the players drawn a card method
4) Check to see if players draw a card method can be used across the class to sub stitudes other code. 
5) Create place holders for client's opponent. 
6) Figure the other empty methods out.
7) Whatever needs to happen next lol!
"""