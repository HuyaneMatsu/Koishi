import vampytest
from hata import Embed, GuildProfile, User

from ..embed_builders import build_success_embed_divorce_cancelled


def _iter_options():
    guild_id = 202501050002
    
    target_user = User.precreate(202501050003, name = 'Satori')
    target_user.guild_profiles[guild_id] = GuildProfile(nick = 'Sato')
    
    yield (
        target_user,
        0,
        Embed(
            'Divorcing cancelled',
            'You cancelled divorcing Satori.',
        )
    )
    
    yield (
        target_user,
        guild_id,
        Embed(
            'Divorcing cancelled',
            'You cancelled divorcing Sato.',
        )
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_success_embed_divorce_cancelled(target_user, guild_id):
    """
    Tests whether ``build_success_embed_divorce_cancelled`` works as intended.
    
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
    output = build_success_embed_divorce_cancelled(target_user, guild_id)
    vampytest.assert_instance(output, Embed)
    return output
