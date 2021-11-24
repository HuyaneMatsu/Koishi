from random import random
from math import floor

from hata import Client, Embed
from hata.ext.slash import abort

from sqlalchemy.sql import select

from bot_utils.constants import GUILD__SUPPORT, IN_GAME_IDS, EMOJI__HEART_CURRENCY
from bot_utils.models import DB_ENGINE, user_common_model, USER_COMMON_TABLE

SLASH_CLIENT: Client

MULTIPLIERS = (0.4, 0.6, 1.0, 1,4, 1,6, 1.2, 0.8, 0.2,)

ARROWS = (
    (
        '\\¨ ',
        '|\\ ',
        '  \\',
    ), (
        '/|\\',
        ' | ',
        ' | ',
    ), (
        ' ¨/',
        ' /|',
        '/  ',
    ), (
        '   ',
        '<--',
        '   ',
    ), (
        '   ',
        '-->',
        '   ',
    ), (
        '  /',
        '|/ ',
        '/_ ',
    ), (
        ' | ',
        ' | ',
        '\\|/',
    ), (
        '\\  ',
        ' \\|',
        ' _\\',
    )
)

ARROW_BLOCKS = tuple(
    (
        f'```py'
        f'[{MULTIPLIERS[0]:.01f}]' f'    ' f'[{MULTIPLIERS[1]:.01f}]' f'    ' f'[{MULTIPLIERS[2]:.01f}]' f'\n'
        f'     '                   f'    ' f'     '                   f'    ' f'     '                   f'\n'
        f'     '                   f'    ' f' [{arrow[0]}] '          f'    ' f'     '                   f'\n'
        f'[{MULTIPLIERS[3]:.01f}]' f'    ' f' [{arrow[1]}] '          f'    ' f'[{MULTIPLIERS[4]:.01f}]' f'\n'
        f'     '                   f'    ' f' [{arrow[2]}] '          f'    ' f'     '                   f'\n'
        f'     '                   f'    ' f'     '                   f'    ' f'     '                   f'\n'
        f'[{MULTIPLIERS[5]:.01f}]' f'    ' f'[{MULTIPLIERS[6]:.01f}]' f'    ' f'[{MULTIPLIERS[7]:.01f}]' f'\n'
        f'```'
    ) for arrow in ARROWS
)



@SLASH_CLIENT.interactions(guild=GUILD__SUPPORT)
async def lucky_spin(client, event,
    amount: ('int', 'The amount of hearts to bet') = None,
):
    index = floor(random()*8.0)
    
    if (amount is None):
        description = ARROW_BLOCKS[index]
    else:
        if (amount < 10):
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
                    available_love = total_love-total_allocated
                else:
                    available_love = total_love
                
                if amount > available_love:
                    enough_hearts = False
                else:
                    enough_hearts = True
            
            if not enough_hearts:
                abort(f'You have only {available_love} {EMOJI__HEART_CURRENCY} available hearts.')
            
            change = floor((MULTIPLIERS[index]-1.0)*amount)
            
            await connector.execute(
                USER_COMMON_TABLE.update(
                    user_common_model.id == entry_id,
                ).values(
                    total_love = user_common_model.total_love+change,
                )
            )
        
        if change < 0:
            change = -change
            state = 'lost'
        else:
            state = 'won'
        
        description = f'{ARROW_BLOCKS[index]}\n\nYou have {state} {change} {EMOJI__HEART_CURRENCY} !'
    
    return Embed(description=description).add_author(client.avatar_url, f'{client.name}\'s lucky spin')
