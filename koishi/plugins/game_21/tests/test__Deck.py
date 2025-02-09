import vampytest

from ..deck import Deck


def _assert_fields_set(deck):
    """
    Tests whether every field of the given deck is set.
    
    Parameters
    ----------
    deck : ``deck``
        The deck to test.
    """
    vampytest.assert_instance(deck, Deck)
    vampytest.assert_instance(deck.all_pulled, list)


def test__Deck__new():
    """
    Tests whether ``Deck.__new__`` works as intended.
    """
    deck = Deck()
    _assert_fields_set(deck)


def test__Deck__pull_card():
    """
    Tests whether ``Deck.pull_card`` works as intended.
    """
    deck = Deck()
    
    # pull 1 card
    card_0 = deck.pull_card()
    
    vampytest.assert_instance(card_0, int)
    vampytest.assert_in(card_0, deck.all_pulled)
    
    # pull another card
    card_1 = deck.pull_card()
    
    vampytest.assert_instance(card_1, int)
    vampytest.assert_in(card_1, deck.all_pulled)
    
    # card should not be same even if random is same.
    vampytest.assert_ne(card_0, card_1)


def test__Deck__repr():
    """
    Tests whether ``Deck.__repr__`` works as intended.
    """
    deck = Deck()
    
    deck.pull_card()
    deck.pull_card()
    
    output = repr(deck)
    vampytest.assert_instance(output, str)


def test__Deck__push_card__pulled():
    """
    Tests whether ``Deck.push_card`` works as intended.
    
    Case: card pulled.
    """
    deck = Deck()
    
    card_0 = deck.pull_card()
    card_1 = deck.pull_card()
    
    output = deck.push_card(card_0)
    vampytest.assert_instance(output, bool)
    vampytest.assert_eq(output, True)
    
    vampytest.assert_eq(deck.all_pulled, [card_1])


def test__Deck__push_card__invalid():
    """
    Tests whether ``Deck.push_card`` works as intended.
    
    Case: invalid card.
    """
    deck = Deck()
    
    card_0 = -2
    card_1 = deck.pull_card()
    
    output = deck.push_card(card_0)
    vampytest.assert_instance(output, bool)
    vampytest.assert_eq(output, False)
    
    vampytest.assert_eq(deck.all_pulled, [card_1])
