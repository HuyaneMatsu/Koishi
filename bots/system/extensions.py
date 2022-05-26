from re import compile as re_compile, escape as re_escape, I as re_ignore_case

from hata.ext.extension_loader import EXTENSION_LOADER, EXTENSIONS, ExtensionError
from hata import Embed, Client, CLIENTS
from hata.ext.slash import set_permission, Select, Option, InteractionResponse, abort

from bot_utils.constants import GUILD__SUPPORT, ROLE__SUPPORT__ADMIN

SLASH_CLIENT : Client

def check_permission(event):
    if not event.user.has_role(ROLE__SUPPORT__ADMIN):
        abort(f'You must have {ROLE__SUPPORT__ADMIN.mention} to invoke this command.')

EXTENSION_COMMANDS = SLASH_CLIENT.interactions(
    set_permission(GUILD__SUPPORT, ROLE__SUPPORT__ADMIN, True) @ set_permission(GUILD__SUPPORT, ('role', 0), False),
    name = 'extension',
    description = 'extension related commands',
    guild = GUILD__SUPPORT,
)

EXTENSION_LIST_PER_GUILD_CUSTOM_ID = 'extension.list_per_client'

@EXTENSION_COMMANDS.interactions
async def list_per_client(event):
    """Lists the extensions for each client."""
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
    
    extensions = selected_client.extensions
    limit = len(extensions)
    if limit:
        index = 0
        
        while True:
            extension = extensions[index]
            index += 1
            
            description_parts.append('`')
            description_parts.append(extension.name)
            description_parts.append('`')
            
            if index == limit:
                break
            
            description_parts.append('\n')
            continue
    
    else:
        description_parts.append('*No extension detected.*')
    
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

def extension_item_sort_key(item):
    return item[0]

@EXTENSION_COMMANDS.interactions
async def list_all(event):
    """Lists all the available extensions."""
    check_permission(event)
    
    items = sorted(
        ((extension.name, extension.locked) for extension in EXTENSIONS.values()),
        key = extension_item_sort_key,
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
            extension_name, extension_locked = items[index]
            index += 1
            
            description_parts.append('- `')
            description_parts.append(extension_name)
            description_parts.append('`')
            
            if extension_locked:
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
        description = '*No extensions detected*'
    
    return Embed('Available extensions', description)


def get_extension_by_name(name):
    extension = EXTENSION_LOADER.get_extension(name)
    if (extension is None):
        abort('There is no extension with the specified name.')
    
    if extension.locked:
        abort('The extension is locked, probably for reason.')
    
    return extension


async def run_extension_coroutine(extension_name, action_name, coroutine):
    try:
        extensions = await coroutine
    except ExtensionError as err:
        title = f'{action_name.title()}ing {extension_name} failed.'
        
        description = err.message
        if len(description) > 4000:
            description = description[-4000:]
    
    else:
        title = f'{action_name.title()}ing was successful!'
        
        description_length = 4
        description_parts = ['```\n']
        
        for extension in extensions:
            extension_name = extension.name
            extension_name_length = len(extension_name)
            description_length += extension_name_length + 1
            if description_length > 3993:
                description_parts.append('...\n')
                break
            
            description_parts.append(extension_name)
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
    """Loads the specified extension by it's name."""
    check_permission(event)
    extension = get_extension_by_name(name)
    
    yield
    name = extension.name
    yield await run_extension_coroutine(
        name,
        'load',
        EXTENSION_LOADER.load(name, deep=deep),
    )


@EXTENSION_COMMANDS.interactions
async def reload(event,
    name: ('str', 'Please provide a name to reload.'),
    deep: ('bool', 'you know what it means') = True,
):
    """Reloads the specified extension by it's name."""
    check_permission(event)
    extension = get_extension_by_name(name)
    
    yield
    name = extension.name
    yield await run_extension_coroutine(
        name,
        'reload',
        EXTENSION_LOADER.reload(name, deep=deep),
    )


@EXTENSION_COMMANDS.interactions
async def unload(event,
    name: ('str', 'Please provide a name to unload.'),
    deep: ('bool', 'you know what it means') = True,
):
    """Unloads the specified extension by it's name."""
    check_permission(event)
    extension = get_extension_by_name(name)
    
    yield
    name = extension.name
    yield await run_extension_coroutine(
        name,
        'unload',
        EXTENSION_LOADER.unload(name, deep=deep),
    )


@EXTENSION_COMMANDS.interactions
async def register(event,
    name: ('str', 'Please provide a name to register.'),
):
    """Registers the specified extension by it's name."""
    check_permission(event)
    
    extension = EXTENSION_LOADER.get_extension(name)
    if (extension is not None):
        abort(f'There is already an extension added with the given name: `{extension.name}`.')
    
    try:
        EXTENSION_LOADER.add(name)
    except ImportError:
        title = f'Registering {name!r} extension failed.'
        description = 'There is no such extension.'
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
async def autocomplete_extension_name(value):
    if value is None:
        extensions = list(EXTENSIONS.values())
    else:
        extensions = []
        
        pattern = re_compile(re_escape(value), re_ignore_case)
        
        for extension in EXTENSIONS.values():
            if (not extension.locked) and (pattern.search(extension.name) is not None):
                extensions.append(extension)
    
    if not extensions:
        return None
    
    del extensions[20:]
    return [extension.name for extension in extensions]
