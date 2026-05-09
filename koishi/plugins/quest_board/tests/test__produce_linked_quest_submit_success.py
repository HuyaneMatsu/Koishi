import vampytest

from ....bot_utils.constants import EMOJI__HEART_CURRENCY

from ...item_core import ITEM_ID_PEACH, get_item_nullable
from ...quest_core import AMOUNT_TYPE_COUNT, AMOUNT_TYPE_VALUE, AMOUNT_TYPE_WEIGHT

from ..content_building import produce_linked_quest_submit_success


def _iter_options():
    item_id = ITEM_ID_PEACH
    item = get_item_nullable(item_id)
    assert item is not None
    
    yield (
        [
            (item, AMOUNT_TYPE_COUNT, 50, 20, 12),
        ],
        (
            (
                f'You have submitted **12** {item.emoji} {item.name}.\n'
                f'**18** more to submit.'
            ),
            True,
        ),
    )
    
    yield (
        [
            (item, AMOUNT_TYPE_WEIGHT, 50, 20, 13),
        ],
        (
            (
                f'You have submitted **0.013 kg** {item.emoji} {item.name}.\n'
                f'**0.017 kg** more to submit.'
            ),
            True,
        ),
    )
    
    yield (
        [
            (item, AMOUNT_TYPE_VALUE, 50, 20, 14),
        ],
        (
            (
                f'You have submitted **14** {EMOJI__HEART_CURRENCY} worth of {item.emoji} {item.name}.\n'
                f'**16** {EMOJI__HEART_CURRENCY} worth of more to submit.'
            ),
            True,
        ),
    )
    
    yield (
        None,
        (
            '',
            False,
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__produce_linked_quest_submit_success(submissions_normalised):
    """
    Tests whether ``produce_linked_quest_submit_success`` works as intended.
    
    Parameters
    ----------
    submissions_normalised : ``None | list<(Item, int, int, int, int)>``
        The submitted amounts normalised.
    
    Returns
    -------
    output : `(str, bool)`
    """
    output = []
    generator = produce_linked_quest_submit_success(submissions_normalised)
    
    while True:
        try:
            part = generator.send(None)
        except StopIteration as exception:
            add_extra_line_break_after = exception.value
            break
        
        output.append(part)
        continue
    
    for element in output:
        vampytest.assert_instance(element, str)
    
    vampytest.assert_instance(add_extra_line_break_after, bool)
    
    return ''.join(output), add_extra_line_break_after
