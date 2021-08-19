from hata import Client, Embed, StickerFormat
from hata.ext.extension_loader import require

from bot_utils.shared import CHANNEL__NEKO_DUNGEON__LOG_EMOJI, GUILD__NEKO_DUNGEON

require('Satori')

Satori: Client

def render_all_emoji_field(emoji):
    description_parts = []
    
    description_parts.append('**Name:** ')
    description_parts.append(emoji.name)
    
    
    description_parts.append(
        '\n'
        '**Animated:** '
    )
    description_parts.append('true' if emoji.animated else 'false')
    
    
    description_parts.append(
        '\n'
        '**Available:** '
    )
    description_parts.append('true' if emoji.available else 'false')
    
    
    description_parts.append(
        '\n'
        '**Allowed roles:** '
    )
    
    roles = emoji.roles
    if (roles is None):
        description_parts.append('null')
    else:
        index = 0
        limit = len(roles)
        
        while True:
            role = roles[index]
            index += 1
            
            description_parts.append(role.mention)
            
            if index == limit:
                break
            
            description_parts.append(', ')
            continue
    
    
    description_parts.append(
        '\n'
        '**Managed:** '
    )
    description_parts.append('true' if emoji.managed else 'false')
    
    
    description_parts.append(
        '\n'
        '**Require colons:** '
    )
    description_parts.append('true' if emoji.require_colons else 'false')
    
    
    return ''.join(description_parts)


@Satori.events
async def emoji_create(client, emoji):
    if emoji.guild is not GUILD__NEKO_DUNGEON:
        return
    
    description = render_all_emoji_field(emoji)
    emoji_url = emoji.url
    
    embed = Embed(f'Emoji created: {emoji.name} ({emoji.id})', description, url=emoji_url).add_thumbnail(emoji_url)
    
    await client.message_create(CHANNEL__NEKO_DUNGEON__LOG_EMOJI, embed=embed, allowed_mentions=None)


@Satori.events
async def emoji_edit(client, emoji, old_attributes):
    if emoji.guild is not GUILD__NEKO_DUNGEON:
        return
    
    description_parts = []
    
    try:
        old_name = old_attributes['name']
    except KeyError:
        pass
    else:
        new_name = emoji.name
        
        description_parts.append('**Name:** ')
        description_parts.append(old_name)
        description_parts.append(' -> ')
        description_parts.append(new_name)
    
    
    try:
        old_animated = old_attributes['animated']
    except KeyError:
        pass
    else:
        new_animated = emoji.animated
        
        if description_parts:
            description_parts.append('\n')
        
        description_parts.append('**Animated:** ')
        description_parts.append('true' if old_animated else 'false')
        description_parts.append(' -> ')
        description_parts.append('true' if new_animated else 'false')
    
    
    try:
        old_available = old_attributes['available']
    except KeyError:
        pass
    else:
        new_available = emoji.available
        
        if description_parts:
            description_parts.append('\n')
        
        description_parts.append('**Available:** ')
        description_parts.append('true' if old_available else 'false')
        description_parts.append(' -> ')
        description_parts.append('true' if new_available else 'false')
    
    
    try:
        old_roles = old_attributes['roles']
    except KeyError:
        pass
    else:
        new_roles = emoji.roles
        
        if description_parts:
            description_parts.append('\n')
        
        description_parts.append('**Allowed roles:** ')
        
        if (old_roles is None):
            description_parts.append('null')
        else:
            index = 0
            limit = len(old_roles)
            
            while True:
                role = old_roles[index]
                index += 1
                
                description_parts.append(role.mention)
        
                if index == limit:
                    break
                
                description_parts.append(', ')
                continue
        
        description_parts.append(' -> ')
        
        if (new_roles is None):
            description_parts.append('null')
        else:
            index = 0
            limit = len(new_roles)
            
            while True:
                role = new_roles[index]
                index += 1
                
                description_parts.append(role.mention)
        
                if index == limit:
                    break
                
                description_parts.append(', ')
                continue
        
        description_parts.append(' -> ')
    
    
    try:
        old_managed = old_attributes['managed']
    except KeyError:
        pass
    else:
        new_managed = emoji.managed
        
        if description_parts:
            description_parts.append('\n')
        
        description_parts.append('**Managed:** ')
        description_parts.append('true' if old_managed else 'false')
        description_parts.append(' -> ')
        description_parts.append('true' if new_managed else 'false')
    
    
    try:
        old_require_colons = old_attributes['require_colons']
    except KeyError:
        pass
    else:
        new_require_colons = emoji.require_colons
        
        if description_parts:
            description_parts.append('\n')
        
        description_parts.append('**Require colons:** ')
        description_parts.append('true' if old_require_colons else 'false')
        description_parts.append(' -> ')
        description_parts.append('true' if new_require_colons else 'false')
    
    
    description = ''.join(description_parts)
    emoji_url = emoji.url
    
    embed = Embed(f'Emoji edited: {emoji.name} ({emoji.id})', description, url=emoji_url).add_thumbnail(emoji_url)

    await client.message_create(CHANNEL__NEKO_DUNGEON__LOG_EMOJI, embed=embed, allowed_mentions=None)


@Satori.events
async def emoji_delete(client, emoji):
    if emoji.guild is not GUILD__NEKO_DUNGEON:
        return
    
    description = render_all_emoji_field(emoji)
    embed = Embed(f'Emoji deleted: {emoji.name} ({emoji.id})', description)
    
    await client.message_create(CHANNEL__NEKO_DUNGEON__LOG_EMOJI, embed=embed, allowed_mentions=None)


def render_all_sticker_field(sticker):
    description_parts = []
    
    description_parts.append('**Name:** ')
    description_parts.append(sticker.name)
    
    
    description_parts.append(
        '\n'
        '**Description:** '
    )
    description = sticker.description
    if (description is None):
        description_parts.append('null')
    else:
        description_parts.append(repr(description))
    
    
    description_parts.append(
        '\n'
        '**Format:** '
    )
    sticker_format = sticker.format
    description_parts.append(sticker_format.name)
    description_parts.append(' (')
    description_parts.append(str(sticker_format.value))
    description_parts.append(')')
    
    
    description_parts.append(
        '\n'
        '**Available:** '
    )
    description_parts.append('true' if sticker.available else 'false')
    
    
    description_parts.append(
        '\n'
        '**Tags:** '
    )
    tags = sticker.tags
    if (tags is None):
        description_parts.append('null')
    else:
        tags = sorted(tags)
        
        index = 0
        limit = len(tags)
        
        while True:
            tag = tags[index]
            index += 1
            
            description_parts.append(repr(tag))
            
            if index == limit:
                break
            
            description_parts.append(', ')
            continue
    
    
    return ''.join(description_parts)


@Satori.events
async def sticker_create(client, sticker):
    if sticker.guild is not GUILD__NEKO_DUNGEON:
        return
    
    description = render_all_sticker_field(sticker)
    sticker_url = sticker.url
    
    embed = Embed(f'Sticker created: {sticker.name} ({sticker.id})', description, url=sticker_url)
    
    sticker_format = sticker.format
    if (sticker_format is StickerFormat.png) or (sticker_format is StickerFormat.apng):
        embed.add_image(sticker_url)
    
    await client.message_create(CHANNEL__NEKO_DUNGEON__LOG_EMOJI, embed=embed, allowed_mentions=None)


@Satori.events
async def sticker_edit(client, sticker, old_attributes):
    if sticker.guild is not GUILD__NEKO_DUNGEON:
        return
    
    description_parts = []

    try:
        old_name = old_attributes['name']
    except KeyError:
        pass
    else:
        new_name = sticker.name
        
        description_parts.append('**Name:** ')
        description_parts.append(old_name)
        description_parts.append(' -> ')
        description_parts.append(new_name)
    
    
    try:
        old_description = old_attributes['description']
    except KeyError:
        pass
    else:
        new_description = sticker.description
        
        if description_parts:
            description_parts.append('\n')
        
        description_parts.append('**Description:** ')
        
        if (old_description is None):
            description_parts.append('null')
        else:
            description_parts.append(repr(old_description))
        
        description_parts.append(' -> ')
        
        if (new_description is None):
            description_parts.append('null')
        else:
            description_parts.append(repr(new_description))
    
    
    try:
        old_available = old_attributes['available']
    except KeyError:
        pass
    else:
        new_available = sticker.available
        
        if description_parts:
            description_parts.append('\n')
        
        description_parts.append('**Available:** ')
        description_parts.append('true' if old_available else 'false')
        description_parts.append(' -> ')
        description_parts.append('true' if new_available else 'false')
    
    
    try:
        old_tags = old_attributes['tags']
    except KeyError:
        pass
    else:
        new_tags = sticker.tags
        
        if description_parts:
            description_parts.append('\n')
        
        description_parts.append('**Tags:** ')
        
        if description_parts:
            description_parts.append('\n')
        
        if (old_tags is None):
            description_parts.append('null')
        else:
            tags = sorted(old_tags)
            
            index = 0
            limit = len(tags)
            
            while True:
                tag = tags[index]
                index += 1
                
                description_parts.append(repr(tag))
                
                if index == limit:
                    break
                
                description_parts.append(', ')
                continue
        
        description_parts.append(' -> ')
        
        if (new_tags is None):
            description_parts.append('null')
        else:
            tags = sorted(new_tags)
            
            index = 0
            limit = len(tags)
            
            while True:
                tag = tags[index]
                index += 1
                
                description_parts.append(repr(tag))
                
                if index == limit:
                    break
                
                description_parts.append(', ')
                continue
    
    
    description = ''.join(description_parts)
    sticker_url = sticker.url
    
    embed = Embed(f'Sticker edited: {sticker.name} ({sticker.id})', description, url=sticker_url)
    
    sticker_format = sticker.format
    if (sticker_format is StickerFormat.png) or (sticker_format is StickerFormat.apng):
        embed.add_image(sticker_url)
    
    await client.message_create(CHANNEL__NEKO_DUNGEON__LOG_EMOJI, embed=embed, allowed_mentions=None)


@Satori.events
async def sticker_delete(client, sticker):
    if sticker.guild is not GUILD__NEKO_DUNGEON:
        return
    
    description = render_all_sticker_field(sticker)
    embed = Embed(f'Sticker deleted: {sticker.name} ({sticker.id})', description)
    
    await client.message_create(CHANNEL__NEKO_DUNGEON__LOG_EMOJI, embed=embed, allowed_mentions=None)
