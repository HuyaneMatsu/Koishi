__all__ = ()

from datetime import datetime as DateTime, timezone as TimeZone
from math import floor

from hata import ClientUserBase, Embed, InteractionType, create_button
from hata.ext.slash import InteractionAbortedError, P, abort

from ...bot_utils.user_getter import get_user, get_users_unordered
from ...bot_utils.utils import send_embed_to
from ...bots import FEATURE_CLIENTS

from ..relationships_core import (
    CUSTOM_ID_RELATIONSHIP_PROPOSAL_ACCEPT_PATTERN, CUSTOM_ID_RELATIONSHIP_PROPOSAL_REJECT_PATTERN, Relationship,
    RelationshipRequest, autocomplete_relationship_request_source_user_name,
    autocomplete_relationship_request_target_user_name, build_component_relationship_proposal_actions,
    calculate_relationship_value, get_affinity_multiplier, get_relationship_listing,
    get_relationship_request_and_user_like_at, get_relationship_request, get_relationship_request_listing,
)
from ..user_balance import get_user_balance, get_user_balances, save_user_balance
from ..user_settings import (
    USER_SETTINGS_CUSTOM_ID_NOTIFICATION_PROPOSAL_DISABLE, get_one_user_settings, get_preferred_client_for_user
)

from .checks import (
    async_check_can_propose_to_bot, async_check_source_already_has_waifu, async_check_source_already_has_waifu_request,
    async_check_target_already_has_mama, async_check_target_already_has_mistress, async_check_target_already_has_waifu,
    check_already_proposing, check_already_related, check_insufficient_available_balance, check_insufficient_investment,
    check_insufficient_relationship_slots, check_self_propose
)
from .constants import RELATIONSHIP_REQUEST_CREATABLE
from .embed_builders import (
    build_notification_embed_request_accepted, build_notification_embed_request_cancelled,
    build_notification_embed_request_created, build_notification_embed_request_rejected,
    build_relationship_request_listing_embed, build_success_embed_request_accepted,
    build_success_embed_request_cancelled, build_success_embed_request_created, build_success_embed_request_rejected
)
from .helpers import is_private_channel_of_two


PROPOSAL_COMMANDS = FEATURE_CLIENTS.interactions(
    None,
    description = 'Initiate a relationship.',
    integration_types = ['guild_install', 'user_install'],
    is_global = True,
    name = 'proposal',
)


@PROPOSAL_COMMANDS.interactions
async def create(
    client,
    event,
    target_user : (ClientUserBase, 'Who do you want to propose to?'),
    relationship_request_name : (
        sorted(RELATIONSHIP_REQUEST_CREATABLE.keys()), 'What kind of relation you want?', 'kind'
    ),
    investment : (int, 'How much do you want to spend on engaging in the relationship?'),
):
    """
    Propose to the given user.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    
    event : ``InteractionEvent``
        The received interaction event.
    
    target_user : ``ClientUserBase``
        The targeted user.
    
    relationship_request_name : `str`
        The name of the relationship request.
    
    investment : `int`
        The amount of balance to invest.
    """
    await client.interaction_application_command_acknowledge(event, False, show_for_invoking_user_only = True)
    
    try:
        relationship_type = RELATIONSHIP_REQUEST_CREATABLE[relationship_request_name]
    except KeyError:
        return abort(f'Invalid option selected: {relationship_request_name!s}.')
    
    source_user = event.user
    
    # Important pre-check
    check_self_propose(source_user, target_user)
    
    # Query required data
    user_balances = await get_user_balances((source_user.id, target_user.id),)
    source_user_balance = user_balances[source_user.id]
    target_user_balance = user_balances[target_user.id]
    
    source_relationship_listing = await get_relationship_listing(source_user.id)
    target_relationship_listing = await get_relationship_listing(target_user.id)
    
    source_relationship_request_listing = await get_relationship_request_listing(source_user.id, True)
    
    # Already checks.
    check_already_related(source_relationship_listing, True, source_user, target_user, event.guild_id)
    check_already_proposing(source_relationship_request_listing, target_user, event.guild_id)
    
    # Slot check
    check_insufficient_relationship_slots(
        (0 if source_relationship_listing is None else len(source_relationship_listing)),
        (0 if source_relationship_request_listing is None else len(source_relationship_request_listing)),
        (source_user_balance.relationship_slots),
    )
    
    # Some math -> investment checks
    relationship_value = calculate_relationship_value(
        target_user.id, target_user_balance.relationship_value, target_relationship_listing
    )
    relationship_value = floor(relationship_value * get_affinity_multiplier(source_user.id, target_user.id))
    
    check_insufficient_investment(relationship_value, investment)
    check_insufficient_available_balance(
        source_user_balance.balance - source_user_balance.get_cumulative_allocated_balance(), investment
    )
    
    # Edge cases
    await async_check_source_already_has_waifu(
        relationship_type, source_relationship_listing, True, source_user, target_user, event.guild_id
    )
    await async_check_source_already_has_waifu_request(
        relationship_type, source_relationship_request_listing, target_user, event.guild_id
    )
    await async_check_target_already_has_waifu(
        relationship_type, target_relationship_listing, True, source_user, target_user, event.guild_id
    )
    await async_check_target_already_has_mama(
        relationship_type, target_relationship_listing, True, source_user, target_user, event.guild_id
    )
    await async_check_target_already_has_mistress(
        relationship_type, target_relationship_listing, True, source_user, target_user, event.guild_id
    )
    
    # Bot post-check.
    await async_check_can_propose_to_bot(
        source_user,
        target_user,
        (0 if target_relationship_listing is None else len(target_relationship_listing)),
        target_user_balance.relationship_slots,
        event.guild_id,
    )
    
    # Everything is good
    if target_user.bot:
        target_user_balance.modify_balance_by(investment >> 1)
        await save_user_balance(target_user_balance)
        
        relationship = Relationship(
            source_user.id, target_user.id, relationship_type, investment, DateTime.now(tz = TimeZone.utc)
        )
        await relationship.save()
    
    else:
        relationship_request = RelationshipRequest(source_user.id, target_user.id, relationship_type, investment)
        await relationship_request.save()
    
    source_user_balance.modify_balance_by(-investment)
    await save_user_balance(source_user_balance)
    
    await client.interaction_response_message_edit(
        event,
        embed = build_success_embed_request_created(relationship_type, investment, target_user, event.guild_id),
    )
    
    # Send out notifications
    if not target_user.bot:
        if is_private_channel_of_two(event.channel, source_user, target_user):
            await client.interaction_followup_message_create(
                event,
                content = target_user.mention,
                embed = build_notification_embed_request_created(
                    relationship_type, investment, source_user, event.guild_id
                ),
                components = build_component_relationship_proposal_actions(source_user.id, target_user.id),
            )
        
        else:
            target_user_settings = await get_one_user_settings(target_user.id)
            if target_user_settings.notification_proposal:
                await send_embed_to(
                    get_preferred_client_for_user(target_user, target_user_settings.preferred_client_id, client),
                    target_user,
                    build_notification_embed_request_created(
                        relationship_type, investment, source_user, event.guild_id
                    ),
                    [
                        build_component_relationship_proposal_actions(source_user.id, target_user.id),
                        create_button(
                            'I don\'t want notifs, nya!!',
                            custom_id = USER_SETTINGS_CUSTOM_ID_NOTIFICATION_PROPOSAL_DISABLE,
                        ),
                    ],
                )
    
    if (not source_user.bot) and target_user.bot:
        await client.interaction_followup_message_create(
            event,
            embed = build_notification_embed_request_accepted(
                relationship_type, investment, target_user, event.guild_id
            ),
            show_for_invoking_user_only = True,
        )


async def build_relationship_request_listing(outgoing, user_id, guild_id):
    """
    Builds relationship request user listing.
    
    This function is a coroutine.
    
    Parameters
    ----------
    outgoing : `bool`
        Whether to render the outgoing embed.
    
    user_id : `int`
        The user's identifier who is requesting.
    
    guild_id : `int`
        The respective guild's identifier.
    
    Returns
    -------
    embed : ``Embed``
    """
    relationship_request_listing = await get_relationship_request_listing(user_id, outgoing)
    if relationship_request_listing is None:
        users = None
    else:
        users = await get_users_unordered(
            (relationship_request.target_user_id if outgoing else relationship_request.source_user_id)
            for relationship_request in relationship_request_listing
        )
    
    return build_relationship_request_listing_embed(outgoing, relationship_request_listing, users, guild_id)


@PROPOSAL_COMMANDS.interactions
async def list_incoming(
    client,
    event,
):
    """
    Lists the incoming relationship requests.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    
    event : ``InteractionEvent``
        The received interaction event.
    
    Returns
    -------
    embed : ``Embed``
    """
    await client.interaction_application_command_acknowledge(event, False)
    return await build_relationship_request_listing(False, event.user_id, event.guild_id)


@PROPOSAL_COMMANDS.interactions
async def list_outgoing(
    client,
    event,
):
    """
    Lists the outgoing relationship requests.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    
    event : ``InteractionEvent``
        The received interaction event.
    
    Returns
    -------
    embed : ``Embed``
    """
    await client.interaction_application_command_acknowledge(event, False)
    return await build_relationship_request_listing(True, event.user_id, event.guild_id)


@PROPOSAL_COMMANDS.interactions
async def cancel(
    client,
    event,
    target_user_name : P(
        str, 'The target user.', 'target', autocomplete = autocomplete_relationship_request_target_user_name
    ),
):
    """
    Cancels an outgoing request.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the request.
    
    event : ``InteractionEvent``
        The received interaction event.
    
    target_user_name : `str`
        The target user's name.
    
    Returns
    -------
    embed : ``Embed``
    """
    await client.interaction_application_command_acknowledge(event, False, show_for_invoking_user_only = True)
    
    source_user = event.user
    
    relationship_request, target_user = await get_relationship_request_and_user_like_at(
        source_user.id, True, target_user_name, event.guild_id
    )
    source_user_balance = await get_user_balance(source_user.id)
    
    relationship_request.delete()
    
    source_user_balance.modify_balance_by(relationship_request.investment)
    await save_user_balance(source_user_balance)
    
    relationship_type = relationship_request.relationship_type
    investment = relationship_request.investment
    
    await client.interaction_response_message_edit(
        event,
        embed = build_success_embed_request_cancelled(relationship_type, investment, target_user, event.guild_id),
    )
    
    # Send out notifications.
    if not target_user.bot:
        if is_private_channel_of_two(event.channel, source_user, target_user):
            await client.interaction_followup_message_create(
                event,
                content = target_user.mention,
                embed = build_notification_embed_request_cancelled(
                    relationship_type, investment, source_user, event.guild_id
                ),
            )
        
        else:
            target_user_settings = await get_one_user_settings(target_user.id)
            if target_user_settings.notification_proposal:
                await send_embed_to(
                    get_preferred_client_for_user(target_user, target_user_settings.preferred_client_id, client),
                    target_user,
                    build_notification_embed_request_cancelled(
                        relationship_type, investment, source_user, event.guild_id
                    ),
                    create_button(
                        'I don\'t want notifs, nya!!',
                        custom_id = USER_SETTINGS_CUSTOM_ID_NOTIFICATION_PROPOSAL_DISABLE,
                    ),
                )


@PROPOSAL_COMMANDS.interactions
async def reject(
    client,
    event,
    source_user_name : P(
        str, 'The source user.', 'source', autocomplete = autocomplete_relationship_request_source_user_name,
    ),
):
    """
    Rejects an incoming request.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    
    event : ``InteractionEvent``
        The received interaction event.
    
    source_user_name : `str`
        The source user's name.
    """
    await client.interaction_application_command_acknowledge(event, False, show_for_invoking_user_only = True)
    
    target_user = event.user
    
    relationship_request, source_user = await get_relationship_request_and_user_like_at(
        target_user.id, False, source_user_name, event.guild_id
    )
    await _handle_relationship_proposal_reject(client, event, source_user, target_user, relationship_request)


@FEATURE_CLIENTS.interactions(custom_id = CUSTOM_ID_RELATIONSHIP_PROPOSAL_REJECT_PATTERN)
async def handle_component_interaction_reject(client, event, source_user_id, target_user_id):
    """
    Rejects an incoming request. Handles a component interaction.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    
    event : ``InteractionEvent``
        The received interaction event.
    
    source_user_id : `str`
        The source user's identifier as hexadecimal integer.
    
    target_user_id : `str`
        The source user's identifier as hexadecimal integer.
    """
    await client.interaction_component_acknowledge(event)
    
    source_user_id = int(source_user_id, base = 16)
    target_user_id = int(target_user_id, base = 16)
    target_user = event.user
    
    if target_user.id != target_user_id:
        return
    
    try:
        relationship_request = await get_relationship_request(source_user_id, target_user.id)
    except InteractionAbortedError as exception:
        exception.response.abort = False
        raise
    
    source_user = await get_user(source_user_id)
    await _handle_relationship_proposal_reject(client, event, source_user, target_user, relationship_request)


async def _handle_relationship_proposal_reject(client, event, source_user, target_user, relationship_request):
    """
    Handles an interaction proposal rejection.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    
    event : ``InteractionEvent``
        The received interaction event.
    
    source_user : ``ClientUserBase``
        The source user.
    
    target_user_id : ``ClientUserBase``
        The target user.
    
    relationship_request : ``RelationshipRequest``
        The relationship request to reject.
    """
    source_user_balance = await get_user_balance(source_user.id)
    
    relationship_type = relationship_request.relationship_type
    investment = relationship_request.investment
    
    relationship_request.delete()
    
    source_user_balance.modify_balance_by(investment)
    await save_user_balance(source_user_balance)
    
    await client.interaction_response_message_edit(
        event,
        components = None,
        embed = build_success_embed_request_rejected(relationship_type, investment, source_user, event.guild_id),
    )
    
    # Send out the notifications.
    if not source_user.bot:
        if is_private_channel_of_two(event.channel, source_user, target_user):
            await client.interaction_followup_message_create(
                event,
                content = source_user.mention,
                embed = build_notification_embed_request_rejected(
                    relationship_type, investment, target_user, event.guild_id
                ),
            )
        
        else:
            source_user_settings = await get_one_user_settings(source_user.id)
            await send_embed_to(
                get_preferred_client_for_user(source_user, source_user_settings.preferred_client_id, client),
                source_user,
                build_notification_embed_request_rejected(relationship_type, investment, target_user, event.guild_id),
            )


@PROPOSAL_COMMANDS.interactions
async def accept(
    client,
    event,
    source_user_name : P(
        str, 'The source user.', 'source', autocomplete = autocomplete_relationship_request_source_user_name,
    ),
):
    """
    Accepts an incoming request.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the request.
    
    event : ``InteractionEvent``
        The received interaction event.
    
    source_user_name : `str`
        The source user's name.
    
    Returns
    -------
    embed : ``Embed``
    """
    await client.interaction_application_command_acknowledge(event, False, show_for_invoking_user_only = True)
    
    target_user = event.user
    
    relationship_request, source_user = await get_relationship_request_and_user_like_at(
        target_user.id, False, source_user_name, event.guild_id
    )
    
    await _handle_relationship_proposal_accept(client, event, source_user, target_user, relationship_request)


@FEATURE_CLIENTS.interactions(custom_id = CUSTOM_ID_RELATIONSHIP_PROPOSAL_ACCEPT_PATTERN)
async def handle_component_interaction_accept(client, event, source_user_id, target_user_id):
    """
    Accepts an incoming request. Handles a component interaction.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    
    event : ``InteractionEvent``
        The received interaction event.
    
    source_user_id : `str`
        The source user's identifier as hexadecimal integer.
    
    target_user_id : `str`
        The source user's identifier as hexadecimal integer.
    """
    await client.interaction_component_acknowledge(event)
    
    source_user_id = int(source_user_id, base = 16)
    target_user_id = int(target_user_id, base = 16)
    target_user = event.user
    
    if target_user.id != target_user_id:
        return
    
    try:
        relationship_request = await get_relationship_request(source_user_id, target_user.id)
    except InteractionAbortedError as exception:
        exception.response.abort = False
        raise
    
    source_user = await get_user(source_user_id)
    await _handle_relationship_proposal_accept(client, event, source_user, target_user, relationship_request)


async def _handle_relationship_proposal_accept(client, event, source_user, target_user, relationship_request):
    """
    Handles an interaction proposal acceptage.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    
    event : ``InteractionEvent``
        The received interaction event.
    
    source_user : ``ClientUserBase``
        The source user.
    
    target_user_id : ``ClientUserBase``
        The target user.
    
    relationship_request : ``RelationshipRequest``
        The relationship request to accept.
    """
    relationship_type = relationship_request.relationship_type
    investment = relationship_request.investment
    
    # Queries
    target_user_balance = await get_user_balance(target_user.id)
    
    source_relationship_listing = await get_relationship_listing(source_user.id)
    target_relationship_listing = await get_relationship_listing(target_user.id)
    
    target_relationship_request_listing = await get_relationship_request_listing(target_user.id, True)
    
    try:
        check_already_related(source_relationship_listing, False, source_user, target_user, event.guild_id)
        
        # Slot check
        check_insufficient_relationship_slots(
            (0 if target_relationship_listing is None else len(target_relationship_listing)),
            (0 if target_relationship_request_listing is None else len(target_relationship_request_listing)),
            (target_user_balance.relationship_slots),
        )
        
        # Edge cases
        await async_check_source_already_has_waifu(
            relationship_type, source_relationship_listing, False, source_user, target_user, event.guild_id
        )
        await async_check_target_already_has_waifu(
            relationship_type, target_relationship_listing, False, source_user, target_user, event.guild_id
        )
        await async_check_target_already_has_mama(
            relationship_type, target_relationship_listing, False, source_user, target_user, event.guild_id
        )
        await async_check_target_already_has_mistress(
            relationship_type, target_relationship_listing, False, source_user, target_user, event.guild_id
        )
    except InteractionAbortedError as exception:
        if event.type is InteractionType.message_component:
            exception.response.abort = False
        raise
    
    # Everything is good
    relationship_request.delete()
    
    target_user_balance.modify_relationship_value_by(relationship_request.investment >> 1)
    await save_user_balance(target_user_balance)
    
    relationship = Relationship(
        source_user.id, target_user.id, relationship_type, investment >> 1, DateTime.now(tz = TimeZone.utc)
    )
    await relationship.save()
    
    await client.interaction_response_message_edit(
        event,
        components = None,
        embed = build_success_embed_request_accepted(relationship_type, investment, source_user, event.guild_id),
    )
    
    if not source_user.bot:
        if is_private_channel_of_two(event.channel, source_user, target_user):
            await client.interaction_followup_message_create(
                event,
                content = source_user.mention,
                embed = build_notification_embed_request_accepted(
                    relationship_type, investment, target_user, event.guild_id
                ),
            )
        
        else:
            source_user_settings = await get_one_user_settings(source_user.id)
            
            await send_embed_to(
                get_preferred_client_for_user(source_user, source_user_settings.preferred_client_id, client),
                source_user,
                build_notification_embed_request_accepted(relationship_type, investment, target_user, event.guild_id),
            )
