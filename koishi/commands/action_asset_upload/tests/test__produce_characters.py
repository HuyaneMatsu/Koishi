import vampytest

from ....plugins.touhou_core import CHEN, YAKUMO_RAN, YAKUMO_YUKARI

from ..rendering import _produce_characters


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
def test__produce_characters(characters):
    """
    Tests whether ``_produce_characters`` works as intended.
    
    Parameters
    ----------
    characters : `None | set<TouhouCharacter>`
        The characters to render.
    
    Returns
    -------
    output : `str`
    """
    output = [*_produce_characters(characters)]
    
    for element in output:
        vampytest.assert_instance(element, str)
        
    return ''.join(output)
