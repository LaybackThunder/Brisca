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
        self.oPlayer1 = Player()
        self.oPlayer2 = Player()
        self.playerList = [self.oPlayer1, self.oPlayer2]
        self.potScore = 0
        self.potScoreText = pygwidgets.DisplayText(window, (450, 164),
                                        f'Pot Score: {self.potScore}',
                                        fontSize=36, textColor=(255, 255, 255))
        
        self.messageText = pygwidgets.DisplayText(window, (50, 460),
                                        f'', width=900, justified='center'
                                        fontSize=36, textColor=(255, 255, 255))
        
        # Sounds go here
            # Card shuffle
            # Win sound
            # Lost sound
        
        # Calculating Players card positions within the player's hand
        self.cardXPositionList = []
        thisLeft = Game.CARDS_LEFT # Starting card to the left of hand

        # Calculate the x positions of all cards, once 
        for cardNum in range(Game.DISPLAY_STARTING_HANDS): # 3 cards
            self.cardXPositionList.append(thisLeft)
            thisLeft += Game.HAND_CARD_OFFSET 
        # Both players can share X position
        self.player1CardXPositionList = self.cardXPositionList.copy()
        self.player2CardXPositionList = self.cardXPositionList.copy()
        
        # Game decides who goes first at random before game starts
        self.highestCardWinds()
        
        
    
    def reset(self):
        """This method is called when a new round starts"""
        # play shuffle sound

        # shuffle deck
        oDeck.shuffle()

        # deal cards to players
        for oPlayer in self.playerList: # LEFT OFF ----> Check how cards are delt toplayers

            # take one card from deck
            oCard = self.oDeck.getCard()

            # set card coordinates where player is ...
            if oPlayer.getPlayerId == 1:
                oPlayer.setHand(oCard)
                if oPlayer == oPlayer1:
                    cardLocX = self.player1CardXPositionList.pop(0)
                    oCard.setLoc(cardLocX, Game.PLAYER1_HAND_CARDS_BOTTOM)
                else:
                    cardLocX = self.player2CardXPositionList.pop(0)
                    oCard.setLoc(cardLocX, Game.PLAYER2_HAND_CARDS_TOP)
            else:
                oPlayer.setHand(oCard)
                if oPlayer == oPlayer1:
                    cardLocX = self.player1CardXPositionList.pop(0)
                    oCard.setLoc(cardLocX, Game.PLAYER1_HAND_CARDS_BOTTOM)
                else:
                    cardLocX = self.player2CardXPositionList.pop(0)
                    oCard.setLoc(cardLocX, Game.PLAYER2_HAND_CARDS_TOP)

        
        # show player card
        # hide player2 cards
    
    def highestCardWinds(self):
        print()
        # highestCardWins method
            # Loop player list
                # player draws
            # Does players have a card?
                # False:
                    # Loop till all players have cards
                # True:
                    # Players compare cards
                        # If one is greater than the other
                            # Greater player is ID is set to 1

                        # else: its a tie, tie is set to True
                    # While tie
                        # Winning player plays first
                        # Break
                        # if tie:
                            # tie is set to false
                            # break 
                    # Cards are returned to deck
        print()
        self.reset()# start a round of the game
        pass