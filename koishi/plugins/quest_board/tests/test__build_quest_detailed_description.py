import vampytest
from hata import BUILTIN_EMOJIS

from ....bot_utils.constants import EMOJI__HEART_CURRENCY

from ...quest_core import QUEST_TEMPLATE_ID_MYSTIA_PEACH, Quest, get_quest_template

from ..content_builders import build_quest_detailed_description


def _iter_options():
    quest_template_id = QUEST_TEMPLATE_ID_MYSTIA_PEACH
    quest_template = get_quest_template(quest_template_id)
    assert quest_template is not None
    
    yield (
        Quest(
            quest_template_id,
            20,
            3600 * 24,
            2,
            1000,
        ),
        quest_template,
        1,
        (
            f'**Task: Submit 20 Peach {BUILTIN_EMOJIS["peach"]} to Mystia.**\n'
            f'\n'
            f'{quest_template.description}\n'
            f'\n'
            f'**Reward:**\n'
            f'- **1000** {EMOJI__HEART_CURRENCY}\n'
            f'- **1** credibility\n'
            f'**Time available:**\n'
            f'- **1 day**'
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_quest_detailed_description(quest, quest_template, user_level):
    """
    Tests whether ``build_quest_detailed_description`` works as intended.
    
    Parameters
    ----------
    quest : ``Quest``
        The quest in context.
    
    quest_template : `int`
        The quest's template.
    
    user_level : `int`
        The user's adventurer rank.
    
    Returns
    -------
    output : `str`
    """
    output = build_quest_detailed_description(quest, quest_template, user_level)
    vampytest.assert_instance(output, str)
    return output
