__all__ = ()

from dateutil.relativedelta import relativedelta as RelativeDelta

from ..item_core import get_item, get_item_group_nullable, get_item_nullable

from ..quest_core import (
    AMOUNT_TYPE_VALUE, AMOUNT_TYPE_WEIGHT, LINKED_QUEST_COMPLETION_STATE_COMPLETED, QUEST_REQUIREMENT_TYPE_DURATION,
    QUEST_REQUIREMENT_TYPE_EXPIRATION, QUEST_REQUIREMENT_TYPE_ITEM_CATEGORY, QUEST_REQUIREMENT_TYPE_ITEM_EXACT,
    QUEST_REQUIREMENT_TYPE_ITEM_GROUP, QUEST_REWARD_TYPE_BALANCE, QUEST_REWARD_TYPE_CREDIBILITY,
    QUEST_REWARD_TYPE_ITEM_EXACT, calculate_received_reward_credibility, get_guild_adventurer_rank_info
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
        
        multiplier = max(multiplier, 1)
        
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


def get_quest_in_possession_count(quest, inventory):
    """
    Returns how much times the user owns the items to complete the quests for.
    
    Parameters
    ----------
    quest : ``Quest``
        Quest to work with.
    
    inventory : ``Inventory``
        The user's inventory.
    
    Returns
    -------
    possession_count : `int`
    """
    possession_count = 0
    
    requirements = quest.requirements
    if (requirements is not None):
        for requirement in requirements:
            requirement_type = requirement.TYPE
            
            # If we require category or group, disable
            if (
                (requirement_type == QUEST_REQUIREMENT_TYPE_ITEM_GROUP) or
                (requirement_type == QUEST_REQUIREMENT_TYPE_ITEM_CATEGORY)
            ):
                possession_count = 0
                break
            
            # If we require an  exact item, try to process it
            if requirement_type == QUEST_REQUIREMENT_TYPE_ITEM_EXACT:
                item = get_item_nullable(requirement.item_id)
                if item is None:
                    continue
                
                amount_type = requirement.amount_type
                if (amount_type == AMOUNT_TYPE_WEIGHT) or (amount_type == AMOUNT_TYPE_VALUE):
                    if amount_type == AMOUNT_TYPE_WEIGHT:
                        multiplier = item.weight
                    else:
                        multiplier = item.value
                    
                    multiplier = max(multiplier, 1)
                
                else:
                    # AMOUNT_TYPE_COUNT and else
                    multiplier = 1
                
                # DO not calculate it by completion to allow the user submitting it multiple times.
                amount_owned = inventory.get_item_amount(item) * multiplier
                amount_required = requirement.amount_required
                
                completable_count = amount_owned // amount_required
                if (not possession_count) or (completable_count < possession_count):
                    possession_count = completable_count
                continue
            
            # Rest can be ignored for now
            continue
    
    return possession_count


def get_allowed_completion_count(linked_quest, quest_template, possession_count):
    """
    Gets how much a quest is allowed to be completed, up to possession count.
    
    Parameters
    ----------
    linked_quest : : ``None | LinkedQuest``
        The linked quest if the user already completed this quest before.
    
    quest_template : ``QuestTemplate``
        The quest's template.
    
    possession_count : `int`
        How much times the required items are possessed by the user.
    
    Returns
    -------
    allowed_count : `int`
    """
    repeat_count = quest_template.repeat_count
    
    if not repeat_count:
        allowed_count = possession_count
    
    else:
        if (linked_quest is not None):
            repeat_count = max(0, repeat_count - linked_quest.completion_count)
        
        allowed_count = min(repeat_count, possession_count)
    
    return allowed_count


def try_submit_item(requirement, inventory, item_entry, submissions_normalised):
    """
    Tries to submit the given item.
    
    Parameters
    ----------
    requirement : ``QuestRequirementSerialisableItemExact | QuestRequirementSerialisableItemGroup | QuestRequirementSerialisable``
        Requirement to submit to.
    
    inventory : ``Inventory``
        The user's inventory.
    
    item_entry : ``ItemEntry``
        Specific item entry to submit from.
    
    submissions_normalised : ``None | list<(Item, int, int, int, int)>``
        Already done submissions.
    
    Returns
    -------
    submissions_normalised : ``None | list<(Item, int, int, int, int)>``
    """
    amount_required = requirement.amount_required
    amount_submitted = requirement.amount_submitted
    
    # Do not submit 0 if all is already submitted
    if (amount_submitted >= amount_required):
        return submissions_normalised
    
    current_amount_count = item_entry.amount
    item = item_entry.item
    
    amount_type = requirement.amount_type
    amount_to_be_used = amount_required - amount_submitted
    amount_used, amount_used_count = get_submit_amount(
        item, amount_type, amount_to_be_used, current_amount_count
    )
    requirement.amount_submitted = amount_submitted + amount_used
    inventory.modify_item_amount(item, -amount_used_count)
    
    if (submissions_normalised is None):
        submissions_normalised = []
    
    submissions_normalised.append((
        item, amount_type, amount_required, amount_submitted, amount_used
    ))
    return submissions_normalised


def do_submit_complete_item(requirement, inventory, item_entry, submissions_normalised, submission_count):
    """
    Submits the given item until completion count completion.
    Ignores already submitted item count and the user having les items as well.
    
    Parameters
    ----------
    requirement : ``QuestRequirementSerialisableItemExact | QuestRequirementSerialisableItemGroup | QuestRequirementSerialisable``
        Requirement to submit to.
    
    inventory : ``Inventory``
        The user's inventory.
    
    item_entry : ``ItemEntry``
        Specific item entry to submit from.
    
    submissions_normalised : ``None | list<(Item, int, int, int, int)>``
        Already done submissions.
    
    submission_count : `int`
        How much times to submit the requirement.
    
    Returns
    -------
    submissions_normalised : ``list<(Item, int, int, int, int)>``
    """
    amount_required = requirement.amount_required
    
    current_amount_count = item_entry.amount
    item = item_entry.item
    amount_required_total = amount_required * submission_count
    
    amount_type = requirement.amount_type
    amount_used, amount_used_count = get_submit_amount(
        item, amount_type, amount_required_total, current_amount_count
    )
    inventory.modify_item_amount(item, -amount_used_count)
    
    # If you submit extra items, keep the extra in `.amount_submitted`.
    # If you submitted less for whatever reason, do not point out that you indeed submitted less.
    requirement.amount_submitted = max(amount_required, amount_required + amount_used - amount_required_total)
    
    if (submissions_normalised is None):
        submissions_normalised = []
    
    submissions_normalised.append((
        item, amount_type, amount_required_total, 0, amount_used
    ))
    return submissions_normalised


def do_reward_user(
    linked_quest, inventory, user_stats, user_balance, guild_stats, quest_level, user_level, reward_count
):
    """
    Rewards the user.
    
    Parameters
    ----------
    linked_quest : ``LinkedQuest``
        Linked quest to distribute the awards from..
    
    inventory : ``Inventory``
        The user's inventory.
    
    user_stats : ``UserStats``
        The user's stats.
    
    user_balance : ``UserBalance``
        The user's balance.
    
    guild_stats : ``GuildStats``
        The guild's stats.
    
    quest_level : `int`
        The quest's level.
    
    user_level : `int`
        The user's level.
    
    reward_count : `int`
        How much times to reward the user.
    
    Returns
    -------
    rewards_normalised : ``None | list<(int, int, int)>``
    """
    rewards_normalised = None
    
    rewards = linked_quest.rewards
    if (rewards is not None):
        for reward in rewards:
            reward_type = reward.TYPE
            if reward_type == QUEST_REWARD_TYPE_BALANCE:
                balance_given = reward.balance * reward_count
                
                user_balance.modify_balance_by(balance_given)
                
                if (rewards_normalised is None):
                    rewards_normalised = []
                
                rewards_normalised.append((QUEST_REWARD_TYPE_BALANCE, 0, balance_given))
            
            elif reward_type == QUEST_REWARD_TYPE_CREDIBILITY:
                credibility_given = reward.credibility * reward_count
                
                user_reward_credibility = calculate_received_reward_credibility(
                    credibility_given, quest_level, user_level
                )
                user_stats.modify_credibility_by(user_reward_credibility)
                
                guild_adventurer_rank_info = get_guild_adventurer_rank_info(guild_stats.credibility)
                guild_reward_credibility = calculate_received_reward_credibility(
                    credibility_given, quest_level, guild_adventurer_rank_info.level
                )
                guild_stats.set('credibility', guild_stats.credibility + guild_reward_credibility)
                
                if (rewards_normalised is None):
                    rewards_normalised = []
                
                rewards_normalised.append((QUEST_REWARD_TYPE_CREDIBILITY, 0, user_reward_credibility))
            
            elif reward_type == QUEST_REWARD_TYPE_ITEM_EXACT:
                amount_given = reward.amount_given * reward_count
                item_id = reward.item_id
                inventory.modify_item_amount(get_item(item_id), amount_given)
                
                if (rewards_normalised is None):
                    rewards_normalised = []
                
                rewards_normalised.append((QUEST_REWARD_TYPE_ITEM_EXACT, item_id, amount_given))
            
            else:
                # No other cases
                pass
    
    return rewards_normalised
