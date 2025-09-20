import vampytest
from hata import BUILTIN_EMOJIS

from ...quest_core import QUEST_TEMPLATE_ID_MYSTIA_PEACH, QUEST_TEMPLATE_ID_SAKUYA_STRAWBERRY, get_quest_template

from ..content_builders import produce_quest_short_description


def _iter_options():
    yield (
        get_quest_template(QUEST_TEMPLATE_ID_MYSTIA_PEACH),
        20,
        (
            f'Required rank: G\n'
            f'Submit 20 {BUILTIN_EMOJIS["peach"]} Peach to Mystia.'
        ),
    )
    
    yield (
        get_quest_template(QUEST_TEMPLATE_ID_SAKUYA_STRAWBERRY),
        500,
        (
            f'Required rank: F\n'
            f'Submit 0.5 kg {BUILTIN_EMOJIS["strawberry"]} Strawberry to Sakuya.'
        ),
    )
    
    # No submit items by value quests yet
    # No subjugation quests yet


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__produce_quest_short_description(quest_template, amount_required):
    """
    Tests whether ``produce_quest_short_description`` works as intended.
    
    Parameters
    ----------
    quest_template : ``QuestTemplate``
        The quest's template.
    
    amount_required : `int`
        The required amount of items to submit.
    
    Returns
    -------
    output : `str`
    """
    output = [*produce_quest_short_description(quest_template, amount_required)]
    
    for element in output:
        vampytest.assert_instance(element, str)
    
    return ''.join(output)
