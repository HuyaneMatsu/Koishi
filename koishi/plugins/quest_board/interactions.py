__all__ = ()

from datetime import datetime as DateTime, timezone as TimeZone

from ...bots import FEATURE_CLIENTS

from ..adventure_core import get_active_adventure
from ..guild_stats import get_guild_stats
from ..inventory_core import get_inventory, save_inventory
from ..quest_core import (
    LINKED_QUEST_COMPLETION_STATE_ACTIVE, LINKED_QUEST_COMPLETION_STATE_COMPLETED, LinkedQuest, add_linked_quest,
    delete_linked_quest, get_current_batch_id, get_linked_quest_abandon_credibility_penalty,
    get_linked_quest_completion_ratio, get_linked_quest_listing, get_quest_template_nullable,
    get_user_adventurer_rank_info, instantiate_quest, reset_linked_quest, update_linked_quest
)
from ..user_balance import get_user_balance, save_user_balance
from ..user_stats_core import get_user_stats, save_user_stats

from .component_building import (
    build_linked_quest_abandon_confirmation_form, build_linked_quest_abandon_success_components,
    build_linked_quest_details_components, build_linked_quest_item_components, build_linked_quest_item_group_components,
    build_linked_quest_submit_select_item_components, build_linked_quest_submit_select_requirement_components,
    build_linked_quest_submit_success, build_linked_quest_submit_success_completed_components,
    build_linked_quests_listing_components, build_quest_accept_success_components,
    build_quest_complete_confirmation_form, build_quest_board_item_components, build_quest_board_item_group_components,
    build_quest_board_quest_listing_components, build_quest_details_components,
    build_quest_select_requirement_components
)
from .constants import (
    BACK_DIRECT_LOCATION_QUEST, BACK_DIRECT_LOCATION_SELECT_ITEM_NESTED, BACK_DIRECT_LOCATION_SELECT_ITEM_TOP,
    BACK_DIRECT_LOCATION_SELECT_REQUIREMENT, BROKEN_QUEST_DESCRIPTION
)
from .custom_ids import (
    CUSTOM_ID_COMPLETION_COUNT, CUSTOM_ID_LINKED_QUEST_ABANDON_PATTERN, CUSTOM_ID_LINKED_QUEST_INFO_ITEM_DISABLED,
    CUSTOM_ID_LINKED_QUEST_INFO_ITEM_PATTERN, CUSTOM_ID_LINKED_QUEST_ITEM_INFO_PATTERN,
    CUSTOM_ID_LINKED_QUEST_PAGE_INDEX_DECREMENT_DISABLED, CUSTOM_ID_LINKED_QUEST_PAGE_INDEX_INCREMENT_DISABLED,
    CUSTOM_ID_LINKED_QUEST_PAGE_INDEX_NAVIGATE_PATTERN, CUSTOM_ID_LINKED_QUEST_SUBMIT_AUTO_PATTERN,
    CUSTOM_ID_LINKED_QUEST_SUBMIT_DISABLED, CUSTOM_ID_LINKED_QUEST_SUBMIT_EXECUTE_ITEM_NESTED_PATTERN,
    CUSTOM_ID_LINKED_QUEST_SUBMIT_EXECUTE_ITEM_TOP_PATTERN, CUSTOM_ID_LINKED_QUEST_SUBMIT_EXECUTE_REQUIREMENT_PATTERN,
    CUSTOM_ID_LINKED_QUEST_SUBMIT_INFO_ITEM_GROUP_REQUIREMENT_PATTERN,
    CUSTOM_ID_LINKED_QUEST_SUBMIT_INFO_ITEM_NESTED_PATTERN, CUSTOM_ID_LINKED_QUEST_SUBMIT_INFO_ITEM_REQUIREMENT_PATTERN,
    CUSTOM_ID_LINKED_QUEST_SUBMIT_INFO_ITEM_TOP_PATTERN, CUSTOM_ID_LINKED_QUEST_SUBMIT_SELECT_ITEM_NESTED_PATTERN,
    CUSTOM_ID_LINKED_QUEST_SUBMIT_SELECT_ITEM_PAGE_INDEX_DECREMENT_DISABLED,
    CUSTOM_ID_LINKED_QUEST_SUBMIT_SELECT_ITEM_PAGE_INDEX_INCREMENT_DISABLED,
    CUSTOM_ID_LINKED_QUEST_SUBMIT_SELECT_ITEM_TOP_PATTERN,
    CUSTOM_ID_LINKED_QUEST_SUBMIT_SELECT_REQUIREMENT_PAGE_INDEX_DECREMENT_DISABLED,
    CUSTOM_ID_LINKED_QUEST_SUBMIT_SELECT_REQUIREMENT_PAGE_INDEX_INCREMENT_DISABLED,
    CUSTOM_ID_LINKED_QUEST_SUBMIT_SELECT_REQUIREMENT_PATTERN, CUSTOM_ID_QUEST_ACCEPT_DISABLED,
    CUSTOM_ID_QUEST_ACCEPT_PATTERN, CUSTOM_ID_QUEST_BOARD_COMPLETE_PATTERN, CUSTOM_ID_QUEST_BOARD_ITEM_DISABLED,
    CUSTOM_ID_QUEST_BOARD_ITEM_PATTERN, CUSTOM_ID_QUEST_BOARD_PAGE_INDEX_DECREMENT_DISABLED,
    CUSTOM_ID_QUEST_BOARD_PAGE_INDEX_INCREMENT_DISABLED, CUSTOM_ID_QUEST_BOARD_PAGE_INDEX_NAVIGATE_PATTERN,
    CUSTOM_ID_QUEST_BOARD_QUEST_DETAILS_PATTERN, CUSTOM_ID_QUEST_BOARD_SELECT_ITEM_GROUP_REQUIREMENT_PATTERN,
    CUSTOM_ID_QUEST_BOARD_SELECT_ITEM_REQUIREMENT_PATTERN,
    CUSTOM_ID_QUEST_BOARD_SELECT_REQUIREMENT_PAGE_INDEX_DECREMENT_DISABLED,
    CUSTOM_ID_QUEST_BOARD_SELECT_REQUIREMENT_PAGE_INDEX_INCREMENT_DISABLED,
    CUSTOM_ID_QUEST_BOARD_SELECT_REQUIREMENT_PATTERN
)
from .helpers import (
    do_reward_user, do_submit_complete_item, get_allowed_completion_count, get_linked_quest_expiration,
    get_linked_quest_for_deduplication, get_linked_quest_submission_requirement_at_index,
    get_linked_quest_with_entry_id, get_quest_in_possession_count, get_quest_with_template_id,
    iter_submission_requirement_item_entries_of_requirement, try_submit_item
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
        CUSTOM_ID_QUEST_BOARD_SELECT_REQUIREMENT_PAGE_INDEX_DECREMENT_DISABLED,
        CUSTOM_ID_QUEST_BOARD_SELECT_REQUIREMENT_PAGE_INDEX_INCREMENT_DISABLED,
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
            inventory = await get_inventory(user_id)
            
            components = build_quest_details_components(
                user_id, guild_id, interaction_event.guild_id, page_index, quest, linked_quest, inventory, user_stats
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


async def _check_quest_accept_conditions_common(
    user_id, guild_id, quest_template_id, check_for_empty_quest_slot
):
    """
    Common check to execute when accepting a quest.
    
    This function is a coroutine.
    
    Parameters
    ----------
    user_id : `str`
        The invoking user's identifier.
    
    guild_id : `int`
        The guild's identifier where the quest belongs to.
    
    quest_template_id : `str`
        The quest's template identifier.
    
    check_for_empty_quest_slot : `int`
        Whether should check for empty quest slot.
    
    Returns
    -------
    error_message_or_fields : ``(None | str, None | (QuestBatch, Quest, None | LinkedQuest, QuestTemplate, UserStats))``
    """
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
        
        user_stats = await get_user_stats(user_id)
        user_adventurer_rank_info = get_user_adventurer_rank_info(user_stats.credibility)
        # Check whether the user has enough slots.
        if (
            check_for_empty_quest_slot and
            (linked_quest_listing is not None) and
            sum(
                looped_linked_quest.completion_state == LINKED_QUEST_COMPLETION_STATE_ACTIVE
                for looped_linked_quest in linked_quest_listing
            ) >= user_adventurer_rank_info.quest_limit
        ):
            error_message = 'You cannot accept more quests.'
            break
        
        # Check whether the user's level is sufficient.
        quest_template = get_quest_template_nullable(quest_template_id)
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
        
        return None, (quest_batch, quest, linked_quest, quest_template, user_stats)
    
    return error_message, None


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
        The current page's index as a string representing a hexadecimal integer.
    
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
        error_message, fields = await _check_quest_accept_conditions_common(
            user_id, guild_id, quest_template_id, True
        )
        if (error_message is not None):
            break
        
        quest_batch, quest, linked_quest, quest_template, user_stats = fields
        
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



@FEATURE_CLIENTS.interactions(custom_id = CUSTOM_ID_QUEST_BOARD_COMPLETE_PATTERN)
async def handle_quest_board_complete(
    client, interaction_event, user_id, guild_id, page_index, quest_template_id
):
    """
    Handles a quest board complete component interaction.
    
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
    
    # Cannot acknowledge since we may respond with a form.
    
    while True:
        error_message, fields = await _check_quest_accept_conditions_common(
            user_id, guild_id, quest_template_id, False
        )
        if (error_message is not None):
            break
        
        quest_batch, quest, linked_quest, quest_template, user_stats = fields
        inventory = await get_inventory(user_id)
        possession_count = get_quest_in_possession_count(quest, inventory)
        if not possession_count:
            error_message = 'You do not have enough items in possession to complete this quest.'
            break
        
        await client.interaction_form_send(
            interaction_event,
            build_quest_complete_confirmation_form(
                user_id, guild_id, page_index, quest, linked_quest, quest_template, user_stats, possession_count
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
        
        quest_template = get_quest_template_nullable(linked_quest.template_id)
        if (quest_template is None):
            error_message = BROKEN_QUEST_DESCRIPTION
            break
        
        submissions_normalised = None
        inventory = await get_inventory(user_id)
        
        requirements = linked_quest.requirements
        if (requirements is not None):
            for requirement in requirements:
                for item_entry in [*iter_submission_requirement_item_entries_of_requirement(inventory, requirement)]:
                    submissions_normalised = try_submit_item(
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
                BACK_DIRECT_LOCATION_QUEST,
                submissions_normalised,
            )
        
        else:
            user_stats = await get_user_stats(user_id)
            user_balance = await get_user_balance(linked_quest.user_id)
            guild_stats = await get_guild_stats(linked_quest.guild_id)
            user_level = get_user_adventurer_rank_info(user_stats.credibility).level
            
            rewards_normalised = do_reward_user(
                linked_quest, inventory, user_stats, user_balance, guild_stats, quest_template.level, user_level, 1
            )
            
            await save_user_stats(user_stats)
            await save_user_balance(user_balance)
            await save_inventory(inventory)
            await guild_stats.save()
            
            if linked_quest.batch_id != get_current_batch_id():
                await delete_linked_quest(linked_quest)
            else:
                linked_quest.completion_count += 1
                linked_quest.completion_state = LINKED_QUEST_COMPLETION_STATE_COMPLETED
                await update_linked_quest(linked_quest)
            
            components = build_linked_quest_submit_success_completed_components(
                client.id,
                user_id,
                0,
                page_index,
                interaction_event.guild_id,
                linked_quest,
                quest_template,
                user_stats,
                user_level,
                submissions_normalised,
                rewards_normalised,
                1,
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
        
        quest_template = get_quest_template_nullable(linked_quest.template_id)
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
            submissions_normalised = try_submit_item(
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
            user_balance = await get_user_balance(linked_quest.user_id)
            guild_stats = await get_guild_stats(linked_quest.guild_id)
            user_level = get_user_adventurer_rank_info(user_stats.credibility).level
            
            rewards_normalised = do_reward_user(
                linked_quest, inventory, user_stats, user_balance, guild_stats, quest_template.level, user_level, 1
            )
            
            await save_user_stats(user_stats)
            await save_user_balance(user_balance)
            await save_inventory(inventory)
            await guild_stats.save()
            
            if linked_quest.batch_id != get_current_batch_id():
                await delete_linked_quest(linked_quest)
            else:
                linked_quest.completion_count += 1
                linked_quest.completion_state = LINKED_QUEST_COMPLETION_STATE_COMPLETED
                await update_linked_quest(linked_quest)
            
            components = build_linked_quest_submit_success_completed_components(
                client.id,
                user_id,
                0,
                page_index,
                interaction_event.guild_id,
                linked_quest,
                quest_template,
                user_stats,
                user_level,
                submissions_normalised,
                rewards_normalised,
                1,
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
        BACK_DIRECT_LOCATION_SELECT_REQUIREMENT,
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
        BACK_DIRECT_LOCATION_SELECT_ITEM_TOP,
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
        BACK_DIRECT_LOCATION_SELECT_ITEM_NESTED,
    )


@FEATURE_CLIENTS.interactions(custom_id = CUSTOM_ID_QUEST_BOARD_COMPLETE_PATTERN, target = 'form')
async def handle_quest_board_complete_execute(
    client,
    interaction_event,
    user_id,
    guild_id,
    page_index,
    quest_template_id,
    *,
    completion_count_string : CUSTOM_ID_COMPLETION_COUNT = None,
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
    
    guild_id : `str`
        The parent quest's guild's identifier as a string representing a hexadecimal integer.
    
    page_index : `str`
        The quest board's current page's index as a string representing a hexadecimal integer.
    
    quest_template_id : `str`
        The quest's template identifier as a string representing a hexadecimal integer.
    
    completion_count_string : `None | str` = `None`, Optional (Keyword only)
        How much times to complete the quest.
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
        # Convert `completion_count_string`.
        if (
            (completion_count_string is None) or
            (not completion_count_string.isdecimal()) or
            (len(completion_count_string) > 22)
        ):
            completion_count = -1
        else:
            try:
                completion_count = int(completion_count_string)
            except ValueError:
                completion_count = -1
        
        if not completion_count:
            error_message = 'Cannot complete a quest zero times'
            break
        
        error_message, fields = await _check_quest_accept_conditions_common(
            user_id, guild_id, quest_template_id, False
        )
        if (error_message is not None):
            break
        
        quest_batch, quest, linked_quest, quest_template, user_stats = fields
        inventory = await get_inventory(user_id)
        possession_count = get_quest_in_possession_count(quest, inventory)
        if not possession_count:
            error_message = 'You do not own enough items to complete the quest any times.'
            break
        
        if completion_count == -1:
            completion_count = possession_count
        
        allowed_completion_count = get_allowed_completion_count(linked_quest, quest_template, completion_count)
        if not allowed_completion_count:
            error_message = 'You cannot complete this quest more times.'
            break
        
        # Create the linked quest if it does not exist yet.
        if linked_quest is None:
            linked_quest = instantiate_quest(user_id, guild_id, quest_batch.id, quest)
            linked_quest_created = True
        else:
            reset_linked_quest(linked_quest)
            linked_quest_created = False
        
        # Submit items.
        submissions_normalised = None
        
        requirements = linked_quest.requirements
        if (requirements is not None):
            for requirement in requirements:
                for item_entry in [*iter_submission_requirement_item_entries_of_requirement(inventory, requirement)]:
                    submissions_normalised = do_submit_complete_item(
                        requirement, inventory, item_entry, submissions_normalised, allowed_completion_count
                    )
        
        # Reward user
        user_stats = await get_user_stats(user_id)
        user_balance = await get_user_balance(linked_quest.user_id)
        guild_stats = await get_guild_stats(linked_quest.guild_id)
        user_level = get_user_adventurer_rank_info(user_stats.credibility).level
        
        rewards_normalised = do_reward_user(
            linked_quest,
            inventory,
            user_stats,
            user_balance,
            guild_stats,
            quest_template.level,
            user_level,
            allowed_completion_count,
        )
        
        await save_user_stats(user_stats)
        await save_user_balance(user_balance)
        await save_inventory(inventory)
        await guild_stats.save()
        
        # Update quest.
        linked_quest.completion_count += allowed_completion_count
        linked_quest.completion_state = LINKED_QUEST_COMPLETION_STATE_COMPLETED
        
        if linked_quest_created:
            await add_linked_quest(linked_quest)
        else:
            await update_linked_quest(linked_quest)
        
        # Respond.
        components = build_linked_quest_submit_success_completed_components(
            client.id,
            user_id,
            page_index,
            0,
            interaction_event.guild_id,
            linked_quest,
            quest_template,
            user_stats,
            user_level,
            submissions_normalised,
            rewards_normalised,
            allowed_completion_count,
        )
    
        await client.interaction_response_message_edit(
            interaction_event,
            components = components,
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
    client : ``Client``batch_id
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
        
        credibility_penalty = get_linked_quest_abandon_credibility_penalty(
            linked_quest,
            get_user_adventurer_rank_info(user_stats.credibility).level,
        )
        
        # Ask the user for confirmation if the quest is still alive.
        expiration = get_linked_quest_expiration(linked_quest)
        if (expiration is None) or (expiration > DateTime.now(TimeZone.utc)):
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
async def handle_linked_quest_abandon_confirm(client, interaction_event, user_id, page_index, linked_quest_entry_id):
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
        
        credibility_penalty = get_linked_quest_abandon_credibility_penalty(
            linked_quest,
            get_user_adventurer_rank_info(user_stats.credibility).level,
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


async def _handle_quest_board_info_item_common(
    client,
    interaction_event,
    user_id,
    guild_id,
    page_index,
    quest_template_id,
    requirement_index,
    item_id,
    back_direct_location,
):
    """
    Handles item info received from a quest page.
    
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
        The page's identifier as a string representing a hexadecimal integer.
    
    quest_template_id : `int`
        The currently selected quest detail's template's identifier.
    
    requirement_index : `None | str`
        Requirement index to submit to as a string representing a hexadecimal integer.
    
    item_id : `str`
        The item's identifier to submit as a string representing a hexadecimal integer.
    
    back_direct_location : `int`
        The location's identifier to back-direct the user to.
    """
    try:
        user_id = int(user_id, 16)
        guild_id = int(guild_id, 16)
        page_index = int(page_index, 16)
        quest_template_id = int(quest_template_id, 16)
        requirement_index = 0 if (requirement_index is None) else int(requirement_index, 16)
        item_id = int(item_id, 16)
    except ValueError:
        return
    
    if user_id != interaction_event.user_id:
        return
    
    await client.interaction_component_message_edit(
        interaction_event,
        components = build_quest_board_item_components(
            user_id,
            guild_id,
            page_index,
            quest_template_id,
            requirement_index,
            back_direct_location,
            item_id,
        ),
    )


@FEATURE_CLIENTS.interactions(custom_id = CUSTOM_ID_QUEST_BOARD_ITEM_PATTERN)
async def handle_quest_board_item(client, interaction_event, user_id, guild_id, page_index, quest_template_id, item_id):
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
    await _handle_quest_board_info_item_common(
        client,
        interaction_event,
        user_id,
        guild_id,
        page_index,
        quest_template_id,
        None,
        item_id,
        BACK_DIRECT_LOCATION_QUEST,
    )


@FEATURE_CLIENTS.interactions(custom_id = CUSTOM_ID_QUEST_BOARD_SELECT_ITEM_REQUIREMENT_PATTERN)
async def handle_quest_board_select_item_requirement(
    client, interaction_event, user_id, guild_id, page_index, quest_template_id, requirement_index, item_id
):
    """
    Handles a quest board select item requirement component interaction.
    
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
    
    requirement_index : `str`
        Requirement index to submit to as a string representing a hexadecimal integer.
    
    item_id : `str`
        The item's identifier to show as a string representing a hexadecimal integer.
    """
    await _handle_quest_board_info_item_common(
        client,
        interaction_event,
        user_id,
        guild_id,
        page_index,
        quest_template_id,
        requirement_index,
        item_id,
        BACK_DIRECT_LOCATION_SELECT_REQUIREMENT,
    )


@FEATURE_CLIENTS.interactions(custom_id = CUSTOM_ID_QUEST_BOARD_SELECT_ITEM_GROUP_REQUIREMENT_PATTERN)
async def handle_quest_board_select_item_group_requirement(
    client, interaction_event, user_id, guild_id, page_index, quest_template_id, requirement_index, item_group_id
):
    """
    Handles a quest board select item group requirement component interaction.
    
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
    
    requirement_index : `str`
        Requirement index to submit to as a string representing a hexadecimal integer.
    
    item_group_id : `str`
        The item group's identifier to show as a string representing a hexadecimal integer.
    """
    try:
        user_id = int(user_id, 16)
        guild_id = int(guild_id, 16)
        page_index = int(page_index, 16)
        quest_template_id = int(quest_template_id, 16)
        requirement_index = int(requirement_index, 16)
        item_group_id = int(item_group_id, 16)
    except ValueError:
        return
    
    if user_id != interaction_event.user_id:
        return
    
    await client.interaction_component_message_edit(
        interaction_event,
        components = build_quest_board_item_group_components(
            user_id,
            guild_id,
            page_index,
            quest_template_id,
            requirement_index,
            BACK_DIRECT_LOCATION_SELECT_REQUIREMENT,
            item_group_id,
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
    Handles item info received from a linked quest page.
    
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
    
    await client.interaction_component_message_edit(
        interaction_event,
        components = build_linked_quest_item_components(
            user_id,
            page_index,
            linked_quest_entry_id,
            requirement_index,
            item_page_index,
            back_direct_location,
            item_id,
        ),
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
        BACK_DIRECT_LOCATION_QUEST,
    )


@FEATURE_CLIENTS.interactions(custom_id = CUSTOM_ID_LINKED_QUEST_SUBMIT_INFO_ITEM_REQUIREMENT_PATTERN)
async def handle_linked_quest_submit_item_info_requirement(
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
        BACK_DIRECT_LOCATION_SELECT_REQUIREMENT,
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
        BACK_DIRECT_LOCATION_SELECT_ITEM_TOP,
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
        BACK_DIRECT_LOCATION_SELECT_ITEM_NESTED,
    )


async def _handle_linked_quest_info_item_group_common(
    client,
    interaction_event,
    user_id,
    page_index,
    linked_quest_entry_id,
    requirement_index,
    item_group_page_index,
    item_group_id,
    back_direct_location,
):
    """
    Handles item group info.
    
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
    
    item_group_page_index : `None | str`
        The submitted item_group's page's index as a string representing a hexadecimal integer.
    
    item_group_id : `str`
        The item_group's identifier to submit as a string representing a hexadecimal integer.
    
    back_direct_location : `int`
        The location's identifier to back-direct the user to.
    """
    try:
        user_id = int(user_id, 16)
        page_index = int(page_index, 16)
        linked_quest_entry_id = int(linked_quest_entry_id, 16)
        requirement_index = 0 if (requirement_index is None) else int(requirement_index, 16)
        item_group_page_index = 0 if (item_group_page_index is None) else int(item_group_page_index, 16)
        item_group_id = int(item_group_id, 16)
    except ValueError:
        return
    
    if user_id != interaction_event.user_id:
        return
    
    components = build_linked_quest_item_group_components(
        user_id,
        page_index,
        linked_quest_entry_id,
        requirement_index,
        item_group_page_index,
        back_direct_location,
        item_group_id,
    )
    
    await client.interaction_component_message_edit(
        interaction_event,
        components = components,
    )


@FEATURE_CLIENTS.interactions(custom_id = CUSTOM_ID_LINKED_QUEST_SUBMIT_INFO_ITEM_GROUP_REQUIREMENT_PATTERN)
async def handle_linked_quest_submit_item_group_info_requirement(
    client, interaction_event, user_id, page_index, linked_quest_entry_id, requirement_index, item_group_id
):
    """
    Handles a linked quest requirement (item group) info component interaction.
    
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
    
    item_group_id : `str`
        The item group's identifier to show as a string representing a hexadecimal integer.
    """
    await _handle_linked_quest_info_item_group_common(
        client,
        interaction_event,
        user_id,
        page_index,
        linked_quest_entry_id,
        requirement_index,
        None,
        item_group_id,
        BACK_DIRECT_LOCATION_SELECT_REQUIREMENT,
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


@FEATURE_CLIENTS.interactions(custom_id = CUSTOM_ID_QUEST_BOARD_SELECT_REQUIREMENT_PATTERN)
async def handle_quest_board_select_requirement(
    client, interaction_event, user_id, guild_id, page_index, quest_template_id, requirement_select_page_index
):
    """
    Handles a quest board select requirement component interaction.
    
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
    
    requirement_select_page_index : `int`
        The requirement page index to display.
    """
    try:
        user_id = int(user_id, 16)
        guild_id = int(guild_id, 16)
        page_index = int(page_index, 16)
        quest_template_id = int(quest_template_id, 16)
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
        guild_stats = await get_guild_stats(guild_id)
        quest_batch = guild_stats.get_quest_batch()
        
        quest = get_quest_with_template_id(quest_batch, quest_template_id)
        
        if (quest is None):
            error_message = 'This quest is no longer available.'
            break
        
        inventory = await get_inventory(user_id)
        
        await client.interaction_response_message_edit(
            interaction_event,
            components = build_quest_select_requirement_components(
                user_id, guild_id, quest, inventory, page_index, requirement_select_page_index
            ),
        )
        return
    
    await client.interaction_followup_message_create(
        interaction_event,
        content = error_message,
        show_for_invoking_user_only = True,
    )
