__all__ = (
    'command_in_guild_emoji_statistics', 'command_of_guild_emoji_statistics', 'command_in_guild_sticker_statistics',
    'command_of_guild_sticker_statistics',
)

from hata.ext.slash import P

from ..expression_tracking import (
    ACTION_TYPE_EMOJI_CONTENT, ACTION_TYPE_EMOJI_REACTION, ACTION_TYPE_STICKER, ENTITY_FILTER_RULE_EMOJI_ANIMATED,
    ENTITY_FILTER_RULE_EMOJI_STATIC, ENTITY_FILTER_RULE_NONE, query_expression_in_guild_most_used,
    query_expression_of_guild_most_used
)

from .component_building import build_components
from .constants import MODE_GUILD_IN, MODE_GUILD_OF
from .helpers import pack_action_types, unpack_action_types


PARAMETER_MONTHS = P(
    [(str(index), format(index, 'x')) for index in range(1, 13)],
    'The amount of months to query for?',
    'months',
)
PARAMETER_MONTHS_DEFAULT = format(1, 'x')

PARAMETER_ORDER_DECREASING = P(
    [
        ('Decreasing', format(True, 'x')),
        ('Increasing', format(False, 'x')),
    ],
    'Ordering?'
    'order',
)
PARAMETER_ORDER_DECREASING_DEFAULT = format(True, 'x')

PARAMETER_PAGE_SIZE = P(
    [(str(index), format(index, 'x')) for index in range(10, 60, 10)],
    'Page size to use.',
)
PARAMETER_PAGE_SIZE_DEFAULT = format(30, 'x')


PARAMETER_ACTION_TYPES_PACKED_EMOJI = P(
    [
        ('all', format(pack_action_types((ACTION_TYPE_EMOJI_CONTENT, ACTION_TYPE_EMOJI_REACTION)), 'x')),
        ('content', format(pack_action_types((ACTION_TYPE_EMOJI_CONTENT,)), 'x')),
        ('reaction', format(pack_action_types((ACTION_TYPE_EMOJI_REACTION,)), 'x')),
    ],
    'Actions to filter for.',
    'actions',
)
PARAMETER_ACTION_TYPES_PACKED_EMOJI_DEFAULT = format(
    pack_action_types((ACTION_TYPE_EMOJI_CONTENT, ACTION_TYPE_EMOJI_REACTION)),
    'x'
)

PARAMETER_ENTITY_FILTER_RULE_EMOJI = P(
    [
        ('all', format(ENTITY_FILTER_RULE_NONE, 'x')),
        ('static', format(ENTITY_FILTER_RULE_EMOJI_STATIC, 'x')),
        ('animated', format(ENTITY_FILTER_RULE_EMOJI_ANIMATED, 'x')),
    ],
    'The kind of emoji to filter for.',
    'kind',
)
PARAMETER_ENTITY_FILTER_RULE_EMOJI_DEFAULT = format(ENTITY_FILTER_RULE_NONE, 'x')


async def _respond_guild_statistics_command_invocation(
    client,
    interaction_event,
    guild,
    mode,
    action_types_packed,
    entity_filter_rule,
    months,
    page_size,
    order_decreasing,
):
    """
    Responds on a guild statistic command invocation.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client receiving this interaction.
    
    interaction_event : ``InteractionEvent``
        The received interaction event.
    
    mode : `int`
        The usage mode to respond with.
    
    action_types_packed : `int`
        The action types packed.
    
    entity_filter_rule : `int`
        Entity filter rule for detailed filtering.
    
    months : `int`
        The amount of months to look back as a hexadecimal integer.
    
    page_size : `int`
        The page's size to display.
    
    order_decreasing : `bool`
        Whether to order in a decreasing order.
    """
    await client.interaction_application_command_acknowledge(
        interaction_event,
        False,
    )
    
    # Get data
    if mode == MODE_GUILD_OF:
        entries, page_count = await query_expression_of_guild_most_used(
            guild,
            unpack_action_types(action_types_packed),
            entity_filter_rule,
            months,
            0,
            page_size,
            order_decreasing,
        )
    
    elif mode == MODE_GUILD_IN:
        entries, page_count = await query_expression_in_guild_most_used(
            guild,
            unpack_action_types(action_types_packed),
            months,
            0,
            page_size,
            order_decreasing,
        )
    
    else:
        # No other cases:
        entries = []
        page_count = 0
    
    # Respond
    await client.interaction_response_message_edit(
        interaction_event,
        components = build_components(
            client,
            interaction_event.user,
            guild,
            entries,
            page_count,
            mode,
            action_types_packed,
            entity_filter_rule,
            months,
            0,
            page_size,
            order_decreasing,
        ),
    )


async def command_in_guild_emoji_statistics(
    client,
    interaction_event,
    action_types_packed : PARAMETER_ACTION_TYPES_PACKED_EMOJI = PARAMETER_ACTION_TYPES_PACKED_EMOJI_DEFAULT,
    months : PARAMETER_MONTHS = PARAMETER_MONTHS_DEFAULT,
    order_decreasing : PARAMETER_ORDER_DECREASING = PARAMETER_ORDER_DECREASING_DEFAULT,
    page_size : PARAMETER_PAGE_SIZE = PARAMETER_PAGE_SIZE_DEFAULT,
):
    """
    Shows the usage statistics about the emojis used in the guild.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client receiving this interaction.
    
    interaction_event : ``InteractionEvent``
        The received interaction event.
    action_types_packed = `str` = `PARAMETER_ACTION_TYPES_PACKED_EMOJI_DEFAULT`
        The action types packed as a hexadecimal integer.
    
    months : `str` = `PARAMETER_MONTHS_DEFAULT`
        The amount of months to query for as a hexadecimal integer.
    
    order_decreasing : `str` = `PARAMETER_ORDER_DECREASING_DEFAULT`
        Whether to order in a decreasing order as a hexadecimal integer.
    
    page_size : `str` = `PARAMETER_PAGE_SIZE_DEFAULT`
        The page's size to display as a hexadecimal integer.
    """
    # Convert
    try:
        action_types_packed = int(action_types_packed, 16)
        months = int(months, 16)
        order_decreasing = int(order_decreasing, 16)
        page_size = int(page_size, 16)
    except ValueError:
        return
    
    order_decreasing = True if order_decreasing else False
    
    # Validate
    guild = interaction_event.guild
    if guild is None:
        return
    
    await _respond_guild_statistics_command_invocation(
        client,
        interaction_event,
        guild,
        MODE_GUILD_IN,
        action_types_packed,
        ENTITY_FILTER_RULE_NONE,
        months,
        page_size,
        order_decreasing,
    )


async def command_of_guild_emoji_statistics(
    client,
    interaction_event,
    action_types_packed : PARAMETER_ACTION_TYPES_PACKED_EMOJI = PARAMETER_ACTION_TYPES_PACKED_EMOJI_DEFAULT,
    entity_filter_rule : PARAMETER_ENTITY_FILTER_RULE_EMOJI = PARAMETER_ENTITY_FILTER_RULE_EMOJI_DEFAULT,
    months : PARAMETER_MONTHS = PARAMETER_MONTHS_DEFAULT,
    order_decreasing : PARAMETER_ORDER_DECREASING = PARAMETER_ORDER_DECREASING_DEFAULT,
    page_size : PARAMETER_PAGE_SIZE = PARAMETER_PAGE_SIZE_DEFAULT,
):
    """
    Shows the usage statistics of the emojis of the guild.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client receiving this interaction.
    
    interaction_event : ``InteractionEvent``
        The received interaction event.
    
    action_types_packed = `str` = `PARAMETER_ACTION_TYPES_PACKED_EMOJI_DEFAULT`
        The action types packed as a hexadecimal integer.
    
    entity_filter_rule : `str` = `PARAMETER_ENTITY_FILTER_RULE_EMOJI_DEFAULT`
        Entity filter rule for detailed filtering as hexadecimal integer.
    
    months : `str` = `PARAMETER_MONTHS_DEFAULT`
        The amount of months to query for as a hexadecimal integer.
    
    order_decreasing : `str` = `PARAMETER_ORDER_DECREASING_DEFAULT`
        Whether to order in a decreasing order as a hexadecimal integer.
    
    page_size : `str` = `PARAMETER_PAGE_SIZE_DEFAULT`
        The page's size to display as a hexadecimal integer.
    """
    # Convert
    try:
        action_types_packed = int(action_types_packed, 16)
        entity_filter_rule = int(entity_filter_rule, 16)
        months = int(months, 16)
        order_decreasing = int(order_decreasing, 16)
        page_size = int(page_size, 16)
    except ValueError:
        return
    
    order_decreasing = True if order_decreasing else False
    
    # Validate
    guild = interaction_event.guild
    if guild is None:
        return
    
    await _respond_guild_statistics_command_invocation(
        client,
        interaction_event,
        guild,
        MODE_GUILD_OF,
        action_types_packed,
        entity_filter_rule,
        months,
        page_size,
        order_decreasing,
    )


async def command_in_guild_sticker_statistics(
    client,
    interaction_event,
    months : PARAMETER_MONTHS = PARAMETER_MONTHS_DEFAULT,
    order_decreasing : PARAMETER_ORDER_DECREASING = PARAMETER_ORDER_DECREASING_DEFAULT,
    page_size : PARAMETER_PAGE_SIZE = PARAMETER_PAGE_SIZE_DEFAULT,
):
    """
    Shows the usage statistics about the stickers used in the guild.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client receiving this interaction.
    
    interaction_event : ``InteractionEvent``
        The received interaction event.
    
    months : `str` = `PARAMETER_MONTHS_DEFAULT`
        The amount of months to query for as a hexadecimal integer.
    
    order_decreasing : `str` = `PARAMETER_ORDER_DECREASING_DEFAULT`
        Whether to order in a decreasing order as a hexadecimal integer.
    
    page_size : `str` = `PARAMETER_PAGE_SIZE_DEFAULT`
        The page's size to display as a hexadecimal integer.
    """
    # Convert
    try:
        months = int(months, 16)
        order_decreasing = int(order_decreasing, 16)
        page_size = int(page_size, 16)
    except ValueError:
        return
    
    order_decreasing = True if order_decreasing else False
    
    # Validate
    guild = interaction_event.guild
    if guild is None:
        return
    
    await _respond_guild_statistics_command_invocation(
        client,
        interaction_event,
        guild,
        MODE_GUILD_IN,
        pack_action_types((ACTION_TYPE_STICKER, )),
        ENTITY_FILTER_RULE_NONE,
        months,
        page_size,
        order_decreasing,
    )


async def command_of_guild_sticker_statistics(
    client,
    interaction_event,
    months : PARAMETER_MONTHS = PARAMETER_MONTHS_DEFAULT,
    order_decreasing : PARAMETER_ORDER_DECREASING = PARAMETER_ORDER_DECREASING_DEFAULT,
    page_size : PARAMETER_PAGE_SIZE = PARAMETER_PAGE_SIZE_DEFAULT,
):
    """
    Shows the usage statistics of the stickers of the guild.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client receiving this interaction.
    
    interaction_event : ``InteractionEvent``
        The received interaction event.
    
    months : `str` = `PARAMETER_MONTHS_DEFAULT`
        The amount of months to query for as a hexadecimal integer.
    
    order_decreasing : `str` = `PARAMETER_ORDER_DECREASING_DEFAULT`
        Whether to order in a decreasing order as a hexadecimal integer.
    
    page_size : `str` = `PARAMETER_PAGE_SIZE_DEFAULT`
        The page's size to display as a hexadecimal integer.
    """
    # Convert
    try:
        months = int(months, 16)
        order_decreasing = int(order_decreasing, 16)
        page_size = int(page_size, 16)
    except ValueError:
        return
    
    order_decreasing = True if order_decreasing else False
    
    # Validate
    guild = interaction_event.guild
    if guild is None:
        return
    
    await _respond_guild_statistics_command_invocation(
        client,
        interaction_event,
        guild,
        MODE_GUILD_OF,
        pack_action_types((ACTION_TYPE_STICKER, )),
        ENTITY_FILTER_RULE_NONE,
        months,
        page_size,
        order_decreasing,
    )
