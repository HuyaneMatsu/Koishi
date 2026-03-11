import vampytest
from hata import BUILTIN_EMOJIS

from ....bot_utils.constants import EMOJI__HEART_CURRENCY

from ...item_core import ITEM_ID_PEACH
from ...quest_core import (
    AMOUNT_TYPE_COUNT, QUEST_TEMPLATE_ID_MYSTIA_PEACH, Quest, QuestRequirementInstantiableDuration,
    QuestRequirementInstantiableItemExact, QuestRewardInstantiableBalance, QuestRewardInstantiableCredibility,
    get_quest_template
)

from ..content_building import produce_quest_detailed_description


def _iter_options():
    quest_template_id = QUEST_TEMPLATE_ID_MYSTIA_PEACH
    quest_template = get_quest_template(quest_template_id)
    assert quest_template is not None
    
    yield (
        Quest(
            quest_template_id,
            (
                QuestRequirementInstantiableDuration(3600 * 24),
                QuestRequirementInstantiableItemExact(ITEM_ID_PEACH, AMOUNT_TYPE_COUNT, 20),
            ),
            (
                QuestRewardInstantiableBalance(1000),
                QuestRewardInstantiableCredibility(10),
            ),
        ),
        quest_template,
        1,
        2,
        (
            f'**Task: Submit 20 {BUILTIN_EMOJIS["peach"]} Peach to Mystia.**\n'
            f'\n'
            f'{quest_template.description}\n'
            f'\n'
            f'**Rewards:**\n'
            f'- **1000** {EMOJI__HEART_CURRENCY}\n'
            f'- **10** credibility\n'
            f'**Time available:**\n'
            f'- **1 day**\n'
            f'**Completable:**\n'
            f'- **3** times (1 left)'
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__produce_quest_detailed_description(quest, quest_template, user_level, completion_count):
    """
    Tests whether ``produce_quest_detailed_description`` works as intended.
    
    Parameters
    ----------
    quest : ``Quest``
        The quest in context.
    
    quest_template : `int`
        The quest's template.
    
    user_level : `int`
        The user's adventurer rank.
    
    completion_count : `int`
        HHow much times was the quest already completed.
    
    Returns
    -------
    output : `str`
    """
    output = [*produce_quest_detailed_description(quest, quest_template, user_level, completion_count)]
    
    for element in output:
        vampytest.assert_instance(element, str)
    
    return ''.join(output)
