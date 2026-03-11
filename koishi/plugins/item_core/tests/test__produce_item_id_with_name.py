import vampytest

from ..constants import ITEM_NAME_DEFAULT
from ..item_ids import ITEM_ID_GARLIC
from ..utils import produce_item_id_with_name


def _iter_options():
    yield (
        1 << 63,
        ''.join([repr(1 << 63), ' (', ITEM_NAME_DEFAULT, ')']),
    )
    
    yield (
        ITEM_ID_GARLIC,
        ''.join([repr(ITEM_ID_GARLIC), ' (', 'Garlic', ')']),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__produce_item_id_with_name(item_id):
    """
    Tests whether ``produce_item_id_with_name`` works as intended.
    
    Parameters
    ----------
    item_id : `int`
        Item identifier.
    
    Returns
    -------
    output : `str`
    """
    output = [*produce_item_id_with_name(item_id)]
    for element in output:
        vampytest.assert_instance(element, str)
    
    return ''.join(output)
