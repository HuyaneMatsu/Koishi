import vampytest
from hata import User

from ..deck import Deck
from ..helpers import create_player_bot
from ..player import Player


def test__create_player_bot__no_difficulty():
    """
    Tests whether ``create_player_bot`` works as intended.
    
    Case: no difficulty.
    """
    client = User.precreate(202502040002)
    deck = Deck()
    difficulty = 0.0
    
    output = create_player_bot(client, deck, difficulty)
    vampytest.assert_instance(output, Player)
    vampytest.assert_eq(deck.all_pulled, sorted(output.hand.cards))


def test__create_player_bot__max_difficulty():
    """
    Tests whether ``create_player_bot`` works as intended.
    
    Case: max difficulty.
    """
    client = User.precreate(202502040003)
    deck = Deck()
    difficulty = 1.0
    
    output = create_player_bot(client, deck, difficulty)
    vampytest.assert_instance(output, Player)
    vampytest.assert_eq(deck.all_pulled, sorted(output.hand.cards))
