import vampytest
from hata import Embed, GuildProfile, User

from ..embed_builders import build_question_embed_divorce


def _iter_options():
    guild_id = 202501050000
    
    target_user = User.precreate(202501050001, name = 'Satori')
    target_user.guild_profiles[guild_id] = GuildProfile(nick = 'Sato')
    
    yield (
        target_user,
        0,
        Embed(
            'Divorcing',
            f'Are you sure to divorce Satori?',
        )
    )
    
    yield (
        target_user,
        guild_id,
        Embed(
            'Divorcing',
            f'Are you sure to divorce Sato?',
        )
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_question_embed_divorce(target_user, guild_id):
    """
    Tests whether ``build_question_embed_divorce`` works as intended.
    
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
    output = build_question_embed_divorce(target_user, guild_id)
    vampytest.assert_instance(output, Embed)
    return output
