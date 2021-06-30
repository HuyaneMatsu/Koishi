from hata.ext.extension_loader import EXTENSION_LOADER, EXTENSIONS
from hata import chunkify, Embed, Client, CLIENTS
from hata.ext.command_utils import Pagination
from hata.ext.commands_v2 import checks


COMMAND_CLIENT : Client
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
