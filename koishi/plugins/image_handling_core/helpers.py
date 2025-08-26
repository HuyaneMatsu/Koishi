__all__ = ()

from random import random
from math import floor

from .constants import PAGE_SIZE



def _append_tags_requested(tags, tags_required, tags_banned, tags_requested):
    """
    Appends the processed tags from the required.
    
    Parameters
    ----------
    tags : `list<(bool, str)>`
        Processed tags.
    
    tags_required : `None | frozenset<str>`
        Tags to enable.
    
    tags_banned : `None | frozenset<str>`
        Tags to disable.
    
    tags_requested : `set<(bool, str)>`
        The requested tags.
    """
    for allowed, tag in tags_requested:
        if allowed:
            if (tags_banned is not None) and (tag in tags_banned):
                continue
        
        else:
            if (tags_required is not None) and (tag in tags_required):
                continue
        
        tags.append((allowed, tag))


def _join_tags(tags):
    """
    Joins the given processed tags.
    
    Parameters
    ----------
    tags : `list<(bool, str)>`
        Processed tags.
    
    Returns
    -------
    joined_tags : `str`
    """
    tags.sort()
    tag_added = False
    parts = []
    
    for allowed, tag in tags:
        if tag_added:
            parts.append(' ')
        else:
            tag_added = True
        
        if not allowed:
            parts.append('-')
        
        parts.append(tag)
    
    return ''.join(parts)


def join_tags(tags_required, tags_banned, tags_requested):
    """
    Joins the given tags.
    
    Parameters
    ----------
    tags_required : `None | frozenset<str>`
        Tags to enable.
    
    tags_banned : `None | frozenset<str>`
        Tags to disable.
    
    tags_requested : `set<(bool, str)>`
        The requested tags.
    
    Returns
    -------
    joined_tags : `str`
    """
    tags = []
    
    if (tags_required is not None):
        for tag in tags_required:
            tags.append((1, tag))
    
    if (tags_banned is not None):
        for tag in tags_banned:
            tags.append((0, tag))
    
    _append_tags_requested(tags, tags_required, tags_banned, tags_requested)
    return _join_tags(tags)


def join_tags_raw(tags_required, tags_banned, tags_requested):
    """
    Joins the given tags. Instead of adding every filter tag to the join, it just regularly filters the requested ones.
    
    Parameters
    ----------
    tags_required : `None | frozenset<str>`
        Tags to enable.
    
    tags_banned : `None | frozenset<str>`
        Tags to disable.
    
    tags_requested : `set<(bool, str)>`
        The requested tags.
    
    Returns
    -------
    joined_tags : `str`
    """
    tags = []
    _append_tags_requested(tags, tags_required, tags_banned, tags_requested)
    return _join_tags(tags)


def get_next_page_index(current_page, total_entry_count, random_order):
    """
    Get the next page's index.
    
    Parameters
    ----------
    current_page : `int`
        The current page's index.
    
    total_entry_count : `int`
        The total amount of entries.
    
    random_order : `bool`
        Whether images should be shown in random order.
    
    Returns
    -------
    next_page_index : `int`
    """
    if random_order:
        page_count = floor((total_entry_count + PAGE_SIZE - 1) / PAGE_SIZE)
        if page_count < 3:
            if page_count == 2:
                current_page ^= 1
            else:
                current_page = 0
        
        else:
            new_page = floor(page_count * random() ** 2)
            if (new_page + 1) >= page_count:
                current_page = 0
            elif (new_page == current_page):
                current_page += 1
            else:
                current_page = new_page
    
    else:
        current_page += 1
        leftover = total_entry_count - current_page * PAGE_SIZE
        if leftover <= 0:
            current_page = 0
    
    return current_page
