# -*- coding: utf-8 -*-
from hata.ext.extension_loader import EXTENSION_LOADER, EXTENSIONS
from hata import chunkify,  Embed
from hata.ext.commands import checks, Pagination

main_client.command_processer.create_category('EXTENSIONS', checks=checks.owner_only())

@main_client.commands(category='EXTENSIONS')
async def list_extensions(client, message):
    """
    Lists the registered extensions.
    """
    lines = []
    for extension in  EXTENSIONS.values():
        lines.append(f'- `{extension.name}`{" (locked)" if extension.locked else ""}')
    
    pages = [Embed('Avaliable extensions', chunk) for chunk in chunkify(lines)]
    
    limit = len(pages)
    index = 0
    while index < limit:
        embed = pages[index]
        index += 1
        embed.add_footer(f'page {index}/{limit}')
    
    await Pagination(client, message.channel, pages)

@main_client.commands(category='EXTENSIONS')
async def load(client, message, name:str=None):
    """
    Loads the specified extension by it's name.
    """
    while True:
        if name is None:
            result = 'Please define an extension to load.'
            break
        
        try:
            extension = EXTENSION_LOADER.extensions[name]
        except KeyError:
            result = 'There is no extension with the specified name.'
            break
        
        if extension.locked:
            result = 'The extension is locked, probably for reason.'
            break
        
        try:
            await EXTENSION_LOADER.load(name)
        except BaseException as err:
            result = repr(err)
            if len(result) > 2000:
                result = result[-2000:]
            
            break
            
        result = 'Extension successfully loaded.'
        break
    
    await client.message_create(message.channel, result)
    return

@main_client.commands(category='EXTENSIONS')
async def register_extension(client, message, name:str=None):
    """
    Registers the specified extension by it's name.
    """
    while True:
        if name is None:
            result = 'Please define an extension to register.'
            break
        
        if name in EXTENSION_LOADER.extensions:
            result = 'There is already an extension added with the given name.'
            break
        
        try:
            EXTENSION_LOADER.add(name)
        except BaseException as err:
            result = repr(err)
            if len(result) > 2000:
                result = result[-2000:]
            
            break
            
        result = 'Extension successfully loaded.'
        break
    
    await client.message_create(message.channel, result)
    return

@main_client.commands(category='EXTENSIONS')
async def reload(client, message, name:str=None):
    """
    Reloads the specified extension by it's name.
    """
    while True:
        if name is None:
            result = 'Please define an extension to reload.'
            break
        
        try:
            extension = EXTENSION_LOADER.extensions[name]
        except KeyError:
            result = 'There is no extension with the specified name.'
            break
        
        if extension.locked:
            result = 'The extension is locked, probably for reason.'
            break
        
        try:
            await EXTENSION_LOADER.reload(name)
        except BaseException as err:
            result = repr(err)
            if len(result) > 2000:
                result = result[-2000:]
            
            break
            
        result = 'Extension successfully reloaded.'
        break
    
    await client.message_create(message.channel, result)
    return

@main_client.commands(category='EXTENSIONS')
async def unload(client, message, name:str=None):
    """
    Unloads the specified extension by it's name.
    """
    while True:
        if name is None:
            result = 'Please define an extension to unload.'
            break
        
        try:
            extension = EXTENSION_LOADER.extensions[name]
        except KeyError:
            result = 'There is no extension with the specified name'
            break
        
        if extension.locked:
            result = 'The extension is locked, probably for reason.'
            break
        
        try:
            await EXTENSION_LOADER.unload(name)
        except BaseException as err:
            result = repr(err)
            if len(result) > 2000:
                result = result[-2000:]
            
            break
            
        result = 'Extension successfully unloaded.'
        break
    
    await client.message_create(message.channel, result)
    return
