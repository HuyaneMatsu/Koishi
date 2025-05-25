import vampytest
from hata import Embed, User, create_button, create_row
from hata.ext.slash import InteractionResponse

from ..action_counter import ActionCounter
from ..builders import build_top_list_response
from ..constants import (
    BUTTON_CLOSE, BUTTON_PAGE_NEXT_DISABLED, CUSTOM_ID_PAGE_BASE, EMOJI_PAGE_PREVIOUS, NAME_ALL_HEADER, NAME_BAN_HEADER,
    NAME_KICK_HEADER, NAME_MUTE_HEADER, STYLE_ALL, STYLE_BAN, STYLE_FOCUS, STYLE_KICK, STYLE_NAME, STYLE_NUMBER,
    TYPE_BAN, TYPE_KICK, TYPE_MUTE
)


def test__build_top_list_response():
    """
    Tests whether ``build_top_list_response`` works as intended.
    """
    page_index = 1
    sort_by = TYPE_MUTE
    days = 45
    
    user_0 = User.precreate(202308020009, name = 'orin')
    user_1 = User.precreate(202308020010, name = 'okuu')
    user_2 = User.precreate(202308020011, name = 'satori')
    user_3 = User.precreate(202308020012, name = 'koishi')
    
    entries = [
        (user_0, ActionCounter().increment_with(TYPE_BAN, 3)),
        (user_1, ActionCounter().increment_with(TYPE_KICK, 2)),
        (user_2, ActionCounter().increment_with(TYPE_MUTE, 2)),
        (user_3, ActionCounter().increment_with(TYPE_MUTE, 1)),
    ]
    
    
    mocked = vampytest.mock_globals(
        build_top_list_response,
        2,
        PAGE_SIZE = 2,
    )
    
    output = mocked(page_index, entries, sort_by, days)
    
    vampytest.assert_eq(
        output,
        InteractionResponse(
            embed = Embed(
                'Mod top-list',
                (
                    f'```ansi\n'
                    f'    {STYLE_ALL}{NAME_ALL_HEADER} {STYLE_BAN}{NAME_BAN_HEADER} '
                    f'{STYLE_KICK}{NAME_KICK_HEADER} {STYLE_FOCUS}{NAME_MUTE_HEADER}\n'
                    f'{STYLE_NUMBER}3.: {STYLE_ALL}  2 {STYLE_BAN}  0 {STYLE_KICK}   0 {STYLE_FOCUS}   2 {STYLE_NAME}satori\n'
                    f'{STYLE_NUMBER}4.: {STYLE_ALL}  1 {STYLE_BAN}  0 {STYLE_KICK}   0 {STYLE_FOCUS}   1 {STYLE_NAME}koishi\n'
                    f'```'
                ),
            ).add_field(
                'Sorted by',
                (
                    f'```\n'
                    f'{"mute"}\n'
                    f'```'
                ),
                inline = True,
            ).add_field(
                'Days',
                (
                    f'```\n'
                    f'{days}\n'
                    f'```'
                ),
                inline = True,
            ).add_field(
                'Page',
                (
                    f'```\n'
                    f'{page_index + 1}\n'
                    f'```'
                ),
                inline = True,
            ),
            components = create_row(
                create_button(
                    'Page 1',
                    emoji = EMOJI_PAGE_PREVIOUS,
                    custom_id = f'{CUSTOM_ID_PAGE_BASE}{page_index - 1 !s};s={sort_by!s};d={days!s}',
                ),
                BUTTON_PAGE_NEXT_DISABLED.copy_with(
                    label = 'Page 3',
                ),
                BUTTON_CLOSE,
            ),
        ),
    )
