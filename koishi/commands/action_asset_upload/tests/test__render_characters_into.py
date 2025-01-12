import vampytest

from ....plugins.touhou_core import CHEN, YAKUMO_RAN, YAKUMO_YUKARI

from ..rendering import _render_characters_into


def _iter_options():
    yield (
        {CHEN},
        (
            '.with_character(\n'
            '    CHEN,\n'
            ')'
        ),
    )
    
    yield (
        {YAKUMO_YUKARI, YAKUMO_RAN},
        (
            '.with_characters(\n'
            '    YAKUMO_RAN,\n'
            '    YAKUMO_YUKARI,\n'
            ')'
        ),
    )
    
    yield (
        None,
        (
            ''
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__render_characters_into(characters):
    """
    Tests whether ``_render_characters_into`` works as intended.
    
    Parameters
    ----------
    characters : `None | set<TouhouCharacter>`
        The characters to render.
    
    Returns
    -------
    output : `str`
    """
    into = _render_characters_into([], characters)
    
    vampytest.assert_instance(into, list)
    for element in into:
        vampytest.assert_instance(element, str)
    return ''.join(into)
