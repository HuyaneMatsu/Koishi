__all__ = ()

from decimal import Decimal
from random import random
from math import floor

from hata import DiscordException, ERROR_CODES

from ...bot_utils.constants import EMOJI__HEART_CURRENCY
from ...bots import FEATURE_CLIENTS

from ..user_balance import get_user_balance

from .component_building import build_lucky_spin_response_components
from .constants import BET_MIN, MULTIPLIERS


@FEATURE_CLIENTS.interactions(
    integration_types = ['guild_install', 'user_install'],
    is_global = True,
)
async def lucky_spin(
    client,
    interaction_event,
    bet: ('int', 'The bet of hearts to bet'),
):
    """
    Test your luck, spin the wheel!
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    
    interaction_event : ``InteractionEvent``
        The received interaction event.
    
    bet : `int`
        How much is the user betting.
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
    
    index = floor(random() * 8.0)
    
    if (bet < BET_MIN):
        try:
            await client.interaction_response_message_edit(
                interaction_event,
                f'You must bet at least {BET_MIN} {EMOJI__HEART_CURRENCY}.',
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
    
    user_balance = await get_user_balance(interaction_event.user_id)
    balance = user_balance.balance
    available = balance - user_balance.allocated
    
    if (bet > available):
        try:
            await client.interaction_response_message_edit(
                interaction_event,
                f'You have only {available} {EMOJI__HEART_CURRENCY} available hearts.',
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
    
    change = floor((MULTIPLIERS[index] - Decimal(1)) * bet)
    
    user_balance.set('balance', balance + change)
    await user_balance.save()
    
    try:
        await client.interaction_response_message_edit(interaction_event, '-# _ _')
        await client.interaction_response_message_delete(interaction_event)
        
        await client.interaction_followup_message_create(
            interaction_event,
            components = build_lucky_spin_response_components(client, interaction_event.guild_id, index, bet + change),
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
