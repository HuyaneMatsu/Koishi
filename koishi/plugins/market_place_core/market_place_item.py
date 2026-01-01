__all__ = ('MarketPlaceItem',)

from datetime import timezone as TimeZone

from hata import DATETIME_FORMAT_CODE
from scarletio import RichAttributeErrorBaseType


class MarketPlaceItem(RichAttributeErrorBaseType):
    """
    Represents an entry in the market.
    
    Parameters
    -----------
    finalises_at : `DateTime`
        When the bid ends.
    
    entry_id : `int`
        Entry identifier.
    
    flags : `int`
        Additional bitwise flags describing the entry.
    
    initial_sell_fee : `int`
        The amount of balance the user initially payed to create the item.
    
    item_flags : `int`
        The item's flags to simplify the query process.
    
    item_id : `int`
        The item's identifier.
    
    item_amount : `int`
        Item amount.
    
    purchaser_user_id : `int`
        The purchaser user's identifier.
    
    purchaser_balance_amount : `int`
        Buyer balance amount.
    
    seller_balance_amount : `int`
        The seller's initial required balance.
    
    seller_user_id : `int`
        The seller user's identifier.
    """
    __slots__ = (
        '__weakref__', 'finalises_at', 'entry_id', 'flags', 'initial_sell_fee', 'item_flags', 'item_id', 'item_amount',
        'purchaser_user_id', 'purchaser_balance_amount', 'seller_balance_amount', 'seller_user_id'
    )
    
    def __new__(cls, item, item_amount, user_id, balance_amount, finalises_at, initial_sell_fee):
        """
        Creates a new marker place entry.
        
        Parameters
        ----------
        item_id : `int`
            The item put on the market.
        
        item_amount : `int`
            The amount of items put on the market.
        
        user_id : `int`
            The user's identifier.
        
        balance_amount : `int`
            Initial required balance.
        
        finalises_at : `DateTime`
            When the bet ends.
        
        initial_sell_fee : `int`
            The amount of balance the user initially payed to create the item.
        """ 
        self = object.__new__(cls)
        self.finalises_at = finalises_at
        self.entry_id = 0
        self.flags = 0
        self.initial_sell_fee = initial_sell_fee
        self.item_flags = item.flags
        self.item_id = item.id
        self.item_amount = item_amount
        self.purchaser_user_id = 0
        self.purchaser_balance_amount = 0
        self.seller_balance_amount = balance_amount
        self.seller_user_id = user_id
        return self
    
    
    @classmethod
    def from_entry(cls, entry):
        """
        Creates an automation configuration from the given entry.
        
        Parameters
        ----------
        entry : `sqlalchemy.engine.result.RowProxy`
            The entry to create the instance based on.
        
        Returns
        -------
        self : `instance<cls>`
        """
        self = object.__new__(cls)
        self.finalises_at = entry['finalises_at'].replace(tzinfo = TimeZone.utc)
        self.entry_id = entry['id']
        self.flags = entry['flags']
        self.initial_sell_fee = entry['initial_sell_fee']
        self.item_flags = entry['item_flags']
        self.item_id = entry['item_id']
        self.item_amount = entry['item_amount']
        self.purchaser_user_id = entry['purchaser_user_id']
        self.purchaser_balance_amount = entry['purchaser_balance_amount']
        self.seller_balance_amount = entry['seller_balance_amount']
        self.seller_user_id = entry['seller_user_id']
        return self
    
    
    def __repr__(self):
        """Returns repr(self)."""
        repr_parts = ['<', type(self).__name__]
        
        # entry_id
        entry_id = self.entry_id
        if entry_id:
            repr_parts.append(' entry_id = ')
            repr_parts.append(repr(entry_id))
            repr_parts.append(',')
        
        # finalises_at
        repr_parts.append(' finalises_at = ')
        repr_parts.append(format(self.finalises_at, DATETIME_FORMAT_CODE))
        
        # flags
        repr_parts.append(', flags = ')
        repr_parts.append(repr(self.flags))
        
        # initial_sell_fee
        repr_parts.append(', initial_sell_fee = ')
        repr_parts.append(repr(self.initial_sell_fee))
        
        # item_flags
        repr_parts.append(', item_flags = ')
        repr_parts.append(repr(self.item_flags))
        
        # item_id
        repr_parts.append(', item_id = ')
        repr_parts.append(repr(self.item_id))
        
        # item_amount
        repr_parts.append(', item_amount = ')
        repr_parts.append(repr(self.item_amount))
        
        # purchaser_user_id
        repr_parts.append(' purchaser_user_id = ')
        repr_parts.append(repr(self.purchaser_user_id))
        
        # purchaser_balance_amount
        repr_parts.append(', purchaser_balance_amount = ')
        repr_parts.append(repr(self.purchaser_balance_amount))
        
        # seller_balance_amount
        repr_parts.append(', seller_balance_amount = ')
        repr_parts.append(repr(self.seller_balance_amount))
        
        # seller_user_id
        repr_parts.append(', seller_user_id = ')
        repr_parts.append(repr(self.seller_user_id))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
