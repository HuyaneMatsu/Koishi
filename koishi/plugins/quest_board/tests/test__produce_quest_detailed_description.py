import vampytest

from ....bot_utils.constants import EMOJI__HEART_CURRENCY

from ...item_core import ITEM_GROUP_ID_FIREWOOD, ITEM_ID_PEACH, get_item_nullable, get_item_group_nullable
from ...quest_core import (
    AMOUNT_TYPE_COUNT, QUEST_TEMPLATE_ID_MYSTIA_FIREWOOD, QUEST_TEMPLATE_ID_MYSTIA_PEACH, Quest,
    QuestRequirementInstantiableDuration, QuestRequirementInstantiableItemExact, QuestRequirementInstantiableItemGroup,
    QuestRewardInstantiableBalance, QuestRewardInstantiableCredibility, get_quest_template_nullable
)

from ..content_building import produce_quest_detailed_description


def _iter_options():
    item_peach = get_item_nullable(ITEM_ID_PEACH)
    assert item_peach is not None
    
    item_group_firewood = get_item_group_nullable(ITEM_GROUP_ID_FIREWOOD)
    assert item_group_firewood is not None
    
    quest_template_mystia_peach = get_quest_template_nullable(QUEST_TEMPLATE_ID_MYSTIA_PEACH)
    assert quest_template_mystia_peach is not None
    
    quest_template_mystia_firewood = get_quest_template_nullable(QUEST_TEMPLATE_ID_MYSTIA_FIREWOOD)
    assert quest_template_mystia_firewood is not None
    
    yield (
        'Default, 3 times',
        Quest(
            QUEST_TEMPLATE_ID_MYSTIA_PEACH,
            (
                QuestRequirementInstantiableDuration(3600 * 24),
                QuestRequirementInstantiableItemExact(ITEM_ID_PEACH, AMOUNT_TYPE_COUNT, 20),
            ),
            (
                QuestRewardInstantiableBalance(1000),
                QuestRewardInstantiableCredibility(10),
            ),
        ),
        quest_template_mystia_peach,
        1,
        0,
        0,
        (
            f'**Task: Submit 20 {item_peach.emoji} {item_peach.name} to Mystia.**\n'
            f'\n'
            f'{quest_template_mystia_peach.description}\n'
            f'\n'
            f'**Rewards:**\n'
            f'- **1000** {EMOJI__HEART_CURRENCY}\n'
            f'- **10** credibility\n'
            f'**Time available:**\n'
            f'- **1 day**\n'
            f'**Completable:**\n'
            f'- **3** times'
        ),
    )
    
    yield (
        'Bland',
        Quest(
            QUEST_TEMPLATE_ID_MYSTIA_FIREWOOD,
            None,
            None,
        ),
        quest_template_mystia_firewood,
        1,
        0,
        0,
        (
            f'{quest_template_mystia_firewood.description}\n'
            f'\n'
            f'**Time available:**\n'
            f'- **unlimited**\n'
            f'**Completable:**\n'
            f'- **unlimited** times'
        ),
    )
    
    yield (
        'Completed 2 / 3 times',
        Quest(
            QUEST_TEMPLATE_ID_MYSTIA_PEACH,
            (
                QuestRequirementInstantiableItemExact(ITEM_ID_PEACH, AMOUNT_TYPE_COUNT, 20),
            ),
            None,
        ),
        quest_template_mystia_peach,
        1,
        2,
        0,
        (
            f'**Task: Submit 20 {item_peach.emoji} {item_peach.name} to Mystia.**\n'
            f'\n'
            f'{quest_template_mystia_peach.description}\n'
            f'\n'
            f'**Time available:**\n'
            f'- **unlimited**\n'
            f'**Completable:**\n'
            f'- **3** times (**1** left)'
        ),
    )
    
    yield (
        'Completed 2 / unlimited times',
        Quest(
            QUEST_TEMPLATE_ID_MYSTIA_FIREWOOD,
            (
                QuestRequirementInstantiableItemGroup(ITEM_GROUP_ID_FIREWOOD, AMOUNT_TYPE_COUNT, 20),
            ),
            None,
        ),
        quest_template_mystia_firewood,
        1,
        2,
        0,
        (
            f'**Task: Submit 20 {item_group_firewood.emoji} {item_group_firewood.name} to Mystia.**\n'
            f'\n'
            f'{quest_template_mystia_firewood.description}\n'
            f'\n'
            f'**Time available:**\n'
            f'- **unlimited**\n'
            f'**Completable:**\n'
            f'- **unlimited** times'
        ),
    )
    
    yield (
        'Completed 2 / 3 times; 6 times in possession',
        Quest(
            QUEST_TEMPLATE_ID_MYSTIA_PEACH,
            (
                QuestRequirementInstantiableItemExact(ITEM_ID_PEACH, AMOUNT_TYPE_COUNT, 20),
            ),
            None,
        ),
        quest_template_mystia_peach,
        1,
        2,
        6,
        (
            f'**Task: Submit 20 {item_peach.emoji} {item_peach.name} to Mystia.**\n'
            f'\n'
            f'{quest_template_mystia_peach.description}\n'
            f'\n'
            f'**Time available:**\n'
            f'- **unlimited**\n'
            f'**Completable:**\n'
            f'- **3** times (**1** left; **6** times in possession)'
        ),
    )
    
    yield (
        'Completed 2 / unlimited times; 6 times in possession',
        Quest(
            QUEST_TEMPLATE_ID_MYSTIA_FIREWOOD,
            (
                QuestRequirementInstantiableItemGroup(ITEM_GROUP_ID_FIREWOOD, AMOUNT_TYPE_COUNT, 20),
            ),
            None,
        ),
        quest_template_mystia_firewood,
        1,
        2,
        6,
        (
            f'**Task: Submit 20 {item_group_firewood.emoji} {item_group_firewood.name} to Mystia.**\n'
            f'\n'
            f'{quest_template_mystia_firewood.description}\n'
            f'\n'
            f'**Time available:**\n'
            f'- **unlimited**\n'
            f'**Completable:**\n'
            f'- **unlimited** times (**6** times in possession)'
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).named_first().returning_last())
def test__produce_quest_detailed_description(quest, quest_template, user_level, completion_count, possession_count):
    """
    Tests whether ``produce_quest_detailed_description`` works as intended.
    
    Parameters
    ----------
    quest : ``Quest``
        The quest in context.
    
    quest_template : ``None | QuestTemplate``
        The quest's template.
    
    user_level : `int`
        The user's adventurer rank.
    
    completion_count : `int`
        How much times was the quest already completed.
    
    possession_count : `int`
        How much times the required items are possessed by the user.
    
    Returns
    -------
    output : `str`
    """
    output = [*produce_quest_detailed_description(
        quest, quest_template, user_level, completion_count, possession_count
    )]
    
    for element in output:
        vampytest.assert_instance(element, str)
    
    return ''.join(output)
