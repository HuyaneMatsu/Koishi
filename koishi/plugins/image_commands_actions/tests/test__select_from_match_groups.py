import vampytest

from ...image_handling_core import ImageDetail
from ...touhou_core import KOMEIJI_KOISHI, KOMEIJI_SATORI

from ..character_preference import select_from_match_groups


def _iter_options():
    image_detail_0 = ImageDetail('https://orindance.party/').with_source(KOMEIJI_KOISHI).with_target(KOMEIJI_SATORI)
    image_detail_1 = ImageDetail('https://orindance.party/').with_source(KOMEIJI_SATORI).with_target(KOMEIJI_KOISHI)
    
    yield ([], []), None
    yield ([image_detail_0], [image_detail_1]), image_detail_1
    yield ([image_detail_1], [image_detail_0]), image_detail_0
    yield ([image_detail_0], []), image_detail_0
    yield ([], [image_detail_1]), image_detail_1


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__select_from_match_groups(match_groups):
    """
    Tests whether ``select_from_match_groups`` works as intended.
    
    Parameters
    ----------
    match_groups : `tuple<list<ImageDetail>>`
        A tuple of image details.
    
    Returns
    -------
    output : `None | ImageDetail`
    """
    mocked = vampytest.mock_globals(
        select_from_match_groups,
        OPTIMAL_GROUP_LENGTH = 1,
    )
    
    return mocked(match_groups)
