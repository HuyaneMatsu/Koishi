__all__ = ()

from hata import Embed, Emoji
from hata.ext.slash import Button, InteractionResponse, Row

from ..bot_utils.constants import EMOJI__HEART_CURRENCY, MAX_WAIFU_SLOTS, WAIFU_SLOT_COSTS, WAIFU_SLOT_COST_DEFAULT
from ..bots import FEATURE_CLIENTS

from .user_balance import get_user_balance


EMOJI_YES = Emoji.precreate(990558169963049041)
EMOJI_NO = Emoji.precreate(994540311990784041)


CUSTOM_ID_BUY_WAIFU_SLOT_CONFIRM = 'relationship.buy_relationship_slot.confirm'
CUSTOM_ID_BUY_WAIFU_SLOT_CANCEL = 'relationship.buy_relationship_slot.cancel'
CUSTOM_ID_BUY_WAIFU_SLOT_INVOKE = 'relationship.buy_relationship_slot.invoke'


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


@FEATURE_CLIENTS.interactions(custom_id = CUSTOM_ID_BUY_WAIFU_SLOT_INVOKE)
async def buy_relationship_slot_in_inline(event):
    if event.message.interaction.user_id == event.user_id:
        return await buy_relationship_slot_invoke(event)


async def buy_relationship_slot_invoke(event):
    user_id = event.user.id
    
    user_balance = await get_user_balance(user_id)
    relationship_slots = user_balance.relationship_slots
    
    
    if relationship_slots >= MAX_WAIFU_SLOTS:
        return InteractionResponse(
            embed = Embed(
                None,
                'You reached the maximum amount of relationship slots.',
            ),
            components = None,
        )
    
    new_relationship_slot_count = relationship_slots + 1
    available_balance = user_balance.balance - user_balance.allocated
    cost = WAIFU_SLOT_COSTS.get(new_relationship_slot_count, WAIFU_SLOT_COST_DEFAULT)
    
    if (cost != WAIFU_SLOT_COST_DEFAULT) and (available_balance >= cost):
        return InteractionResponse(
            embed = Embed(
                None,
                (
                    f'Are you sure you want to buy your {new_relationship_slot_count}'
                    f'{GET_NUMBER_TH_ENDING.get(new_relationship_slot_count, DEFAULT_TH_ENDING)} relationship slot for '
                    f'{cost} {EMOJI__HEART_CURRENCY.as_emoji}?'
                ),
            ),
            components = BUY_WAIFU_SLOT_COMPONENTS,
        )
    
    return InteractionResponse(
        embed = Embed(
            None,
            (
                'You do not have enough available heart to buy more relationship slots.\n'
                f'You need {cost} {EMOJI__HEART_CURRENCY.as_emoji} to buy the {new_relationship_slot_count}'
                f'{GET_NUMBER_TH_ENDING.get(new_relationship_slot_count, DEFAULT_TH_ENDING)} slot.'
            ),
        ),
        components = None,
    )


@FEATURE_CLIENTS.interactions(custom_id = CUSTOM_ID_BUY_WAIFU_SLOT_CANCEL)
async def buy_relationship_slot_cancel(event):
    if event.user is not event.message.interaction.user:
        return
    
    return InteractionResponse(
        embed = Embed(
            None,
            'The relationship slot purchase has been cancelled.',
        ),
        components = None,
    )

@FEATURE_CLIENTS.interactions(custom_id = CUSTOM_ID_BUY_WAIFU_SLOT_CONFIRM)
async def buy_relationship_slot_confirm(event):
    user = event.user
    if user is not event.message.interaction.user:
        return
    
    user_id = user.id
    
    user_balance = await get_user_balance(user_id)
    relationship_slots = user_balance.relationship_slots
    
    if relationship_slots >= MAX_WAIFU_SLOTS:
        return Embed(
            None,
            'You reached the maximum amount of relationship slots meanwhile.',
        )
    
    new_relationship_slot_count = relationship_slots + 1
    available_balance = user_balance.balance - user_balance.allocated
    cost = WAIFU_SLOT_COSTS.get(new_relationship_slot_count, WAIFU_SLOT_COST_DEFAULT)
    
    if (cost == WAIFU_SLOT_COST_DEFAULT) or (available_balance < cost):
        return InteractionResponse(
            embed = Embed(
                None,
                'Your heart amount or relationship slot amount changed, you cannot buy the next relationship slot anymore.'
            ),
            components = None,
        )
    
    user_balance.set('balance', user_balance.balance - cost)
    user_balance.set('relationship_slots', new_relationship_slot_count)
    await user_balance.save()
    
    return InteractionResponse(
        embed = Embed(
            None,
            (
                f'You bought your {new_relationship_slot_count}'
                f'{GET_NUMBER_TH_ENDING.get(new_relationship_slot_count, DEFAULT_TH_ENDING)} relationship slot for '
                f'{cost} {EMOJI__HEART_CURRENCY.as_emoji}.'
            ),
        ),
        components = None,
    )
