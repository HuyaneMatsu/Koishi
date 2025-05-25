import vampytest
from hata import Guild, GuildProfile, User

from ..field_renderers import render_user_field_into


def _iter_options():
    user_id = 202402010000
    guild_id = 202402010001
    name = 'koishi'
    nick = 'koi'
    user = User.precreate(user_id, name = name)
    user.guild_profiles[guild_id] = GuildProfile(nick = nick)
    guild = Guild.precreate(guild_id)
    
    yield False, None, False, None, 'User', ('User: *none*', True)
    yield True, None, False, None, 'User', ('\nUser: *none*', True)
    yield False, user, False, None, 'User', (f'User: {name!s} ({user_id!s})', True)
    yield True, user, False, None, 'User', (f'\nUser: {name!s} ({user_id!s})', True)
    yield False, None, True, None, 'User', ('', False)
    yield True, None, True, None, 'User', ('', True)
    yield False, user, True, None, 'User', (f'User: {name!s} ({user_id!s})', True)
    yield True, user, True, None, 'User', (f'\nUser: {name!s} ({user_id!s})', True)
    
    # guild
    yield False, user, True, guild, 'User', (f'User: {name!s} [*{nick!s}*] ({user_id!s})', True)
    
    # title
    yield False, user, True, None, 'Author', (f'Author: {name!s} ({user_id!s})', True)


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__render_user_field_into(field_added, user, optional, guild, title):
    """
    Tests whether ``render_user_field_into`` works as intended.
    
    Parameters
    ----------
    field_added : `bool`
        Whether a field was already added.
    user : `None | ClientUserBase`
        The user to render.
    optional : `bool`
        Whether the field should not be rendered if `user` is `None`.
    guild : ``None | Guild``
        The guild to pull name for.
    title : `str`
        The title to use.
    
    Returns
    -------
    output : `str`
    field_added : `bool`
    """
    into, field_added = render_user_field_into(
        [], field_added, user, guild = guild, optional = optional, title = title
    ) 
    
    for element in into:
        vampytest.assert_instance(element, str)
    
    return ''.join(into), field_added
