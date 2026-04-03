import vampytest

from ..constants import ITEM_NAME_DEFAULT
from ..item_ids import ITEM_ID_GARLIC
from ..utils import get_item_name


def _iter_options():
    yield -1, ITEM_NAME_DEFAULT
    yield ITEM_ID_GARLIC, 'Garlic'


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__get_item_name(item_id):
    """
    Tests whether ``get_item_name`` works as intended.
    
    Parameters
    ----------
    item_id : `int`
        Item identifier to test with.
    
    Returns
    -------
    output : `str`
    """
    output = get_item_name(item_id)
    vampytest.assert_instance(output, str)
    return output
