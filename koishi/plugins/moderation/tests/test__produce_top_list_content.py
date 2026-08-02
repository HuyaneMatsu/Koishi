import vampytest
from hata import User

from ..constants import (
    ACTION_TYPE_BAN, ACTION_TYPE_KICK, ACTION_TYPE_MUTE, ACTION_TYPE_NONE, TOP_LIST_NAME_ALL_HEADER,
    TOP_LIST_NAME_BAN_HEADER, TOP_LIST_NAME_KICK_HEADER, TOP_LIST_NAME_MUTE_HEADER, TOP_LIST_STYLE_ALL,
    TOP_LIST_STYLE_BAN, TOP_LIST_STYLE_FOCUS, TOP_LIST_STYLE_KICK, TOP_LIST_STYLE_MUTE, TOP_LIST_STYLE_NAME,
    TOP_LIST_STYLE_NUMBER
)
from ..content_building import produce_top_list_content
from ..top_list_action_counter import TopListActionCounter, top_list_action_counter_increment_with


def _iter_options():
    user_0 = User.precreate(202308020005, name = 'orin')
    user_1 = User.precreate(202308020006, name = 'okuu')
    user_2 = User.precreate(202308020007, name = 'satori')
    user_3 = User.precreate(202308020008, name = 'koishi')
    
    # This should not happen.
    yield (
        0,
        [],
        ACTION_TYPE_BAN,
        0,
        20,
        (
            '```ansi\n'
            '```'
        ),
    )
    
    top_list_action_counter_0 = TopListActionCounter()
    top_list_action_counter_increment_with(top_list_action_counter_0, ACTION_TYPE_BAN, 3)
    top_list_action_counter_1 = TopListActionCounter()
    top_list_action_counter_increment_with(top_list_action_counter_1, ACTION_TYPE_KICK, 2)
    
    yield (
        0,
        [
            (user_0, top_list_action_counter_0),
            (user_1, top_list_action_counter_1),
        ],
        ACTION_TYPE_BAN,
        0,
        20,
        (
            f'```ansi\n'
            f'    {TOP_LIST_STYLE_ALL}{TOP_LIST_NAME_ALL_HEADER} {TOP_LIST_STYLE_FOCUS}{TOP_LIST_NAME_BAN_HEADER} '
            f'{TOP_LIST_STYLE_KICK}{TOP_LIST_NAME_KICK_HEADER} {TOP_LIST_STYLE_MUTE}{TOP_LIST_NAME_MUTE_HEADER}\n'
            f'{TOP_LIST_STYLE_NUMBER}1.: {TOP_LIST_STYLE_ALL}  3 {TOP_LIST_STYLE_FOCUS}  3 {TOP_LIST_STYLE_KICK}   0 {TOP_LIST_STYLE_MUTE}   0 {TOP_LIST_STYLE_NAME}orin\n'
            f'{TOP_LIST_STYLE_NUMBER}2.: {TOP_LIST_STYLE_ALL}  2 {TOP_LIST_STYLE_FOCUS}  0 {TOP_LIST_STYLE_KICK}   2 {TOP_LIST_STYLE_MUTE}   0 {TOP_LIST_STYLE_NAME}okuu\n'
            f'```'
        ),
    )
    
    top_list_action_counter_0 = TopListActionCounter()
    top_list_action_counter_increment_with(top_list_action_counter_0, ACTION_TYPE_BAN, 30000)
    top_list_action_counter_1 = TopListActionCounter()
    top_list_action_counter_increment_with(top_list_action_counter_1, ACTION_TYPE_KICK, 20000)
    top_list_action_counter_2 = TopListActionCounter()
    top_list_action_counter_increment_with(top_list_action_counter_2, ACTION_TYPE_MUTE, 10000)
    
    yield (
        0,
        [
            (user_0, top_list_action_counter_0),
            (user_1, top_list_action_counter_1),
            (user_2, top_list_action_counter_2),
        ],
        ACTION_TYPE_NONE,
        0,
        20,
        (
            f'```ansi\n'
            f'    {TOP_LIST_STYLE_FOCUS}{TOP_LIST_NAME_ALL_HEADER:>5} {TOP_LIST_STYLE_BAN}{TOP_LIST_NAME_BAN_HEADER:>5} '
            f'{TOP_LIST_STYLE_KICK}{TOP_LIST_NAME_KICK_HEADER:>5} {TOP_LIST_STYLE_MUTE}{TOP_LIST_NAME_MUTE_HEADER:>5}\n'
            f'{TOP_LIST_STYLE_NUMBER}1.: {TOP_LIST_STYLE_FOCUS}30000 {TOP_LIST_STYLE_BAN}30000 {TOP_LIST_STYLE_KICK}    0 {TOP_LIST_STYLE_MUTE}    0 {TOP_LIST_STYLE_NAME}orin\n'
            f'{TOP_LIST_STYLE_NUMBER}2.: {TOP_LIST_STYLE_FOCUS}20000 {TOP_LIST_STYLE_BAN}    0 {TOP_LIST_STYLE_KICK}20000 {TOP_LIST_STYLE_MUTE}    0 {TOP_LIST_STYLE_NAME}okuu\n'
            f'{TOP_LIST_STYLE_NUMBER}3.: {TOP_LIST_STYLE_FOCUS}10000 {TOP_LIST_STYLE_BAN}    0 {TOP_LIST_STYLE_KICK}    0 {TOP_LIST_STYLE_MUTE}10000 {TOP_LIST_STYLE_NAME}satori\n'
            f'```'
        ),
    )
    
    # top_list_action_counter_0 = TopListActionCounter()
    # top_list_action_counter_increment_with(top_list_action_counter_0, ACTION_TYPE_BAN, 3)
    # top_list_action_counter_1 = TopListActionCounter()
    # top_list_action_counter_increment_with(top_list_action_counter_1, ACTION_TYPE_KICK, 2)
    top_list_action_counter_2 = TopListActionCounter()
    top_list_action_counter_increment_with(top_list_action_counter_2, ACTION_TYPE_MUTE, 2)
    top_list_action_counter_3 = TopListActionCounter()
    top_list_action_counter_increment_with(top_list_action_counter_3, ACTION_TYPE_MUTE, 1)
    
    yield (
        1,
        [
            (user_2, top_list_action_counter_2),
            (user_3, top_list_action_counter_3),
        ],
        ACTION_TYPE_MUTE,
        0,
        2,
        (
            f'```ansi\n'
            f'    {TOP_LIST_STYLE_ALL}{TOP_LIST_NAME_ALL_HEADER} {TOP_LIST_STYLE_BAN}{TOP_LIST_NAME_BAN_HEADER} '
            f'{TOP_LIST_STYLE_KICK}{TOP_LIST_NAME_KICK_HEADER} {TOP_LIST_STYLE_FOCUS}{TOP_LIST_NAME_MUTE_HEADER}\n'
            f'{TOP_LIST_STYLE_NUMBER}3.: {TOP_LIST_STYLE_ALL}  2 {TOP_LIST_STYLE_BAN}  0 {TOP_LIST_STYLE_KICK}   0 {TOP_LIST_STYLE_FOCUS}   2 {TOP_LIST_STYLE_NAME}satori\n'
            f'{TOP_LIST_STYLE_NUMBER}4.: {TOP_LIST_STYLE_ALL}  1 {TOP_LIST_STYLE_BAN}  0 {TOP_LIST_STYLE_KICK}   0 {TOP_LIST_STYLE_FOCUS}   1 {TOP_LIST_STYLE_NAME}koishi\n'
            f'```'
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__produce_top_list_content(page_index, entries, sort_by, guild_id, page_size):
    """
    Tests whether ``produce_top_list_content`` works as intended.
    
    Parameters
    ----------
    page_index : `int`
        The page to show. Used to calculate entry index.
    
    entries : ``list<(ClientUserBase, ActionCounter)>``
        Top list entries.
    
    sort_by : `int`
        The actions' identifier to sort by. Used to highlight that specific row.
    
    guild_id : `int`
        The local guild's identifier.
    
    page_size : `int`
        Custom page size to use.
    
    Returns
    -------
    output : `str`
    """
    mocked = vampytest.mock_globals(
        produce_top_list_content,
        TOP_LIST_PAGE_SIZE = page_size,
    )
    
    parts = [*mocked(page_index, entries, sort_by, guild_id)]
    for part in parts:
        vampytest.assert_instance(part, str)
    return ''.join(parts)
