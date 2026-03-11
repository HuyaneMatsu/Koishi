__all__ = ()

from datetime import datetime as DateTime, timedelta as TimeDelta, timezone as TimeZone
from math import floor, inf, isnan as is_nan

from hata.ext.slash import EvaluationError, evaluate_text

from ...bot_utils.constants import EMOJI__HEART_CURRENCY
from ...bots import FEATURE_CLIENTS

from ..adventure_core import get_active_adventure
from ..inventory_core import get_inventory, save_inventory
from ..item_core import get_item, get_item_nullable
from ..market_place_core import (
    CUSTOM_ID_MARKET_PLACE_OFFER_RP, MARKET_PLACE_ITEM_FLAG_BUYER_RETRIEVED, MARKET_PLACE_ITEM_FLAG_SELLER_RETRIEVED,
    MarketPlaceItem, get_market_place_item, get_market_place_item_listing_active, get_market_place_item_listing_inbox,
    get_market_place_item_listing_own_offers, insert_market_place_item, update_market_place_item
)
from ..user_balance import ALLOCATION_FEATURE_ID_MARKET_PLACE, get_user_balance, save_user_balance

from .component_building import (
    build_bid_form, build_bid_success_components, build_claim_success_components, build_inbox_view_components,
    build_own_offers_view_components, build_purchase_details_components, build_purchase_view_components,
    build_sell_success_components
)
from .constants import BID_INCREASE_LOWER_THRESHOLD, FINALISATION_DELAY_AFTER_BID, PAGE_SIZE_DEFAULT
from .custom_ids import (
    CUSTOM_ID_BID_BALANCE_AMOUNT, CUSTOM_ID_MARKET_PLACE_BID_DISABLED, CUSTOM_ID_MARKET_PLACE_BID_RP,
    CUSTOM_ID_MARKET_PLACE_CLOSE_RP, CUSTOM_ID_MARKET_PLACE_INBOX_CLAIM_RP,
    CUSTOM_ID_MARKET_PLACE_INBOX_VIEW_PAGE_INDEX_DECREMENT_DISABLED,
    CUSTOM_ID_MARKET_PLACE_INBOX_VIEW_PAGE_INDEX_INCREMENT_DISABLED, CUSTOM_ID_MARKET_PLACE_INBOX_VIEW_RP,
    CUSTOM_ID_MARKET_PLACE_OWN_OFFERS_VIEW_PAGE_INDEX_DECREMENT_DISABLED,
    CUSTOM_ID_MARKET_PLACE_OWN_OFFERS_VIEW_PAGE_INDEX_INCREMENT_DISABLED, CUSTOM_ID_MARKET_PLACE_OWN_OFFERS_VIEW_RP,
    CUSTOM_ID_MARKET_PLACE_PURCHASE_DETAILS_RP, CUSTOM_ID_MARKET_PLACE_PURCHASE_VIEW_PAGE_INDEX_DECREMENT_DISABLED,
    CUSTOM_ID_MARKET_PLACE_PURCHASE_VIEW_PAGE_INDEX_INCREMENT_DISABLED, CUSTOM_ID_MARKET_PLACE_PURCHASE_VIEW_RP,
    CUSTOM_ID_MARKET_PLACE_SELL_RP
)
from .helpers import calculate_duration, calculate_initial_sell_fee, calculate_lowest_required_bid_amount


@FEATURE_CLIENTS.interactions(
    custom_id = [
        CUSTOM_ID_MARKET_PLACE_OWN_OFFERS_VIEW_PAGE_INDEX_DECREMENT_DISABLED,
        CUSTOM_ID_MARKET_PLACE_OWN_OFFERS_VIEW_PAGE_INDEX_INCREMENT_DISABLED,
        CUSTOM_ID_MARKET_PLACE_INBOX_VIEW_PAGE_INDEX_DECREMENT_DISABLED,
        CUSTOM_ID_MARKET_PLACE_INBOX_VIEW_PAGE_INDEX_INCREMENT_DISABLED,
        CUSTOM_ID_MARKET_PLACE_PURCHASE_VIEW_PAGE_INDEX_DECREMENT_DISABLED,
        CUSTOM_ID_MARKET_PLACE_PURCHASE_VIEW_PAGE_INDEX_INCREMENT_DISABLED,
        CUSTOM_ID_MARKET_PLACE_BID_DISABLED,
    ],
)
async def handle_dummy():
    """
    Handles a dummy interaction.
    
    This function is a coroutine.
    """
    return


@FEATURE_CLIENTS.interactions(custom_id = CUSTOM_ID_MARKET_PLACE_CLOSE_RP)
async def handle_own_offers_close(
    client,
    interaction_event,
    user_id,
):
    """
    Handles a close interaction.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        Client receiving this interaction.
    
    interaction_event : ``InteractionEvent``
        The received interaction event.
    
    user_id : `str`
        THe source user's identifier as a string representing a hexadecimal integer.
    """
    try:
        user_id = int(user_id, 16)
    except ValueError:
        return
    
    if interaction_event.user_id != user_id:
        return
    
    await client.interaction_component_acknowledge(
        interaction_event,
    )
    await client.interaction_response_message_delete(
        interaction_event,
    )


@FEATURE_CLIENTS.interactions(custom_id = CUSTOM_ID_MARKET_PLACE_SELL_RP, target = 'form')
async def handle_sell_confirmation(
    client,
    interaction_event,
    item_id,
    item_amount,
    duration_days,
    starting_sell_price,
):
    """
    Handles a sell confirmation.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        Client receiving this interaction.
    
    interaction_event : ``InteractionEvent``
        The received interaction event.
    
    item_id : `str`
        The item's identifier to sell as a string representing a hexadecimal integer.
    
    item_amount : `str`
        The amount of items to sell as a string representing a hexadecimal integer.
    
    duration_days : `str`
        The amount of days the item will be auctioned for as a string representing a hexadecimal integer.
    
    starting_sell_price : `str`
        The amount of balance the user has to pay to put the item(s) on the market place as a string representing a
        hexadecimal integer.
    """
    try:
        item_id = int(item_id, 16)
        item_amount = int(item_amount, 16)
        duration_days = int(duration_days, 16)
        starting_sell_price = int(starting_sell_price, 16)
    except ValueError:
        return
    
    item = get_item_nullable(item_id)
    if item is None:
        return
    
    await client.interaction_application_command_acknowledge(
        interaction_event,
    )
    
    while True:
        adventure = await get_active_adventure(interaction_event.user_id)
        if (adventure is not None):
            error_message = 'You cannot sell while on adventure.'
            break
        
        # Validate item
        inventory = await get_inventory(interaction_event.user_id)
        
        # Item amount
        owned_amount = inventory.get_item_amount(item)
        if owned_amount < item_amount:
            error_message = f'The amount of {item.name}-s you own decreased in the meanwhile.'
            break
        
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
        
        # Execute action
        market_place_item = MarketPlaceItem(
            item,
            item_amount,
            interaction_event.user_id,
            starting_sell_price,
            DateTime.now(TimeZone.utc) + TimeDelta(seconds = calculate_duration(duration_days)),
            initial_sell_fee,
        )
        inventory.modify_item_amount(item, -item_amount)
        user_balance.modify_balance_by(-initial_sell_fee)
        
        await insert_market_place_item(market_place_item)
        await save_inventory(inventory)
        await save_user_balance(user_balance)
        
        # Respond
        await client.interaction_response_message_edit(interaction_event, '-# _ _ ')
        await client.interaction_response_message_delete(interaction_event)
        
        await client.interaction_followup_message_create(
            interaction_event,
            components = build_sell_success_components(
                interaction_event.user_id,
                item,
                item_amount,
                duration_days,
                starting_sell_price,
                initial_sell_fee,
            ),
        )
        return
    
    await client.interaction_response_message_edit(
        interaction_event,
        allowed_mentions = None,
        content = error_message,
        show_for_invoking_user_only = True,
    )


@FEATURE_CLIENTS.interactions(custom_id = CUSTOM_ID_MARKET_PLACE_OWN_OFFERS_VIEW_RP)
async def handle_own_offers_view(
    client,
    interaction_event,
    user_id,
    page_index,
    page_size,
):
    """
    Handles an own-offers view interaction.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        Client receiving this interaction.
    
    interaction_event : ``InteractionEvent``
        The received interaction event.
    
    user_id : `str`
        THe source user's identifier as a string representing a hexadecimal integer.
    
    page_index : `str`
        The page's index to show as a string representing a hexadecimal integer.
    
    page_size : `str`
        The page's size to show as a string representing a hexadecimal integer.
    """
    try:
        user_id = int(user_id, 16)
        page_index = int(page_index, 16)
        page_size = int(page_size, 16)
    except ValueError:
        return
    
    if interaction_event.user_id != user_id:
        return
    
    await client.interaction_component_acknowledge(
        interaction_event,
        False,
    )
    
    
    now = DateTime.now(TimeZone.utc)
    
    market_place_item_listing, has_more = await get_market_place_item_listing_own_offers(
        interaction_event.user_id, now, 0, page_size
    )
    
    await client.interaction_response_message_edit(
        interaction_event,
        components = build_own_offers_view_components(
            interaction_event.user,
            interaction_event.guild_id,
            now,
            page_index,
            page_size,
            market_place_item_listing,
            has_more,
        ),
    )


@FEATURE_CLIENTS.interactions(custom_id = CUSTOM_ID_MARKET_PLACE_INBOX_VIEW_RP)
async def handle_inbox_view(
    client,
    interaction_event,
    user_id,
    page_index,
    page_size,
):
    """
    Handles an inbox view interaction.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        Client receiving this interaction.
    
    interaction_event : ``InteractionEvent``
        The received interaction event.
    
    user_id : `str`
        THe source user's identifier as a string representing a hexadecimal integer.
    
    page_index : `str`
        The page's index to show as a string representing a hexadecimal integer.
    
    page_size : `str`
        The page's size to show as a string representing a hexadecimal integer.
    """
    try:
        user_id = int(user_id, 16)
        page_index = int(page_index, 16)
        page_size = int(page_size, 16)
    except ValueError:
        return
    
    if interaction_event.user_id != user_id:
        return
    
    await client.interaction_component_acknowledge(
        interaction_event,
        False,
    )
    
    
    now = DateTime.now(TimeZone.utc)
    
    market_place_item_listing, has_more = await get_market_place_item_listing_inbox(
        interaction_event.user_id, now, page_index, page_size
    )
    
    await client.interaction_response_message_edit(
        interaction_event,
        components = build_inbox_view_components(
            interaction_event.user,
            interaction_event.guild_id,
            now,
            page_index,
            page_size,
            market_place_item_listing,
            has_more,
        ),
    )


@FEATURE_CLIENTS.interactions(custom_id = CUSTOM_ID_MARKET_PLACE_INBOX_CLAIM_RP)
async def handle_inbox_claim(
    client,
    interaction_event,
    user_id,
    page_index,
    page_size,
    entry_id,
):
    """
    Handles an inbox view interaction.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        Client receiving this interaction.
    
    interaction_event : ``InteractionEvent``
        The received interaction event.
    
    user_id : `str`
        THe source user's identifier as a string representing a hexadecimal integer.
    
    page_index : `str`
        The page's index to redirect back to as a string representing a hexadecimal integer.
    
    page_size : `str`
        The page's size to redirect back to as a string representing a hexadecimal integer.
    
    entry_id : `str`
        The entry's identifier as a string representing a hexadecimal integer.
    """
    try:
        user_id = int(user_id, 16)
        page_index = int(page_index, 16)
        page_size = int(page_size, 16)
        entry_id = int(entry_id, 16)
    except ValueError:
        return
    
    if interaction_event.user_id != user_id:
        return
    
    await client.interaction_component_acknowledge(
        interaction_event,
        False,
    )
    
    while True:
        adventure = await get_active_adventure(user_id)
        if (adventure is not None):
            error_message = 'You cannot claim while on adventure.'
            break
        
        market_place_item = await get_market_place_item(entry_id)
        if market_place_item is None:
            error_message = 'The offer does not exist (anymore).'
            break
        
        if (user_id != market_place_item.seller_user_id) and (user_id != market_place_item.purchaser_user_id):
            error_message = 'The offer does not belong to you.'
            break
        
        now = DateTime.now(TimeZone.utc)
        if market_place_item.finalises_at > now:
            error_message = 'The offer is not yet finalised.'
            break
        
        purchaser_user_id = market_place_item.purchaser_user_id
        if purchaser_user_id == user_id:
            flag_mask = MARKET_PLACE_ITEM_FLAG_BUYER_RETRIEVED
        else:
            flag_mask = MARKET_PLACE_ITEM_FLAG_SELLER_RETRIEVED
        
        flags = market_place_item.flags
        if flags & flag_mask:
            error_message = 'You already claimed your part of the offer.'
            break
        
        item = get_item(market_place_item.item_id)
        item_amount = market_place_item.item_amount
        reward_balance = market_place_item.purchaser_balance_amount
        
        # Modify the flags at the start to avoid multi retrieval
        market_place_item.flags = flags | flag_mask
        
        if (not purchaser_user_id) or (purchaser_user_id == user_id):
            receive_items = True
            fee = 0
            inventory = await get_inventory(user_id)
            inventory.modify_item_amount(item, item_amount)
            await save_inventory(inventory)
        
        else:
            receive_items = False
            fee = (reward_balance // 100) - market_place_item.initial_sell_fee
            if fee > 0:
                reward_balance -= fee
            
            user_balance = await get_user_balance(user_id)
            user_balance.modify_balance_by(reward_balance)
            await save_user_balance(user_balance)
        
        await update_market_place_item(market_place_item)
        
        
        await client.interaction_response_message_edit(
            interaction_event,
            components = build_claim_success_components(
                user_id,
                receive_items,
                item,
                item_amount,
                reward_balance,
                fee,
                page_index,
                page_size,
            ),
        )
        return
    
    await client.interaction_followup_message_create(
        interaction_event,
        content = error_message,
        show_for_invoking_user_only = True,
    )


@FEATURE_CLIENTS.interactions(custom_id = CUSTOM_ID_MARKET_PLACE_PURCHASE_VIEW_RP)
async def handle_purchase_view(
    client,
    interaction_event,
    user_id,
    item_id,
    required_flags,
    page_index,
    page_size,
):
    """
    Handles an purchase view interaction.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        Client receiving this interaction.
    
    interaction_event : ``InteractionEvent``
        The received interaction event.
    
    user_id : `str`
        THe source user's identifier as a string representing a hexadecimal integer.
    
    item_id : `str`
        The item's identifier the user is filtering for as a string representing a hexadecimal integer.
    
    required_flags : `str`
        Item flags the user is filtering for  as a string representing a hexadecimal integer.
    
    page_index : `str`
        The page's index to show as a string representing a hexadecimal integer.
    
    page_size : `str`
        The page's size to show as a string representing a hexadecimal integer.
    """
    try:
        user_id = int(user_id, 16)
        item_id = int(item_id, 16)
        required_flags = int(required_flags, 16)
        page_index = int(page_index, 16)
        page_size = int(page_size, 16)
    except ValueError:
        return
    
    if interaction_event.user_id != user_id:
        return
    
    item = get_item_nullable(item_id)
    
    await client.interaction_component_acknowledge(
        interaction_event,
        False,
    )
    
    now = DateTime.now(TimeZone.utc)
    
    market_place_item_listing, has_more = await get_market_place_item_listing_active(
        (0 if item is None else item.id), required_flags, now, page_index, page_size
    )
    
    await client.interaction_response_message_edit(
        interaction_event,
        components = build_purchase_view_components(
            interaction_event.user_id,
            item,
            required_flags,
            now,
            page_index,
            page_size,
            market_place_item_listing,
            has_more,
        ),
    )


@FEATURE_CLIENTS.interactions(custom_id = CUSTOM_ID_MARKET_PLACE_OFFER_RP)
async def handle_purchase_details_external(
    client,
    interaction_event,
    user_id,
    entry_id,
    create_new_message_when_responding,
):
    """
    Handles a purchase details interaction that comes from an external source.
    
    Parameters
    ----------
    client : ``Client``
        Client receiving this interaction.
    
    interaction_event : ``InteractionEvent``
        The received interaction event.
    
    user_id : `str`
        THe source user's identifier as a string representing a hexadecimal integer.
    
    entry_id : `str`
        The entry's identifier as a string representing a hexadecimal integer.
    
    create_new_message_when_responding : `str`
        Whether to create a new message when responding as a string representing a hexadecimal integer.
    """
    try:
        user_id = int(user_id, 16)
        entry_id = int(entry_id, 16)
        create_new_message_when_responding = int(create_new_message_when_responding, 16)
    except ValueError:
        return
    
    if interaction_event.user_id != user_id:
        return
    
    
    await client.interaction_component_acknowledge(
        interaction_event,
        False,
    )
    
    while True:
        market_place_item = await get_market_place_item(entry_id)
        if market_place_item is None:
            error_message = 'The offer does not exist (anymore).'
            break
        
        now = DateTime.now(TimeZone.utc)
        if market_place_item.finalises_at <= now:
            error_message = 'The offer is already finalised.'
            break
        
        if create_new_message_when_responding:
            function = type(client).interaction_followup_message_create
        else:
            function = type(client).interaction_response_message_edit
        
        await function(
            client,
            interaction_event,
            components = build_purchase_details_components(
                user_id,
                None,
                0,
                now,
                0,
                PAGE_SIZE_DEFAULT,
                False,
                market_place_item,
            ),
        )
        return
    
    await client.interaction_followup_message_create(
        interaction_event,
        content = error_message,
        show_for_invoking_user_only = True,
    )


@FEATURE_CLIENTS.interactions(custom_id = CUSTOM_ID_MARKET_PLACE_PURCHASE_DETAILS_RP)
async def handle_purchase_details(
    client,
    interaction_event,
    user_id,
    item_id,
    required_flags,
    page_index,
    page_size,
    entry_id,
):
    """
    Handles an purchase view interaction.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        Client receiving this interaction.
    
    interaction_event : ``InteractionEvent``
        The received interaction event.
    
    user_id : `str`
        THe source user's identifier as a string representing a hexadecimal integer.
    
    item_id : `str`
        The item's identifier the user is filtering for as a string representing a hexadecimal integer.
    
    required_flags : `str`
        Item flags the user is filtering for  as a string representing a hexadecimal integer.
    
    page_index : `str`
        The page's index to show as a string representing a hexadecimal integer.
    
    page_size : `str`
        The page's size to show as a string representing a hexadecimal integer.
    
    entry_id : `str`
        The entry's identifier as a string representing a hexadecimal integer.
    """
    try:
        user_id = int(user_id, 16)
        item_id = int(item_id, 16)
        required_flags = int(required_flags, 16)
        page_index = int(page_index, 16)
        page_size = int(page_size, 16)
        entry_id = int(entry_id, 16)
    except ValueError:
        return
    
    if interaction_event.user_id != user_id:
        return
    
    item = get_item_nullable(item_id)
    
    await client.interaction_component_acknowledge(
        interaction_event,
        False,
    )
    
    while True:
        market_place_item = await get_market_place_item(entry_id)
        if market_place_item is None:
            error_message = 'The offer does not exist (anymore).'
            break
        
        now = DateTime.now(TimeZone.utc)
        if market_place_item.finalises_at <= now:
            error_message = 'The offer is already finalised.'
            break
        
        await client.interaction_response_message_edit(
            interaction_event,
            components = build_purchase_details_components(
                user_id,
                item,
                required_flags,
                now,
                page_index,
                page_size,
                True,
                market_place_item,
            ),
        )
        return
    
    await client.interaction_followup_message_create(
        interaction_event,
        content = error_message,
        show_for_invoking_user_only = True,
    )


@FEATURE_CLIENTS.interactions(custom_id = CUSTOM_ID_MARKET_PLACE_BID_RP)
async def handle_bid_invocation(
    client,
    interaction_event,
    user_id,
    item_id,
    required_flags,
    page_index,
    page_size,
    internal_call,
    entry_id,
):
    """
    Handles an purchase view interaction.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        Client receiving this interaction.
    
    interaction_event : ``InteractionEvent``
        The received interaction event.
    
    user_id : `str`
        THe source user's identifier as a string representing a hexadecimal integer.
    
    item_id : `str`
        The item's identifier the user is filtering for as a string representing a hexadecimal integer.
    
    required_flags : `str`
        Item flags the user is filtering for  as a string representing a hexadecimal integer.
    
    
    page_index : `str`
        The page's index to show as a string representing a hexadecimal integer.
    
    page_size : `str`
        The page's size to show as a string representing a hexadecimal integer.
    
    internal_call : `bool`
        Whether the bid was invoked internally.
    
    entry_id : `str`
        The entry's identifier as a string representing a hexadecimal integer.
    """
    try:
        user_id = int(user_id, 16)
        item_id = int(item_id, 16)
        required_flags = int(required_flags, 16)
        page_index = int(page_index, 16)
        page_size = int(page_size, 16)
        internal_call = int(internal_call, 16)
        entry_id = int(entry_id, 16)
    except ValueError:
        return
    
    internal_call = (True if internal_call else False)
    
    if interaction_event.user_id != user_id:
        return
    
    while True:
        adventure = await get_active_adventure(user_id)
        if (adventure is not None):
            error_message = 'You cannot bid while on adventure.'
            break
        
        market_place_item = await get_market_place_item(entry_id)
        if market_place_item is None:
            error_message = 'The offer does not exist (anymore).'
            break
        
        if market_place_item.seller_user_id == user_id:
            error_message = 'You cannot bid on your own offer.'
            break
        
        now = DateTime.now(TimeZone.utc)
        if market_place_item.finalises_at <= now:
            error_message = 'The offer is already finalised.'
            break
        
        await client.interaction_form_send(
            interaction_event,
            build_bid_form(
                user_id,
                item_id,
                required_flags,
                now,
                page_index,
                page_size,
                internal_call,
                market_place_item,
            ),
        )
        return
    
    await client.interaction_component_acknowledge(
        interaction_event,
        True,
    )
    await client.interaction_followup_message_create(
        interaction_event,
        content = error_message,
        show_for_invoking_user_only = True,
    )


@FEATURE_CLIENTS.interactions(custom_id = CUSTOM_ID_MARKET_PLACE_BID_RP, target = 'form')
async def handle_bid_confirmation(
    client,
    interaction_event,
    user_id,
    item_id,
    required_flags,
    page_index,
    page_size,
    internal_call,
    entry_id,
    *,
    bid_balance_expression : CUSTOM_ID_BID_BALANCE_AMOUNT = None
):
    """
    Handles an purchase view interaction.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        Client receiving this interaction.
    
    interaction_event : ``InteractionEvent``
        The received interaction event.
    
    user_id : `str`
        THe source user's identifier as a string representing a hexadecimal integer.
    
    item_id : `str`
        The item's identifier the user is filtering for as a string representing a hexadecimal integer.
    
    required_flags : `str`
        Item flags the user is filtering for  as a string representing a hexadecimal integer.
    
    page_index : `str`
        The page's index to show as a string representing a hexadecimal integer.
    
    page_size : `str`
        The page's size to show as a string representing a hexadecimal integer.
    
    internal_call : `bool`
        Whether the bid was invoked internally.
    
    entry_id : `str`
        The entry's identifier as a string representing a hexadecimal integer.
    
    bid_balance_expression : `None | str` = `None`, Optional (Keyword only)
        The amount of balance the user bid.
    """
    try:
        user_id = int(user_id, 16)
        item_id = int(item_id, 16)
        required_flags = int(required_flags, 16)
        page_index = int(page_index, 16)
        page_size = int(page_size, 16)
        internal_call = int(internal_call, 16)
        entry_id = int(entry_id, 16)
    except ValueError:
        return
    
    internal_call = (True if internal_call else False)
    
    if interaction_event.user_id != user_id:
        return
    
    await client.interaction_component_acknowledge(
        interaction_event,
        False,
    )
    
    while True:
        adventure = await get_active_adventure(user_id)
        if (adventure is not None):
            error_message = 'You cannot bid while on adventure.'
            break
        
        # Prevalidate bid
        if bid_balance_expression is None:
            bid_balance_amount_specified = False
            bid_balance_amount = 0
        
        else:
            try:
                bid_balance_amount =  evaluate_text(bid_balance_expression)
            except EvaluationError as exception:
                error_message = exception.pretty_repr
                break
            
            if isinstance(bid_balance_amount, float):
                if is_nan(bid_balance_amount):
                    bid_all = False
                    bid_balance_amount = 0
                        
                elif bid_balance_amount == inf:
                    bid_all = True
                    bid_balance_amount = 0
                
                elif bid_balance_amount == -inf:
                    bid_all = False
                    bid_balance_amount = 0
                
                else:
                    bid_all = False
                    bid_balance_amount = floor(bid_balance_amount)
            
            else:
                bid_all = False
            
            if bid_balance_amount <= 0:
                error_message = 'You cannot bid with non positive amount.'
                break
            
            if bid_all:
                error_message = f'Bidding all your {EMOJI__HEART_CURRENCY} is not allowed.'
                break
            
            bid_balance_amount_specified = True
        
        # Validate market place item
        market_place_item = await get_market_place_item(entry_id)
        if market_place_item is None:
            error_message = 'The offer does not exist (anymore).'
            break
        
        if market_place_item.seller_user_id == user_id:
            error_message = 'You cannot bid on your own offer.'
            break
        
        now = DateTime.now(TimeZone.utc)
        if market_place_item.finalises_at <= now:
            error_message = 'The offer is already finalised.'
            break
        
        # Validate bid with the item
        purchaser_user_id = market_place_item.purchaser_user_id
        required_bid_amount = market_place_item.purchaser_balance_amount
        if user_id != purchaser_user_id:
            if required_bid_amount:
                required_bid_amount = calculate_lowest_required_bid_amount(required_bid_amount)
            else:
                required_bid_amount = market_place_item.seller_balance_amount
                if not required_bid_amount:
                    required_bid_amount = BID_INCREASE_LOWER_THRESHOLD
        
        if not bid_balance_amount_specified:
            bid_balance_amount = required_bid_amount
        
        else:
            if required_bid_amount > bid_balance_amount:
                error_message = f'You must bid at least {required_bid_amount} {EMOJI__HEART_CURRENCY}'
                break
        
        # Validate bid with balance
        user_balance = await get_user_balance(user_id)
        available = user_balance.balance - user_balance.get_cumulative_allocated_balance()
        if user_id == purchaser_user_id:
            available += market_place_item.purchaser_balance_amount 
        
        if bid_balance_amount > available:
            error_message = (
                f'You have only {available} {EMOJI__HEART_CURRENCY}, '
                f'which is lower than your bid {bid_balance_amount} {EMOJI__HEART_CURRENCY}.'
            )
            break
        
        # Apply changes
        other_user_balance = None
        
        if user_id == purchaser_user_id:
            user_balance.remove_allocation(ALLOCATION_FEATURE_ID_MARKET_PLACE, entry_id)
        
        elif purchaser_user_id:
            other_user_balance = await get_user_balance(purchaser_user_id)
            other_user_balance.remove_allocation(ALLOCATION_FEATURE_ID_MARKET_PLACE, entry_id)
        
        # To avoid sniping, set `finalises_at` to a minimum amount. This allows other users to rect.
        finalises_at = max(market_place_item.finalises_at, now + FINALISATION_DELAY_AFTER_BID)
        
        # Update the market place item.
        market_place_item.finalises_at = finalises_at
        market_place_item.purchaser_user_id = user_id
        market_place_item.purchaser_balance_amount = bid_balance_amount
        
        user_balance.add_allocation(
            ALLOCATION_FEATURE_ID_MARKET_PLACE,
            entry_id,
            bid_balance_amount,
            int(finalises_at.timestamp()).to_bytes(8, 'little'),
        )
        
        await update_market_place_item(market_place_item)
        if (other_user_balance is not None):
            await save_user_balance(other_user_balance)
        await save_user_balance(user_balance)
        
        # Respond
        await client.interaction_response_message_edit(
            interaction_event,
            components = build_bid_success_components(
                user_id,
                item_id,
                required_flags,
                page_index,
                page_size,
                internal_call,
            ),
        )
        return
    
    await client.interaction_followup_message_create(
        interaction_event,
        content = error_message,
        show_for_invoking_user_only = True,
    )
