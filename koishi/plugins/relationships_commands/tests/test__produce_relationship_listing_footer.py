import vampytest

from hata import User

from ....bot_utils.constants import EMOJI__HEART_CURRENCY

from ..content_building import produce_relationship_listing_footer


def _iter_options():
    user_id_0 = 202501240000
    user_id_1 = 202501240000
    
    user_0 = User.precreate(
        user_id_0,
        name = 'Satori',
    )
    
    user_1 = User.precreate(
        user_id_1,
        name = 'Koishi',
    )
    
    yield (
        user_0,
        user_1,
        0,
        100,
        (
            f'To propose to Koishi you need at least 210 {EMOJI__HEART_CURRENCY}.'
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__produce_relationship_listing_footer(
    source_user,
    target_user,
    guild_id,
    relationship_value,
):
    """
    Tests whether ``produce_relationship_listing_footer`` works as intended.
    
    Parameters
    ----------
    target_user : ``ClientUserBase``
        The user, who's relationships are shown.
    
    guild_id : `int`
        The local guild's identifier.
    
    relationship_value : `int`
        The targeted user's relationships value.
    
    Returns
    -------
    output : `str`
    """
    output = [*produce_relationship_listing_footer(
        source_user,
        target_user,
        guild_id,
        relationship_value,
    )]
    
    for element in output:
        vampytest.assert_instance(element, str)
    
    return ''.join(output)
