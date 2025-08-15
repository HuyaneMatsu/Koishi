__all__ = ()

from datetime import datetime as DateTime, timezone as TimeZone

from hata import Permission, ClientUserBase
from hata.ext.slash import P

from ...bot_utils.constants import EMOJI__HEART_CURRENCY, GUILD__SUPPORT
from ...bot_utils.daily import calculate_daily_new
from ...bot_utils.utils import send_embed_to
from ...bots import FEATURE_CLIENTS

from ..user_balance import get_user_balance
from ..user_settings import get_one_user_settings, get_preferred_client_for_user

from .embed_builders import build_notification_embed, build_success_embed
from .constants import AWARD_TYPES, AWARD_TYPE_BALANCE


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
    with_: (AWARD_TYPES, 'Select award type') = AWARD_TYPE_BALANCE,
):
    """
    Awards the user with hearts or streak.
    
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
    
    with_ : `str` = `AWARD_TYPE_BALANCE`, Optional
        What to award the user with.
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
            f'You have to award at least 1 {with_}.',
            show_for_invoking_user_only = True
        )
        return
    
    await client.interaction_application_command_acknowledge(
        interaction_event,
        False,
    )
    
    target_user_balance = await get_user_balance(target_user.id)
    target_balance = target_user_balance.balance
    target_streak = target_user_balance.streak
    target_daily_can_claim_at = target_user_balance.daily_can_claim_at
    
    if with_ == AWARD_TYPE_BALANCE:
        target_new_balance = target_balance + amount
        target_new_streak = target_streak
    else:
        now = DateTime.now(TimeZone.utc)
        target_new_balance = target_user_balance.balance
        target_new_streak, target_daily_can_claim_at = calculate_daily_new(
            target_streak, 
            target_daily_can_claim_at,
            now,
        )
        
        target_new_streak = target_streak + amount
    
    target_user_balance.set('balance', target_new_balance)
    target_user_balance.set('streak', target_new_streak)
    target_user_balance.set('daily_can_claim_at', target_daily_can_claim_at)
    await target_user_balance.save()
    
    if with_ == AWARD_TYPE_BALANCE:
        awarded_with = EMOJI__HEART_CURRENCY.as_emoji
        up_from = target_balance
    else:
        awarded_with = 'streak(s)'
        up_from = target_streak
    
    await client.interaction_response_message_edit(
        interaction_event,
        embed = build_success_embed(target_user, interaction_event.guild_id, up_from, amount, awarded_with, message),
    )
    
    
    if target_user.bot:
        return
    
    target_user_settings = await get_one_user_settings(target_user.id)
    
    await send_embed_to(
        get_preferred_client_for_user(target_user, target_user_settings.preferred_client_id, client),
        target_user.id,
        build_notification_embed(
            interaction_event.user, interaction_event.guild_id, up_from, amount, awarded_with, message,
        ),
        None,
    )
