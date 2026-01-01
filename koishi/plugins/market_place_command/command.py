__all__ = ()

from datetime import datetime as DateTime, timezone as TimeZone
from math import floor, inf, isnan as is_nan

from hata.ext.slash import P

from ...bot_utils.constants import EMOJI__HEART_CURRENCY
from ...bots import FEATURE_CLIENTS

from ..adventure_core import get_active_adventure
from ..inventory_core import create_item_suggestions, get_inventory, select_item
from ..market_place_core import (
    get_market_place_item_listing_active, get_market_place_item_listing_inbox, get_market_place_item_listing_own_offers
)
from ..user_balance import get_user_balance

from .component_building import (
    build_inbox_view_components, build_own_offers_view_components, build_purchase_view_components,
    build_sell_confirmation_form
)
from .constants import (
    DURATION_DAYS_DEFAULT, DURATION_DAYS_THRESHOLD_LOWER, DURATION_DAYS_THRESHOLD_UPPER, ITEM_CATEGORY_CHOICES,
    PAGE_SIZE_DEFAULT
)
from .helpers import calculate_initial_sell_fee
from .item_name_auto_completion import (
    get_best_matching_item, get_item_name_suggestions, item_category_to_required_flags
)


MARKET_PLACE_COMMANDS = FEATURE_CLIENTS.interactions(
    None,
    is_global = True,
    name = 'market_place',
)


@MARKET_PLACE_COMMANDS.interactions(
    name = 'sell',
)
async def command_sell(
    client,
    interaction_event,
    item_name : P(str, 'The item\'s name.', 'item'),
    amount : P('expression', 'The amount of items to sell.') = (1 << 64) - 1,
    duration_days : P(
        [*range(DURATION_DAYS_THRESHOLD_LOWER, DURATION_DAYS_THRESHOLD_UPPER + 1)],
        'The amount of days the item will be auctioned for.',
        'days',
    ) = DURATION_DAYS_DEFAULT,
    starting_sell_price : ('expression', 'The minimal amount to sell the item for.', 'starting-sell-price') = None,
):
    """
    Sell an item of yours.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client receiving the event.
    
    interaction_event : ``InteractionEvent``
        The received interaction event.
    
    item_name : `str`
        The selected item's name.
    
    amount : `int | float` = `(1 << 64) - 1`
        The amount of item to discard.
    
    duration_days : `int` = `8`
        The amount of days the item will be auctioned for.
    
    starting_sell_price : `int | float` = `0`
        Starting sell price.
    """
    while True:
        adventure = await get_active_adventure(interaction_event.user_id)
        if (adventure is not None):
            error_message = 'You cannot sell while on adventure.'
            break
        
        # Validate amount
        if isinstance(amount, float):
            if is_nan(amount):
                amount = 0
            
            elif amount == inf:
                amount = (1 << 64) - 1
            
            elif amount == -inf:
                amount = -1
            
            else:
                amount = floor(amount)
        
        if amount <= 0:
            error_message = 'You cannot sell non positive amount of items.'
            break
        
        # Validate sell price
        
        if starting_sell_price is None:
            starting_sell_price = 0
        
        elif isinstance(starting_sell_price, float):
            if is_nan(starting_sell_price):
                starting_sell_price = 0
            
            elif starting_sell_price == inf:
                starting_sell_price = (1 << 64) - 1
            
            elif starting_sell_price == -inf:
                starting_sell_price = -1
            
            else:
                starting_sell_price = floor(starting_sell_price)
        
        else:
            # It is int, but we do nothing.
            pass
        
        if starting_sell_price > 1000000:
            error_message = f'Starting sell price cannot be higher than a million.'
            break
        
        if starting_sell_price < 0:
            starting_sell_price = 0
        
        # Validate item
        inventory = await get_inventory(interaction_event.user_id)
        item = select_item(inventory, 0, item_name)
        if item is None:
            error_message = f'You do not have an item called: {item_name!s}.'
            break
        
        # Item amount
        item_amount = min(inventory.get_item_amount(item), amount)
        
        # Initial sell fee
        user_balance = await get_user_balance(interaction_event.user_id)
        
        initial_sell_fee = calculate_initial_sell_fee(item, item_amount, duration_days, starting_sell_price)
        
        balance = user_balance.balance
        allocated_balance = user_balance.get_cumulative_allocated_balance()
        available_balance = balance - allocated_balance
        if initial_sell_fee > available_balance:
            error_message = (
                f'You have only {available_balance!s} available {EMOJI__HEART_CURRENCY}, '
                f'which is lower than the required {initial_sell_fee!s} sell fee.'
            )
            break
        
        await client.interaction_form_send(
            interaction_event,
            build_sell_confirmation_form(item, item_amount, duration_days, starting_sell_price, initial_sell_fee),
        )
        return
    
    await client.interaction_response_message_create(
        interaction_event,
        allowed_mentions = None,
        content = error_message,
        show_for_invoking_user_only = True,
    )


@command_sell.autocomplete('item_name')
async def command_sell_autocomplete_item_name(interaction_event, value):
    """
    Gets item suggestions for the given value.
    
    This function is a coroutine.
    
    Parameters
    ----------
    interaction_event : ``InteractionEvent``
        The received interaction event.
    
    value : `None | str`
        Value to filter for.
    
    Returns
    -------
    suggestions : `None | list<(str, int)>`
    """
    inventory = await get_inventory(interaction_event.user_id)
    return create_item_suggestions(inventory, 0, value)


@MARKET_PLACE_COMMANDS.interactions(
    name = 'own-offers',
)
async def command_own_offers(
    client,
    interaction_event,
):
    """
    View your own offers.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client receiving the event.
    
    interaction_event : ``InteractionEvent``
        The received interaction event.
    """
    await client.interaction_application_command_acknowledge(
        interaction_event,
        False,
    )
    
    now = DateTime.now(TimeZone.utc)
    
    market_place_item_listing, has_more = await get_market_place_item_listing_own_offers(
        interaction_event.user_id, now, 0, PAGE_SIZE_DEFAULT
    )
    
    await client.interaction_response_message_edit(
        interaction_event,
        components = build_own_offers_view_components(
            interaction_event.user,
            interaction_event.guild_id,
            now,
            0,
            PAGE_SIZE_DEFAULT,
            market_place_item_listing,
            has_more,
        ),
    )


@MARKET_PLACE_COMMANDS.interactions(
    name = 'inbox',
)
async def command_inbox(
    client,
    interaction_event,
):
    """
    View your inbox.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client receiving the event.
    
    interaction_event : ``InteractionEvent``
        The received interaction event.
    """
    await client.interaction_application_command_acknowledge(
        interaction_event,
        False,
    )
    
    now = DateTime.now(TimeZone.utc)
    
    market_place_item_listing, has_more = await get_market_place_item_listing_inbox(
        interaction_event.user_id, now, 0, PAGE_SIZE_DEFAULT
    )
    
    await client.interaction_response_message_edit(
        interaction_event,
        components = build_inbox_view_components(
            interaction_event.user,
            interaction_event.guild_id,
            now,
            0,
            PAGE_SIZE_DEFAULT,
            market_place_item_listing,
            has_more,
        ),
    )


@MARKET_PLACE_COMMANDS.interactions(
    name = 'view',
)
async def command_purchase(
    client,
    interaction_event,
    item_category : P(
        [(name, format(value, 'x')) for name, value in ITEM_CATEGORY_CHOICES],
        'Select item category to filter for',
        'category',
    ) = None,
    item_name : P(str, 'The item\'s name.', 'item') = None,
):
    """
    Buy items on the market place.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client receiving the event.
    
    interaction_event : ``InteractionEvent``
        The received interaction event.
    
    item_category : `str`
        The item's category as hexadecimal integer.
    
    item_name : `None | str`
        The item's name to filter for.
    """
    await client.interaction_application_command_acknowledge(
        interaction_event,
        False,
    )
    
    required_flags = item_category_to_required_flags(item_category)
    item = get_best_matching_item(required_flags, item_name)
    
    now = DateTime.now(TimeZone.utc)
    
    market_place_item_listing, has_more = await get_market_place_item_listing_active(
        (0 if item is None else item.id), required_flags, now, 0, PAGE_SIZE_DEFAULT
    )
    
    await client.interaction_response_message_edit(
        interaction_event,
        components = build_purchase_view_components(
            interaction_event.user_id,
            item,
            required_flags,
            now,
            0,
            PAGE_SIZE_DEFAULT,
            market_place_item_listing,
            has_more,
        ),
    )


@command_purchase.autocomplete('item_name')
async def command_purchase_autocomplete_item_name(interaction_event, value):
    """
    Auto completes the item's name.
    
    This function is a coroutine.
    
    Parameters
    ----------
    interaction_event : ``InteractionEvent``
        The received interaction event.
    
    value : `None | str`
        The value typed by the user,
    
    Returns
    -------
    suggestions : `list<(str, str)>`
    """
    item_category = interaction_event.get_value_of('category')
    required_flags = item_category_to_required_flags(item_category)
    return get_item_name_suggestions(required_flags, value)
