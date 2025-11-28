__all__ = ()

from hata import ClientUserBase
from hata.ext.slash import P, abort

from ...bot_utils.user_getter import get_user, get_users_unordered
from ...bot_utils.utils import send_embed_to
from ...bots import FEATURE_CLIENTS

from ..relationship_divorces_core import build_component_invoke_relationship_divorces_decrement_purchase_self
from ..relationships_core import (
    CUSTOM_ID_RELATIONSHIP_DIVORCE_CANCEL_PATTERN, CUSTOM_ID_RELATIONSHIP_DIVORCE_CONFIRM_PATTERN,
    RELATIONSHIP_TYPE_NONE, RELATIONSHIP_TYPE_RELATIONSHIPS, autocomplete_relationship_unset_outgoing_user_name,
    autocomplete_relationship_user_name, build_component_relationship_divorce_question,
    get_relationship_and_user_like_at, get_relationship_listing, get_relationship_listing_with_extend,
    get_relationship_request_listing, get_relationship_unset_outgoing_and_user_like_at, get_root, get_square
)
from ..user_balance import get_user_balance, get_user_balances, save_user_balance
from ..user_settings import get_one_user_settings, get_preferred_client_for_user

from .checks import (
    async_check_source_already_has_waifu, async_check_target_already_has_mama, async_check_target_already_has_mistress,
    async_check_target_already_has_waifu
)
from .constants import RELATIONSHIP_REQUEST_CREATABLE
from .embed_builders import (
    build_failure_embed_cannot_divorce_not_related_anymore, build_failure_embed_you_cannot_cancel_this_divorce,
    build_failure_embed_you_cannot_confirm_this_divorce, build_notification_embed_divorced,
    build_question_embed_divorce, build_relationship_listing_embed, build_success_embed_divorce_cancelled,
    build_success_embed_divorce_confirmed, build_success_embed_relationship_updated
)


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
    event,
    target_user: (ClientUserBase, 'The user to get', 'user') = None,
):
    """
    Shows the user's relationship info.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the interaction.
    
    event : ``InteractionEvent``
        The received interaction event.
    
    target_user : `None | ClientUserBase` = `None`, Optional
        The user to show their relationship info of.
    """
    source_user = event.user
    if target_user is None:
        target_user = source_user
    
    await client.interaction_application_command_acknowledge(event, False)
    
    # Query
    target_user_balance = await get_user_balance(target_user.id)
    target_relationship_listing_with_extend = await get_relationship_listing_with_extend(target_user.id)
    target_relationship_request_listing = await get_relationship_request_listing(target_user.id, True)
    
    # Request users
    user_ids = set()
    
    if (target_relationship_listing_with_extend is not None):
        for relationship, relationship_listing in target_relationship_listing_with_extend:
            user_ids.add(relationship.source_user_id)
            user_ids.add(relationship.target_user_id)
        
            if (relationship_listing is None):
                continue
            
            for relationship in relationship_listing:
                    user_ids.add(relationship.source_user_id)
                    user_ids.add(relationship.target_user_id)
    
    user_ids.discard(target_user.id)
    
    if user_ids:
        users = await get_users_unordered(user_ids)
    else:
        users = None
    
    # Respond
    await client.interaction_response_message_edit(
        event,
        embed = build_relationship_listing_embed(
            source_user,
            target_user,
            target_user_balance,
            target_relationship_listing_with_extend,
            target_relationship_request_listing,
            users,
            event.guild_id,
        ),
    )


@RELATIONSHIPS_COMMANDS.interactions
async def break_up(
    client,
    event,
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
    await client.interaction_application_command_acknowledge(event, False, show_for_invoking_user_only = True)
    source_user = event.user
    relationship, target_user = await get_relationship_and_user_like_at(
        source_user.id, target_user_name, event.guild_id
    )
    
    await client.interaction_response_message_edit(
        event,
        embed = build_question_embed_divorce(target_user, event.guild_id),
        components = build_component_relationship_divorce_question(source_user.id, target_user.id),
    )


@FEATURE_CLIENTS.interactions(custom_id = CUSTOM_ID_RELATIONSHIP_DIVORCE_CANCEL_PATTERN)
async def divorce_cancel(
    client,
    event,
    source_user_id,
    target_user_id,
):
    """
    Cancels divorcing the user.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the interaction.
    
    event : ``InteractionEvent``
        The received interaction event.
    
    source_user_id : `str`
        The source user's identifier who invoked the command. Hexadecimal integer as a string. Converted to int.
    
    target_user_id : `str`
        The target user's identifier who is targeted by the command. Hexadecimal integer as a string. Converted to int.
    """
    source_user_id = int(source_user_id, base = 16)
    target_user_id = int(target_user_id, base = 16)
    
    invoking_user_id = event.user_id
    if invoking_user_id == source_user_id:
        pass
    
    elif invoking_user_id == target_user_id:
        source_user_id, target_user_id = target_user_id, source_user_id
    
    else:
        await client.interaction_component_acknowledge(event)
        await client.interaction_followup_message_create(
            event,
            embed = build_failure_embed_you_cannot_cancel_this_divorce(),
            show_for_invoking_user_only = True,
        )
        return
    
    await client.interaction_component_acknowledge(event, False)
    
    if invoking_user_id == target_user_id:
        target_user = event.user
    else:
        target_user = await get_user(target_user_id)
    
    await client.interaction_response_message_edit(
        event,
        embed = build_success_embed_divorce_cancelled(target_user, event.guild_id),
        components = None,
    )


@FEATURE_CLIENTS.interactions(custom_id = CUSTOM_ID_RELATIONSHIP_DIVORCE_CONFIRM_PATTERN)
async def divorce_confirm(
    client,
    event,
    source_user_id,
    target_user_id,
):
    """
    Cancels divorcing the user.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the interaction.
    
    event : ``InteractionEvent``
        The received interaction event.
    
    source_user_id : `str`
        The source user's identifier who invoked the command. Hexadecimal integer as a string. Converted to int.
    
    target_user_id : `str`
        The target user's identifier who is targeted by the command. Hexadecimal integer as a string. Converted to int.
    """
    source_user_id = int(source_user_id, base = 16)
    target_user_id = int(target_user_id, base = 16)
    
    invoking_user_id = event.user_id
    if invoking_user_id == source_user_id:
        pass
    
    elif invoking_user_id == target_user_id:
        source_user_id, target_user_id = target_user_id, source_user_id
    
    else:
        await client.interaction_component_acknowledge(event)
        await client.interaction_followup_message_create(
            event,
            embed = build_failure_embed_you_cannot_confirm_this_divorce(),
            show_for_invoking_user_only = True,
        )
        return
    
    await client.interaction_component_acknowledge(event, False)
    
    if invoking_user_id == target_user_id:
        target_user = event.user
    else:
        target_user = await get_user(target_user_id)
    
    # Get relationship
    
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
        await client.interaction_response_message_edit(
            event,
            embed = build_failure_embed_cannot_divorce_not_related_anymore(target_user, event.guild_id),
            components = None,
        )
        return
    
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
    
    relationship.delete()
    await save_user_balance(source_user_balance)
    await save_user_balance(target_user_balance)
    
    await client.interaction_response_message_edit(
        event,
        embed = build_success_embed_divorce_confirmed(target_user, source_receives, target_receives, event.guild_id),
        components = build_component_invoke_relationship_divorces_decrement_purchase_self(),
    )
    
    # Notify
    
    if not target_user.bot:
        target_user_user_settings = await get_one_user_settings(target_user_id)
        
        if invoking_user_id == source_user_id:
            source_user = event.user
        else:
            source_user = await get_user(source_user_id)
            
        await send_embed_to(
            get_preferred_client_for_user(target_user, target_user_user_settings.preferred_client_id, client),
            target_user.id,
            build_notification_embed_divorced(source_user, target_receives, event.guild_id),
        )


@RELATIONSHIPS_COMMANDS.interactions
async def update_unset(
    client,
    event,
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
    
    event : ``InteractionEvent``
        The received interaction event.
    
    target_user_name : `str`
        The user's name the relationship with.
    
    relationship_request_name : `str`
        The name of the relationship request.
    """
    await client.interaction_application_command_acknowledge(event, False)
    source_user = event.user
    
    try:
        relationship_type = RELATIONSHIP_REQUEST_CREATABLE[relationship_request_name]
    except KeyError:
        return abort(f'Invalid option selected: {relationship_request_name!s}.')
    
    relationship, target_user = await get_relationship_unset_outgoing_and_user_like_at(
        source_user.id, target_user_name, event.guild_id
    )
    
    if relationship.source_user_id == source_user.id:
        set_relationship_type = relationship_type
    else:
        set_relationship_type = RELATIONSHIP_TYPE_RELATIONSHIPS.get(relationship_type, RELATIONSHIP_TYPE_NONE)
    
    # Queries
    source_relationship_listing = await get_relationship_listing(source_user.id)
    target_relationship_listing = await get_relationship_listing(target_user.id)
    
    # Edge cases
    await async_check_source_already_has_waifu(
        relationship_type, source_relationship_listing, True, source_user, target_user, event.guild_id
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
    
    # Everything is good
    relationship.set('relationship_type', set_relationship_type)
    await relationship.save()
    
    await client.interaction_response_message_edit(
        event,
        embed = build_success_embed_relationship_updated(relationship_type, target_user, event.guild_id),
    )
