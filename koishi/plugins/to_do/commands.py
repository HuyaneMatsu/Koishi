__all__ = ()


from hata.ext.slash import Form, InteractionResponse, P, Row, abort

from ...bot_utils.constants import GUILD__SUPPORT
from ...bot_utils.user_getter import get_user
from ...bots import MAIN_CLIENT

from .constants import (
    ADD_TO_DO_FORM, CUSTOM_ID_TO_DO_DELETE_BASE, CUSTOM_ID_TO_DO_EDIT_BASE, DELETE_TO_DO_APPROVE, DELETE_TO_DO_CANCEL,
    TEXT_INPUT_DESCRIPTION, TEXT_INPUT_NAME
)
from .helpers import (
    check_permission, create_to_do_embed, create_to_do_page_components, get_to_do_suggestions, render_to_do_page,
    request_to_dos, resolve_to_do, resolve_to_dos
)


TO_DO = MAIN_CLIENT.interactions(
    None,
    name = 'todo',
    description = 'To-Do list for koishi',
    guild = GUILD__SUPPORT,
)


@TO_DO.autocomplete('name')
async def autocomplete_to_do_name(value):
    """
    Autocompletes a to-do command's name.
    
    This function is a coroutine.
    
    Parameters
    ----------
    value : `None | str`
        Value to match.
    
    Returns
    -------
    suggestions : `list<(str, str)>`
    """
    return get_to_do_suggestions(value)


@TO_DO.interactions
async def add(event):
    """
    Adds a new to-do!
    
    This function is a coroutine.
    
    Parameters
    ----------
    event : ``InteractionEvent``
        The received interaction event.
    
    Returns
    -------
    form : ``InteractionForm``
    """
    check_permission(event)
    return ADD_TO_DO_FORM


@TO_DO.interactions
async def get(
    event,
    name: (str, 'The entry\'s name | Use # to search by id.'),
):
    """
    Shows the defined to-do.
    
    This function is a coroutine.
    
    Parameters
    ----------
    event : ``InteractionEvent``
        The received interaction event.
    
    name : `str`
        The to-do's name to get.
    
    Returns
    -------
    response : ``Embed``
    """
    check_permission(event)
    await request_to_dos()
    to_do = resolve_to_do(name)
    if (to_do is None):
        abort('Could not match any to-do.')
    
    user = await get_user(to_do.creator_id)
    return create_to_do_embed(to_do, user)


@TO_DO.interactions
async def list_(
    event,
    page: P(int, 'Select a page.', min_value = 1, max_value = 10000) = 1,
    query: P(str, 'The entry\'s name', min_length = 2, max_length = 30) = None,
):
    """
    Lists to-dos.
    
    This function is a coroutine.
    
    Parameters
    ----------
    event : ``InteractionEvent``
        The received interaction event.
    
    page : `int` = `1`, Optional
        The page to show.
    
    query : `None | str` = `None`, Optional
        The to-do's name to get.
    
    Returns
    -------
    response : ``InteractionResponse``
    """
    check_permission(event)
    await request_to_dos()
    to_dos_list = resolve_to_dos(query)
    return InteractionResponse(
        content = render_to_do_page(to_dos_list, page, query),
        components = create_to_do_page_components(to_dos_list, page, query),
    )


@TO_DO.interactions
async def edit(
    event,
    name: (str, 'The entry\'s name | Use # to search by id.'),
):
    """
    Edit the defined to-do!
    
    Parameters
    ----------
    event : ``InteractionEvent``
        The received interaction event.
    name : `str`
        The to-do's name to get.
    
    Returns
    -------
    form : ``InteractionForm``
    
    """
    check_permission(event)
    await request_to_dos()
    to_do = resolve_to_do(name)
    if (to_do is None):
        abort('Could not match any to-do.')
    
    if to_do.creator_id != event.user.id:
        abort('You can edit only your own to-dos.')
    
    return Form(
        f'Editing todo entry #{to_do.entry_id}',
        [
            TEXT_INPUT_NAME.copy_with(value = to_do.name),
            TEXT_INPUT_DESCRIPTION.copy_with(value = to_do.description),
        ],
        custom_id = f'{CUSTOM_ID_TO_DO_EDIT_BASE}.{to_do.entry_id}.form',
    )


@TO_DO.interactions
async def del_(
    event,
    name: (str, 'The entry\'s name | Use # to search by id.'),
):
    """
    Removes the defined to-do.
    
    Parameters
    ----------
    event : ``InteractionEvent``
        The received interaction event.
    
    name : `str`
        The to-do's name to get.
    
    Returns
    -------
    response : ``InteractionResponse``
    """
    check_permission(event)
    await request_to_dos()
    to_do = resolve_to_do(name)
    if (to_do is None):
        abort('Could not match any to-do.')
    
    user = await get_user(to_do.creator_id)
    embed = create_to_do_embed(to_do, user)
    embed.add_author('Are you sure to delete this entry?')
    
    return InteractionResponse(
        embed = embed,
        components = Row(
            DELETE_TO_DO_APPROVE.copy_with(custom_id = f'{CUSTOM_ID_TO_DO_DELETE_BASE}.{to_do.entry_id}.1'),
            DELETE_TO_DO_CANCEL.copy_with(custom_id = f'{CUSTOM_ID_TO_DO_DELETE_BASE}.{to_do.entry_id}.0'),
        )
    )
