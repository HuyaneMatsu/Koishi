import vampytest
from hata import Embed, GuildProfile, User

from ....bot_utils.constants import EMOJI__HEART_CURRENCY

from ...relationships_core import RELATIONSHIP_TYPE_MAMA

from ..embed_builders import build_notification_embed_request_accepted


def _iter_options():
    guild_id = 202412300000
    
    target_user = User.precreate(202412300001, name = 'Satori')
    target_user.guild_profiles[guild_id] = GuildProfile(nick = 'Sato')
    
    yield (
        RELATIONSHIP_TYPE_MAMA,
        1000,
        target_user,
        0,
        Embed(
            'Your proposal has been accepted',
            (
                f'Satori is now your daughter.\n'
                f'Now you are mama and daughter.\n'
                f'They received half of your investment (500 {EMOJI__HEART_CURRENCY}).'
            ),
        )
    )
    
    yield (
        RELATIONSHIP_TYPE_MAMA,
        1000,
        target_user,
        guild_id,
        Embed(
            'Your proposal has been accepted',
            (
                f'Sato is now your daughter.\n'
                f'Now you are mama and daughter.\n'
                f'They received half of your investment (500 {EMOJI__HEART_CURRENCY}).'
            ),
        )
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_notification_embed_request_accepted(relationship_type, investment, target_user, guild_id):
    """
    Tests whether ``build_notification_embed_request_accepted`` works as intended.
    
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
    output = build_notification_embed_request_accepted(relationship_type, investment, target_user, guild_id)
    vampytest.assert_instance(output, Embed)
    return output
