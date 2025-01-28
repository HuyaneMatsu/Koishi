import vampytest
from hata import Embed, GuildProfile, User

from ..embed_builders import build_failure_embed_max_relationship_slots_other


def _iter_options():
    user_id = 202501260006
    guild_id = 202501260007
    
    user = User.precreate(user_id, name = 'Keine')
    user.guild_profiles[guild_id] = GuildProfile(nick = 'Caver')
    
    yield (
        user,
        0,
        Embed(
            'Suffering from success',
            'Keine reached their maximum amount of relationship slots.',
        ),
    )
    
    yield (
        user,
        guild_id,
        Embed(
            'Suffering from success',
            'Caver reached their maximum amount of relationship slots.',
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_failure_embed_max_relationship_slots_other(user, guild_id):
    """
    Tests whether ``build_failure_embed_max_relationship_slots_other`` works as intended.
    
    Parameters
    ----------
    user : `ClientUserBase``
        The targeted user.
    
    guild_id : `int`
        The respective guild's identifier.
    
    Returns
    -------
    output : ``Embed``
    """
    output = build_failure_embed_max_relationship_slots_other(user, guild_id)
    vampytest.assert_instance(output, Embed)
    return output
