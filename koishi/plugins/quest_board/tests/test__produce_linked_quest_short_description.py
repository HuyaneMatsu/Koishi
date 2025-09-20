from datetime import datetime as DateTime, timedelta as TimeDelta, timezone as TimeZone

import vampytest
from hata import BUILTIN_EMOJIS

from ...quest_core import QUEST_TEMPLATE_ID_MYSTIA_PEACH, get_quest_template

from ..content_builders import produce_linked_quest_short_description


def _iter_options():
    yield (
        get_quest_template(QUEST_TEMPLATE_ID_MYSTIA_PEACH),
        20,
        0,
        DateTime.now(tz = TimeZone.utc) + TimeDelta(seconds = 3600 * 24),
        (
            f'Time left: 23 hours, 59 minutes, 59 seconds\n'
            f'Submit 0 / 20 {BUILTIN_EMOJIS["peach"]} Peach to Mystia.'
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__produce_linked_quest_short_description(quest_template, amount_required, amount_submitted, expires_at):
    """
    Tests whether ``produce_linked_quest_short_description`` works as intended.
    
    Parameters
    ----------
    quest_template : ``QuestTemplate``
        The quest's template.
    
    amount_required : ``QuestTemplate``
        The required amount of items to submit.
    
    amount_submitted : `int`
        The already submitted amount.
    
    expires_at : `DateTime`
        When the quest expires.
    
    Returns
    -------
    output : `str`
    """
    output = [*produce_linked_quest_short_description(quest_template, amount_required, amount_submitted, expires_at)]
    
    for element in output:
        vampytest.assert_instance(element, str)
    
    return ''.join(output)
