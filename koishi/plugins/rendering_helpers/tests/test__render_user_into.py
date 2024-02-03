import vampytest
from hata import Guild, GuildProfile, User

from ..value_renderers import render_user_into


def test__render_user_into__no_nick():
    """
    Tests whether ``render_user_into`` works as intended.
    
    Case: No nick.
    """
    user_id = 202401300000
    name = 'koishi'
    user = User.precreate(user_id, name = name)
    guild = None
    
    into = render_user_into([], user, guild)
    
    for element in into:
        vampytest.assert_instance(element, str)
    
    output = ''.join(into)
    
    vampytest.assert_eq(output, f'{name!s} ({user_id!s})')


def test__render_user_into__with_nick():
    """
    Tests whether ``render_user_into`` works as intended.
    
    Case: With nick.
    """
    user_id = 202401300001
    guild_id = 202401300002
    name = 'koishi'
    nick = 'koi'
    user = User.precreate(user_id, name = name)
    user.guild_profiles[guild_id] = GuildProfile(nick = nick)
    guild = Guild.precreate(guild_id)
    
    into = render_user_into([], user, guild)
    
    for element in into:
        vampytest.assert_instance(element, str)
    
    output = ''.join(into)
    
    vampytest.assert_eq(output, f'{name!s} [*{nick!s}*] ({user_id!s})')
