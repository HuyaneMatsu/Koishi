import vampytest

from ..constants import PREFERRED_IMAGE_SOURCE_NONE, PREFERRED_IMAGE_SOURCE_TOUHOU
from ..utils import is_preferred_image_source_weight_map_valuable


def _iter_options():
    yield {}, False
    yield {PREFERRED_IMAGE_SOURCE_NONE: 1.0}, False
    yield {PREFERRED_IMAGE_SOURCE_TOUHOU: 1.0}, True
    yield {PREFERRED_IMAGE_SOURCE_NONE: 1.0, PREFERRED_IMAGE_SOURCE_TOUHOU: 1.0}, True


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__is_preferred_image_source_weight_map_valuable(weight_map):
    """
    Tests whether ``is_preferred_image_source_weight_map_valuable`` works as intended.
    
    Parameters
    ----------
    preferred_image_source_weight_map : `dict<int, int>`
        Weight map.
    
    Returns
    -------
    output : `bool`
    """
    output = is_preferred_image_source_weight_map_valuable(weight_map)
    vampytest.assert_instance(output, int)
    return True if output else False
