import vampytest
from hata import BUILTIN_EMOJIS

from ....bot_utils.constants import EMOJI__HEART_CURRENCY

from ...quest_core import LinkedQuest, QUEST_TEMPLATE_ID_MYSTIA_PEACH, Quest, get_quest_template

from ..content_builders import produce_linked_quest_detailed_description


def _iter_options():
    quest_template_id = QUEST_TEMPLATE_ID_MYSTIA_PEACH
    quest_template = get_quest_template(quest_template_id)
    assert quest_template is not None
    
    user_id = 202505230020
    guild_id = 202505230021
    batch_id = 55555
    
    yield (
        LinkedQuest(
            user_id,
            guild_id,
            batch_id,
            Quest(
                quest_template_id,
                20,
                3600 * 24,
                2,
                1000,
            ),
        ),
        quest_template,
        1,
        (
            f'**Task: Submit 0 / 20 {BUILTIN_EMOJIS["peach"]} Peach to Mystia.**\n'
            f'\n'
            f'{quest_template.description}\n'
            f'\n'
            f'**Reward:**\n'
            f'- **1000** {EMOJI__HEART_CURRENCY}\n'
            f'- **1** credibility\n'
            f'**Time available:**\n'
            f'- **1 day**\n'
            f'**Time left:**\n'
            f'- **23 hours, 59 minutes, 59 seconds**'
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__produce_linked_quest_detailed_description(linked_quest, quest_template, user_level):
    """
    Tests whether ``produce_linked_quest_detailed_description`` works as intended.
    
    Parameters
    ----------
    linked_quest : ``LinkedQuest``
        The linked quest in context.
    
    quest_template : `int`
        The quest's template.
    
    user_level : `int`
        The user's adventurer rank.
    
    Returns
    -------
    output : `str`
    """
    output = [*produce_linked_quest_detailed_description(linked_quest, quest_template, user_level)]
    
    for element in output:
        vampytest.assert_instance(element, str)
    
    return ''.join(output)
