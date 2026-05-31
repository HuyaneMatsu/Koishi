__all__ = ()

from itertools import islice

from ...bot_utils.constants import ROLE__SUPPORT__TESTER

from .constants import  ENTRY_BY_ID_RP, PAGE_SIZE


def check_for_required_role(event):
    """
    Checks whether the invoking user has required permissions.
    
    Parameters
    ----------
    event : ``InteractionEvent``
        The received interaction event.
    
    Returns
    -------
    error_message : `None | str`
    """
    if not event.user.has_role(ROLE__SUPPORT__TESTER):
        return f'{ROLE__SUPPORT__TESTER.name} only!'


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
    
    description = to_do.description
    if (description is not None):
        index = description.casefold().find(value)
        if index != -1:
            return 1, index, to_do.entry_id
    
    return None


def match_to_do_listing(to_do_listing, value):
    """
    Returns the matching to do do-s.
    
    Parameters
    ----------
    to_do_listing : ``list<ToDo>``
        To do listing to filter from.
    
    value : `None | str`
        Value to match.
    
    Returns
    -------
    matched_to_do_listing : ``list<ToDo>``
    """
    if value is None:
        return to_do_listing
    
    # If value is #n
    parsed = ENTRY_BY_ID_RP.fullmatch(value)
    if parsed is not None:
        entry_id = parsed.group(1)
        if not entry_id:
            return to_do_listing
        
        entry_id = int(entry_id)
        for to_do in to_do_listing:
            if to_do.entry_id == entry_id:
                matched_to_do_listing = [to_do]
                break
        else:
            matched_to_do_listing = []
        
        return matched_to_do_listing
    
    # anything else
    to_sort = []
    value = value.casefold()
    for to_do in to_do_listing:
        sort_key = get_to_do_match_rate_for_value(to_do, value)
        if sort_key is not None:
            to_sort.append((sort_key, to_do))
    
    to_sort.sort(key = _to_do_sort_key_getter_by_match_rate)
    
    return [item[1] for item in to_sort]


def match_to_do(to_do_listing, value):
    """
    Returns a single matching to-do.
    
    Parameters
    ----------
    to_do_listing : ``list<ToDo>``
        To do listing to filter from.
    
    value : `None | str`
        Value to match.
    
    Returns
    -------
    matched_to_do : ``None | ToDo``
    """
    matched_to_do_listing = match_to_do_listing(to_do_listing, value)
    if matched_to_do_listing:
        return matched_to_do_listing[0]


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


def get_to_do_suggestions(to_do_listing, value):
    """
    Gets to do suggestions for the given value.
    
    Parameters
    ----------
    to_do_listing : ``list<ToDo>``
        To do listing to filter from.
    
    value : `None | str`
        Value to match.
    
    Returns
    -------
    suggestions : `list<(str, str)>`
    """
    return [create_to_do_suggestion(to_do) for to_do in islice(match_to_do_listing(to_do_listing, value), 0, 25)]


def get_to_do_page_count(to_do_listing):
    """
    Gets how much to-do pages there are.
    
    Parameters
    ----------
    to_dos_list : ``list<ToDo>``
        The matched to-dos.
    
    Returns
    -------
    page_count : `int`
    """
    page_count, leftover = divmod(len(to_do_listing), PAGE_SIZE)
    if leftover:
        page_count += 1
    
    return page_count
