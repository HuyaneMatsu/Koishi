from hata.ext.plugin_loader import register_plugin, load_plugin, get_plugin, reload_plugin, unload_plugin, \
    get_plugins_like, PLUGINS, PluginError, get_plugin_like
from hata import Embed, Client, CLIENTS, Permission
from hata.ext.slash import Select, Option, InteractionResponse, abort

from bot_utils.constants import GUILD__SUPPORT, ROLE__SUPPORT__ADMIN

SLASH_CLIENT : Client

def check_permission(event):
    if not event.user.has_role(ROLE__SUPPORT__ADMIN):
        abort(f'You must have {ROLE__SUPPORT__ADMIN.mention} to invoke this command.')

EXTENSION_COMMANDS = SLASH_CLIENT.interactions(
    None,
    name = 'plugin',
    description = 'plugin related commands',
    guild = GUILD__SUPPORT,
    required_permissions = Permission().update_by_keys(administrator=True),
)

EXTENSION_LIST_PER_GUILD_CUSTOM_ID = 'plugin.list_per_client'

@EXTENSION_COMMANDS.interactions
async def list_per_client(event):
    """Lists the plugins for each client."""
    check_permission(event)
    
    clients = sorted(CLIENTS.values())
    if len(clients) > 25:
        del clients[25:]
    
    client = clients[0]
    
    return list_per_client_get_response(client, clients)



@SLASH_CLIENT.interactions(custom_id=EXTENSION_LIST_PER_GUILD_CUSTOM_ID)
async def handle_list_per_client_component(event):
    if not event.user.has_role(ROLE__SUPPORT__ADMIN):
        return
    
    options = event.interaction.options
    
    client_detected = False
    while True:
        if options is None:
            break
        
        option = options[0]
    
        try:
            client_id = int(option)
        except ValueError:
            break
        
        try:
            client = CLIENTS[client_id]
        except KeyError:
            break
        
        client_detected = True
        break
    
    clients = sorted(CLIENTS.values())
    if len(clients) > 25:
        del clients[25:]
    
    if not client_detected:
        client = clients[0]
    
    return list_per_client_get_response(client, clients)


def list_per_client_get_response(selected_client, clients):
    description_parts = []
    
    plugins = selected_client.plugins
    limit = len(plugins)
    if limit:
        index = 0
        
        while True:
            plugin = plugins[index]
            index += 1
            
            description_parts.append('`')
            description_parts.append(plugin.name)
            description_parts.append('`')
            
            if index == limit:
                break
            
            description_parts.append('\n')
            continue
    
    else:
        description_parts.append('*No plugin detected.*')
    
    description = ''.join(description_parts)
    
    # Keep title building like this. Later we might alter it.
    title_parts = []
    
    title_parts.append('Extensions of ')
    title_parts.append(selected_client.full_name)
    title_parts.append(' (')
    title_parts.append(str(selected_client.id))
    title_parts.append(')')
    
    title = ''.join(title_parts)
    
    embed = Embed(title, description).add_thumbnail(selected_client.avatar_url)

    components = Select(
        [
            Option(str(client.id), client.full_name, default=(client is selected_client))
            for client in clients
        ],
        custom_id = EXTENSION_LIST_PER_GUILD_CUSTOM_ID,
        placeholder = 'Select a client',
    )
    
    return InteractionResponse(embed=embed, components=components)


EXTENSION_LIMIT = 40

def plugin_item_sort_key(item):
    return item[0]

@EXTENSION_COMMANDS.interactions
async def list_all(event):
    """Lists all the available plugins."""
    check_permission(event)
    
    items = sorted(
        ((plugin.name, plugin.locked) for plugin in PLUGINS.values()),
        key = plugin_item_sort_key,
    )
    
    items_length = len(items)
    if items_length:
        index = 0
        
        if items_length > EXTENSION_LIMIT:
            limit = EXTENSION_LIMIT
        else:
            limit = items_length
        
        description_parts = []
        
        while True:
            plugin_name, plugin_locked = items[index]
            index += 1
            
            description_parts.append('- `')
            description_parts.append(plugin_name)
            description_parts.append('`')
            
            if plugin_locked:
                description_parts.append('*(locked)*')
            
            if index == limit:
                break
            
            description_parts.append('\n')
            continue
        
        if limit > EXTENSION_LIMIT:
            description_parts.append('\n\n*')
            description_parts.append(str(limit - EXTENSION_LIMIT))
            description_parts.append(' truncated*')
        
        description = ''.join(description_parts)
    else:
        description = '*No plugins detected*'
    
    return Embed('Available plugins', description)


def get_plugin_by_name(name):
    plugin = get_plugin_like(name)
    if (plugin is None):
        abort('There is no plugin with the specified name.')
    
    if plugin.locked:
        abort('The plugin is locked, probably for reason.')
    
    return plugin


async def run_plugin_coroutine(plugin_name, action_name, coroutine):
    try:
        plugins = await coroutine
    except PluginError as err:
        title = f'{action_name.title()}ing {plugin_name} failed.'
        
        description = err.message
        if len(description) > 4000:
            description = description[-4000:]
    
    else:
        title = f'{action_name.title()}ing was successful!'
        
        description_length = 4
        description_parts = ['```\n']
        
        for plugin in plugins:
            plugin_name = plugin.name
            plugin_name_length = len(plugin_name)
            description_length += plugin_name_length + 1
            if description_length > 3993:
                description_parts.append('...\n')
                break
            
            description_parts.append(plugin_name)
            description_parts.append('\n')
            continue
        
        description_parts.append('\n```')
        
        description = ''.join(description_parts)
        description_parts = None
    
    return Embed(title, description)


@EXTENSION_COMMANDS.interactions
async def load(event,
    name: ('str', 'Please provide a name to load.'),
    deep: ('bool', 'you know what it means') = True,
):
    """Loads the specified plugin by it's name."""
    check_permission(event)
    plugin = get_plugin_by_name(name)
    
    yield
    name = plugin.name
    yield await run_plugin_coroutine(
        name,
        'load',
        load_plugin(name, deep=deep),
    )


@EXTENSION_COMMANDS.interactions
async def reload(event,
    name: ('str', 'Please provide a name to reload.'),
    deep: ('bool', 'you know what it means') = True,
):
    """Reloads the specified plugin by it's name."""
    check_permission(event)
    plugin = get_plugin_by_name(name)
    
    yield
    name = plugin.name
    yield await run_plugin_coroutine(
        name,
        'reload',
        reload_plugin(name, deep=deep),
    )


@EXTENSION_COMMANDS.interactions
async def unload(event,
    name: ('str', 'Please provide a name to unload.'),
    deep: ('bool', 'you know what it means') = True,
):
    """Unloads the specified plugin by it's name."""
    check_permission(event)
    plugin = get_plugin_by_name(name)
    
    yield
    name = plugin.name
    yield await run_plugin_coroutine(
        name,
        'unload',
        unload_plugin(name, deep=deep),
    )


@EXTENSION_COMMANDS.interactions
async def register(event,
    name: ('str', 'Please provide a name to register.'),
):
    """Registers the specified plugin by it's name."""
    check_permission(event)
    
    plugin = get_plugin(name)
    if (plugin is not None):
        abort(f'There is already an plugin added with the given name: `{plugin.name}`.')
    
    try:
        register_plugin(name)
    except ImportError:
        title = f'Registering {name!r} plugin failed.'
        description = 'There is no such plugin.'
    else:
        title = f'Registering {name!r} was successful.'
        description = None
    
    return Embed(title, description)


@EXTENSION_COMMANDS.interactions
async def discard_kept_commands(client, event):
    """Discards all the kept commands, which are not yet deleted."""
    check_permission(event)
    
    yield Embed('Discarding')
    
    await client.slasher.discard_kept_commands()
    
    yield Embed('Finished')


@load.autocomplete('name')
@reload.autocomplete('name')
@unload.autocomplete('name')
async def autocomplete_plugin_name(value):
    if value is None:
        plugins = list(PLUGINS.values())
    else:
        plugins = get_plugins_like(value)
    
    if not plugins:
        return None
    
    del plugins[20:]
    return [plugin.name for plugin in plugins]
