import vampytest
from hata import Embed

from ....bot_utils.constants import COLOR__GAMBLING, EMOJI__HEART_CURRENCY

from ..constants import ASSET_URL_KOISHI_COIN_EYE, ASSET_URL_KOISHI_COIN_HAT
from ..embed_builders import build_success_embed


def _iter_options():
    yield (
        0,
        300,
        +100,
        Embed(
            'Hat!',
            f'You won 100 {EMOJI__HEART_CURRENCY}.',
            color = COLOR__GAMBLING,
        ).add_thumbnail(
            ASSET_URL_KOISHI_COIN_HAT,
        ).add_field(
            f'Your {EMOJI__HEART_CURRENCY}',
            (
                '```\n'
                '300 -> 400\n'
                '```'
            ),
        ),
    )
    
    yield (
        1,
        300,
        +100,
        Embed(
            'Eye!',
            f'You won 100 {EMOJI__HEART_CURRENCY}.',
            color = COLOR__GAMBLING,
        ).add_thumbnail(
            ASSET_URL_KOISHI_COIN_EYE,
        ).add_field(
            f'Your {EMOJI__HEART_CURRENCY}',
            (
                '```\n'
                '300 -> 400\n'
                '```'
            ),
        ),
    )
    
    yield (
        0,
        300,
        -100,
        Embed(
            'Hat!',
            f'You lost 100 {EMOJI__HEART_CURRENCY}.',
            color = COLOR__GAMBLING,
        ).add_thumbnail(
            ASSET_URL_KOISHI_COIN_HAT,
        ).add_field(
            f'Your {EMOJI__HEART_CURRENCY}',
            (
                '```\n'
                '300 -> 200\n'
                '```'
            ),
        ),
    )
    
    yield (
        1,
        300,
        -100,
        Embed(
            'Eye!',
            f'You lost 100 {EMOJI__HEART_CURRENCY}.',
            color = COLOR__GAMBLING,
        ).add_thumbnail(
            ASSET_URL_KOISHI_COIN_EYE,
        ).add_field(
            f'Your {EMOJI__HEART_CURRENCY}',
            (
                '```\n'
                '300 -> 200\n'
                '```'
            ),
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_success_embed(rolled_side, balance_before, change):
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
    
    Returns
    -------
    output : ``Embed``
    """
    output = build_success_embed(rolled_side, balance_before, change)
    vampytest.assert_instance(output, Embed)
    return output
