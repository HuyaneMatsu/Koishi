__all__ = ()

from hata import Client, ClientUserBase, Embed, Permission
from hata.ext.plugin_loader import (
    PLUGINS, get_plugin, get_plugins_like, load_plugin, register_plugin, reload_plugin, unload_plugin
)
from hata.ext.slash import InteractionResponse, P, abort

from ...bot_utils.constants import GUILD__SUPPORT
from ...bots import MAIN_CLIENT

from .helpers import (
    check_permission, create_plugins_page_components, get_plugin_by_name, get_plugins_sequence,
    build_plugin_coroutine_result_response, render_plugins_page, run_plugin_coroutine
)


PLUGIN_COMMANDS = MAIN_CLIENT.interactions(
    None,
    name = 'plugin',
    description = 'plugin related commands',
    guild = GUILD__SUPPORT,
    required_permissions = Permission().update_by_keys(administrator = True),
)


@PLUGIN_COMMANDS.interactions
async def load(
    event,
    name: ('str', 'Please provide a name to load.'),
    deep: ('bool', 'You know what it means :3') = True,
):
    """
    Loads the specified plugin by it's name.
    
    Parameters
    ----------
    event : ``InteractionEvent``
        The received interaction event.
    name : ˙str`
        The plugin's name to load.
    deep : `bool`
        Whether the whole related plugin tree should be loaded.
    
    Yields
    ------
    acknowledge / response : `None` / ``InteractionResponse``
    """
    check_permission(event)
    plugin = get_plugin_by_name(name)
    name = plugin.name
    
    yield
    plugins_and_exception = await run_plugin_coroutine(load_plugin(name, deep = deep))
    yield await build_plugin_coroutine_result_response(name, 'load', *plugins_and_exception)


@PLUGIN_COMMANDS.interactions
async def reload(
    event,
    name: ('str', 'Please provide a name to reload.'),
    deep: ('bool', 'You know what it means :3') = True,
):
    """
    Reloads the specified plugin by it's name.
    
    This function is a coroutine generator.
    
    Parameters
    ----------
    event : ``InteractionEvent``
        The received interaction event.
    name : ˙str`
        The plugin's name to reload.
    deep : `bool`
        Whether the whole related plugin tree should be reloaded.
    
    Yields
    ------
    acknowledge / response : `None` / ``InteractionResponse``
    """
    check_permission(event)
    
    plugin = get_plugin_by_name(name)
    name = plugin.name
    
    yield
    plugins_and_exception = await run_plugin_coroutine(reload_plugin(name, deep = deep))
    yield await build_plugin_coroutine_result_response(name, 'reload', *plugins_and_exception)


@PLUGIN_COMMANDS.interactions
async def unload(
    event,
    name: ('str', 'Please provide a name to unload.'),
    deep: ('bool', 'You know what it means :3') = True,
):
    """
    Unloads the specified plugin by it's name.
    
    This function is a coroutine generator.
    
    Parameters
    ----------
    event : ``InteractionEvent``
        The received interaction event.
    name : ˙str`
        The plugin's name to unload.
    deep : `bool`
        Whether the whole related plugin tree should be unloaded.
    
    Yields
    ------
    acknowledge / response : `None` / ``InteractionResponse``
    
    """
    check_permission(event)
    
    plugin = get_plugin_by_name(name)
    name = plugin.name
    
    yield
    plugins_and_exception = await run_plugin_coroutine(unload_plugin(name, deep = deep))
    yield await build_plugin_coroutine_result_response(name, 'unload', *plugins_and_exception)


@PLUGIN_COMMANDS.interactions
async def register(
    event,
    name: ('str', 'Please provide a name to register.'),
):
    """
    Registers the specified plugin by it's name.
    
    This function is a coroutine generator.
    
    Parameters
    ----------
    event : ``InteractionEvent``
        The received interaction event.
    name : `str`
        The name plugin's name to register.
    
    Yields
    ------
    acknowledge / response : `None` / ``Embed``
    """
    check_permission(event)
    
    plugin = get_plugin(name)
    if (plugin is not None):
        abort(f'There is already a plugin added with the given name: `{plugin.name}`.')
    
    yield
    
    try:
        register_plugin(name)
    except ImportError:
        title = f'Registering {name!r} plugin failed.'
        description = 'There is no such plugin.'
    else:
        title = f'Registering {name!r} was successful.'
        description = None
    
    yield Embed(title, description)


@PLUGIN_COMMANDS.interactions
async def discard_kept_commands(client, event):
    """
    Discards all the kept commands, which are not yet deleted.
    
    This function is a coroutine generator.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    event : ``InteractionEvent``
        The received interaction event.
    
    Yields
    ------
    response : ``Embed``
    """
    check_permission(event)
    
    yield Embed('Discarding')
    
    await client.slasher.discard_kept_commands()
    
    yield Embed('Finished')


@load.autocomplete('name')
@reload.autocomplete('name')
@unload.autocomplete('name')
async def autocomplete_plugin_name(event, value):
    """
    Auto completes the plugin's name.
    
    Parameters
    ----------
    event : ``InteractionEvent``
        The received interaction event.
    value : `None | str`
        The value to auto complete.
    
    Returns
    -------
    suggestions : `list<str>`
    """
    check_permission(event)
    
    if value is None:
        plugins = [*PLUGINS.values()]
    else:
        plugins = get_plugins_like(value)
    
    if not plugins:
        return None
    
    del plugins[20:]
    return [plugin.name for plugin in plugins]


@PLUGIN_COMMANDS.interactions
async def list_(
    event,
    page : P(int, 'The page to get', min_value = 1, max_value = 10000) = 1,
    selected_client : (ClientUserBase, 'Select a client to show their plugins of.') = None,
):
    """
    Lists the available plugins.
    
    This function is a coroutine.
    
    Parameters
    ----------
    event : ``InteractionEvent``
        The received event.
    page : `int` = `1`, Optional.
        Page number.
    selected_client : `None | ClientUserBase`
        Selected client to list the plugins of.
    
    Returns
    -------
    response : ``InteractionResponse``
    """
    check_permission(event)
    
    if (selected_client is not None) and (not isinstance(selected_client, Client)):
        abort('Did not select a valid client.')
    
    plugins_sequence = get_plugins_sequence(selected_client)
    return InteractionResponse(
        content = render_plugins_page(selected_client, plugins_sequence, page),
        components = create_plugins_page_components(selected_client, plugins_sequence, page),
    )
