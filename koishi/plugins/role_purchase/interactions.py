__all__ = ('purchase_role_other', 'purchase_role_self',)

from hata import DiscordException, ERROR_CODES
from hata.ext.slash import abort

from ...bot_utils.utils import send_embed_to
from ...bots import MAIN_CLIENT

from ..user_balance import get_user_balance
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
    available_balance = user_balance.balance - max(user_balance.allocated, 0)
    
    check_insufficient_available_balance(role, available_balance, required_balance)
    success = await _add_role(target_user, role)
    if not success:
        abort(
            embed = build_failure_embed_not_in_guild_self(role)
        )
    
    balance = user_balance.balance
    user_balance.set('balance', balance - required_balance)
    await user_balance.save()
    
    await client.interaction_response_message_edit(
        event,
        embed = build_success_embed_self(role, balance, required_balance)
    )


async def purchase_role_other(client, event, role, required_balance, target_user):
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
    
    Raises
    ------
    InteractionAbortedError
    """
    check_has_role_other(role, target_user, event.guild_id)
    check_not_in_guild_other(role, target_user, event.guild_id)
    
    await client.interaction_application_command_acknowledge(event, False, show_for_invoking_user_only = True)
    
    user_balance = await get_user_balance(event.user_id)
    available_balance = user_balance.balance - max(user_balance.allocated, 0)
    
    check_insufficient_available_balance(role, available_balance, required_balance)
    success = await _add_role(target_user, role)
    if not success:
        abort(
            embed = build_failure_embed_not_in_guild_other(role, target_user, event.guild_id)
        )
    
    balance = user_balance.balance
    user_balance.set('balance', balance - required_balance)
    await user_balance.save()
    
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
