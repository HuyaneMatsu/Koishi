import vampytest

from ....bot_utils.constants import EMOJI__HEART_CURRENCY

from ...item_core import ITEM_ID_PEACH, get_item_nullable
from ...quest_core import AMOUNT_TYPE_COUNT, AMOUNT_TYPE_VALUE, AMOUNT_TYPE_WEIGHT

from ..content_builders import build_linked_quest_submit_success_n_left_description


def _iter_options():
    item_id = ITEM_ID_PEACH
    item = get_item_nullable(item_id)
    assert item is not None
    
    yield (
        item,
        AMOUNT_TYPE_COUNT,
        20,
        50,
        12,
        (
            f'You have submitted **12** {item.name} {item.emoji}.\n'
            f'**18** more to submit.'
        ),
    )
    
    yield (
        item,
        AMOUNT_TYPE_WEIGHT,
        20,
        50,
        13,
        (
            f'You have submitted **0.013 kg** {item.name} {item.emoji}.\n'
            f'**0.017 kg** more to submit.'
        ),
    )
    
    yield (
        item,
        AMOUNT_TYPE_VALUE,
        20,
        50,
        14,
        (
            f'You have submitted **14** {EMOJI__HEART_CURRENCY} worth of {item.name} {item.emoji}.\n'
            f'**16** {EMOJI__HEART_CURRENCY} worth of more to submit.'
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_linked_quest_submit_success_n_left_description(
    item, amount_type, amount_submitted, amount_required, amount_used,
):
    """
    Tests whether ``build_linked_quest_submit_success_n_left_description`` works as intended.
    
    Parameters
    ----------
    item : ``None | Item``
        The submitted item.
    
    amount_type : `int`
        The amount's type.
    
    amount_submitted : `int`
        Already submitted amount.
    
    amount_required : `int`
        The amount of required items.
    
    amount_used : `int`
        The used up amount.
    
    Returns
    -------
    output : `str`
    """
    output = build_linked_quest_submit_success_n_left_description(
        item, amount_type, amount_submitted, amount_required, amount_used,
    )
    vampytest.assert_instance(output, str)
    return output
