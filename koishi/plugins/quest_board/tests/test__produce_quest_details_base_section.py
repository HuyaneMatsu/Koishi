import vampytest

from ....bot_utils.constants import EMOJI__HEART_CURRENCY

from ...item_core import (
    ITEM_GROUP_ID_FIREWOOD, ITEM_ID_PEACH, ITEM_ID_SCARLET_ONION, ITEM_ID_STRAWBERRY, get_item_group_nullable,
    get_item_nullable
)
from ...quest_core import (
    AMOUNT_TYPE_COUNT, LinkedQuest, QUEST_TEMPLATE_ID_MYSTIA_FIREWOOD, QUEST_TEMPLATE_ID_MYSTIA_PEACH, Quest,
    QuestRequirementInstantiableDuration, QuestRequirementInstantiableItemExact, QuestRequirementInstantiableItemGroup,
    QuestRequirementSerialisableItemExact, QuestRewardInstantiableBalance, QuestRewardInstantiableCredibility,
    get_quest_template_nullable
)

from ..content_building import produce_quest_details_base_section


def _iter_options():
    item_peach = get_item_nullable(ITEM_ID_PEACH)
    assert item_peach is not None
    
    item_strawberry = get_item_nullable(ITEM_ID_STRAWBERRY)
    assert item_strawberry is not None
    
    item_scarlet_onion = get_item_nullable(ITEM_ID_SCARLET_ONION)
    assert item_scarlet_onion is not None
    
    item_group_firewood = get_item_group_nullable(ITEM_GROUP_ID_FIREWOOD)
    assert item_group_firewood is not None
    
    quest_template_mystia_peach = get_quest_template_nullable(QUEST_TEMPLATE_ID_MYSTIA_PEACH)
    assert quest_template_mystia_peach is not None
    
    quest_template_mystia_firewood = get_quest_template_nullable(QUEST_TEMPLATE_ID_MYSTIA_FIREWOOD)
    assert quest_template_mystia_firewood is not None
    
    user_id = 202604130000
    guild_id = 202604130001
    batch_id = 55555
    
    yield (
        'Default',
        None,
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
        (
            (
                f'**Task: Submit 20 {item_peach.emoji} {item_peach.name} to Mystia.**\n'
                f'\n'
                f'{quest_template_mystia_peach.description}\n'
                f'\n'
                f'**Rewards:**\n'
                f'- **1000** {EMOJI__HEART_CURRENCY}\n'
                f'- **10** credibility'
            ),
            False,
        ),
    )
    
    yield (
        'Bland',
        None,
        Quest(
            QUEST_TEMPLATE_ID_MYSTIA_FIREWOOD,
            None,
            None,
        ),
        None,
        1,
        (
            '',
            False,
        ),
    )
    
    yield (
        'Template',
        None,
        Quest(
            QUEST_TEMPLATE_ID_MYSTIA_FIREWOOD,
            None,
            None,
        ),
        quest_template_mystia_firewood,
        1,
        (
            f'{quest_template_mystia_firewood.description}',
            True,
        ),
    )
    
    
    yield (
        'Group',
        None,
        Quest(
            QUEST_TEMPLATE_ID_MYSTIA_FIREWOOD,
            (
                QuestRequirementInstantiableItemGroup(ITEM_GROUP_ID_FIREWOOD, AMOUNT_TYPE_COUNT, 20),
            ),
            None,
        ),
        quest_template_mystia_firewood,
        1,
        (
            (
                f'**Task: Submit 20 {item_group_firewood.emoji} {item_group_firewood.name} to Mystia.**\n'
                f'\n'
                f'{quest_template_mystia_firewood.description}'
            ),
            True,
        ),
    )
    
    yield (
        'linked',
        LinkedQuest(
            user_id,
            guild_id,
            batch_id,
            QUEST_TEMPLATE_ID_MYSTIA_PEACH,
            (
                QuestRequirementSerialisableItemExact(ITEM_ID_PEACH, AMOUNT_TYPE_COUNT, 20, 0),
                QuestRequirementSerialisableItemExact(ITEM_ID_STRAWBERRY, AMOUNT_TYPE_COUNT, 19, 0),
                QuestRequirementSerialisableItemExact(ITEM_ID_SCARLET_ONION, AMOUNT_TYPE_COUNT, 18, 2),
            ),
            None,
        ),
        None,
        quest_template_mystia_peach,
        1,
        (
            (
                f'**Task: Submit 0 / 20 {item_peach.emoji} {item_peach.name}, '
                f'0 / 19 {item_strawberry.emoji} {item_strawberry.name} and '
                f'2 / 18 {item_scarlet_onion.emoji} {item_scarlet_onion.name} to Mystia.**\n'
                f'\n'
                f'{quest_template_mystia_peach.description}'
            ),
            True,
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).named_first().returning_last())
def test__produce_quest_details_base_section(linked_quest, quest, quest_template, user_level):
    """
    Tests whether ``produce_quest_details_base_section`` works as intended.
    
    Parameters
    ----------
    linked_quest : ``None | LinkedQuest``
        The linked quest to render.
    
    quest : ``None | Quest``
        The quest in context.
    
    quest_template : ``None | QuestTemplate``
        The quest's template.
    
    user_level : `int`
        The user's adventurer rank.
    
    Returns
    -------
    output : `(str, bool)`
    """
    output = []
    
    generator = produce_quest_details_base_section(linked_quest, quest, quest_template, user_level)
    
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
