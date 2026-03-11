__all__ = ()

from datetime import datetime as DateTime, timezone as TimeZone

from ...bots import FEATURE_CLIENTS

from ..adventure_core import get_active_adventure
from ..guild_stats import get_guild_stats
from ..inventory_core import get_inventory, save_inventory
from ..item_core import get_item
from ..quest_core import (
    LINKED_QUEST_COMPLETION_STATE_ACTIVE, LINKED_QUEST_COMPLETION_STATE_COMPLETED, LinkedQuest,
    QUEST_REWARD_TYPE_BALANCE, QUEST_REWARD_TYPE_CREDIBILITY, QUEST_REWARD_TYPE_ITEM_EXACT, add_linked_quest,
    calculate_received_reward_credibility, delete_linked_quest, get_current_batch_id, get_guild_adventurer_rank_info,
    get_linked_quest_abandon_credibility_penalty, get_linked_quest_completion_ratio, get_linked_quest_listing,
    get_quest_template, get_user_adventurer_rank_info, instantiate_quest, reset_linked_quest, update_linked_quest
)
from ..user_balance import get_user_balance, save_user_balance
from ..user_stats_core import get_user_stats, save_user_stats

from .component_building import (
    build_linked_quest_abandon_confirmation_form, build_linked_quest_abandon_success_components,
    build_linked_quest_details_components, build_linked_quest_item_components,
    build_linked_quest_submit_select_item_components, build_linked_quest_submit_select_requirement_components,
    build_linked_quest_submit_success, build_linked_quest_submit_success_completed_components,
    build_linked_quests_listing_components, build_quest_accept_success_components, build_quest_board_item_components,
    build_quest_board_quest_listing_components, build_quest_details_components
)
from .constants import (
    BROKEN_QUEST_DESCRIPTION, LINKED_QUEST_BACK_DIRECT_LOCATION_QUEST,
    LINKED_QUEST_BACK_DIRECT_LOCATION_SELECT_ITEM_NESTED, LINKED_QUEST_BACK_DIRECT_LOCATION_SELECT_ITEM_TOP,
    LINKED_QUEST_BACK_DIRECT_LOCATION_SELECT_REQUIREMENT
)
from .custom_ids import (
    CUSTOM_ID_LINKED_QUEST_ABANDON_PATTERN, CUSTOM_ID_LINKED_QUEST_INFO_ITEM_DISABLED,
    CUSTOM_ID_LINKED_QUEST_INFO_ITEM_PATTERN, CUSTOM_ID_LINKED_QUEST_ITEM_INFO_PATTERN,
    CUSTOM_ID_LINKED_QUEST_PAGE_INDEX_DECREMENT_DISABLED, CUSTOM_ID_LINKED_QUEST_PAGE_INDEX_INCREMENT_DISABLED,
    CUSTOM_ID_LINKED_QUEST_PAGE_INDEX_NAVIGATE_PATTERN, CUSTOM_ID_LINKED_QUEST_SUBMIT_AUTO_PATTERN,
    CUSTOM_ID_LINKED_QUEST_SUBMIT_DISABLED, CUSTOM_ID_LINKED_QUEST_SUBMIT_EXECUTE_ITEM_NESTED_PATTERN,
    CUSTOM_ID_LINKED_QUEST_SUBMIT_EXECUTE_ITEM_TOP_PATTERN, CUSTOM_ID_LINKED_QUEST_SUBMIT_EXECUTE_REQUIREMENT_PATTERN,
    CUSTOM_ID_LINKED_QUEST_SUBMIT_INFO_ITEM_NESTED_PATTERN, CUSTOM_ID_LINKED_QUEST_SUBMIT_INFO_ITEM_TOP_PATTERN,
    CUSTOM_ID_LINKED_QUEST_SUBMIT_INFO_REQUIREMENT_PATTERN, CUSTOM_ID_LINKED_QUEST_SUBMIT_SELECT_ITEM_NESTED_PATTERN,
    CUSTOM_ID_LINKED_QUEST_SUBMIT_SELECT_ITEM_PAGE_INDEX_DECREMENT_DISABLED,
    CUSTOM_ID_LINKED_QUEST_SUBMIT_SELECT_ITEM_PAGE_INDEX_INCREMENT_DISABLED,
    CUSTOM_ID_LINKED_QUEST_SUBMIT_SELECT_ITEM_TOP_PATTERN,
    CUSTOM_ID_LINKED_QUEST_SUBMIT_SELECT_REQUIREMENT_PAGE_INDEX_DECREMENT_DISABLED,
    CUSTOM_ID_LINKED_QUEST_SUBMIT_SELECT_REQUIREMENT_PAGE_INDEX_INCREMENT_DISABLED,
    CUSTOM_ID_LINKED_QUEST_SUBMIT_SELECT_REQUIREMENT_PATTERN, CUSTOM_ID_QUEST_ACCEPT_DISABLED,
    CUSTOM_ID_QUEST_ACCEPT_PATTERN, CUSTOM_ID_QUEST_BOARD_ITEM_DISABLED, CUSTOM_ID_QUEST_BOARD_ITEM_PATTERN,
    CUSTOM_ID_QUEST_BOARD_PAGE_INDEX_DECREMENT_DISABLED, CUSTOM_ID_QUEST_BOARD_PAGE_INDEX_INCREMENT_DISABLED,
    CUSTOM_ID_QUEST_BOARD_PAGE_INDEX_NAVIGATE_PATTERN, CUSTOM_ID_QUEST_BOARD_QUEST_DETAILS_PATTERN
)
from .helpers import (
    get_linked_quest_expiration, get_linked_quest_for_deduplication, get_linked_quest_submission_requirement_at_index,
    get_linked_quest_with_entry_id, get_quest_with_template_id, get_submit_amount,
    iter_submission_requirement_item_entries_of_requirement
)


@FEATURE_CLIENTS.interactions(
    custom_id = [
        CUSTOM_ID_QUEST_BOARD_PAGE_INDEX_DECREMENT_DISABLED,
        CUSTOM_ID_QUEST_BOARD_PAGE_INDEX_INCREMENT_DISABLED,
        CUSTOM_ID_QUEST_ACCEPT_DISABLED,
        CUSTOM_ID_LINKED_QUEST_PAGE_INDEX_DECREMENT_DISABLED,
        CUSTOM_ID_LINKED_QUEST_PAGE_INDEX_INCREMENT_DISABLED,
        CUSTOM_ID_LINKED_QUEST_SUBMIT_DISABLED,
        CUSTOM_ID_QUEST_BOARD_ITEM_DISABLED,
        CUSTOM_ID_LINKED_QUEST_INFO_ITEM_DISABLED,
        CUSTOM_ID_LINKED_QUEST_SUBMIT_SELECT_REQUIREMENT_PAGE_INDEX_DECREMENT_DISABLED,
        CUSTOM_ID_LINKED_QUEST_SUBMIT_SELECT_REQUIREMENT_PAGE_INDEX_INCREMENT_DISABLED,
        CUSTOM_ID_LINKED_QUEST_SUBMIT_SELECT_ITEM_PAGE_INDEX_DECREMENT_DISABLED,
        CUSTOM_ID_LINKED_QUEST_SUBMIT_SELECT_ITEM_PAGE_INDEX_INCREMENT_DISABLED,
    ],
)
async def quest_action_disabled():
    """
    Dummy handler for component interactions that supposed be disabled.
    
    This function is a coroutine.
    """
    pass


@FEATURE_CLIENTS.interactions(custom_id = CUSTOM_ID_QUEST_BOARD_QUEST_DETAILS_PATTERN)
async def quest_board_quest_details(client, interaction_event, user_id, guild_id, page_index, quest_template_id):
    """
    Handles a quest board quest details component interaction.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the interaction.
    
    interaction_event : ``InteractionEvent``
        The received interaction event.
    
    user_id : `str`
        The invoking user's identifier as a string representing a hexadecimal integer.
    
    guild_id : `str`
        The guild's identifier from where the quest is from as a string representing a hexadecimal integer.
    
    page_index : `str`
        The quest board's current page's index as a string representing a hexadecimal integer.
    
    quest_template_id : `str`
        The quest's template identifier as a string representing a hexadecimal integer.
    """
    try:
        user_id = int(user_id, 16)
        guild_id = int(guild_id, 16)
        page_index = int(page_index, 16)
        quest_template_id = int(quest_template_id, 16)
    except ValueError:
        return
    
    if user_id != interaction_event.user_id:
        return
    
    await client.interaction_component_acknowledge(
        interaction_event,
        False,
    )
    
    while True:
        guild_stats = await get_guild_stats(guild_id)
        quest_batch = guild_stats.get_quest_batch()
        
        quest = get_quest_with_template_id(quest_batch, quest_template_id)
        
        if (quest is None):
            error_message = 'This quest is no longer available.'
            break
        
        user_stats = await get_user_stats(user_id)
        
        # Check whether the user already has a quest like this. If yes then redirect them to it.
        linked_quest_listing = await get_linked_quest_listing(user_id)
        linked_quest = get_linked_quest_for_deduplication(
            linked_quest_listing, guild_id, quest_batch.id, quest_template_id
        )
        if (linked_quest is not None) and (linked_quest.completion_state == LINKED_QUEST_COMPLETION_STATE_ACTIVE):
            components = build_linked_quest_details_components(linked_quest, user_stats, 0)
        else:
            components = build_quest_details_components(
                user_id, guild_id, interaction_event.guild_id, page_index, quest, linked_quest, user_stats
            )
        
        await client.interaction_response_message_edit(
            interaction_event,
            components = components,
        )
        return
    
    await client.interaction_followup_message_create(
        interaction_event,
        content = error_message,
        show_for_invoking_user_only = True,
    )


@FEATURE_CLIENTS.interactions(custom_id = CUSTOM_ID_QUEST_BOARD_PAGE_INDEX_NAVIGATE_PATTERN)
async def quest_board_quest_listing_page_index_navigate(client, interaction_event, user_id, page_index):
    """
    Handles a quest board page index navigation component interaction.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the interaction.
    
    interaction_event : ``InteractionEvent``
        The received interaction event.
    
    user_id : `str`
        The invoking user's identifier as a string representing a hexadecimal integer.
    
    page_index : `str`
        The page's identifier as a string representing a hexadecimal integer.
    """
    try:
        user_id = int(user_id, 16)
        page_index = int(page_index, 16)
    except ValueError:
        return
    
    if user_id != interaction_event.user_id:
        return
    
    await client.interaction_component_acknowledge(
        interaction_event,
        False,
    )
    
    while True:
        guild = interaction_event.guild
        if guild is None:
            error_message = 'Only guilds have quest board.'
            break
        
        guild_stats = await get_guild_stats(guild.id)
        user_stats = await get_user_stats(user_id)
        linked_quest_listing = await get_linked_quest_listing(user_id)
        
        await client.interaction_response_message_edit(
            interaction_event,
            components = build_quest_board_quest_listing_components(
                guild, guild_stats, user_stats, linked_quest_listing, page_index
            ),
        )
        return
    
    await client.interaction_followup_message_create(
        interaction_event,
        content = error_message,
        show_for_invoking_user_only = True,
    )


@FEATURE_CLIENTS.interactions(custom_id = CUSTOM_ID_QUEST_ACCEPT_PATTERN)
async def quest_accept(client, interaction_event, user_id, guild_id, page_index, quest_template_id):
    """
    Handles a quest accept component interaction.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the interaction.
    
    interaction_event : ``InteractionEvent``
        The received interaction event.
    
    user_id : `str`
        The invoking user's identifier as a string representing a hexadecimal integer.
    
    guild_id : `int`
        The guild's identifier where the quest belongs to as a string representing a hexadecimal integer.
    
    page_index : `int`
        The current page's index in hexadecimal number.
    
    quest_template_id : `str`
        The quest's template identifier as a string representing a hexadecimal integer.
    """
    try:
        user_id = int(user_id, 16)
        guild_id = int(guild_id, 16)
        page_index = int(page_index, 16)
        quest_template_id = int(quest_template_id, 16)
    except ValueError:
        return
    
    if user_id != interaction_event.user_id:
        return
    
    await client.interaction_component_acknowledge(
        interaction_event,
        False,
    )
    
    while True:
        adventure = await get_active_adventure(user_id)
        if (adventure is not None):
            error_message = 'You cannot accept quests while adventuring.'
            break
        
        # Get the quest from the board.
        guild_stats = await get_guild_stats(guild_id)
        quest_batch = guild_stats.get_quest_batch()
        
        quest = get_quest_with_template_id(quest_batch, quest_template_id)
        
        # Check whether there is such a quest.
        if (quest is None):
            error_message = 'This quest is no longer available.'
            break
        
        # Check whether the user already has a quest like this.
        linked_quest_listing = await get_linked_quest_listing(user_id)
        linked_quest = get_linked_quest_for_deduplication(
            linked_quest_listing, guild_id, quest_batch.id, quest_template_id
        )
        if (linked_quest is not None) and (linked_quest.completion_state == LINKED_QUEST_COMPLETION_STATE_ACTIVE):
            error_message = 'You already have this quest currently accepted.'
            break
        
        # Check whether the user has enough slots.
        user_stats = await get_user_stats(user_id)
        user_adventurer_rank_info = get_user_adventurer_rank_info(user_stats.credibility)
        if (
            (linked_quest_listing is not None) and
            sum(
                looped_linked_quest.completion_state == LINKED_QUEST_COMPLETION_STATE_ACTIVE
                for looped_linked_quest in linked_quest_listing
            ) >= user_adventurer_rank_info.quest_limit
        ):
            error_message = 'You cannot accept more quests.'
            break
        
        # Check whether the user's level is sufficient.
        quest_template = get_quest_template(quest_template_id)
        if quest_template is None:
            error_message = BROKEN_QUEST_DESCRIPTION
            break
        
        if quest_template.level > user_adventurer_rank_info.level + 1:
            error_message = 'Your rank is too low to accept this quest.'
            break
        
        # Check whether the user can repeat this quest anymore.
        if (linked_quest is not None):
            repeat_count = quest_template.repeat_count
            if repeat_count and (linked_quest.completion_count >= repeat_count):
                error_message = 'You already completed this quest the maximal amount of times.'
                break
        
        # Add quest.
        if linked_quest is None:
            linked_quest = instantiate_quest(user_id, guild_id, quest_batch.id, quest)
            await add_linked_quest(linked_quest)
        else:
            reset_linked_quest(linked_quest)
            await update_linked_quest(linked_quest)
        
        await client.interaction_response_message_edit(
            interaction_event,
            components = build_quest_accept_success_components(user_id, page_index, linked_quest.entry_id),
        )
        return
    
    await client.interaction_followup_message_create(
        interaction_event,
        content = error_message,
        show_for_invoking_user_only = True,
    )


@FEATURE_CLIENTS.interactions(custom_id = CUSTOM_ID_LINKED_QUEST_PAGE_INDEX_NAVIGATE_PATTERN)
async def page_linked_quest_listing_page_index_navigate(client, interaction_event, user_id, page_index):
    """
    Handles a user linked quest page index navigation component interaction.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the interaction.
    
    interaction_event : ``InteractionEvent``
        The received interaction event.
    
    user_id : `str`
        The invoking user's identifier as a string representing a hexadecimal integer.
    
    page_index : `str`
        The page's identifier as a string representing a hexadecimal integer.
    """
    try:
        user_id = int(user_id, 16)
        page_index = int(page_index, 16)
    except ValueError:
        return
    
    if user_id != interaction_event.user_id:
        return
    
    await client.interaction_component_acknowledge(
        interaction_event,
        False,
    )
    
    linked_quest_listing = await get_linked_quest_listing(user_id)
    
    user_stats = await get_user_stats(user_id)
    components = build_linked_quests_listing_components(
        interaction_event.user, interaction_event.guild_id, user_stats, linked_quest_listing, page_index
    )
    
    await client.interaction_response_message_edit(
        interaction_event,
        components = components,
    )


@FEATURE_CLIENTS.interactions(custom_id = CUSTOM_ID_LINKED_QUEST_ITEM_INFO_PATTERN)
async def linked_quest_details(client, interaction_event, user_id, page_index, linked_quest_entry_id):
    """
    Handles a user linked quest page index navigation component interaction.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the interaction.
    
    interaction_event : ``InteractionEvent``
        The received interaction event.
    
    user_id : `str`
        The invoking user's identifier as a string representing a hexadecimal integer.
    
    page_index : `str`
        The page's identifier as a string representing a hexadecimal integer.
    
    linked_quest_entry_id : `str`
        The linked quest's entries identifier in the database as a string representing a hexadecimal integer.
    """
    try:
        user_id = int(user_id, 16)
        page_index = int(page_index, 16)
        linked_quest_entry_id = int(linked_quest_entry_id, 16)
    except ValueError:
        return
    
    if user_id != interaction_event.user_id:
        return
    
    await client.interaction_component_acknowledge(
        interaction_event,
        False,
    )
    
    while True:
        linked_quest_listing = await get_linked_quest_listing(user_id)
        linked_quest = get_linked_quest_with_entry_id(linked_quest_listing, linked_quest_entry_id)
        
        if (linked_quest is None):
            error_message = 'You do not have such a quest.'
            break
        
        user_stats = await get_user_stats(user_id)
        
        await client.interaction_response_message_edit(
            interaction_event,
            components = build_linked_quest_details_components(linked_quest, user_stats, page_index),
        )
        return
    
    
    await client.interaction_followup_message_create(
        interaction_event,
        content = error_message,
        show_for_invoking_user_only = True,
    )


def _try_submit_item(requirement, inventory, item_entry, submissions_normalised):
    """
    Tries to submit the given item
    
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
    submissions_normalised : ``list<(Item, int, int, int, int)>``
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


async def _reward_user(linked_quest, inventory, user_stats, quest_level, user_level):
    """
    Rewards the user.
    
    This function is a coroutine.
    
    Parameters
    ----------
    linked_quest : ``LinkedQuest``
        Linked quest to distribute the awards from..
    
    inventory : ``Inventory``
        The user's inventory.
    
    user_stats : ``UserStats``
        The user's stats.
    
    quest_level : `int`
        The quest's level.
    
    user_level : `int`
        The user's level.
    
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
                balance_given = reward.balance
                
                user_balance = await get_user_balance(linked_quest.user_id)
                user_balance.modify_balance_by(balance_given)
                await save_user_balance(user_balance)
                
                if (rewards_normalised is None):
                    rewards_normalised = []
                
                rewards_normalised.append((QUEST_REWARD_TYPE_BALANCE, 0, balance_given))
            
            elif reward_type == QUEST_REWARD_TYPE_CREDIBILITY:
                credibility_given = reward.credibility
                
                user_reward_credibility = calculate_received_reward_credibility(
                    credibility_given, quest_level, user_level
                )
                user_stats.modify_credibility_by(user_reward_credibility)
                await save_user_stats(user_stats)
                
                guild_stats = await get_guild_stats(linked_quest.guild_id)
                guild_adventurer_rank_info = get_guild_adventurer_rank_info(guild_stats.credibility)
                guild_reward_credibility = calculate_received_reward_credibility(
                    credibility_given, quest_level, guild_adventurer_rank_info.level
                )
                guild_stats.set('credibility', guild_stats.credibility + guild_reward_credibility)
                await guild_stats.save()
                
                if (rewards_normalised is None):
                    rewards_normalised = []
                
                rewards_normalised.append((QUEST_REWARD_TYPE_CREDIBILITY, 0, user_reward_credibility))
            
            elif reward_type == QUEST_REWARD_TYPE_ITEM_EXACT:
                amount_given = reward.amount_given
                item_id = reward.item_id
                inventory.modify_item_amount(get_item(item_id), amount_given)
                
                if (rewards_normalised is None):
                    rewards_normalised = []
                
                rewards_normalised.append((QUEST_REWARD_TYPE_ITEM_EXACT, item_id, amount_given))
            
            else:
                # No other cases
                pass
    
    return rewards_normalised


@FEATURE_CLIENTS.interactions(custom_id = CUSTOM_ID_LINKED_QUEST_SUBMIT_AUTO_PATTERN)
async def handle_linked_quest_submit_item_auto(client, interaction_event, user_id, page_index, linked_quest_entry_id):
    """
    Handles a user linked quest item submission component interaction.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the interaction.
    
    interaction_event : ``InteractionEvent``
        The received interaction event.
    
    user_id : `str`
        The invoking user's identifier as a string representing a hexadecimal integer.
    
    page_index : `str`
        The page's identifier as a string representing a hexadecimal integer.
    
    linked_quest_entry_id : `str`
        The linked quest's entries identifier in the database as a string representing a hexadecimal integer.
    """
    try:
        user_id = int(user_id, 16)
        page_index = int(page_index, 16)
        linked_quest_entry_id = int(linked_quest_entry_id, 16)
    except ValueError:
        return
    
    if user_id != interaction_event.user_id:
        return
    
    await client.interaction_component_acknowledge(
        interaction_event,
        False,
    )
    
    while True:
        adventure = await get_active_adventure(user_id)
        if (adventure is not None):
            error_message = 'You cannot submit items while on adventure.'
            break
        
        linked_quest_listing = await get_linked_quest_listing(user_id)
        linked_quest = get_linked_quest_with_entry_id(linked_quest_listing, linked_quest_entry_id)
        
        if (linked_quest is None):
            error_message = 'You do not have such a quest.'
            break
        
        if linked_quest.completion_state == LINKED_QUEST_COMPLETION_STATE_COMPLETED:
            error_message = 'The quest is already completed'
            break
        
        expiration = get_linked_quest_expiration(linked_quest)
        if (expiration is not None) and (expiration < DateTime.now(TimeZone.utc)):
            error_message = 'The quest expired, you cannot interact with it anymore.'
            break
        
        quest_template = get_quest_template(linked_quest.template_id)
        if (quest_template is None):
            error_message = BROKEN_QUEST_DESCRIPTION
            break
        
        submissions_normalised = None
        inventory = await get_inventory(user_id)
        
        requirements = linked_quest.requirements
        if (requirements is not None):
            for requirement in requirements:
                for item_entry in iter_submission_requirement_item_entries_of_requirement(inventory, requirement):
                    submissions_normalised = _try_submit_item(
                        requirement, inventory, item_entry, submissions_normalised
                    )
        
        if submissions_normalised is None:
            error_message = 'You do not have any item to submit.'
            break
        
        await update_linked_quest(linked_quest)
        await save_inventory(inventory)
        
        quest_completion_ratio = get_linked_quest_completion_ratio(linked_quest)
        if quest_completion_ratio < 1.0:
            components = build_linked_quest_submit_success(
                user_id,
                page_index,
                linked_quest_entry_id,
                0,
                0,
                LINKED_QUEST_BACK_DIRECT_LOCATION_QUEST,
                submissions_normalised,
            )
        
        else:
            user_stats = await get_user_stats(user_id)
            user_level = get_user_adventurer_rank_info(user_stats.credibility).level
            rewards_normalised = await _reward_user(
                linked_quest, inventory, user_stats, quest_template.level, user_level
            )
            
            if linked_quest.batch_id != get_current_batch_id():
                await delete_linked_quest(linked_quest)
            else:
                linked_quest.completion_count += 1
                linked_quest.completion_state = LINKED_QUEST_COMPLETION_STATE_COMPLETED
                await update_linked_quest(linked_quest)
            
            components = build_linked_quest_submit_success_completed_components(
                client.id,
                user_id,
                page_index,
                interaction_event.guild_id,
                linked_quest,
                quest_template,
                user_stats,
                user_level,
                submissions_normalised,
                rewards_normalised,
            )
        
        await client.interaction_response_message_edit(
            interaction_event,
            components = components,
        )
        return
    
    
    await client.interaction_followup_message_create(
        interaction_event,
        content = error_message,
        show_for_invoking_user_only = True,
    )


async def _handle_submit_item_common(
    client,
    interaction_event,
    user_id,
    page_index,
    linked_quest_entry_id,
    requirement_index,
    item_page_index,
    item_id,
    back_direct_location,
):
    """
    Handles item submission.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the interaction.
    
    interaction_event : ``InteractionEvent``
        The received interaction event.
    
    user_id : `str`
        The invoking user's identifier as a string representing a hexadecimal integer.
    
    page_index : `str`
        The page's identifier as a string representing a hexadecimal integer.
    
    linked_quest_entry_id : `str`
        The linked quest's entries identifier in the database as a string representing a hexadecimal integer.
    
    requirement_index : `None | str`
        Requirement index to submit to as a string representing a hexadecimal integer.
    
    item_page_index : `None | str`
        The submitted item's page's index as a string representing a hexadecimal integer.
    
    item_id : `str`
        The item's identifier to submit as a string representing a hexadecimal integer.
    
    back_direct_location : `int`
        The location's identifier to back-direct the user to.
    """
    try:
        user_id = int(user_id, 16)
        page_index = int(page_index, 16)
        linked_quest_entry_id = int(linked_quest_entry_id, 16)
        requirement_index = 0 if (requirement_index is None) else int(requirement_index, 16)
        item_page_index = 0 if (item_page_index is None) else int(item_page_index, 16)
        item_id = int(item_id, 16)
    except ValueError:
        return
    
    if user_id != interaction_event.user_id:
        return
    
    await client.interaction_component_acknowledge(
        interaction_event,
        False,
    )
    
    while True:
        adventure = await get_active_adventure(user_id)
        if (adventure is not None):
            error_message = 'You cannot submit items while on adventure.'
            break
        
        linked_quest_listing = await get_linked_quest_listing(user_id)
        linked_quest = get_linked_quest_with_entry_id(linked_quest_listing, linked_quest_entry_id)
        
        if (linked_quest is None):
            error_message = 'You do not have such a quest.'
            break
        
        if linked_quest.completion_state == LINKED_QUEST_COMPLETION_STATE_COMPLETED:
            error_message = 'The quest is already completed'
            break
        
        expiration = get_linked_quest_expiration(linked_quest)
        if (expiration is not None) and (expiration < DateTime.now(TimeZone.utc)):
            error_message = 'The quest expired, you cannot interact with it anymore.'
            break
        
        quest_template = get_quest_template(linked_quest.template_id)
        if (quest_template is None):
            error_message = BROKEN_QUEST_DESCRIPTION
            break
        
        requirement = get_linked_quest_submission_requirement_at_index(linked_quest, requirement_index)
        if (requirement is None):
            error_message = 'The quest does not have such a requirement.'
            break
        
        inventory = await get_inventory(user_id)
        
        submissions_normalised = None
        
        item_entry = inventory.get_item_entry_by_id(item_id)
        if (item_entry is not None):
            submissions_normalised = _try_submit_item(
                requirement, inventory, item_entry, submissions_normalised
            )
        
        if submissions_normalised is None:
            error_message = 'You do not have any item to submit.'
            break
        
        await update_linked_quest(linked_quest)
        await save_inventory(inventory)
        
        quest_completion_ratio = get_linked_quest_completion_ratio(linked_quest)
        if quest_completion_ratio < 1.0:
            components = build_linked_quest_submit_success(
                user_id,
                page_index,
                linked_quest_entry_id,
                requirement_index,
                item_page_index,
                back_direct_location,
                submissions_normalised,
            )
        
        else:
            user_stats = await get_user_stats(user_id)
            user_level = get_user_adventurer_rank_info(user_stats.credibility).level
            rewards_normalised = await _reward_user(
                linked_quest, inventory, user_stats, quest_template.level, user_level
            )
            
            if linked_quest.batch_id != get_current_batch_id():
                await delete_linked_quest(linked_quest)
            else:
                linked_quest.completion_count += 1
                linked_quest.completion_state = LINKED_QUEST_COMPLETION_STATE_COMPLETED
                await update_linked_quest(linked_quest)
            
            components = build_linked_quest_submit_success_completed_components(
                client.id,
                user_id,
                page_index,
                interaction_event.guild_id,
                linked_quest,
                quest_template,
                user_stats,
                user_level,
                submissions_normalised,
                rewards_normalised,
            )
        
        await client.interaction_response_message_edit(
            interaction_event,
            components = components,
        )
        return
    
    
    await client.interaction_followup_message_create(
        interaction_event,
        content = error_message,
        show_for_invoking_user_only = True,
    )


@FEATURE_CLIENTS.interactions(custom_id = CUSTOM_ID_LINKED_QUEST_SUBMIT_EXECUTE_REQUIREMENT_PATTERN)
async def handle_linked_quest_submit_execute_requirement(
    client, interaction_event, user_id, page_index, linked_quest_entry_id, requirement_index, item_id
):
    """
    Handles a user linked quest requirement (item) submission component interaction.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the interaction.
    
    interaction_event : ``InteractionEvent``
        The received interaction event.
    
    user_id : `str`
        The invoking user's identifier as a string representing a hexadecimal integer.
    
    page_index : `str`
        The page's identifier as a string representing a hexadecimal integer.
    
    linked_quest_entry_id : `str`
        The linked quest's entries identifier in the database as as a string representing a hexadecimal integer.
    
    requirement_index : `str`
        Requirement index to submit to as a string representing a hexadecimal integer.
    
    item_id : `str`
        The item's identifier to submit as a string representing a hexadecimal integer.
    """
    await _handle_submit_item_common(
        client,
        interaction_event,
        user_id,
        page_index,
        linked_quest_entry_id,
        requirement_index,
        None,
        item_id,
        LINKED_QUEST_BACK_DIRECT_LOCATION_SELECT_REQUIREMENT,
    )


@FEATURE_CLIENTS.interactions(custom_id = CUSTOM_ID_LINKED_QUEST_SUBMIT_EXECUTE_ITEM_TOP_PATTERN)
async def handle_linked_quest_submit_execute_item_top(
    client, interaction_event, user_id, page_index, linked_quest_entry_id, item_page_index, item_id
):
    """
    Handles a user linked quest item submission component interaction.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the interaction.
    
    interaction_event : ``InteractionEvent``
        The received interaction event.
    
    user_id : `str`
        The invoking user's identifier as a string representing a hexadecimal integer.
    
    page_index : `str`
        The page's identifier as a string representing a hexadecimal integer.
    
    linked_quest_entry_id : `str`
        The linked quest's entries identifier in the database as as a string representing a hexadecimal integer.
    
    item_page_index : `str`
        The submitted item's page's index as a string representing a hexadecimal integer.
    
    item_id : `str`
        The item's identifier to submit as a string representing a hexadecimal integer.
    """
    await _handle_submit_item_common(
        client,
        interaction_event,
        user_id,
        page_index,
        linked_quest_entry_id,
        None,
        item_page_index,
        item_id,
        LINKED_QUEST_BACK_DIRECT_LOCATION_SELECT_ITEM_TOP,
    )


@FEATURE_CLIENTS.interactions(custom_id = CUSTOM_ID_LINKED_QUEST_SUBMIT_EXECUTE_ITEM_NESTED_PATTERN)
async def handle_linked_quest_submit_execute_item_nested(
    client, interaction_event, user_id, page_index, linked_quest_entry_id, requirement_index, item_page_index, item_id
):
    """
    Handles a user linked quest item submission component interaction.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the interaction.
    
    interaction_event : ``InteractionEvent``
        The received interaction event.
    
    user_id : `str`
        The invoking user's identifier as a string representing a hexadecimal integer.
    
    page_index : `str`
        The page's identifier as a string representing a hexadecimal integer.
    
    linked_quest_entry_id : `str`
        The linked quest's entries identifier in the database as a string representing a hexadecimal integer.
    
    requirement_index : `str`
        Requirement index to submit to as a string representing a hexadecimal integer.
    
    item_page_index : `str`
        The submitted item's page's index as a string representing a hexadecimal integer.
    
    item_id : `str`
        The item's identifier to submit as a string representing a hexadecimal integer.
    """
    await _handle_submit_item_common(
        client,
        interaction_event,
        user_id,
        page_index,
        linked_quest_entry_id,
        requirement_index,
        item_page_index,
        item_id,
        LINKED_QUEST_BACK_DIRECT_LOCATION_SELECT_ITEM_NESTED,
    )


async def _linked_quest_abandon(linked_quest, user_stats, credibility_penalty):
    """
    Abandons the linked quest.
    Reduces the user's credibility count for the amount.
    
    This function is a coroutine.
    
    Parameters
    ----------
    linked_quest : ``LinkedQuest``
        The linked quest to abandon.
    
    user_stats : ``UserStats``
        The user's stats.
    
    credibility_penalty : `int`
        Abandon credibility penalty.
    """
    if linked_quest.batch_id != get_current_batch_id():
        await delete_linked_quest(linked_quest)
    else:
        linked_quest.completion_state = LINKED_QUEST_COMPLETION_STATE_COMPLETED
        await update_linked_quest(linked_quest)
    
    if credibility_penalty:
        user_stats.modify_credibility_by(- credibility_penalty)
        await save_user_stats(user_stats)


@FEATURE_CLIENTS.interactions(custom_id = CUSTOM_ID_LINKED_QUEST_ABANDON_PATTERN)
async def linked_quest_abandon_invoke(client, interaction_event, user_id, page_index, linked_quest_entry_id):
    """
    Handles a user linked quest's abandoning component interaction.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the interaction.
    
    interaction_event : ``InteractionEvent``
        The received interaction event.
    
    user_id : `str`
        The invoking user's identifier as a string representing a hexadecimal integer.
    
    page_index : `str`
        The page's identifier as a string representing a hexadecimal integer.
    
    linked_quest_entry_id : `int`
        The linked quest's entries identifier in the database as a string representing a hexadecimal integer.
    """
    try:
        user_id = int(user_id, 16)
        page_index = int(page_index, 16)
        linked_quest_entry_id = int(linked_quest_entry_id, 16)
    except ValueError:
        return
    
    if user_id != interaction_event.user_id:
        return
    
    while True:
        linked_quest_listing = await get_linked_quest_listing(user_id)
        linked_quest = get_linked_quest_with_entry_id(linked_quest_listing, linked_quest_entry_id)
        
        if (linked_quest is None):
            error_message = 'You do not have such a quest.'
            break
        
        user_stats = await get_user_stats(user_id)
        
        quest_completion_ratio = get_linked_quest_completion_ratio(linked_quest)
        quest_template = get_quest_template(linked_quest.template_id)
        credibility_penalty = get_linked_quest_abandon_credibility_penalty(
            linked_quest.reward_credibility,
            (0 if quest_template is None else quest_template.level),
            get_user_adventurer_rank_info(user_stats.credibility).level,
            quest_completion_ratio,
        )
        
        # Ask the user for confirmation if the quest is still alive.
        expiration = get_linked_quest_expiration(linked_quest)
        if (expiration is None) or (expiration > DateTime.now(tz = TimeZone.utc)):
            await client.interaction_form_send(
                interaction_event,
                build_linked_quest_abandon_confirmation_form(linked_quest, user_stats, page_index, credibility_penalty),
            )
            return
        
        # Otherwise delete it.
        await client.interaction_component_acknowledge(
            interaction_event,
            False,
        )
        await _linked_quest_abandon(linked_quest, user_stats, credibility_penalty)
        await client.interaction_response_message_edit(
            interaction_event,
            components = build_linked_quest_abandon_success_components(
                user_id, page_index, interaction_event.guild_id, credibility_penalty
            ),
        )
        return
    
    
    await client.interaction_component_acknowledge(
        interaction_event,
    )
    await client.interaction_followup_message_create(
        interaction_event,
        content = error_message,
        show_for_invoking_user_only = True,
    )


@FEATURE_CLIENTS.interactions(custom_id = CUSTOM_ID_LINKED_QUEST_ABANDON_PATTERN, target = 'form')
async def linked_quest_abandon_confirm(client, interaction_event, user_id, page_index, linked_quest_entry_id):
    """
    Handles a user linked quest's abandoning component interaction.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the interaction.
    
    interaction_event : ``InteractionEvent``
        The received interaction event.
    
    user_id : `str`
        The invoking user's identifier as a string representing a hexadecimal integer.
    
    page_index : `str`
        The page's identifier as a string representing a hexadecimal integer.
    
    linked_quest_entry_id : `int`
        The linked quest's entries identifier in the database as a string representing a hexadecimal integer.
    """
    try:
        user_id = int(user_id, 16)
        page_index = int(page_index, 16)
        linked_quest_entry_id = int(linked_quest_entry_id, 16)
    except ValueError:
        return
    
    if user_id != interaction_event.user_id:
        return
    
    await client.interaction_component_acknowledge(
        interaction_event,
        False,
    )
    
    while True:
        linked_quest_listing = await get_linked_quest_listing(user_id)
        linked_quest = get_linked_quest_with_entry_id(linked_quest_listing, linked_quest_entry_id)
        
        if (linked_quest is None):
            error_message = 'You do not have such a quest.'
            break
        
        user_stats = await get_user_stats(user_id)
        
        quest_completion_ratio = get_linked_quest_completion_ratio(linked_quest)
        quest_template = get_quest_template(linked_quest.template_id)
        credibility_penalty = get_linked_quest_abandon_credibility_penalty(
            linked_quest.reward_credibility,
            (0 if quest_template is None else quest_template.level),
            get_user_adventurer_rank_info(user_stats.credibility).level,
            quest_completion_ratio,
        )
        
        await _linked_quest_abandon(linked_quest, user_stats, credibility_penalty)
        await client.interaction_response_message_edit(
            interaction_event,
            components = build_linked_quest_abandon_success_components(
                user_id, page_index, interaction_event.guild_id, credibility_penalty
            ),
        )
        return
    
    await client.interaction_followup_message_create(
        interaction_event,
        content = error_message,
        show_for_invoking_user_only = True,
    )


@FEATURE_CLIENTS.interactions(custom_id = CUSTOM_ID_QUEST_BOARD_ITEM_PATTERN)
async def quest_board_item(client, interaction_event, user_id, guild_id, page_index, quest_template_id, item_id):
    """
    Handles a quest board item component interaction.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the interaction.
    
    interaction_event : ``InteractionEvent``
        The received interaction event.
    
    user_id : `str`
        The invoking user's identifier as a string representing a hexadecimal integer.
    
    guild_id : `str`
        The parent quest's guild's identifier as a string representing a hexadecimal integer.
    
    page_index : `str`
        The quest board's current page's index as a string representing a hexadecimal integer.
    
    quest_template_id : `str`
        The quest's template identifier as a string representing a hexadecimal integer.
    
    item_id : `str`
        The item's identifier to show as a string representing a hexadecimal integer.
    """
    try:
        user_id = int(user_id, 16)
        guild_id = int(guild_id, 16)
        page_index = int(page_index, 16)
        quest_template_id = int(quest_template_id, 16)
        item_id = int(item_id, 16)
    except ValueError:
        return
    
    if user_id != interaction_event.user_id:
        return
    
    await client.interaction_component_message_edit(
        interaction_event,
        components = build_quest_board_item_components(
            user_id, guild_id, interaction_event.guild_id, page_index, quest_template_id, item_id
        ),
    )


async def _handle_linked_quest_info_item_common(
    client,
    interaction_event,
    user_id,
    page_index,
    linked_quest_entry_id,
    requirement_index,
    item_page_index,
    item_id,
    back_direct_location,
):
    """
    Handles item info.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the interaction.
    
    interaction_event : ``InteractionEvent``
        The received interaction event.
    
    user_id : `str`
        The invoking user's identifier as a string representing a hexadecimal integer.
    
    page_index : `str`
        The page's identifier as a string representing a hexadecimal integer.
    
    linked_quest_entry_id : `str`
        The linked quest's entries identifier in the database as a string representing a hexadecimal integer.
    
    requirement_index : `None | str`
        Requirement index to submit to as a string representing a hexadecimal integer.
    
    item_page_index : `None | str`
        The submitted item's page's index as a string representing a hexadecimal integer.
    
    item_id : `str`
        The item's identifier to submit as a string representing a hexadecimal integer.
    
    back_direct_location : `int`
        The location's identifier to back-direct the user to.
    """
    try:
        user_id = int(user_id, 16)
        page_index = int(page_index, 16)
        linked_quest_entry_id = int(linked_quest_entry_id, 16)
        requirement_index = 0 if (requirement_index is None) else int(requirement_index, 16)
        item_page_index = 0 if (item_page_index is None) else int(item_page_index, 16)
        item_id = int(item_id, 16)
    except ValueError:
        return
    
    if user_id != interaction_event.user_id:
        return
    
    components = build_linked_quest_item_components(
        user_id,
        page_index,
        linked_quest_entry_id,
        requirement_index,
        item_page_index,
        back_direct_location,
        item_id,
    )
    
    await client.interaction_component_message_edit(
        interaction_event,
        components = components,
    )


@FEATURE_CLIENTS.interactions(custom_id = CUSTOM_ID_LINKED_QUEST_INFO_ITEM_PATTERN)
async def handle_linked_quest_item_info(
    client, interaction_event, user_id, page_index, linked_quest_entry_id, item_id
):
    """
    Handles a linked quest item info component interaction.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the interaction.
    
    interaction_event : ``InteractionEvent``
        The received interaction event.
    
    user_id : `str`
        The invoking user's identifier as a string representing a hexadecimal integer.
    
    page_index : `str`
        The quest board's current page's index as a string representing a hexadecimal integer.
    
    linked_quest_entry_id : `str`
        The currently selected quest's entry's identifier  as a string representing a hexadecimal integer.
    
    item_id : `str`
        The item's identifier to show as a string representing a hexadecimal integer.
    """
    await _handle_linked_quest_info_item_common(
        client,
        interaction_event,
        user_id,
        page_index,
        linked_quest_entry_id,
        None,
        None,
        item_id,
        LINKED_QUEST_BACK_DIRECT_LOCATION_QUEST,
    )


@FEATURE_CLIENTS.interactions(custom_id = CUSTOM_ID_LINKED_QUEST_SUBMIT_INFO_REQUIREMENT_PATTERN)
async def handle_linked_quest_submit_item_info_top(
    client, interaction_event, user_id, page_index, linked_quest_entry_id, requirement_index, item_id
):
    """
    Handles a linked quest requirement (item) info component interaction.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the interaction.
    
    interaction_event : ``InteractionEvent``
        The received interaction event.
    
    user_id : `str`
        The invoking user's identifier as a string representing a hexadecimal integer.
    
    page_index : `str`
        The quest board's current page's index as a string representing a hexadecimal integer.
    
    linked_quest_entry_id : `str`
        The currently selected quest's entry's identifier  as a string representing a hexadecimal integer.
    
    requirement_index : `str`
        Requirement index to submit to as a string representing a hexadecimal integer.
    
    item_id : `str`
        The item's identifier to show as a string representing a hexadecimal integer.
    """
    await _handle_linked_quest_info_item_common(
        client,
        interaction_event,
        user_id,
        page_index,
        linked_quest_entry_id,
        requirement_index,
        None,
        item_id,
        LINKED_QUEST_BACK_DIRECT_LOCATION_SELECT_REQUIREMENT,
    )


@FEATURE_CLIENTS.interactions(custom_id = CUSTOM_ID_LINKED_QUEST_SUBMIT_INFO_ITEM_TOP_PATTERN)
async def handle_linked_quest_submit_item_info_top(
    client, interaction_event, user_id, page_index, linked_quest_entry_id, item_page_index, item_id
):
    """
    Handles a linked quest item info component interaction.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the interaction.
    
    interaction_event : ``InteractionEvent``
        The received interaction event.
    
    user_id : `str`
        The invoking user's identifier as a string representing a hexadecimal integer.
    
    page_index : `str`
        The quest board's current page's index as a string representing a hexadecimal integer.
    
    linked_quest_entry_id : `str`
        The currently selected quest's entry's identifier  as a string representing a hexadecimal integer.
    
    item_page_index : `int`
        The currently shown item's page's index.
    
    item_id : `str`
        The item's identifier to show as a string representing a hexadecimal integer.
    """
    await _handle_linked_quest_info_item_common(
        client,
        interaction_event,
        user_id,
        page_index,
        linked_quest_entry_id,
        None,
        item_page_index,
        item_id,
        LINKED_QUEST_BACK_DIRECT_LOCATION_SELECT_ITEM_TOP,
    )


@FEATURE_CLIENTS.interactions(custom_id = CUSTOM_ID_LINKED_QUEST_SUBMIT_INFO_ITEM_NESTED_PATTERN)
async def handle_linked_quest_submit_item_info_nested(
    client, interaction_event, user_id, page_index, linked_quest_entry_id, requirement_index, item_page_index, item_id
):
    """
    Handles a linked quest item info component interaction.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the interaction.
    
    interaction_event : ``InteractionEvent``
        The received interaction event.
    
    user_id : `str`
        The invoking user's identifier as a string representing a hexadecimal integer.
    
    page_index : `str`
        The quest board's current page's index as a string representing a hexadecimal integer.
    
    linked_quest_entry_id : `str`
        The currently selected quest's entry's identifier  as a string representing a hexadecimal integer.
    
    requirement_index : `str`
        Requirement index to submit to as a string representing a hexadecimal integer.
    
    item_page_index : `int`
        The currently shown item's page's index.
    
    item_id : `str`
        The item's identifier to show as a string representing a hexadecimal integer.
    """
    await _handle_linked_quest_info_item_common(
        client,
        interaction_event,
        user_id,
        page_index,
        linked_quest_entry_id,
        requirement_index,
        item_page_index,
        item_id,
        LINKED_QUEST_BACK_DIRECT_LOCATION_SELECT_ITEM_NESTED,
    )


@FEATURE_CLIENTS.interactions(custom_id = CUSTOM_ID_LINKED_QUEST_SUBMIT_SELECT_REQUIREMENT_PATTERN)
async def handle_linked_quest_submit_select_requirement(
    client,
    interaction_event,
    user_id,
    page_index,
    linked_quest_entry_id,
    requirement_select_page_index,
):
    """
    Handles a linked quest submit select requirement interaction.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the interaction.
    
    interaction_event : ``InteractionEvent``
        The received interaction event.
    
    user_id : `str`
        The invoking user's identifier as a string representing a hexadecimal integer.
    
    page_index : `str`
        The linked quest view's current page's index as a string representing a hexadecimal integer.
    
    linked_quest_entry_id : `str`
        The selected linked quest's identifier as a string representing a hexadecimal integer.
    
    requirement_select_page_index : `str`
        The submission requirement page's index to show as a string representing a hexadecimal integer.
    """
    try:
        user_id = int(user_id, 16)
        page_index = int(page_index, 16)
        linked_quest_entry_id = int(linked_quest_entry_id, 16)
        requirement_select_page_index = int(requirement_select_page_index, 16)
    except ValueError:
        return
    
    if user_id != interaction_event.user_id:
        return
    
    await client.interaction_component_acknowledge(
        interaction_event,
        False,
    )
    
    while True:
        linked_quest_listing = await get_linked_quest_listing(user_id)
        linked_quest = get_linked_quest_with_entry_id(linked_quest_listing, linked_quest_entry_id)
        
        if (linked_quest is None):
            error_message = 'You do not have such a quest.'
            break
        
        inventory = await get_inventory(user_id)
        
        await client.interaction_response_message_edit(
            interaction_event,
            components = build_linked_quest_submit_select_requirement_components(
                linked_quest, inventory, page_index, requirement_select_page_index
            ),
        )
        return
    
    await client.interaction_followup_message_create(
        interaction_event,
        content = error_message,
        show_for_invoking_user_only = True,
    )


async def _handle_linked_submit_select_item_common(
    client,
    interaction_event,
    user_id,
    page_index,
    linked_quest_entry_id,
    requirement_index,
    item_page_index,
    top
):
    """
    handles a linked quest submit select item interaction.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the interaction.
    
    interaction_event : ``InteractionEvent``
        The received interaction event.
    
    user_id : `str`
        The invoking user's identifier as a string representing a hexadecimal integer.
    
    page_index : `str`
        The linked quest view's current page's index as a string representing a hexadecimal integer.
    
    linked_quest_entry_id : `str`
        The selected linked quest's identifier as a string representing a hexadecimal integer.
    
    requirement_index : `None | int`
        The submission requirement's index as a string representing a hexadecimal integer.
    
    item_page_index : `int`
        The item's page's index to render as a string representing a hexadecimal integer.
    
    top : `int`
        Whether to use top custom identifiers.
    """
    try:
        user_id = int(user_id, 16)
        page_index = int(page_index, 16)
        linked_quest_entry_id = int(linked_quest_entry_id, 16)
        requirement_index = 0 if (requirement_index is None) else int(requirement_index, 16)
        item_page_index = int(item_page_index, 16)
    except ValueError:
        return
    
    if user_id != interaction_event.user_id:
        return
    
    await client.interaction_component_acknowledge(
        interaction_event,
        False,
    )
    
    while True:
        linked_quest_listing = await get_linked_quest_listing(user_id)
        linked_quest = get_linked_quest_with_entry_id(linked_quest_listing, linked_quest_entry_id)
        
        if (linked_quest is None):
            error_message = 'You do not have such a quest.'
            break
        
        inventory = await get_inventory(user_id)
        
        await client.interaction_response_message_edit(
            interaction_event,
            components = build_linked_quest_submit_select_item_components(
                linked_quest, inventory, page_index, requirement_index, item_page_index, top
            ),
        )
        return
    
    await client.interaction_followup_message_create(
        interaction_event,
        content = error_message,
        show_for_invoking_user_only = True,
    )


@FEATURE_CLIENTS.interactions(custom_id = CUSTOM_ID_LINKED_QUEST_SUBMIT_SELECT_ITEM_TOP_PATTERN)
async def handle_linked_quest_submit_select_item_top(
    client,
    interaction_event,
    user_id,
    page_index,
    linked_quest_entry_id,
    item_page_index,
):
    """
    handles a linked quest submit select item top interaction.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the interaction.
    
    interaction_event : ``InteractionEvent``
        The received interaction event.
    
    user_id : `str`
        The invoking user's identifier as a string representing a hexadecimal integer.
    
    page_index : `str`
        The linked quest view's current page's index as a string representing a hexadecimal integer.
    
    linked_quest_entry_id : `str`
        The selected linked quest's identifier as a string representing a hexadecimal integer.
    
    item_page_index : `int`
        The item's page's index to render as a string representing a hexadecimal integer.
    """
    await _handle_linked_submit_select_item_common(
        client,
        interaction_event,
        user_id,
        page_index,
        linked_quest_entry_id,
        None,
        item_page_index,
        True,
    )


@FEATURE_CLIENTS.interactions(custom_id = CUSTOM_ID_LINKED_QUEST_SUBMIT_SELECT_ITEM_NESTED_PATTERN)
async def handle_linked_quest_submit_select_item_nested(
    client,
    interaction_event,
    user_id,
    page_index,
    linked_quest_entry_id,
    requirement_index,
    item_page_index,
):
    """
    handles a linked quest submit select item nested interaction.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the interaction.
    
    interaction_event : ``InteractionEvent``
        The received interaction event.
    
    user_id : `str`
        The invoking user's identifier as a string representing a hexadecimal integer.
    
    page_index : `str`
        The linked quest view's current page's index as a string representing a hexadecimal integer.
    
    linked_quest_entry_id : `str`
        The selected linked quest's identifier as a string representing a hexadecimal integer.
    
    requirement_index : `int`
        The submission requirement's index as a string representing a hexadecimal integer.
    
    item_page_index : `int`
        The item's page's index to render as a string representing a hexadecimal integer.
    """
    await _handle_linked_submit_select_item_common(
        client,
        interaction_event,
        user_id,
        page_index,
        linked_quest_entry_id,
        requirement_index,
        item_page_index,
        False
    )
