import vampytest
from hata import User

from ..attachment_builders import render_voters_into


def test__render_voters_into__no_users():
    """
    Tests whether ``render_voters_into`` works as intended.
    
    Case: No users.
    """
    users = set()
    guild = None
    
    into = render_voters_into([], users, guild)
    
    vampytest.assert_instance(into, list)
    for element in into:
        vampytest.assert_instance(element, str)
    
    output = ''.join(into)
    vampytest.assert_eq(output, '')


def test__render_voters_into__with_users():
    """
    tests whether ``render_voters_into`` works as intended.
    
    Case: With mentions.
    """
    user_id_0 = 202402010003
    user_name_0 = 'koishi'
    
    user_id_1 = 202402010004
    user_name_1 = 'satori'
    
    users = {
        User.precreate(user_id_0, name = user_name_0),
        User.precreate(user_id_1, name = user_name_1),
    }
    
    guild = None
    
    
    into = render_voters_into([], users, guild)

    vampytest.assert_instance(into, list)
    for element in into:
        vampytest.assert_instance(element, str)
    
    output = ''.join(into)
    
    vampytest.assert_eq(
        output,
        (
            f'1.: {user_name_0!s} ({user_id_0!s})\n'
            f'2.: {user_name_1!s} ({user_id_1!s})'
        ),
    )
