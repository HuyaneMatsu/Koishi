__all__ = ()

from dateutil.relativedelta import relativedelta as RelativeDelta
from hata import elapsed_time

from ...bot_utils.constants import EMOJI__HEART_CURRENCY

from ..item_modifier_core import produce_modifiers_section
from ..item_core import get_item, produce_flags_section, produce_weight

from .constants import ITEM_CATEGORY_CHOICES


def _produce_item_with_amount(item, item_amount):
    """
    Produces an item with its amount.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    item : ``Item``
        The item to produce.
    
    item_amount : `int`
        The item's amount.
    
    Yields
    ------
    part : `str`
    """
    yield str(item_amount)
    yield ' '
    
    emoji = item.emoji
    if (emoji is not None):
        yield emoji.as_emoji
    
    yield ' '
    yield item.name
    yield ' ('
    yield from produce_weight(item.weight * item_amount)
    yield ' kg)'


def produce_sell_confirmation_description(
    item,
    item_amount,
    duration_days,
    starting_sell_price,
    initial_sell_fee,
):
    """
    Builds sell confirmation description.
    
    This function is an iterable generator.
    
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
    
    Yields
    ------
    part : `str`
    """
    yield 'Are you sure to put '
    yield from _produce_item_with_amount(item, item_amount)
    yield ' on the market for '
    yield str(duration_days)
    yield ' days'
    
    if starting_sell_price:
        yield ', starting at '
        yield str(starting_sell_price)
        yield ' '
        yield EMOJI__HEART_CURRENCY.as_emoji
    
    yield '?\nYou will have to pay '
    yield str(initial_sell_fee)
    yield ' '
    yield EMOJI__HEART_CURRENCY.as_emoji
    yield ' initial fee.'


def produce_sell_success_description(item, item_amount, duration_days, starting_sell_price, initial_sell_fee):
    """
    Builds sell success description.
    
    This function is an iterable generator.
    
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
    
    Yields
    ------
    part : `str`
    """
    yield 'You put '
    yield from _produce_item_with_amount(item, item_amount)
    yield ' on the market for '
    yield str(duration_days)
    yield ' days'
    
    if starting_sell_price:
        yield ', starting at '
        yield str(starting_sell_price)
        yield ' '
        yield EMOJI__HEART_CURRENCY.as_emoji
    
    yield '.\nYou payed '
    yield str(initial_sell_fee)
    yield ' '
    yield EMOJI__HEART_CURRENCY.as_emoji
    yield ' initial fee.'


def produce_offer_market_place_item_description(market_place_item, now):
    """
    Produces an my offer market place item's description.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    market_place_item : ``MarketPlaceItem``
        The market place item to render.
    
    now : `DateTime`
        The current time.
    
    Yields
    ------
    part : `str`
    """
    # Produce item
    yield from _produce_item_with_amount(get_item(market_place_item.item_id), market_place_item.item_amount)
    yield '\n'
    
    # Produce time left
    yield 'Time left: '
    yield elapsed_time(RelativeDelta(now, market_place_item.finalises_at))
    yield '\n'
    
    # Produce highest offer
    while True:
        purchaser_balance_amount = market_place_item.purchaser_balance_amount
        if purchaser_balance_amount:
            title = 'Highest bid'
            balance_amount = purchaser_balance_amount
            break
        
        seller_balance_amount = market_place_item.seller_balance_amount
        if seller_balance_amount:
            title = 'Starting price'
            balance_amount = seller_balance_amount
            break
        
        title = None
        balance_amount = 0
        break
    
    if (title is None):
        yield 'No bids yet...'
    
    else:
        yield title
        yield ': '
        yield str(balance_amount)
        yield ' '
        yield EMOJI__HEART_CURRENCY.as_emoji


def produce_inbox_unsold_market_place_item_description(market_place_item, now):
    """
    Produces inbox untaken market place item description.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    market_place_item : ``MarketPlaceItem``
        The market place item to render.
    
    now : `DateTime`
        The current time.
    
    Yields
    ------
    part : `str`
    """
    # Produce item
    yield 'Your '
    yield from _produce_item_with_amount(get_item(market_place_item.item_id), market_place_item.item_amount)
    yield ' offer\n'
    
    # Produce finalised
    yield 'Finalised: '
    yield elapsed_time(RelativeDelta(market_place_item.finalises_at, now))
    yield ' ago\n'
    
    # Produce starting price
    seller_balance_amount = market_place_item.seller_balance_amount
    if seller_balance_amount:
        yield 'Starting at '
        yield str(seller_balance_amount)
        yield ' '
        yield EMOJI__HEART_CURRENCY.as_emoji
        yield ' w'
    
    else:
        yield 'W'
    
    # Produce note
    yield 'as not sold D:'


def produce_inbox_purchased_market_place_item_description(market_place_item, now):
    """
    Produces inbox purchased market place item description.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    market_place_item : ``MarketPlaceItem``
        The market place item to render.
    
    now : `DateTime`
        The current time.
    
    Yields
    ------
    part : `str`
    """
    # Produce item
    yield 'You purchased '
    yield from _produce_item_with_amount(get_item(market_place_item.item_id), market_place_item.item_amount)
    yield '\n'
    
    # Produce finalised
    yield 'Finalised: '
    yield elapsed_time(RelativeDelta(market_place_item.finalises_at, now))
    yield ' ago\n'
    
    # produce purchase price
    yield 'For '
    yield str(market_place_item.purchaser_balance_amount)
    yield ' '
    yield EMOJI__HEART_CURRENCY.as_emoji
    yield ' :3'


def produce_inbox_sold_market_place_item_description(market_place_item, now):
    """
    Produces inbox sold market place item description.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    market_place_item : ``MarketPlaceItem``
        The market place item to render.
    
    now : `DateTime`
        The current time.
    
    Yields
    ------
    part : `str`
    """
    # Produce item
    yield 'Your '
    yield from _produce_item_with_amount(get_item(market_place_item.item_id), market_place_item.item_amount)
    yield ' offer\n'
    
    # Produce finalised
    yield 'Finalised: '
    yield elapsed_time(RelativeDelta(market_place_item.finalises_at, now))
    yield ' ago\n'
    
    # produce purchase price
    yield 'Was sold for '
    yield str(market_place_item.purchaser_balance_amount)
    yield ' '
    yield EMOJI__HEART_CURRENCY.as_emoji
    yield ' :D'


def produce_claim_unsold_description(
    item,
    item_amount,
    reward_balance,
    fee,
):
    """
    Produces claim unsold description.
    
    Parameters
    ----------
    item : ``Item``
        Item to be sold.
    
    item_amount : `int`
        The amount of items to be sold.
    
    reward_balance : `int`
        The reward balance.
    
    fee : `int`
        Fee payed.
    
    Yields
    ------
    part : `str`
    """
    yield 'You received your '
    yield from _produce_item_with_amount(item, item_amount)
    yield ' back, after nobody bought it.'


def produce_claim_purchased_description(
    item,
    item_amount,
    reward_balance,
    fee,
):
    """
    Produces claim unsold description.
    
    Parameters
    ----------
    item : ``Item``
        Item to be sold.
    
    item_amount : `int`
        The amount of items to be sold.
    
    reward_balance : `int`
        The reward balance.
    
    fee : `int`
        Fee payed.
    
    Yields
    ------
    part : `str`
    """
    yield 'You received the '
    yield from _produce_item_with_amount(item, item_amount)
    yield ', that you purchased for '
    yield str(reward_balance)
    yield ' '
    yield EMOJI__HEART_CURRENCY.as_emoji
    yield '.'


def produce_claim_sold_description(
    item,
    item_amount,
    reward_balance,
    fee,
):
    """
    Produces claim unsold description.
    
    Parameters
    ----------
    item : ``Item``
        Item to be sold.
    
    item_amount : `int`
        The amount of items to be sold.
    
    reward_balance : `int`
        The reward balance.
    
    fee : `int`
        Fee payed.
    
    Yields
    ------
    part : `str`
    """
    yield 'You received '
    yield str(reward_balance)
    yield ' '
    yield EMOJI__HEART_CURRENCY.as_emoji
    if fee > 0:
        yield ', after paying additional '
        yield str(fee)
        yield ' '
        yield EMOJI__HEART_CURRENCY.as_emoji
        yield ' fee'
    
    yield ', for selling '
    yield from _produce_item_with_amount(item, item_amount)
    yield '.'


def produce_purchase_view_header(item, required_flags, page_index):
    """
    Produces purchase view header.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    item : ``None | Item``
        Item the user is filtering for.
    
    required_flags : `int`
        Item flags the user is filtering for.
    
    page_index : `int`
        The page's index.
    
    Yields
    ------
    part : `str`
    """
    yield '# Market place\nPage: '
    yield str(page_index + 1)
    
    while True:
        if (item is not None):
            yield '; filtered for item: '
            emoji = item.emoji
            if (emoji is not None):
                yield emoji.as_emoji
                yield ' '
            
            yield item.name
            break
        
        if required_flags:
            for name, value in ITEM_CATEGORY_CHOICES:
                if value == required_flags:
                    break
            else:
                name = 'unknown'
            
            yield '; filtered for category: '
            yield name
            break
        
        # No more cases
        break


def produce_item_description(item_id):
    """
    Produces item description for the given identifier.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    item_id : `int`
        Item identifier.
    
    Yields
    ------
    part : `str`
    """
    item = get_item(item_id)
    
    description = item.description
    if (description is not None):
        yield description
        yield '\n\n'
    
    yield '### Trading information\nWeight: '
    yield from produce_weight(item.weight)
    yield ' kg\nValue: '
    yield str(item.value)
    yield ' '
    yield EMOJI__HEART_CURRENCY.as_emoji
    
    flags = item.flags
    if flags:
        yield '\n### Categories\n'
        yield from produce_flags_section(flags)
    
    modifiers = item.modifiers
    if (modifiers is not None):
        yield '\n### Modifiers\n'
        yield from produce_modifiers_section(modifiers)
