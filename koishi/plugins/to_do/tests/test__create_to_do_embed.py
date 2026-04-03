from datetime import datetime as DateTime, timezone as TimeZone

import vampytest
from hata import Embed, GuildProfile, Icon, IconType, User

from ..helpers import create_to_do_embed
from ..to_do import ToDo


def _iter_options():
    created_at = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    creator_id = 202409170030
    guild_id = 202503290006
    description = 'nyan nyan'
    name = 'miau'
    
    entry_id = 120
    
    to_do = ToDo(name, description, created_at, creator_id)
    to_do.entry_id = entry_id
    
    user = User.precreate(creator_id, avatar = Icon(IconType.static, 2), name = 'orin')
    user.guild_profiles[guild_id] = GuildProfile(avatar = Icon(IconType.static, 3), nick = 'maid')
    
    yield (
        to_do,
        user,
        0,
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
    
    yield (
        to_do,
        user,
        guild_id,
        Embed(
            'To-Do entry #120',
        ).add_field(
            'By',
            (
                '```\n'
                'maid\n'
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
            f'https://cdn.discordapp.com/guilds/{guild_id}/users/{creator_id!s}/avatars/00000000000000000000000000000003.png'
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__create_to_do_embed(to_do, user, guild_id):
    """
    Tests whether ``create_to_do_embed`` works as intended.
    
    Parameters
    ----------
    to_do : ``ToDo``
        The to-do to represent.
    
    user : ``ClientUserBase``
        The user who added the to-do entry.
    
    guild_id : `int`
        The respective guild's identifier.
    
    Returns
    -------
    embed : ``Embed``
    """
    output = create_to_do_embed(to_do, user, guild_id)
    vampytest.assert_instance(output, Embed)
    return output
