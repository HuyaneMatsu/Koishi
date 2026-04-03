from hata import Embed

import vampytest

from ....bot_utils.constants import EMOJI__HEART_CURRENCY

from ..constants import COLOR_CODE_GREEN, COLOR_CODE_RED, COLOR_CODE_RESET
from ..change import add_modification_embed_field


def _iter_options():
    yield (
        'mister',
        1000,
        +100,
        Embed().add_field(
            'mister',
            (
                f'```ansi\n'
                f'1000 {COLOR_CODE_GREEN}->{COLOR_CODE_RESET} 1100\n'
                f'```'
            ),
            True,
        ),
    )
    
    yield (
        'mister',
        1000,
        -100,
        Embed().add_field(
            'mister',
            (
                f'```ansi\n'
                f'1000 {COLOR_CODE_RED}->{COLOR_CODE_RESET} 900\n'
                f'```'
            ),
            True,
        ),
    )
    
    yield (
        'mister',
        1000,
        0,
        Embed().add_field(
            'mister',
            (
                f'```ansi\n'
                f'1000 -> 1000\n'
                f'```'
            ),
            True,
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__add_modification_embed_field(title, balance, modification):
    """
    Tests whether ``add_modification_embed_field`` works as intended.
    
    Parameters
    ----------
    title : `str`
        Title to use.
    
    balance : `int`
        The balance before the action.
    
    modification : `int`
        Balance modification.
    
    Returns
    -------
    embed : ``Embed``
    """
    output = add_modification_embed_field(Embed(), title, balance, modification)
    vampytest.assert_instance(output, Embed)
    return output
