import vampytest

from ..constants import ITEM_GROUP_NAME_DEFAULT
from ..item_group_ids import ITEM_GROUP_ID_KNIFE
from ..utils import produce_item_group_id_with_name


def _iter_options():
    yield (
        1 << 63,
        ''.join([repr(1 << 63), ' (', ITEM_GROUP_NAME_DEFAULT, ')']),
    )
    
    yield (
        ITEM_GROUP_ID_KNIFE,
        ''.join([repr(ITEM_GROUP_ID_KNIFE), ' (', 'knife', ')']),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__produce_item_group_id_with_name(item_group_id):
    """
    Tests whether ``produce_item_group_id_with_name`` works as intended.
    
    Parameters
    ----------
    item_group_id : `int`
        Item group identifier.
    
    Returns
    -------
    output : `str`
    """
    output = [*produce_item_group_id_with_name(item_group_id)]
    for element in output:
        vampytest.assert_instance(element, str)
    
    return ''.join(output)
