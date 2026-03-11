__all__ = ()

from dateutil.relativedelta import relativedelta as RelativeDelta

from ..item_core import get_item_group_nullable

from ..quest_core import (
    AMOUNT_TYPE_VALUE, AMOUNT_TYPE_WEIGHT, LINKED_QUEST_COMPLETION_STATE_COMPLETED, QUEST_REQUIREMENT_TYPE_DURATION,
    QUEST_REQUIREMENT_TYPE_EXPIRATION, QUEST_REQUIREMENT_TYPE_ITEM_CATEGORY, QUEST_REQUIREMENT_TYPE_ITEM_EXACT,
    QUEST_REQUIREMENT_TYPE_ITEM_GROUP, QUEST_REWARD_TYPE_BALANCE, QUEST_REWARD_TYPE_CREDIBILITY,
    QUEST_REWARD_TYPE_ITEM_EXACT, calculate_received_reward_credibility
)


def get_quest_with_template_id(quest_batch, quest_template_id):
    """
    Gets the quest from the batch with the given template identifier.
    
    Parameters
    ----------
    quest_batch : ``QuestBatch``
        Quest batch to get the quest from.
    
    quest_template_id : `int`
        The quest template's identifier.
    
    Returns
    -------
    quest : ``None | Quest``
    """
    for quest in quest_batch.quests:
        if quest.template_id == quest_template_id:
            return quest


def get_linked_quest_with_entry_id(linked_quest_listing, entry_id):
    """
    Gets the quest from the batch with the given template identifier.
    
    Parameters
    ----------
    linked_quest_listing : ``None | list<LinkedQuest>``
        Linked quests.
    
    entry_id : `int`
        Linked quest entry identifier.
    
    Returns
    -------
    quest : ``None | LinkedQuest``
    """
    if (linked_quest_listing is not None):
        for linked_quest in linked_quest_listing:
            if linked_quest.entry_id == entry_id:
                return linked_quest


def get_submit_amount(item, amount_type, amount_to_be_used, current_amount_count):
    """
    Gets how much amount is submittable in required format and in count format.
    
    Parameters
    ----------
    item : ``Item``
        The item submitted.
    
    amount_type : `int`
        In what format the item is required.
    
    amount_to_be_used : `int`
        Up to how much amount can be used.
    
    current_amount_count : `int`
        The amount of `item`-s owned and possible to be submitted.
    
    Returns
    -------
    amount_used_and_amount_used_count : `(int, int)`
        The used up amount in the required format and  the used up amount in count format.
    """
    if amount_type == AMOUNT_TYPE_WEIGHT or amount_type == AMOUNT_TYPE_VALUE:
        if amount_type == AMOUNT_TYPE_WEIGHT:
            multiplier = item.weight
        else:
            multiplier = item.value
        
        amount_used = min(amount_to_be_used, current_amount_count * multiplier)
        amount_used_count, modulus = divmod(amount_used, multiplier)
        if modulus:
            amount_used += multiplier - modulus
            amount_used_count += 1
    
    else:
        # AMOUNT_TYPE_COUNT and else
        amount_used = amount_used_count = min(amount_to_be_used, current_amount_count)
    
    return amount_used, amount_used_count


def get_linked_quest_for_deduplication(linked_quest_listing, guild_id, quest_batch_id, quest_template_id):
    """
    Gets the linked quest for deduplication. If a linked quest with the given attributes exists, returns it.
    
    Parameters
    ----------
    linked_quest_listing : ``None | list<LinkedQuest>``
        Linked quests.
    
    guild_id : `int`
        The guild's identifier is quest is from.
    
    quest_batch_id : `int`
        The identifier of the batch the quest is from.
    
    quest_template_id : `int`
        The quest's template's identifier.
    
    Returns
    -------
    quest : ``None | LinkedQuest``
    """
    if (linked_quest_listing is not None):
        for linked_quest in linked_quest_listing:
            if (
                linked_quest.guild_id == guild_id and
                linked_quest.batch_id == quest_batch_id and
                linked_quest.template_id == quest_template_id
            ):
                return linked_quest


def get_quest_submission_requirements_normalised(quest):
    """
    Gets quest submission requirements.
    
    Parameters
    ----------
    quest : ``Quest``
        Quest to work with.
    
    Returns
    -------
    submission_requirements_normalised : `None | list<(int, int, int, int, int)>`
    """
    requirements = quest.requirements
    if requirements is None:
        return
    
    normalised = None
    
    for requirement in requirements:
        requirement_type = requirement.TYPE
        if requirement_type == QUEST_REQUIREMENT_TYPE_ITEM_EXACT:
            required_identifier = requirement.item_id
            
        elif requirement_type == QUEST_REQUIREMENT_TYPE_ITEM_GROUP:
            required_identifier = requirement.item_group_id
            
        elif requirement_type == QUEST_REQUIREMENT_TYPE_ITEM_CATEGORY:
            required_identifier = requirement.item_flags
            
        else:
            continue
        
        amount_type = requirement.amount_type
        amount_required = requirement.amount_required
        
        if normalised is None:
            normalised = []
        
        normalised.append((
            requirement_type,
            required_identifier,
            amount_type,
            amount_required,
            -1,
        ))
    
    return normalised


def get_linked_quest_submission_requirements_normalised(linked_quest):
    """
    Gets quest submission requirements.
    
    Parameters
    ----------
    linked_quest : ``LinkedQuest``
        Linked quest to work with.
    
    Returns
    -------
    submission_requirements_normalised : `None | list<(int, int, int, int, int)>`
    """
    requirements = linked_quest.requirements
    if requirements is None:
        return
    
    normalised = None
    completed = linked_quest.completion_state == LINKED_QUEST_COMPLETION_STATE_COMPLETED
    
    for requirement in requirements:
        requirement_type = requirement.TYPE
        if requirement_type == QUEST_REQUIREMENT_TYPE_ITEM_EXACT:
            required_identifier = requirement.item_id
            
        elif requirement_type == QUEST_REQUIREMENT_TYPE_ITEM_GROUP:
            required_identifier = requirement.item_group_id
            
        elif requirement_type == QUEST_REQUIREMENT_TYPE_ITEM_CATEGORY:
            required_identifier = requirement.item_flags
            
        else:
            continue
        
        amount_type = requirement.amount_type
        amount_required = requirement.amount_required
        
        if completed:
            amount_submitted = -1
        else:
            amount_submitted = requirement.amount_submitted
        
        if normalised is None:
            normalised = []
        
        normalised.append((
            requirement_type,
            required_identifier,
            amount_type,
            amount_required,
            amount_submitted,
        ))
    
    return normalised


def get_quest_rewards_normalised(quest, quest_level, user_level):
    """
    Gets quest rewards.
    
    Parameters
    ----------
    quest : ``Quest``
        Quest to work with.
    
    quest_level : `int`
        The quest's level.
    
    user_level : `int`
        The user's level.
    
    Returns
    -------
    rewards_normalised : `None | list<(int, int, int)>`
    """
    rewards = quest.rewards
    if rewards is None:
        return
    
    normalised = None
    
    for reward in rewards:
        reward_type = reward.TYPE
        if reward_type == QUEST_REWARD_TYPE_BALANCE:
            reward_identifier = 0
            amount_given = reward.balance
            
        elif reward_type == QUEST_REWARD_TYPE_CREDIBILITY:
            reward_identifier = 0
            amount_given = calculate_received_reward_credibility(reward.credibility, quest_level, user_level)
            
        elif reward_type == QUEST_REWARD_TYPE_ITEM_EXACT:
            reward_identifier = reward.item_id
            amount_given = reward.amount_given
            
        else:
            continue
        
        if normalised is None:
            normalised = []
        
        normalised.append((
            reward_type,
            reward_identifier,
            amount_given,
        ))
    
    return normalised
        

def get_linked_quest_rewards_normalised(linked_quest, quest_level, user_level):
    """
    Gets quest rewards.
    
    Parameters
    ----------
    linked_quest : ``LinkedQuest``
        Linked quest to work with.
    
    quest_level : `int`
        The quest's level.
    
    user_level : `int`
        The user's level.
    
    Returns
    -------
    rewards_normalised : `None | list<(int, int, int)>`
    """
    rewards = linked_quest.rewards
    if rewards is None:
        return
    
    normalised = None
    
    for reward in rewards:
        reward_type = reward.TYPE
        if reward_type == QUEST_REWARD_TYPE_BALANCE:
            reward_identifier = 0
            amount_given = reward.balance
            
        elif reward_type == QUEST_REWARD_TYPE_CREDIBILITY:
            reward_identifier = 0
            amount_given = calculate_received_reward_credibility(reward.credibility, quest_level, user_level)
            
        elif reward_type == QUEST_REWARD_TYPE_ITEM_EXACT:
            reward_identifier = reward.item_id
            amount_given = reward.amount_given
            
        else:
            continue
        
        if normalised is None:
            normalised = []
        
        normalised.append((
            reward_type,
            reward_identifier,
            amount_given,
        ))
    
    return normalised


def get_quest_expiration(quest):
    """
    Gets a quest's duration.
    
    Parameters
    ----------
    quest : ``Quest``
        Quest to work with.
    
    Returns
    -------
    expiration : ``None | Datetime``
    """
    requirements = quest.requirements
    if (requirements is not None):
        for requirement in requirements:
            if requirement.TYPE == QUEST_REQUIREMENT_TYPE_EXPIRATION:
                return requirement.expiration


def get_linked_quest_expiration(linked_quest):
    """
    Gets when the linked expires.
    
    Parameters
    ----------
    linked_quest : ``LinkedQuest``
        Linked quest to work with.
    
    Returns
    -------
    expiration : ``None | Datetime``
    """
    requirements = linked_quest.requirements
    if (requirements is not None):
        for requirement in requirements:
            if requirement.TYPE == QUEST_REQUIREMENT_TYPE_EXPIRATION:
                return requirement.expiration


def get_quest_duration_delta(quest):
    """
    Gets a quest's duration.
    
    Parameters
    ----------
    quest : ``Quest``
        Quest to work with.
    
    Returns
    -------
    duration_delta : ``None | RelativeDelta``
    """
    requirements = quest.requirements
    if (requirements is not None):
        for requirement in requirements:
            if requirement.TYPE == QUEST_REQUIREMENT_TYPE_DURATION:
                return RelativeDelta(seconds = requirement.duration)


def get_linked_quest_duration_delta(linked_quest):
    """
    Gets a quest's duration.
    
    Parameters
    ----------
    linked_quest : ``LinkedQuest``
        Linked quest to work with.
    
    Returns
    -------
    duration_delta : ``None | RelativeDelta``
    """
    requirements = linked_quest.requirements
    if (requirements is not None):
        for requirement in requirements:
            if requirement.TYPE == QUEST_REQUIREMENT_TYPE_DURATION:
                return RelativeDelta(seconds = requirement.duration)


def get_linked_quest_submission_requirement_at_index(linked_quest, requirement_index):
    """
    Gets a linked quest's submission requirement at the given index.
    
    Parameters
    ----------
    linked_quest : ``LinkedQuest``
        Linked quest to work with.
    
    requirement_index : `int`
        The index of the submission requirement.
    
    Returns
    -------
    requirement : ``None | QuestRequirementSerialisableBase``
    """
    requirements = linked_quest.requirements
    if (requirements is not None):
        index = 0
        for requirement in requirements:
            if requirement.TYPE not in (
                QUEST_REQUIREMENT_TYPE_ITEM_EXACT,
                QUEST_REQUIREMENT_TYPE_ITEM_GROUP,
                QUEST_REQUIREMENT_TYPE_ITEM_CATEGORY,
            ):
                continue
            
            if index == requirement_index:
                return requirement
            
            index += 1
            continue


def _iter_submission_requirement_item_exact_item_entries(inventory, item_id):
    """
    Iterates over the item entries of the inventory that match the given item identifier.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    inventory : ``Inventory``
        Inventory to filter from.
    
    item_id : `int`
        Item identifier to match.
    
    Yields
    ------
    item_entry : ``ItemEntry``
    """
    item_entry = inventory.get_item_entry_by_id(item_id)
    if (item_entry is None):
        return
    
    yield item_entry


def _iter_submission_requirement_item_exact_item_group(inventory, item_group_id):
    """
    Iterates over the item entries of the inventory that match the given item group identifier.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    inventory : ``Inventory``
        Inventory to filter from.
    
    item_group_id : `int`
        Item group identifier to match.
    
    Yields
    ------
    item_entry : ``ItemEntry``
    """
    item_group = get_item_group_nullable(item_group_id)
    if (item_group is None):
        return
    
    item_ids = item_group.item_ids
    if (item_ids is None):
        return
    
    for item_entry in inventory.iter_item_entries():
        if (item_entry.item.id not in item_ids):
            continue
        
        yield item_entry
        continue
    

def _iter_submission_requirement_item_exact_item_category(inventory, item_flags):
    """
    Iterates over the item entries of the inventory that match the given item flags.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    inventory : ``Inventory``
        Inventory to filter from.
    
    item_flags : `int`
        Item flags to match.
    
    Yields
    ------
    item_entry : ``ItemEntry``
    """
    for item_entry in inventory.iter_item_entries():
        if (item_entry.item.flags & item_flags != item_flags):
            continue
        
        yield item_entry
        continue


def iter_submission_requirement_item_entries_of_requirement(inventory, requirement):
    """
    Iterates over item entries of the inventory that match the given requirement.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    inventory : ``Inventory``
        Inventory to filter from.
    
    requirement : ``QuestRequirementSerialisableBase``
        Requirement to match items for.
    
    Yields
    ------
    item_entry : ``ItemEntry``
    """
    requirement_type = requirement.TYPE
    if requirement_type == QUEST_REQUIREMENT_TYPE_ITEM_EXACT:
        required_identifier = requirement.item_id
        iterator_function = _iter_submission_requirement_item_exact_item_entries
    
    elif requirement_type == QUEST_REQUIREMENT_TYPE_ITEM_GROUP:
        required_identifier = requirement.item_group_id
        iterator_function = _iter_submission_requirement_item_exact_item_group
    
    elif requirement_type == QUEST_REQUIREMENT_TYPE_ITEM_CATEGORY:
        required_identifier = requirement.item_flags
        iterator_function = _iter_submission_requirement_item_exact_item_category
    
    else:
        return
    
    yield from iterator_function(inventory, required_identifier)


def iter_submission_requirement_item_entries_of_normalised(inventory, submission_requirement_normalised):
    """
    Iterates over item entries of the inventory that match the given normalised requirement.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    inventory : ``Inventory``
        Inventory to filter from.
    
    submission_requirement_normalised : `(int, int, int, int, int)`
        Normalised requirement to match items for.
    
    Yields
    ------
    item_entry : ``ItemEntry``
    """
    requirement_type = submission_requirement_normalised[0]
    if requirement_type == QUEST_REQUIREMENT_TYPE_ITEM_EXACT:
        iterator_function = _iter_submission_requirement_item_exact_item_entries
    
    elif requirement_type == QUEST_REQUIREMENT_TYPE_ITEM_GROUP:
        iterator_function = _iter_submission_requirement_item_exact_item_group
    
    elif requirement_type == QUEST_REQUIREMENT_TYPE_ITEM_CATEGORY:
        iterator_function = _iter_submission_requirement_item_exact_item_category
    
    else:
        return
    
    yield from iterator_function(inventory, submission_requirement_normalised[1])
