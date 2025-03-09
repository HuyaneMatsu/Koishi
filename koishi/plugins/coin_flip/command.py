__all__ = ()

from random import random
from math import floor

from ...bots import FEATURE_CLIENTS

from ..user_balance import get_user_balance

from .checks import check_sufficient_available_balance, check_sufficient_bet 
from .embed_builders import build_success_embed


@FEATURE_CLIENTS.interactions(
    integration_types = ['guild_install', 'user_install'],
    is_global = True,
)
async def coin_flip(
    event,
    bet_amount: (int, 'The bet of hearts to bet?', 'bet'),
    picked_side : ([('hat', 0), ('eye', 1)], 'Pick a side', 'side'),
):
    """
    Flip a coin and win 180% of your bet, or lose all.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    
    event : ``InteractionEvent``
        The received interaction event.
    
    bet_amount : `int`
        The amount bet.
    
    side : `int`
        The picked side by the user.
    
    Returns
    -------
    output : ``Embed``
    """
    check_sufficient_bet(bet_amount)
    user_balance = await get_user_balance(event.user_id)
    balance = user_balance.balance
    check_sufficient_available_balance(balance - user_balance.allocated, bet_amount)
    
    rolled_side = random() > 0.5
    
    if rolled_side == picked_side:
        change = +floor(bet_amount * 0.8)
    else:
        change = -bet_amount
    
    user_balance.set('balance', balance + change)
    await user_balance.save()
    
    return build_success_embed(rolled_side, balance, change)
