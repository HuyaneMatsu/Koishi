import vampytest

from ..constants import ITEM_FLAG_NAME_DEFAULT
from ..flags import ITEM_FLAG_EDIBLE, ITEM_FLAG_WEAPON
from ..utils import produce_item_flags_with_names


def _iter_options():
    yield (
        1 << 63,
        ''.join([repr(1 << 63), ' (', ITEM_FLAG_NAME_DEFAULT, ')']),
    )
    
    yield (
        ITEM_FLAG_EDIBLE,
        ''.join([repr(ITEM_FLAG_EDIBLE), ' (', 'edible', ')']),
    )
    
    yield (
        ITEM_FLAG_EDIBLE | ITEM_FLAG_WEAPON,
        ''.join([repr(ITEM_FLAG_EDIBLE | ITEM_FLAG_WEAPON), ' (', 'edible', ' | ', 'weapon', ')']),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__produce_item_flags_with_names(item_flags):
    """
    Tests whether ``produce_item_flags_with_names`` works as intended.
    
    Parameters
    ----------
    item_flags : `int`
        Item's flags.
    
    Returns
    -------
    output : `str`
    """
    output = [*produce_item_flags_with_names(item_flags)]
    for element in output:
        vampytest.assert_instance(element, str)
    
    return ''.join(output)
