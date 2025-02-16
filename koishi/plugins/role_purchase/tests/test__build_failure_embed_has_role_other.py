import vampytest
from hata import Role, Embed, GuildProfile, User

from ..embed_builders import build_failure_embed_has_role_other


def _iter_options():
    role_id = 202502130000
    user_id = 202502130001
    guild_id = 202502130002
    
    user = User.precreate(user_id, name = 'Keine')
    user.guild_profiles[guild_id] = GuildProfile(nick = 'Caver', role_ids = [role_id])
    role = Role.precreate(role_id, name = 'Nyan', guild_id = guild_id)
    
    
    yield (
        role,
        user,
        0,
        Embed(
            'Suffering from success',
            'Keine already has the Nyan role.'
        ),
    )
    
    yield (
        role,
        user,
        guild_id,
        Embed(
            'Suffering from success',
            'Caver already has the Nyan role.'
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_failure_embed_has_role_other(role, user, guild_id):
    """
    Tests whether ``build_failure_embed_has_role_other`` works as intended.
    
    Parameters
    ----------
    role : ``Role``
        The role to check for.
    
    user : `ClientUserBase``
        The targeted user.
    
    guild_id : `int`
        The respective guild's identifier.
    
    Returns
    -------
    output : ``Embed``
    """
    output = build_failure_embed_has_role_other(role, user, guild_id)
    vampytest.assert_instance(output, Embed)
    return output
