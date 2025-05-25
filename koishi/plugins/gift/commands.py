__all__ = ()

from hata import ClientUserBase, create_button
from hata.ext.slash import P

from ...bot_utils.utils import send_embed_to
from ...bots import FEATURE_CLIENTS

from ..gift_common import check_can_gift, identify_targeted_user
from ..relationships_core import autocomplete_relationship_extended_user_name
from ..user_balance import get_user_balance
from ..user_settings import (
    USER_SETTINGS_CUSTOM_ID_NOTIFICATION_GIFT_DISABLE, get_one_user_settings, get_preferred_client_for_user
)

from .checks import check_is_amount_valid, check_is_balance_sufficient, check_is_target_valid
from .embed_builders import build_notification_embed, build_success_embed


@FEATURE_CLIENTS.interactions(
    integration_types = ['guild_install', 'user_install'],
    is_global = True,
)
async def gift(
    client,
    event,
    amount: ('expression', 'How much do u love them?'),
    target_related_name : P(
        str,
        'Buy relationship slot for someone related',
        'related',
        autocomplete = autocomplete_relationship_extended_user_name,
    ) = None,
    target_user : (
        ClientUserBase,
        'Buy waifu slot for someone else?',
        'someone-else',
    ) = None,
    message: P('str', 'Optional message to send with the gift.', max_length = 1000) = None,
):
    """
    Gifts hearts to the chosen by your heart.
    
    This function is a coroutine generator.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    
    event : ``InteractionEvent``
        The received event.
    
    amount : `int`
        The amount of hearts to gift.
    
    target_related_name : `None | str` = `None`, Optional
        The targeted related user's name.
    
    target_user : `None | ClientUserBase` = `None`, Optional
        The targeted user.
    
    message : `None | str` = `None`, Optional
        Additional message to send.
    
    Yields
    ------
    response : `None | Embed`
    """
    await client.interaction_application_command_acknowledge(event, False, show_for_invoking_user_only = True)
    
    source_user = event.user
    
    target_user, relationship_to_deepen = await identify_targeted_user(
        source_user, target_related_name, target_user, event.guild_id
    )
    
    check_can_gift(source_user, relationship_to_deepen)
    check_is_target_valid(source_user, target_user)
    check_is_amount_valid(amount)
    
    source_user_balance = await get_user_balance(source_user.id)
    
    source_balance =  source_user_balance.balance
    source_allocated = max(source_user_balance.allocated, 0)
    
    check_is_balance_sufficient(source_balance, source_allocated)
    
    target_user_balance = await get_user_balance(target_user.id)
    target_balance = target_user_balance.balance
    
    amount = min(source_balance - source_allocated, amount)
    
    source_user_balance.set('balance', source_balance - amount)
    await source_user_balance.save()
    
    target_user_balance.set('balance', target_balance + amount)
    await target_user_balance.save()
    
    await client.interaction_response_message_edit(
        event,
        embed = build_success_embed(source_balance, target_balance, amount, target_user, event.guild_id, message),
    )
    
    if (not target_user.bot):
        target_user_settings = await get_one_user_settings(target_user.id)
        if target_user_settings.notification_gift:
            await send_embed_to(
                get_preferred_client_for_user(target_user, target_user_settings.preferred_client_id, client),
                target_user.id,
                build_notification_embed(target_balance, amount, source_user, event.guild_id, message),
                create_button(
                    'I don\'t want notifs, nya!!',
                    custom_id = USER_SETTINGS_CUSTOM_ID_NOTIFICATION_GIFT_DISABLE,
                ),
            )
