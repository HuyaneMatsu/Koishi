__all__ = ()

from datetime import datetime as DateTime, timezone as TimeZone
from math import floor

from hata import DiscordException, ERROR_CODES, KOKORO, create_button
from hata.ext.slash import P
from scarletio import Task

from ...bot_utils.daily import DAILY_INTERVAL, calculate_daily_for, refresh_streak
from ...bot_utils.multi_client_utils import has_client_message_create_permissions
from ...bot_utils.utils import send_embed_to
from ...bots import FEATURE_CLIENTS

from ..relationships_core import (
    deepen_and_boost_relationship, get_extender_relationship_and_relationship_and_user_like_at
)
from ..user_balance import get_user_balance, get_user_balances
from ..user_settings import (
    USER_SETTINGS_CUSTOM_ID_NOTIFICATION_DAILY_BY_WAIFU_DISABLE, get_one_user_settings, get_preferred_client_for_user
)

from .embed_builders import (
    build_embed_already_claimed_other, build_embed_already_claimed_self, build_embed_daily_claimed_other,
    build_embed_daily_claimed_other_notification, build_embed_daily_claimed_self
)
from .helpers import should_top_gg_notify
from .related_completion import autocomplete_related_name, remove_comment


async def _try_respond(client, interaction_event, content, embed):
    """
    Tries to respond by editing the acknowledged message. If it fails then tries to create a new message instead.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        Client to respond with.
    
    interaction_event : ``InteractionEvent``
        Interaction event to respond to.
    
    content : `None | str`
        Content to send.
    
    embed : ``None | Embed``
        Embed to send.
    """
    try:
        await client.interaction_response_message_edit(
            interaction_event,
            content = content,
            embed = embed,
        )
    except GeneratorExit:
        raise
    
    except ConnectionError:
        retry_with_message_create = False
    
    except DiscordException as exception:
        if exception.status >= 500:
            retry_with_message_create = False
        else:
            exception_code = exception.code
            if exception_code in (
                ERROR_CODES.cannot_message_user_0,
                ERROR_CODES.cannot_message_user_1, # Perhaps the user blocked the bot and used it (in a dm ofc)?
                ERROR_CODES.missing_permissions, # Perhaps the client is unlinked or removed in the meanwhile?
            ):
                retry_with_message_create = False
            
            elif exception_code == ERROR_CODES.unknown_interaction:
                retry_with_message_create = True
            
            else:
                raise
    else:
        retry_with_message_create = False
    
    if not retry_with_message_create:
        return
    
    # Retry with message edit.
    if not has_client_message_create_permissions(interaction_event.channel, client):
        return
    
    try:
        await client.message_create(
            interaction_event.channel,
            content = content,
            embed = embed,
        )
    except GeneratorExit:
        raise
    
    except ConnectionError:
        pass
    
    except DiscordException as exception:
        if (
            (exception.status < 500) and
            (
                exception.code not in (
                    ERROR_CODES.unknown_message, # message deleted
                    ERROR_CODES.unknown_channel, # message's channel deleted
                    ERROR_CODES.missing_access, # client removed
                    ERROR_CODES.missing_permissions, # permissions changed meanwhile
                )
            )
        ):
            raise


async def claim_daily_for_yourself(client, interaction_event):
    """
    Claims daily for yourself.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    
    interaction_event : ``InteractionEvent``
        The received interaction event.
    """
    user = interaction_event.user
    
    user_balance = await get_user_balance(user.id)
    daily_can_claim_at = user_balance.daily_can_claim_at
    
    now = DateTime.now(TimeZone.utc)
    if daily_can_claim_at > now:
        await _try_respond(
            client,
            interaction_event,
            None,
            build_embed_already_claimed_self(daily_can_claim_at),
        )
        return
    
    streak = user_balance.streak
    streak_new = refresh_streak(streak, daily_can_claim_at, now)
    received = calculate_daily_for(user, streak_new)
    streak_new += 1
    balance_new = user_balance.balance + received
    
    user_balance.modify_balance_by(received)
    user_balance.set_streak(streak_new)
    user_balance.set_daily_can_claim_at(now + DAILY_INTERVAL)
    user_balance.increment_count_daily_self()
    user_balance.set_daily_reminded(False)
    
    send_response_task = Task(
        KOKORO,
        _try_respond(
            client,
            interaction_event,
            None,
            build_embed_daily_claimed_self(
                received,
                balance_new,
                streak,
                streak_new,
                should_top_gg_notify(user_balance.count_top_gg_vote, user_balance.top_gg_voted_at, now),
            ),
        ),
    )
    
    try:
        await deepen_and_boost_relationship(user_balance, None, None, received, save_source_user_balance = 2)
    except:
        send_response_task.cancel()
        raise
    
    try:
        await send_response_task
    except GeneratorExit:
        raise
    
    except ConnectionError:
        pass
    
    except DiscordException as exception:
        if (
            exception.status < 500 and
            exception.code != ERROR_CODES.unknown_interaction
        ):
            raise
    return


async def claim_daily_for_other(client, interaction_event, extender_relationship, relationship, target_user):
    """
    Claims daily for someone else.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    
    interaction_event : ``InteractionEvent``
        The received interaction event.
    
    extender_relationship : ``None | Relationship``
        The relationship through what is the target user is related to the source user if its through some-one else.
        Given as `None` if its a direct relationship.
    
    relationship : ``Relationship``
        The targeted user's relationship.
    
    target_user : ``ClientUserBase``
        The targeted user.
    """
    source_user = interaction_event.user
    
    user_balances = await get_user_balances((source_user.id, target_user.id),)
    source_user_balance = user_balances[source_user.id]
    target_user_balance = user_balances[target_user.id]

    now = DateTime.now(TimeZone.utc)
    
    target_daily_can_claim_at = target_user_balance.daily_can_claim_at
    
    if target_daily_can_claim_at > now:
        await _try_respond(
            client,
            interaction_event,
            None,
            build_embed_already_claimed_other(
                    target_daily_can_claim_at, target_user, interaction_event.guild_id
                ),
        )
        return
    
    streak = target_user_balance.streak
    streak_new = refresh_streak(streak, target_daily_can_claim_at, now)
    
    received = calculate_daily_for(target_user, streak)
    balance_new = target_user_balance.balance + received
    
    streak_new += 1
    relationship_value_increase = 1 + floor(received * 0.01)
    
    source_user_balance.increment_count_daily_for_related()
    
    target_user_balance.modify_balance_by(received)
    target_user_balance.set_streak(streak_new)
    target_user_balance.set_daily_can_claim_at(now + DAILY_INTERVAL)
    target_user_balance.increment_count_daily_by_related()
    target_user_balance.set_daily_reminded(False)
    
    
    send_response_task = Task(
        KOKORO,
        _try_respond(
            client,
            interaction_event,
            None,
            build_embed_daily_claimed_other(
                received, balance_new, streak, streak_new, target_user, interaction_event.guild_id
            ),
        ),
    )
    
    try:
        await deepen_and_boost_relationship(
            source_user_balance,
            target_user_balance,
            (relationship if (extender_relationship is None) else extender_relationship),
            relationship_value_increase,
            save_source_user_balance = 2,
            save_target_user_balance = 2,
        )
    except:
        send_response_task.cancel()
        raise
    
    try:
        await send_response_task
    except GeneratorExit:
        raise
    
    except ConnectionError:
        pass
    
    except DiscordException as exception:
        if (
            exception.status < 500 and
            exception.code != ERROR_CODES.unknown_interaction
        ):
            raise
    
    if (not target_user.bot):
        target_user_settings = await get_one_user_settings(target_user.id)
        if target_user_settings.notification_daily_by_waifu:
            await send_embed_to(
                get_preferred_client_for_user(target_user, target_user_settings.preferred_client_id, client),
                target_user.id,
                build_embed_daily_claimed_other_notification(
                    received, balance_new, streak_new, source_user, interaction_event.guild_id
                ),
                create_button(
                    'I don\'t want notifs, nya!!',
                    custom_id = USER_SETTINGS_CUSTOM_ID_NOTIFICATION_DAILY_BY_WAIFU_DISABLE,
                ),
            )


@FEATURE_CLIENTS.interactions(
    allowed_mentions = None,
    integration_types = ['guild_install', 'user_install'],
    is_global = True,
)
async def daily(
    client,
    interaction_event,
    target_user_name: P(
        str, 'Claiming daily for someone related?', 'related', autocomplete = autocomplete_related_name
    ) = None,
):
    """
    Claim a share of my hearts every day for yourself or for your related.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``ClientUserBase``
        The client who received the interaction.
    
    interaction_event : ``InteractionEvent``
        The received interaction event.
    
    target_user_name : `None | str` = `None`, Optional
        The targeted user's name if any.
    """
    await client.interaction_application_command_acknowledge(
        interaction_event,
        False,
    )
    
    if (target_user_name is None):
        await claim_daily_for_yourself(client, interaction_event)
        return
    
    extender_relationship_and_relationship_and_user = await get_extender_relationship_and_relationship_and_user_like_at(
        interaction_event.user_id, remove_comment(target_user_name), interaction_event.guild_id
    )
    if extender_relationship_and_relationship_and_user is None:
        await _try_respond(
            client,
            interaction_event,
            'Could not match anyone.',
            None,
        )
        return
    
    await claim_daily_for_other(client, interaction_event, *extender_relationship_and_relationship_and_user)
