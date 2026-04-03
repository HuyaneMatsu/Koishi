import vampytest
from hata import User

from ....bot_utils.constants import EMOJI__HEART_CURRENCY

from ...relationships_core import RELATIONSHIP_TYPE_MAMA

from ..content_building import produce_relationship_request_cancelled_description


def _iter_options():
    target_user = User.precreate(20241231005, name = 'Satori')
    
    yield (
        RELATIONSHIP_TYPE_MAMA,
        1000,
        target_user,
        0,
        (
            f'You cancelled your adoption agreement towards Satori.\n'
            f'Your 1000 {EMOJI__HEART_CURRENCY} investment have been unallocated.'
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__produce_relationship_request_cancelled_description(relationship_type, investment, target_user, guild_id):
    """
    Tests whether ``produce_relationship_request_cancelled_description`` works as intended.
    
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
    output : `str`
    """
    output = [*produce_relationship_request_cancelled_description(relationship_type, investment, target_user, guild_id)]
    
    for element in output:
        vampytest.assert_instance(element, str)
    
    return ''.join(output)
