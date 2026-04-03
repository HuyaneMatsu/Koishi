__all__ = ()

from hata import Permission, ClientUserBase
from hata.ext.slash import P

from ...bot_utils.constants import EMOJI__HEART_CURRENCY, GUILD__SUPPORT
from ...bot_utils.utils import send_embed_to
from ...bots import FEATURE_CLIENTS

from ..user_balance import get_user_balance, save_user_balance
from ..user_settings import get_one_user_settings, get_preferred_client_for_user

from .embed_builders import build_notification_embed, build_success_embed


@FEATURE_CLIENTS.interactions(
    guild = GUILD__SUPPORT,
    required_permissions = Permission().update_by_keys(administrator = True),
)
async def award(
    client,
    interaction_event,
    target_user: (ClientUserBase, 'Who do you want to award?'),
    amount: (int, 'With how much hearts do you wanna award them?'),
    message : P(str, 'Optional message to send with the gift.', min_length = 0, max_length = 1000) = None,
):
    """
    Awards the user with hearts.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``InteractionResponse``
        The client who received this interaction.
    
    target_user : ``ClientUserBase``
        The user to gift.
    
    interaction_event : ``InteractionEvent``
        The received interaction event.
    
    amount : `int`
        The amount to gift.
    
    message : `None | str` = `None`, Optional
        Message to include with the award.
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
            f'You have to award at least 1 {EMOJI__HEART_CURRENCY}.',
            show_for_invoking_user_only = True
        )
        return
    
    await client.interaction_application_command_acknowledge(
        interaction_event,
        False,
    )
    
    user_balance = await get_user_balance(target_user.id)
    balance = user_balance.balance
    user_balance.modify_balance_by(amount)
    await save_user_balance(user_balance)
    
    await client.interaction_response_message_edit(
        interaction_event,
        embed = build_success_embed(target_user, interaction_event.guild_id, balance, amount, message),
    )
    
    if target_user.bot:
        return
    
    target_user_settings = await get_one_user_settings(target_user.id)
    
    await send_embed_to(
        get_preferred_client_for_user(target_user, target_user_settings.preferred_client_id, client),
        target_user.id,
        build_notification_embed(
            interaction_event.user, interaction_event.guild_id, balance, amount, message,
        ),
        None,
    )
