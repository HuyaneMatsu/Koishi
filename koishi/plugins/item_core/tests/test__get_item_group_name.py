import vampytest

from ..constants import ITEM_GROUP_NAME_DEFAULT
from ..item_group_ids import ITEM_GROUP_ID_KNIFE
from ..utils import get_item_group_name


def _iter_options():
    yield -1, ITEM_GROUP_NAME_DEFAULT
    yield ITEM_GROUP_ID_KNIFE, 'knife'


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__get_item_group_name(item_group_id):
    """
    Tests whether ``get_item_group_name`` works as intended.
    
    Parameters
    ----------
    item_group_id : `int`
        Item identifier to test with.
    
    Returns
    -------
    output : `str`
    """
    output = get_item_group_name(item_group_id)
    vampytest.assert_instance(output, str)
    return output
