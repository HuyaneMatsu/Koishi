__all__ = ()

from hata import Permission, ClientUserBase

from ...bot_utils.constants import GUILD__SUPPORT
from ...bots import FEATURE_CLIENTS

from ..user_balance import get_user_balance

from .embed_builders import build_success_embed


@FEATURE_CLIENTS.interactions(
    guild = GUILD__SUPPORT,
    required_permissions = Permission().update_by_keys(administrator = True),
)
async def take(
    client,
    interaction_event,
    target_user: (ClientUserBase, 'From who do you want to take hearts away?'),
    amount: (int, 'How much hearts do you want to take away?'),
):
    """
    Takes away hearts form the lucky user.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``InteractionResponse``
        The client who received this interaction.
    
    interaction_event : ``InteractionEvent``
        The received interaction event.
    
    target_user : ``ClientUserBase``
        The user to take away hearst from.
    
    amount : `int`
        The amount to take away.
    """
    if not interaction_event.user_permissions.administrator:
        await client.interaction_response_message_create(
            interaction_event,
            'You must have administrator permission to invoke this command.',
            show_for_invoking_user_only = True
        )
        return
    
    if amount <= 0:
        await client.interaction_response_message_create(
            interaction_event,
            f'You have to take away at least 1 heart.',
            show_for_invoking_user_only = True
        )
        return
    
    await client.interaction_application_command_acknowledge(
        interaction_event,
        False,
    )
    
    user_balance = await get_user_balance(target_user.id)
    
    balance = target_user.balance
    amount = min(balance - user_balance.allocated, amount)
    
    if amount:
        user_balance.set('balance', balance - amount)
        await user_balance.save()
    
    await client.interaction_response_message_edit(
        interaction_event,
        embed = build_success_embed(target_user, interaction_event.guild_id, balance, amount),
    )
