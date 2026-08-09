__all__ = ()

from hata import ButtonStyle, create_button, create_row, create_text_display

from config import FLANDRE_ID

from ...bot_utils.constants import EMOJI__HEART_CURRENCY

from ..market_place_core import MARKET_PLACE_INBOX_PAGE_SIZE_DEFAULT, CUSTOM_ID_MARKET_PLACE_INBOX_CLAIM_ONE_BUILDER

from ..item_core import get_item
from ..unit_core import produce_kilogram
from ..user_settings import USER_SETTINGS_CUSTOM_ID_NOTIFICATION_MARKET_PLACE_ITEM_FINALISATION_DISABLE


def produce_notification_content(
    user_id,
    seller_user_id,
    purchaser_user_id,
    item_id,
    item_amount,
    seller_balance_amount,
    purchaser_balance_amount,
    notification_content_prefix,
):
    """
    Produces notification content.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    user_id : `int`
        The point of view user's identifier.
    
    seller_user_id : `int`
        The seller user's identifier.
    
    purchaser_user_id : `int`
        The purchaser user's identifier.
    
    item_id : `int`
        The item's identifier.
    
    item_amount : ``int`
        The sold items' amount.
    
    seller_balance_amount : `int`
        The minimal amount of balance the seller requested.
    
    purchaser_balance_amount : `int`
        The amount of balance the purchaser bid with.
    
    notification_content_prefix : `str`
        Value to prefix notification content with.
    
    Yields
    ------
    part : `str`
    """
    yield notification_content_prefix
    yield ', '
    yield ('your offer' if user_id == seller_user_id else 'you purchased')
    yield ' '
    
    item = get_item(item_id)
    yield str(item_amount)
    yield ' '
    
    emoji = item.emoji
    if (emoji is not None):
        yield emoji.as_emoji
    
    yield ' '
    yield item.name
    yield ' ('
    yield from produce_kilogram(item.weight * item_amount)
    yield ')'
    
    if user_id != seller_user_id:
        balance_description_prefix = 'for'
        balance_amount = purchaser_balance_amount
        balance_description_postfix = None
    else:
        if purchaser_user_id:
            balance_description_prefix = 'was sold for'
            balance_amount = purchaser_balance_amount
            balance_description_postfix = None
        else:
            balance_description_prefix = 'starting at'
            balance_amount = seller_balance_amount
            balance_description_postfix = 'was not sold'
    
    if balance_amount:
        yield ' '
        yield balance_description_prefix
        yield ' '
        yield str(balance_amount)
        yield ' '
        yield EMOJI__HEART_CURRENCY.as_emoji
    
    if (balance_description_postfix is not None):
        yield ' '
        yield balance_description_postfix
    
    yield '.'


def build_notification_components(
    preferred_client_id,
    user_id,
    entry_id,
    seller_user_id,
    purchaser_user_id,
    item_id,
    item_amount,
    seller_balance_amount,
    purchaser_balance_amount,
):
    """
    Notification builder.
    
    Parameters
    ----------
    preferred_client_id : `int`
        The notifier client's identifier to select style for.
    
    user_id : `int`
        The point of view user's identifier.
    
    entry_id : `int`
        The entry's identifier.
    
    seller_user_id : `int`
        The seller user's identifier.
    
    purchaser_user_id : `int`
        The purchaser user's identifier.
    
    item_id : `int`
        The item's identifier.
    
    item_amount : ``int`
        The sold items' amount.
    
    seller_balance_amount : `int`
        The minimal amount of balance the seller requested.
    
    purchaser_balance_amount : `int`
        The amount of balance the purchaser bid with.
    
    Returns
    -------
    components : ``list<Component>``
    """
    if preferred_client_id == FLANDRE_ID:
        notification_content_prefix = 'Nee-sama'
        disable_notification_button_text = 'Go back to your basement!!'
    else:
        notification_content_prefix = 'Hey mister'
        disable_notification_button_text = 'I don\'t want notifs, nya!!'
    
    return [
        create_text_display(''.join([*produce_notification_content(
            user_id,
            seller_user_id,
            purchaser_user_id,
            item_id,
            item_amount,
            seller_balance_amount,
            purchaser_balance_amount,
            notification_content_prefix,
        )])),
        create_row(
            create_button(
                'Claim',
                custom_id = CUSTOM_ID_MARKET_PLACE_INBOX_CLAIM_ONE_BUILDER(
                    user_id, 0, MARKET_PLACE_INBOX_PAGE_SIZE_DEFAULT, entry_id, True
                ),
                style = ButtonStyle.green,
            ),
            create_button(
                disable_notification_button_text,
                custom_id = USER_SETTINGS_CUSTOM_ID_NOTIFICATION_MARKET_PLACE_ITEM_FINALISATION_DISABLE,
            ),
        ),
    ]
