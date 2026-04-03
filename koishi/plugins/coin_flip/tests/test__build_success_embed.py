import vampytest
from hata import Embed

from ....bot_utils.constants import COLOR__GAMBLING, EMOJI__HEART_CURRENCY

from ...balance_rendering.constants import COLOR_CODE_GREEN, COLOR_CODE_RED, COLOR_CODE_RESET

from ..constants import ASSET_URL_KOISHI_COIN_EYE, ASSET_URL_KOISHI_COIN_HAT
from ..embed_builders import build_success_embed


def _iter_options():
    yield (
        0,
        300,
        +100,
        False,
        Embed(
            'Hat!',
            f'You won 100 {EMOJI__HEART_CURRENCY}.',
            color = COLOR__GAMBLING,
        ).add_thumbnail(
            ASSET_URL_KOISHI_COIN_HAT,
        ).add_field(
            f'Your {EMOJI__HEART_CURRENCY}',
            (
                f'```ansi\n'
                f'300 {COLOR_CODE_GREEN}->{COLOR_CODE_RESET} 400\n'
                f'```'
            ),
            True,
        ),
    )
    
    yield (
        1,
        300,
        +100,
        False,
        Embed(
            'Eye!',
            f'You won 100 {EMOJI__HEART_CURRENCY}.',
            color = COLOR__GAMBLING,
        ).add_thumbnail(
            ASSET_URL_KOISHI_COIN_EYE,
        ).add_field(
            f'Your {EMOJI__HEART_CURRENCY}',
            (
                f'```ansi\n'
                f'300 {COLOR_CODE_GREEN}->{COLOR_CODE_RESET} 400\n'
                f'```'
            ),
            True,
        ),
    )
    
    yield (
        0,
        300,
        -100,
        False,
        Embed(
            'Hat!',
            f'You lost 100 {EMOJI__HEART_CURRENCY}.',
            color = COLOR__GAMBLING,
        ).add_thumbnail(
            ASSET_URL_KOISHI_COIN_HAT,
        ).add_field(
            f'Your {EMOJI__HEART_CURRENCY}',
            (
                f'```ansi\n'
                f'300 {COLOR_CODE_RED}->{COLOR_CODE_RESET} 200\n'
                f'```'
            ),
            True,
        ),
    )
    
    yield (
        1,
        300,
        -100,
        False,
        Embed(
            'Eye!',
            f'You lost 100 {EMOJI__HEART_CURRENCY}.',
            color = COLOR__GAMBLING,
        ).add_thumbnail(
            ASSET_URL_KOISHI_COIN_EYE,
        ).add_field(
            f'Your {EMOJI__HEART_CURRENCY}',
            (
                f'```ansi\n'
                f'300 {COLOR_CODE_RED}->{COLOR_CODE_RESET} 200\n'
                f'```'
            ),
            True,
        ),
    )
    
    # large coin
    yield (
        0,
        300,
        +100,
        True,
        Embed(
            'Hat!',
            f'You won 100 {EMOJI__HEART_CURRENCY}.',
            color = COLOR__GAMBLING,
        ).add_image(
            ASSET_URL_KOISHI_COIN_HAT,
        ).add_field(
            f'Your {EMOJI__HEART_CURRENCY}',
            (
                f'```ansi\n'
                f'300 {COLOR_CODE_GREEN}->{COLOR_CODE_RESET} 400\n'
                f'```'
            ),
            True,
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_success_embed(rolled_side, balance_before, change, large_coin):
    """
    Tests whether ``build_success_embed`` works as intend.
    
    Parameters
    ----------
    rolled_side : `int`
        The rolled side by the user.
    
    balance_before : `int`
        The user's balance before betting.
    
    change : `int`
        The change in user balance.
    
    large_coin : `bool`
        Whether large coin should be shown.
    
    Returns
    -------
    output : ``Embed``
    """
    output = build_success_embed(rolled_side, balance_before, change, large_coin)
    vampytest.assert_instance(output, Embed)
    return output
