__all__ = ()

from random import random
from math import floor

from hata import Client, Embed
from hata.ext.slash import abort

from sqlalchemy.sql import select

from bot_utils.constants import IN_GAME_IDS, EMOJI__HEART_CURRENCY
from bot_utils.models import DB_ENGINE, user_common_model, USER_COMMON_TABLE

SLASH_CLIENT: Client

MULTIPLIERS = (1.7, 2.4, 1.2, 0.5, 0.3, 0.1, 0.2, 1.5,)

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


@SLASH_CLIENT.interactions(is_global = True)
async def lucky_spin(client, event,
    bet: ('int', 'The bet of hearts to bet') = None,
):
    index = floor(random() * 8.0)
    
    if (bet is None):
        description = ARROW_BLOCKS[index]
    else:
        if (bet < 10):
            abort(f'You must bet at least 10 {EMOJI__HEART_CURRENCY}.')
        
        async with DB_ENGINE.connect() as connector:
            response = await connector.execute(
                select(
                    [
                        user_common_model.id,
                        user_common_model.total_love,
                        user_common_model.total_allocated,
                    ]
                ).where(
                    user_common_model.user_id == event.user.id,
                )
            )
            
            result = await response.fetchone()
            if result is None:
                enough_hearts = False
                available_love = 0
            else:
                entry_id, total_love, total_allocated = result
                if (event.user.id in IN_GAME_IDS) and total_allocated:
                    available_love = total_love - total_allocated
                else:
                    available_love = total_love
                
                if bet > available_love:
                    enough_hearts = False
                else:
                    enough_hearts = True
            
            if not enough_hearts:
                abort(f'You have only {available_love} {EMOJI__HEART_CURRENCY} available hearts.')
            
            change = floor((MULTIPLIERS[index]-1.0) * bet)
            
            await connector.execute(
                USER_COMMON_TABLE.update(
                    user_common_model.id == entry_id,
                ).values(
                    total_love = user_common_model.total_love + change,
                )
            )
        
        description = f'{ARROW_BLOCKS[index]}\n\nYou won {bet + change} {EMOJI__HEART_CURRENCY} !'
    
    return Embed(description = description).add_author(f'{client.name}\'s lucky wheel')
