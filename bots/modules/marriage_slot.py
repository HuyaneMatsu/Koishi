__all__ = ()

from hata import Client, Embed, Emoji
from hata.ext.slash import Button, InteractionResponse, Row
from sqlalchemy.sql import select

from bot_utils.constants import (
    EMOJI__HEART_CURRENCY, MAX_WAIFU_SLOTS, WAIFU_SLOT_2_COST, WAIFU_SLOT_COSTS, WAIFU_SLOT_COST_DEFAULT
)
from bot_utils.models import DB_ENGINE, USER_COMMON_TABLE, user_common_model


SLASH_CLIENT: Client


EMOJI_YES = Emoji.precreate(990558169963049041)
EMOJI_NO = Emoji.precreate(994540311990784041)


CUSTOM_ID_BUY_WAIFU_SLOT_CONFIRM = 'marriage.buy_waifu_slot.confirm'
CUSTOM_ID_BUY_WAIFU_SLOT_CANCEL = 'marriage.buy_waifu_slot.cancel'
CUSTOM_ID_BUY_WAIFU_SLOT_INVOKE = 'marriage.buy_waifu_slot.invoke'


GET_NUMBER_TH_ENDING = {
    1: 'st',
    2: 'nd',
    3: 'rd',
}

DEFAULT_TH_ENDING = 'th'



BUY_WAIFU_SLOT_COMPONENTS = Row(
    Button(
        'Yes',
        EMOJI_YES,
        custom_id = CUSTOM_ID_BUY_WAIFU_SLOT_CONFIRM,
    ),
    Button(
        'No',
        EMOJI_NO,
        custom_id = CUSTOM_ID_BUY_WAIFU_SLOT_CANCEL,
    ),
)

BUY_WAIFU_SLOT_INVOKE_COMPONENT = Button(
    'I want some More! More!',
    custom_id = CUSTOM_ID_BUY_WAIFU_SLOT_INVOKE,
)


@SLASH_CLIENT.interactions(custom_id = CUSTOM_ID_BUY_WAIFU_SLOT_INVOKE)
async def buy_waifu_slot_in_inline(event):
    if event.message.interaction.user is event.user:
        return await buy_waifu_slot_invoke(event)


async def buy_waifu_slot_invoke(event):
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
            new_waifu_slot_count = waifu_slots + 1
            
            if waifu_slots >= MAX_WAIFU_SLOTS:
                return
                InteractionResponse(
                    Embed(
                        None,
                        'You reached the maximum amount of waifu slots.',
                    ),
                    components = None,
                )
            
            available_love = total_love - total_allocated
            required_love = WAIFU_SLOT_COSTS.get(new_waifu_slot_count, WAIFU_SLOT_COST_DEFAULT)
            
            if (required_love != WAIFU_SLOT_COST_DEFAULT) and (available_love >= required_love):
                return InteractionResponse(
                    embed = Embed(
                        None,
                        (
                            f'Are you sure you want to buy your {new_waifu_slot_count}'
                            f'{GET_NUMBER_TH_ENDING.get(new_waifu_slot_count, DEFAULT_TH_ENDING)} waifu slot for '
                            f'{required_love} {EMOJI__HEART_CURRENCY.as_emoji}?'
                        ),
                    ),
                    components = BUY_WAIFU_SLOT_COMPONENTS,
                )
        
        else:
            required_love = WAIFU_SLOT_2_COST
            new_waifu_slot_count = 2
    
    return InteractionResponse(
        Embed(
            None,
            (
                'You do not have enough available love to buy more waifu slots.\n'
                f'You need {required_love} {EMOJI__HEART_CURRENCY.as_emoji} to buy the {new_waifu_slot_count}'
                f'{GET_NUMBER_TH_ENDING.get(new_waifu_slot_count, DEFAULT_TH_ENDING)} slot.'
            ),
        ),
        components = None,
    )


@SLASH_CLIENT.interactions(custom_id = CUSTOM_ID_BUY_WAIFU_SLOT_CANCEL)
async def buy_marriage_slot_cancel(event):
    if event.user is not event.message.interaction.user:
        return
    
    return InteractionResponse(
        Embed(
            None,
            'The waifu slot purchase has been cancelled.',
        ),
        components = None,
    )

@SLASH_CLIENT.interactions(custom_id = CUSTOM_ID_BUY_WAIFU_SLOT_CONFIRM)
async def buy_marriage_slot_confirm(event):
    user = event.user
    if user is not event.message.interaction.user:
        return
    
    user_id = user.id
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
        if not results:
            return
            
        entry_id, waifu_slots, total_love, total_allocated = results[0]
        new_waifu_slot_count = waifu_slots + 1
        
        if waifu_slots >= MAX_WAIFU_SLOTS:
            return Embed(
                None,
                'You reached the maximum amount of waifu slots meanwhile.',
            )
        
        available_love = total_love - total_allocated
        required_love = WAIFU_SLOT_COSTS.get(new_waifu_slot_count, WAIFU_SLOT_COST_DEFAULT)
        
        if (required_love == WAIFU_SLOT_COST_DEFAULT) or (available_love < required_love):
            return InteractionResponse(
                embed = Embed(
                    None,
                    'Your heart amount or waifu slot amount changed, you cannot buy the next waifu slot anymore.'
                ),
                components = None,
            )
        
        await connector.execute(
            USER_COMMON_TABLE.update(
                user_common_model.id == entry_id,
            ).values(
                total_love = user_common_model.total_love - required_love,
                waifu_slots = user_common_model.waifu_slots + 1,
            )
        )
        
        return InteractionResponse(
            embed = Embed(
                None,
                (
                    f'You bought your {new_waifu_slot_count}'
                    f'{GET_NUMBER_TH_ENDING.get(new_waifu_slot_count, DEFAULT_TH_ENDING)} waifu slot for '
                    f'{required_love} {EMOJI__HEART_CURRENCY.as_emoji}.'
                ),
            ),
            components = None,
        )
