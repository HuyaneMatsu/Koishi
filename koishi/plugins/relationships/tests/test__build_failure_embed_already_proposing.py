import vampytest
from hata import Embed, GuildProfile, User

from ....bot_utils.constants import EMOJI__HEART_CURRENCY

from ..embed_builders import build_failure_embed_already_proposing
from ..relationship_types import RELATIONSHIP_TYPE_MAMA


def _iter_options():
    guild_id = 202412280003
    
    target_user = User.precreate(202412280004, name = 'Satori')
    target_user.guild_profiles[guild_id] = GuildProfile(nick = 'Sato')
    
    yield (
        RELATIONSHIP_TYPE_MAMA,
        1000,
        target_user,
        0,
        Embed(
            'You are already proposing',
            (
                f'You have already sent an adoption agreement towards Satori with 1000 {EMOJI__HEART_CURRENCY}.\n'
                f'Cancel the old proposal before reissuing a new one.'
            ),
        )
    )
    
    yield (
        RELATIONSHIP_TYPE_MAMA,
        1000,
        target_user,
        guild_id,
        Embed(
            'You are already proposing',
            (
                f'You have already sent an adoption agreement towards Sato with 1000 {EMOJI__HEART_CURRENCY}.\n'
                f'Cancel the old proposal before reissuing a new one.'
            ),
        )
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_failure_embed_already_proposing(relationship_type, investment, target_user, guild_id):
    """
    Tests whether ``build_failure_embed_already_proposing`` works as intended.
    
    Parameters
    ----------
    relationship_type : `int`
        The requested relation type.
    
    investment : `int`
        The amount of balance to propose with.
    
    target_user : ``ClientUserBase``
        The user who is the target of the proposal.
    
    guild_id : `int`
        The respective guild's identifier.
    
    Returns
    -------
    output : ``Embed``
    """
    output = build_failure_embed_already_proposing(relationship_type, investment, target_user, guild_id)
    vampytest.assert_instance(output, Embed)
    return output
