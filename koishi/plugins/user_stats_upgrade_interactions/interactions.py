__all__ = (
    'stat_upgrade_invoke_other_question', 'stat_upgrade_invoke_self_question',
)

from hata import InteractionType
from hata.ext.slash import InteractionAbortedError, InteractionResponse

from ...bot_utils.user_getter import get_user
from ...bot_utils.utils import send_embed_to
from ...bots import FEATURE_CLIENTS

from ..gift_common import check_can_gift
from ..relationships_core import deepen_and_boost_relationship, get_relationship_to_deepen
from ..user_stats_core import get_user_stat_value_for_index, get_user_stats, set_user_stat_value_for_index
from ..user_stats_upgrade_core import (
    CUSTOM_ID_STAT_UPGRADE_PURCHASE_CANCEL_OTHER_PATTERN, CUSTOM_ID_STAT_UPGRADE_PURCHASE_CANCEL_SELF_PATTERN,
    CUSTOM_ID_STAT_UPGRADE_PURCHASE_CONFIRM_OTHER_PATTERN, CUSTOM_ID_STAT_UPGRADE_PURCHASE_CONFIRM_SELF_PATTERN,
    build_component_question_stat_upgrade_purchase_other, build_component_question_stat_upgrade_purchase_self,
    calculate_stat_upgrade_cost
)
from ..user_balance import get_user_balance, get_user_balances
from ..user_settings import get_one_user_settings, get_preferred_client_for_user

from .checks import check_sufficient_available_balance_other, check_sufficient_available_balance_self
from .embed_builders import (
    build_notification_embed_other, build_question_embed_purchase_confirmation_other,
    build_question_embed_purchase_confirmation_self, build_success_embed_purchase_cancelled,
    build_success_embed_purchase_completed_other, build_success_embed_purchase_completed_self
)


async def stat_upgrade_invoke_self_question(client, event, stat_index):
    """
    Questions whether the user really wanna upgrade a stat of their.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the interaction.
    
    event : ``InteractionEvent``
        The received interaction event.
    
    stat_index : `int`
        The stat's index.
    """
    if event.type is InteractionType.application_command:
        await client.interaction_application_command_acknowledge(event, False, show_for_invoking_user_only = True)
    
    user_id = event.user.id
    
    user_balance = await get_user_balance(user_id)
    stats = await get_user_stats(user_id)
    
    stat_value_after = get_user_stat_value_for_index(stats, stat_index) + 1
    required_balance = calculate_stat_upgrade_cost(
        stats.stat_housewife + stats.stat_cuteness + stats.stat_bedroom + stats.stat_charm + stats.stat_loyalty,
        stat_value_after,
    )
    check_sufficient_available_balance_self(
        required_balance, user_balance.balance - user_balance.allocated, stat_index, stat_value_after
    )
    
    await client.interaction_response_message_edit(
        event,
        embed = build_question_embed_purchase_confirmation_self(required_balance, stat_index, stat_value_after),
        components = build_component_question_stat_upgrade_purchase_self(stat_index),
    )


async def stat_upgrade_invoke_other_question(client, event, target_user, relationship_to_deepen, stat_index):
    """
    Questions whether the user really wanna upgrade a stat of someone else.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the interaction.
    
    event : ``InteractionEvent``
        The received interaction event.
    
    target_user : ``ClientUserBase``
        The targeted user.
    
    relationship_to_deepen : `None | Relationship`
        The relationship to deepen by the purchase.
    
    stat_index : `int`
        The stat's index.
    """
    if event.type is InteractionType.application_command:
        await client.interaction_application_command_acknowledge(event, False, show_for_invoking_user_only = True)
    
    source_user = event.user
    check_can_gift(source_user, relationship_to_deepen)
    
    source_user_balance = await get_user_balance(source_user.id)
    stats = await get_user_stats(target_user.id)
    
    stat_value_after = get_user_stat_value_for_index(stats, stat_index) + 1
    required_balance = calculate_stat_upgrade_cost(
        stats.stat_housewife + stats.stat_cuteness + stats.stat_bedroom + stats.stat_charm + stats.stat_loyalty,
        stat_value_after,
    )
    check_sufficient_available_balance_other(
        required_balance,
        source_user_balance.balance - source_user_balance.allocated,
        stat_index,
        stat_value_after,
        target_user,
        event.guild_id,
    )
    
    await client.interaction_response_message_edit(
        event,
        embed = build_question_embed_purchase_confirmation_other(
            required_balance, stat_index, stat_value_after, target_user, event.guild_id,
        ),
        components = build_component_question_stat_upgrade_purchase_other(target_user.id, stat_index),
    )


@FEATURE_CLIENTS.interactions(
    custom_id = [
        CUSTOM_ID_STAT_UPGRADE_PURCHASE_CANCEL_SELF_PATTERN,
        CUSTOM_ID_STAT_UPGRADE_PURCHASE_CANCEL_OTHER_PATTERN,
    ],
)
async def stat_upgrade_cancel(event):
    """
    Cancels the stat upgrade purchase.
    
    This function is a coroutine.
    
    Parameters
    ----------
    event : ``InteractionEvent``
        The received interaction event.
    
    Returns
    -------
    response : `None | InteractionEvent`
    """
    if event.message.interaction.user_id != event.user_id:
        return
    
    return InteractionResponse(
        embed = build_success_embed_purchase_cancelled(),
        components = None,
    )


@FEATURE_CLIENTS.interactions(custom_id = CUSTOM_ID_STAT_UPGRADE_PURCHASE_CONFIRM_SELF_PATTERN)
async def stat_upgrade_confirm_self(event, stat_index):
    """
    Confirms the stat upgrade for yourself.
    
    This function is a coroutine generator.
    
    Parameters
    ----------
    event : ``InteractionEvent``
        The received interaction event.
    
    stat_index : `str`
        The stat's index encoded as base 16.
    
    Yields
    -------
    acknowledge / response : `None | InteractionEvent`
    """
    user_id = event.user_id
    if event.message.interaction.user_id != user_id:
        return
    
    try:
        stat_index = int(stat_index, base = 16)
    except ValueError:
        return
    
    yield
    
    user_balance = await get_user_balance(user_id)
    stats = await get_user_stats(user_id)
    
    stat_value_after = get_user_stat_value_for_index(stats, stat_index) + 1
    required_balance = calculate_stat_upgrade_cost(
        stats.stat_housewife + stats.stat_cuteness + stats.stat_bedroom + stats.stat_charm + stats.stat_loyalty,
        stat_value_after,
    )
    
    balance = user_balance.balance
    try:
        check_sufficient_available_balance_self(
            required_balance,
            balance - user_balance.allocated,
            stat_index, stat_value_after,
        )
    except InteractionAbortedError as exception:
        exception.response.abort = False
        raise
    
    set_user_stat_value_for_index(stats, stat_index, stat_value_after)
    await stats.save()
    
    user_balance.set('balance', balance - required_balance)
    await deepen_and_boost_relationship(user_balance, None, None, required_balance, save_source_user_balance = 2)
    
    yield InteractionResponse(
        embed = build_success_embed_purchase_completed_self(balance, required_balance, stat_index, stat_value_after),
        components = None,
    )


@FEATURE_CLIENTS.interactions(custom_id = CUSTOM_ID_STAT_UPGRADE_PURCHASE_CONFIRM_OTHER_PATTERN)
async def stat_upgrade_confirm_other(client, event, target_user_id, stat_index):
    """
    Confirms stat upgrade purchase for someone else.
    
    This function is a coroutine generator.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    
    event : ``InteractionEvent``
        The received interaction event.
    
    target_user_id : `str`
        The targeted user's identifier encoded as base 16.
    
    stat_index : `str`
        The stat's index encoded as base 16.
    
    Yields
    -------
    acknowledge / response : `None | InteractionEvent`
    """
    source_user = event.user
    if event.message.interaction.user_id != source_user.id:
        return
    
    try:
        target_user_id = int(target_user_id, base = 16)
        stat_index = int(stat_index, base = 16)
    except ValueError:
        return
    
    yield
    
    target_user = await get_user(target_user_id)
    
    # Get relationship to increment its value if any.
    relationship_to_deepen = await get_relationship_to_deepen(source_user.id, target_user_id)
    
    try:
        check_can_gift(source_user, relationship_to_deepen)
    except InteractionAbortedError as exception:
        exception.response.abort = False
        raise
    
    user_balances = await get_user_balances((source_user.id, target_user_id))
    source_user_balance = user_balances[source_user.id]
    target_user_balance = user_balances[target_user_id]
    stats = await get_user_stats(target_user_id)
    
    
    stat_value_after = get_user_stat_value_for_index(stats, stat_index) + 1
    required_balance = calculate_stat_upgrade_cost(
        stats.stat_housewife + stats.stat_cuteness + stats.stat_bedroom + stats.stat_charm + stats.stat_loyalty,
        stat_value_after,
    )
    
    balance = source_user_balance.balance
    
    try:
        check_sufficient_available_balance_other(
            required_balance,
            balance - source_user_balance.allocated,
            stat_index,
            stat_value_after,
            target_user,
            event.guild_id,
        )
    except InteractionAbortedError as exception:
        exception.response.abort = False
        raise
    
    set_user_stat_value_for_index(stats, stat_index, stat_value_after)
    await stats.save()
    
    source_user_balance.set('balance', balance - required_balance)

    await deepen_and_boost_relationship(
        source_user_balance,
        target_user_balance,
        relationship_to_deepen,
        required_balance,
        save_source_user_balance = 2,
        save_target_user_balance = 2,
    )
    
    yield InteractionResponse(
        embed = build_success_embed_purchase_completed_other(
            balance, required_balance, stat_index, stat_value_after, target_user, event.guild_id
        ),
        components = None,
    )
    
    if not target_user.bot:
        target_user_settings = await get_one_user_settings(target_user.id)
        if target_user_settings.notification_gift:
            await send_embed_to(
                get_preferred_client_for_user(target_user, target_user_settings.preferred_client_id, client),
                target_user,
                build_notification_embed_other(stat_index, stat_value_after, source_user, event.guild_id),
            )
