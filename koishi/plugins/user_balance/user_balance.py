__all__ = (
    'UserBalance', 'user_balance_create', 'user_balance_create_from_entry', 'user_balance_iter_allocations',
    'user_balance_accumulate_allocated_balance', 'user_balance_add_allocation', 'user_balance_remove_allocation',
    'user_balance_modify_balance_by', 'user_balance_modify_relationship_value_by',
    'user_balance_set_relationship_value', 'user_balance_set_streak', 'user_balance_set_daily_can_claim_at',
    'user_balance_set_top_gg_voted_at', 'user_balance_increment_count_daily_self', 
    'user_balance_increment_count_daily_for_related', 'user_balance_increment_count_daily_by_related',
    'user_balance_increment_count_top_gg_vote', 'user_balance_increment_relationship_slots',
    'user_balance_increment_relationship_divorces', 'user_balance_decrement_relationship_divorces',
    'user_balance_set_daily_reminded', 'user_balance_collect_modifications'
)

from datetime import datetime as DateTime, timezone as TimeZone
from hata import DATETIME_FORMAT_CODE
from scarletio import RichAttributeErrorBaseType

from .allocation_feature_ids import get_allocation_data_size
from .constants import ALLOCATION_STRUCT, ALLOCATION_STRUCT_SIZE, USER_RELATIONSHIP_SLOTS_DEFAULT


USER_BALANCE_MODIFICATION_FLAG_BALANCE = 1 << 0
USER_BALANCE_MODIFICATION_FLAG_COUNT_DAILY_BY_RELATED = 1 << 1
USER_BALANCE_MODIFICATION_FLAG_COUNT_DAILY_FOR_RELATED = 1 << 2
USER_BALANCE_MODIFICATION_FLAG_COUNT_DAILY_SELF = 1 << 3
USER_BALANCE_MODIFICATION_FLAG_COUNT_TOP_GG_VOTE = 1 << 4
USER_BALANCE_MODIFICATION_FLAG_DAILY_CAN_CLAIM_AT = 1 << 5
USER_BALANCE_MODIFICATION_FLAG_DAILY_REMINDED = 1 << 6
USER_BALANCE_MODIFICATION_FLAG_RELATIONSHIP_DIVORCES = 1 << 7
USER_BALANCE_MODIFICATION_FLAG_RELATIONSHIP_SLOTS = 1 << 8
USER_BALANCE_MODIFICATION_FLAG_RELATIONSHIP_VALUE = 1 << 9
USER_BALANCE_MODIFICATION_FLAG_STREAK = 1 << 10
USER_BALANCE_MODIFICATION_FLAG_TOP_GG_VOTED_AT = 1 << 11
USER_BALANCE_MODIFICATION_FLAG_ALLOCATIONS = 1 << 12


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
    
    modification_flags : `int`
        Bit flags describing which fields were modified.
    
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
        'count_daily_self', 'count_top_gg_vote', 'daily_can_claim_at', 'daily_reminded', 'entry_id',
        'modification_flags', 'relationship_divorces', 'relationship_slots', 'relationship_value', 'streak',
        'top_gg_voted_at', 'user_id', 
    )
    
    
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


def user_balance_create(user_id):
    """
    Creates a new user balance.
    
    Parameters
    ----------
    user_id : `int`
        The parent user identifier.
    
    Returns
    -------
    user_balance : ``UserBalance``
    """
    now = DateTime.now(TimeZone.utc)
    
    user_balance = object.__new__(UserBalance)
    user_balance.allocations = None
    user_balance.balance = 0
    user_balance.count_daily_by_related = 0
    user_balance.count_daily_for_related = 0
    user_balance.count_daily_self = 0
    user_balance.count_top_gg_vote = 0
    user_balance.daily_can_claim_at = now
    user_balance.daily_reminded = False
    user_balance.entry_id = 0
    user_balance.modification_flags = 0
    user_balance.relationship_divorces = 0
    user_balance.relationship_slots = USER_RELATIONSHIP_SLOTS_DEFAULT
    user_balance.relationship_value = 0
    user_balance.streak = 0
    user_balance.top_gg_voted_at = now
    user_balance.user_id = user_id
    return user_balance


def user_balance_create_from_entry(entry):
    """
    Creates an new instance from the given entry.
    
    Parameters
    ----------
    entry : `sqlalchemy.engine.result.RowProxy`
        The entry to create the instance based on.
    
    Returns
    -------
    user_balance : ``UserBalance``
    """
    user_balance = object.__new__(UserBalance)
    user_balance.user_id = entry['user_id']
    user_balance.modification_flags = 0
    user_balance.entry_id = entry['id']
    user_balance.allocations = entry['allocations']
    user_balance.balance = entry['balance']
    user_balance.count_daily_by_related = entry['count_daily_by_related']
    user_balance.count_daily_for_related = entry['count_daily_for_related']
    user_balance.count_daily_self = entry['count_daily_self']
    user_balance.count_top_gg_vote = entry['count_top_gg_vote']
    user_balance.daily_can_claim_at = entry['daily_can_claim_at'].replace(tzinfo = TimeZone.utc)
    user_balance.daily_reminded = entry['daily_reminded']
    user_balance.streak = entry['streak']
    user_balance.top_gg_voted_at = entry['top_gg_voted_at'].replace(tzinfo = TimeZone.utc)
    user_balance.relationship_value = entry['relationship_value']
    user_balance.relationship_divorces = entry['relationship_divorces']
    user_balance.relationship_slots = entry['relationship_slots']
    
    return user_balance


def user_balance_iter_allocations(user_balance):
    """
    Iterates over the allocations of the user balance.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    user_balance : ``UserBalance``
        User balance to work with.
    
    Yields
    ------
    allocation : `(int, int, int, None | memoryview)`
    """
    allocations = user_balance.allocations
    if (allocations is None):
        return
    
    index = 0
    allocations_data_length = len(allocations)
    allocations = memoryview(allocations)
    while index < allocations_data_length:
        end = index + ALLOCATION_STRUCT_SIZE
        allocation_feature_id, session_id, amount = ALLOCATION_STRUCT.unpack(
            allocations[index : end]
        )
        allocation_data_size = get_allocation_data_size(allocation_feature_id)
        if not allocation_data_size:
            data = None
        
        else:
            index = end
            end = index + allocation_data_size
            data = allocations[index : end]
        
        index = end
        yield (allocation_feature_id, session_id, amount, data)


def user_balance_accumulate_allocated_balance(user_balance):
    """
    Gets the cumulatively allocated balance.
    
    Parameters
    ----------
    user_balance : ``UserBalance``
        User balance to work with.
    
    Returns
    -------
    cumulative_allocated_balance : `int`
    """
    allocations = user_balance.allocations
    if (allocations is None):
        return 0
    
    cumulative_allocated_balance = 0
    allocations_data_length = len(allocations)
    allocations = memoryview(allocations)
    index = 0
    while index < allocations_data_length:
        end = index + ALLOCATION_STRUCT_SIZE
        allocation_feature_id, session_id, amount = ALLOCATION_STRUCT.unpack(
            allocations[index : end]
        )
        allocation_data_size = get_allocation_data_size(allocation_feature_id)
        index = end + allocation_data_size
        cumulative_allocated_balance += amount
    
    return cumulative_allocated_balance


def user_balance_add_allocation(user_balance, allocation_feature_id, session_id, amount, data):
    """
    Adds a new allocation to the user balance.
    
    Parameters
    ----------
    user_balance : ``UserBalance``
        User balance to work with.
    
    allocation_feature_id : `int`
        The allocation's feature's identifier.
    
    session_id : `int`
        The internal session identifier of the feature.
    
    amount : `int`
        The amount of allocated balance.
    
    data : `None | bytes`
        Allocation data.
    """
    data_length = (0 if data is None else len(data))
    expected_data_length = get_allocation_data_size(allocation_feature_id)
    
    if data_length != expected_data_length:
        raise RuntimeError(
            f'Badly sized data.\n'
            f'allocation_feature_id = {allocation_feature_id!r}\n'
            f'session_id = {session_id!r}\n'
            f'data = {data!r}\n'
            f'data_length = {data_length!r}\n'
            f'expected_data_length = {expected_data_length!r}\n'
        )
    
    allocation = ALLOCATION_STRUCT.pack(allocation_feature_id, session_id, amount)
    if (data is not None):
        allocation += data
    
    allocations = user_balance.allocations
    if (allocations is None):
        allocations = allocation
    else:
        allocations = allocations + allocation
    user_balance.allocations = allocations
    user_balance.modification_flags |= USER_BALANCE_MODIFICATION_FLAG_ALLOCATIONS


def user_balance_remove_allocation(user_balance, allocation_feature_id, session_id):
    """
    Removes a single allocation.
    
    Parameters
    ----------
    user_balance : ``UserBalance``
        User balance to work with.
    
    allocation_feature_id : `int`
        The allocation's feature's identifier.
    
    session_id : `int`
        The internal session identifier of the feature.
    """
    allocations = user_balance.allocations
    if (allocations is None):
        return
    
    index = 0
    allocations_data_length = len(allocations)
    allocations = memoryview(allocations)
    while index < allocations_data_length:
        end = index + ALLOCATION_STRUCT_SIZE
        iterated_allocation_feature_id, iterated_session_id, iterated_amount = ALLOCATION_STRUCT.unpack(
            allocations[index : end]
        )
        allocation_data_size = get_allocation_data_size(iterated_allocation_feature_id)
        if (allocation_feature_id == iterated_allocation_feature_id) and (session_id == iterated_session_id):
            break
        
        index = end + allocation_data_size
        continue
    
    else:
        return
    
    allocation_size = ALLOCATION_STRUCT_SIZE + allocation_data_size
    if (index == 0) and (allocations_data_length == allocation_size):
        allocations = None
    
    else:
        allocations = b''.join((allocations[: index], allocations[index + allocation_size :]))
    
    user_balance.allocations = allocations
    user_balance.modification_flags |= USER_BALANCE_MODIFICATION_FLAG_ALLOCATIONS


def user_balance_modify_balance_by(user_balance, amount):
    """
    Modifies the balance by the given amount.
    
    Parameters
    ----------
    user_balance : ``UserBalance``
        User balance to work with.
    
    amount : `int`
        Amount to modify the balance by.
    """
    user_balance.balance = max(user_balance.balance + amount, 0)
    user_balance.modification_flags |= USER_BALANCE_MODIFICATION_FLAG_BALANCE


def user_balance_modify_relationship_value_by(user_balance, amount):
    """
    Modifies the relationship value by the given amount.
    
    Parameters
    ----------
    user_balance : ``UserBalance``
        User balance to work with.
    
    amount : `int`
        Amount to modify the relationship value by.
    """
    user_balance.relationship_value = max(user_balance.relationship_value + amount, 0)
    user_balance.modification_flags |= USER_BALANCE_MODIFICATION_FLAG_RELATIONSHIP_VALUE


def user_balance_set_relationship_value(user_balance, amount):
    """
    Sets the relationship value.
    
    Parameters
    ----------
    user_balance : ``UserBalance``
        User balance to work with.
    
    amount : `int`
        Amount to set the relationship value to.
    """
    user_balance.relationship_value = amount
    user_balance.modification_flags |= USER_BALANCE_MODIFICATION_FLAG_RELATIONSHIP_VALUE


def user_balance_set_streak(user_balance, amount):
    """
    Sets the streak to the given value.
    
    Parameters
    ----------
    user_balance : ``UserBalance``
        User balance to work with.
    
    amount : `int`
        Amount to set to.
    """
    user_balance.streak = amount
    user_balance.modification_flags |= USER_BALANCE_MODIFICATION_FLAG_STREAK


def user_balance_set_daily_can_claim_at(user_balance, date_time):
    """
    Sets the daily can claim at to the given value.
    
    Parameters
    ----------
    user_balance : ``UserBalance``
        User balance to work with.
    
    date_time : `DateTime`
        Amount to set to.
    """
    user_balance.daily_can_claim_at = date_time
    user_balance.modification_flags |= USER_BALANCE_MODIFICATION_FLAG_DAILY_CAN_CLAIM_AT


def user_balance_set_top_gg_voted_at(user_balance, date_time):
    """
    Sets the top gg voted at to the given value.
    
    Parameters
    ----------
    user_balance : ``UserBalance``
        User balance to work with.
    
    date_time : `DateTime`
        Amount to set to.
    """
    user_balance.top_gg_voted_at = date_time
    user_balance.modification_flags |= USER_BALANCE_MODIFICATION_FLAG_TOP_GG_VOTED_AT


def user_balance_increment_count_daily_self(user_balance):
    """
    Increments the daily count self.
    
    Parameters
    ----------
    user_balance : ``UserBalance``
        User balance to work with.
    """
    user_balance.count_daily_self += 1
    user_balance.modification_flags |= USER_BALANCE_MODIFICATION_FLAG_COUNT_DAILY_SELF


def user_balance_increment_count_daily_for_related(user_balance):
    """
    Increments the daily count for related.
    
    Parameters
    ----------
    user_balance : ``UserBalance``
        User balance to work with.
    """
    user_balance.count_daily_for_related += 1
    user_balance.modification_flags |= USER_BALANCE_MODIFICATION_FLAG_COUNT_DAILY_FOR_RELATED


def user_balance_increment_count_daily_by_related(user_balance):
    """
    Increments the daily count by related.
    
    Parameters
    ----------
    user_balance : ``UserBalance``
        User balance to work with.
    """
    user_balance.count_daily_by_related += 1
    user_balance.modification_flags |= USER_BALANCE_MODIFICATION_FLAG_COUNT_DAILY_BY_RELATED


def user_balance_increment_count_top_gg_vote(user_balance):
    """
    Increments the top gg vote count.
    
    Parameters
    ----------
    user_balance : ``UserBalance``
        User balance to work with.
    """
    user_balance.count_top_gg_vote += 1
    user_balance.modification_flags |= USER_BALANCE_MODIFICATION_FLAG_COUNT_TOP_GG_VOTE

    
def user_balance_increment_relationship_slots(user_balance):
    """
    Increments the relationship slots.
    
    Parameters
    ----------
    user_balance : ``UserBalance``
        User balance to work with.
    """
    user_balance.relationship_slots += 1
    user_balance.modification_flags |= USER_BALANCE_MODIFICATION_FLAG_RELATIONSHIP_SLOTS


def user_balance_increment_relationship_divorces(user_balance):
    """
    Increments the relationship divorces.
    
    Parameters
    ----------
    user_balance : ``UserBalance``
        User balance to work with.
    """
    user_balance.relationship_divorces += 1
    user_balance.modification_flags |= USER_BALANCE_MODIFICATION_FLAG_RELATIONSHIP_DIVORCES


def user_balance_decrement_relationship_divorces(user_balance):
    """
    Decrements the relationship divorces.
    
    Parameters
    ----------
    user_balance : ``UserBalance``
        User balance to work with.
    """
    user_balance.relationship_divorces = max(user_balance.relationship_divorces - 1, 0)
    user_balance.modification_flags |= USER_BALANCE_MODIFICATION_FLAG_RELATIONSHIP_DIVORCES


def user_balance_set_daily_reminded(user_balance, value):
    """
    Sets whether the user had their daily reminded.
    
    Parameters
    ----------
    user_balance : ``UserBalance``
        User balance to work with.
    
    value : `bool`
        Value to set.
    """
    user_balance.daily_reminded = value
    user_balance.modification_flags |= USER_BALANCE_MODIFICATION_FLAG_DAILY_REMINDED


def user_balance_collect_modifications(user_balance):
    """
    Collects the modifications done to the user balance.
    
    Parameters
    ----------
    user_balance : ``UserBalance``
        The user stats to collect of.
    
    Returns
    -------
    modifications : `None | dict<str, object>`
    """
    modification_flags = user_balance.modification_flags
    if not modification_flags:
        return None
    
    user_balance.modification_flags = 0
    
    modifications = {}
    
    if modification_flags & USER_BALANCE_MODIFICATION_FLAG_BALANCE:
        modifications['balance'] = user_balance.balance
    
    if modification_flags & USER_BALANCE_MODIFICATION_FLAG_COUNT_DAILY_BY_RELATED:
        modifications['count_daily_by_related'] = user_balance.count_daily_by_related
    
    if modification_flags & USER_BALANCE_MODIFICATION_FLAG_COUNT_DAILY_FOR_RELATED:
        modifications['count_daily_for_related'] = user_balance.count_daily_for_related
    
    if modification_flags & USER_BALANCE_MODIFICATION_FLAG_COUNT_DAILY_SELF:
        modifications['count_daily_self'] = user_balance.count_daily_self
    
    if modification_flags & USER_BALANCE_MODIFICATION_FLAG_COUNT_TOP_GG_VOTE:
        modifications['count_top_gg_vote'] = user_balance.count_top_gg_vote
    
    if modification_flags & USER_BALANCE_MODIFICATION_FLAG_DAILY_CAN_CLAIM_AT:
        modifications['daily_can_claim_at'] = user_balance.daily_can_claim_at
    
    if modification_flags & USER_BALANCE_MODIFICATION_FLAG_DAILY_REMINDED:
        modifications['daily_reminded'] = user_balance.daily_reminded
    
    if modification_flags & USER_BALANCE_MODIFICATION_FLAG_RELATIONSHIP_DIVORCES:
        modifications['relationship_divorces'] = user_balance.relationship_divorces
    
    if modification_flags & USER_BALANCE_MODIFICATION_FLAG_RELATIONSHIP_SLOTS:
        modifications['relationship_slots'] = user_balance.relationship_slots
    
    if modification_flags & USER_BALANCE_MODIFICATION_FLAG_RELATIONSHIP_VALUE:
        modifications['relationship_value'] = user_balance.relationship_value
    
    if modification_flags & USER_BALANCE_MODIFICATION_FLAG_STREAK:
        modifications['streak'] = user_balance.streak
    
    if modification_flags & USER_BALANCE_MODIFICATION_FLAG_TOP_GG_VOTED_AT:
        modifications['top_gg_voted_at'] = user_balance.top_gg_voted_at
    
    if modification_flags & USER_BALANCE_MODIFICATION_FLAG_ALLOCATIONS:
        modifications['user_id'] = user_balance.user_id
    
    return modifications
