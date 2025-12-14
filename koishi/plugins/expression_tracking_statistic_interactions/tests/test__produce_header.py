__all__ = ()

import vampytest
from hata import Guild

from ...expression_tracking import (
    ACTION_TYPE_EMOJI_CONTENT, ACTION_TYPE_EMOJI_REACTION, ENTITY_FILTER_RULE_NONE, ENTITY_FILTER_RULE_EMOJI_STATIC
)

from ..constants import MODE_GUILD_IN, MODE_GUILD_OF
from ..content_building import produce_header
from ..helpers import pack_action_types


def _iter_options():
    guild_id = 202512120000
    guild = Guild.precreate(
        guild_id,
        name = 'Koishi',
    )
    
    yield (
        guild,
        MODE_GUILD_IN,
        pack_action_types((ACTION_TYPE_EMOJI_CONTENT, )),
        ENTITY_FILTER_RULE_NONE,
        12,
        1,
        20,
        True,
        (
            '# In Koishi\'s emojis in content\n'
            'Page: 2; page size: 20; months: 12; order: decreasing'
        ),
    )
    
    yield (
        guild,
        MODE_GUILD_OF,
        pack_action_types((ACTION_TYPE_EMOJI_CONTENT, ACTION_TYPE_EMOJI_REACTION)),
        ENTITY_FILTER_RULE_EMOJI_STATIC,
        6,
        0,
        10,
        False,
        (
            '# Of Koishi\'s static emojis\n'
            'Page: 1; page size: 10; months: 6; order: increasing'
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__produce_header(
    guild,
    mode,
    action_types_packed,
    entity_filter_rule,
    months,
    page_index,
    page_size,
    order_decreasing,
):
    """
    Tests whether ``produce_header`` works as intended.
    
    Parameters
    ----------
    guild : ``None | Guild``
        The guild in context.
    
    mode : `int`
        The usage mode to respond with.
    
    action_types_packed : `int`
        The action types packed.
    
    entity_filter_rule : `int`
        Entity filter rule for detailed filtering.
    
    months : `int`
        The amount of months to look back.
    
    page_index : `int`
        The page's index to display.
    
    page_size : `int`
        The page's size to display.
    
    order_decreasing : `bool`
        Whether to order in a decreasing order.
    
    Returns
    -------
    output : `str`
    """
    output = [*produce_header(
        guild,
        mode,
        action_types_packed,
        entity_filter_rule,
        months,
        page_index,
        page_size,
        order_decreasing,
    )]
    
    for element in output:
        vampytest.assert_instance(element, str)
    
    return ''.join(output)
