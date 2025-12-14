import vampytest
from hata import User

from ..content_building import produce_buy_relationship_slot_notification_description


def _iter_options():
    user = User.precreate(
        202511300012,
        name = 'Satori',
    )
    
    yield (
        5,
        user,
        0,
        (
            f'Satori gifted you your 5th relationship slot.'
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__produce_buy_relationship_slot_notification_description(
    new_relationship_slot_count,
    source_user,
    guild_id,
):
    """
    Tests whether ``produce_buy_relationship_slot_notification_description`` works as intended.
    
    Parameters
    ----------
    new_relationship_slot_count : `int`
        The relationship slot count after purchase.
    
    source_user : `ClientUserBase``
        The purchasing user.
    
    guild_id : `int`
        The respective guild's identifier.
    
    Returns
    -------
    output : `str`
    """
    output = [*produce_buy_relationship_slot_notification_description(
        new_relationship_slot_count,
        source_user,
        guild_id,
    )]
    
    for element in output:
        vampytest.assert_instance(element, str)
    
    return ''.join(output)
