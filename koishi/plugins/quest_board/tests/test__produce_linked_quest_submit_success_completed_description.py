import vampytest

from ....bot_utils.constants import EMOJI__HEART_CURRENCY

from ...item_core import ITEM_ID_PEACH, get_item_nullable
from ...quest_core import AMOUNT_TYPE_COUNT

from ..content_builders import produce_linked_quest_submit_success_completed_description


def _iter_options():
    item_id = ITEM_ID_PEACH
    item = get_item_nullable(item_id)
    assert item is not None
    
    yield (
        item,
        AMOUNT_TYPE_COUNT,
        50,
        12,
        900,
        3,
        (
            f'You have submitted **12** {item.emoji} {item.name}.\n'
            f'For a total of **50** and finished the quest.\n'
            f'\n'
            f'**You received:**\n'
            f'- **900** {EMOJI__HEART_CURRENCY}\n'
            f'- **3** credibility'
        ),
    )
    
    # Credibility is optional.
    # If you accept a lower rank quest it is possible you receive 0.
    yield (
        item,
        AMOUNT_TYPE_COUNT,
        50,
        12,
        900,
        0,
        (
            f'You have submitted **12** {item.emoji} {item.name}.\n'
            f'For a total of **50** and finished the quest.\n'
            f'\n'
            f'**You received:**\n'
            f'- **900** {EMOJI__HEART_CURRENCY}'
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__produce_linked_quest_submit_success_completed_description(
    item, amount_type, amount_required, amount_used, reward_balance, reward_credibility,
):
    """
    Tests whether ``produce_linked_quest_submit_success_completed_description`` works as intended.
    
    Parameters
    ----------
    item : ``None | Item``
        The submitted item.
    
    amount_type : `int`
        The amount's type.
    
    amount_required : `int`
        The amount of required items.
    
    amount_used : `int`
        The used up amount.
    
    reward_balance : `int`
        The amount of balance the user receives.
    
    reward_credibility : `int`
        The amount of credibility the user receives.
    
    Returns
    -------
    output : `str`
    """
    output = ''.join([*produce_linked_quest_submit_success_completed_description(
        item, amount_type, amount_required, amount_used, reward_balance, reward_credibility,
    )])
    
    for element in output:
        vampytest.assert_instance(element, str)
    
    return ''.join(output)
