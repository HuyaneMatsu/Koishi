__all__ = ()

from datetime import datetime as DateTime, timezone as TimeZone

from hata import create_text_display

from ...bot_utils.user_getter import get_user, get_users_unordered
from ...bot_utils.utils import send_embed_to
from ...bots import FEATURE_CLIENTS

from ..relationships_core import (
    CUSTOM_ID_RELATIONSHIPS_REQUEST_DETAILS_RP, RELATIONSHIP_TYPE_UNSET, Relationship, delete_relationship,
    delete_relationship_request, get_relationship_extension_traces, get_relationship_listing,
    get_relationship_request_from, get_relationship_request_listing, get_root, get_square, save_relationship
)
from ..user_balance import (
    ALLOCATION_FEATURE_ID_RELATIONSHIP_REQUEST, get_user_balance, get_user_balances, save_user_balance
)
from ..user_settings import get_one_user_settings, get_preferred_client_for_user

from .checks import (
    async_check_source_already_has_waifu, async_check_target_already_has_mama, async_check_target_already_has_mistress,
    async_check_target_already_has_waifu, check_already_related, check_insufficient_relationship_slots
)
from .component_building import (
    build_break_up_success_components, build_relationship_listing_components,
    build_relationship_request_accepted_components, build_relationship_request_cancellation_notification_components,
    build_relationship_request_cancelled_components, build_relationship_request_details_components,
    build_relationship_request_listing_components, build_relationship_request_rejected_components
)
from .content_building import (
    produce_break_up_notification_description, produce_relationship_request_accept_notification_description,
    produce_relationship_request_reject_notification_description
)
from .custom_ids import (
    CUSTOM_ID_RELATIONSHIPS_BREAK_UP_RP, CUSTOM_ID_RELATIONSHIPS_MODE_RP, CUSTOM_ID_RELATIONSHIPS_REQUEST_VIEW_CLOSE_RP,
    CUSTOM_ID_RELATIONSHIPS_REQUEST_VIEW_DECREMENT_DISABLED, CUSTOM_ID_RELATIONSHIPS_REQUEST_VIEW_INCREMENT_DISABLED,
    CUSTOM_ID_RELATIONSHIPS_REQUEST_VIEW_RP, CUSTOM_ID_RELATIONSHIPS_VIEW_CLOSE_RP,
    CUSTOM_ID_RELATIONSHIPS_VIEW_DECREMENT_DISABLED, CUSTOM_ID_RELATIONSHIPS_VIEW_INCREMENT_DISABLED,
    CUSTOM_ID_RELATIONSHIPS_VIEW_RP, CUSTOM_ID_RELATIONSHIP_REQUEST_ACCEPT_RP, CUSTOM_ID_RELATIONSHIP_REQUEST_CANCEL_RP,
    CUSTOM_ID_RELATIONSHIP_REQUEST_REJECT_RP
)
from .helpers import is_private_channel_of_two, select_existing_relationship


@FEATURE_CLIENTS.interactions(
    custom_id = [
        CUSTOM_ID_RELATIONSHIPS_REQUEST_VIEW_DECREMENT_DISABLED,
        CUSTOM_ID_RELATIONSHIPS_REQUEST_VIEW_INCREMENT_DISABLED,
        CUSTOM_ID_RELATIONSHIPS_VIEW_DECREMENT_DISABLED,
        CUSTOM_ID_RELATIONSHIPS_VIEW_INCREMENT_DISABLED,
    ],
)
async def quest_action_disabled():
    """
    Dummy handler for component interactions that supposed be disabled.
    
    This function is a coroutine.
    """
    pass


@FEATURE_CLIENTS.interactions(custom_id = CUSTOM_ID_RELATIONSHIPS_BREAK_UP_RP, target = 'form')
async def handle_break_up_confirmation(
    client,
    interaction_event,
    target_user_id,
):
    """
    Cancels divorcing the user.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the interaction.
    
    interaction_event : ``InteractionEvent``
        The received interaction event.
    
    target_user_id : `str`
        The target user's identifier who is targeted by the command. Hexadecimal integer as a string. Converted to int.
    """
    try:
        target_user_id = int(target_user_id, base = 16)
    except ValueError:
        return
    
    await client.interaction_application_command_acknowledge(
        interaction_event,
        False,
    )
    
    while True:
        target_user = await get_user(target_user_id)
        
        # Get relationship
        source_user_id = interaction_event.user_id
        source_relationships = await get_relationship_listing(source_user_id)
        if source_relationships is None:
            relationship = None
        else:
            for relationship in source_relationships:
                if (
                    (relationship.source_user_id == source_user_id and relationship.target_user_id == target_user_id) or
                    (relationship.target_user_id == source_user_id and relationship.source_user_id == target_user_id)
                ):
                    break
            else:
                relationship = None
        
        if relationship is None:
            error_components = [
                create_text_display(
                    f'You are not related to {target_user.name_at(interaction_event.guild_id)} anymore.'
                ),
            ]
            break
        
        source_investment = relationship.source_investment
        target_investment = relationship.target_investment
        
        if relationship.source_user_id != source_user_id:
            source_investment, target_investment = target_investment, source_investment
        
        # We do some math
        #
        # The users get back some hearts.
        # Lets say:
        #    user 0 investment: 3000
        #    user 1 investment: 1000
        # We create a water level for it which will be 1000 ((3000 + 1000) >> 2).
        #
        # Everything above the water level is given back to the users:
        #     user 0 receives: 2000
        #     user 1 receives: 0
        # Note: cannot be negative.
        #
        # Everything above water level // 3 is added to the user's value.
        #    user 0 receives: 666
        #    user 1 receives: 0
        # Note: can be negative
        
        value_water_level = (source_investment + target_investment) >> 2
        source_receives = source_investment - value_water_level
        target_receives = target_investment - value_water_level
        
        user_balances = await get_user_balances((source_user_id, target_user_id))
        source_user_balance = user_balances[source_user_id]
        target_user_balance = user_balances[target_user_id]
        
        
        if source_receives > 0:
            source_user_balance.modify_relationship_value_by(source_receives)
        if target_receives > 0:
            target_user_balance.modify_relationship_value_by(target_receives)
        
        source_user_balance.set_relationship_value(
            get_root(get_square(source_user_balance.relationship_value) + get_square(source_receives // 3)),
        )
        source_user_balance.increment_relationship_divorces()
        target_user_balance.set_relationship_value(
            get_root(get_square(target_user_balance.relationship_value) + get_square(target_receives // 3)),
        )
        
        # Save
        
        await delete_relationship(relationship)
        await save_user_balance(source_user_balance)
        await save_user_balance(target_user_balance)
        
        await client.interaction_response_message_edit(
            interaction_event,
            components = build_break_up_success_components(
                target_user, source_receives, target_receives, interaction_event.guild_id,
            ),
        )
        
        # Notify
        
        if not target_user.bot:
            target_user_user_settings = await get_one_user_settings(target_user_id)
            
            await send_embed_to(
                get_preferred_client_for_user(target_user, target_user_user_settings.preferred_client_id, client),
                target_user.id,
                None,
                [
                    create_text_display(
                        ''.join([*produce_break_up_notification_description(
                            interaction_event.user, target_receives, interaction_event.guild_id
                        )])
                    )
                ],
            )
        return
    
    await client.interaction_followup_message_create(
        interaction_event,
        components = error_components,
        show_for_invoking_user_only = True,
    )
    return


@FEATURE_CLIENTS.interactions(custom_id = CUSTOM_ID_RELATIONSHIPS_REQUEST_VIEW_RP)
async def handle_relationship_request_page_view(
    client,
    interaction_event,
    user_id,
    outgoing,
    page_index,
):
    """
    Handles a relationship request page view interaction.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the interaction.
    
    interaction_event : ``InteractionEvent``
        The received interaction event.
    
    user_id : `str`
        The original invoking user's identifiers as a string representing a hexadecimal integer.
    
    outgoing : `str`
       Whether to display outgoing relationship requests as a string representing a hexadecimal boolean.
    
    page_index : `str`
       the page's index to display as a string representing a hexadecimal integer.
    """
    try:
        user_id = int(user_id, 16)
        outgoing = int(outgoing, 16)
        page_index = int(page_index, 16)
    except ValueError:
        return
    
    outgoing = True if outgoing else False
    
    if interaction_event.user_id != user_id:
        return
    
    await client.interaction_component_acknowledge(
        interaction_event,
        False,
    )
    
    relationship_request_listing = await get_relationship_request_listing(user_id, outgoing)
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
            page_index,
        ),
    )


@FEATURE_CLIENTS.interactions(
    custom_id = [
        CUSTOM_ID_RELATIONSHIPS_REQUEST_VIEW_CLOSE_RP,
        CUSTOM_ID_RELATIONSHIPS_VIEW_CLOSE_RP,
    ],
)
async def handle_close(
    client,
    interaction_event,
    user_id,
):
    """
    handles a close interaction.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the interaction.
    
    interaction_event : ``InteractionEvent``
        The received interaction event.
    
    user_id : `str`
        The original invoking user's identifiers as a string representing a hexadecimal integer.
    """
    try:
        user_id = int(user_id, 16)
    except ValueError:
        return
    
    if interaction_event.user_id != user_id:
        return
    
    await client.interaction_component_acknowledge(
        interaction_event,
    )
    
    await client.interaction_response_message_delete(
        interaction_event,
    )


@FEATURE_CLIENTS.interactions(custom_id = CUSTOM_ID_RELATIONSHIPS_REQUEST_DETAILS_RP)
async def handle_relationship_request_details_view(
    client,
    interaction_event,
    user_id,
    outgoing,
    page_index,
    entry_id,
):
    """
    Handles a relationship request page view interaction.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the interaction.
    
    interaction_event : ``InteractionEvent``
        The received interaction event.
    
    user_id : `str`
        The original invoking user's identifiers as a string representing a hexadecimal integer.
    
    outgoing : `str`
       Whether it is from outgoing relationship requests as a string representing a hexadecimal boolean.
    
    page_index : `str`
       The page's index to back-direct to as a string representing a hexadecimal integer.
    
    entry_id : `str`
       The entry's identifier as a string representing a hexadecimal integer.
    """
    try:
        user_id = int(user_id, 16)
        outgoing = int(outgoing, 16)
        page_index = int(page_index, 16)
        entry_id = int(entry_id, 16)
    except ValueError:
        return
    
    outgoing = True if outgoing else False
    
    if interaction_event.user_id != user_id:
        return
    
    await client.interaction_component_acknowledge(
        interaction_event,
        False,
    )
    
    while True:
        relationship_request = await get_relationship_request_from(user_id, outgoing, entry_id)
        if (relationship_request is None):
            error_components = [
                create_text_display(
                    'You do not have such a relationship request anymore.'
                ),
            ]
            break
        
        target_user = await get_user(
            relationship_request.target_user_id if outgoing else relationship_request.source_user_id
        )
        
        await client.interaction_response_message_edit(
            interaction_event,
            components = build_relationship_request_details_components(
                interaction_event.user,
                outgoing,
                relationship_request,
                target_user,
                interaction_event.guild_id,
                page_index,
            )
        )
        return
    
    await client.interaction_followup_message_create(
        interaction_event,
        components = error_components,
        show_for_invoking_user_only = True,
    )
    return


@FEATURE_CLIENTS.interactions(custom_id = CUSTOM_ID_RELATIONSHIP_REQUEST_ACCEPT_RP)
async def hande_relationship_proposal_accept(
    client,
    interaction_event,
    user_id,
    outgoing,
    page_index,
    entry_id,
):
    """
    Handles interaction proposal acceptage.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    
    interaction_event : ``InteractionEvent``
        The received interaction event.
    
    user_id : `str`
        The original invoking user's identifiers as a string representing a hexadecimal integer.
    
    outgoing : `str`
       Whether it is from outgoing relationship requests as a string representing a hexadecimal boolean.
    
    page_index : `str`
       The page's index to back-direct to as a string representing a hexadecimal integer.
    
    entry_id : `str`
       The entry's identifier as a string representing a hexadecimal integer.
    """
    try:
        user_id = int(user_id, 16)
        outgoing = int(outgoing, 16)
        page_index = int(page_index, 16)
        entry_id = int(entry_id, 16)
    except ValueError:
        return
    
    outgoing = True if outgoing else False
    
    target_user = interaction_event.user
    if target_user.id != user_id:
        return
    
    await client.interaction_component_acknowledge(
        interaction_event,
        False,
    )
    
    while True:
        relationship_request = await get_relationship_request_from(user_id, outgoing, entry_id)
        if (relationship_request is None):
            error_components = [
                create_text_display(
                    'You do not have such a relationship request anymore.'
                ),
            ]
            break
        
        source_user = await get_user(relationship_request.source_user_id)
        
        relationship_type = relationship_request.relationship_type
        investment = relationship_request.investment
        
        # Queries
        user_balances = await get_user_balances((source_user.id, target_user.id),)
        source_user_balance = user_balances[source_user.id]
        target_user_balance = user_balances[target_user.id]
        
        source_relationship_listing = await get_relationship_listing(source_user.id)
        target_relationship_listing = await get_relationship_listing(target_user.id)
        
        target_relationship_request_listing = await get_relationship_request_listing(target_user.id, True)
        
        current_relationship = select_existing_relationship(
            source_relationship_listing, source_user.id, target_user.id
        )
        # Already checks.
        error_components = check_already_related(
            relationship_type, current_relationship, False, source_user, target_user, interaction_event.guild_id
        )
        if (error_components is not None):
            break
        
        # Slot check
        error_components = check_insufficient_relationship_slots(
            (0 if target_relationship_listing is None else len(target_relationship_listing)),
            (0 if target_relationship_request_listing is None else len(target_relationship_request_listing)),
            (current_relationship is not None),
            target_user_balance.relationship_slots,
        )
        if (error_components is not None):
            break
        
        # Edge cases
        if (current_relationship is None):
            # Allow marriage if they are already related, nyehehe
            error_components = await async_check_source_already_has_waifu(
                relationship_type, source_relationship_listing, False, source_user, interaction_event.guild_id
            )
            if (error_components is not None):
                break
            
            error_components = await async_check_target_already_has_waifu(
                relationship_type, target_relationship_listing, False, target_user, interaction_event.guild_id
            )
            if (error_components is not None):
                break
        
        error_components = await async_check_target_already_has_mama(
            relationship_type, target_relationship_listing, False, target_user, interaction_event.guild_id
        )
        if (error_components is not None):
            break
        
        error_components = await async_check_target_already_has_mistress(
            relationship_type, target_relationship_listing, False, target_user, interaction_event.guild_id
        )
        if (error_components is not None):
            break
        
        # Everything is good
        source_user_balance.remove_allocation(ALLOCATION_FEATURE_ID_RELATIONSHIP_REQUEST, relationship_request.entry_id)
        source_user_balance.modify_balance_by(-investment)
        await save_user_balance(source_user_balance)
        
        if current_relationship is None:
            current_relationship = Relationship(
                source_user.id, target_user.id, relationship_type, investment >> 1, DateTime.now(tz = TimeZone.utc)
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
        
        await delete_relationship_request(relationship_request)
        
        target_user_balance.modify_balance_by(investment >> 1)
        await save_user_balance(target_user_balance)
        
        # Respond
        await client.interaction_response_message_edit(
            interaction_event,
            components = build_relationship_request_accepted_components(
                user_id, outgoing, relationship_request, source_user, interaction_event.guild_id, page_index
            ),
        )
        
        # Notify
        if not source_user.bot:
            if is_private_channel_of_two(interaction_event.channel, source_user, target_user):
                await client.interaction_followup_message_create(
                    interaction_event,
                    components = [
                        create_text_display(source_user.mention),
                        create_text_display(
                            ''.join([*produce_relationship_request_accept_notification_description(
                                relationship_type, investment, target_user, interaction_event.guild_id
                            )])
                        ),
                    ],
                )
            
            else:
                source_user_settings = await get_one_user_settings(source_user.id)
                
                await send_embed_to(
                    get_preferred_client_for_user(source_user, source_user_settings.preferred_client_id, client),
                    source_user,
                    None,
                    [
                        create_text_display(
                            ''.join([*produce_relationship_request_accept_notification_description(
                                relationship_type, investment, target_user, interaction_event.guild_id
                            )])
                        ),
                    ],
                )
        return
    
    await client.interaction_followup_message_create(
        interaction_event,
        components = error_components,
    )


@FEATURE_CLIENTS.interactions(custom_id = CUSTOM_ID_RELATIONSHIP_REQUEST_REJECT_RP)
async def hande_relationship_proposal_reject(
    client,
    interaction_event,
    user_id,
    outgoing,
    page_index,
    entry_id,
):
    """
    Handles interaction proposal rejection.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    
    interaction_event : ``InteractionEvent``
        The received interaction event.
    
    user_id : `str`
        The original invoking user's identifiers as a string representing a hexadecimal integer.
    
    outgoing : `str`
       Whether it is from outgoing relationship requests as a string representing a hexadecimal boolean.
    
    page_index : `str`
       The page's index to back-direct to as a string representing a hexadecimal integer.
    
    entry_id : `str`
       The entry's identifier as a string representing a hexadecimal integer.
    """
    try:
        user_id = int(user_id, 16)
        outgoing = int(outgoing, 16)
        page_index = int(page_index, 16)
        entry_id = int(entry_id, 16)
    except ValueError:
        return
    
    outgoing = True if outgoing else False
    
    target_user = interaction_event.user
    if target_user.id != user_id:
        return
    
    await client.interaction_component_acknowledge(
        interaction_event,
        False,
    )
    
    while True:
        relationship_request = await get_relationship_request_from(user_id, outgoing, entry_id)
        if (relationship_request is None):
            error_components = [
                create_text_display(
                    'You do not have such a relationship request anymore.'
                ),
            ]
            break
        
        source_user = await get_user(relationship_request.source_user_id)
        source_user_balance = await get_user_balance(source_user.id)
        
        relationship_type = relationship_request.relationship_type
        investment = relationship_request.investment
        
        source_user_balance.remove_allocation(
            ALLOCATION_FEATURE_ID_RELATIONSHIP_REQUEST, relationship_request.entry_id
        )
        await save_user_balance(source_user_balance)
        
        await delete_relationship_request(relationship_request)
        
        await client.interaction_response_message_edit(
            interaction_event,
            components = build_relationship_request_rejected_components(
                user_id, outgoing, relationship_request, source_user, interaction_event.guild_id, page_index
            ),
        )
        
        # Send out the notifications.
        if not source_user.bot:
            if is_private_channel_of_two(interaction_event.channel, source_user, target_user):
                await client.interaction_followup_message_create(
                    interaction_event,
                    [
                        create_text_display(source_user.mention),
                        create_text_display(
                            ''.join([*produce_relationship_request_reject_notification_description(
                                relationship_type, investment, target_user, interaction_event.guild_id
                            )])
                        ),
                    ],
                )
            
            else:
                source_user_settings = await get_one_user_settings(source_user.id)
                await send_embed_to(
                    get_preferred_client_for_user(source_user, source_user_settings.preferred_client_id, client),
                    source_user,
                    None,
                    [
                        create_text_display(
                            ''.join([*produce_relationship_request_reject_notification_description(
                                relationship_type, investment, target_user, interaction_event.guild_id
                            )])
                        ),
                    ],
                )

        return
    
    await client.interaction_followup_message_create(
        interaction_event,
        components = error_components,
    )


@FEATURE_CLIENTS.interactions(custom_id = CUSTOM_ID_RELATIONSHIP_REQUEST_CANCEL_RP)
async def hande_relationship_proposal_cancel(
    client,
    interaction_event,
    user_id,
    outgoing,
    page_index,
    entry_id,
):
    """
    Handles interaction proposal cancellation.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    
    interaction_event : ``InteractionEvent``
        The received interaction event.
    
    user_id : `str`
        The original invoking user's identifiers as a string representing a hexadecimal integer.
    
    outgoing : `str`
       Whether it is from outgoing relationship requests as a string representing a hexadecimal boolean.
    
    page_index : `str`
       The page's index to back-direct to as a string representing a hexadecimal integer.
    
    entry_id : `str`
       The entry's identifier as a string representing a hexadecimal integer.
    """
    try:
        user_id = int(user_id, 16)
        outgoing = int(outgoing, 16)
        page_index = int(page_index, 16)
        entry_id = int(entry_id, 16)
    except ValueError:
        return
    
    outgoing = True if outgoing else False
    
    source_user = interaction_event.user
    if source_user.id != user_id:
        return
    
    await client.interaction_component_acknowledge(
        interaction_event,
        False,
    )
    
    while True:
        relationship_request = await get_relationship_request_from(user_id, outgoing, entry_id)
        if (relationship_request is None):
            error_components = [
                create_text_display(
                    'You do not have such a relationship request anymore.'
                ),
            ]
            break
        
        target_user = await get_user(relationship_request.target_user_id)
        
        source_user_balance = await get_user_balance(source_user.id)
        
        source_user_balance.remove_allocation(
            ALLOCATION_FEATURE_ID_RELATIONSHIP_REQUEST, relationship_request.entry_id
        )
        await save_user_balance(source_user_balance)
        
        await delete_relationship_request(relationship_request)
        
        
        await client.interaction_response_message_edit(
            interaction_event,
            components = build_relationship_request_cancelled_components(
                user_id, outgoing, relationship_request, target_user, interaction_event.guild_id, page_index
            ),
        )
        
        # Send out notifications.
        if not target_user.bot:
            if is_private_channel_of_two(interaction_event.channel, source_user, target_user):
                await client.interaction_followup_message_create(
                    interaction_event,
                    components = [
                        create_text_display(target_user.mention),
                        *build_relationship_request_cancellation_notification_components(
                            source_user, relationship_request, interaction_event.guild_id
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
                        build_relationship_request_cancellation_notification_components(
                            source_user, relationship_request, interaction_event.guild_id
                        ),
                    )
        return
    
    await client.interaction_followup_message_create(
        interaction_event,
        components = error_components,
    )


async def _respond_relationships_view(
    client,
    interaction_event,
    source_user_id,
    target_user_id,
    relationship_listing_mode,
    page_index,
):
    """
    Responds by showing relationships view.
    
    Handles a relationships view interaction.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    
    interaction_event : ``InteractionEvent``
        The received interaction event.
    
    source_user_id : `str`
        The original invoking user's identifiers as a string representing a hexadecimal integer.
    
    target_user_id : `str`
        the targeted user's identifier as a string representing a hexadecimal integer.
    
    relationship_listing_mode : `str`
       The rendering mode of displaying the relationship listing as a string representing a hexadecimal boolean.
    
    page_index : `str`
       The page's index to back-direct to as a string representing a hexadecimal integer.
    """
    try:
        source_user_id = int(source_user_id, 16)
        target_user_id = int(target_user_id, 16)
        relationship_listing_mode = int(relationship_listing_mode, 16)
        page_index = int(page_index, 16)
    except ValueError:
        return
    
    source_user = interaction_event.user
    if source_user.id != source_user_id:
        return
    
    await client.interaction_component_acknowledge(
        interaction_event,
        False,
    )
    
    if source_user_id == target_user_id:
        target_user = source_user
    else:
        target_user = await get_user(target_user_id)
    
    # Query
    target_user_balance = await get_user_balance(target_user_id)
    target_relationship_extension_traces = await get_relationship_extension_traces(target_user_id)
    target_relationship_request_listing = await get_relationship_request_listing(target_user_id, True)
    
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
            page_index,
        ),
    )


@FEATURE_CLIENTS.interactions(custom_id = CUSTOM_ID_RELATIONSHIPS_VIEW_RP)
async def handle_relationships_view(
    client,
    interaction_event,
    source_user_id,
    target_user_id,
    relationship_listing_mode,
    page_index,
):
    """
    Handles a relationships view interaction.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    
    interaction_event : ``InteractionEvent``
        The received interaction event.
    
    source_user_id : `str`
        The original invoking user's identifiers as a string representing a hexadecimal integer.
    
    target_user_id : `str`
        the targeted user's identifier as a string representing a hexadecimal integer.
    
    relationship_listing_mode : `str`
       The rendering mode of displaying the relationship listing as a string representing a hexadecimal boolean.
    
    page_index : `str`
       The page's index to back-direct to as a string representing a hexadecimal integer.
    """
    await _respond_relationships_view(
        client,
        interaction_event,
        source_user_id,
        target_user_id,
        relationship_listing_mode,
        page_index,
    )
    

@FEATURE_CLIENTS.interactions(custom_id = CUSTOM_ID_RELATIONSHIPS_MODE_RP)
async def handle_relationships_mode_select(
    client,
    interaction_event,
    source_user_id,
    target_user_id,
    page_index,
    *,
    relationship_listing_mode,
):
    """
    Handles a relationships mode select interaction.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    
    interaction_event : ``InteractionEvent``
        The received interaction event.
    
    source_user_id : `str`
        The original invoking user's identifiers as a string representing a hexadecimal integer.
    
    target_user_id : `str`
        the targeted user's identifier as a string representing a hexadecimal integer.
    
    page_index : `str`
       The page's index to back-direct to as a string representing a hexadecimal integer.
   
    relationship_listing_mode : `None | tuple<str>` (Keyword only)
       The rendering mode of displaying the relationship listing as a string representing a hexadecimal boolean.
    """
    if relationship_listing_mode is None:
        return
    
    await _respond_relationships_view(
        client,
        interaction_event,
        source_user_id,
        target_user_id,
        relationship_listing_mode[0],
        page_index,
    )
