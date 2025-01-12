import vampytest

from ....plugins.touhou_core import CHEN, YAKUMO_RAN, YAKUMO_YUKARI

from ..rendering import _render_single_action_into


def _iter_options():
    yield (
        'kiss',
        None,
        None,
        (
            '.with_action(\n'
            '    ACTION_TAG_KISS, None, None,\n'
            ')'
        ),
    )
    
    yield (
        'kiss',
        CHEN,
        None,
        (
            '.with_action(\n'
            '    ACTION_TAG_KISS, CHEN, None,\n'
            ')'
        ),
    )
    
    yield (
        'kiss',
        None,
        CHEN,
        (
            '.with_action(\n'
            '    ACTION_TAG_KISS, None, CHEN,\n'
            ')'
        ),
    )
    
    yield (
        'kiss',
        YAKUMO_RAN,
        YAKUMO_YUKARI,
        (
            '.with_action(\n'
            '    ACTION_TAG_KISS, YAKUMO_RAN, YAKUMO_YUKARI,\n'
            ')'
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__render_single_action_into(action_tag, source_character, target_character):
    """
    Tests whether ``_render_single_action_into`` works as intended.
    
    Parameters
    ----------
    action_tag : `str`
        The action tag to render.
    
    source_character : `None | TouhouCharacter`
        Source touhou character.
    
    target_character : `None | TouhouCharacter`
        Target touhou character.
    
    Returns
    -------
    output : `str`
    """
    into = _render_single_action_into([], action_tag, source_character, target_character)
    
    vampytest.assert_instance(into, list)
    for element in into:
        vampytest.assert_instance(element, str)
    return ''.join(into)
