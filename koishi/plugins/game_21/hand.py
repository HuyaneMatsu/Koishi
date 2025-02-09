__all__ = ()


from scarletio import RichAttributeErrorBaseType

from .constants import ACE_INDEX, CARD_NUMBERS


class Hand(RichAttributeErrorBaseType):
    """
    Represents a hand.
    
    Attributes
    ----------
    ace : `int`
        The amount of aces that are counted as `11`.
    cards : `list<int>`
        The pulled cards.
    total : `int`
        Total weight.
    """
    __slots__ = ('ace', 'cards', 'total')
    
    def __new__(cls):
        """
        Creates a new hand.
        """
        self = object.__new__(cls)
        self.ace = 0
        self.cards = []
        self.total = 0
        return self
    
    
    def __repr__(self):
        repr_parts = ['<', type(self).__name__]
        
        # ace
        repr_parts.append(' ace = ')
        repr_parts.append(repr(self.ace))
        
        # total
        repr_parts.append(', total = ')
        repr_parts.append(repr(self.total))
        
        # cards
        repr_parts.append(', cards = ')
        repr_parts.append(repr(self.cards))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def should_auto_pull(self):
        """
        Returns whether the hand should auto pull from the deck.
        
        Returns
        -------
        should_auto_pull : `bool`
        """
        return self.total <= 10 or len(self.cards) < 2
    
    
    def auto_pull_starting_cards(self, deck):
        """
        Auto pulls starting cards. Stops after 2 cards or if we have over 10 weight.
        
        Parameters
        ----------
        deck : ``Deck``
            Deck to pull from.
        """
        while self.should_auto_pull():
            self.pull_card(deck)
    
    
    def should_pull(self):
        """
        Returns whether the hand should pull from the deck.
        
        Returns
        -------
        should_pull : `bool`
        """
        return self.total <= (17 if self.ace else 15)
    
    
    def auto_finish(self, deck):
        """
        Auto finishes the pulling. Keeps pulling till statistically we should not pull anymore.
        
        Parameters
        ----------
        deck : ``Deck``
            Deck to pull from.
        """
        while self.should_pull():
            self.pull_card(deck)
    
    
    def is_finished(self):
        """
        Returns whether pulling is not any option anymore.
        """
        return self.total >= 21
    
    
    def pull_card(self, deck):
        """
        Pulls a card and returns whether the user is done pulling.
        
        Parameters
        ----------
        deck : ``Deck``
            Deck to pull from.
        """
        self.add_card(deck.pull_card())
    
    
    def add_card(self, card):
        """
        Adds a card to the deck.
        
        Parameters
        ----------
        card : `int`
            The card to add.
        """
        self.cards.append(card)
        
        total = self.total
        ace = self.ace
        
        number_index = card % len(CARD_NUMBERS)
        if number_index == ACE_INDEX:
            ace += 1
            card_weight = 11
        elif number_index > 7:
            card_weight = 10
        else:
            card_weight = number_index + 2
        
        total += card_weight
        
        while total > 21 and ace:
            total -= 10
            ace -= 1
            
        self.total = total
        self.ace = ace
    
    
    def restore(self, deck):
        """
        Restores the hand's cards to the deck.
        """
        self.ace = 0
        self.total = 0
        
        cards = self.cards
        while cards:
            deck.push_card(cards.pop())
