import vampytest
from hata import User

from ....bot_utils.constants import EMOJI__HEART_CURRENCY

from ...relationships_core import RELATIONSHIP_TYPE_MAMA

from ..content_building import produce_relationship_request_cancellation_notification_description


def _iter_options():
    source_user = User.precreate(202412300007, name = 'Satori')
    
    yield (
        RELATIONSHIP_TYPE_MAMA,
        1000,
        source_user,
        0,
        (
            f'Satori cancelled their adoption agreement towards you, '
            f'with investment of 1000 {EMOJI__HEART_CURRENCY}.'
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__produce_relationship_request_cancellation_notification_description(
    relationship_type, investment, source_user, guild_id
):
    """
    Tests whether ``produce_relationship_request_cancellation_notification_description`` works as intended.
    
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
    output : `str`
    """
    output = [*produce_relationship_request_cancellation_notification_description(
        relationship_type, investment, source_user, guild_id
    )]
    
    for element in output:
        vampytest.assert_instance(element, str)
    
    return ''.join(output)
