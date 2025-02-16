import vampytest
from hata import Embed, GuildProfile, Role, Guild, User

from ..embed_builders import build_failure_embed_not_in_guild_other


def _iter_options():
    role_id = 202502130007
    guild_id_0 = 202502130008
    guild_id_1 = 202502130009
    user_id = 202502130010
    
    user = User.precreate(user_id, name = 'Keine')
    user.guild_profiles[guild_id_0] = GuildProfile(nick = 'Caver')
    role = Role.precreate(role_id, name = 'Nyan', guild_id = guild_id_1)
    guild = Guild.precreate(guild_id_1, name = 'Hell')
    
    yield (
        role,
        user,
        0,
        [guild],
        Embed(
            'Not in guild',
            'Keine must be in Hell to receive the Nyan role.'
        ),
    )
    yield (
        role,
        user,
        guild_id_0,
        [guild],
        Embed(
            'Not in guild',
            'Caver must be in Hell to receive the Nyan role.'
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_failure_embed_not_in_guild_other(role, user, guild_id, cache):
    """
    Tests whether ``build_failure_embed_not_in_guild_other`` works as intended.
    
    Parameters
    ----------
    role : ``Role``
        The role to check for.
    
    user : `ClientUserBase``
        The targeted user.
    
    guild_id : `int`
        The respective guild's identifier.
    
    cache : `None | list<object>`
        Additional objects to keep in cache.
    
    Returns
    -------
    output : ``Embed``
    """
    output = build_failure_embed_not_in_guild_other(role, user, guild_id)
    vampytest.assert_instance(output, Embed)
    return output
