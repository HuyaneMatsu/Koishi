import vampytest
from hata import Embed, GuildProfile, User

from ....bot_utils.constants import EMOJI__HEART_CURRENCY

from ...relationships_core import RELATIONSHIP_TYPE_MAMA

from ..embed_builders import build_success_embed_request_rejected


def _iter_options():
    guild_id = 202412310002
    
    source_user = User.precreate(202412310003, name = 'Satori')
    source_user.guild_profiles[guild_id] = GuildProfile(nick = 'Sato')
    
    yield (
        RELATIONSHIP_TYPE_MAMA,
        1000,
        source_user,
        0,
        Embed(
            'Relationship request rejected',
            (
                f'You rejected Satori\'s adoption agreement.\n'
                f'Their 1000 {EMOJI__HEART_CURRENCY} investment have been refunded.'
            ),
        )
    )
    
    yield (
        RELATIONSHIP_TYPE_MAMA,
        1000,
        source_user,
        guild_id,
        Embed(
            'Relationship request rejected',
            (
                f'You rejected Sato\'s adoption agreement.\n'
                f'Their 1000 {EMOJI__HEART_CURRENCY} investment have been refunded.'
            ),
        )
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_success_embed_request_rejected(relationship_type, investment, source_user, guild_id):
    """
    Tests whether ``build_success_embed_request_rejected`` works as intended.
    
    Parameters
    ----------
    relationship_type : `int`
        The requested relation type.
    
    investment : `int`
        The amount of balance to propose with.
    
    source_user : ``ClientUserBase``
        The source use who is the source of the proposal.
    
    guild_id : `int`
        The respective guild's identifier.
    
    Returns
    -------
    output : ``Embed``
    """
    output = build_success_embed_request_rejected(relationship_type, investment, source_user, guild_id)
    vampytest.assert_instance(output, Embed)
    return output
