import vampytest

from ...item_core import ITEM_ID_PEACH, get_item_nullable
from ...quest_core import AMOUNT_TYPE_COUNT, AMOUNT_TYPE_WEIGHT, QUEST_REQUIREMENT_TYPE_ITEM_EXACT

from ..content_building import produce_linked_quest_submission_requirements_entry_description


def _iter_options():
    item_peach = get_item_nullable(ITEM_ID_PEACH)
    assert item_peach is not None
    
    yield (
        (
            QUEST_REQUIREMENT_TYPE_ITEM_EXACT,
            item_peach.id,
            AMOUNT_TYPE_COUNT,
            100,
            20,
        ),
        0,
        0,
        0,
        f'20 / 100 {item_peach.emoji} {item_peach.name}, none on stock',
    )
    
    yield (
        (
            QUEST_REQUIREMENT_TYPE_ITEM_EXACT,
            item_peach.id,
            AMOUNT_TYPE_COUNT,
            100,
            20,
        ),
        20,
        100,
        100,
        f'20 / 100 {item_peach.emoji} {item_peach.name}, 20 on stock',
    )
    
    yield (
        (
            QUEST_REQUIREMENT_TYPE_ITEM_EXACT,
            item_peach.id,
            AMOUNT_TYPE_WEIGHT,
            1000,
            200,
        ),
        20,
        1000,
        1000,
        f'0.2 / 1 kg {item_peach.emoji} {item_peach.name}, 20 on stock (1 kg)',
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__produce_linked_quest_submission_requirements_entry_description(
    submission_requirement_normalised, accumulated_amount, accumulated_weight, accumulated_value
):
    """
    Produces a submission requirements entry's description.
    
    Parameters
    ----------
    submission_requirement_normalised : `(int, int, int, int, int)`
        Normalised requirement to produce.
    
    accumulated_amount : `int`
        The amount of items the user has that satisfies the requirement.
    
    accumulated_weight : `int`
        The weight of items the user has that satisfies the requirement.
    
    accumulated_value : `int`
        The value of items the user has that satisfies the requirement.
    
    Returns
    -------
    output : `str`
    """
    output = [*produce_linked_quest_submission_requirements_entry_description(
        submission_requirement_normalised, accumulated_amount, accumulated_weight, accumulated_value
    )]
    
    for element in output:
        vampytest.assert_instance(element, str)
    
    return ''.join(output)
