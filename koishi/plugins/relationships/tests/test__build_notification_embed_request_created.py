import vampytest
from hata import Embed, GuildProfile, User

from ....bot_utils.constants import EMOJI__HEART_CURRENCY

from ..embed_builders import build_notification_embed_request_created
from ..relationship_types import RELATIONSHIP_TYPE_MAMA


def _iter_options():
    guild_id = 202412290006
    
    source_user = User.precreate(202412290007, name = 'Satori')
    source_user.guild_profiles[guild_id] = GuildProfile(nick = 'Sato')
    
    yield (
        RELATIONSHIP_TYPE_MAMA,
        1000,
        source_user,
        0,
        Embed(
            'You received a proposal',
            (
                f'Satori wants to adopt you.\n'
                f'They are proposing with 1000 {EMOJI__HEART_CURRENCY}.'
            ),
        )
    )
    
    yield (
        RELATIONSHIP_TYPE_MAMA,
        1000,
        source_user,
        guild_id,
        Embed(
            'You received a proposal',
            (
                f'Sato wants to adopt you.\n'
                f'They are proposing with 1000 {EMOJI__HEART_CURRENCY}.'
            ),
        )
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_notification_embed_request_created(relationship_type, investment, source_user, guild_id):
    """
    Tests whether ``build_notification_embed_request_created`` works as intended.
    
    Parameters
    ----------
    relationship_type : `int`
        The requested relation type.
    
    investment : `int`
        The amount of balance to propose with.
    
    source_user : ``ClientUserBase``
        The user who is the source of the proposal.
    
    guild_id : `int`
        The respective guild's identifier.
    
    Returns
    -------
    output : ``Embed``
    """
    output = build_notification_embed_request_created(relationship_type, investment, source_user, guild_id)
    vampytest.assert_instance(output, Embed)
    return output
