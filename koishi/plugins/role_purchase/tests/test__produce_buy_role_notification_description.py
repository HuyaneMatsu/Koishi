import vampytest
from hata import User

from ....bot_utils.constants import ROLE__SUPPORT__ELEVATED

from ..content_building import produce_buy_role_notification_description


def _iter_options():
    user = User.precreate(
        202512030022,
        name = 'Satori',
    )
    
    yield (
        ROLE__SUPPORT__ELEVATED,
        user,
        0,
        (
            f'Satori gifted you {ROLE__SUPPORT__ELEVATED.name} role.'
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__produce_buy_role_notification_description(
    role,
    source_user,
    guild_id,
):
    """
    Tests whether ``produce_buy_role_notification_description`` works as intended.
    
    Parameters
    ----------
    role : ``Role``
        The role to be purchased.
    
    source_user : `ClientUserBase``
        The purchasing user.
    
    guild_id : `int`
        The respective guild's identifier.
    
    Returns
    -------
    output : `str`
    """
    output = [*produce_buy_role_notification_description(
        role,
        source_user,
        guild_id,
    )]
    
    for element in output:
        vampytest.assert_instance(element, str)
    
    return ''.join(output)
