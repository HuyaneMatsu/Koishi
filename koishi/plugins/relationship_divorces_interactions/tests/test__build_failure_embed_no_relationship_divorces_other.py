import vampytest
from hata import Embed, GuildProfile, User

from ..embed_builders import build_failure_embed_no_relationship_divorces_other


def _iter_options():
    user_id = 202502050002
    guild_id = 202502050003
    
    user = User.precreate(user_id, name = 'Keine')
    user.guild_profiles[guild_id] = GuildProfile(nick = 'Caver')
    
    yield (
        user,
        0,
        Embed(
            'Suffering from success',
            'Keine has no divorces.',
        ),
    )
    
    yield (
        user,
        guild_id,
        Embed(
            'Suffering from success',
            'Caver has no divorces.',
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_failure_embed_no_relationship_divorces_other(user, guild_id):
    """
    Tests whether ``build_failure_embed_no_relationship_divorces_other`` works as intended.
    
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
    output = build_failure_embed_no_relationship_divorces_other(user, guild_id)
    vampytest.assert_instance(output, Embed)
    return output
