__all__ = ()

from ..quest_core import AMOUNT_TYPE_VALUE, AMOUNT_TYPE_WEIGHT


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
        The identifier of the batch teh quest is from.
    
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
