import vampytest

from ....plugins.touhou_core import YAKUMO_RAN, YAKUMO_YUKARI

from ..rendering import _produce_multiple_action


def _iter_options():
    yield (
        (
            (
                'kiss',
                None,
                None,
            ),
            (
                'kiss',
                YAKUMO_RAN,
                YAKUMO_YUKARI,
            ),
        ),
        (
            '.with_actions(\n'
            '    (ACTION_TAG_KISS, None, None),\n'
            '    (ACTION_TAG_KISS, YAKUMO_RAN, YAKUMO_YUKARI),\n'
            ')'
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__produce_multiple_action(items):
    """
    Tests whether ``_produce_multiple_action`` works as intended.
    
    Parameters
    ----------
    items : `tuple<(str, None | TouhouCharacter, None | TouhouCharacter)>`
        Action items to produce.
    
    Returns
    -------
    output : `str`
    """
    output = [*_produce_multiple_action(*items)]
    
    for element in output:
        vampytest.assert_instance(element, str)
    
    return ''.join(output)
