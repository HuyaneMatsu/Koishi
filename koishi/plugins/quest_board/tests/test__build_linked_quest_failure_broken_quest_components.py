import vampytest

from hata import Component, create_text_display

from ..component_building import build_linked_quest_failure_broken_quest_components
from ..constants import BROKEN_QUEST_DESCRIPTION


def _iter_options():
    yield (
        [
            create_text_display(BROKEN_QUEST_DESCRIPTION),
        ],
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_linked_quest_failure_broken_quest_components():
    """
    Tests whether ``build_linked_quest_failure_broken_quest_components`` works as intended.
    
    Returns
    -------
    output : ``list<Component>``
    """
    output = build_linked_quest_failure_broken_quest_components()
    
    vampytest.assert_instance(output, list)
    for element in output:
        vampytest.assert_instance(element, Component)
    
    return output
