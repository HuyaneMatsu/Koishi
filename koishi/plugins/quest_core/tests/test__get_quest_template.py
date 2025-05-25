import vampytest

from ..quest_template import QuestTemplate
from ..quest_templates import QUEST_TEMPLATE_MYSTIA_SCARLET_ONION
from ..utils import get_quest_template


def _iter_options():
    yield -1, None
    yield QUEST_TEMPLATE_MYSTIA_SCARLET_ONION.id, QUEST_TEMPLATE_MYSTIA_SCARLET_ONION


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__get_quest_template(quest_template_id):
    """
    Tests whether the ``get_quest_template`` works as intended.
    
    Parameters
    ----------
    quest_template_id : `int`
        The quest template's identifier.
    
    Returns
    -------
    output : ``None | QuestTemplate``
    """
    output = get_quest_template(quest_template_id)
    vampytest.assert_instance(output, QuestTemplate, nullable = True)
    return output
