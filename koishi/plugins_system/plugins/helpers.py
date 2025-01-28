__all__ = ()

from itertools import islice
from re import compile as re_compile

from hata import BUILTIN_EMOJIS, CLIENTS, KOKORO
from hata.ext.plugin_loader import PLUGINS, PluginError, frame_filter, get_plugin_like
from hata.ext.slash import Button, InteractionResponse, Option, Row, Select, abort
from scarletio import render_exception_into_async

from ...bot_utils.constants import ROLE__SUPPORT__ADMIN


VALUE_LOCKED = '*(locked)*'
PAGE_SIZE = 20


EMOJI_LEFT = BUILTIN_EMOJIS['arrow_backward']
EMOJI_RIGHT = BUILTIN_EMOJIS['arrow_forward']
EMOJI_CLOSE = BUILTIN_EMOJIS['x']

CUSTOM_ID_PAGE_CLOSE = 'plugins.page.close'
create_custom_switch_client = lambda page: f'plugins.page.switch.{page:x}'
create_custom_id_page_n = lambda client_id, page: f'plugins.page.{client_id:x}.{page:x}'
CUSTOM_ID_SWITCH_CLIENT_RP = re_compile('plugins\\.page\\.switch\\.([0-9a-f]+)')
CUSTOM_ID_PAGE_N_RP = re_compile('plugins\\.page\\.([0-9a-f]+)\\.([0-9a-f]+)')


def check_permission(event):
    """
    Checks whether the event's invoker has the required permissions.
    
    Parameters
    ----------
    event : ``InteractionEvent``
        The received interaction event.
    
    Raises
    ------
    InteractionAbortedError
    """
    if not event.user.has_role(ROLE__SUPPORT__ADMIN):
        abort(f'You must have {ROLE__SUPPORT__ADMIN.mention} to invoke this command.')


def get_plugins_sequence(client):
    """
    Gets a sequence of plugins for the given client.
    
    Parameters
    ----------
    client : `None | Client`
        Client to get the plugins for.
    
    Returns
    -------
    plugins_sequence : `sequence<Plugin>`
    """
    if client is None:
        plugins_sequence = PLUGINS.values()
    else:
        plugins_sequence = client.plugins
    
    return plugins_sequence


def get_plugins_page_count(plugins_sequence):
    """
    Gets how much plugins there are.
    
    Parameters
    ----------
    plugins_sequence : `sequence<Plugin>`
        The plugins to get page count for.
    
    Returns
    -------
    page_count : `int`
    """
    page_count, leftover = divmod(len(plugins_sequence), PAGE_SIZE)
    if leftover:
        page_count += 1
    
    return page_count


def render_plugins_page(client, plugins_sequence, page):
    """
    Renders a page for the given page number.
    
    Parameters
    ----------
    client : `None | Client`
        Client to render page for.
    
    plugins_sequence : `sequence<Plugin>`
        A sequence of plugins to page for.
    
    page : ``Page``
        Page number to get.
    
    Returns
    -------
    result : `str`
    """
    plugin_list = get_plugin_list(plugins_sequence, page, PAGE_SIZE)
    
    into = []
    if (client is not None):
        into.append('Plugins for ')
        into.append(client.full_name)
        into.append(' (')
        into.append(str(client.id))
        into.append(')\n')
    
    into = render_plugin_listing_into(plugin_list, into)
    into.append('\nPage ')
    into.append(str(page))
    into.append(' / ')
    into.append(str(get_plugins_page_count(plugins_sequence)))
    return ''.join(into)


def create_plugins_page_components(client, plugins_sequence, page):
    """
    Creates plugins page components.
    
    Parameters
    ----------
    client : `None | Client`
        Client to get page for.
    
    plugins_sequence : `sequence<Plugin>`
        A sequence of plugins to get page for.
    
    page : ``Page``
        Page number to create components for.
    
    Returns
    -------
    components : `list<Component>`
    """
    page_count = get_plugins_page_count(plugins_sequence)
    
    components = []
    
    components.append(
        Row(
            Button(
                f'Page {page - 1!s}',
                 EMOJI_LEFT,
                custom_id = create_custom_id_page_n(0 if client is None else client.id, page - 1),
                enabled = (page > 1),
                
            ),
            Button(
                f'Page {page + 1!s}',
                EMOJI_RIGHT,
                custom_id = create_custom_id_page_n(0 if client is None else client.id, page + 1),
                enabled = (page < page_count),
            ),
            Button(
                None,
                EMOJI_CLOSE,
                custom_id = CUSTOM_ID_PAGE_CLOSE,
            )
        )
    )
    
    if (client is not None):
        components.append(
            Row(
                Select(
                    [
                        Option(
                            format(option_client.id, 'x'),
                            option_client.full_name,
                            default = (option_client is client),
                        )
                        for option_client in islice(sorted(CLIENTS.values()), 0, 25)
                    ],
                    custom_id = create_custom_switch_client(page),
                    placeholder = 'Select a client',
                )
            )
        )
    
    return components


def get_plugin_by_name(name):
    """
    Gets a plugin by name.
    
    Parameters
    ----------
    name : `str`
        The plugin's name.
    
    Returns
    -------
    plugin : ``Plugin``
    
    Raises
    ------
    InteractionAbortedError
        - No plugin with name found.
        - The found plugin is locked.
    """
    plugin = get_plugin_like(name)
    if (plugin is None):
        abort('There is no plugin with the specified name.')
    
    if plugin.locked:
        abort('The plugin is locked, probably for reason.')
    
    return plugin


def _plugin_sort_key(plugin):
    """
    Sort key used to sort plugins.
    
    Parameters
    ----------
    plugin : ``Plugin``
        Plugin to get sort key of.
    
    Returns
    -------
    sort_key : `str`
    """
    return plugin.name


def get_plugin_list(plugins_sequence, page, page_size):
    """
    Gets a list of plugins.
    
    Parameters
    ----------
    plugins_sequence : `sequence<Plugin>`
        A sequence of plugins to filter from.
    
    page : ``Page``
        Page number to get.
    
    page_size : `int`
        The size of the page.
    
    Returns
    -------
    plugin_list : `list<Plugin>`
    """
    return sorted(plugins_sequence, key = _plugin_sort_key)[page_size * (page - 1) : page_size * page]


def render_plugin_listing_element_into(plugin, into):
    """
    Renders a plugin listing element.
    
    Parameters
    ----------
    plugin : ``Plugin``
        Element.
    
    into : `list<str>`
        Container to render into.
    
    Parameters
    ----------
    into : `list<str>`
    """
    into.append(plugin.name)
    
    if plugin.locked:
        into.append(' ')
        into.append(VALUE_LOCKED)
    
    into.append('\n')
    return into


def get_plugin_listing_element_length(plugin):
    """
    Get plugin listing element's rendered form's length.
    
    Parameters
    ----------
    plugin : ``Plugin``
        Element.
    
    Returns
    -------
    length : `int`
    """
    length = len(plugin.name) + 1
    
    if plugin.locked:
        length += len(VALUE_LOCKED) + 1
    
    return length


def render_plugin_iterable_elements(plugin_iterable, into):
    """
    Renders the plugin list elements.
    
    Parameters
    ----------
    plugin_iterable : `iterable<<Plugin>`
        The plugins to render.
    
    into : `list<str>`
        Container to render into.
    
    Returns
    -------
    into : `list<str>`
    """
    for plugin in plugin_iterable:
        render_plugin_listing_element_into(plugin, into)
    
    return into


def get_elements_truncation_point(plugin_list, truncate_at):
    """
    Gets where the elements should be truncated at.
    
    Parameters
    ----------
    plugin_list : `list<<Plugin>`
        The plugins to get truncation point of.
    truncate_at : `int`
        Where to truncate.
    
    Returns
    -------
    truncation_point : `int`
    """
    index = 0
    for element in plugin_list:
        length = get_plugin_listing_element_length(element)
        truncate_at -= length
        
        if truncate_at < 0:
            return index
        
        index += 1
        continue
    
    return index


def wrap_in_code_block(into):
    """
    Wraps the encapsulated block within code block.
    
    This function is a generator.
    
    Parameters
    ----------
    into : `list<str>`
        Container to render into.
    """
    into.append('```\n')
    yield
    into.append('```')


def render_plugin_listing_into(plugin_list, into):
    """
    Renders a list of plugins.
    
    Parameters
    ----------
    plugin_list : `list<<Plugin>`
        The plugins to render.
    into : `list<str>`
        Container to render into.
    
    Returns
    -------
    into : `list<str>`
    """
    for _ in wrap_in_code_block(into):
        render_plugin_iterable_elements(plugin_list, into)
    
    return into


def render_plugin_listing_with_truncation_into(plugin_list, truncate_at, into):
    """
    Renders a list of plugins.
    
    Parameters
    ----------
    plugin_list : `list<<Plugin>`
        The plugins to render.
    truncate_at : `int`
        Where to truncate.
    into : `list<str>`
        Container to render into.
    
    Returns
    -------
    into : `list<str>`
    """
    truncation_point = get_elements_truncation_point(plugin_list, truncate_at - 30)
    
    for _ in wrap_in_code_block(into):
        into = render_plugin_iterable_elements(islice(plugin_list, 0, truncation_point), into)
    
    truncated_count = len(plugin_list) - truncation_point
    if truncated_count:
        into.append('\n')
        into.append(str(truncated_count))
        into.append(' truncated.')
    
    return into


async def run_plugin_coroutine(coroutine):
    """
    Runs a plugin coroutine.
    
    This function is a coroutine.
    
    Parameters
    ----------
    coroutine : `CoroutineType | GeneratorType`
        The coroutine to run.
    
    Returns
    -------
    plugins_and_exception : `(None | list<Plugin>, None | PluginError`
        A tuple of 2 elements reloaded (if success) and the catched exception (if failure)
    """
    try:
        plugins = await coroutine
    except PluginError as exception:
        return None, exception
    else:
        return plugins, None


async def build_plugin_coroutine_result_response(plugin_name, action_name, plugins, exception):
    """
    Renders a plugin coroutine's result.
    
    This function is a coroutine.
    
    Parameters
    ----------
    plugin_name : `str`
        The plugin's name to execute action on.
    
    action_name : `str`
        The action's name.
    
    plugins : `None | list<Plugin>`
        The plugins the operation successfully finished on.
    
    exception : `None | PluginError`
        The occurred exception.
    
    Returns
    -------
    response : ``InteractionResponse``
    """
    description_parts = ['> ', action_name.title(), 'ing ']
    
    if (exception is None):
        description_parts.append('was successful!')
        if (plugins is not None):
            description_parts.append('\n')
            description_parts = render_plugin_listing_with_truncation_into(plugins, 1980, description_parts)
    
    else:
        description_parts.append(plugin_name)
        description_parts.append(' failed. ')
        description_parts.append(exception.message[:1980])
    
    
    content = ''.join(description_parts)
    
    
    if (exception is None):
        attachments = None
    else:
        attachments = [
            (
                'traceback.py',
                ''.join(await render_exception_into_async(exception, [], filter = frame_filter, loop = KOKORO)),
            ),
        ]
    
    return InteractionResponse(
        attachments = attachments,
        content = content,
    )
