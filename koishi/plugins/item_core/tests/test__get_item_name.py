import vampytest

from ..item_ids import ITEM_ID_GARLIC
from ..utils import get_item_name


def _iter_options():
    yield -1
    yield ITEM_ID_GARLIC


@vampytest._(vampytest.call_from(_iter_options()))
def test__get_item_name(item_id):
    """
    Tests whether ``get_item_name`` works as intended.
    
    Parameters
    ----------
    item_id : `int`
        Item identifier to test with.
    """
    output = get_item_name(item_id)
    vampytest.assert_instance(output, str)
