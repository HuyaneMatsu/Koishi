import vampytest
from ....bot_utils.constants import EMOJI__HEART_CURRENCY

from ...item_core import ITEM_ID_PEACH, ITEM_ID_SCARLET_ONION, ITEM_ID_STRAWBERRY, get_item_nullable
from ...quest_core import (
    QUEST_TEMPLATE_ID_MYSTIA_PEACH, get_quest_template_nullable, linked_quest_create,
    quest_requirement_serialisable_create_duration, quest_requirement_serialisable_create_expiration,
    quest_requirement_serialisable_create_item_exact, quest_reward_serialisable_create_balance,
    quest_reward_serialisable_create_credibility
)
from ...unit_core import AMOUNT_TYPE_COUNT

from ..content_building import produce_linked_quest_detailed_description


def _iter_options():
    item_peach = get_item_nullable(ITEM_ID_PEACH)
    assert item_peach is not None
    
    item_strawberry = get_item_nullable(ITEM_ID_STRAWBERRY)
    assert item_strawberry is not None
    
    item_scarlet_onion = get_item_nullable(ITEM_ID_SCARLET_ONION)
    assert item_scarlet_onion is not None
    
    quest_template = get_quest_template_nullable(QUEST_TEMPLATE_ID_MYSTIA_PEACH)
    assert quest_template is not None
    
    user_id = 202505230020
    guild_id = 202505230021
    batch_id = 55555
    
    yield (
        linked_quest_create(
            user_id,
            guild_id,
            batch_id,
            QUEST_TEMPLATE_ID_MYSTIA_PEACH,
            (
                quest_requirement_serialisable_create_duration(3600 * 24),
                quest_requirement_serialisable_create_expiration(1000000 + 3600 * 24),
                quest_requirement_serialisable_create_item_exact(ITEM_ID_PEACH, AMOUNT_TYPE_COUNT, 20, 0),
            ),
            (
                quest_reward_serialisable_create_balance(1000),
                quest_reward_serialisable_create_credibility(10),
            ),
        ),
        quest_template,
        1,
        False,
        (
            f'**Task: Submit 0 / 20 {item_peach.emoji} {item_peach.name} to Mystia.**\n'
            f'\n'
            f'{quest_template.description}\n'
            f'\n'
            f'**Rewards:**\n'
            f'- **1000** {EMOJI__HEART_CURRENCY}\n'
            f'- **10** credibility\n'
            f'**Time available:**\n'
            f'- **1 day**\n'
            f'**Time left:**\n'
            f'- **1 day**\n'
            f'**Completed:**\n'
            f'- **0 / 3** times, cannot be re-accepted anymore'
        ),
    )
    
    yield (
        linked_quest_create(
            user_id,
            guild_id,
            batch_id,
            QUEST_TEMPLATE_ID_MYSTIA_PEACH,
            (
                quest_requirement_serialisable_create_item_exact(ITEM_ID_PEACH, AMOUNT_TYPE_COUNT, 20, 0),
                quest_requirement_serialisable_create_item_exact(ITEM_ID_STRAWBERRY, AMOUNT_TYPE_COUNT, 19, 0),
                quest_requirement_serialisable_create_item_exact(ITEM_ID_SCARLET_ONION, AMOUNT_TYPE_COUNT, 18, 2),
            ),
            None,
        ),
        quest_template,
        1,
        False,
        (
            f'**Task: Submit 0 / 20 {item_peach.emoji} {item_peach.name}, '
            f'0 / 19 {item_strawberry.emoji} {item_strawberry.name} and '
            f'2 / 18 {item_scarlet_onion.emoji} {item_scarlet_onion.name} to Mystia.**\n'
            f'\n'
            f'{quest_template.description}\n'
            f'\n'
            f'**Time available:**\n'
            f'- **unlimited**\n'
            f'**Time left:**\n'
            f'- **unlimited**\n'
            f'**Completed:**\n'
            f'- **0 / 3** times, cannot be re-accepted anymore'
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__produce_linked_quest_detailed_description(
    linked_quest, quest_template, user_level, highlight_only_missing_requirements
):
    """
    Tests whether ``produce_linked_quest_detailed_description`` works as intended.
    
    Parameters
    ----------
    linked_quest : ``LinkedQuest``
        The linked quest in context.
    
    quest_template : ``None | QuestTemplate``
        The quest's template.
    
    user_level : `int`
        The user's adventurer rank.
    
    highlight_only_missing_requirements : `bool`
        Whether only missing requirements should be highlighted.
    
    Returns
    -------
    output : `str`
    """
    def unix_time_seconds_get():
        return 1000000
    
    mocked = vampytest.mock_globals(
        produce_linked_quest_detailed_description,
        2,
        unix_time_seconds_get = unix_time_seconds_get,
    )
    
    output = [*mocked(
        linked_quest, quest_template, user_level, highlight_only_missing_requirements
    )]
    
    for element in output:
        vampytest.assert_instance(element, str)
    
    return ''.join(output)
