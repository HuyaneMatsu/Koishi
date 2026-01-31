__all__ = ()

from config import MARISA_MODE


from datetime import datetime as DateTime, timezone as TimeZone

from dateutil.relativedelta import relativedelta as RelativeDelta
from hata import (
    ButtonStyle, create_button, create_row, create_section, create_separator, create_text_display, elapsed_time
)

from ..user_balance import ALLOCATION_FEATURE_ID_MARKET_PLACE

from .custom_ids import (
    USER_ALLOCATIONS_CUSTOM_ID_DETAILS_BUILDER, USER_ALLOCATION_CUSTOM_ID_LINK_DISABLED,
    USER_ALLOCATIONS_CUSTOM_ID_VIEW_PAGE_BUILDER,
)


# Use `get_item_nullable` instead of `get_item`, so we can patch it better.
try:
    from ..item_core import get_item_nullable, produce_weight
except ImportError:
    if not MARISA_MODE:
        raise
    
    get_item_nullable = lambda item_id : None
    
    def produce_weight(value):
        yield 'unknown kg'


try:
    from ..market_place_core import CUSTOM_ID_MARKET_PLACE_OFFER_BUILDER
except ImportError:
    if not MARISA_MODE:
        raise
    
    CUSTOM_ID_MARKET_PLACE_OFFER_BUILDER = None


def _produce_market_place_short_description(amount):
    """
    Produces market place short description.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    amount : `int`
        The allocated amount.
    
    Yields
    ------
    part : `str`
    """
    yield '`/market-place` allocating '
    yield str(amount)


def _produce_market_place_title(amount):
    """
    Produces market place title.
    
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
    yield from _produce_market_place_short_description(amount)


def _produce_market_place_long_description(session, guild_id):
    """
    Produces market place long description
    
    This function is an iterable generator.
    
    Parameters
    ----------
    session : ``MarketPlaceItem``
        The allocation's session.
    
    guild_id : `int`
        The local guild's identifier.
    
    Yields
    ------
    part : `str`
    """
    yield 'Purchasing: '
    item_amount = session.item_amount
    yield str(item_amount)
    yield ' '
    item = get_item_nullable(session.item_id)
    if item is None:
        yield 'unknown'
    
    else:
        emoji = item.emoji
        if (emoji is not None):
            yield emoji.as_emoji
            yield ' '
        
        yield item.name
        yield ' ('
        yield from produce_weight(item.weight * item_amount)
        yield ' kg)'
    
    # Produce time left
    yield '\nTime left: '
    yield elapsed_time(RelativeDelta(DateTime.now(TimeZone.utc), session.finalises_at))


def build_market_place_entry_component(user_id, page_index, session_id, amount):
    """
    Builds market place item components.
    
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
            ''.join([*_produce_market_place_short_description(amount)])
        ),
        thumbnail = create_button(
            'Details',
            custom_id = USER_ALLOCATIONS_CUSTOM_ID_DETAILS_BUILDER(
                user_id, page_index, ALLOCATION_FEATURE_ID_MARKET_PLACE, session_id
            ),
        ),
    )


def build_market_place_detailed_components(user_id, page_index, session_id, amount, session, extra, guild_id):
    """
    Builds market place detailed components.
    
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
    
    session : ``None | MarketPlaceItem``
        The game's session.
    
    extra : `None`
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
        ''.join([*_produce_market_place_title(amount)])
    ))
    
    # Add description
    
    if (session is not None):
        components.append(create_text_display(
            ''.join(_produce_market_place_long_description(session, guild_id))
        ))
    
    components.append(create_separator())
    
    # Add control
    
    while True:
        if (session is not None) and (CUSTOM_ID_MARKET_PLACE_OFFER_BUILDER is not None):
            custom_id = CUSTOM_ID_MARKET_PLACE_OFFER_BUILDER(user_id, session.entry_id, True)
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
