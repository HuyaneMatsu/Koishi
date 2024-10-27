import vampytest

from ...touhou_core import KOMEIJI_KOISHI, KOMEIJI_SATORI, TouhouHandlerKey

from ..commands_core import build_characters_section_description
from ..constants import STYLE_BLUE, STYLE_GREEN, STYLE_RED, STYLE_RESET


def _iter_options():
    yield (
        None,
        (
            f'```ansi\n'
            f'{STYLE_RESET}{STYLE_RED}'
            f'unknown\n'
            f'```'
        ),
    )
    
    yield (
        (
            TouhouHandlerKey(solo = False),
        ),
        (
            f'```ansi\n'
            f'{STYLE_RESET}{STYLE_BLUE}'
            f'*all*\n'
            f'```'
        ),
    )
    
    yield (
        (
            TouhouHandlerKey(solo = True),
        ),
        (
            f'```ansi\n'
            f'{STYLE_RESET}{STYLE_BLUE}'
            f'*all* (solo)\n'
            f'```'
        ),
    )
    
    yield (
        (
            TouhouHandlerKey(KOMEIJI_KOISHI, solo = False),
            TouhouHandlerKey(KOMEIJI_KOISHI, solo = True),
            TouhouHandlerKey(KOMEIJI_KOISHI, KOMEIJI_SATORI),
        ),
        (
            f'```ansi\n'
            f'{STYLE_RESET}{STYLE_GREEN}'
            f'{KOMEIJI_KOISHI.name}\n'
            f'{KOMEIJI_KOISHI.name} (solo)\n'
            f'{KOMEIJI_KOISHI.name} + {KOMEIJI_SATORI.name}\n'
            f'```'
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_characters_section_description(handler_keys):
    """
    Tests whether ``build_characters_section_description`` works as intended.
    
    Parameters
    ----------
    handler_keys : `tuple<TouhouHandlerKey>`
        The handler keys to render.
    
    Returns
    -------
    output : `str`
    """
    output = build_characters_section_description(handler_keys)
    vampytest.assert_instance(output, str)
    return output
