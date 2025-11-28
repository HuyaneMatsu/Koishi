__all__ = ('UserBalance',)

from datetime import datetime as DateTime, timezone as TimeZone
from hata import DATETIME_FORMAT_CODE
from scarletio import RichAttributeErrorBaseType

from .constants import ALLOCATION_STRUCT, ALLOCATION_STRUCT_SIZE, USER_RELATIONSHIP_SLOTS_DEFAULT


class UserBalance(RichAttributeErrorBaseType):
    """
    User balance.
    
    Attributes
    ----------
    allocations : `None | bytes`
        The allocations binary packed.
    
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
    
    entry_id : `int`
        The entry's identifier in the database.
    
    modified_fields : `None | dict<str, object>`
        The name of the already modified fields.
    
    relationship_divorces : `int`
        How much times the user divorced.
    
    relationship_slots : `int`
        The maximal amount of waifus the user can have.
    
    relationship_value : `int`
        The user's waifu cost.
    
    streak : `int`
        The user's daily streak
    
    top_gg_voted_at : `DateTime`
        When the user voted on the bot last time on top.gg.
    
    user_id : `int`
        The parent user's identifier.
    """
    __slots__ = (
        '__weakref__', 'allocations', 'balance', 'count_daily_by_related', 'count_daily_for_related',
        'count_daily_self', 'count_top_gg_vote', 'daily_can_claim_at', 'daily_reminded', 'entry_id', 'modified_fields',
        'relationship_divorces', 'relationship_slots', 'relationship_value', 'streak', 'top_gg_voted_at', 'user_id', 
    )
    
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
        self.allocations = None
        self.balance = 0
        self.count_daily_by_related = 0
        self.count_daily_for_related = 0
        self.count_daily_self = 0
        self.count_top_gg_vote = 0
        self.daily_can_claim_at = now
        self.daily_reminded = False
        self.entry_id = 0
        self.modified_fields = None
        self.relationship_divorces = 0
        self.relationship_slots = USER_RELATIONSHIP_SLOTS_DEFAULT
        self.relationship_value = 0
        self.streak = 0
        self.top_gg_voted_at = now
        self.user_id = user_id
        return self
    
    
    def __repr__(self):
        """Returns repr(self)."""
        repr_parts = ['<', type(self).__name__]
        
        # user_id
        repr_parts.append(' user_id = ')
        repr_parts.append(repr(self.user_id))
        
        # entry_id
        entry_id = self.entry_id
        if (entry_id is not None):
            repr_parts.append(', entry_id = ')
            repr_parts.append(repr(entry_id))
        
        # balance
        balance = self.balance
        if balance:
            repr_parts.append(', balance = ')
            repr_parts.append(repr(balance))
        
        # allocations
        allocations = self.allocations
        if (allocations is not None):
            repr_parts.append(', allocations = ')
            repr_parts.append(repr(allocations))
        
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
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    @classmethod
    def from_entry(cls, entry):
        """
        Creates an entry proxy from the given entry.
        
        Parameters
        ----------
        entry : `sqlalchemy.engine.result.RowProxy`
            The entry to create the instance based on.
        
        Returns
        -------
        self : `instance<cls>`
        """
        self = object.__new__(cls)
        self.user_id = entry['user_id']
        self.modified_fields = None
        self.entry_id = entry['id']
        self.allocations = entry['allocations']
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
    
    
    def _mark_modification(self, key, value):
        """
        Marks a field as modified.
        
        Parameters
        ----------
        key : `str`
            The field's key.
        
        value : `object`
            The field's value.
        """
        modified_fields = self.modified_fields
        if (modified_fields is None):
            self.modified_fields = modified_fields = {}
        
        modified_fields[key] = value
    
    
    def iter_allocations(self):
        """
        Iterates over the allocations of the user balance.
        
        This function is an iterable generator.
        
        Yields
        ------
        allocation : `(int, int, int)`
        
        """
        allocations = self.allocations
        if (allocations is not None):
            yield from ALLOCATION_STRUCT.iter_unpack(allocations)
    
    
    def get_cumulative_allocated_balance(self):
        """
        Gets the cumulatively allocated balance.
        
        Returns
        -------
        cumulative_allocated_balance : `int`
        """
        return sum(allocation[2] for allocation in self.iter_allocations())
    
    
    def add_allocation(self, allocation_feature_id, session_id, amount):
        """
        Adds a new allocation to the user balance.
        
        Parameters
        ----------
        allocation_feature_id : `int`
            The allocation's feature's identifier.
        
        session_id : `int`
            The internal session identifier of the feature.
        
        amount : `int`
            The amount of allocated balance.
        """
        allocation = ALLOCATION_STRUCT.pack(allocation_feature_id, session_id, amount)
        allocations = self.allocations
        if (allocations is None):
            allocations = allocation
        else:
            allocations = allocations + allocation
        self.allocations = allocations
        self._mark_modification('allocations', allocations)
    
    
    def remove_allocation(self, allocation_feature_id, session_id):
        """
        Removes a single allocation.
        
        Parameters
        ----------
        allocation_feature_id : `int`
            The allocation's feature's identifier.
        
        session_id : `int`
            The internal session identifier of the feature.
        """
        allocations = self.allocations
        if (allocations is None):
            return
        
        for (
            index, (iterated_allocation_feature_id, iterated_session_id, amount)
        ) in enumerate(ALLOCATION_STRUCT.iter_unpack(allocations)):
            if (allocation_feature_id == iterated_allocation_feature_id) and (session_id == iterated_session_id):
                break
        else:
            return
        
        allocations_size = len(allocations)
        if allocations_size == ALLOCATION_STRUCT_SIZE:
            allocations = None
        else:
            allocations = (
                allocations[: index * ALLOCATION_STRUCT_SIZE] +
                allocations[(index + 1) * ALLOCATION_STRUCT_SIZE :]
            )
        
        self.allocations = allocations
        self._mark_modification('allocations', allocations)
    
    
    def modify_balance_by(self, amount):
        """
        Modifies the balance by the given amount.
        
        Parameters
        ----------
        amount : `int`
            Amount to modify the balance by.
        """
        self.balance = balance = max(self.balance + amount, 0)
        self._mark_modification('balance', balance)
    
    
    def modify_relationship_value_by(self, amount):
        """
        Modifies the relationship value by the given amount.
        
        Parameters
        ----------
        amount : `int`
            Amount to modify the relationship value by.
        """
        self.relationship_value = relationship_value = max(self.relationship_value + amount, 0)
        self._mark_modification('relationship_value', relationship_value)
    
    
    def set_relationship_value(self, amount):
        """
        Sets the relationship .
        
        Parameters
        ----------
        amount : `int`
            Amount to set the relationship value to.
        """
        self.relationship_value = amount
        self._mark_modification('relationship_value', amount)
    
    
    def set_streak(self, amount):
        """
        Sets the streak to the given value.
        Parameters
        ----------
        amount : `int`
            Amount to set to.
        """
        self.streak = amount
        self._mark_modification('streak', amount)
    
    
    def set_daily_can_claim_at(self, date_time):
        """
        Sets the daily can claim at to the given value.
        
        Parameters
        ----------
        date_time : `DateTime`
            Amount to set to.
        """
        self.daily_can_claim_at = date_time
        self._mark_modification('daily_can_claim_at', date_time)
    
    
    def set_top_gg_voted_at(self, date_time):
        """
        Sets the top gg voted at to the given value.
        
        Parameters
        ----------
        date_time : `DateTime`
            Amount to set to.
        """
        self.top_gg_voted_at = date_time
        self._mark_modification('top_gg_voted_at', date_time)
    
    
    def increment_count_daily_self(self):
        """
        Increments the daily count self.
        """
        self.count_daily_self = count_daily_self = self.count_daily_self + 1
        self._mark_modification('count_daily_self', count_daily_self)
    
    
    def increment_count_daily_for_related(self):
        """
        Increments the daily count for related.
        """
        self.count_daily_for_related = count_daily_for_related = self.count_daily_for_related + 1
        self._mark_modification('count_daily_for_related', count_daily_for_related)
    
    
    def increment_count_daily_by_related(self):
        """
        Increments the daily count by related.
        """
        self.count_daily_by_related = count_daily_by_related = self.count_daily_by_related + 1
        self._mark_modification('count_daily_by_related', count_daily_by_related)
    
    
    def increment_count_top_gg_vote(self):
        """
        Increments the top gg vote count.
        """
        self.count_top_gg_vote = count_top_gg_vote = self.count_top_gg_vote + 1
        self._mark_modification('count_top_gg_vote', count_top_gg_vote)
    
    
    def increment_relationship_slots(self):
        """
        Increments the relationship slots.
        """
        self.relationship_slots = relationship_slots = self.relationship_slots + 1
        self._mark_modification('relationship_slots', relationship_slots)
    
    
    def increment_relationship_divorces(self):
        """
        Increments the relationship divorces.
        """
        self.relationship_divorces = relationship_divorces = self.relationship_divorces + 1
        self._mark_modification('relationship_divorces', relationship_divorces)

    
    def decrement_relationship_divorces(self):
        """
        Decrements the relationship divorces.
        """
        self.relationship_divorces = relationship_divorces = max(self.relationship_divorces - 1, 0)
        self._mark_modification('relationship_divorces', relationship_divorces)
    
    
    def set_daily_reminded(self, value):
        """
        Sets whether the user had their daily reminded.
        
        Parameters
        ----------
        value : `bool`
            Value to set.
        """
        self.daily_reminded = value
        self._mark_modification('daily_reminded', value)
