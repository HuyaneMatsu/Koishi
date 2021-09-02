from hata import Client, Embed, mention_user_by_id
from hata.ext.slash import InteractionResponse

from bot_utils.models import DB_ENGINE, user_common_model, USER_COMMON_TABLE, get_create_common_user_expression, \
    waifu_list_model, WAIFU_LIST_TABLE
from bot_utils.shared import EMOJI__HEART_CURRENCY, GUILD__NEKO_DUNGEON

from sqlalchemy.sql import select, desc

SLASH_CLIENT: Client

"""
y = 0
for x in range(0, 13):
    v = x*x*1000
    y += v
    print(y)
"""

WAIFU_COST_DEFAULT = 500

WAIFU_SLOT_COST_DEFAULT = 0

WAIFU_SLOT_2_COST = 5000
WAIFU_SLOT_3_COST = 14000
WAIFU_SLOT_4_COST = 30000
WAIFU_SLOT_5_COST = 55000
WAIFU_SLOT_6_COST = 91000
WAIFU_SLOT_7_COST = 140000
WAIFU_SLOT_8_COST = 204000
WAIFU_SLOT_9_COST = 285000
WAIFU_SLOT_10_COST = 385000
WAIFU_SLOT_11_COST = 506000
WAIFU_SLOT_12_COST = 650000


WAIFU_SLOT_NEXT_COSTS = {
    1: WAIFU_SLOT_2_COST,
    2: WAIFU_SLOT_3_COST,
    3: WAIFU_SLOT_4_COST,
    4: WAIFU_SLOT_5_COST,
    5: WAIFU_SLOT_6_COST,
    6: WAIFU_SLOT_7_COST,
    7: WAIFU_SLOT_8_COST,
    8: WAIFU_SLOT_9_COST,
    9: WAIFU_SLOT_10_COST,
    10: WAIFU_SLOT_11_COST,
    11: WAIFU_SLOT_12_COST,
}


GET_NUMBER_TH_ENDING = {
    1: 'st',
    2: 'nd',
    3: 'rd',
}

DEFAULT_TH_ENDING = 'th'

MAX_WAIFU_SLOTS = 12

@SLASH_CLIENT.interactions(guild=GUILD__NEKO_DUNGEON)
async def buy_waifu_slot(event):
    user_id = event.user.id
    async with DB_ENGINE.connect() as connector:
        response = await connector.execute(
            select(
                [
                    user_common_model.id,
                    user_common_model.waifu_slots,
                    user_common_model.total_love,
                    user_common_model.total_allocated,
                ]
            ).where(
                user_common_model.user_id == user_id,
            )
        )
        
        results = await response.fetchall()
        if results:
            entry_id, waifu_slots, total_love, total_allocated = results[0]
            
            if waifu_slots >= MAX_WAIFU_SLOTS:
                return Embed(
                    None,
                    'You reached the maximal amount of waifu slots.',
                )
            
            available_love = total_love-total_allocated
            required_love = WAIFU_SLOT_NEXT_COSTS.get(waifu_slots, WAIFU_SLOT_COST_DEFAULT)
            
            if (required_love != WAIFU_SLOT_COST_DEFAULT) and (available_love > required_love):
                await connector.execute(
                    USER_COMMON_TABLE.update(
                        user_common_model.id == entry_id,
                    ).values(
                        total_love = user_common_model.total_love-required_love,
                        waifu_slots = user_common_model.waifu_slots+1,
                    )
                )
                
                return Embed(
                    'Great success!',
                    f'Your waifu slots have been increased to {waifu_slots+1} for '
                    f'{required_love} {EMOJI__HEART_CURRENCY.as_emoji}',
                )
        
        else:
            required_love = WAIFU_SLOT_2_COST
            waifu_slots = 1
    
    waifu_slots += 1
    return Embed(
        None,
        'You do not have enough available love to buy more waifu slots.\n'
        f'You need {required_love} {EMOJI__HEART_CURRENCY.as_emoji} to buy the {waifu_slots}'
        f'{GET_NUMBER_TH_ENDING.get(waifu_slots, DEFAULT_TH_ENDING)} slot.',
    )


@SLASH_CLIENT.interactions(guild=GUILD__NEKO_DUNGEON)
async def waifu_info(event,
        user: ('user', 'The user to get') = None,
            ):
    
    if user is None:
        user = event.user
    
    user_id = user.id
    
    async with DB_ENGINE.connect() as connector:
        response = await connector.execute(
            select(
                [
                    user_common_model.waifu_owner_id,
                    user_common_model.waifu_cost,
                    user_common_model.waifu_divorces,
                    user_common_model.waifu_slots,
                ]
            ).where(
                user_common_model.user_id == user_id,
            )
        )
        
        results = await response.fetchall()
        if results:
            waifu_owner_id, waifu_cost, waifu_divorces, waifu_slots = results[0]
            
            response = await connector.execute(
                select(
                    [
                        waifu_list_model.waifu_id,
                    ]
                ).where(
                    waifu_list_model.user_id == user_id,
                )
            )
            
            results = await response.fetchall()
            if results:
                waifu_ids = sorted(result[0] for result in results)
            else:
                waifu_ids = None
        else:
            waifu_owner_id = 0
            waifu_cost = WAIFU_COST_DEFAULT
            waifu_divorces = 0
            waifu_slots = 1
            waifu_ids = None
    
    embed = Embed(
        f'{user.full_name}\'s waifu info'
    )
    
    if waifu_owner_id:
        field_value = mention_user_by_id(waifu_owner_id)
    else:
        field_value = '*none*'
    
    embed.add_field(
        f'Claimed by:',
        field_value,
        inline = True,
    )
    
    if not waifu_cost:
        waifu_cost = WAIFU_COST_DEFAULT
    
    embed.add_field(
        f'Cost:',
        str(waifu_cost),
        inline = True,
    )
    
    embed.add_field(
        'Divorces',
        str(waifu_divorces),
        inline = True,
    )
    
    embed.add_field(
        'Waifu slots',
        str(waifu_slots),
        inline = True,
    )
    
    if waifu_ids is None:
        field_value = '*none*'
    else:
        field_value = '\n'.join(mention_user_by_id(waifu_id) for waifu_id in waifu_ids)
    
    embed.add_field(
        'Waifus',
        field_value,
        inline = True,
    )
    
    return InteractionResponse(embed=embed, allowed_mentions=None)
