import vampytest
from hata import Embed, GuildProfile, User

from ....bot_utils.constants import EMOJI__HEART_CURRENCY

from ...relationships_core import RELATIONSHIP_TYPE_MAMA

from ..embed_builders import build_success_embed_request_cancelled


def _iter_options():
    guild_id = 202412310004
    
    target_user = User.precreate(20241231005, name = 'Satori')
    target_user.guild_profiles[guild_id] = GuildProfile(nick = 'Sato')
    
    yield (
        RELATIONSHIP_TYPE_MAMA,
        1000,
        target_user,
        0,
        Embed(
            'Relationship request cancelled',
            (
                f'You cancelled your adoption agreement towards Satori.\n'
                f'Your 1000 {EMOJI__HEART_CURRENCY} investment have been refunded.'
            ),
        )
    )
    
    yield (
        RELATIONSHIP_TYPE_MAMA,
        1000,
        target_user,
        guild_id,
        Embed(
            'Relationship request cancelled',
            (
                f'You cancelled your adoption agreement towards Sato.\n'
                f'Your 1000 {EMOJI__HEART_CURRENCY} investment have been refunded.'
            ),
        )
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_success_embed_request_cancelled(relationship_type, investment, target_user, guild_id):
    """
    Tests whether ``build_success_embed_request_cancelled`` works as intended.
    
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
    output = build_success_embed_request_cancelled(relationship_type, investment, target_user, guild_id)
    vampytest.assert_instance(output, Embed)
    return output
