__all__ = ()

from random import random
from math import floor

from hata import DiscordException, ERROR_CODES

from ...bots import FEATURE_CLIENTS

from ..user_balance import get_user_balance

from .checks import check_sufficient_available_balance, check_sufficient_bet
from .constants import BET_LARGE_COIN_THRESHOLD
from .embed_builders import build_success_embed


@FEATURE_CLIENTS.interactions(
    integration_types = ['guild_install', 'user_install'],
    is_global = True,
)
async def coin_flip(
    client,
    interaction_event,
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
    
    interaction_event : ``InteractionEvent``
        The received interaction event.
    
    bet_amount : `int`
        The amount bet.
    
    side : `int`
        The picked side by the user.
    
    Returns
    -------
    output : ``Embed``
    """
    try:
        await client.interaction_application_command_acknowledge(
            interaction_event,
            False,
            show_for_invoking_user_only = True,
        )
    except GeneratorExit:
        raise
    
    except ConnectionError:
        return
    
    except DiscordException as exception:
        if (
            exception.status < 500 and
            exception.code != ERROR_CODES.unknown_interaction
        ):
            raise
        return
    
    user_balance = await get_user_balance(interaction_event.user_id)
    
    check_sufficient_bet(bet_amount)
    balance = user_balance.balance
    check_sufficient_available_balance(balance - user_balance.allocated, bet_amount)
    
    rolled_side = random() > 0.5
    
    if rolled_side == picked_side:
        change = +floor(bet_amount * 0.8)
    else:
        change = -bet_amount
    
    user_balance.set('balance', balance + change)
    await user_balance.save()
    
    try:
        await client.interaction_response_message_edit(interaction_event, '-# _ _')
        await client.interaction_response_message_delete(interaction_event)
        
        await client.interaction_followup_message_create(
            interaction_event,
            embed = build_success_embed(rolled_side, balance, change, bet_amount >= BET_LARGE_COIN_THRESHOLD),
        )
    except GeneratorExit:
        raise
    
    except ConnectionError:
        pass
    
    except DiscordException as exception:
        if (
            exception.status < 500 and
            exception.code != ERROR_CODES.unknown_interaction
        ):
            raise
    
    return
