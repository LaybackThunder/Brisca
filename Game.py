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
    CARD_BACK_IMAGE = Card()
    
    def __init__(self, window, playerList):
        """Initisialize attributes."""
        self.window = window
        self.oDeck = Deck(self.window)
        self.trumpCard = None
        self.dealerPot = []
        self.oPlayer = Player()
        self.playerList = playerList # LIST is given by client
        # When to create player and iterate to give it a player id???????????????????
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

        # Game decides who goes first at random before game starts
        self.reset()
        
    def draw(self): # draw image to screen.
        """Tell each card to draw an image of itself"""
        for oCard in self.cardList:
            oCard.draw()

        self.potScoreText.draw()
        self.messageText.draw()

    def setDealerPot(self, playersAndCards):
        """
        Appends object Cards to dealerPot list after a trick tie.
        Player obj is not appeneded back.
        """
        potCards = []

        for i in range(len(playersAndCards.copy())):
            dict = playersAndCards.pop(0)
            card = dict.pop('card')
            potCards.append(card)
        for oCard in potCards:
            self.dealerPot.append(oCard)
    
    def getDealerPot(self):
        """This method is used by setPot Transfer """
        return self.dealerPot
    
    def dealerPotTransfer(self, player=None):
        """The dealerPot gives all it's cards to the player's pot or to the deck."""

        if player != None: # Give cards to player
            dealerPot = self.getDealerPot.copy() # Itterate using a copy of the list
            for card in dealerPot:
                card = self.dealerPot.pop(0) # Remove items using real list
                player.setPot(card)

        else: # Return cards to deck
            dealerPot = self.getDealerPot.copy()
            for card in dealerPot:
                card = self.dealerPot.pop(0)
                self.oDeck.returnCardToDeck(card)

    def showTrumpCard(self, oCard):
        oCard.reveal()

    def setTrump(self, oCard):
        self.trumpCard = oCard

    def highestCardWins(self):
        """
        When players enter the game room the dealer gives each player a card.
        Player with the highest card value wins to be turnPlayer=True.
        Player's var turnPlayer is False by defult.
        """
        print('highestCardWin - Enter method')
        
        tie = False
    
        if not tie: 
            # Place holder to identify to whom the card belongs too
            playersAndCards = []

            # Each player draws one card each
            for playerIndex in range(len(self.playerList.copy())): # Pick player index
                self.playerDrawsACard(playerIndex)
                playersAndCards.append(
                    {'player': self.playerList[index], 'card': self.playerList[index].getHand()}
                    )

            # Players compare the card's trickValue and decide who will be turn player   
            tie = self.compareCards(playersAndCards) # Returns and checks for tie

            # Remove the 1st card from each player's hand and pass back to deck
            for index in range(len(self.playerList.copy())):
                oCard = self.playerList[index].removeCardFromHand(0) # Remove card from player's hand
                self.oDeck.returnCardToDeck(oCard) # Card returns to deck

        while tie:
            # Place holder to identify to whom the card belongs too
            playersAndCards = []

            # Each player draws one card each
            for playerIndex in range(len(self.playerList.copy())): # Pick player index
                self.playerDrawsACard(playerIndex)
                playersAndCards.append(
                    {'player': self.playerList[index], 'card': self.playerList[index].getHand()}
                    )

            # Players compare the card's trickValue and decide who will be turn player   
            tie = self.compareCards(playersAndCards) # Returns and checks for tie

            # Remove the 1st card from each player's hand and pass back to deck
            for index in range(len(self.playerList.copy())):
                oCard = self.playerList[index].removeCardFromHand(0) # Remove card from player's hand
                self.oDeck.returnCardToDeck(oCard) # Card returns to deck

            # If true shuffle deck after cards return deck after
            if tie:
                self.oDeck.shuffle() 

        print('highestCardWin - exit method')

    def reset(self):
        """
        This method is called when a new round starts. 
        Resets: deck, pots, points
        """
        # Reset every Player's pot points

        # Remove any cards in every player's pot and put it back int the deck
        for player in self.playerList:
            for card in range(len(player.getPot().copy())): # Number iteration
                  discard = player.removeCardFromPot(card) # Pop using the index
                  self.oDeck.returnCardToDeck(discard) # The resturned value is placed back in the deck

        # Remove any cards in dealer's pot and put it back int the deck
        if self.getDealerPot(): # is it true that there are cards?
            for card in range(len(self.getDealerPot.copy())): # Number iteration
                discard = player.removeCardFromPot(card) # Pop using the index
                self.oDeck.returnCardToDeck(discard) # The resturned value is placed back at the bottom of the deck

        # Decide which player becomes turnPlayer when game resets
        self.highestCardWins()

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
                
        # Deal cards to players before the game starts
        for i in range(Game.MAX_HAND): # Players draw up to 3 cards
                
            didTurnPlayerDraw = False # Tells none turn player to avoid drawing till turn player has drawn
            keepDrawing = True # Keep drawing till all players have drawn
            while keepDrawing:
                
                for i in range(len(self.playerList.copy())): 

                    # set card coordinates per player hand location is...
                    if self.playerList[i].getTurnPlayer and not didTurnPlayerDraw:  # If player is turnPlayer draw!
                        self.playerDrawsACard(i)
                        didTurnPlayerDraw = True
                    
                    elif didTurnPlayerDraw: # player draw if turnPlayer drew first!
                        self.playerDrawsACard(i)
                        keepDrawing = False # Exit while loop

                    # Set card coordinates for place holder 'player' ____LEFT OOOOFFFF_____
                    """PLACE HOLDERS ARE EMPTY CARDS with a back image"""
                    cardLocX = self.cardXPositionList.copy().pop(0)
                    Game.CARD_BACK_IMAGE.setLoc(cardLocX, Game.PLAYER2_HAND_CARDS_TOP)

        # Start game
        self._briscaGame()

    def playerDrawsACard(self, playerIndex):
        """Players draw a card and remembers card's posX."""
        # Player draws one card
        oCard = self.oDeck.getCard() # Take one card from the top of the deck
        self.playerList[playerIndex].setHand(oCard) # Set card in player's hand
        
        # Player remembers card's posX
        currentPlayerHand = self.playerList[playerIndex].getHand() # Get list
        cardIndex = len(currentPlayerHand) # How long is the list?
        cardLocX = self.cardXPositionList[cardIndex] # Get x-coordinates
        self.playerList[playerIndex].setHandPosX(cardLocX) # Set player's card's posX to the end of list

        # Tell card its posX and show it to client
        oCard.setLoc(cardLocX, Game.PLAYER1_HAND_CARDS_BOTTOM) # Add coordinates to player's card
        oCard.reveal() # Show client running the sofware their cards a.k.a. the player's card 
        
    def selectCard(self):
        """
        Players can select to enter a trick session or if applicable, a trump swap
        Returns the card. If players can't select a card from their hands, 
        let them draw a card from the deck and place it in their hand.
        """
        pass

    def trumpHandSwap(self):
        """Swap one card in the player's hand for the trump card."""
        pass

    def compareCards(self, playersAndCards):
            """
            Sets a turnPlayer by comparing the highest value card.
            Arrange player list; winner is first item on playerList.
            Returns True or False for tie.
            """
            # playersAndCards is a list nesing a dictionary with the player's iD and corresponding cards
            # E.g. playersAndCards = [{'player: oPlayer, 'card': oCard}]

            player1CardValue = playersAndCards[0]['card'].getTrickValue()
            player2CardValue = playersAndCards[1]['card'].getTrickValue()

            if player1CardValue > player2CardValue:
                print("-------You WIN!")
                playersAndCards[0]['player'].setTurnPlayer(True) # Player1 is turnPlayer, player 2 is false by defult
                self.playerList = [playersAndCards[0]['player'], playersAndCards[1]['player']] # Player arrangement decides who draws first
                tie = False
            
            elif player1CardValue < player2CardValue:
                print("-------You LOSE!")
                playersAndCards[1]['player'].setTurnPlayer(True) # Player1 is turnPlayer, player 2 is false by defult
                self.playerList = [playersAndCards[1]['player'], playersAndCards[0]['player']] # Player arrangement decides who draws first
                tie = False

            else: # If players end in a tie: cards return to deck
                print("Tie")
                tie = True

            return tie # Return the value of Tie

    def trickWinner(self, playersAndCards):
        """Give trick winner the pot cards."""

        # Place the cards in a list
        potCards = [playersAndCards[0]['card'], playersAndCards[1]['card']]
        # Add cards into winning player's pot
        for card in potCards.copy():
            card = potCards.pop(0)
            # The trick winner is rearranged in the player list as 1st item
            self.playerList[0].setPot(card)
        
        if self.dealerPot: # If there are cards in the dealer list, give them all to player1
                self.dealerPotTransfer(self.playerList[0]) # Player has all the dealer cards in their pot

    def trick(self, playersAndCards):
        """
        Players have chosen their cards for battle; now they fight for supremacy, but mostly points.
        If tie, cards are placed with the dealer pot; after a tie, which ever player wins the following trick
        obtains all the dealer pot cards, uuh nice!
        """
        # playersAndCards is a list nesing a dictionary with the players and their corresponding cards
        # E.g. playersAndCards = [{'player': oPlayer, 'card': oCard}]

        # Compare player's trump cards to the main trump card
        isPlayer1Trump = playersAndCards[0]['card'].getSuit() == self.trumpCard.getSuit()
        isPlayer2Trump = playersAndCards[1]['card'].getSuit() == self.trumpCard.getSuit()

        if isPlayer1Trump and isPlayer2Trump: # Both players have a trump card | No tie can HAPPEN!
            # Compares player's cards: the higest value card wins; turn player is selected and 
            self.compareCards(playersAndCards) # turn player is rearranged as 1st iteam in the playerList   

        elif isPlayer1Trump or isPlayer2Trump: # A player has a trump card | No tie can HAPPEN!
            if isPlayer1Trump:
                print("-------You win!")
                # Player1 is turnPlayer, player 2 is false by defult
                playersAndCards[0]['player'].setTurnPlayer(True) 
                # Player arrangement decides who draws first
                self.playerList = [playersAndCards[0]['player'], playersAndCards[1]['player']] 
            else:
                print("-------You Lose!")
                # Player2 is turnPlayer, player 1 is false by defult
                playersAndCards[1]['player'].setTurnPlayer(True) 
                # Player arrangement decides who draws first
                self.playerList = [playersAndCards[1]['player'], playersAndCards[0]['player']] 

        else: # No player has a trump card, a tie can happen using trickValues.
            tie = self.compareCards(playersAndCards)

            if tie: # Tie
                # Give dealer your pot cards till tie is resolved
                self.setDealerPot(playersAndCards) # Trick cards are in dealer's possetion 

                while tie:
                    playersAndCards = [] # Parameter var is empty
                    # Players select another card from their hands
                    for player in self.playerList:
                        card = self.selectCard(player) 
                        playersAndCards.append({'player': player, 'card': card})

                    # Players compare cards and decide who will be turn player   
                    tie = self.compareCards(playersAndCards) # Check for tie

                    if tie: # Give dealer your pot cards till tie is resolved
                        self.setDealerPot(playersAndCards)
                    
                    else: # Not tie
                        print('Tie is False insde the while loop!')

            else: # Not tie
                print('Not a tie out side the while loop.')
        
        # After one logic gate has a been checked the Winner gets the chicken dinner. 
        self.trickWinner(playersAndCards) 

    def _briscaGame(self):
        """The logic of the game loop"""
        pass

"""
Todo list: 
2) Re-check writen methods one more time for logoc consistency.
    *DID
    - Modified highestCardWins, creat compareCards method
    - Add comments in the reset() and arrange highestCardWins() in the reset method
    - Modify a lot of shit in the Game class between highestCardWins(), compareCards() and trick().
    - Clean trick() and fix logic
    - Check, fix and clean highestCardWin()
    - Check, fix and clean reset()
    - Add 'playerList' parameter to Game class init magic method. 
    - Add set and get HandPosX methods to Player class.
    - Write playerDrawsACard method in Game class. Work on the players drawn a card method

4) Check to see if players draw a card method can be used across the class to sub stitudes other code. 
5) Create place holders for client's opponent. 
6) Figure the other empty methods out.
7) If there is no deck, draw trump card.
8) Whatever needs to happen next lol!
"""