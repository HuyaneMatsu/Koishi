import vampytest
from hata import InteractionForm, create_label, create_text_display, create_text_input

from ....bot_utils.constants import EMOJI__HEART_CURRENCY

from ...item_core import (
    ITEM_GROUP_ID_FIREWOOD, ITEM_ID_PEACH, ITEM_ID_SCARLET_ONION, ITEM_ID_STRAWBERRY, get_item_group_nullable,
    get_item_nullable
)
from ...quest_core import (
    AMOUNT_TYPE_COUNT, LINKED_QUEST_COMPLETION_STATE_COMPLETED, LinkedQuest, QUEST_TEMPLATE_ID_MYSTIA_FIREWOOD,
    QUEST_TEMPLATE_ID_MYSTIA_PEACH, Quest, QuestRequirementInstantiableDuration, QuestRequirementInstantiableItemExact,
    QuestRequirementSerialisableDuration, QuestRequirementSerialisableItemExact, QuestRewardInstantiableBalance,
    QuestRewardInstantiableCredibility, QuestRewardSerialisableBalance, QuestRewardSerialisableCredibility,
    get_quest_template_nullable
)
from ...user_stats_core import UserStats

from ..component_building import build_quest_complete_confirmation_form


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
    
    
    user_id = 202604130002
    guild_id = 202604130003
    batch_id = 55555
    
    
    yield (
        'default',
        user_id,
        guild_id,
        0,
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
        None,
        quest_template_mystia_peach,
        1 << 10,
        6,
        InteractionForm(
            'Please confirm completion',
            [
                create_text_display(
                    f'**Task: Submit 20 {item_peach.emoji} {item_peach.name} to Mystia.**\n'
                    f'\n'
                    f'{quest_template_mystia_peach.description}\n'
                    f'\n'
                    f'**Rewards:**\n'
                    f'- **1000** {EMOJI__HEART_CURRENCY}\n'
                    f'- **10** credibility'
                ),
                create_label(
                    'How much times do you wish to complete it?',
                    f'Up to {3} times.',
                    create_text_input(
                        custom_id = 'completion_count',
                        placeholder = '3',
                        required = False,
                        max_length = 1,
                        min_length = 1,
                        value = '3',
                    ),
                ),
            ],
            f'quest_board.complete.{user_id:x}.{guild_id:x}.{0:x}.{QUEST_TEMPLATE_ID_MYSTIA_PEACH:x}',
        )
    )
    
    linked_quest = LinkedQuest(
        user_id,
        guild_id,
        batch_id,
        QUEST_TEMPLATE_ID_MYSTIA_PEACH,
        (
            QuestRequirementSerialisableDuration(3600 * 24),
            QuestRequirementSerialisableItemExact(ITEM_ID_PEACH, AMOUNT_TYPE_COUNT, 20, 0),
        ),
        (
            QuestRewardSerialisableBalance(1000),
            QuestRewardSerialisableCredibility(10),
        ),
    )
    linked_quest.completion_count = 1
    linked_quest.completion_state = LINKED_QUEST_COMPLETION_STATE_COMPLETED
    
    yield (
        'linked',
        user_id,
        guild_id,
        0,
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
        linked_quest,
        quest_template_mystia_peach,
        1 << 10,
        6,
        InteractionForm(
            'Please confirm completion',
            [
                create_text_display(
                    f'**Task: Submit 20 {item_peach.emoji} {item_peach.name} to Mystia.**\n'
                    f'\n'
                    f'{quest_template_mystia_peach.description}\n'
                    f'\n'
                    f'**Rewards:**\n'
                    f'- **1000** {EMOJI__HEART_CURRENCY}\n'
                    f'- **10** credibility'
                ),
                create_label(
                    'How much times do you wish to complete it?',
                    f'Up to {2} times.',
                    create_text_input(
                        custom_id = 'completion_count',
                        placeholder = '2',
                        required = False,
                        max_length = 1,
                        min_length = 1,
                        value = '2',
                    ),
                ),
            ],
            f'quest_board.complete.{user_id:x}.{guild_id:x}.{0:x}.{QUEST_TEMPLATE_ID_MYSTIA_PEACH:x}',
        )
    )


@vampytest._(vampytest.call_from(_iter_options()).named_first().returning_last())
def test__build_quest_complete_confirmation_form(
    user_id, guild_id, page_index, quest, linked_quest, quest_template, user_credibility, possession_count
):
    """
    Tests whether ``build_quest_complete_confirmation_form`` works as intended.
    
    Parameters
    ----------
    user_id : `int`
        The invoking user's identifier.
    
    guild_id : `int`
        The local guild's identifier.
    
    page_index : `int`
        The linked quests' current page's index.
    
    quest : ``Quest``
        The quest to describe.
    
    linked_quest : : ``None | LinkedQuest``
        The linked quest if the user already completed this quest before.
    
    quest_template : ``QuestTemplate``
        The quest's template.
    
    credibility : `int`
        The user's  credibility.
    
    possession_count : `int`
        How much times the required items are possessed by the user.
    
    Returns
    -------
    output : ``InteractionForm``
    """
    user_stats = UserStats(user_id)
    user_stats.modify_credibility_by(user_credibility)
    
    output = build_quest_complete_confirmation_form(
        user_id, guild_id, page_index, quest, linked_quest, quest_template, user_stats, possession_count
    )
    vampytest.assert_instance(output, InteractionForm)
    return output
