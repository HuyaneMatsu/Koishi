__all__ = ('build_guild_quest_board_response', 'build_user_quests_response')

from datetime import datetime as DateTime, timezone as TimeZone

from hata.ext.slash import InteractionResponse

from ...bots import FEATURE_CLIENTS

from ..adventure_core import get_active_adventure
from ..guild_stats import get_guild_stats
from ..inventory_core import get_inventory, save_inventory
from ..item_core import get_item_nullable
from ..quest_core import (
    LinkedQuest, add_linked_quest, delete_linked_quest, get_guild_adventurer_rank_info, get_linked_quest_listing,
    get_quest_template, get_user_adventurer_rank_info, modify_linked_quest_amount_submitted
)
from ..user_balance import get_user_balance
from ..user_stats_core import get_user_stats

from .component_building import (
    build_linked_quest_abandon_success_components, build_linked_quest_details_components,
    build_linked_quest_failure_broken_quest_components, build_linked_quest_failure_expired_quest_components,
    build_linked_quest_failure_no_such_quest_components, build_linked_quest_failure_on_adventure_components,
    build_linked_quest_item_components, build_linked_quest_submit_failure_no_items_to_submit_components,
    build_linked_quest_submit_success_completed_components, build_linked_quest_submit_success_n_left_components,
    build_linked_quests_listing_components, build_quest_accept_failure_duplicate_components,
    build_quest_accept_failure_quest_limit_components, build_quest_accept_failure_user_level_low_components,
    build_quest_accept_success_components, build_quest_board_failure_guild_only_components,
    build_quest_board_item_components, build_quest_board_quest_listing_components, build_quest_details_components,
    build_quest_failure_no_such_quest_components, build_quest_failure_on_adventure_components
)
from .constants import (
    CUSTOM_ID_LINKED_QUEST_ABANDON_PATTERN, CUSTOM_ID_LINKED_QUEST_DETAILS_PATTERN,
    CUSTOM_ID_LINKED_QUEST_ITEM_DISABLED, CUSTOM_ID_LINKED_QUEST_ITEM_PATTERN,
    CUSTOM_ID_LINKED_QUEST_PAGE_INDEX_DECREMENT_DISABLED, CUSTOM_ID_LINKED_QUEST_PAGE_INDEX_INCREMENT_DISABLED,
    CUSTOM_ID_LINKED_QUEST_PAGE_INDEX_NAVIGATE_PATTERN, CUSTOM_ID_LINKED_QUEST_SUBMIT_DISABLED,
    CUSTOM_ID_LINKED_QUEST_SUBMIT_PATTERN, CUSTOM_ID_QUEST_ACCEPT_DISABLED, CUSTOM_ID_QUEST_ACCEPT_PATTERN,
    CUSTOM_ID_QUEST_BOARD_ITEM_DISABLED, CUSTOM_ID_QUEST_BOARD_ITEM_PATTERN,
    CUSTOM_ID_QUEST_BOARD_PAGE_INDEX_DECREMENT_DISABLED, CUSTOM_ID_QUEST_BOARD_PAGE_INDEX_INCREMENT_DISABLED,
    CUSTOM_ID_QUEST_BOARD_PAGE_INDEX_NAVIGATE_PATTERN, CUSTOM_ID_QUEST_BOARD_QUEST_DETAILS_PATTERN
)
from .helpers import (
    get_linked_quest_for_deduplication, get_linked_quest_with_entry_id, get_quest_with_template_id, get_submit_amount
)


async def build_guild_quest_board_response(guild, user_id):
    """
    Builds guild quest board response.
    
    This function is a coroutine.
    
    Parameters
    ----------
    guild : ``Guild``
        Respective guild.
    
    user_id : `int`
        The user who invoked the interaction.
    
    Returns
    -------
    response : ``InteractionResponse``
    """
    guild_stats = await get_guild_stats(guild.id)
    
    return InteractionResponse(
        components = build_quest_board_quest_listing_components(guild, guild_stats, user_id, 0)
    )


async def build_user_quests_response(user, guild_id):
    """
    Builds guild quest board response.
    
    This function is a coroutine.
    
    Parameters
    ----------
    user : ``ClientUserbase``
        The respective user.
    
    guild_id : `int`
        The guild identifier the command is called from.
    
    Returns
    -------
    response : ``InteractionResponse``
    """
    linked_quest_listing = await get_linked_quest_listing(user.id)
    user_stats = await get_user_stats(user.id)
    
    return InteractionResponse(
        components = build_linked_quests_listing_components(user, guild_id, user_stats, linked_quest_listing, 0)
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
        CUSTOM_ID_LINKED_QUEST_ITEM_DISABLED,
    ],
)
async def quest_action_disabled():
    """
    Dummy handler for component interactions that supposed be disabled.
    
    This function is a coroutine.
    """
    pass


@FEATURE_CLIENTS.interactions(custom_id = CUSTOM_ID_QUEST_BOARD_QUEST_DETAILS_PATTERN)
async def quest_board_quest_details(client, event, user_id, page_index, quest_template_id):
    """
    Handles a quest board quest details component interaction.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the interaction.
    
    event : ``InteractionEvent``
        The received interaction event.
    
    user_id : `str`
        The invoking user's identifier as hexadecimal number.
    
    page_index : `str`
        The quest board's current page's index as hexadecimal number.
    
    quest_template_id : `str`
        The quest's template identifier as hexadecimal number.
    """
    try:
        user_id = int(user_id, 16)
        page_index = int(page_index, 16)
        quest_template_id = int(quest_template_id, 16)
    except ValueError:
        return
    
    if user_id != event.user_id:
        return
    
    await client.interaction_component_acknowledge(event)
    
    while True:
        guild = event.guild
        if guild is None:
            components = build_quest_board_failure_guild_only_components()
            new_message = True
            break
        
        guild_stats = await get_guild_stats(guild.id)
        quest_batch = guild_stats.get_quest_batch()
        
        quest = get_quest_with_template_id(quest_batch, quest_template_id)
        
        if (quest is None):
            components = build_quest_failure_no_such_quest_components()
            new_message = True
            break
        
        user_stats = await get_user_stats(user_id)
        
        # Check whether the user already has a quest like this. If yes then redirect them to it.
        linked_quest_listing = await get_linked_quest_listing(user_id)
        linked_quest = get_linked_quest_for_deduplication(
            linked_quest_listing, guild.id, quest_batch.id, quest_template_id
        )
        if (linked_quest is not None):
            components = build_linked_quest_details_components(linked_quest, user_stats, 0)
            new_message = False
            break
        
        components = build_quest_details_components(user_id, page_index, quest, user_stats)
        new_message = False
        break
    
    if new_message:
        await client.interaction_followup_message_create(
            event,
            components = components,
            show_for_invoking_user_only = True,
        )
    else:
        await client.interaction_response_message_edit(
            event,
            components = components,
        )


@FEATURE_CLIENTS.interactions(custom_id = CUSTOM_ID_QUEST_BOARD_PAGE_INDEX_NAVIGATE_PATTERN)
async def quest_board_quest_listing_page_index_navigate(client, event, user_id, page_index):
    """
    Handles a quest board page index navigation component interaction.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the interaction.
    
    event : ``InteractionEvent``
        The received interaction event.
    
    user_id : `str`
        The invoking user's identifier as hexadecimal number.
    
    page_index : `str`
        The page's identifier as hexadecimal number.
    """
    try:
        user_id = int(user_id, 16)
        page_index = int(page_index, 16)
    except ValueError:
        return
    
    if user_id != event.user_id:
        return
    
    await client.interaction_component_acknowledge(event)
    
    while True:
        guild = event.guild
        if guild is None:
            components = build_quest_board_failure_guild_only_components()
            new_message = True
            break
        
        guild_stats = await get_guild_stats(guild.id)
        components = build_quest_board_quest_listing_components(guild, guild_stats, user_id, page_index)
        new_message = False
        break
    
    if new_message:
        await client.interaction_followup_message_create(
            event,
            components = components,
            show_for_invoking_user_only = True,
        )
    else:
        await client.interaction_response_message_edit(
            event,
            components = components,
        )


@FEATURE_CLIENTS.interactions(custom_id = CUSTOM_ID_QUEST_ACCEPT_PATTERN)
async def quest_accept(client, event, user_id, page_index, quest_template_id):
    """
    Handles a quest accept component interaction.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the interaction.
    
    event : ``InteractionEvent``
        The received interaction event.
    
    user_id : `str`
        The invoking user's identifier as hexadecimal number.
    
    page_index : `int`
        The current page's index in hexadecimal number.
    
    quest_template_id : `str`
        The quest's template identifier as hexadecimal number.
    """
    try:
        user_id = int(user_id, 16)
        page_index = int(page_index, 16)
        quest_template_id = int(quest_template_id, 16)
    except ValueError:
        return
    
    if user_id != event.user_id:
        return
    
    await client.interaction_component_acknowledge(event)
    
    while True:
        adventure = await get_active_adventure(user_id)
        if (adventure is not None):
            components = build_quest_failure_on_adventure_components()
            new_message = True
            break
        
        guild = event.guild
        if guild is None:
            components = build_quest_board_failure_guild_only_components()
            new_message = True
            break
        
        # Get the quest from the board.
        guild_stats = await get_guild_stats(guild.id)
        quest_batch = guild_stats.get_quest_batch()
        
        quest = get_quest_with_template_id(quest_batch, quest_template_id)
        
        # Check whether there is such a quest.
        if (quest is None):
            components = build_quest_failure_no_such_quest_components()
            new_message = True
            break
        
        # Check whether the user already has a quest like this.
        linked_quest_listing = await get_linked_quest_listing(user_id)
        linked_quest = get_linked_quest_for_deduplication(
            linked_quest_listing, guild.id, quest_batch.id, quest_template_id
        )
        if (linked_quest is not None):
            components = build_quest_accept_failure_duplicate_components()
            new_message = True
            break
        
        # Check whether the user has enough slots.
        user_stats = await get_user_stats(user_id)
        user_adventurer_rank_info = get_user_adventurer_rank_info(user_stats.credibility)
        if (linked_quest_listing is not None):
            if len(linked_quest_listing) >= user_adventurer_rank_info.quest_limit:
                components = build_quest_accept_failure_quest_limit_components()
                new_message = True
                break
        
        # Check whether the user's level is sufficient.
        quest_template = get_quest_template(quest_template_id)
        if quest_template is None:
            components = build_linked_quest_failure_broken_quest_components()
            new_message = False
            break
        
        if quest_template.level > user_adventurer_rank_info.level:
            components = build_quest_accept_failure_user_level_low_components()
            new_message = False
            break
        
        # Add quest.
        linked_quest = LinkedQuest(user_id, guild.id, quest_batch.id, quest)
        await add_linked_quest(linked_quest)
        
        components = build_quest_accept_success_components(user_id, page_index, linked_quest.entry_id)
        new_message = False
        break
    
    if new_message:
        await client.interaction_followup_message_create(
            event,
            components = components,
            show_for_invoking_user_only = True,
        )
    else:
        await client.interaction_response_message_edit(
            event,
            components = components,
        )


@FEATURE_CLIENTS.interactions(custom_id = CUSTOM_ID_LINKED_QUEST_PAGE_INDEX_NAVIGATE_PATTERN)
async def page_linked_quest_listing_page_index_navigate(client, event, user_id, page_index):
    """
    Handles a user linked quest page index navigation component interaction.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the interaction.
    
    event : ``InteractionEvent``
        The received interaction event.
    
    user_id : `str`
        The invoking user's identifier as hexadecimal number.
    
    page_index : `str`
        The page's identifier as hexadecimal number.
    """
    try:
        user_id = int(user_id, 16)
        page_index = int(page_index, 16)
    except ValueError:
        return
    
    if user_id != event.user_id:
        return
    
    await client.interaction_component_acknowledge(event)
    
    linked_quest_listing = await get_linked_quest_listing(user_id)
    
    user_stats = await get_user_stats(user_id)
    components = build_linked_quests_listing_components(
        event.user, event.guild_id, user_stats, linked_quest_listing, page_index
    )
    
    await client.interaction_response_message_edit(
        event,
        components = components,
    )


@FEATURE_CLIENTS.interactions(custom_id = CUSTOM_ID_LINKED_QUEST_DETAILS_PATTERN)
async def linked_quest_details(client, event, user_id, page_index, linked_quest_entry_id):
    """
    Handles a user linked quest page index navigation component interaction.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the interaction.
    
    event : ``InteractionEvent``
        The received interaction event.
    
    user_id : `str`
        The invoking user's identifier as hexadecimal number.
    
    page_index : `str`
        The page's identifier as hexadecimal number.
    
    linked_quest_entry_id : `str`
        The linked quest's entries identifier in the database.
    """
    try:
        user_id = int(user_id, 16)
        page_index = int(page_index, 16)
        linked_quest_entry_id = int(linked_quest_entry_id, 16)
    except ValueError:
        return
    
    if user_id != event.user_id:
        return
    
    await client.interaction_component_acknowledge(event)
    
    while True:
        linked_quest_listing = await get_linked_quest_listing(user_id)
        linked_quest = get_linked_quest_with_entry_id(linked_quest_listing, linked_quest_entry_id)
        
        if (linked_quest is None):
            components = build_linked_quest_failure_no_such_quest_components()
            new_message = True
            break
        
        user_stats = await get_user_stats(user_id)
        components = build_linked_quest_details_components(linked_quest, user_stats, page_index)
        new_message = False
        break
    
    
    if new_message:
        await client.interaction_followup_message_create(
            event,
            components = components,
            show_for_invoking_user_only = True,
        )
    else:
        await client.interaction_response_message_edit(
            event,
            components = components,
        )


@FEATURE_CLIENTS.interactions(custom_id = CUSTOM_ID_LINKED_QUEST_SUBMIT_PATTERN)
async def linked_quest_submit_item(client, event, user_id, page_index, linked_quest_entry_id):
    """
    Handles a user linked quest item submission component interaction.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the interaction.
    
    event : ``InteractionEvent``
        The received interaction event.
    
    user_id : `str`
        The invoking user's identifier as hexadecimal number.
    
    page_index : `str`
        The page's identifier as hexadecimal number.
    
    linked_quest_entry_id : `str`
        The linked quest's entries identifier in the database.
    """
    try:
        user_id = int(user_id, 16)
        page_index = int(page_index, 16)
        linked_quest_entry_id = int(linked_quest_entry_id, 16)
    except ValueError:
        return
    
    if user_id != event.user_id:
        return
    
    await client.interaction_component_acknowledge(event)
    
    while True:
        adventure = await get_active_adventure(user_id)
        if (adventure is not None):
            components = build_linked_quest_failure_on_adventure_components()
            new_message = False
            break
        
        linked_quest_listing = await get_linked_quest_listing(user_id)
        linked_quest = get_linked_quest_with_entry_id(linked_quest_listing, linked_quest_entry_id)
        
        if (linked_quest is None):
            components = build_linked_quest_failure_no_such_quest_components()
            new_message = False
            break
        
        if linked_quest.expires_at < DateTime.now(TimeZone.utc):
            components = build_linked_quest_failure_expired_quest_components()
            new_message = False
            break
        
        quest_template = get_quest_template(linked_quest.template_id)
        if (quest_template is None):
            components = build_linked_quest_failure_broken_quest_components()
            new_message = False
            break
        
        item = get_item_nullable(quest_template.item_id)
        if (item is None):
            components = build_linked_quest_failure_broken_quest_components()
            new_message = False
            break
        
        inventory = await get_inventory(user_id)
        current_amount_count = inventory.get_item_amount(item)
        if not current_amount_count:
            components = build_linked_quest_submit_failure_no_items_to_submit_components()
            new_message = True
            break
        
        amount_type = quest_template.amount_type
        amount_required = linked_quest.amount_required
        amount_submitted = linked_quest.amount_submitted
        amount_to_be_used = amount_required - amount_submitted
        amount_used, amount_used_count = get_submit_amount(item, amount_type, amount_to_be_used, current_amount_count)
        
        if amount_to_be_used > amount_used:
            await modify_linked_quest_amount_submitted(linked_quest, amount_submitted + amount_used)
            
            inventory.modify_item_amount(item, -amount_used_count)
            await save_inventory(inventory)
            
            components = build_linked_quest_submit_success_n_left_components(
                user_id,
                page_index,
                linked_quest.entry_id,
                item,
                amount_type,
                amount_submitted,
                amount_required,
                amount_used,
            )
            new_message = False
            break
        
        user_balance = await get_user_balance(user_id)
        user_balance.set('balance', user_balance.balance + linked_quest.reward_balance)
        await user_balance.save()
        
        reward_credibility = linked_quest.reward_credibility
        
        user_stats = await get_user_stats(user_id)
        user_adventurer_rank_info = get_user_adventurer_rank_info(user_stats.credibility)
        user_reward_credibility = max(reward_credibility - user_adventurer_rank_info.level, 0)
        if user_reward_credibility:
            user_stats.set('credibility', user_stats.credibility + user_reward_credibility)
            await user_stats.save()
        
        guild_stats = await get_guild_stats(event.guild_id)
        guild_adventurer_rank_info = get_guild_adventurer_rank_info(guild_stats.credibility)
        guild_reward_credibility = max(reward_credibility - guild_adventurer_rank_info.level, 0)
        if guild_reward_credibility:
            guild_stats.set('credibility', guild_stats.credibility + guild_reward_credibility)
            await guild_stats.save()
        
        inventory.modify_item_amount(item, -amount_used_count)
        await save_inventory(inventory)
        
        await delete_linked_quest(linked_quest)
        
        components = build_linked_quest_submit_success_completed_components(
            user_id,
            page_index,
            event.guild_id,
            item,
            amount_type,
            amount_required,
            amount_used,
            linked_quest.reward_balance,
            user_reward_credibility,
        )
        new_message = False
        break
    
    
    if new_message:
        await client.interaction_followup_message_create(
            event,
            components = components,
            show_for_invoking_user_only = True,
        )
    else:
        await client.interaction_response_message_edit(
            event,
            components = components,
        )


@FEATURE_CLIENTS.interactions(custom_id = CUSTOM_ID_LINKED_QUEST_ABANDON_PATTERN)
async def linked_quest_abandon(client, event, user_id, page_index, linked_quest_entry_id):
    """
    Handles a user linked quest's abandoning component interaction.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the interaction.
    
    event : ``InteractionEvent``
        The received interaction event.
    
    user_id : `str`
        The invoking user's identifier as hexadecimal number.
    
    page_index : `str`
        The page's identifier as hexadecimal number.
    
    linked_quest_entry_id : `int`
        The linked quest's entries identifier in the database.
    """
    try:
        user_id = int(user_id, 16)
        page_index = int(page_index, 16)
        linked_quest_entry_id = int(linked_quest_entry_id, 16)
    except ValueError:
        return
    
    if user_id != event.user_id:
        return
    
    await client.interaction_component_acknowledge(event)
    
    while True:
        linked_quest_listing = await get_linked_quest_listing(user_id)
        linked_quest = get_linked_quest_with_entry_id(linked_quest_listing, linked_quest_entry_id)
        
        if (linked_quest is None):
            components = build_linked_quest_failure_no_such_quest_components()
            new_message = True
            break
        
        await delete_linked_quest(linked_quest)
        
        user_stats = await get_user_stats(user_id)
        user_adventurer_rank_info = get_user_adventurer_rank_info(user_stats.credibility)
        user_reward_credibility = linked_quest.reward_credibility + user_adventurer_rank_info.level
        if user_reward_credibility:
            user_stats.set('credibility', max(user_stats.credibility - user_reward_credibility, 0))
            await user_stats.save()
            
        components = build_linked_quest_abandon_success_components(user_id, page_index, event.guild_id)
        new_message = False
        break
    
    
    if new_message:
        await client.interaction_followup_message_create(
            event,
            components = components,
            show_for_invoking_user_only = True,
        )
    else:
        await client.interaction_response_message_edit(
            event,
            components = components,
        )


@FEATURE_CLIENTS.interactions(custom_id = CUSTOM_ID_QUEST_BOARD_ITEM_PATTERN)
async def quest_board_item(client, event, user_id, page_index, quest_template_id, item_id):
    """
    Handles a quest board item component interaction.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the interaction.
    
    event : ``InteractionEvent``
        The received interaction event.
    
    user_id : `str`
        The invoking user's identifier as hexadecimal number.
    
    page_index : `str`
        The quest board's current page's index as hexadecimal number.
    
    quest_template_id : `str`
        The quest's template identifier as hexadecimal number.
    
    item_id : `str`
        The item's identifier to show as hexadecimal number.
    """
    try:
        user_id = int(user_id, 16)
        page_index = int(page_index, 16)
        quest_template_id = int(quest_template_id, 16)
        item_id = int(item_id, 16)
    except ValueError:
        return
    
    if user_id != event.user_id:
        return
    
    components = build_quest_board_item_components(user_id, page_index, quest_template_id, item_id)
    
    await client.interaction_component_message_edit(
        event,
        components = components,
    )


@FEATURE_CLIENTS.interactions(custom_id = CUSTOM_ID_LINKED_QUEST_ITEM_PATTERN)
async def linked_quest_item(client, event, user_id, page_index, linked_quest_entry_id, item_id):
    """
    Handles a linked quest item component interaction.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the interaction.
    
    event : ``InteractionEvent``
        The received interaction event.
    
    user_id : `str`
        The invoking user's identifier as hexadecimal number.
    
    page_index : `str`
        The quest board's current page's index as hexadecimal number.
    
    linked_quest_entry_id : `str`
        The currently selected quest's entry's identifier  as hexadecimal number.
    
    item_id : `str`
        The item's identifier to show as hexadecimal number.
    """
    try:
        user_id = int(user_id, 16)
        page_index = int(page_index, 16)
        linked_quest_entry_id = int(linked_quest_entry_id, 16)
        item_id = int(item_id, 16)
    except ValueError:
        return
    
    if user_id != event.user_id:
        return
    
    components = build_linked_quest_item_components(user_id, page_index, linked_quest_entry_id, item_id)
    
    await client.interaction_component_message_edit(
        event,
        components = components,
    )
