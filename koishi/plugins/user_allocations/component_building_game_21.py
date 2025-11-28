__all__ = ()

from hata import ButtonStyle, USERS, create_button, create_row, create_section, create_separator, create_text_display

from ..user_balance import ALLOCATION_FEATURE_ID_GAME_21

from .custom_ids import (
    USER_ALLOCATIONS_CUSTOM_ID_DETAILS_BUILDER, USER_ALLOCATION_CUSTOM_ID_LINK_DISABLED,
    USER_ALLOCATIONS_CUSTOM_ID_VIEW_PAGE_BUILDER,
)


def _produce_game_21_short_description(amount):
    """
    Produces game 21 short description.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    amount : `int`
        The allocated amount.
    
    Yields
    ------
    part : `str`
    """
    yield '`/21` allocating '
    yield str(amount)


def _produce_game_21_title(amount):
    """
    Produces game 21 title.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    amount : `int`
        The allocated amount.
    
    Yields
    ------
    part : `str`
    """
    yield '# '
    yield from _produce_game_21_short_description(amount)


def _produce_game_21_long_description(session, guild_id):
    """
    Produces game 21 log description
    
    This function is an iterable generator.
    
    Parameters
    ----------
    session : ``Game21Session``
        The game's session.
    
    guild_id : `int`
        The local guild's identifier.
    
    Yields
    ------
    part : `str`
    """
    yield '**Participants:**'
    user_ids = session.user_ids
    if (user_ids is None):
        yield ' *none*'
    
    else:
        for user_id in user_ids:
            yield '\n- '
            
            try:
                user = USERS[user_id]
            except KeyError:
                user_name = 'unknown'
            else:
                user_name = user.name_at(guild_id)
            
            yield user_name


def build_game_21_entry_component(user_id, page_index, session_id, amount):
    """
    Builds game 21 entry components.
    
    Parameters
    ----------
    user_id : `int`
        The invoking user's identifier.
    
    page_index : `int`
        Page index to redirect to.
    
    session_id : `int`
        The session's identifier.
    
    amount : `int`
        The allocated amount.
    
    Returns
    -------
    component : ``Component``
    """
    return create_section(
        create_text_display(
            ''.join([*_produce_game_21_short_description(amount)])
        ),
        thumbnail = create_button(
            'Details',
            custom_id = USER_ALLOCATIONS_CUSTOM_ID_DETAILS_BUILDER(
                user_id, page_index, ALLOCATION_FEATURE_ID_GAME_21, session_id
            ),
        ),
    )


def build_game_21_detailed_components(user_id, page_index, session_id, amount, session, guild_id):
    """
    Builds game 21 detailed components.
    
    Parameters
    ----------
    user_id : `int`
        The invoking user's identifier.
    
    page_index : `int`
        Page index to redirect to.
    
    session_id : `int`
        The session's identifier.
    
    amount : `int`
        The allocated amount.
    
    session : ``None | Game21Session``
        The game's session.
    
    guild_id : `int`
        The local guild's identifier.
    
    Returns
    -------
    components : ``list<Component>``
    """
    components = []
    
    # Add title
    components.append(create_text_display(
        ''.join([*_produce_game_21_title(amount)])
    ))
    
    if (session is not None):
        # Add description
        components.append(create_text_display(
            ''.join(_produce_game_21_long_description(session, guild_id))
        ))
        components.append(create_separator())
    
    # Add control
    message = None if (session is None) else session.message
    link_component = create_button(
        'Get me there',
        custom_id = (USER_ALLOCATION_CUSTOM_ID_LINK_DISABLED if (message is None) else None),
        enabled = (message is not None),
        url = (None if (message is None) else message.url),
        style = (ButtonStyle.gray if (message is None) else ButtonStyle.link),
    )
    
    components.append(create_row(
        create_button(
            'Back to allocations',
            custom_id = USER_ALLOCATIONS_CUSTOM_ID_VIEW_PAGE_BUILDER(user_id, page_index),
        ),
        link_component,
    ))
    
    return components
