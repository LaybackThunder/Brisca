 def handleEvent(self, event):
        """Handles mouse and keyboard events when triggering card behavior."""
        for oPlayer in self.playerList:

            # Checks conditions to allow player to draw.
            if oPlayer.getLengthCardsOnHand() < Game.HAND_LIMIT:

                if self.trickList: 
                    # As long as one card is in the battle phase, draw is disabled
                    self.drawCardButton.disable()

                elif self.trumpCard != None: 
                    # As long as there is a trump card drawing is possible
                    self.drawCardButton.enable()
                    # Keeps player from triggering a card's behavior when clicked
                    oPlayer.disableAllCardsOnHand()  
                
                
                else: # When deck is empty and there is no trump card to draw, do below
                    self.drawCardButton.disable() # Desibale draw button
                    oPlayer.enableAllCardsOnHand() # Allows player to play (click) any cards on hand

                    # Card is selected ; disable all hand cards
                    oCardClick = oPlayer.getCardClick()    
                    if oCardClick: 
                        oPlayer.disableAllCardsOnHand()

# --------------------------------------------------------------------------------
                         
            else: # After HAND_LIMIT is reached draw button is disabled
                self.drawCardButton.disable() 

# --------------------------------------------------------------------------------