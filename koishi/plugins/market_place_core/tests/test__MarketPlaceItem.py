from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ...item_core import ITEM_ID_PEACH, get_item

from ..market_place_item import MarketPlaceItem


def _assert_fields_set(market_place_item):
    """
    Asserts whether every fields are set of the given market place entry.
    
    Parameters
    ----------
    market_place_item : ``MarketPlaceItem``
        The instance to check.
    """
    vampytest.assert_instance(market_place_item, MarketPlaceItem)
    vampytest.assert_instance(market_place_item.finalises_at, DateTime)
    vampytest.assert_instance(market_place_item.entry_id, int)
    vampytest.assert_instance(market_place_item.flags, int)
    vampytest.assert_instance(market_place_item.initial_sell_fee, int)
    vampytest.assert_instance(market_place_item.item_flags, int)
    vampytest.assert_instance(market_place_item.item_id, int)
    vampytest.assert_instance(market_place_item.item_amount, int)
    vampytest.assert_instance(market_place_item.purchaser_user_id, int)
    vampytest.assert_instance(market_place_item.purchaser_balance_amount, int)
    vampytest.assert_instance(market_place_item.seller_balance_amount, int)
    vampytest.assert_instance(market_place_item.seller_user_id, int)


def test__MarketPlaceItem__new():
    """
    Tests whether ``MarketPlaceItem.__new__`` works as intended.
    """
    item = get_item(ITEM_ID_PEACH)
    item_amount = 30
    user_id = 202512220000
    balance_amount = 20
    finalises_at = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    initial_sell_fee = 100
    
    market_place_item = MarketPlaceItem(
        item,
        item_amount,
        user_id,
        balance_amount,
        finalises_at,
        initial_sell_fee,
    )
    _assert_fields_set(market_place_item)
    
    vampytest.assert_eq(market_place_item.item_flags, item.flags)
    vampytest.assert_eq(market_place_item.item_id, item.id)
    vampytest.assert_eq(market_place_item.item_amount, item_amount)
    vampytest.assert_eq(market_place_item.seller_user_id, user_id)
    vampytest.assert_eq(market_place_item.seller_balance_amount, balance_amount)
    vampytest.assert_eq(market_place_item.finalises_at, finalises_at)
    vampytest.assert_eq(market_place_item.initial_sell_fee, initial_sell_fee)


def test__MarketPlaceItem__from_entry():
    """
    Tests whether ``MarketPlaceItem`` works as intended.
    """
    item = get_item(ITEM_ID_PEACH)
    item_amount = 30
    seller_user_id = 202512220001
    seller_balance_amount = 20
    finalises_at = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    flags = 1234
    initial_sell_fee = 100
    purchaser_user_id = 202512220002
    purchaser_balance_amount = 200
    entry_id = 6
    
    market_place_item = MarketPlaceItem.from_entry({
        'item_flags': item.flags,
        'item_id': item.id,
        'item_amount': item_amount,
        'seller_user_id': seller_user_id,
        'seller_balance_amount': seller_balance_amount,
        'finalises_at': finalises_at,
        'flags': flags,
        'initial_sell_fee': initial_sell_fee,
        'purchaser_user_id': purchaser_user_id,
        'purchaser_balance_amount': purchaser_balance_amount,
        'id': entry_id,
    })
    _assert_fields_set(market_place_item)
    
    vampytest.assert_eq(market_place_item.item_flags, item.flags)
    vampytest.assert_eq(market_place_item.item_id, item.id)
    vampytest.assert_eq(market_place_item.item_amount, item_amount)
    vampytest.assert_eq(market_place_item.seller_user_id, seller_user_id)
    vampytest.assert_eq(market_place_item.seller_balance_amount, seller_balance_amount)
    vampytest.assert_eq(market_place_item.finalises_at, finalises_at)
    vampytest.assert_eq(market_place_item.flags, flags)
    vampytest.assert_eq(market_place_item.initial_sell_fee, initial_sell_fee)
    vampytest.assert_eq(market_place_item.purchaser_user_id, purchaser_user_id)
    vampytest.assert_eq(market_place_item.purchaser_balance_amount, purchaser_balance_amount)
    vampytest.assert_eq(market_place_item.entry_id, entry_id)


def test__MarketPlaceItem__repr():
    """
    Tests whether ``MarketPlaceItem.__repr__`` works as intended.
    """
    item = get_item(ITEM_ID_PEACH)
    item_amount = 30
    user_id = 202512220003
    balance_amount = 20
    finalises_at = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    initial_sell_fee = 100
    
    market_place_item = MarketPlaceItem(
        item,
        item_amount,
        user_id,
        balance_amount,
        finalises_at,
        initial_sell_fee,
    )
    
    output = repr(market_place_item)
    vampytest.assert_instance(output, str)
