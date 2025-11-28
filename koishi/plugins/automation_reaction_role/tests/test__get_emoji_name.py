import vampytest
from hata import BUILTIN_EMOJIS, Emoji, Guild, GuildProfile, User

from ..content_builders import get_emoji_name


def _iter_options():
    user_id = 202510010000
    guild_id = 202510010001
    emoji_id_0 = 202510010002
    emoji_id_1 = 202510010003
    
    emoji_0 = Emoji.precreate(
        emoji_id_0,
        guild_id = guild_id,
        name = 'satori',
    )
    
    emoji_1 = Emoji.precreate(
        emoji_id_1,
        name = 'satori',
    )
    
    emoji_2 = BUILTIN_EMOJIS['heart']
    
    
    user = User.precreate(user_id,)
    user.guild_profiles[guild_id] = GuildProfile()
    
    guild = Guild.precreate(
        guild_id,
        emojis = [emoji_0, emoji_1, emoji_2],
    )
    
    yield (
        user,
        emoji_0.id,
        [guild, emoji_0],
        f'{emoji_0} {emoji_0.name}',
    )
    
    yield (
        user,
        emoji_1.id,
        [guild, emoji_1],
        f'{emoji_1.name}',
    )
    
    yield (
        user,
        emoji_2.id,
        [guild, emoji_2],
        f'{emoji_2} {emoji_2.name}',
    )
    
    yield (
        user,
        999999,
        [guild],
        'unknown',
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__get_emoji_name(user, emoji_id, entity_cache):
    """
    Tests whether ``get_emoji_name`` works as intended.
    
    Parameters
    ----------
    user : ``ClientUserBase``
        The use from who's view point we are inspecting the emoji.
    
    emoji_id : `int`
        The emoji's identifier.
    
    entity_cache : `list<object>`
        Additional objects to keep cached.
    
    Returns
    -------
    output : `str`
    """
    output = get_emoji_name(user, emoji_id)
    vampytest.assert_instance(output, str)
    return output
