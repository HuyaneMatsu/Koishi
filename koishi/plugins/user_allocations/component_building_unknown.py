__all__ = ()

from hata import create_button, create_row, create_section, create_separator, create_text_display

from ..user_balance import ALLOCATION_FEATURE_ID_NONE

from .custom_ids import (
    USER_ALLOCATIONS_CUSTOM_ID_DETAILS_BUILDER, USER_ALLOCATIONS_CUSTOM_ID_VIEW_PAGE_BUILDER,
)



def _produce_unknown_short_description(amount):
    """
    Produces unknown short description.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    amount : `int`
        The allocated amount.
    
    Yields
    ------
    part : `str`
    """
    yield '`unknown` allocating '
    yield str(amount)


def _produce_unknown_title(amount):
    """
    Produces unknown title.
    
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
    yield from _produce_unknown_short_description(amount)


def build_unknown_entry_component(user_id, page_index, session_id, amount):
    """
    Builds unknown entry components.
    
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
            ''.join([*_produce_unknown_short_description(amount)])
        ),
        thumbnail = create_button(
            'Details',
            custom_id = USER_ALLOCATIONS_CUSTOM_ID_DETAILS_BUILDER(
                user_id, page_index, ALLOCATION_FEATURE_ID_NONE, session_id,
            ),
            enabled = False,
        ),
    )


def build_unknown_detailed_components(user_id, page_index, session_id, amount, session, guild_id):
    """
    Builds unknown detailed components.
    
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
    
    session : `NoneType`
        The session.
    
    guild_id : `int`
        The local guild's identifier.
    
    Returns
    -------
    components : ``list<Component>``
    """
    components = []
    
    # Add title
    components.append(create_text_display(
        ''.join([*_produce_unknown_title(amount)])
    ))
    components.append(create_separator())
    
    # Add control
    components.append(create_row(
        create_button(
            'Back to allocations',
            custom_id = USER_ALLOCATIONS_CUSTOM_ID_VIEW_PAGE_BUILDER(user_id, page_index),
        ),
    ))
    
    return components
