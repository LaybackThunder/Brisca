# Brisca - pygame version
# Main program

# 1 - Import packages
import pygame
from pygame.locals import *
import sys
import pygwidgets
from Player import *
from Game import *

# 2 - Define constants
WINDOW_WIDTH = 1100
WINDOW_HEIGHT = 900
FRAMES_PER_SECOND = 30

# Brisca Deck Constants
SUIT_TUPLE = ('Swords', 'Coins', 'Cups', 'Clubs')
# Deck example: '2' is rank, value is list [pointsValue, trcikValue] of rank
BRISCA_DICT = {'2':[0, 2], '3':[0, 13], '4':[0, 4], '5':[0, 5],
                        '6':[0, 6], '7':[0, 7], 'Jack':[2, 10],
                        'Knight':[3, 11], 'King':[4, 12], 'Ace':[11, 14]}

# 3 - Initialize the world
pygame.init()
clock = pygame.time.Clock()
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

# 4 - Load assets: image(s), sounds,  etc.
background = pygwidgets.Image(window, (0, 0),
                                'images/background.jpg')

newGameButton = pygwidgets.TextButton(window, (880, 840),
                                    'New Game', width=100, height=45)

quitButton = pygwidgets.TextButton(window, (990, 840),
                                    'Quit', width=100, height=45)


# 5 - Initialize variables
oPlayer = Player(window)
oGame = Game(window, oPlayer, SUIT=SUIT_TUPLE, BRISCA_DICT=BRISCA_DICT)

# 6 - Loop forever 
while True:

    # 7 - Check for and handle events
    for event in pygame.event.get():
        # Quit Event
        if ((event.type == QUIT) or
            ((event.type == KEYDOWN) and (event.key == K_ESCAPE)) or
            (quitButton.handleEvent(event))):
            pygame.quit()
            sys.exit()
        
        # Check for new game
        if newGameButton.handleEvent(event):
            oPlayer = Player(window)
            oGame = Game(window, oPlayer, SUIT=SUIT_TUPLE, BRISCA_DICT=BRISCA_DICT)
        
        # Check events to play game
        oGame.handleEvent(event)

    # 8 - Do any "per frame" actions

    # 9 - Clear the window before drawing it again
    background.draw()

    # 10 - Draw the window elements
    # Draw remaining user interface components
    newGameButton.draw()
    quitButton.draw()
    # Draw Game elements
    oGame.draw()

    # 11 - Update the window
    pygame.display.update()

    # 12 - Slow things down a bit
    clock.tick(FRAMES_PER_SECOND)