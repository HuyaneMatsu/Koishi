__all__ = ()

from base64 import b64decode as base64_decode
from binascii import Error as BinasciiError

from hata.ext.slash import InteractionResponse

from ...bot_utils.user_getter import get_user
from ...bots import MAIN_CLIENT

from .custom_ids import CUSTOM_ID_TO_DO_LISTING_PAGE_DECREMENT_DISABLED, CUSTOM_ID_TO_DO_LISTING_PAGE_INCREMENT_DISABLED, \
    CUSTOM_ID_TO_DO_LISTING_CLOSE, CUSTOM_ID_TO_DO_LISTING_PAGE_PATTERN, CUSTOM_ID_TO_DO_EDIT_PATTERN, \
    CUSTOM_ID_TO_DO_DELETE_PATTERN, CUSTOM_ID_TO_DO_CREATE, CUSTOM_ID_NAME, CUSTOM_ID_DESCRIPTION
from .to_do import ToDo
from .helpers import check_for_required_role, match_to_do_listing
from .queries import get_to_do_listing, insert_to_do, update_to_do, delete_to_do
from .component_building import build_to_do_view, build_to_do_listing


@MAIN_CLIENT.interactions(
    custom_id = [
        CUSTOM_ID_TO_DO_LISTING_PAGE_DECREMENT_DISABLED,
        CUSTOM_ID_TO_DO_LISTING_PAGE_INCREMENT_DISABLED,
    ],
)
async def to_do_handle_dummy():
    """
    Dummy interactions handler.
    
    This function is a coroutine.
    """


@MAIN_CLIENT.interactions(custom_id = CUSTOM_ID_TO_DO_CREATE, target = 'form')
async def handle_to_do_create(
    client,
    interaction_event,
    *,
    name : CUSTOM_ID_NAME,
    description : CUSTOM_ID_DESCRIPTION,
):
    """
    handles a to do creation.
    
    Parameters
    ----------
    client : ``Client``
        The client receiving this interaction.
    
    interaction_event : ``InteractionEvent``
        The received interaction event.
    
    name : `str` (Keyword only)
        Name for the to-do.
    
    description : `None | str` (Keyword only)
        Description for the to-do.`
    """
    await client.interaction_application_command_acknowledge(
        interaction_event,
        show_for_invoking_user_only = True,
    )
    while True:
        error_message = check_for_required_role(interaction_event)
        if (error_message is not None):
            break
        
        name = name.replace('`', '').replace('\n', '').strip()
        if not name:
            error_message = 'Name became empty after sanitisation.'
            break
        
        # Make sure we are already cached.
        await get_to_do_listing()
        
        created_at = interaction_event.created_at
        creator_id = interaction_event.user_id
        
        to_do = ToDo(name, description, created_at, creator_id)
        await insert_to_do(to_do)
        
        await client.interaction_response_message_edit(interaction_event, '-# _ _')
        await client.interaction_response_message_delete(interaction_event)
        await client.interaction_followup_message_create(
            interaction_event,
            allowed_mentions = None,
            components = build_to_do_view(to_do, interaction_event.user, interaction_event.guild_id),
        )
        return
    
    await client.interaction_response_message_edit(
        interaction_event,
        allowed_mentions = None,
        content = error_message,
    )



@MAIN_CLIENT.interactions(custom_id = CUSTOM_ID_TO_DO_EDIT_PATTERN, target = 'form')
async def handle_to_do_edit(
    client,
    interaction_event,
    entry_id,
    *,
    name : CUSTOM_ID_NAME,
    description : CUSTOM_ID_DESCRIPTION,
):
    """
    Handles a `to-do edit` form submit.
    
    Parameters
    ----------
    client : ``Client``
        The client receiving this interaction.
    
    interaction_event : ``InteractionEvent``
        The received interaction event.
    
    entry_id : `str`
        The entry's identifier. Later converted to `int`.
    
    name : `str` (Keyword only)
        Name for the to-do.
    
    description : `str`
        Description for the to-do.`
    
    Returns
    -------
    response : ``Embed``
    """
    try:
        entry_id = int(entry_id, 16)
    except ValueError:
        return
    
    await client.interaction_application_command_acknowledge(
        interaction_event,
        show_for_invoking_user_only = True,
    )
    while True:
        error_message = check_for_required_role(interaction_event)
        if (error_message is not None):
            break
        
        name = name.replace('`', '').replace('\n', '').strip()
        if not name:
            error_message = 'Name became empty after sanitisation.'
            break
        
        # Make sure we are already cached.
        to_do_listing = await get_to_do_listing()
        for to_do in to_do_listing:
            if to_do.entry_id == entry_id:
                break
        else:
            error_message = 'Could not match any to-do.'
            break
        
        to_do.name = name
        to_do.description = description
        
        await update_to_do(to_do)
        user = await get_user(to_do.creator_id)
        
        await client.interaction_response_message_edit(interaction_event, '-# _ _')
        await client.interaction_response_message_delete(interaction_event)
        await client.interaction_followup_message_create(
            interaction_event,
            allowed_mentions = None,
            components = build_to_do_view(to_do, user, interaction_event.guild_id),
        )
        return
    
    await client.interaction_response_message_edit(
        interaction_event,
        allowed_mentions = None,
        content = error_message,
    )


@MAIN_CLIENT.interactions(custom_id = CUSTOM_ID_TO_DO_DELETE_PATTERN, target = 'form')
async def handle_to_do_delete(
    client,
    interaction_event,
    entry_id,
):
    """
    Handles a `to-do delete` component click.
    
    Parameters
    ----------
    client : ``Client``
        The client receiving this interaction.
    
    interaction_event : ``InteractionEvent``
        The received interaction event.
    
    entry_id : `str`
        The entry's identifier. Later converted to `int`.
    
    Returns
    -------
    response : ``InteractionResponse``
    """
    try:
        entry_id = int(entry_id, 16)
    except ValueError:
        return
    
    await client.interaction_application_command_acknowledge(
        interaction_event,
        show_for_invoking_user_only = True,
    )
    while True:
        error_message = check_for_required_role(interaction_event)
        if (error_message is not None):
            break
        
        # Make sure we are already cached.
        to_do_listing = await get_to_do_listing()
        for to_do in to_do_listing:
            if to_do.entry_id == entry_id:
                break
        else:
            error_message = 'Could not match any to-do.'
            break
        
        await delete_to_do(to_do)
        
        await client.interaction_response_message_edit(interaction_event, '-# _ _')
        await client.interaction_response_message_delete(interaction_event)
        await client.interaction_followup_message_create(
            interaction_event,
            content = 'To-do deleted.',
        )
        return
    
    await client.interaction_response_message_edit(
        interaction_event,
        allowed_mentions = None,
        content = error_message,
    )


@MAIN_CLIENT.interactions(custom_id = CUSTOM_ID_TO_DO_LISTING_PAGE_PATTERN)
async def handle_page_change(
    client,
    interaction_event,
    page_index,
    query,
):
    """
    Lists to-dos.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client receiving this interaction.
    
    interaction_event : ``InteractionEvent``
        The received interaction event.
    
    page_index : `str`
        The pages index to show encoded as a hexadecimal.
    
    query : `None | str`
        Query value.
    
    Returns
    -------
    response : ``InteractionResponse``
    """
    try:
        page_index = int(page_index, 16)
    except ValueError:
        return
    
    if (query is not None):
        try:
            query = base64_decode(query)
        except BinasciiError:
            return
        
        try:
            query = query.decode()
        except UnicodeDecodeError:
            return
    
    await client.interaction_component_acknowledge(interaction_event)
    
    while True:
        error_message = check_for_required_role(interaction_event)
        if (error_message is not None):
            break
        
        to_do_listing = await get_to_do_listing()
        to_do_listing = match_to_do_listing(to_do_listing, query)
        
        await client.interaction_response_message_edit(
            interaction_event,
            allowed_mentions = None,
            components = build_to_do_listing(to_do_listing, page_index, query),
        )
        return
    
    await client.interaction_followup_message_create(
        interaction_event,
        allowed_mentions = None,
        content = error_message,
        show_for_invoking_user_only = True,
    )


@MAIN_CLIENT.interactions(custom_id = CUSTOM_ID_TO_DO_LISTING_CLOSE)
async def page_close(
    client,
    interaction_event,
):
    """
    Closes the to-do page.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client receiving this interaction.
    
    interaction_event : ``InteractionEvent``
        The received interaction event.
    """
    await client.interaction_component_acknowledge(interaction_event)
    
    while True:
        error_message = check_for_required_role(interaction_event)
        if (error_message is not None):
            break
        
        await client.interaction_response_message_delete(interaction_event)
        return
    
    await client.interaction_followup_message_create(
        interaction_event,
        allowed_mentions = None,
        content = error_message,
        show_for_invoking_user_only = True,
    )
