import vampytest

from ....bot_utils.constants import EMOJI__HEART_CURRENCY

from ...item_core import ITEM_ID_PEACH, get_item_nullable
from ...quest_core import AMOUNT_TYPE_COUNT, QUEST_REWARD_TYPE_BALANCE, QUEST_REWARD_TYPE_CREDIBILITY

from ..content_building import produce_linked_quest_submit_success_completed_description

from config import ORIN_ID


def _iter_options():
    item_id = ITEM_ID_PEACH
    item = get_item_nullable(item_id)
    assert item is not None
    
    yield (
        'rank up, generic',
        0,
        [
            (item, AMOUNT_TYPE_COUNT, 50, 38, 12)
        ],
        [
            (QUEST_REWARD_TYPE_BALANCE, 0, 900),
            (QUEST_REWARD_TYPE_CREDIBILITY, 0, 3),
        ],
        1,
        1,
        2,
        (
            f'You have submitted **12** {item.emoji} {item.name}.\n'
            f'For a total of **50**.\n'
            f'By doing so, you completed the quest.\n'
            f'\n'
            f'**You received:**\n'
            f'- **900** {EMOJI__HEART_CURRENCY}\n'
            f'- **3** credibility\n'
            f'\n'
            f'By completing this quest you have ranked up from **G** to **F** rank.\n'
            f'Orin! Bring the buffet chariot! Let the party begin!'
        ),
    )
    
    yield (
        'rank up, orin',
        ORIN_ID,
        [
            (item, AMOUNT_TYPE_COUNT, 50, 38, 12)
        ],
        [
            (QUEST_REWARD_TYPE_BALANCE, 0, 900),
            (QUEST_REWARD_TYPE_CREDIBILITY, 0, 3),
        ],
        1,
        1,
        2,
        (
            f'You have submitted **12** {item.emoji} {item.name}.\n'
            f'For a total of **50**.\n'
            f'By doing so, you completed the quest.\n'
            f'\n'
            f'**You received:**\n'
            f'- **900** {EMOJI__HEART_CURRENCY}\n'
            f'- **3** credibility\n'
            f'\n'
            f'By completing this quest you have ranked up from **G** to **F** rank.\n'
            f'Maids! Bring my buffet chariot! Let the party begin!'
        ),
    )
    
    # Credibility is optional.
    # If you accept a lower rank quest it is possible you receive 0.
    yield (
        'no credibility',
        0,
        [
            (item, AMOUNT_TYPE_COUNT, 50, 38, 12)
        ],
        [
            (QUEST_REWARD_TYPE_BALANCE, 0, 900),
        ],
        1,
        0,
        0,
        (
            f'You have submitted **12** {item.emoji} {item.name}.\n'
            f'For a total of **50**.\n'
            f'By doing so, you completed the quest.\n'
            f'\n'
            f'**You received:**\n'
            f'- **900** {EMOJI__HEART_CURRENCY}'
        ),
    )

    yield (
        'multi-completion',
        0,
        [
            (item, AMOUNT_TYPE_COUNT, 50, 38, 12)
        ],
        [
            (QUEST_REWARD_TYPE_BALANCE, 0, 900),
            (QUEST_REWARD_TYPE_CREDIBILITY, 0, 3),
        ],
        5,
        1,
        1,
        (
            f'You have submitted **12** {item.emoji} {item.name}.\n'
            f'For a total of **50**.\n'
            f'By doing so, you completed the quest 5 times.\n'
            f'\n'
            f'**You received:**\n'
            f'- **900** {EMOJI__HEART_CURRENCY}\n'
            f'- **3** credibility'
        ),
    )

    yield (
        'No submission',
        0,
        None,
        [
            (QUEST_REWARD_TYPE_BALANCE, 0, 900),
        ],
        1,
        0,
        0,
        (
            f'You completed the quest.\n'
            f'\n'
            f'**You received:**\n'
            f'- **900** {EMOJI__HEART_CURRENCY}'
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).named_first().returning_last())
def test__produce_linked_quest_submit_success_completed_description(
    client_id,
    submissions_normalised,
    rewards_normalised,
    executed_completion_count,
    user_level_old,
    user_level_new,
):
    """
    Tests whether ``produce_linked_quest_submit_success_completed_description`` works as intended.
    
    Parameters
    ----------
    client_id : `int`
        The client's identifier who is rendering this message.
    
    submissions_normalised : ``list<(Item, int, int, int, int)>``
        The submitted amounts normalised.
    
    rewards_normalised : `None | list<(int, int, int)>`
        The rewards given by the quest in a normalised form.
    
    executed_completion_count : `int`
        How much times completion was executed.
    
    user_level_old : `int`
        The user's adventurer rank before completing the quest.
    
    user_level_new : `int`
        The user's adventurer rank after completing the quest.
    
    Returns
    -------
    output : `str`
    """
    output = ''.join([*produce_linked_quest_submit_success_completed_description(
        client_id,
        submissions_normalised,
        rewards_normalised,
        executed_completion_count,
        user_level_old,
        user_level_new,
    )])
    
    for element in output:
        vampytest.assert_instance(element, str)
    
    return ''.join(output)
