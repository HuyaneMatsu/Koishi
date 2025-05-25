__all__ = ('UserBalance',)

from datetime import datetime as DateTime, timezone as TimeZone
from hata import DATETIME_FORMAT_CODE
from scarletio import copy_docs

from ...bot_utils.entry_proxy import EntryProxy

from .user_balance_saver import UserBalanceSaver
from .constants import USER_RELATIONSHIP_SLOTS_DEFAULT, USER_BALANCE_CACHE, USER_BALANCE_CACHE_SIZE


class UserBalance(EntryProxy):
    """
    User balance.
    
    Attributes
    ----------
    allocated : `int`
        How much hearts the user cannot use currently due to they being in use by a command temporarily.
    
    balance : `int`
        The total love of the user.
    
    count_daily_by_related : `int`
        How much daily times the user got claimed by someone else.
    
    count_daily_for_related : `int`
        How much times the user claimed daily of someone else.
    
    count_daily_self : `int`
        How much times the user claimed their own daily.
    
    count_top_gg_vote : `int`
        How much times the user voted on us on top.gg.
    
    daily_can_claim_at : `DateTime`
        When the user can vote next.
    
    daily_reminded : `bool`
        Whether the user had their daily reminded and should not be reminded again till they claim actually claim
        their daily.
    
    streak : `int`
        The user's daily streak
    
    entry_id : `int`
        The entry's identifier in the database.
    
    top_gg_voted_at : `DateTime`
        When the user voted on the bot last time on top.gg.
    
    user_id : `int`
        The parent user's identifier.
    
    relationship_value : `int`
        The user's waifu cost.
    
    relationship_divorces : `int`
        How much times the user divorced.
    
    relationship_slots : `int`
        The maximal amount of waifus the user can have.
    
    saver : ``None | UserBalanceSaver``
        Saver set while saving.
    """
    __slots__ = (
        'balance', 'allocated', 'count_daily_by_related', 'count_daily_for_related', 'count_daily_self',
        'count_top_gg_vote', 'daily_can_claim_at', 'daily_reminded', 'streak', 'top_gg_voted_at', 'user_id',
        'relationship_value', 'relationship_divorces', 'relationship_slots',
    )
    
    saver_type = UserBalanceSaver
    
    
    def __new__(cls, user_id):
        """
        Creates a new user balance.
        
        Parameters
        ----------
        user_id : `int`
            The parent user identifier.
        """
        now = DateTime.now(TimeZone.utc)
        
        self = object.__new__(cls)
        self.allocated = 0
        self.balance = 0
        self.count_daily_by_related = 0
        self.count_daily_for_related = 0
        self.count_daily_self = 0
        self.count_top_gg_vote = 0
        self.daily_can_claim_at = now
        self.daily_reminded = False
        self.entry_id = -1
        self.streak = 0
        self.saver = None
        self.top_gg_voted_at = now
        self.user_id = user_id
        self.relationship_value = 0
        self.relationship_divorces = 0
        self.relationship_slots = USER_RELATIONSHIP_SLOTS_DEFAULT
        return self
    
    
    @copy_docs(EntryProxy._put_repr_parts)
    def _put_repr_parts(self, repr_parts, field_added):
        if field_added:
            repr_parts.append(',')
        
        # user_id
        repr_parts.append(' user_id = ')
        repr_parts.append(repr(self.user_id))
        
        # balance
        balance = self.balance
        if balance:
            repr_parts.append(', balance = ')
            repr_parts.append(repr(balance))
        
        # allocated
        allocated = self.allocated
        if allocated:
            repr_parts.append(', allocated = ')
            repr_parts.append(repr(allocated))
        
        # count_daily_self
        count_daily_self = self.count_daily_self
        if count_daily_self:
            repr_parts.append(', count_daily_self = ')
            repr_parts.append(repr(count_daily_self))
        
        # count_daily_by_related
        count_daily_by_related = self.count_daily_by_related
        if count_daily_by_related:
            repr_parts.append(', count_daily_by_related = ')
            repr_parts.append(repr(count_daily_by_related))
        
        # count_daily_for_related
        count_daily_for_related = self.count_daily_for_related
        if count_daily_for_related:
            repr_parts.append(', count_daily_for_related = ')
            repr_parts.append(repr(count_daily_for_related))
        
        # count_top_gg_vote
        count_top_gg_vote = self.count_top_gg_vote
        if count_top_gg_vote:
            repr_parts.append(', count_top_gg_vote = ')
            repr_parts.append(repr(count_top_gg_vote))
        
        # daily_reminded
        daily_reminded = self.daily_reminded
        if daily_reminded:
            repr_parts.append(', daily_reminded = ')
            repr_parts.append(repr(daily_reminded))
        
        # daily_can_claim_at
        daily_can_claim_at = self.daily_can_claim_at
        repr_parts.append(', daily_can_claim_at = ')
        repr_parts.append(format(daily_can_claim_at, DATETIME_FORMAT_CODE))
        
        # streak
        streak = self.streak
        repr_parts.append(', streak = ')
        repr_parts.append(repr(streak))
        
        # top_gg_voted_at
        top_gg_voted_at = self.top_gg_voted_at
        repr_parts.append(', top_gg_voted_at = ')
        repr_parts.append(format(top_gg_voted_at, DATETIME_FORMAT_CODE))
        
        # relationship_value
        relationship_value = self.relationship_value
        if relationship_value:
            repr_parts.append(', relationship_value = ')
            repr_parts.append(repr(relationship_value))
        
        # relationship_divorces
        relationship_divorces = self.relationship_divorces
        if relationship_divorces:
            repr_parts.append(', relationship_divorces = ')
            repr_parts.append(repr(relationship_divorces))
        
        # relationship_slots
        relationship_slots = self.relationship_slots
        if relationship_slots != USER_RELATIONSHIP_SLOTS_DEFAULT:
            repr_parts.append(', relationship_slots = ')
            repr_parts.append(repr(relationship_slots))
    
    
    async def save(self):
        """
        Saves the entry and then caches it.
        
        This function is a coroutine.
        """
        saver = self.get_saver()
        await saver.begin()
        self._store_in_cache()
    
    
    @copy_docs(EntryProxy._store_in_cache)
    def _store_in_cache(self):
        user_id = self.user_id
        if user_id in USER_BALANCE_CACHE:
            USER_BALANCE_CACHE.move_to_end(user_id)
        else:
            USER_BALANCE_CACHE[user_id] = self
            
            if len(USER_BALANCE_CACHE) > USER_BALANCE_CACHE_SIZE:
                del USER_BALANCE_CACHE[next(iter(USER_BALANCE_CACHE))]
    
    
    @copy_docs(EntryProxy._pop_from_cache)
    def _pop_from_cache(self):
        try:
            del USER_BALANCE_CACHE[self.user_id]
        except KeyError:
            pass
    
    
    @classmethod
    @copy_docs(EntryProxy.from_entry)
    def from_entry(cls, entry):
        user_id = entry['user_id']
        
        try:
            self = USER_BALANCE_CACHE[user_id]
        except KeyError:
            self = object.__new__(cls)
            self.user_id = user_id
            self.saver = None
            USER_BALANCE_CACHE[user_id] = self
        
        self.entry_id = entry['id']
        self.allocated = entry['allocated']
        self.balance = entry['balance']
        self.count_daily_by_related = entry['count_daily_by_related']
        self.count_daily_for_related = entry['count_daily_for_related']
        self.count_daily_self = entry['count_daily_self']
        self.count_top_gg_vote = entry['count_top_gg_vote']
        self.daily_can_claim_at = entry['daily_can_claim_at'].replace(tzinfo = TimeZone.utc)
        self.daily_reminded = entry['daily_reminded']
        self.streak = entry['streak']
        self.top_gg_voted_at = entry['top_gg_voted_at'].replace(tzinfo = TimeZone.utc)
        self.relationship_value = entry['relationship_value']
        self.relationship_divorces = entry['relationship_divorces']
        self.relationship_slots = entry['relationship_slots']
        
        return self
