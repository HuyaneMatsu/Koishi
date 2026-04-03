import vampytest

from ...item_core import ITEM_ID_CARROT, get_item_nullable
from ...quest_core import AMOUNT_TYPE_COUNT, AMOUNT_TYPE_VALUE, AMOUNT_TYPE_WEIGHT

from ..helpers import get_submit_amount


def _iter_options():
    item_id = ITEM_ID_CARROT
    item = get_item_nullable(item_id)
    assert item is not None
    
    # count -> under
    yield (
        item,
        AMOUNT_TYPE_COUNT,
        100,
        50,
        (
            50,
            50,
        )
    )
    
    # count -> exact
    yield (
        item,
        AMOUNT_TYPE_COUNT,
        100,
        100,
        (
            100,
            100,
        )
    )
    
    # count -> over
    yield (
        item,
        AMOUNT_TYPE_COUNT,
        100,
        120,
        (
            100,
            100,
        )
    )
    
    # weight -> under
    yield (
        item,
        AMOUNT_TYPE_WEIGHT,
        100 * item.weight,
        50,
        (
            50 * item.weight,
            50,
        )
    )
    
    # weight -> exact
    yield (
        item,
        AMOUNT_TYPE_WEIGHT,
        100 * item.weight,
        100,
        (
            100 * item.weight,
            100,
        )
    )
    
    # weight -> over
    yield (
        item,
        AMOUNT_TYPE_WEIGHT,
        100 * item.weight,
        120,
        (
            100 * item.weight,
            100,
        )
    )
    
    # weight -> over (required is diverged from exact)
    yield (
        item,
        AMOUNT_TYPE_WEIGHT,
        100 * item.weight - 1,
        120,
        (
            100 * item.weight,
            100,
        )
    )
    
    # value -> under
    yield (
        item,
        AMOUNT_TYPE_VALUE,
        100 * item.value,
        50,
        (
            50 * item.value,
            50,
        )
    )
    
    # value -> exact
    yield (
        item,
        AMOUNT_TYPE_VALUE,
        100 * item.value,
        100,
        (
            100 * item.value,
            100,
        )
    )
    
    # value -> over
    yield (
        item,
        AMOUNT_TYPE_VALUE,
        100 * item.value,
        120,
        (
            100 * item.value,
            100,
        )
    )
    
    # value -> over (required is diverged from exact)
    yield (
        item,
        AMOUNT_TYPE_VALUE,
        100 * item.value - 1,
        120,
        (
            100 * item.value,
            100,
        )
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__get_submit_amount(item, amount_type, amount_to_be_used, current_amount_count):
    """
    Tests whether ``get_submit_amount`` works as intended.
    
    Parameters
    ----------
    item : ``Item``
        The item submitted.
    
    amount_type : `int`
        In what format the item is required.
    
    amount_to_be_used : `int`
        Up to how much amount can be used.
    
    current_amount_count : `int`
        The amount of `item`-s owned and possible to be submitted.
    
    Returns
    -------
    output : ``None | LinkedQuest``
    """
    output = get_submit_amount(item, amount_type, amount_to_be_used, current_amount_count)
    vampytest.assert_instance(output, tuple)
    vampytest.assert_eq(len(output), 2)
    vampytest.assert_instance(output[0], int)
    vampytest.assert_instance(output[1], int)
    return output
