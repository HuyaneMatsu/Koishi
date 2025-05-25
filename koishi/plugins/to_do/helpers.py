__all__ = ()

from base64 import b64encode as base64_encode
from itertools import islice

from hata import DATETIME_FORMAT_CODE, Embed, create_button, create_row
from hata.ext.slash import abort
from sqlalchemy.exc import OperationalError

from ...bot_utils.constants import ROLE__SUPPORT__TESTER

from .constants import (
    CUSTOM_ID_TO_DO_LIST_CLOSE, EMOJI_CLOSE, EMOJI_LEFT, EMOJI_RIGHT, ENTRY_BY_ID_RP, PAGE_SIZE, TO_DOS,
    create_custom_id_to_do_change_page
)
from .queries import query_to_dos


def create_to_do_embed(to_do, user, guild_id):
    """
    Creates an embed representing a to-do.
    
    Parameters
    ----------
    to_do : ``ToDo``
        The to-do to represent.
    
    user : ``ClientUserBase``
        The user who added the to-do entry.
    
    guild_id : `int`
        The respective guild's identifier.
    
    Returns
    -------
    embed : ``Embed``
    """
    return Embed(
        f'To-Do entry #{to_do.entry_id}',
    ).add_field(
        'By',
        (
            f'```\n'
            f'{user.name_at(guild_id)}\n'
            f'```'
        ),
        inline = True,
    ).add_field(
        'At',
        (
            f'```\n'
            f'{to_do.created_at:{DATETIME_FORMAT_CODE}}\n'
            f'```'
        ),
        inline = True,
    ).add_field(
        'Name',
        (
            f'```\n'
            f'{to_do.name}\n'
            f'```'
        ),
    ).add_field(
        'Description',
        (
            f'```\n'
            f'{to_do.description}\n'
            f'```'
        ),
    ).add_thumbnail(
        user.avatar_url_at(guild_id),
    )


def _to_do_sort_key_getter_entry_id(to_do):
    """
    Sort key getter used to sort to-do entries.
    
    Parameters
    ----------
    to_do : ``ToDo``
        Entry to get its sort key of.
    
    Returns
    -------
    key : `int`
    """
    return to_do.entry_id


def _to_do_sort_key_getter_by_match_rate(item):
    """
    Sort key getter used to sort to-do entries.
    
    Parameters
    ----------
    item : `((int, int, int), ToDo)`
        Entry to get its sort key of.
    
    Returns
    -------
    key : `(int, int, int)`
    """
    return item[0]


def get_to_dos_sorted():
    """
    Gets the to-do sorted.
    
    Returns
    -------
    to_dos : `list<ToDo>`
    """
    return sorted(TO_DOS.values(), key = _to_do_sort_key_getter_entry_id)


def get_to_do_match_rate_for_value(to_do, value):
    """
    Gets match rate for the given to-do.
    
    Parameters
    ----------
    to_do : ``ToDo``
        To-do to get match rate for.
    
    value : `str`
        The value to match. Should be `.casefold()`-ed before passing.
    
    Returns
    -------
    match_rate : `None | (int, int, int)`
    """
    index = to_do.name.casefold().find(value)
    if index != -1:
        return 0, index, to_do.entry_id
    
    index = to_do.description.casefold().find(value)
    if index != -1:
        return 1, index, to_do.entry_id
    
    return None


def resolve_to_dos(value):
    """
    Resolves the to-do-s matching the given value.
    
    Parameters
    ----------
    value : `None | str`
        Value to match.
    
    Returns
    -------
    match : `list<ToDo>`
    """
    # If value is None
    if value is None:
        return get_to_dos_sorted()
    
    # If value is #n
    parsed = ENTRY_BY_ID_RP.fullmatch(value)
    if parsed is not None:
        entry_id = parsed.group(1)
        if not entry_id:
            return get_to_dos_sorted()
            
        entry_id = int(entry_id)
        try:
            entry = TO_DOS[entry_id]
        except KeyError:
            entries = []
        else:
            entries = [entry]
        
        return entries
    
    # anything else
    to_sort = []
    value = value.casefold()
    for entry in TO_DOS.values():
        sort_key = get_to_do_match_rate_for_value(entry, value)
        if sort_key is not None:
            to_sort.append((sort_key, entry))
    
    to_sort.sort(key = _to_do_sort_key_getter_by_match_rate)
    
    return [item[1] for item in to_sort]


def resolve_to_do(value):
    """
    Resolves a single to-do for the given value.
    
    Parameters
    ----------
    value : `None | str`
        Value to match.
    
    Returns
    -------
    match : `None | ToDo`
    """
    to_dos = resolve_to_dos(value)
    if to_dos:
        return to_dos[0]


def create_to_do_suggestion(to_do):
    """
    Creates a to-do suggestion.
    
    Parameters
    ----------
    to_do : ``ToDo``
        To-do to create suggestion for.
    
    Returns
    -------
    suggestion : `(str, str)`
    """
    name = to_do.name
    if len(name) > 40:
        name = name[:37]
        postfix = '...'
    else:
        postfix = ''
    
    return f'#{to_do.entry_id}: {name}{postfix}', f'#{to_do.entry_id}'


def get_to_do_suggestions(value):
    """
    Gets to do suggestions for the given value.
    
    Parameters
    ----------
    value : `None | str`
        Value to match.
    
    Returns
    -------
    suggestions : `list<(str, str)>`
    """
    return [create_to_do_suggestion(to_do) for to_do in islice(resolve_to_dos(value), 0, 25)]


def check_permission(event):
    """
    Checks whether the invoking user has required permissions.
    
    Parameters
    ----------
    event : ``InteractionEvent``
        The received interaction event.
    
    Raises
    ------
    InteractionAbortedError
    """
    if not event.user.has_role(ROLE__SUPPORT__TESTER):
        abort(f'{ROLE__SUPPORT__TESTER.name} only!')


TO_DOS_REQUESTED = False

async def request_to_dos():
    """
    Requests the to-dos from the database.
    
    If the to-dos are already requested does nothing.
    
    This function is a coroutine.
    """
    global TO_DOS_REQUESTED
    
    if TO_DOS_REQUESTED:
        return
    
    try:
        await query_to_dos()
    except OperationalError:
        abort('No connection to database')
    else:
        TO_DOS_REQUESTED = True


def render_to_do_listing_element_into(to_do, into):
    """
    Renders a to-do listing element.
    
    Parameters
    ----------
    to_do : ``ToDo``
        The to-do to render.
    
    into : `list<str>`
        Container to render into.
    
    Returns
    -------
    into : `list<str>`
    """
    into.append('#')
    into.append(str(to_do.entry_id))
    into.append(': ')
    
    name = to_do.name
    if len(name) > 40:
        name = name[:37]
        postfix = '...'
    else:
        postfix = None
    
    into.append(name)
    if (postfix is not None):
        into.append(postfix)
    
    into.append('\n')
    return into


def render_to_dos_into(to_do_slice, into):
    """
    Renders a to-do sequence.
    
    Parameters
    ----------
    to_do_slice : `iterable<ToDo>`
        A slice of to-dos.
    
    into : `list<str>`
        Container to render into.
    
    Returns
    -------
    into : `list<str>`
    """
    into.append('```\n')
    
    for to_do in to_do_slice:
        into = render_to_do_listing_element_into(to_do, into)
    
    into.append('```')
    return into


def get_to_do_page_count(to_dos_list):
    """
    Gets how much to-do pages there are.
    
    Parameters
    ----------
    to_dos_list : `list<ToDo>`
        The matched to-dos.
    
    Returns
    -------
    page_count : `int`
    """
    page_count, leftover = divmod(len(to_dos_list), PAGE_SIZE)
    if leftover:
        page_count += 1
    
    return page_count


def render_to_do_page(to_dos_list, page, value):
    """
    Builds a to-do page.
    
    Parameters
    ----------
    to_dos_list : `list<ToDo>`
        The matched to-dos.
    
    page : `int`
        The page number to build.
    
    value : `None | str`
        The queried value if any.
    
    Returns
    -------
    page : `str`
    """
    into = []
    if (value is not None):
        into.append('To-dos for: ')
        into.append(value)
        into.append('\n')
    
    # Do not show empty code block if there are no to-dos to show.
    page_count = get_to_do_page_count(to_dos_list)
    if page <= page_count:
        into = render_to_dos_into(islice(to_dos_list, (page - 1) * PAGE_SIZE, page * PAGE_SIZE), into)
        into.append('\n')
    
    into.append('Page ')
    into.append(str(page))
    into.append(' / ')
    into.append(str(page_count))
    
    return ''.join(into)


def create_to_do_page_components(to_dos_list, page, value):
    """
    Creates to-do page's components.
    
    Parameters
    ----------
    page : `int`
        The page number to build.
    
    value : `None | str`
        The queried value if any.
    
    Returns
    -------
    components : `list<Component>`
    """
    query = "" if value is None else base64_encode(value.encode()).decode()
    page_count = get_to_do_page_count(to_dos_list)
    
    return [
        create_row(
            create_button(
                f'Page {page - 1!s}',
                 EMOJI_LEFT,
                custom_id = create_custom_id_to_do_change_page(query, page - 1),
                enabled = (page > 1),
                
            ),
            create_button(
                f'Page {page + 1!s}',
                EMOJI_RIGHT,
                custom_id = create_custom_id_to_do_change_page(query, page + 1),
                enabled = (page < page_count),
            ),
            create_button(
                None,
                EMOJI_CLOSE,
                custom_id = CUSTOM_ID_TO_DO_LIST_CLOSE,
            )
        )
    ]
