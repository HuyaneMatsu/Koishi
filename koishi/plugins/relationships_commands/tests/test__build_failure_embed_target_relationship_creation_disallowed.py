import vampytest
from hata import Embed, GuildProfile, User

from ..embed_builders import build_failure_embed_target_relationship_creation_disallowed


def _iter_options():
    guild_id = 202501100003
    
    user = User.precreate(202501100004, name = 'Satori')
    user.guild_profiles[guild_id] = GuildProfile(nick = 'Sato')
    
    yield (
        user,
        0,
        Embed(
            'Target relationship creation disallowed',
            (
                'Satori is disallowed to create relationships.\n'
                'Therefore creating a proposal towards them is not allowed.'
            ),
        )
    )
    
    yield (
        user,
        guild_id,
        Embed(
            'Target relationship creation disallowed',
            (
                'Sato is disallowed to create relationships.\n'
                'Therefore creating a proposal towards them is not allowed.'
            ),
        )
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_failure_embed_target_relationship_creation_disallowed(target_user, guild_id):
    """
    Tests whether ``build_failure_embed_target_relationship_creation_disallowed`` works as intended.
    
    Parameters
    ----------
    target_user : ``ClientUserBase``
        The targeted user.
    
    guild_id : `int`
        The respective guild's identifier.
    
    Returns
    -------
    output : ``Embed``
    """
    output = build_failure_embed_target_relationship_creation_disallowed(target_user, guild_id)
    vampytest.assert_instance(output, Embed)
    return output
