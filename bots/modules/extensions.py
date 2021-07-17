import re

from hata.ext.extension_loader import EXTENSION_LOADER, EXTENSIONS
from hata import chunkify, Embed, Client, CLIENTS
from hata.ext.command_utils import Pagination
from hata.ext.commands_v2 import checks
from hata.ext.slash import Button, Row, set_permission, Select

from bot_utils.shared import GUILD__NEKO_DUNGEON, ROLE__NEKO_DUNGEON__ADMIN

COMMAND_CLIENT : Client
SLASH_CLIENT : Client
COMMAND_CLIENT.command_processor.create_category('EXTENSIONS', checks=checks.owner_only())

@COMMAND_CLIENT.commands(category='EXTENSIONS')
async def list_extensions(client, message):
    """
    Lists the registered extensions.
    """
    lines = []
    for extension in  EXTENSIONS.values():
        lines.append(f'- `{extension.name}`{" (locked)" if extension.locked else ""}')
    
    pages = [Embed('Available extensions', chunk) for chunk in chunkify(lines)]
    
    limit = len(pages)
    index = 0
    while index < limit:
        embed = pages[index]
        index += 1
        embed.add_footer(f'page {index}/{limit}')
    
    await Pagination(client, message.channel, pages)


@COMMAND_CLIENT.commands(category='EXTENSIONS')
async def load(name:str=None):
    """
    Loads the specified extension by it's name.
    """
    if name is None:
        return 'Please define an extension to load.'
    
    extension = EXTENSION_LOADER.get_extension(name)
    if (extension is None):
        return 'There is no extension with the specified name.'
    
    if extension.locked:
        return 'The extension is locked, probably for reason.'
    
    await EXTENSION_LOADER.load(extension.name)
    
    return 'Extension successfully loaded.'


@COMMAND_CLIENT.commands(category='EXTENSIONS')
async def register_extension(name:str=None):
    """
    Registers the specified extension by it's name.
    """
    if name is None:
        return 'Please define an extension to register.'
    
    if (EXTENSION_LOADER.get_extension(name) is not None):
        return 'There is already an extension added with the given name.'
    
    EXTENSION_LOADER.add(name)
    
    return 'Extension successfully loaded.'


@COMMAND_CLIENT.commands(category='EXTENSIONS')
async def reload(name:str=None):
    """
    Reloads the specified extension by it's name.
    """
    if name is None:
        return 'Please define an extension to reload.'
    
    extension = EXTENSION_LOADER.get_extension(name)
    if (extension is None):
        return 'There is no extension with the specified name.'
    
    if extension.locked:
        return 'The extension is locked, probably for reason.'
    
    await EXTENSION_LOADER.reload(extension.name)
        
    return 'Extension successfully reloaded.'


@COMMAND_CLIENT.commands(category='EXTENSIONS')
async def unload(name:str=None):
    """
    Unloads the specified extension by it's name.
    """
    if name is None:
        return 'Please define an extension to unload.'
    
    extension = EXTENSION_LOADER.get_extension(name)
    if (extension is None):
        return 'There is no extension with the specified name'
    
    if extension.locked:
        return 'The extension is locked, probably for reason.'
    
    await EXTENSION_LOADER.unload(extension.name)
        
    return 'Extension successfully unloaded.'


@COMMAND_CLIENT.commands(category='EXTENSIONS')
async def debug_extensions():
    """
    Lists extensions for each client.
    """
    result_parts = []
    
    for client in CLIENTS.values():
        result_parts.append(client.mention)
        result_parts.append(' :')
        result_parts.append('\n')
        extensions = client.extensions
        for extension in extensions:
            result_parts.append('`')
            result_parts.append(extension.name)
            result_parts.append('`')
            result_parts.append('\n')
        result_parts.append('\n')
    
    del result_parts[-2:]
    
    return ''.join(result_parts)

# TODO
"""
EXTENSION_COMMANDS = SLASH_CLIENT.interactions(
    set_permission(
        GUILD__NEKO_DUNGEON,
        ROLE__NEKO_DUNGEON__ADMIN,
        True)
    (None),
    name = 'extension',
    description = 'extension related commands',
    guild = GUILD__NEKO_DUNGEON,
    enabled_by_default = False
)

@EXTENSION_COMMANDS.interactions
async def list_per_client():
    pass

# Use select maybe?
async def get_client_extensions_components(selected_client):
    clients = sorted(CLIENTS.values)[:5] # Limit the number of clients for now.
    
    return Row(*(Button(
            client.full_name,
            custom_id = f'extension.list_per_client.{client.id}',
            enabled = (client is not selected_client)
        ) for client in clients))


def get_client_extensions_embed(client):
    description_parts = []
    
    extensions = client.extensions
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
    title_parts.append(client.full_name)
    title_parts.append(' (')
    title_parts.append(client.id)
    title_parts.append(')')
    
    title = ''.join(title_parts)
    
    return Embed(title, description).add_thumbnail(client.avatar_url)

"""
