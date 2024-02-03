import vampytest
from hata import Message, Role, User

from ..attachment_builders import iter_build_attachment_message_mentions


def test__iter_build_attachment_message_mentions__no_mentions():
    """
    tests whether ``iter_build_attachment_message_mentions`` works as intended.
    
    Case: No mentions.
    """
    mentioned_users = None
    mentioned_roles = None
    message_id = 202401310012
    
    message = Message.precreate(
        message_id,
        mentioned_users = mentioned_users,
        mentioned_roles = mentioned_roles,
    )
    
    output = [*iter_build_attachment_message_mentions(message)]
    vampytest.assert_eq(len(output), 0)


def test__iter_build_attachment_message_mentions__with_mentions():
    """
    tests whether ``iter_build_attachment_message_mentions`` works as intended.
    
    Case: With mentions.
    """
    user_id_0 = 202401310013
    user_name_0 = 'koishi'
    
    user_id_1 = 202401310014
    user_name_1 = 'satori'
    
    role_id_0 = 202401310015
    role_name_0 = 'okuu'
    
    role_id_1 = 202401310016
    role_name_1 = 'orin'
    
    mentioned_users = [
        User.precreate(user_id_0, name = user_name_0),
        User.precreate(user_id_1, name = user_name_1),
    ]
    mentioned_roles = [
        Role.precreate(role_id_0, name = role_name_0),
        Role.precreate(role_id_1, name = role_name_1),
    ]
    message_id = 202401310017
    
    message = Message.precreate(
        message_id,
        mentioned_everyone = True,
        mentioned_users = mentioned_users,
        mentioned_roles = mentioned_roles,
    )
    
    output = [*iter_build_attachment_message_mentions(message)]
    vampytest.assert_eq(len(output), 1)
    
    vampytest.assert_eq(
        output[0],
        (
            'mentions.txt',
            (
                f'### Mentioned everyone\n'
                f'\n'
                f'true\n'
                f'\n'
                f'### Mentioned roles\n'
                f'\n'
                f'1.: {role_name_0!s} ({role_id_0!s})\n'
                f'2.: {role_name_1!s} ({role_id_1!s})\n'
                f'\n'
                f'### Mentioned users\n'
                f'\n'
                f'1.: {user_name_0!s} ({user_id_0!s})\n'
                f'2.: {user_name_1!s} ({user_id_1!s})\n'
            ),
        ),
    )
