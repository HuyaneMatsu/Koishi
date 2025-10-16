import vampytest

from ..font import TextWallFont
from ..modes import build_horizontal


def _iter_options():
    font = TextWallFont(
        'pudding',
        1,
        2,
        {
            'a': b'\x00\x01',
            'b': b'\x02\x02',
        },
    )
    
    yield (
        font,
        'a',
        (
            '_ _',
            ' ',
            'X',
        ),
        (
            '_ _\n'
            ' '
        )
    )
    
    yield (
        font,
        'ab',
        (
            '_ _',
            ' ',
            'X',
        ),
        (
            '_ _X\n'
            ' X'
        )
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_horizontal(font, text, replace_resolution_table):
    """
    Tests whether ``build_horizontal`` works as intended.
    
    Parameters
    ----------
    font : ``TextWallFont``
        Text wall font to use,
    
    text : `str`
        text to produce from
    
    replace_resolution_table : `tuple<str>`
        Character used to produce the replace output.
    
    Returns
    -------
    output : `str`
    """
    output = build_horizontal(font, text, replace_resolution_table)
    vampytest.assert_instance(output, str)
    return output
