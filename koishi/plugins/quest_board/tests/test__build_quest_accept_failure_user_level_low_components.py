import vampytest

from hata import Component, create_text_display

from ..component_building import build_quest_accept_failure_user_level_low_components


def _iter_options():
    yield (
        [
            create_text_display('Your rank is too low to accept this quest.'),
        ],
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_quest_accept_failure_user_level_low_components():
    """
    Tests whether ``build_quest_accept_failure_user_level_low_components`` works as intended.
    
    Returns
    -------
    output : ``list<Component>``
    """
    output = build_quest_accept_failure_user_level_low_components()
    
    vampytest.assert_instance(output, list)
    for element in output:
        vampytest.assert_instance(element, Component)
    
    return output
