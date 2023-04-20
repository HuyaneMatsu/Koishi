__all__ = ()

from .constants import (
    ARRAY_IDENTIFIER_EMPTY, CUSTOM_ID_MAP, GAME_STATE_DRAW, GAME_STATE_NONE, GAME_STATE_P1_WIN, GAME_STATE_P2_WIN,
    LINES
)


def check_event_user(user, event):
    """
    Checks whether the event's user is same as the defined one.
    
    Parameters
    ----------
    user : ``ClientUserBase``
        The user to check the event's against.
    event : ``InteractionEvent``
        The received interaction event.
    
    Returns
    -------
    users_match : `bool`
    """
    return event.user is user


def check_event_other_user(user, event):
    """
    Checks whether the event's user is different than the defined one.
    
    Parameters
    ----------
    user : ``ClientUserBase``
        The user to check the event's against.
    event : ``InteractionEvent``
        The received interaction event.
    
    Returns
    -------
    users_match : `bool`
    """
    return event.user is not user


def click(array, custom_id, identifier):
    """
    Marks the position represented by the given custom identifier as clicked by the player.
    
    Parameters
    ----------
    array : `list` of `int`
        Game array.
    custom_id : `str`
        The clicked component's custom id.
    identifier : `int`
        The player's identifier.
    
    Returns
    -------
    success : `bool`
    """
    try:
        index = CUSTOM_ID_MAP[custom_id]
    except KeyError:
        return False
    
    element = array[index]
    if element == ARRAY_IDENTIFIER_EMPTY:
        array[index] = identifier
        return True
    
    return False


def get_game_state(array, identifier_player_1):
    """
    Gets the game's state for the given player.
    
    Parameters
    ----------
    array : `list` of `int`
        Game array.
    identifier_player_1 : `int`
        Player one's identifier.
    
    Returns
    -------
    game_state : `int`
    """
    # Check same lines
    for index_1, index_2, index_3 in LINES:
        
        element = array[index_1]
        if element == ARRAY_IDENTIFIER_EMPTY:
            continue
        
        if element != array[index_2]:
            continue
        
        if element != array[index_3]:
            continue
        
        if element == identifier_player_1:
            return GAME_STATE_P1_WIN
        else:
            return GAME_STATE_P2_WIN
    
    # Check 3/2 occupied places
    for element in array:
        if element == ARRAY_IDENTIFIER_EMPTY:
            return GAME_STATE_NONE
    
    return GAME_STATE_DRAW
