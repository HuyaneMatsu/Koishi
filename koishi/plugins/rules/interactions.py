__all__ = ()

from hata.ext.slash import InteractionResponse

from ...bot_utils.constants import (
    GUILD__SUPPORT, ROLE__SUPPORT__ANNOUNCEMENTS, ROLE__SUPPORT__BOT_ACCESS__KOISHI__DEFAULT, ROLE__SUPPORT__POLLS,
    ROLE__SUPPORT__VERIFIED
)
from ...bots import FEATURE_CLIENTS

from ..user_settings import OPTION_PREFERRED_CLIENT_ID, get_one_user_settings, set_user_settings_option

from .constants import (
    BOT_ACCESS_ROLES, CUSTOM_ID_CLAIM_ROLE_ANNOUNCEMENTS, CUSTOM_ID_CLAIM_ROLE_BOT_ACCESS, CUSTOM_ID_CLAIM_ROLE_POLLS,
    CUSTOM_ID_CLAIM_ROLE_VERIFIED, RULES_COMPONENTS
)
from .embed_builders import build_embed_rules_all, build_embed_rules_single
from .listing import RULES


@FEATURE_CLIENTS.interactions(
    guild = GUILD__SUPPORT,
    description = f'{GUILD__SUPPORT.name}\'s rules!'
)
async def rules(
    event,
    rule: (
        [(f'{index}. {title}', index) for index, (title, description_builder) in enumerate(RULES)],
        'Select a rule to show.'
    ) = None
):
    """
    Shows da rules.
    
    Parameters
    ----------
    event : ``InteractionEvent``
        The received interaction event.
    
    rule : `int` = `None`, Optional
        The rule to show.
    
    Returns
    -------
    response : ``InteractionResponse``
    """
    if rule is None:
        embed = build_embed_rules_all()
        if event.user_permissions.administrator:
            components = RULES_COMPONENTS
        else:
            components = None

    else:
        embed = build_embed_rules_single(rule)
        components = None
    
    return InteractionResponse(embed = embed, components = components, allowed_mentions = None)


@FEATURE_CLIENTS.interactions(custom_id = CUSTOM_ID_CLAIM_ROLE_VERIFIED)
async def claim_verified_role(client, event):
    """
    Assigns the verified role to the user.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the interaction event.
    
    event : ``InteractionEvent``
        The received interaction event.
    """
    await client.interaction_component_acknowledge(event)
    
    user = event.user
    if user.has_role(ROLE__SUPPORT__VERIFIED):
        response = f'You already have {ROLE__SUPPORT__VERIFIED.name} role claimed.'
    else:
        await client.user_role_add(user, ROLE__SUPPORT__VERIFIED)
        
        # Assign the default koishi bot upon accepting the rules.
        if not any(user.has_role(role) for role in BOT_ACCESS_ROLES.values()):
            await client.user_role_add(user, ROLE__SUPPORT__BOT_ACCESS__KOISHI__DEFAULT)
        
        response = f'You claimed {ROLE__SUPPORT__VERIFIED.name} role.'
    
    await client.interaction_followup_message_create(event, content = response, show_for_invoking_user_only = True)


@FEATURE_CLIENTS.interactions(custom_id = CUSTOM_ID_CLAIM_ROLE_ANNOUNCEMENTS)
async def claim_announcements_role(client, event):
    """
    Assigns or removes the announcements role to / of the user.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the interaction event.
    
    event : ``InteractionEvent``
        The received interaction event.
    """
    await client.interaction_component_acknowledge(event)
    
    user = event.user
    if user.has_role(ROLE__SUPPORT__ANNOUNCEMENTS):
        await client.user_role_delete(user, ROLE__SUPPORT__ANNOUNCEMENTS)
        response = f'Your {ROLE__SUPPORT__ANNOUNCEMENTS.name} role was removed.'
    else:
        await client.user_role_add(user, ROLE__SUPPORT__ANNOUNCEMENTS)
        response = f'You claimed {ROLE__SUPPORT__ANNOUNCEMENTS.name} role.'
    
    await client.interaction_followup_message_create(event, content = response, show_for_invoking_user_only = True)


@FEATURE_CLIENTS.interactions(custom_id = CUSTOM_ID_CLAIM_ROLE_POLLS)
async def claim_polls_role(client, event):
    """
    Assigns or removes the polls role to / of the user.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the interaction event.
    
    event : ``InteractionEvent``
        The received interaction event.
    """
    await client.interaction_component_acknowledge(event)
    
    user = event.user
    if user.has_role(ROLE__SUPPORT__POLLS):
        await client.user_role_delete(user, ROLE__SUPPORT__POLLS)
        response = f'Your {ROLE__SUPPORT__POLLS.name} role was removed.'
    else:
        await client.user_role_add(user, ROLE__SUPPORT__POLLS)
        response = f'You claimed {ROLE__SUPPORT__POLLS.name} role.'
    
    await client.interaction_followup_message_create(event, content = response, show_for_invoking_user_only = True)


@FEATURE_CLIENTS.interactions(custom_id = CUSTOM_ID_CLAIM_ROLE_BOT_ACCESS)
async def claim_bot_access_role(client, event, *, selected_bot_ids):
    """
    Assigns a bot access role.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the interaction event.
    
    event : ``InteractionEvent``
        The received interaction event.
    
    selected_bot_ids : `None | tuple<str>`
        The selected bot identifiers.
    """
    await client.interaction_component_acknowledge(event)
    
    if selected_bot_ids is None:
        return
    
    try:
        selected_bot_id = int(selected_bot_ids[0])
    except ValueError:
        return
    
    try:
        selected_role = BOT_ACCESS_ROLES[selected_bot_id]
    except KeyError:
        return
    
    user = event.user
    if user.has_role(selected_role):
        response = f'You already have the {selected_role.name} selected.'
        
    elif not user.has_role(ROLE__SUPPORT__VERIFIED):
        response = 'You must accept the rules first.'
    
    else:
        # remove the koishi default role
        if user.has_role(ROLE__SUPPORT__BOT_ACCESS__KOISHI__DEFAULT):
            await client.user_role_delete(user, ROLE__SUPPORT__BOT_ACCESS__KOISHI__DEFAULT)
        
        # remove all other roles
        for role in BOT_ACCESS_ROLES.values():
            if user.has_role(role):
                await client.user_role_delete(user, role)
        
        # assign new role
        await client.user_role_add(user, selected_role)
        
        # update preference
        user_settings = await get_one_user_settings(user.id)
        await set_user_settings_option(user_settings, OPTION_PREFERRED_CLIENT_ID, selected_bot_id)
        
        response = f'You selected {selected_role.name} <3.'
    
    await client.interaction_followup_message_create(event, content = response, show_for_invoking_user_only = True)
