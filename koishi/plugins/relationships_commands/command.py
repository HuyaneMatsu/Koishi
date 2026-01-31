__all__ = ()

from datetime import datetime as DateTime, timezone as TimeZone
from math import floor

from hata import ClientUserBase, create_text_display
from hata.ext.slash import P

from ...bot_utils.user_getter import get_users_unordered
from ...bot_utils.utils import send_embed_to
from ...bots import FEATURE_CLIENTS

from ..relationships_core import (
    RELATIONSHIP_TYPE_NONE, RELATIONSHIP_TYPE_RELATIONSHIPS, RELATIONSHIP_TYPE_UNSET, Relationship,
    RelationshipRequest, autocomplete_relationship_unset_outgoing_user_name, autocomplete_relationship_user_name,
    calculate_relationship_value, get_affinity_multiplier, get_relationship_and_user_like_at,
    get_relationship_extension_traces, get_relationship_listing, get_relationship_request_listing,
    get_relationship_unset_outgoing_and_user_like_at, get_root, get_square, save_relationship,
    save_relationship_request
)
from ..user_balance import (
    ALLOCATION_FEATURE_ID_RELATIONSHIP_REQUEST, get_user_balance, get_user_balances, save_user_balance
)
from ..user_settings import get_one_user_settings, get_preferred_client_for_user

from .checks import (
    async_check_can_propose_to_bot, async_check_source_already_has_waifu, async_check_source_already_has_waifu_request,
    async_check_target_already_has_mama, async_check_target_already_has_mistress, async_check_target_already_has_waifu,
    check_already_proposing, check_already_related, check_insufficient_available_balance, check_insufficient_investment,
    check_insufficient_relationship_slots, check_self_propose
)
from .component_building import (
    build_break_up_confirmation_form, build_relationship_listing_components,
    build_relationship_request_creation_notification_components, build_relationship_request_listing_components,
    build_request_created_success_components, build_update_unset_success_components
)
from .constants import (
    RELATIONSHIP_LISTING_MODE_DEFAULT, RELATIONSHIP_LISTING_MODE_LEGACY, RELATIONSHIP_LISTING_MODE_LONG,
    RELATIONSHIP_LISTING_MODE_WIDE, RELATIONSHIP_REQUEST_CREATABLE
)
from .content_building import produce_relationship_request_accept_notification_description
from .helpers import is_private_channel_of_two, select_existing_relationship



RELATIONSHIPS_COMMANDS = FEATURE_CLIENTS.interactions(
    None,
    description = 'Manage existing relationships.',
    integration_types = ['guild_install', 'user_install'],
    is_global = True,
    name = 'relationships',
)


@RELATIONSHIPS_COMMANDS.interactions
async def info(
    client,
    interaction_event,
    target_user: (ClientUserBase, 'The user to get', 'user') = None,
    relationship_listing_mode : (
        [
            ('Legacy', format(RELATIONSHIP_LISTING_MODE_LEGACY, 'x')),
            ('Long', format(RELATIONSHIP_LISTING_MODE_LONG, 'x')),
            ('Wide', format(RELATIONSHIP_LISTING_MODE_WIDE, 'x')),
        ],
        'How should the relationships be displayed',
        'listing mode',
    ) = None
):
    """
    Shows the user's relationship info.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the interaction.
    
    interaction_event : ``InteractionEvent``
        The received interaction event.
    
    target_user : ``None | ClientUserBase`` = `None`, Optional
        The user to show their relationship info of.
    
    relationship_listing_mode : `None | str` = `None`, Optional
        The mode to render as as a string representing a hexadecimal integer. 
    """
    source_user = interaction_event.user
    if target_user is None:
        target_user = source_user
    
    if relationship_listing_mode is None:
        relationship_listing_mode = RELATIONSHIP_LISTING_MODE_DEFAULT
    else:
        try:
            relationship_listing_mode = int(relationship_listing_mode, 16)
        except ValueError:
            relationship_listing_mode = RELATIONSHIP_LISTING_MODE_DEFAULT
    
    await client.interaction_application_command_acknowledge(interaction_event, False)
    
    # Query
    target_user_balance = await get_user_balance(target_user.id)
    target_relationship_extension_traces = await get_relationship_extension_traces(target_user.id)
    target_relationship_request_listing = await get_relationship_request_listing(target_user.id, True)
    
    # Request users
    if (target_relationship_extension_traces is None):
        users = None
    else:
        users = await get_users_unordered(target_relationship_extension_traces.keys())
    
    # Respond
    await client.interaction_response_message_edit(
        interaction_event,
        components = build_relationship_listing_components(
            source_user,
            target_user,
            users,
            interaction_event.guild_id,
            target_user_balance,
            target_relationship_extension_traces,
            target_relationship_request_listing,
            relationship_listing_mode,
            0,
        ),
    )


@RELATIONSHIPS_COMMANDS.interactions
async def break_up(
    client,
    interaction_event,
    target_user_name: P(
        str, 'The user to break up with.', 'user', autocomplete = autocomplete_relationship_user_name
    ),
):
    """
    Breaks up with the given user.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the interaction.
    
    event : ``InteractionEvent``
        The received interaction event.
    
    target_user_name : `str`
        The user's name to divorce.
    """
    source_user = interaction_event.user
    while True:
        relationship_and_target_user = await get_relationship_and_user_like_at(
            source_user.id, target_user_name, interaction_event.guild_id
        )
        if relationship_and_target_user is None:
            error_components = [
                create_text_display('Cound not match anyone.')
            ]
            break
        
        await client.interaction_form_send(
            interaction_event,
            build_break_up_confirmation_form(relationship_and_target_user[1], interaction_event.guild_id),
        )
        return
    
    await client.interaction_response_message_create(
        interaction_event,
        components = error_components,
        show_for_invoking_user_only = True,
    )
    return


@RELATIONSHIPS_COMMANDS.interactions
async def update_unset(
    client,
    interaction_event,
    target_user_name: P(
        str, 'The user to get', 'user', autocomplete = autocomplete_relationship_unset_outgoing_user_name
    ),
    relationship_request_name : (
        sorted(RELATIONSHIP_REQUEST_CREATABLE.keys()), 'What kind of relation you want?', 'kind'
    ),
):
    """
    Update an old unset relationship.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the interaction.
    
    interaction_event : ``InteractionEvent``
        The received interaction event.
    
    target_user_name : `str`
        The user's name the relationship with.
    
    relationship_request_name : `str`
        The name of the relationship request.
    """
    await client.interaction_application_command_acknowledge(
        interaction_event,
        False,
        show_for_invoking_user_only = True,
    )
    
    while True:
        source_user = interaction_event.user
        
        try:
            relationship_type = RELATIONSHIP_REQUEST_CREATABLE[relationship_request_name]
        except KeyError:
            error_components = [
                create_text_display(f'Invalid option selected: {relationship_request_name!s}.')
            ]
            break
        
        relationship_and_target_user = await get_relationship_unset_outgoing_and_user_like_at(
            source_user.id, target_user_name, interaction_event.guild_id
        )
        if (relationship_and_target_user is None):
            error_components = [
                create_text_display('Could not match anyone.'),
            ]
            break
        
        relationship, target_user = relationship_and_target_user
        if relationship.source_user_id == source_user.id:
            set_relationship_type = relationship_type
        else:
            set_relationship_type = RELATIONSHIP_TYPE_RELATIONSHIPS.get(relationship_type, RELATIONSHIP_TYPE_NONE)
        
        # Queries
        source_relationship_listing = await get_relationship_listing(source_user.id)
        target_relationship_listing = await get_relationship_listing(target_user.id)
        
        # Edge cases
        if (relationship is None):
            error_components = await async_check_source_already_has_waifu(
                relationship_type, source_relationship_listing, True, source_user, interaction_event.guild_id
            )
            if (error_components is not None):
                break
            
            error_components = await async_check_target_already_has_waifu(
                relationship_type, target_relationship_listing, True, target_user, interaction_event.guild_id
            )
            if (error_components is not None):
                break
        
        error_components = await async_check_target_already_has_mama(
            relationship_type, target_relationship_listing, True, target_user, interaction_event.guild_id
        )
        if (error_components is not None):
            break
        
        error_components = await async_check_target_already_has_mistress(
            relationship_type, target_relationship_listing, True, target_user, interaction_event.guild_id
        )
        if (error_components is not None):
            break
        
        # Everything is good
        new_relationship_type = relationship.relationship_type
        new_relationship_type &= ~RELATIONSHIP_TYPE_UNSET
        new_relationship_type |= set_relationship_type
        relationship.set_relationship_type(new_relationship_type)
        await save_relationship(relationship)
        
        await client.interaction_response_message_edit(interaction_event, '-# _ _ ')
        await client.interaction_response_message_delete(interaction_event)
        
        await client.interaction_followup_message_create(
            interaction_event,
            components = build_update_unset_success_components(
                relationship_type, target_user, interaction_event.guild_id
            ),
        )
        return
    
    await client.interaction_response_message_edit(
        interaction_event,
        components = error_components,
    )
    

@RELATIONSHIPS_COMMANDS.interactions
async def proposal_create(
    client,
    interaction_event,
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
    
    interaction_event : ``InteractionEvent``
        The received interaction event.
    
    target_user : ``ClientUserBase``
        The targeted user.
    
    relationship_request_name : `str`
        The name of the relationship request.
    
    investment : `int`
        The amount of balance to invest.
    """
    await client.interaction_application_command_acknowledge(
        interaction_event,
        False,
        show_for_invoking_user_only = True,
    )
    
    while True:
        try:
            relationship_type = RELATIONSHIP_REQUEST_CREATABLE[relationship_request_name]
        except KeyError:
            error_components = [
                create_text_display(f'Invalid option selected: {relationship_request_name!s}.'),
            ]
            break
        
        source_user = interaction_event.user
        
        # Important pre-check
        error_components = check_self_propose(source_user, target_user)
        if (error_components is not None):
            break
        
        # Query required data
        user_balances = await get_user_balances((source_user.id, target_user.id),)
        source_user_balance = user_balances[source_user.id]
        target_user_balance = user_balances[target_user.id]
        
        source_relationship_listing = await get_relationship_listing(source_user.id)
        target_relationship_listing = await get_relationship_listing(target_user.id)
        
        source_relationship_request_listing = await get_relationship_request_listing(source_user.id, True)
        
        current_relationship = select_existing_relationship(
            source_relationship_listing, source_user.id, target_user.id
        )
        # Already checks.
        error_components = check_already_related(
            relationship_type, current_relationship, True, source_user, target_user, interaction_event.guild_id
        )
        if (error_components is not None):
            break
        
        error_components = check_already_proposing(
            source_relationship_request_listing, target_user, interaction_event.guild_id
        )
        if (error_components is not None):
            break
        
        # Slot check
        # Even do current relationship may exist, we still require the user to have a slot.
        error_components = check_insufficient_relationship_slots(
            (0 if source_relationship_listing is None else len(source_relationship_listing)),
            (0 if source_relationship_request_listing is None else len(source_relationship_request_listing)),
            0,
            source_user_balance.relationship_slots,
        )
        if (error_components is not None):
            break
        
        # Some math -> investment checks
        relationship_value = calculate_relationship_value(
            target_user.id, target_user_balance.relationship_value, target_relationship_listing
        )
        relationship_value = floor(relationship_value * get_affinity_multiplier(source_user.id, target_user.id))
        
        error_components = check_insufficient_investment(relationship_value, investment)
        if (error_components is not None):
            break
        
        error_components = check_insufficient_available_balance(
            source_user_balance.balance - source_user_balance.get_cumulative_allocated_balance(), investment
        )
        if (error_components is not None):
            break
        
        # Edge cases
        if (current_relationship is None):
            # Allow marriage if they are already related, nyehehe
            error_components = await async_check_source_already_has_waifu(
                relationship_type, source_relationship_listing, True, source_user, interaction_event.guild_id
            )
            if (error_components is not None):
                break
            
            error_components = await async_check_target_already_has_waifu(
                relationship_type, target_relationship_listing, True, target_user, interaction_event.guild_id
            )
            if (error_components is not None):
                break
        
        error_components = await async_check_source_already_has_waifu_request(
            relationship_type, source_relationship_request_listing, target_user, interaction_event.guild_id
        )
        if (error_components is not None):
            break
        
        error_components = await async_check_target_already_has_mama(
            relationship_type, target_relationship_listing, True, target_user, interaction_event.guild_id
        )
        if (error_components is not None):
            break
        
        error_components = await async_check_target_already_has_mistress(
            relationship_type, target_relationship_listing, True, target_user, interaction_event.guild_id
        )
        if (error_components is not None):
            break
        
        # Bot post-check.
        if (current_relationship is None):
            error_components = await async_check_can_propose_to_bot(
                source_user,
                target_user,
                (0 if target_relationship_listing is None else len(target_relationship_listing)),
                target_user_balance.relationship_slots,
                interaction_event.guild_id,
            )
            if (error_components is not None):
                break
        
        # Everything is good
        if target_user.bot:
            target_user_balance.modify_balance_by(investment >> 1)
            await save_user_balance(target_user_balance)
            
            if current_relationship is None:
                current_relationship = Relationship(
                    source_user.id, target_user.id, relationship_type, investment, DateTime.now(tz = TimeZone.utc)
                )
            else:
                new_relationship_type = current_relationship.relationship_type
                new_relationship_type &= ~RELATIONSHIP_TYPE_UNSET
                new_relationship_type |= relationship_type
                current_relationship.set_relationship_type(new_relationship_type)
                
                if (current_relationship.source_user_id == source_user.id):
                    existing_investment = current_relationship.source_investment
                    applicator = Relationship.set_source_investment
                else:
                    existing_investment = current_relationship.target_investment
                    applicator = Relationship.set_target_investment
                
                applicator(current_relationship, get_root(get_square(existing_investment) + get_square(investment >> 1)))
            
            await save_relationship(current_relationship)
            
            source_user_balance.modify_balance_by(-investment)
            await save_user_balance(source_user_balance)
        
        else:
            relationship_request = RelationshipRequest(source_user.id, target_user.id, relationship_type, investment)
            await save_relationship_request(relationship_request)
            
            source_user_balance.add_allocation(
                ALLOCATION_FEATURE_ID_RELATIONSHIP_REQUEST, relationship_request.entry_id, investment, None
            )
            await save_user_balance(source_user_balance)
        
        await client.interaction_response_message_edit(interaction_event, '-# _ _ ')
        await client.interaction_response_message_delete(interaction_event)
        
        await client.interaction_followup_message_create(
            interaction_event,
            components = build_request_created_success_components(
                relationship_type, investment, target_user, interaction_event.guild_id
            ),
        )
        
        # Send out notifications
        if not target_user.bot:
            if is_private_channel_of_two(interaction_event.channel, source_user, target_user):
                await client.interaction_followup_message_create(
                    interaction_event,
                    components = [
                        create_text_display(target_user.mention),
                        *build_relationship_request_creation_notification_components(
                            source_user, relationship_request, target_user.id, interaction_event.guild_id
                        ),
                    ],
                )
            
            else:
                target_user_settings = await get_one_user_settings(target_user.id)
                if target_user_settings.notification_proposal:
                    await send_embed_to(
                        get_preferred_client_for_user(target_user, target_user_settings.preferred_client_id, client),
                        target_user,
                        None,
                        build_relationship_request_creation_notification_components(
                            source_user, relationship_request, target_user.id, interaction_event.guild_id
                        ),
                    )
        
        if (not source_user.bot) and target_user.bot:
            await client.interaction_followup_message_create(
                interaction_event,
                components = [
                    create_text_display(
                        ''.join([*produce_relationship_request_accept_notification_description(
                            relationship_type, investment, target_user, interaction_event.guild_id
                        )])
                    ),
                ],
                show_for_invoking_user_only = True,
            )
        return
    
    await client.interaction_response_message_edit(
        interaction_event,
        components = error_components,
    )


async def _respond_relationship_request_listing(client, interaction_event, outgoing):
    """
    Builds relationship request user listing.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    
    interaction_event : ``InteractionEvent``
        The received interaction event.
    
    outgoing : `bool`
        Whether redirect to outgoing requests.
    """
    await client.interaction_application_command_acknowledge(
        interaction_event,
        False,
    )
    
    relationship_request_listing = await get_relationship_request_listing(interaction_event.user_id, outgoing)
    if relationship_request_listing is None:
        users = None
    else:
        users = await get_users_unordered(
            (relationship_request.target_user_id if outgoing else relationship_request.source_user_id)
            for relationship_request in relationship_request_listing
        )
    
    await client.interaction_response_message_edit(
        interaction_event,
        components = build_relationship_request_listing_components(
            interaction_event.user,
            outgoing,
            relationship_request_listing,
            users,
            interaction_event.guild_id,
            0,
        ),
    )


@RELATIONSHIPS_COMMANDS.interactions
async def proposal_list_incoming(
    client,
    interaction_event,
):
    """
    Lists the incoming relationship requests.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    
    interaction_event : ``InteractionEvent``
        The received interaction event.
    """
    await _respond_relationship_request_listing(client, interaction_event, False)


@RELATIONSHIPS_COMMANDS.interactions
async def proposal_list_outgoing(
    client,
    interaction_event,
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
    """
    await _respond_relationship_request_listing(client, interaction_event, True)
