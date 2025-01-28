import vampytest
from hata import Embed, GuildProfile, User

from ..embed_builders import build_failure_embed_cannot_divorce_not_related_anymore


def _iter_options():
    guild_id = 202501050006
    
    target_user = User.precreate(202501050007, name = 'Satori')
    target_user.guild_profiles[guild_id] = GuildProfile(nick = 'Sato')
    
    yield (
        target_user,
        0,
        Embed(
            'Divorcing cannot be confirmed',
            'You are not related to Satori anymore.'
        )
    )
    
    yield (
        target_user,
        guild_id,
        Embed(
            'Divorcing cannot be confirmed',
            'You are not related to Sato anymore.'
        )
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_failure_embed_cannot_divorce_not_related_anymore(target_user, guild_id):
    """
    Tests whether ``build_failure_embed_cannot_divorce_not_related_anymore`` works as intended.
    
    Parameters
    ----------
    target_user : ``ClientUserBase``
        The user who is the target of the proposal.
    
    guild_id : `int`
        The respective guild's identifier.
    
    Returns
    -------
    output : ``Embed``
    """
    output = build_failure_embed_cannot_divorce_not_related_anymore(target_user, guild_id)
    vampytest.assert_instance(output, Embed)
    return output
