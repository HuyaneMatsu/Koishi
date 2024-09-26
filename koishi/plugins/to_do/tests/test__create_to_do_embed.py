from datetime import datetime as DateTime, timezone as TimeZone

import vampytest
from hata import Embed, Icon, IconType, User

from ..helpers import create_to_do_embed
from ..to_do import ToDo


def test__create_to_do_embed():
    """
    Tests whether ``create_to_do_embed`` works as intended.
    """
    created_at = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    creator_id = 202409170030
    description = 'nyan nyan'
    name = 'miau'
    
    entry_id = 120
    
    to_do = ToDo(name, description, created_at, creator_id)
    to_do.entry_id = entry_id
    
    user_name = 'orin'
    user = User.precreate(creator_id, avatar = Icon(IconType.static, 2), name = user_name)
    
    output = create_to_do_embed(to_do, user)
    vampytest.assert_instance(output, Embed)
    
    vampytest.assert_eq(
        output,
        Embed(
            'To-Do entry #120',
        ).add_field(
            'By',
            (
                '```\n'
                'orin\n'
                '```'
            ),
            inline = True,
        ).add_field(
            'At',
            (
                '```\n'
                '2016-05-14 00:00:00\n'
                '```'
            ),
            inline = True,
        ).add_field(
            'Name',
            (
                '```\n'
                'miau\n'
                '```'
            ),
        ).add_field(
            'Description',
            (
                '```\n'
                'nyan nyan\n'
                '```'
            ),
        ).add_thumbnail(
            f'https://cdn.discordapp.com/avatars/{creator_id!s}/00000000000000000000000000000002.png'
        ),
    )
