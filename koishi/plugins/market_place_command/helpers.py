__all__ = ()

from config import MARISA_MODE

from math import log, ceil
from scarletio import copy_docs

from .constants import BID_INCREASE_LOWER_THRESHOLD, BID_INCREASE_REQUIRED_RATIO, DURATION_DAYS_THRESHOLD_LOWER


def calculate_initial_sell_fee(item, item_amount, duration_days, starting_sell_price):
    """
    Calculates initial sell fee.
    
    Parameters
    ----------
    item : ``Item``
        Item to get tax for.
    
    item_amount : `int`
        Item amount.
    
    duration_days : `int`
        The amount of days the item will be auctioned for.
    
    starting_sell_price : `int`
        Starting sell price.
    
    Returns
    -------
    sell_fee : `int`
    """
    # Weight
    weight_factor = (item.weight * item_amount) * 0.0001
    if weight_factor < 1.0:
        weight_factor = 1.0
    
    # Duration days
    duration_days_factor = 1.0 + (duration_days - DURATION_DAYS_THRESHOLD_LOWER) * 0.05
    
    # Starting sell price.
    if not starting_sell_price:
        starting_sell_price_factor = 1.0
    else:
        starting_sell_price_factor = log(starting_sell_price, (item.value * item_amount * 4.0))
        if starting_sell_price_factor < 1.0:
            starting_sell_price_factor = 1.0
        else:
            starting_sell_price_factor *= starting_sell_price_factor
    
    return ceil(50 * weight_factor * duration_days_factor * starting_sell_price_factor)


def calculate_lowest_required_bid_amount(current_highest_bid):
    """
    Calculates the lowest required bid amount.
    
    Parameters
    ----------
    current_highest_bid : `int`
        The current highest bid amount.
    
    Returns
    -------
    amount : `int`
    """
    return (
        current_highest_bid +
        max(ceil(current_highest_bid * BID_INCREASE_REQUIRED_RATIO), BID_INCREASE_LOWER_THRESHOLD)
    )


def calculate_duration(duration_days):
    """
    Calculates the duration in seconds how long the offer should be alive for.
    
    Parameters
    ----------
    duration_days : `int`
        The amount of days the item will be auctioned for.
    
    Returns
    -------
    duration_seconds : `int`
    """
    return duration_days * 86400


if MARISA_MODE:
    # Speed up the duration when testing.
    @copy_docs(calculate_duration)
    def calculate_duration(duration_days):
        return duration_days * 60
