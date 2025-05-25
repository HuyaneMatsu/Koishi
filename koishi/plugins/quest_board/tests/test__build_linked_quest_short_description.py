import vampytest
from hata import BUILTIN_EMOJIS

from ...quest_core import LinkedQuest, QUEST_TEMPLATE_ID_MYSTIA_PEACH, Quest, get_quest_template

from ..content_builders import build_linked_quest_short_description


def _iter_options():
    user_id = 202505230010
    guild_id = 202505230011
    batch_id = 55555
    
    yield (
        LinkedQuest(
            user_id,
            guild_id,
            batch_id,
            Quest(
                QUEST_TEMPLATE_ID_MYSTIA_PEACH,
                20,
                3600 * 24,
                2,
                1000,
            ),
        ),
        get_quest_template(QUEST_TEMPLATE_ID_MYSTIA_PEACH),
        (
            f'Time left: 23 hours, 59 minutes, 59 seconds\n'
            f'Submit 0 / 20 Peach {BUILTIN_EMOJIS["peach"]} to Mystia.'
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_linked_quest_short_description(linked_quest, quest_template):
    """
    Tests whether ``build_linked_quest_short_description`` works as intended.
    
    Parameters
    ----------
    linked_quest : ``LinkedQuest``
        The linked quest in context.
    
    quest_template : `int`
        The quest's template.
    
    Returns
    -------
    output : `str`
    """
    output = build_linked_quest_short_description(linked_quest, quest_template)
    vampytest.assert_instance(output, str)
    return output
