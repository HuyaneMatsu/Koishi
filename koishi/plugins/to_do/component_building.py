__all__ = ()

from hata import (
    DATETIME_FORMAT_CODE, InteractionForm, TextInputStyle, create_button, create_container, create_label, create_row,
    create_section, create_separator, create_text_display, create_text_input, create_thumbnail_media
)

from .constants import EMOJI_CLOSE, EMOJI_PAGE_DECREMENT, EMOJI_PAGE_INCREMENT, PAGE_SIZE
from .custom_ids import (
    CUSTOM_ID_DESCRIPTION, CUSTOM_ID_NAME, CUSTOM_ID_TO_DO_CREATE, CUSTOM_ID_TO_DO_DELETE_BUILDER,
    CUSTOM_ID_TO_DO_EDIT_BUILDER, CUSTOM_ID_TO_DO_LISTING_CLOSE, CUSTOM_ID_TO_DO_LISTING_PAGE_BUILDER,
    CUSTOM_ID_TO_DO_LISTING_PAGE_DECREMENT_DISABLED, CUSTOM_ID_TO_DO_LISTING_PAGE_INCREMENT_DISABLED
)
from .helpers import get_to_do_page_count


def build_to_do_create_form():
    """
    Builds a to-do create form.
    
    Returns
    -------
    interaction_form : ``InteractionForm``
    """
    return InteractionForm(
        'Add todo entry',
        [
            create_label(
                'Name',
                component = create_text_input(
                    custom_id = CUSTOM_ID_NAME,
                    max_length = 128,
                    min_length = 2,
                ),
            ),
            create_label(
                'Description',
                component = create_text_input(
                    custom_id = CUSTOM_ID_DESCRIPTION,
                    max_length = 1000,
                    min_length = 0,
                    style = TextInputStyle.paragraph,
                )
            ),
        ],
        custom_id = CUSTOM_ID_TO_DO_CREATE,
    )


def build_to_do_edit_form(to_do):
    """
    Builds a to-do edit form.
    
    Parameters
    ----------
    to_do : ``ToDo``
        Todo entry to edit.
    
    Returns
    -------
    interaction_form : ``InteractionForm``
    """
    return InteractionForm(
        'Edit todo entry',
        [
            create_label(
                'Name',
                component = create_text_input(
                    custom_id = CUSTOM_ID_NAME,
                    max_length = 128,
                    min_length = 2,
                    value = to_do.name,
                ),
            ),
            create_label(
                'Description',
                component = create_text_input(
                    custom_id = CUSTOM_ID_DESCRIPTION,
                    max_length = 1000,
                    min_length = 0,
                    style = TextInputStyle.paragraph,
                    value = to_do.description,
                )
            ),
        ],
        custom_id = CUSTOM_ID_TO_DO_EDIT_BUILDER(to_do.entry_id),
    )


def build_to_do_delete_form(to_do):
    """
    Builds a to-do delete form.
    
    Parameters
    ----------
    to_do : ``ToDo``
        Todo entry to delete.
    
    Returns
    -------
    interaction_form : ``InteractionForm``
    """
    components = [
        create_text_display(
            f'## \\#{to_do.entry_id}: {to_do.name}'
        )
    ]
    
    description = to_do.description
    if (description is not None):
        components.append(create_text_display(description))
    
    return InteractionForm(
        'Are you sure to delete the following to-do?',
        components,
        custom_id = CUSTOM_ID_TO_DO_DELETE_BUILDER(to_do.entry_id),
    )


def _produce_to_do_entry_header(to_do, user, guild_id):
    """
    Produces todo entry header for its view.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    to_do : ``ToDo``
        Todo entry to build view for.
    
    user : ``ClientUserBase``
        The creator user.
    
    guild_id : `int`
        The local guild's identifier.
    
    Yields
    ------
    part : `str`
    """
    yield '## \\#'
    yield str(to_do.entry_id)
    yield ': '
    yield to_do.name
    yield '\n'
    yield '**By**: '
    yield user.name_at(guild_id)
    yield '\n**At**: '
    yield format(to_do.created_at, DATETIME_FORMAT_CODE)


def build_to_do_view(to_do, user, guild_id):
    """
    Builds to-do entry viewing components.
    
    Parameters
    ----------
    to_do : ``ToDo``
        Todo entry to build view for.
    
    user : ``ClientUserBase``
        The creator user.
    
    guild_id : `int`
        The local guild's identifier.
    
    Returns
    -------
    components : ``list<Component>``
    """
    components = []
    
    # Header.
    components.append(
        create_section(
            create_text_display(
                ''.join([*_produce_to_do_entry_header(to_do, user, guild_id)])
            ),
            thumbnail = create_thumbnail_media(user.avatar_url_at(guild_id)),
        ),
    )
    
    # Description.
    description = to_do.description
    if (description is not None):
        components.append(create_container(create_text_display(description)))
    
    return components


def _produce_to_do_listing_header(page_index, query, page_count):
    """
    Produces to-do listing header.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    page_index : `int`
        Page index to show.
    
    query : `None | str`
        Query to match the to-do entries.
    
    page_count : `int`
        The amount of available to-do pages.
    
    Yields
    ------
    part : `str`
    """
    yield 'Page: '
    yield str(page_index + 1)
    yield ' / '
    yield str(page_count)
    
    if (query is not None):
        yield '\nQuery: '
        yield query


def _produce_to_do_listing_slice(slice):
    """
    Produces a to-do listing slice.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    slice : ``list<ToDo>``
        To-do listing slice to render.
    
    Yields
    ------
    part : `str`
    """
    produce_line_break = False
    
    for to_do in slice:
        if produce_line_break:
            yield '\n'
        else:
            produce_line_break = True
        
        yield '\\#'
        yield str(to_do.entry_id)
        yield ': '
        
        name = to_do.name
        if len(name) > 40:
            name = name[:37]
            postfix = '...'
        else:
            postfix = None
        
        yield name
        if (postfix is not None):
            yield postfix


def build_to_do_listing(to_do_listing, page_index, query):
    """
    Builds to-do entry listing components.
    
    Parameters
    ----------
    to_do_listing : ``list<ToDo>``
        To-do listing to render.
    
    page_index : `int`
        Page index to show.
    
    query : `None | str`
        Query to match the to-do entries.
    
    Returns
    -------
    components : ``list<Component>``
    """
    page_count = get_to_do_page_count(to_do_listing)
    components = []
    
    # Header.
    components.append(create_text_display(''.join([*_produce_to_do_listing_header(page_index, query, page_count)])))
    components.append(create_separator())
    
    # Listing.
    slice = to_do_listing[page_index * PAGE_SIZE : (page_index + 1) * PAGE_SIZE]
    if slice:
        components.append(create_text_display(''.join([*_produce_to_do_listing_slice(slice)])))
        components.append(create_separator())
    
    # Control.
    if page_index:
        page_decrement_enabled = True
        page_decrement_custom_id = CUSTOM_ID_TO_DO_LISTING_PAGE_BUILDER(page_index - 1, query)
    else:
        page_decrement_enabled = False
        page_decrement_custom_id = CUSTOM_ID_TO_DO_LISTING_PAGE_DECREMENT_DISABLED
    
    if page_index < page_count - 1:
        page_increment_enabled = True
        page_increment_custom_id = CUSTOM_ID_TO_DO_LISTING_PAGE_BUILDER(page_index + 1, query)
    else:
        page_increment_enabled = False
        page_increment_custom_id = CUSTOM_ID_TO_DO_LISTING_PAGE_INCREMENT_DISABLED
    
    components.append(
        create_row(
            create_button(
                f'Page {page_index!s}',
                 EMOJI_PAGE_DECREMENT,
                custom_id = page_decrement_custom_id,
                enabled = page_decrement_enabled,
                
            ),
            create_button(
                f'Page {page_index + 2!s}',
                EMOJI_PAGE_INCREMENT,
                custom_id = page_increment_custom_id,
                enabled = page_increment_enabled,
            ),
            create_button(
                'Close',
                EMOJI_CLOSE,
                custom_id = CUSTOM_ID_TO_DO_LISTING_CLOSE,
            ),
        ),
    )
    
    return components
