import vampytest

from ...touhou_core import KOMEIJI_KOISHI, KOMEIJI_SATORI, TouhouHandlerKey

from ..commands_core import render_handler_keys_into
from ..constants import STYLE_BLUE, STYLE_GREEN


def _iter_options():
    yield (
        (
            TouhouHandlerKey(KOMEIJI_KOISHI, solo = False),
            TouhouHandlerKey(KOMEIJI_KOISHI, solo = True),
            TouhouHandlerKey(KOMEIJI_KOISHI, KOMEIJI_SATORI),
        ),
        990,
        (
            f'{STYLE_GREEN}'
            f'{KOMEIJI_KOISHI.name}\n'
            f'{KOMEIJI_KOISHI.name} (solo)\n'
            f'{KOMEIJI_KOISHI.name} + {KOMEIJI_SATORI.name}'
        ),
    )
    
    yield (
        (
            TouhouHandlerKey(KOMEIJI_KOISHI, solo = False),
            TouhouHandlerKey(KOMEIJI_KOISHI, solo = True),
            TouhouHandlerKey(KOMEIJI_KOISHI, KOMEIJI_SATORI),
        ),
        50,
        (
            f'{STYLE_GREEN}'
            f'{KOMEIJI_KOISHI.name}\n'
            f'{KOMEIJI_KOISHI.name} (solo)\n'
            f'{STYLE_BLUE}'
            f'... + 1'
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__render_handler_keys_into(handler_keys, truncate_after):
    """
    Tests whether ``render_handler_keys_into`` works as intended.
    
    Parameters
    ----------
    handler_keys : `tuple<TouhouHandlerKey>`
        The handler keys to render.
    
    truncate_after : `int`
        The amount of characters to truncate after.
    
    Returns
    -------
    output : `str`
    """
    into = render_handler_keys_into([], handler_keys, truncate_after)
    vampytest.assert_instance(into, list)
    for element in into:
        vampytest.assert_instance(element, str)
    return ''.join(into)
