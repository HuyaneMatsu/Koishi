import vampytest
from hata import User

from ..content_building import produce_burn_divorce_papers_notification_description


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
            f'Satori hired ninjas to locate and burn your 5th divorce papers.'
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__produce_burn_divorce_papers_notification_description(
    relationship_divorces,
    source_user,
    guild_id,
):
    """
    Tests whether ``produce_burn_divorce_papers_notification_description`` works as intended.
    
    Parameters
    ----------
    relationship_divorces : `int`
        The amount of divorces the user has.
    
    source_user : `ClientUserBase``
        The purchasing user.
    
    guild_id : `int`
        The respective guild's identifier.
    
    Returns
    -------
    output : `str`
    """
    output = [*produce_burn_divorce_papers_notification_description(
        relationship_divorces,
        source_user,
        guild_id,
    )]
    
    for element in output:
        vampytest.assert_instance(element, str)
    
    return ''.join(output)
