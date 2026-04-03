import vampytest

from ...inventory_core import ItemEntry
from ...item_core import ITEM_ID_PEACH, get_item_nullable
from ...quest_core import AMOUNT_TYPE_COUNT, AMOUNT_TYPE_WEIGHT

from ..content_building import produce_linked_quest_submission_item_select_description


def _iter_options():
    item_peach = get_item_nullable(ITEM_ID_PEACH)
    assert item_peach is not None
    
    yield (
        ItemEntry(
            item_peach,
            20,
        ),
        AMOUNT_TYPE_COUNT,
        f'20 {item_peach.emoji} {item_peach.name}',
    )
    
    yield (
        ItemEntry(
            item_peach,
            20,
        ),
        AMOUNT_TYPE_WEIGHT,
        f'20 {item_peach.emoji} {item_peach.name} ({20 * 216 / 1000} kg)',
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__produce_linked_quest_submission_item_select_description(item_entry, amount_type):
    """
    Produces a submission requirements entry's description.
    
    Parameters
    ----------
    item_entry : ``ItemEntry``
        Item entry to build description for.
    
    amount_type : `int`
        The type of the amount.
    
    Returns
    -------
    output : `str`
    """
    output = [*produce_linked_quest_submission_item_select_description(item_entry, amount_type)]
    
    for element in output:
        vampytest.assert_instance(element, str)
    
    return ''.join(output)
