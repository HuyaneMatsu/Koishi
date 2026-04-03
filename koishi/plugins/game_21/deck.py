__all__ = ()

from random import random

from scarletio import RichAttributeErrorBaseType

from .constants import DECK_SIZE


class Deck(RichAttributeErrorBaseType):
    """
    Represents a deck.
    
    Attributes
    ----------
    all_pulled : `list<int>`
        A list representing the pulled cards.
    """
    __slots__ = ('all_pulled',)
    
    def __new__(cls):
        """
        Creates a new deck instance.
        """
        self = object.__new__(cls)
        self.all_pulled = []
        return self
    
    
    def __repr__(self):
        repr_parts = ['<', type(self).__name__]
        
        repr_parts.append(' all_pulled = ')
        repr_parts.append(repr(self.all_pulled))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
            
    
    def pull_card(self):
        """
        Pulls a card from the deck.
        
        Returns
        -------
        card : `int`
        """
        all_pulled = self.all_pulled
        card = int((DECK_SIZE - len(all_pulled)) * random())
        for pulled in all_pulled:
            if pulled > card:
                break
            
            card += 1
            continue
        
        all_pulled.append(card)
        all_pulled.sort()
        
        return card
    
    
    def push_card(self, card):
        """
        Pushes a card into the deck.
        
        Parameters
        ----------
        card : `int`
            The card to push.
        
        Returns
        -------
        success : `bool`
        """
        try:
            self.all_pulled.remove(card)
        except ValueError:
            return False
        
        return True
