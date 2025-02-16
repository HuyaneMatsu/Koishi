__all__ = (
    'relationship_slot_increment_invoke_other_question', 'relationship_slot_increment_invoke_self_question',
)

from math import floor

from hata.ext.slash import InteractionAbortedError, InteractionResponse

from ...bot_utils.constants import WAIFU_SLOT_COSTS, WAIFU_SLOT_COST_DEFAULT
from ...bot_utils.user_getter import get_user
from ...bot_utils.utils import send_embed_to
from ...bots import FEATURE_CLIENTS

from ..relationship_slots_core import (
    CUSTOM_ID_RELATIONSHIP_SLOT_PURCHASE_CANCEL_OTHER_PATTERN, CUSTOM_ID_RELATIONSHIP_SLOT_PURCHASE_CANCEL_SELF,
    CUSTOM_ID_RELATIONSHIP_SLOT_PURCHASE_CONFIRM_OTHER_PATTERN, CUSTOM_ID_RELATIONSHIP_SLOT_PURCHASE_CONFIRM_SELF,
    CUSTOM_ID_RELATIONSHIP_SLOT_PURCHASE_INVOKE_OTHER_PATTERN, CUSTOM_ID_RELATIONSHIP_SLOT_PURCHASE_INVOKE_SELF,
    build_component_question_relationship_slot_purchase_other, build_component_question_relationship_slot_purchase_self
)
from ..relationships_core import get_relationship_to_deepen
from ..user_balance import get_user_balance, get_user_balances
from ..user_settings import get_one_user_settings, get_preferred_client_for_user

from .checks import (
    check_max_relationship_slots_other, check_max_relationship_slots_self, check_sufficient_balance_other,
    check_sufficient_balance_self
)
from .embed_builders import (
    build_notification_embed_other, build_question_embed_purchase_confirmation_other,
    build_question_embed_purchase_confirmation_self, build_success_embed_purchase_cancelled,
    build_success_embed_purchase_completed_other, build_success_embed_purchase_completed_self
)


@FEATURE_CLIENTS.interactions(custom_id = CUSTOM_ID_RELATIONSHIP_SLOT_PURCHASE_INVOKE_SELF)
async def relationship_slot_increment_invoke_self(event):
    """
    Inline caller for buying a relationship slot for yourself.
    
    This function is a coroutine generator.
    
    Parameters
    ----------
    event : ``InteractionEvent``
        The received interaction event.
    
    Yields
    ------
    acknowledge / response : `None | InteractionEvent`
    """
    if event.message.interaction.user_id != event.user_id:
        return
    
    yield
    yield await relationship_slot_increment_invoke_self_question(event)


@FEATURE_CLIENTS.interactions(custom_id = CUSTOM_ID_RELATIONSHIP_SLOT_PURCHASE_INVOKE_OTHER_PATTERN)
async def relationship_slot_increment_invoke_other(event, target_user_id):
    """
    Inline caller for buying a relationship slot for someone else.
    
    This function is a coroutine generator.
    
    Parameters
    ----------
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
    yield await relationship_slot_increment_invoke_other_question(event, target_user)


async def relationship_slot_increment_invoke_self_question(event):
    """
    Questions whether the user really wanna increment their relationship slot count.
    
    This function is a coroutine.
    
    Parameters
    ----------
    event : ``InteractionEvent``
        The received interaction event.
    
    Yields
    ------
    response : ``InteractionResponse``
    """
    user_id = event.user.id
    
    user_balance = await get_user_balance(user_id)
    relationship_slots = user_balance.relationship_slots
    
    check_max_relationship_slots_self(relationship_slots)
    
    new_relationship_slot_count = relationship_slots + 1
    required_balance = WAIFU_SLOT_COSTS.get(new_relationship_slot_count, WAIFU_SLOT_COST_DEFAULT)
    available_balance = user_balance.balance - user_balance.allocated
    
    check_sufficient_balance_self(required_balance, available_balance, new_relationship_slot_count)
    
    return InteractionResponse(
        embed = build_question_embed_purchase_confirmation_self(required_balance, new_relationship_slot_count),
        components = build_component_question_relationship_slot_purchase_self(),
    )


async def relationship_slot_increment_invoke_other_question(event, target_user):
    """
    Questions whether the user really wanna increment someone else's relationship slot count.
    
    This function is a coroutine.
    
    Parameters
    ----------
    event : ``InteractionEvent``
        The received interaction event.
    
    target_user : ``ClientUserBase``
        The targeted user.
    
    Returns
    -------
    response : ``InteractionResponse``
    """
    source_user_id = event.user.id
    
    target_user_balance = await get_user_balance(target_user.id)
    relationship_slots = target_user_balance.relationship_slots
    
    check_max_relationship_slots_other(relationship_slots, target_user, event.guild_id)
    
    source_user_balance = await get_user_balance(source_user_id)
    new_relationship_slot_count = relationship_slots + 1
    required_balance = WAIFU_SLOT_COSTS.get(new_relationship_slot_count, WAIFU_SLOT_COST_DEFAULT)
    available_balance = source_user_balance.balance - source_user_balance.allocated
    
    check_sufficient_balance_other(
        required_balance, available_balance, new_relationship_slot_count, target_user, event.guild_id
    )
    
    return InteractionResponse(
        embed = build_question_embed_purchase_confirmation_other(
            required_balance, new_relationship_slot_count, target_user, event.guild_id,
        ),
        components = build_component_question_relationship_slot_purchase_other(target_user.id),
    )


@FEATURE_CLIENTS.interactions(
    custom_id = [
        CUSTOM_ID_RELATIONSHIP_SLOT_PURCHASE_CANCEL_SELF,
        CUSTOM_ID_RELATIONSHIP_SLOT_PURCHASE_CANCEL_OTHER_PATTERN,
    ],
)
async def relationship_slot_increment_cancel(event):
    """
    Cancels buying the relationship slot.
    
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


@FEATURE_CLIENTS.interactions(custom_id = CUSTOM_ID_RELATIONSHIP_SLOT_PURCHASE_CONFIRM_SELF)
async def relationship_slot_increment_confirm_self(event):
    """
    Confirms a relationship slot increment purchase for yourself.
    
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
    relationship_slots = user_balance.relationship_slots
    
    try:
        check_max_relationship_slots_self(relationship_slots)
    except InteractionAbortedError as exception:
        exception.response.abort = False
        raise
    
    new_relationship_slot_count = relationship_slots + 1
    required_balance = WAIFU_SLOT_COSTS.get(new_relationship_slot_count, WAIFU_SLOT_COST_DEFAULT)
    available_balance = user_balance.balance - user_balance.allocated
    
    
    try:
        check_sufficient_balance_self(required_balance, available_balance, new_relationship_slot_count)
    except InteractionAbortedError as exception:
        exception.response.abort = False
        raise
    
    user_balance.set('balance', user_balance.balance - required_balance)
    user_balance.set('relationship_slots', new_relationship_slot_count)
    await user_balance.save()
    
    yield InteractionResponse(
        embed = build_success_embed_purchase_completed_self(required_balance, new_relationship_slot_count),
        components = None,
    )


@FEATURE_CLIENTS.interactions(custom_id = CUSTOM_ID_RELATIONSHIP_SLOT_PURCHASE_CONFIRM_OTHER_PATTERN)
async def relationship_slot_increment_confirm_other(client, event, target_user_id):
    """
    Confirms a relationship slot increment purchase for someone else.
    
    This function is a coroutine generator.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    
    event : ``InteractionEvent``
        The received interaction event.
    
    target_user_id : `int`
        The targeted user's identifier.
    
    Yields
    -------
    acknowledge / response : `None | InteractionEvent`
    """
    source_user_id = event.user_id
    if event.message.interaction.user_id != source_user_id:
        return
    
    try:
        target_user_id = int(target_user_id, base = 16)
    except ValueError:
        return
    
    yield
    
    target_user = await get_user(target_user_id)
    
    # Get relationship to increment its value if any.
    relationship = await get_relationship_to_deepen(source_user_id, target_user_id)
    
    user_balances = await get_user_balances((source_user_id, target_user_id))
    source_user_balance = user_balances[source_user_id]
    target_user_balance = user_balances[target_user_id]
    
    relationship_slots = target_user_balance.relationship_slots
    
    try:
        check_max_relationship_slots_other(relationship_slots, target_user, event.guild_id)
    except InteractionAbortedError as exception:
        exception.response.abort = False
        raise
    
    new_relationship_slot_count = relationship_slots + 1
    required_balance = WAIFU_SLOT_COSTS.get(new_relationship_slot_count, WAIFU_SLOT_COST_DEFAULT)
    available_balance = source_user_balance.balance - source_user_balance.allocated
    
    try:
        check_sufficient_balance_other(
            required_balance, available_balance, new_relationship_slot_count, target_user, event.guild_id
        )
    except InteractionAbortedError as exception:
        exception.response.abort = False
        raise
    
    source_user_balance.set('balance', source_user_balance.balance - required_balance)
    target_user_balance.set('relationship_slots', new_relationship_slot_count)
    await source_user_balance.save()
    await target_user_balance.save()
    
    
    if (relationship is not None):
        relationship_investment_increase = floor(required_balance * 0.01)
        if relationship.source_user_id == source_user_id:
            relationship.set('source_investment', relationship.source_investment + relationship_investment_increase)
        else:
            relationship.set('target_investment', relationship.target_investment + relationship_investment_increase)
    
    
    yield InteractionResponse(
        embed = build_success_embed_purchase_completed_other(
            required_balance, new_relationship_slot_count, target_user, event.guild_id
        ),
        components = None,
    )
    
    if not target_user.bot:
        target_user_settings = await get_one_user_settings(target_user.id)
        if target_user_settings.notification_gift:
            await send_embed_to(
                get_preferred_client_for_user(target_user, target_user_settings.preferred_client_id, client),
                target_user,
                build_notification_embed_other(new_relationship_slot_count, event.user, event.guild_id),
            )
