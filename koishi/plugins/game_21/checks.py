__all__ = ()

from hata.ext.slash import abort

from ...bot_utils.constants import IN_GAME_IDS

from .constants import BET_MIN, PLAYERS_MAX
from .rendering import (
    build_join_failed_embed_already_in_game, build_join_failed_embed_bet_too_low, build_join_failed_embed_max_players,
    build_join_failed_embed_not_enough_hearts
)


def check_in_game(event):
    """
    Checks whether the user is in a game.
    
    Parameters
    ----------
    event : ``InteractionEvent``
        The received interaction event.
    
    Raises
    ------
    InteractionAbortedError
    """
    if event.user_id in IN_GAME_IDS:
        abort(build_join_failed_embed_already_in_game())


def check_max_players(players):
    """
    Checks whether the amount of players is out of the roof.
    
    Parameters
    ----------
    players : `list<Player>`
        A game's players.
    
    Raises
    ------
    InteractionAbortedError
    """
    if len(players) >= PLAYERS_MAX:
        abort(build_join_failed_embed_max_players())


def check_bet_too_low(amount):
    """
    Checks whether the user bet enough love.
    
    Raises
    ------
    InteractionAbortedError
    """
    if amount < BET_MIN:
        abort(build_join_failed_embed_bet_too_low())


def check_has_enough_love(expected_love, available_love, me):
    """
    Checks whether the user has enough love to bet.
    
    Parameters
    ----------
    expected_love : `int`
        The expected hearts to have.
    
    available_love : `int`
        The available hearts of a user.
    
    me : `bool`
        Whether the client is checking itself.
    
    Raises
    ------
    InteractionAbortedError
    """
    if expected_love > available_love:
        abort(build_join_failed_embed_not_enough_hearts(expected_love, available_love, me))
