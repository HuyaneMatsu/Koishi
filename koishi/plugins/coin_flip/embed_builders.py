__all__ = ()

from hata import Embed

from ...bot_utils.constants import COLOR__GAMBLING, EMOJI__HEART_CURRENCY

from .constants import ASSET_URL_KOISHI_COIN_EYE, ASSET_URL_KOISHI_COIN_HAT, BET_MIN


def build_failure_embed_insufficient_bet():
    """
    Builds a failure embed for the case when the bet amount is too low.
    
    Returns
    -------
    embed : ``Embed``
    """
    return Embed(
        'Insufficient bet',
        f'You must be at least {BET_MIN} {EMOJI__HEART_CURRENCY}.',
        color = COLOR__GAMBLING,
    )


def build_failure_embed_insufficient_available_balance(available_balance, bet_amount):
    """
    Builds a failure embed for the case when the bet amount is higher than the available balance.
    
    Parameters
    ----------
    available_balance : `int`
        The available balance of the user.
    
    bet_amount : `int`
        The amount the user bet.
    
    Returns
    -------
    embed : ``Embed``
    """
    return Embed(
        'Insufficient available balance',
        (
            f'You cannot bet {bet_amount} {EMOJI__HEART_CURRENCY}, '
            f'you have only {available_balance} {EMOJI__HEART_CURRENCY} available.'
        ),
        color = COLOR__GAMBLING,
    )


def build_success_embed(rolled_side, balance_before, change):
    """
    Builds a success embed when the coin is flipped. Just because it is a success embed it does not mean the player won.
    
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
    embed : ``Embed``
    """
    return Embed(
        f'{"Eye" if rolled_side else "Hat"}!',
        f'You {"won" if change > 0 else "lost"} {abs(change)} {EMOJI__HEART_CURRENCY}.',
        color = COLOR__GAMBLING,
    ).add_thumbnail(
        ASSET_URL_KOISHI_COIN_EYE if rolled_side else ASSET_URL_KOISHI_COIN_HAT,
    ).add_field(
        f'Your {EMOJI__HEART_CURRENCY}',
        (
            f'```\n'
            f'{balance_before} -> {balance_before + change}\n'
            f'```'
        ),
    )
