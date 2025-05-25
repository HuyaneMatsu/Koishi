import vampytest
from hata import BUILTIN_EMOJIS

from ...quest_core import QUEST_TEMPLATE_ID_MYSTIA_PEACH, QUEST_TEMPLATE_ID_SAKUYA_STRAWBERRY, Quest, get_quest_template

from ..content_builders import build_quest_short_description


def _iter_options():
    yield (
        Quest(
            QUEST_TEMPLATE_ID_MYSTIA_PEACH,
            20,
            3600 * 24,
            2,
            1000,
        ),
        get_quest_template(QUEST_TEMPLATE_ID_MYSTIA_PEACH),
        (
            f'Required rank: G\n'
            f'Submit 20 Peach {BUILTIN_EMOJIS["peach"]} to Mystia.'
        ),
    )
    
    yield (
        Quest(
            QUEST_TEMPLATE_ID_SAKUYA_STRAWBERRY,
            500,
            3600 * 24,
            3,
            1000,
        ),
        get_quest_template(QUEST_TEMPLATE_ID_SAKUYA_STRAWBERRY),
        (
            f'Required rank: F\n'
            f'Submit 0.5 kg Strawberry {BUILTIN_EMOJIS["strawberry"]} to Sakuya.'
        ),
    )
    
    # No submit items by value quests yet
    # No subjugation quests yet


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_quest_short_description(quest, quest_template):
    """
    Tests whether ``build_quest_short_description`` works as intended.
    
    Parameters
    ----------
    quest : ``Quest``
        The quest in context.
    
    quest_template : `int`
        The quest's template.
    
    Returns
    -------
    output : `str`
    """
    output = build_quest_short_description(quest, quest_template)
    vampytest.assert_instance(output, str)
    return output
