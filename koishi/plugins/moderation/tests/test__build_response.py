import vampytest
from hata import User, create_button, create_row, Guild, Icon, IconType, create_section, create_text_display, \
    create_thumbnail_media, create_separator, Component

from ..constants import (
    ACTION_TYPE_BAN, ACTION_TYPE_KICK, ACTION_TYPE_MUTE, TOP_LIST_NAME_ALL_HEADER,
    TOP_LIST_NAME_BAN_HEADER, TOP_LIST_NAME_KICK_HEADER, TOP_LIST_NAME_MUTE_HEADER, TOP_LIST_STYLE_ALL,
    TOP_LIST_STYLE_BAN, TOP_LIST_STYLE_FOCUS, TOP_LIST_STYLE_KICK, TOP_LIST_STYLE_NAME,
    TOP_LIST_STYLE_NUMBER, EMOJI_PAGE_PREVIOUS, EMOJI_PAGE_NEXT, EMOJI_CLOSE
)
from ..component_building import build_mod_top_list_components
from ..top_list_action_counter import TopListActionCounter, top_list_action_counter_increment_with


def _iter_options():
    user_id = 202308020020
    guild = Guild.precreate(202308020021, icon = Icon(IconType.static, 2), name = 'Moriya shrine')
    
    user_0 = User.precreate(202308020009, name = 'orin')
    user_1 = User.precreate(202308020010, name = 'okuu')
    user_2 = User.precreate(202308020011, name = 'satori')
    user_3 = User.precreate(202308020012, name = 'koishi')
    
    
    top_list_action_counter_0 = TopListActionCounter()
    top_list_action_counter_increment_with(top_list_action_counter_0, ACTION_TYPE_BAN, 3)
    top_list_action_counter_1 = TopListActionCounter()
    top_list_action_counter_increment_with(top_list_action_counter_1, ACTION_TYPE_KICK, 2)
    top_list_action_counter_2 = TopListActionCounter()
    top_list_action_counter_increment_with(top_list_action_counter_2, ACTION_TYPE_MUTE, 2)
    top_list_action_counter_3 = TopListActionCounter()
    top_list_action_counter_increment_with(top_list_action_counter_3, ACTION_TYPE_MUTE, 1)
    
    yield (
        user_id,
        guild,
        1,
        [
            (user_0, top_list_action_counter_0),
            (user_1, top_list_action_counter_1),
            (user_2, top_list_action_counter_2),
            (user_3, top_list_action_counter_3),
        ],
        ACTION_TYPE_MUTE,
        45,
        2,
        [
            create_section(
                create_text_display(
                    '# Moriya shrine\'s mod top-list\n'
                    '\n'
                    'Sort by: mute\n'
                    'Days: 45\n'
                    'Page: 2'
                ),
                thumbnail = create_thumbnail_media(
                    f'https://cdn.discordapp.com/icons/{guild.id}/00000000000000000000000000000002.png',
                ),
            ),
            create_separator(),
            create_text_display(
                f'```ansi\n'
                f'    {TOP_LIST_STYLE_ALL}{TOP_LIST_NAME_ALL_HEADER} {TOP_LIST_STYLE_BAN}{TOP_LIST_NAME_BAN_HEADER} '
                f'{TOP_LIST_STYLE_KICK}{TOP_LIST_NAME_KICK_HEADER} {TOP_LIST_STYLE_FOCUS}{TOP_LIST_NAME_MUTE_HEADER}\n'
                f'{TOP_LIST_STYLE_NUMBER}3.: {TOP_LIST_STYLE_ALL}  2 {TOP_LIST_STYLE_BAN}  0 {TOP_LIST_STYLE_KICK}   0 {TOP_LIST_STYLE_FOCUS}   2 {TOP_LIST_STYLE_NAME}satori\n'
                f'{TOP_LIST_STYLE_NUMBER}4.: {TOP_LIST_STYLE_ALL}  1 {TOP_LIST_STYLE_BAN}  0 {TOP_LIST_STYLE_KICK}   0 {TOP_LIST_STYLE_FOCUS}   1 {TOP_LIST_STYLE_NAME}koishi\n'
                f'```'
            ),
            create_separator(),
            create_row(
                create_button(
                    'Page 1',
                    EMOJI_PAGE_PREVIOUS,
                    custom_id = f'mod.top_list.page.{user_id:x}.{0:x}.{ACTION_TYPE_MUTE:x}.{45:x}',
                    enabled = True,
                ),
                create_button(
                    'Page 3',
                    EMOJI_PAGE_NEXT,
                    custom_id = 'mod.top_list.page.disabled.i',
                    enabled = False,
                ),
                create_button(
                    'Close',
                    EMOJI_CLOSE,
                    custom_id = f'mod.top_list.close.{user_id:x}',
                ),
            ),
        ],
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_mod_top_list_components(user_id, guild, page_index, entries, sort_by, days, page_size):
    """
    Tests whether ``build_mod_top_list_components`` works as intended.
    
    Parameters
    ----------
    user_id : `int`
        The invoking user's identifier.
    
    guild : ``Guild```
        The local guild.
    
    page_index : `int`
        The page to show. Used to calculate entry index.
    
    entries : ``list<(ClientUserBase, ActionCounter)>``
        Top list entries.
    
    sort_by : `int`
        The actions' identifier to sort by. Used to highlight that specific row.
    
    days : `int`
        The days to query for.
    
    page_size : `int`
        Custom page size to use.
    
    Returns
    -------
    output : ``list<Component>``
    """
    mocked = vampytest.mock_globals(
        build_mod_top_list_components,
        2,
        TOP_LIST_PAGE_SIZE = page_size,
    )
    
    output = mocked(user_id, guild, page_index, entries, sort_by, days)
    vampytest.assert_instance(output, list)
    for element in output:
        vampytest.assert_instance(element, Component)
    return output
