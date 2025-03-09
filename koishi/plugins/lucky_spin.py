__all__ = ()

from decimal import Decimal
from random import random
from math import floor

from hata import Embed
from hata.ext.slash import abort

from ..bot_utils.constants import EMOJI__HEART_CURRENCY
from ..bots import FEATURE_CLIENTS

from .user_balance import get_user_balance


MULTIPLIERS = (*(Decimal(value) / 100 for value in (170, 240, 120, 50, 30, 10, 20, 150,)),)

ARROW_BLOCKS = tuple(
    (
        f'```\n'
        f'「{MULTIPLIERS[(7 + push) % 8]:.01f}」    「{MULTIPLIERS[(0 + push) % 8]:.01f}」    「{MULTIPLIERS[(1 + push) % 8]:.01f}」\n'
        f'\n'
        f'　　       　/|\\\n'
        f'「{MULTIPLIERS[(6 + push) % 8]:.01f}」   　/ | \\　   「{MULTIPLIERS[(2 + push) % 8]:.01f}」\n'
        f'　　        　|\n'
        f'\n'
        f'「{MULTIPLIERS[(5 + push) % 8]:.01f}」    「{MULTIPLIERS[(4 + push) % 8]:.01f}」    「{MULTIPLIERS[(3 + push) % 8]:.01f}」\n'
        f'```'
    ) for push in range(8)
)


@FEATURE_CLIENTS.interactions(
    integration_types = ['guild_install', 'user_install'],
    is_global = True,
)
async def lucky_spin(client, event,
    bet: ('int', 'The bet of hearts to bet') = None,
):
    """Test your luck, spin the wheel!"""
    index = floor(random() * 8.0)
    
    if (bet is None):
        description = ARROW_BLOCKS[index]
    else:
        if (bet < 10):
            return abort(f'You must bet at least 10 {EMOJI__HEART_CURRENCY}.')
        
        user_balance = await get_user_balance(event.user_id)
        balance = user_balance.balance
        available = balance - user_balance.allocated
        
        if (bet > available):
            return abort(f'You have only {available} {EMOJI__HEART_CURRENCY} available hearts.')
        
        change = floor((MULTIPLIERS[index] - Decimal(1)) * bet)
        
        user_balance.set('balance', balance + change)
        await user_balance.save()
        
        description = f'{ARROW_BLOCKS[index]}\n\nYou won {bet + change} {EMOJI__HEART_CURRENCY} !'
    
    return Embed(description = description).add_author(f'{client.name}\'s lucky wheel')
