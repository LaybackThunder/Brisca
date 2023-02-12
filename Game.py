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
        
        # deal cards to players
        for oPlayer in self.playerList: # LEFT OFF ----> Check how cards are delt toplayers

            # take one card from deck
            oCard = self.oDeck.getCard()

            # set card coordinates per player hand location is...
            if oPlayer.getTurnPlayer:  # If player is turnPlayer do or die!
                oPlayer.setHand(oCard) # Set card in oPlayer's hand
                if oPlayer.getPlayerId() == 0: # Set card coordinates for oPlayer1
                    cardLocX = self.player1CardXPositionList.pop(0)
                    oCard.setLoc(cardLocX, Game.PLAYER1_HAND_CARDS_BOTTOM)
                    oCard.reveal() # show player card running the software
                else:                          # Set card coordinates for oPlayer2
                    cardLocX = self.player2CardXPositionList.pop(0)
                    oCard.setLoc(cardLocX, Game.PLAYER2_HAND_CARDS_TOP)
            else:                      # If player is not turnPlayer you be gug2go!
                oPlayer.setHand(oCard)
                if oPlayer.getPlayerId() == 0:
                    cardLocX = self.player1CardXPositionList.pop(0)
                    oCard.setLoc(cardLocX, Game.PLAYER1_HAND_CARDS_BOTTOM)
                    oCard.reveal() # show player card running the software
                else:
                    cardLocX = self.player2CardXPositionList.pop(0)
                    oCard.setLoc(cardLocX, Game.PLAYER2_HAND_CARDS_TOP)

    def highestCardWinds(self):
        """Player with the highest card value wins to be turnPlayer."""
        
        for oPlayer in self.playerList: # Players draw one card each
            oCard = self.oDeck.getCard() # player draws
            oPlayer.setHand(oCard) # player puts card in their hand

        # Players compare cards    
        if self.oPlayer1.hand[0].getTrickValue() > self.oPlayer2.hand[0].getTrickValue(): # If player 1 wins and set as turn player
                print("-------Player 1 wins")
                self.oPlayer1.setTurnPlayer(True) # Player1 is turnPlayer, player 2 is false by defult
                # Remove the 1st card from each player's hand
                for oPlayer in self.playerList:
                    oCard = oPlayer.removeCard(0) # Remove card from player's hand
                    oDeck.returnCardToDeck(oCard) # Card returns to deck
           
        elif oPlayer.hand[0].getTrickValue() < oPlayer2.hand[0].getTrickValue():  # if player 2 wins and set as turn player
                print("-------Player 2 wins")
                self.oPlayer2.setTurnPlayer(True) # Player2 is turnPlayer, player 1 is false by defult
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
                    tie = False # Exit loop
                    # Remove the 1st card from each player's hand
                    for oPlayer in self.playerList:
                        oCard = oPlayer.removeCard(0) # Remove card from player's hand
                        oDeck.returnCardToDeck(oCard) # Card returns to deck
           
                elif oPlayer.hand[0].getTrickValue() < oPlayer2.hand[0].getTrickValue():  # if player 2 wins and set as turn player
                    print("-------Player 2 wins")
                    self.oPlayer2.setTurnPlayer(True) # Player2 is turnPlayer, player 1 is false by defult
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