__all__ = ()

from base64 import b64decode as base64_decode
from binascii import Error as BinasciiError

from hata.ext.slash import InteractionResponse, abort

from ...bot_utils.user_getter import get_user
from ...bots import MAIN_CLIENT

from .constants import (
    CUSTOM_ID_TO_DO_ADD, CUSTOM_ID_TO_DO_CHANGE_PAGE_RP, CUSTOM_ID_TO_DO_LIST_CLOSE, CUSTOM_ID_TO_DO_DELETE_RP,
    CUSTOM_ID_TO_DO_EDIT_RP, TO_DOS
)
from .helpers import (
    check_permission, create_to_do_embed, create_to_do_page_components, render_to_do_page, request_to_dos,
    resolve_to_dos
)
from .to_do import ToDo


@MAIN_CLIENT.interactions(custom_id = CUSTOM_ID_TO_DO_ADD, target = 'form')
async def to_do_add_form_submit(
    event,
    *,
    name,
    description,
):
    """
    Handles a `to-do add` form submit.
    
    Parameters
    ----------
    event : ``InteractionEvent``
        The received event.
    
    name : `str` (Keyword only)
        Name for the to-do.
    
    description : `str`
        Description for the to-od.`
    
    Returns
    -------
    response : ``Embed``
    """
    check_permission(event)
    created_at = event.created_at
    creator_id = event.user.id
    
    name = name.replace('`', '')
    description = description.replace('`', '')
    
    to_do = ToDo(name, description, created_at, creator_id)
    await to_do.save()
    
    embed = create_to_do_embed(to_do, event.user)
    embed.add_author('Entry created')
    return embed


@MAIN_CLIENT.interactions(custom_id = CUSTOM_ID_TO_DO_EDIT_RP, target = 'form')
async def to_do_edit_form_submit(
    event,
    entry_id,
    *,
    name,
    description,
):
    """
    Handles a `to-do edit` form submit.
    
    Parameters
    ----------
    event : ``InteractionEvent``
        The received event.
    
    entry_id : `str`
        The entry's identifier. Later converted to `int`.
    
    name : `str` (Keyword only)
        Name for the to-do.
    
    description : `str`
        Description for the to-od.`
    
    Returns
    -------
    response : ``Embed``
    """
    check_permission(event)
    await request_to_dos()
    
    entry_id = int(entry_id)
    name = name.replace('`', '')
    description = description.replace('`', '')
    
    try:
        to_do = TO_DOS[entry_id]
    except KeyError:
        abort('The to-do was deleted meanwhile.')
    
    to_do.set('name', name)
    to_do.set('description', description)
    to_do.get_saver().begin()
    
    user = await get_user(to_do.creator_id)
    embed = create_to_do_embed(to_do, user)
    embed.add_author('Entry edited')
    return embed


@MAIN_CLIENT.interactions(custom_id = CUSTOM_ID_TO_DO_DELETE_RP)
async def to_do_del_approve(
    event,
    entry_id,
    state,
):
    """
    Handles a `to-do delete` component click.
    
    Parameters
    ----------
    event : ``InteractionEvent``
        The received event.
    
    entry_id : `str`
        The entry's identifier. Later converted to `int`.
    
    state : `str`
        Whether the deletion was confirmed. Later converted to itn.
    
    Returns
    -------
    response : ``InteractionResponse``
    """
    check_permission(event)
    await request_to_dos()
    
    entry_id = int(entry_id)
    state = int(state)
    
    try:
        to_do = TO_DOS[entry_id]
    except KeyError:
        return abort('The to-do was deleted meanwhile.')
    
    if state:
        to_do.delete()
    
    user = await get_user(to_do.creator_id)
    embed = create_to_do_embed(to_do, user)
    embed.add_author('Entry deleted' if state else 'Deleting entry cancelled')
    return InteractionResponse(
        embed = embed,
        components = None,
    )


@MAIN_CLIENT.interactions(custom_id = CUSTOM_ID_TO_DO_CHANGE_PAGE_RP)
async def page_switch(
    event,
    value,
    page,
):
    """
    Lists to-dos.
    
    This function is a coroutine.
    
    Parameters
    ----------
    event : ``InteractionEvent``
        The received interaction event.
    
    value : `None | str`
        Query value.
    
    page : `str`
        The page to show. Later converted to `int`.
    
    Returns
    -------
    response : ``InteractionResponse``
    """
    check_permission(event)
    await request_to_dos()
    
    while True:
        if value is None:
            break
        
        try:
            value = base64_decode(value)
        except BinasciiError:
            value = None
            break
        
        try:
            value = value.decode()
        except UnicodeDecodeError:
            value = None
            break
        
        break
    
    page = int(page)
    
    to_dos_list = resolve_to_dos(value)
    return InteractionResponse(
        content = render_to_do_page(to_dos_list, page, value),
        components = create_to_do_page_components(to_dos_list, page, value),
    )


@MAIN_CLIENT.interactions(custom_id = CUSTOM_ID_TO_DO_LIST_CLOSE)
async def page_close(client, event):
    """
    Closes the to-do page.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    
    event : ``InteractionEvent``
        The received event.
    """
    check_permission(event)
    
    await client.interaction_component_acknowledge(event)
    await client.interaction_response_message_delete(event)
