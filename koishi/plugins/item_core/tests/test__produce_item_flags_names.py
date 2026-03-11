import vampytest

from ..constants import ITEM_FLAG_NAME_DEFAULT
from ..flags import ITEM_FLAG_EDIBLE, ITEM_FLAG_WEAPON
from ..utils import produce_item_flags_names


def _iter_options():
    yield (
        1 << 63,
        ', ',
        ITEM_FLAG_NAME_DEFAULT,
    )
    
    yield (
        ITEM_FLAG_EDIBLE,
        ', ',
        'edible',
    )
    
    yield (
        ITEM_FLAG_EDIBLE | ITEM_FLAG_WEAPON,
        ', ',
        'edible, weapon',
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__produce_item_flags_names(item_flags, separator):
    """
    Tests whether ``produce_item_flags_names`` works as intended.
    
    Parameters
    ----------
    item_flags : `int`
        Item's flags.
    
    separator : `str`
        Separator to use.
    
    Returns
    -------
    output : `str`
    """
    output = [*produce_item_flags_names(item_flags, separator)]
    for element in output:
        vampytest.assert_instance(element, str)
    
    return ''.join(output)
