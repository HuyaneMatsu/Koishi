__all__ = ('purchase_role_other', 'purchase_role_self',)

from hata import DiscordException, ERROR_CODES
from hata.ext.slash import abort

from ...bot_utils.utils import send_embed_to
from ...bots import MAIN_CLIENT

from ..gift_common import check_can_gift
from ..relationships_core import deepen_and_boost_relationship
from ..user_balance import get_user_balance, get_user_balances, save_user_balance
from ..user_settings import get_one_user_settings, get_preferred_client_for_user

from .checks import (
    check_has_role_other, check_has_role_self, check_insufficient_available_balance, check_not_in_guild_other,
    check_not_in_guild_self
)
from .embed_builders import (
    build_failure_embed_not_in_guild_other, build_failure_embed_not_in_guild_self, build_notification_embed_other,
    build_success_embed_other, build_success_embed_self
)


async def _add_role(target_user, role):
    """
    Adds a role to the targeted user.
    
    This function is a coroutine.
    
    Parameters
    ----------
    target_user : ``ClientUserBase``
        The user to add role to.
    
    role : ``Role``
        The role to add.
    
    Returns
    -------
    success : `bool`
    """
    try:
        await MAIN_CLIENT.user_role_add(target_user, role)
    except DiscordException as err:
        if err.code in (
            ERROR_CODES.unknown_user,
            ERROR_CODES.unknown_member,
        ):
            success = False
        
        else:
            raise
    
    else:
        success = True
    
    return success


async def purchase_role_self(client, event, role, required_balance):
    """
    Purchases a role for the user.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the interaction.
    
    event : ``InteractionEvent``
        The received interaction event.
    
    role : ``Role``
        The role to be purchased.
    
    required_balance : `int`
        The required balance to purchase the role.
    
    Raises
    ------
    InteractionAbortedError
    """
    target_user = event.user
    
    check_has_role_self(role, target_user)
    check_not_in_guild_self(role, target_user)
    
    await client.interaction_application_command_acknowledge(event, False, show_for_invoking_user_only = True)
    
    user_balance = await get_user_balance(event.user_id)
    available_balance = user_balance.balance - user_balance.get_cumulative_allocated_balance()
    
    check_insufficient_available_balance(role, available_balance, required_balance)
    success = await _add_role(target_user, role)
    if not success:
        abort(
            embed = build_failure_embed_not_in_guild_self(role)
        )
    
    balance = user_balance.balance
    user_balance.modify_balance_by(-required_balance)
    
    await deepen_and_boost_relationship(user_balance, None, None, required_balance, save_source_user_balance = 2)
    
    await client.interaction_response_message_edit(
        event,
        embed = build_success_embed_self(role, balance, required_balance)
    )


async def purchase_role_other(client, event, role, required_balance, target_user, relationship_to_deepen):
    """
    Purchases a role for an other user.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the interaction.
    
    event : ``InteractionEvent``
        The received interaction event.
    
    role : ``Role``
        The role to be purchased.
    
    required_balance : `int`
        The required balance to purchase the role.
    
    target_user : ``ClientUserBase``
        The user to buy the role for.
    
    relationship_to_deepen : `None | Relationship`
        The relationship to deepen by the purchase.
    
    Raises
    ------
    InteractionAbortedError
    """
    await client.interaction_application_command_acknowledge(event, False, show_for_invoking_user_only = True)
    
    source_user = event.user
    check_can_gift(source_user, relationship_to_deepen)
    check_has_role_other(role, target_user, event.guild_id)
    check_not_in_guild_other(role, target_user, event.guild_id)
    
    user_balances = await get_user_balances((source_user.id, target_user.id))
    source_user_balance = user_balances[source_user.id]
    target_user_balance = user_balances[target_user.id]
    
    available_balance = source_user_balance.balance - source_user_balance.get_cumulative_allocated_balance()
    
    check_insufficient_available_balance(role, available_balance, required_balance)
    success = await _add_role(target_user, role)
    if not success:
        abort(
            embed = build_failure_embed_not_in_guild_other(role, target_user, event.guild_id)
        )
    
    balance = source_user_balance.balance
    source_user_balance.modify_relationship_value_by(-required_balance)
    await save_user_balance(source_user_balance)
    
    await deepen_and_boost_relationship(
        source_user_balance,
        target_user_balance,
        relationship_to_deepen,
        required_balance,
        save_source_user_balance = 2,
    )
    
    await client.interaction_response_message_edit(
        event,
        embed = build_success_embed_other(role, balance, required_balance, target_user, event.guild_id)
    )
    
    if not target_user.bot:
        target_user_settings = await get_one_user_settings(target_user.id)
        if target_user_settings.notification_gift:
            await send_embed_to(
                get_preferred_client_for_user(target_user, target_user_settings.preferred_client_id, client),
                target_user,
                build_notification_embed_other(role, event.user, event.guild_id),
            )
