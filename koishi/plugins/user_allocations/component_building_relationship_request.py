__all__ = ()

from config import MARISA_MODE

from hata import (
    ButtonStyle, create_button, create_row, create_section, create_separator, create_text_display
)

from ..user_balance import ALLOCATION_FEATURE_ID_RELATIONSHIP_REQUEST

from .custom_ids import (
    USER_ALLOCATIONS_CUSTOM_ID_DETAILS_BUILDER, USER_ALLOCATION_CUSTOM_ID_LINK_DISABLED,
    USER_ALLOCATIONS_CUSTOM_ID_VIEW_PAGE_BUILDER,
)


try:
    from ..relationships_core import (
        CUSTOM_ID_RELATIONSHIPS_REQUEST_DETAILS_BUILDER, get_relationship_request_type_concept
    )
except ImportError:
    if not MARISA_MODE:
        raise
    
    CUSTOM_ID_RELATIONSHIPS_REQUEST_DETAILS_BUILDER = None
    get_relationship_request_type_concept = lambda relationship_type, capitalised : 'Pudding'


def _produce_relationship_request_short_description(amount):
    """
    Produces relationship request short description.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    amount : `int`
        The allocated amount.
    
    Yields
    ------
    part : `str`
    """
    yield '`/relationships propose` allocating '
    yield str(amount)


def _produce_relationship_request_title(amount):
    """
    Produces relationship request title.
    
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
    yield from _produce_relationship_request_short_description(amount)


def _produce_relationship_request_long_description(session, target_user, guild_id):
    """
    Produces relationship request long description
    
    This function is an iterable generator.
    
    Parameters
    ----------
    session : ``RelationshipRequest``
        The allocation's session.
    
    guild_id : `int`
        The local guild's identifier.
    
    Yields
    ------
    part : `str`
    """
    yield get_relationship_request_type_concept(session.relationship_type, True)
    yield ' towards '
    yield target_user.name_at(guild_id)
    yield '.'


def build_relationship_request_entry_component(user_id, page_index, session_id, amount):
    """
    Builds relationship request item components.
    
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
            ''.join([*_produce_relationship_request_short_description(amount)])
        ),
        thumbnail = create_button(
            'Details',
            custom_id = USER_ALLOCATIONS_CUSTOM_ID_DETAILS_BUILDER(
                user_id, page_index, ALLOCATION_FEATURE_ID_RELATIONSHIP_REQUEST, session_id
            ),
        ),
    )


def build_relationship_request_detailed_components(user_id, page_index, session_id, amount, session, extra, guild_id):
    """
    Builds relationship request detailed components.
    
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
    
    session : ``None | RelationshipRequest``
        The game's session.
    
    extra : ``None | (ClientUserBase, )``
        Additionally requested fields.
    
    guild_id : `int`
        The local guild's identifier.
    
    Returns
    -------
    components : ``list<Component>``
    """
    components = []
    
    # Add title
    
    components.append(create_text_display(
        ''.join([*_produce_relationship_request_title(amount)])
    ))
    
    # Add description
    
    if (session is not None) and (extra is not None):
        components.append(create_text_display(
            ''.join(_produce_relationship_request_long_description(session, extra[0], guild_id))
        ))
    
    components.append(create_separator())
    
    # Add control
    
    while True:
        if (session is not None) and (CUSTOM_ID_RELATIONSHIPS_REQUEST_DETAILS_BUILDER is not None):
            custom_id = CUSTOM_ID_RELATIONSHIPS_REQUEST_DETAILS_BUILDER(user_id, True, 0, session.entry_id)
            enabled = True
            style = ButtonStyle.blue
            break
        
        custom_id = USER_ALLOCATION_CUSTOM_ID_LINK_DISABLED
        enabled = False
        style = ButtonStyle.gray
        break
    
    link_component = create_button(
        'Get me there',
        custom_id = custom_id,
        enabled = enabled,
        style = style,
    )
    
    components.append(create_row(
        create_button(
            'Back to allocations',
            custom_id = USER_ALLOCATIONS_CUSTOM_ID_VIEW_PAGE_BUILDER(user_id, page_index),
        ),
        link_component,
    ))
    
    return components
