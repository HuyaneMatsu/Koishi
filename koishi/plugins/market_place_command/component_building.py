__all__ = ()

from hata import (
    ButtonStyle, InteractionForm, create_button, create_label, create_row, create_section, create_separator,
    create_text_display, create_text_input, create_thumbnail_media
)

from ..market_place_core import MARKET_PLACE_ITEM_FLAG_BUYER_RETRIEVED, MARKET_PLACE_ITEM_FLAG_SELLER_RETRIEVED

from .constants import BID_INCREASE_LOWER_THRESHOLD, EMOJI_CLOSE, EMOJI_LEFT, EMOJI_RIGHT, PAGE_SIZE_DEFAULT
from .content_building import (
    produce_claim_purchased_description, produce_claim_sold_description, produce_claim_unsold_description,
    produce_inbox_purchased_market_place_item_description, produce_inbox_sold_market_place_item_description,
    produce_inbox_unsold_market_place_item_description, produce_item_description,
    produce_offer_market_place_item_description, produce_purchase_view_header, produce_sell_confirmation_description,
    produce_sell_success_description
)
from .custom_ids import (
    CUSTOM_ID_BID_BALANCE_AMOUNT, CUSTOM_ID_MARKET_PLACE_BID_BUILDER, CUSTOM_ID_MARKET_PLACE_BID_DISABLED,
    CUSTOM_ID_MARKET_PLACE_CLOSE_BUILDER, CUSTOM_ID_MARKET_PLACE_INBOX_CLAIM_BUILDER,
    CUSTOM_ID_MARKET_PLACE_INBOX_VIEW_BUILDER, CUSTOM_ID_MARKET_PLACE_INBOX_VIEW_PAGE_INDEX_DECREMENT_DISABLED,
    CUSTOM_ID_MARKET_PLACE_INBOX_VIEW_PAGE_INDEX_INCREMENT_DISABLED, CUSTOM_ID_MARKET_PLACE_OWN_OFFERS_VIEW_BUILDER,
    CUSTOM_ID_MARKET_PLACE_OWN_OFFERS_VIEW_PAGE_INDEX_DECREMENT_DISABLED,
    CUSTOM_ID_MARKET_PLACE_OWN_OFFERS_VIEW_PAGE_INDEX_INCREMENT_DISABLED,
    CUSTOM_ID_MARKET_PLACE_PURCHASE_DETAILS_BUILDER, CUSTOM_ID_MARKET_PLACE_PURCHASE_VIEW_BUILDER,
    CUSTOM_ID_MARKET_PLACE_PURCHASE_VIEW_PAGE_INDEX_DECREMENT_DISABLED,
    CUSTOM_ID_MARKET_PLACE_PURCHASE_VIEW_PAGE_INDEX_INCREMENT_DISABLED, CUSTOM_ID_MARKET_PLACE_SELL_BUILDER
)
from .helpers import calculate_lowest_required_bid_amount


def build_sell_confirmation_form(
    item,
    item_amount,
    duration_days,
    starting_sell_price,
    initial_sell_fee,
):
    """
    Builds sell confirmation form.
    
    Parameters
    ----------
    item : ``Item``
        Item to be sold.
    
    item_amount : `int`
        The amount of items to be sold.
    
    duration_days : `int` = `8`
        The amount of days the item will be auctioned for.
    
    starting_sell_price : `int`
        Starting sell price.
    
    initial_sell_fee : `int`
        The amount of balance the user has to pay to put the item(s) on the market place.
    
    Returns
    -------
    interaction_form : ``InteractionForm``
    """
    return InteractionForm(
        'Sell confirmation',
        [
            create_text_display(''.join([*produce_sell_confirmation_description(
                item,
                item_amount,
                duration_days,
                starting_sell_price,
                initial_sell_fee,
            )])),
        ],
        CUSTOM_ID_MARKET_PLACE_SELL_BUILDER(item.id, item_amount, duration_days, starting_sell_price),
    )


def build_sell_success_components(
    user_id,
    item,
    item_amount,
    duration_days,
    starting_sell_price,
    initial_sell_fee,
):
    """
    Builds sell success components.
    
    Parameters
    ----------
    user_id : `int`
        The invoking user's identifier.
    
    item : ``Item``
        Item to be sold.
    
    item_amount : `int`
        The amount of items to be sold.
    
    duration_days : `int` = `8`
        The amount of days the item will be auctioned for.
    
    starting_sell_price : `int`
        Starting sell price.
    
    initial_sell_fee : `int`
        The amount of balance the user has to pay to put the item(s) on the market place.
    
    Returns
    -------
    components : ``list<Component>``
    """
    components = []
    
    # Description
    components.append(create_text_display(
        ''.join([*produce_sell_success_description(
            item,
            item_amount,
            duration_days,
            starting_sell_price,
            initial_sell_fee,
        )])),
    )
    components.append(create_separator())
    
    # Control
    components.append(create_row(
        create_button(
            'View own offers',
            custom_id = CUSTOM_ID_MARKET_PLACE_OWN_OFFERS_VIEW_BUILDER(
                user_id, 0, PAGE_SIZE_DEFAULT
            ),
        ),
        create_button(
            'Close',
            EMOJI_CLOSE,
            custom_id = CUSTOM_ID_MARKET_PLACE_CLOSE_BUILDER(user_id),
        ),
    ))
    
    return components


def build_own_offers_view_components(
    user,
    guild_id,
    now,
    page_index,
    page_size,
    market_place_item_listing,
    has_more,
):
    """
    Builds a my offers view components.
    
    Parameters
    ----------
    user : ``ClientUserBase``
        The owner user.
    
    guild_id : `int`
        The local guild's identifier.
    
    now : `DateTime`
        The current time.
    
    page_index : `int`
        The page's index.
    
    page_size : `int`
        The page's size.
    
    market_place_item_listing : ``list<MarketPlaceItem>``
        Market place items to display.
    
    has_more : `bool`
        Whether there are more items to show.
    
    Returns
    -------
    components : ``list<Component>``
    """
    components = []
    
    # Header
    
    components.append(create_section(
        create_text_display(
            f'# {user.name_at(guild_id)}\'s offers\n'
            f'\n'
            f'Page: {page_index + 1}'
        ),
        thumbnail = create_thumbnail_media(user.avatar_url_at(guild_id)),
    ))
    
    components.append(create_separator())
    
    # Listing
    
    if market_place_item_listing:
        for market_place_item in market_place_item_listing:
            components.append(create_text_display(
                ''.join([*produce_offer_market_place_item_description(market_place_item, now)])
            ))
        
        components.append(create_separator())
    
    # Control
    
    if page_index:
        page_index_decrement_custom_id = CUSTOM_ID_MARKET_PLACE_OWN_OFFERS_VIEW_BUILDER(
            user.id, page_index - 1, page_size
        )
        page_index_decrement_enabled = True
    
    else:
        page_index_decrement_custom_id = CUSTOM_ID_MARKET_PLACE_OWN_OFFERS_VIEW_PAGE_INDEX_DECREMENT_DISABLED
        page_index_decrement_enabled = False
    
    if has_more:
        page_index_increment_custom_id = CUSTOM_ID_MARKET_PLACE_OWN_OFFERS_VIEW_BUILDER(
            user.id, page_index + 1, page_size
        )
        page_index_increment_enabled = True
    
    else:
        page_index_increment_custom_id = CUSTOM_ID_MARKET_PLACE_OWN_OFFERS_VIEW_PAGE_INDEX_INCREMENT_DISABLED
        page_index_increment_enabled = False
    
    components.append(create_row(
        create_button(
            f'Page {page_index!s}',
            EMOJI_LEFT,
            custom_id = page_index_decrement_custom_id,
            enabled = page_index_decrement_enabled,
        ),
        create_button(
            f'Page {page_index + 2!s}',
            EMOJI_RIGHT,
            custom_id = page_index_increment_custom_id,
            enabled = page_index_increment_enabled,
        ),
        create_button(
            'Close',
            EMOJI_CLOSE,
            custom_id = CUSTOM_ID_MARKET_PLACE_CLOSE_BUILDER(user.id),
        ),
    ))
    
    return components


def build_inbox_view_components(
    user,
    guild_id,
    now,
    page_index,
    page_size,
    market_place_item_listing,
    has_more,
):
    """
    Builds a my offers view components.
    
    Parameters
    ----------
    user : ``ClientUserBase``
        The owner user.
    
    guild_id : `int`
        The local guild's identifier.
    
    now : `DateTime`
        The current time.
    
    page_index : `int`
        The page's index.
    
    page_size : `int`
        The page's size.
    
    market_place_item_listing : ``list<MarketPlaceItem>``
        Market place items to display.
    
    has_more : `bool`
        Whether there are more items to show.
    
    Returns
    -------
    components : ``list<Component>``
    """
    components = []
    
    # Header
    
    components.append(create_section(
        create_text_display(
            f'# {user.name_at(guild_id)}\'s inbox\n'
            f'\n'
            f'Page: {page_index + 1}'
        ),
        thumbnail = create_thumbnail_media(user.avatar_url_at(guild_id)),
    ))
    
    components.append(create_separator())
    
    # Listing
    
    if market_place_item_listing:
        for market_place_item in market_place_item_listing:
            purchaser_user_id = market_place_item.purchaser_user_id
            if not purchaser_user_id:
                function = produce_inbox_unsold_market_place_item_description
                flag_mask = MARKET_PLACE_ITEM_FLAG_SELLER_RETRIEVED
                
            elif purchaser_user_id == user.id:
                function = produce_inbox_purchased_market_place_item_description
                flag_mask = MARKET_PLACE_ITEM_FLAG_BUYER_RETRIEVED
                
            else:
                function = produce_inbox_sold_market_place_item_description
                flag_mask = MARKET_PLACE_ITEM_FLAG_SELLER_RETRIEVED
            
            if market_place_item.flags & flag_mask:
                enabled = False
                style = ButtonStyle.gray
            else:
                enabled = True
                style = ButtonStyle.green
            
            components.append(create_section(
                create_text_display(
                    ''.join([*function(market_place_item, now)])
                ),
                thumbnail = create_button(
                    'Claim',
                    custom_id = CUSTOM_ID_MARKET_PLACE_INBOX_CLAIM_BUILDER(
                        user.id, page_index, page_size, market_place_item.entry_id
                    ),
                    enabled = enabled,
                    style = style,
                )
            ))
        
        components.append(create_separator())
    
    # Control
    
    if page_index:
        page_index_decrement_custom_id = CUSTOM_ID_MARKET_PLACE_INBOX_VIEW_BUILDER(
            user.id, page_index - 1, page_size
        )
        page_index_decrement_enabled = True
    
    else:
        page_index_decrement_custom_id = CUSTOM_ID_MARKET_PLACE_INBOX_VIEW_PAGE_INDEX_DECREMENT_DISABLED
        page_index_decrement_enabled = False
    
    if has_more:
        page_index_increment_custom_id = CUSTOM_ID_MARKET_PLACE_INBOX_VIEW_BUILDER(
            user.id, page_index + 1, page_size
        )
        page_index_increment_enabled = True
    
    else:
        page_index_increment_custom_id = CUSTOM_ID_MARKET_PLACE_INBOX_VIEW_PAGE_INDEX_INCREMENT_DISABLED
        page_index_increment_enabled = False
    
    components.append(create_row(
        create_button(
            f'Page {page_index!s}',
            EMOJI_LEFT,
            custom_id = page_index_decrement_custom_id,
            enabled = page_index_decrement_enabled,
        ),
        create_button(
            f'Page {page_index + 2!s}',
            EMOJI_RIGHT,
            custom_id = page_index_increment_custom_id,
            enabled = page_index_increment_enabled,
        ),
        create_button(
            'Close',
            EMOJI_CLOSE,
            custom_id = CUSTOM_ID_MARKET_PLACE_CLOSE_BUILDER(user.id),
        ),
    ))
    
    return components


def build_claim_success_components(
    user_id,
    receive_items,
    item,
    item_amount,
    reward_balance,
    fee,
    page_index,
    page_size,
):
    """
    Builds claim success components.
    
    Parameters
    ----------
    user_id : `int`
        The invoking user's identifier.
    
    receive_items : `bool`
        Whether the user received items.
    
    item : ``Item``
        Item to be sold.
    
    item_amount : `int`
        The amount of items to be sold.
    
    reward_balance : `int`
        The reward balance.
    
    fee : `int`
        Fee payed.
    
    page_index : `int`
        Page identifier to redirect back to.
    
    page_size : `int`
        Page size to redirect back to.
    
    Returns
    -------
    components : ``list<Component>``
    """
    components = []
    
    # Description
    if not receive_items:
        function = produce_claim_sold_description
    elif reward_balance:
        function = produce_claim_purchased_description
    else:
        function = produce_claim_unsold_description
    
    components.append(create_text_display(
        ''.join([*function(
            item,
            item_amount,
            reward_balance,
            fee,
        )])),
    )
    components.append(create_separator())
    
    # Control
    components.append(create_row(
        create_button(
            'View inbox',
            custom_id = CUSTOM_ID_MARKET_PLACE_INBOX_VIEW_BUILDER(
                user_id, page_index, page_size
            )
        ),
        create_button(
            'Close',
            EMOJI_CLOSE,
            custom_id = CUSTOM_ID_MARKET_PLACE_CLOSE_BUILDER(user_id),
        ),
    ))
    
    return components


def build_purchase_view_components(
    user_id,
    item,
    required_flags,
    now,
    page_index,
    page_size,
    market_place_item_listing,
    has_more,
):
    """
    Builds purchase view components.
    
    Parameters
    ----------
    user_id : `int`
        The invoking user's identifier.
    
    item : ``None | Item``
        Item the user is filtering for.
    
    required_flags : `int`
        Item flags the user is filtering for.
    
    now : `DateTime`
        The current time.
    
    page_index : `int`
        The page's index.
    
    page_size : `int`
        The page's size.
    
    market_place_item_listing : ``list<MarketPlaceItem>``
        Market place items to display.
    
    has_more : `bool`
        Whether there are more items to show.
    
    Returns
    -------
    components : ``list<Components>``
    """
    components = []
    
    # Header
    
    components.append(create_text_display(''.join([*produce_purchase_view_header(item, required_flags, page_index)])))
    components.append(create_separator())
    
    # Listing
    
    if market_place_item_listing:
        for market_place_item in market_place_item_listing:
            if user_id == market_place_item.seller_user_id:
                style = ButtonStyle.gray
            
            elif user_id == market_place_item.purchaser_user_id:
                style = ButtonStyle.green
            
            else:
                style = ButtonStyle.blue
            
            components.append(create_section(
                create_text_display(''.join([*produce_offer_market_place_item_description(
                    market_place_item,
                    now,
                )])),
                thumbnail = create_button(
                    'Details',
                    custom_id = CUSTOM_ID_MARKET_PLACE_PURCHASE_DETAILS_BUILDER(
                        user_id,
                        (0 if item is None else item.id),
                        required_flags,
                        page_index,
                        page_size,
                        market_place_item.entry_id,
                    ),
                    style = style,
                ),
            ))
        
        components.append(create_separator())
    
    # Control
    
    if page_index:
        page_index_decrement_custom_id = CUSTOM_ID_MARKET_PLACE_PURCHASE_VIEW_BUILDER(
            user_id,
            (0 if item is None else item.id),
            required_flags,
            (page_index - 1),
            page_size,
        )
        page_index_decrement_enabled = True
    
    else:
        page_index_decrement_custom_id = CUSTOM_ID_MARKET_PLACE_PURCHASE_VIEW_PAGE_INDEX_DECREMENT_DISABLED
        page_index_decrement_enabled = False
    
    if has_more:
        page_index_increment_custom_id = CUSTOM_ID_MARKET_PLACE_PURCHASE_VIEW_BUILDER(
            user_id,
            (0 if item is None else item.id),
            required_flags,
            (page_index + 1),
            page_size,
        )
        page_index_increment_enabled = True
    
    else:
        page_index_increment_custom_id = CUSTOM_ID_MARKET_PLACE_PURCHASE_VIEW_PAGE_INDEX_INCREMENT_DISABLED
        page_index_increment_enabled = False
    
    components.append(create_row(
        create_button(
            f'Page {page_index!s}',
            EMOJI_LEFT,
            custom_id = page_index_decrement_custom_id,
            enabled = page_index_decrement_enabled,
        ),
        create_button(
            f'Page {page_index + 2!s}',
            EMOJI_RIGHT,
            custom_id = page_index_increment_custom_id,
            enabled = page_index_increment_enabled,
        ),
        create_button(
            'Close',
            EMOJI_CLOSE,
            custom_id = CUSTOM_ID_MARKET_PLACE_CLOSE_BUILDER(user_id),
        ),
    ))
    
    return components


def build_purchase_details_components(
    user_id,
    item,
    required_flags,
    now,
    page_index,
    page_size,
    internal_call,
    market_place_item,
):
    """
    Builds market place purchase details components.
    
    Parameters
    ----------
    user_id : `int`
        The invoking user's identifier.
    
    item : ``None | Item``
        Item the user is filtering for.
    
    required_flags : `int`
        Item flags the user is filtering for.
    
    now : `DateTime`
        The current time.
    
    page_index : `int`
        The page's index.
    
    page_size : `int`
        The page's size.
    
    internal_call : `bool`
        Whether the offer is shown from an internal source.
    
    market_place_item : ``MarketPlaceItem``
        The market place item to display.
    
    Returns
    -------
    components : ``list<Components>``
    """
    components = []
    
    # Header
    
    components.append(create_text_display(
        ''.join(['### ', *produce_offer_market_place_item_description(
            market_place_item,
            now,
        )])
    ))
    components.append(create_separator())
    
    # Description
    
    components.append(create_text_display(
        ''.join([*produce_item_description(market_place_item.item_id)])
    ))
    components.append(create_separator())
    
    # Control
    
    if internal_call:
        back_reference_title = 'Back to offers'
        back_reference_item_id = (0 if item is None else item.id)
        
    else:
        back_reference_title = 'View other offers'
        back_reference_item_id = market_place_item.item_id
    
    if user_id == market_place_item.seller_user_id:
        bid_custom_id = CUSTOM_ID_MARKET_PLACE_BID_DISABLED
        bid_enabled = False
        bid_style = ButtonStyle.gray
    else:
        bid_custom_id = CUSTOM_ID_MARKET_PLACE_BID_BUILDER(
            user_id,
            back_reference_item_id,
            required_flags,
            page_index,
            page_size,
            internal_call,
            market_place_item.entry_id,
        )
        bid_enabled = True
        if user_id == market_place_item.purchaser_user_id:
            bid_style = ButtonStyle.green
        else:
            bid_style = ButtonStyle.blue
        
    
    components.append(create_row(
        create_button(
            back_reference_title,
            custom_id = CUSTOM_ID_MARKET_PLACE_PURCHASE_VIEW_BUILDER(
                user_id,
                back_reference_item_id,
                required_flags,
                page_index,
                page_size,
            )
        ),
        create_button(
            'Bid',
            custom_id = bid_custom_id,
            enabled = bid_enabled,
            style = bid_style,
        ),
        create_button(
            'Close',
            EMOJI_CLOSE,
            custom_id = CUSTOM_ID_MARKET_PLACE_CLOSE_BUILDER(user_id),
        ),
    ))
    
    return components


def build_bid_form(
    user_id,
    item_id,
    required_flags,
    now,
    page_index,
    page_size,
    internal_call,
    market_place_item,
):
    """
    Builds a bid form.
    
    Parameters
    ----------
    user_id : `int`
        The invoking user's identifier.
    
    item_id : `int`
        Item identifier to back-direct to.
    
    required_flags : `int`
        Item flags to back-direct to.
    
    now : `DateTime`
        The current time.
    
    page_index : `int`
        The page's index to back-direct to.
    
    page_size : `int`
        The page's size to back-direct to.
    
    internal_call : `bool`
        Whether the offer is shown from an internal source to back-direct to.
    
    market_place_item : ``MarketPlaceItem``
        The market place item to bid for.
    
    Returns
    -------
    form : ``InteractionForm``
    """
    required_bid_amount = market_place_item.purchaser_balance_amount
    if user_id == market_place_item.purchaser_user_id:
        description = 'You are currently the highest bidder.'
    else:
        if required_bid_amount:
            required_bid_amount = calculate_lowest_required_bid_amount(required_bid_amount)
        else:
            required_bid_amount = market_place_item.seller_balance_amount
            if not required_bid_amount:
                required_bid_amount = BID_INCREASE_LOWER_THRESHOLD
        
        description = 'Lowest allowed bid auto-filled, modify or just confirm.'
    
    return InteractionForm(
        'Specify your bid amount',
        [
            create_text_display(
                ''.join(['### ', *produce_offer_market_place_item_description(
                    market_place_item,
                    now,
                )])
            ),
            create_label(
                'Bid amount',
                description,
                create_text_input(
                    custom_id = CUSTOM_ID_BID_BALANCE_AMOUNT,
                    value = str(required_bid_amount),
                ),
            ),
        ],
        CUSTOM_ID_MARKET_PLACE_BID_BUILDER(
            user_id,
            item_id,
            required_flags,
            page_index,
            page_size,
            internal_call,
            market_place_item.entry_id,
        ),
    )


def build_bid_success_components(
    user_id,
    item_id,
    required_flags,
    page_index,
    page_size,
    internal_call,
):
    """
    Builds market place purchase details components.
    
    Parameters
    ----------
    user_id : `int`
        The invoking user's identifier.
    
    item_id : `int`
        Item identifier to back-direct to.
    
    required_flags : `int`
        Item flags to back-direct to.
    
    page_index : `int`
        The page's index to back-direct to.
    
    page_size : `int`
        The page's size to back-direct to.
    
    internal_call : `bool`
        Whether the offer is shown from an internal source.
    
    Returns
    -------
    components : ``list<Components>``
    """
    components = []
    
    # Header
    
    components.append(create_text_display(
        'You successfully placed your bid.\n'
        '\n'
        'Keep a keen eye on it, it is up to you to see whether others up you.'
    ))
    components.append(create_separator())
    
    # Control
    
    if internal_call:
        back_reference_title = 'Back to offers'
    else:
        back_reference_title = 'View other offers'
    
    components.append(create_row(
        create_button(
            back_reference_title,
            custom_id = CUSTOM_ID_MARKET_PLACE_PURCHASE_VIEW_BUILDER(
                user_id,
                item_id,
                required_flags,
                page_index,
                page_size,
            )
        ),
        create_button(
            'Close',
            EMOJI_CLOSE,
            custom_id = CUSTOM_ID_MARKET_PLACE_CLOSE_BUILDER(user_id),
        ),
    ))
    
    return components
