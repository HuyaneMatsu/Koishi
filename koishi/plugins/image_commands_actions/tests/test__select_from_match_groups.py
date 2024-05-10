import vampytest

from ...image_handling_core import WEIGHT_DIRECT_MATCH, ImageDetailStatic
from ...touhou_core import KOMEIJI_KOISHI, KOMEIJI_SATORI

from ..character_preference import select_from_match_groups


def _iter_options():
    image_detail_0 = ImageDetailStatic(
        'https://orindance.party/',
    ).with_action(
        'kiss', KOMEIJI_KOISHI, KOMEIJI_SATORI,
    )
    
    image_detail_1 = ImageDetailStatic(
        'https://orindance.party/'
    ).with_action(
        'kiss', KOMEIJI_SATORI, KOMEIJI_KOISHI,
    )
    
    yield (
        {},
        None,
    )
    
    yield (
        {
            WEIGHT_DIRECT_MATCH + WEIGHT_DIRECT_MATCH: [image_detail_0],
            WEIGHT_DIRECT_MATCH + 0: [image_detail_1],
        },
        image_detail_1,
    )
    
    yield (
        {
            WEIGHT_DIRECT_MATCH + WEIGHT_DIRECT_MATCH: [image_detail_1],
            WEIGHT_DIRECT_MATCH + 0: [image_detail_0],
        },
        image_detail_0,
    )
    yield (
        {
            WEIGHT_DIRECT_MATCH + WEIGHT_DIRECT_MATCH: [image_detail_0],
        },
        image_detail_0,
    )
    
    yield (
        {
            WEIGHT_DIRECT_MATCH + 0: [image_detail_1],
        },
        image_detail_1,
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__select_from_match_groups(match_groups):
    """
    Tests whether ``select_from_match_groups`` works as intended.
    
    Parameters
    ----------
    match_groups_by_weight : `dict<int, list<ImageDetailBase>>`
        Matched image details by weight.
    
    Returns
    -------
    output : `None | ImageDetailBase`
    """
    mocked = vampytest.mock_globals(
        select_from_match_groups,
        OPTIMAL_GROUP_LENGTH = 1,
    )
    
    return mocked(match_groups)
