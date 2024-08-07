import vampytest

from ..constants import ACE_INDEX
from ..deck import Deck
from ..hand import Hand


def _assert_fields_set(hand):
    """
    Asserts whether the hand has all of its attributes set.
    
    Parameters
    ----------
    hand : ``Hand``
        The hand to test.
    """
    vampytest.assert_instance(hand, Hand)
    vampytest.assert_instance(hand.ace, int)
    vampytest.assert_instance(hand.cards, list)
    vampytest.assert_instance(hand.total, int)


def test__Hand__new():
    """
    Tests whether ``Hand.__new__`` works as intended.
    """
    hand = Hand()
    _assert_fields_set(hand)


def test__Hand__repr():
    """
    Tests whether ``Hand.__repr__`` works as intended.
    """
    hand = Hand()
    output = repr(hand)
    vampytest.assert_instance(output, str)


def test__Hand__auto_pull_starting_cards():
    """
    Tests whether ``Hand.auto_pull_starting_cards`` works as intended.
    """
    hand = Hand()
    deck = Deck()
    
    hand.auto_pull_starting_cards(deck)
    
    vampytest.assert_true(len(hand.cards) >= 2)
    vampytest.assert_true(hand.total > 10)
    
    vampytest.assert_eq({*hand.cards}, {*deck.all_pulled})


def test__Hand__auto_finish():
    """
    Tests whether ``Hand.auto_finish`` works as intended.
    """
    hand = Hand()
    deck = Deck()
    
    hand.auto_finish(deck)
    
    vampytest.assert_true(len(hand.cards) >= 2)
    vampytest.assert_true(hand.total > 15)
    
    vampytest.assert_eq({*hand.cards}, {*deck.all_pulled})


def test__Hand__pull_card__not_finished():
    """
    Tests whether ``Hand.pull_card`` works as intended.
    
    Case: Not finished.
    """
    hand = Hand()
    deck = Deck()
    
    hand.pull_card(deck)
    
    vampytest.assert_true(len(hand.cards) == 1)
    vampytest.assert_true(hand.total > 1)
    
    vampytest.assert_eq({*hand.cards}, {*deck.all_pulled})


def test__Hand__pull_card__finished():
    """
    Tests whether ``Hand.pull_card`` works as intended.
    
    Case: finished.
    """
    hand = Hand()
    deck = Deck()
    
    hand.auto_finish(deck)
    hand.auto_pull_starting_cards(deck)
    
    vampytest.assert_true(len(hand.cards) > 1)
    vampytest.assert_true(hand.total > 1)
    
    vampytest.assert_eq({*hand.cards}, {*deck.all_pulled})


def test__Hand__should_auto_pull__finished():
    """
    Tests whether ``Hand.should_auto_pull`` works as intended.
    
    Case: finished.
    """
    hand = Hand()
    deck = Deck()
    
    hand.auto_finish(deck)
    hand.auto_pull_starting_cards(deck)
    
    vampytest.assert_true(len(hand.cards) > 1)
    vampytest.assert_true(hand.total > 1)
    
    vampytest.assert_eq({*hand.cards}, {*deck.all_pulled})


def _iter_options__is_finished():
    # should auto pull
    yield (8, ), False
    yield (ACE_INDEX, ), False
    yield (6, 0), False
    yield (6, 1), False
    yield (ACE_INDEX, 0), False
    yield (3, 2), False
    yield (3, 2, 0), False
    yield (2, 2, 0), False
    yield (2, 2, 1), False
    
    # should pull cases
    yield (8, 3), False
    yield (8, 4), False
    yield (8, 5), False
    yield (8, 6), False
    yield (ACE_INDEX, 3), False
    yield (ACE_INDEX, 4), False
    yield (ACE_INDEX, 5), False
    
    # finished cases
    yield (8, 2, 0), False
    yield (8, 8), False
    yield (8, 7, 0), True
    yield (8, 8, ACE_INDEX), True
    yield (8, 7, 0), True
    yield (8, 8, 0), True


@vampytest._(vampytest.call_from(_iter_options__is_finished()).returning_last())
def test__Hand__is_finished(cards):
    """
    Tests whether ``Hand.is_finished`` works as intended.
    
    Parameters
    ----------
    cards : `tuple<int>`
        The cards to pull.
    
    Returns
    -------
    output : `bool`
    """
    hand = Hand()
    
    for card in cards:
        hand.add_card(card)
    
    output = hand.is_finished()
    vampytest.assert_instance(output, bool)
    return output


def _iter_options__should_pull():
    # should auto pull
    yield (8, ), True
    yield (ACE_INDEX, ), True
    yield (6, 0), True
    yield (6, 1), True
    yield (ACE_INDEX, 0), True
    yield (3, 2), True
    yield (3, 2, 0), True
    yield (2, 2, 0), True
    yield (2, 2, 1), True
    
    # should pull cases
    yield (8, 3), True
    yield (8, 4), False
    yield (8, 5), False
    yield (8, 6), False
    yield (ACE_INDEX, 3), True
    yield (ACE_INDEX, 4), True
    yield (ACE_INDEX, 5), False
    
    # finished cases
    yield (8, 6, 0), False
    yield (8, 8), False
    yield (8, 7, 0), False
    yield (8, 8, ACE_INDEX), False
    yield (8, 7, 0), False
    yield (8, 8, 0), False


@vampytest._(vampytest.call_from(_iter_options__should_pull()).returning_last())
def test__Hand__should_pull(cards):
    """
    Tests whether ``Hand.should_pull`` works as intended.
    
    Parameters
    ----------
    cards : `tuple<int>`
        The cards to pull.
    
    Returns
    -------
    output : `bool`
    """
    hand = Hand()
    
    for card in cards:
        hand.add_card(card)
    
    output = hand.should_pull()
    vampytest.assert_instance(output, bool)
    return output


def _iter_options__should_auto_pull():
    # should auto pull
    yield (8, ), True
    yield (ACE_INDEX, ), True
    yield (6, 0), True
    yield (6, 1), False
    yield (ACE_INDEX, 0), False
    yield (3, 2), True
    yield (3, 2, 0), False
    yield (2, 2, 0), True
    yield (2, 2, 1), False
    
    # should pull cases
    yield (8, 3), False
    yield (8, 4), False
    yield (8, 5), False
    yield (8, 6), False
    yield (ACE_INDEX, 3), False
    yield (ACE_INDEX, 4), False
    yield (ACE_INDEX, 5), False
    
    # finished cases
    yield (8, 6, 0), False
    yield (8, 8), False
    yield (8, 7, 0), False
    yield (8, 8, ACE_INDEX), False
    yield (8, 7, 0), False
    yield (8, 8, 0), False


@vampytest._(vampytest.call_from(_iter_options__should_auto_pull()).returning_last())
def test__Hand__should_auto_pull(cards):
    """
    Tests whether ``Hand.should_auto_pull`` works as intended.
    
    Parameters
    ----------
    cards : `tuple<int>`
        The cards to pull.
    
    Returns
    -------
    output : `bool`
    """
    hand = Hand()
    
    for card in cards:
        hand.add_card(card)
    
    output = hand.should_auto_pull()
    vampytest.assert_instance(output, bool)
    return output


def _iter_options__add_card():
    yield (0,), (0, 2)
    yield (1,), (0, 3)
    yield (2,), (0, 4)
    yield (3,), (0, 5)
    yield (4,), (0, 6)
    yield (5,), (0, 7)
    yield (6,), (0, 8)
    yield (7,), (0, 9)
    yield (8,), (0, 10)
    yield (9,), (0, 10)
    yield (10,), (0, 10)
    yield (11,), (0, 10)
    yield (ACE_INDEX,), (1, 11)
    yield (ACE_INDEX, 8), (1, 21)
    yield (ACE_INDEX, 8, 7), (0, 20)
    yield (ACE_INDEX, 8, 8), (0, 21)


@vampytest._(vampytest.call_from(_iter_options__add_card()).returning_last())
def test__Hand__add_card(cards):
    """
    Tests whether ``Hand.add_card`` works as intended.
    
    Parameters
    ----------
    cards : `tuple<int>`
        The cards to pull.
    
    Returns
    -------
    output : `(int, int)`
    """
    hand = Hand()
    
    for card in cards:
        hand.add_card(card)
    
    return hand.ace, hand.total
