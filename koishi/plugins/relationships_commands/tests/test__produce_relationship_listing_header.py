import vampytest

from hata import User

from ..constants import RELATIONSHIP_LISTING_MODE_LEGACY
from ..content_building import produce_relationship_listing_header


def _iter_options():
    user_id = 202501240000
    user = User.precreate(
        user_id,
        name = 'Satori',
    )
    
    yield (
        user,
        0,
        100,
        1,
        2,
        0,
        0,
        RELATIONSHIP_LISTING_MODE_LEGACY,
        2,
        (
            '# Satori\'s relationship info\n'
            '\n'
            'Listing mode: legacy; Page: 3\n'
            'Value: 110 - 210; Break-ups: 1; Slots: 0 / 2'
        ),
    )
    
    yield (
        user,
        0,
        100,
        1,
        2,
        1,
        1,
        RELATIONSHIP_LISTING_MODE_LEGACY,
        2,
        (
            '# Satori\'s relationship info\n'
            '\n'
            'Listing mode: legacy; Page: 3\n'
            'Value: 110 - 210; Break-ups: 1; Slots: 2 (1 + 1) / 2'
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__produce_relationship_listing_header(
    target_user,
    guild_id,
    relationship_value,
    relationship_divorces,
    relationship_slots,
    relationship_count,
    relationship_proposal_count,
    relationship_listing_mode,
    page_index,
):
    """
    Tests whether ``produce_relationship_listing_header`` works as intended.
    
    Parameters
    ----------
    target_user : ``ClientUserBase``
        The user, who's relationships are shown.
    
    guild_id : `int`
        The local guild's identifier.
    
    relationship_value : `int`
        The targeted user's relationships value.
    
    relationship_divorces : `int`
        The targeted user's break up count.
    
    relationship_slots : `int`
        The targeted user's relationship slot count.
    
    relationship_count : `int`
        The amount of relationships the targeted user has.
    
    relationship_proposal_count : `int`
        The amount of outgoing proposals the targeted user has.
    
    relationship_listing_mode : `int`
        The mode to render as.
    
    page_index : `int`
        The displayed page's index.
    
    Returns
    -------
    output : `str`
    """
    output = [*produce_relationship_listing_header(
        target_user,
        guild_id,
        relationship_value,
        relationship_divorces,
        relationship_slots,
        relationship_count,
        relationship_proposal_count,
        relationship_listing_mode,
        page_index,
    )]
    
    for element in output:
        vampytest.assert_instance(element, str)
    
    return ''.join(output)
