import vampytest
from hata import Embed, GuildProfile, Role, User

from ..embed_builders import build_notification_embed_other


def _iter_options():
    role_id = 202502130040
    guild_id = 202502130041
    user_id = 202502130042
    
    user = User.precreate(user_id, name = 'Keine')
    user.guild_profiles[guild_id] = GuildProfile(nick = 'Caver')
    role = Role.precreate(role_id, name = 'Nyan', guild_id = guild_id)
    
    yield (
        role,
        user,
        0,
        Embed(
            'Love is in the air',
            f'You have been gifted the Nyan role by Keine.',
        ),
    )
    yield (
        role,
        user,
        guild_id,
        Embed(
            'Love is in the air',
            f'You have been gifted the Nyan role by Caver.',
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_notification_embed_other(role, user, guild_id):
    """
    Tests whether ``build_notification_embed_other`` works as intended.
    
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
    output = build_notification_embed_other(role, user, guild_id)
    vampytest.assert_instance(output, Embed)
    return output
