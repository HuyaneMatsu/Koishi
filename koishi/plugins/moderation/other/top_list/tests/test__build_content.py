import vampytest
from hata import User

from ..action_counter import ActionCounter
from ..builders import build_content
from ..constants import (
    NAME_ALL_HEADER, NAME_BAN_HEADER, NAME_KICK_HEADER, NAME_MUTE_HEADER, STYLE_ALL, STYLE_BAN, STYLE_FOCUS, STYLE_KICK,
    STYLE_MUTE, STYLE_NAME, STYLE_NUMBER, TYPE_ALL, TYPE_BAN, TYPE_KICK, TYPE_MUTE
)


def test__build_content__empty():
    """
    Tests whether ``build_content`` works as intended.
    
    Case: Empty.
    """
    output = build_content(0, [], TYPE_BAN)
    
    vampytest.assert_instance(output, str)
    vampytest.assert_eq(
        output,
        (
            '```\n'
            'no result\n'
            '```'
        ),
    )


def test__build_content__page_0():
    """
    Tests whether ``build_content`` works as intended.
    
    Case: Page 0.
    """
    user_0 = User.precreate(202308020000, name = 'orin')
    user_1 = User.precreate(202308020001, name = 'okuu')
    
    entries = [
        (user_0, ActionCounter().increment_with(TYPE_BAN, 3)),
        (user_1, ActionCounter().increment_with(TYPE_KICK, 2)),
    ]
    
    output = build_content(0, entries, TYPE_BAN)
    
    vampytest.assert_instance(output, str)
    vampytest.assert_eq(
        output,
        (
            f'```ansi\n'
            f'    {STYLE_ALL}{NAME_ALL_HEADER} {STYLE_FOCUS}{NAME_BAN_HEADER} '
            f'{STYLE_KICK}{NAME_KICK_HEADER} {STYLE_MUTE}{NAME_MUTE_HEADER}\n'
            f'{STYLE_NUMBER}1.: {STYLE_ALL}  3 {STYLE_FOCUS}  3 {STYLE_KICK}   0 {STYLE_MUTE}   0 {STYLE_NAME}orin\n'
            f'{STYLE_NUMBER}2.: {STYLE_ALL}  2 {STYLE_FOCUS}  0 {STYLE_KICK}   2 {STYLE_MUTE}   0 {STYLE_NAME}okuu\n'
            f'```'
        ),
    )


def test__build_content__length_overload():
    """
    Tests whether ``build_content`` works as intended.
    
    Case: Value length overloaded.
    """
    user_0 = User.precreate(202308020002, name = 'orin')
    user_1 = User.precreate(202308020003, name = 'okuu')
    user_2 = User.precreate(202308020004, name = 'satori')
    
    entries = [
        (user_0, ActionCounter().increment_with(TYPE_BAN, 30000)),
        (user_1, ActionCounter().increment_with(TYPE_KICK, 20000)),
        (user_2, ActionCounter().increment_with(TYPE_MUTE, 10000)),
    ]
    
    output = build_content(0, entries, TYPE_ALL)
    
    vampytest.assert_instance(output, str)
    vampytest.assert_eq(
        output,
        (
            f'```ansi\n'
            f'    {STYLE_FOCUS}{NAME_ALL_HEADER:>5} {STYLE_BAN}{NAME_BAN_HEADER:>5} '
            f'{STYLE_KICK}{NAME_KICK_HEADER:>5} {STYLE_MUTE}{NAME_MUTE_HEADER:>5}\n'
            f'{STYLE_NUMBER}1.: {STYLE_FOCUS}30000 {STYLE_BAN}30000 {STYLE_KICK}    0 {STYLE_MUTE}    0 {STYLE_NAME}orin\n'
            f'{STYLE_NUMBER}2.: {STYLE_FOCUS}20000 {STYLE_BAN}    0 {STYLE_KICK}20000 {STYLE_MUTE}    0 {STYLE_NAME}okuu\n'
            f'{STYLE_NUMBER}3.: {STYLE_FOCUS}10000 {STYLE_BAN}    0 {STYLE_KICK}    0 {STYLE_MUTE}10000 {STYLE_NAME}satori\n'
            f'```'
        ),
    )



def test__build_content__page_1():
    """
    Tests whether ``build_content`` works as intended.
    
    Case: Page 1
    """
    user_0 = User.precreate(202308020005, name = 'orin')
    user_1 = User.precreate(202308020006, name = 'okuu')
    user_2 = User.precreate(202308020007, name = 'satori')
    user_3 = User.precreate(202308020008, name = 'koishi')
    
    entries = [
        (user_0, ActionCounter().increment_with(TYPE_BAN, 3)),
        (user_1, ActionCounter().increment_with(TYPE_KICK, 2)),
        (user_2, ActionCounter().increment_with(TYPE_MUTE, 2)),
        (user_3, ActionCounter().increment_with(TYPE_MUTE, 1)),
    ]
    
    mocked = vampytest.mock_globals(
        build_content,
        PAGE_SIZE = 2,
    )
    
    output = mocked(1, entries, TYPE_MUTE)
    
    vampytest.assert_instance(output, str)
    vampytest.assert_eq(
        output,
        (
            f'```ansi\n'
            f'    {STYLE_ALL}{NAME_ALL_HEADER} {STYLE_BAN}{NAME_BAN_HEADER} '
            f'{STYLE_KICK}{NAME_KICK_HEADER} {STYLE_FOCUS}{NAME_MUTE_HEADER}\n'
            f'{STYLE_NUMBER}3.: {STYLE_ALL}  2 {STYLE_BAN}  0 {STYLE_KICK}   0 {STYLE_FOCUS}   2 {STYLE_NAME}satori\n'
            f'{STYLE_NUMBER}4.: {STYLE_ALL}  1 {STYLE_BAN}  0 {STYLE_KICK}   0 {STYLE_FOCUS}   1 {STYLE_NAME}koishi\n'
            f'```'
        ),
    )
