import vampytest

from ...item_core import ITEM_FLAG_COSTUME, ITEM_FLAG_EDIBLE, ITEM_ID_PEACH, Item, get_item

from ..item_name_auto_completion import get_best_matching_item


def _iter_options():
    yield (
        0,
        None,
        None,
    )
    yield (
        0,
        'peach',
        get_item(ITEM_ID_PEACH),
    )
    yield (
        0,
        format(ITEM_ID_PEACH, 'x'),
        get_item(ITEM_ID_PEACH),
    )
    yield (
        ITEM_FLAG_EDIBLE,
        None,
        None,
    )
    yield (
        ITEM_FLAG_EDIBLE,
        'peach',
        get_item(ITEM_ID_PEACH),
    )
    yield (
        ITEM_FLAG_EDIBLE,
        format(ITEM_ID_PEACH, 'x'),
        get_item(ITEM_ID_PEACH),
    )
    yield (
        ITEM_FLAG_COSTUME,
        None,
        None,
    )
    yield (
        ITEM_FLAG_COSTUME,
        'peach',
        None,
    )
    yield (
        ITEM_FLAG_COSTUME,
        format(ITEM_ID_PEACH, 'x'),
        None,
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__get_best_matching_item(required_flags, value):
    """
    Tests whether ``get_best_matching_item`` works as intended.
    
    Parameters
    ----------
    required_flags : `int`
        Flags the item should have.
    
    value : `None | str`
        Value the user typed.
    
    Returns
    -------
    output : ``None | Item``
    """
    output = get_best_matching_item(required_flags, value)
    vampytest.assert_instance(output, Item, nullable = True)
    return output
