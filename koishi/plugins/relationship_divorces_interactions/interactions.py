__all__ = (
    'relationship_divorces_decrement_invoke_other_question', 'relationship_divorces_decrement_invoke_self_question',
)

from hata.ext.slash import InteractionAbortedError, InteractionResponse

from ...bot_utils.user_getter import get_user
from ...bot_utils.utils import send_embed_to
from ...bots import FEATURE_CLIENTS

from ..gift_common import check_can_gift
from ..relationship_divorces_core import (
    CUSTOM_ID_RELATIONSHIP_DIVORCES_DECREMENT_PURCHASE_CANCEL_OTHER_PATTERN,
    CUSTOM_ID_RELATIONSHIP_DIVORCES_DECREMENT_PURCHASE_CANCEL_SELF,
    CUSTOM_ID_RELATIONSHIP_DIVORCES_DECREMENT_PURCHASE_CONFIRM_OTHER_PATTERN,
    CUSTOM_ID_RELATIONSHIP_DIVORCES_DECREMENT_PURCHASE_CONFIRM_SELF,
    CUSTOM_ID_RELATIONSHIP_DIVORCES_DECREMENT_PURCHASE_INVOKE_OTHER_PATTERN,
    CUSTOM_ID_RELATIONSHIP_DIVORCES_DECREMENT_PURCHASE_INVOKE_SELF,
    build_component_question_relationship_divorces_decrement_purchase_other,
    build_component_question_relationship_divorces_decrement_purchase_self,
    get_relationship_divorce_reduction_required_balance
)
from ..relationships_core import deepen_and_boost_relationship, get_relationship_to_deepen
from ..user_balance import get_user_balance, get_user_balances
from ..user_settings import get_one_user_settings, get_preferred_client_for_user

from .checks import (
    check_no_relationship_divorces_other, check_no_relationship_divorces_self, check_sufficient_balance_other,
    check_sufficient_balance_self
)
from .embed_builders import (
    build_notification_embed_other, build_question_embed_purchase_confirmation_other,
    build_question_embed_purchase_confirmation_self, build_success_embed_purchase_cancelled,
    build_success_embed_purchase_completed_other, build_success_embed_purchase_completed_self
)


@FEATURE_CLIENTS.interactions(custom_id = CUSTOM_ID_RELATIONSHIP_DIVORCES_DECREMENT_PURCHASE_INVOKE_SELF)
async def relationship_divorces_decrement_invoke_self(client, event):
    """
    Inline caller for hiring ninjas to locate ad burn your relationship divorce papers.
    
    This function is a coroutine generator.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the interaction.
    
    event : ``InteractionEvent``
        The received interaction event.
    
    Yields
    ------
    acknowledge / response : `None | InteractionEvent`
    """
    if event.message.interaction.user_id != event.user_id:
        return
    
    yield
    yield await relationship_divorces_decrement_invoke_self_question(client, event)


@FEATURE_CLIENTS.interactions(custom_id = CUSTOM_ID_RELATIONSHIP_DIVORCES_DECREMENT_PURCHASE_INVOKE_OTHER_PATTERN)
async def relationship_divorces_decrement_invoke_other(client, event, target_user_id):
    """
    Inline caller for hiring ninjas to locate and burn the relationship divorce papers of someone else.
    
    This function is a coroutine generator.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the interaction.
    
    event : ``InteractionEvent``
        The received interaction event.
    
    target_user_id : `str`
        The targeted user's identifier. Converted to int.
    
    Yields
    ------
    acknowledge / response : `None | InteractionEvent`
    """
    if event.message.interaction.user_id != event.user_id:
        return
    
    try:
        target_user_id = int(target_user_id, base = 16)
    except ValueError:
        return
    
    yield
    target_user = await get_user(target_user_id)
    yield await relationship_divorces_decrement_invoke_other_question(client, event, target_user, None)


async def relationship_divorces_decrement_invoke_self_question(client, event):
    """
    Questions whether the user really wanna hire ninjas to locate and burn their relationship divorce papers.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the interaction.
    
    event : ``InteractionEvent``
        The received interaction event.
    """
    await client.interaction_application_command_acknowledge(event, False, show_for_invoking_user_only = True)
    
    user_id = event.user.id
    
    user_balance = await get_user_balance(user_id)
    relationship_divorces = user_balance.relationship_divorces
    
    check_no_relationship_divorces_self(relationship_divorces)
    
    required_balance = get_relationship_divorce_reduction_required_balance(user_id, relationship_divorces)
    available_balance = user_balance.balance - user_balance.get_cumulative_allocated_balance()
    
    check_sufficient_balance_self(required_balance, available_balance, relationship_divorces)
    
    await client.interaction_response_message_edit(
        event,
        embed = build_question_embed_purchase_confirmation_self(required_balance, relationship_divorces),
        components = build_component_question_relationship_divorces_decrement_purchase_self(),
    )


async def relationship_divorces_decrement_invoke_other_question(client, event, target_user, relationship_to_deepen):
    """
    Questions whether the user really wanna hire ninjas to locate and burn someone else's relationship divorce paper.
    
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
    """
    await client.interaction_application_command_acknowledge(event, False, show_for_invoking_user_only = True)
    
    source_user = event.user
    check_can_gift(source_user, relationship_to_deepen)
    
    target_user_balance = await get_user_balance(target_user.id)
    relationship_divorces = target_user_balance.relationship_divorces
    
    check_no_relationship_divorces_other(relationship_divorces, target_user, event.guild_id)
    
    source_user_balance = await get_user_balance(source_user.id)
    
    required_balance = get_relationship_divorce_reduction_required_balance(target_user.id, relationship_divorces)
    available_balance = source_user_balance.balance - source_user_balance.get_cumulative_allocated_balance()
    
    check_sufficient_balance_other(
        required_balance, available_balance, relationship_divorces, target_user, event.guild_id
    )
    
    await client.interaction_response_message_edit(
        event,
        embed = build_question_embed_purchase_confirmation_other(
            required_balance, relationship_divorces, target_user, event.guild_id,
        ),
        components = build_component_question_relationship_divorces_decrement_purchase_other(target_user.id),
    )


@FEATURE_CLIENTS.interactions(
    custom_id = [
        CUSTOM_ID_RELATIONSHIP_DIVORCES_DECREMENT_PURCHASE_CANCEL_SELF,
        CUSTOM_ID_RELATIONSHIP_DIVORCES_DECREMENT_PURCHASE_CANCEL_OTHER_PATTERN,
    ],
)
async def relationship_divorces_decrement_cancel(event):
    """
    Cancels hiring ninjas to locate and burning the relationship divorces.
    
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


@FEATURE_CLIENTS.interactions(custom_id = CUSTOM_ID_RELATIONSHIP_DIVORCES_DECREMENT_PURCHASE_CONFIRM_SELF)
async def relationship_divorces_decrement_confirm_self(event):
    """
    Confirms hiring ninjas to locate and burn the relationship divorce papers of yourself.
    
    This function is a coroutine generator.
    
    Parameters
    ----------
    event : ``InteractionEvent``
        The received interaction event.
    
    Yields
    -------
    acknowledge / response : `None | InteractionEvent`
    """
    user_id = event.user_id
    if event.message.interaction.user_id != user_id:
        return
    
    yield
    
    user_balance = await get_user_balance(user_id)
    relationship_divorces = user_balance.relationship_divorces
    
    try:
        check_no_relationship_divorces_self(relationship_divorces)
    except InteractionAbortedError as exception:
        exception.response.abort = False
        raise
    
    required_balance = get_relationship_divorce_reduction_required_balance(user_id, relationship_divorces)
    available_balance = user_balance.balance - user_balance.get_cumulative_allocated_balance()
    
    
    try:
        check_sufficient_balance_self(required_balance, available_balance, relationship_divorces)
    except InteractionAbortedError as exception:
        exception.response.abort = False
        raise
    
    user_balance.modify_balance_by(-required_balance)
    user_balance.decrement_relationship_divorces()
    
    await deepen_and_boost_relationship(user_balance, None, None, required_balance, save_source_user_balance = 2)
    
    yield InteractionResponse(
        embed = build_success_embed_purchase_completed_self(required_balance, relationship_divorces),
        components = None,
    )


@FEATURE_CLIENTS.interactions(custom_id = CUSTOM_ID_RELATIONSHIP_DIVORCES_DECREMENT_PURCHASE_CONFIRM_OTHER_PATTERN)
async def relationship_divorces_decrement_confirm_other(client, event, target_user_id):
    """
    Confirms hiring ninjas to locate and burn the relationship divorce papers of someone else.
    
    This function is a coroutine generator.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    
    event : ``InteractionEvent``
        The received interaction event.
    
    target_user_id : `str`
        The targeted user's identifier encoded as base 16.
    
    Yields
    -------
    acknowledge / response : `None | InteractionEvent`
    """
    source_user = event.user
    if event.message.interaction.user_id != source_user.id:
        return
    
    try:
        target_user_id = int(target_user_id, base = 16)
    except ValueError:
        return
    
    yield
    
    target_user = await get_user(target_user_id)
    
    # Get relationship to decrement its value if any.
    relationship_to_deepen = await get_relationship_to_deepen(source_user.id, target_user_id)
    
    try:
        check_can_gift(source_user, relationship_to_deepen)
    except InteractionAbortedError as exception:
        exception.response.abort = False
        raise
    
    user_balances = await get_user_balances((source_user.id, target_user_id))
    source_user_balance = user_balances[source_user.id]
    target_user_balance = user_balances[target_user_id]
    
    relationship_divorces = target_user_balance.relationship_divorces
    
    try:
        check_no_relationship_divorces_other(relationship_divorces, target_user, event.guild_id)
    except InteractionAbortedError as exception:
        exception.response.abort = False
        raise
    
    required_balance = get_relationship_divorce_reduction_required_balance(target_user.id, relationship_divorces)
    available_balance = source_user_balance.balance - source_user_balance.get_cumulative_allocated_balance()
    
    try:
        check_sufficient_balance_other(
            required_balance, available_balance, relationship_divorces, target_user, event.guild_id
        )
    except InteractionAbortedError as exception:
        exception.response.abort = False
        raise
    
    source_user_balance.modify_balance_by(-required_balance)
    target_user_balance.decrement_relationship_divorces()
    
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
            required_balance, relationship_divorces, target_user, event.guild_id
        ),
        components = None,
    )
    
    if not target_user.bot:
        target_user_settings = await get_one_user_settings(target_user.id)
        if target_user_settings.notification_gift:
            await send_embed_to(
                get_preferred_client_for_user(target_user, target_user_settings.preferred_client_id, client),
                target_user,
                build_notification_embed_other(relationship_divorces, source_user, event.guild_id),
            )
