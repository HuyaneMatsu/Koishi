# -*- coding: utf-8 -*-

from hata import Client, Embed, DATETIME_FORMAT_CODE

from bot_utils.shared import CHANNEL__NEKO_DUNGEON_LOG, GUILD__NEKO_DUNGEON

Koishi: Client
def setup(lib):
    Koishi.events.message_create.append(GUILD__NEKO_DUNGEON, logger)

def teardown(lib):
    Koishi.events.message_create.remove(GUILD__NEKO_DUNGEON, logger)

CLEAN_CONTENT_MAX_LENGTH = 1000
USER_MENTION_MAX = 7
ROLE_MENTION_MAX = 5
SEPARATOR_LINE = '\\_'*30

async def logger(client, message):
    everyone_mention = message.everyone_mention
    user_mentions = message.user_mentions
    role_mentions = message.role_mentions
    
    if (not everyone_mention) and (user_mentions is None) and (role_mentions is None):
        return
    
    
    description_parts = []
    
    author = message.author
    
    guild = message.channel.guild
    if guild is None:
        nick = None
    else:
        try:
            guild_profile = author.guild_profiles[guild]
        except KeyError:
            nick = None
        else:
            nick = guild_profile.nick
    
    description_parts.append('**Author:** ')
    description_parts.append(author.full_name)
    description_parts.append(' ')
    if (nick is not None):
        description_parts.append('[')
        description_parts.append(nick)
        description_parts.append('] ')
    description_parts.append('(')
    description_parts.append(repr(author.id))
    description_parts.append(')\n')
    
    channel = message.channel
    description_parts.append('**Channel:** ')
    description_parts.append(channel.display_name)
    description_parts.append(' (')
    description_parts.append(repr(channel.id))
    description_parts.append(')\n')
    
    message_id = message.id
    description_parts.append('**Message id**: ')
    description_parts.append(repr(message_id))
    description_parts.append('\n')
    
    message_type = message.type
    description_parts.append('**Message type**: ')
    description_parts.append(message_type.name)
    description_parts.append(' (')
    description_parts.append(repr(message_type.value))
    description_parts.append(')\n')
    
    created_at = message.created_at
    description_parts.append('**Created at**: ')
    description_parts.append(created_at.__format__(DATETIME_FORMAT_CODE))
    description_parts.append('\n')
    
    content_length = len(message)
    description_parts.append('**Message Length:** ')
    description_parts.append(repr(content_length))
    description_parts.append('\n')
    
    description_parts.append('\n**Content**:\n')
    description_parts.append(SEPARATOR_LINE)
    description_parts.append('\n')
    
    clean_content = message.clean_content
    clean_content_length = len(clean_content)
    if clean_content_length > CLEAN_CONTENT_MAX_LENGTH:
        clean_content = clean_content[:CLEAN_CONTENT_MAX_LENGTH]
        truncated = clean_content_length - CLEAN_CONTENT_MAX_LENGTH
    else:
        truncated = 0
    
    description_parts.append(clean_content)
    if truncated:
        description_parts.append('\n*<Truncated )')
        description_parts.append(repr(truncated))
        description_parts.append('>*')
    
    description = ''.join(description_parts)
    embed = Embed('Ping Log!', description)
    
    if everyone_mention:
        embed.add_field('Everyone mention', 'Hecatia Yeah!')
    
    if (user_mentions is not None):
        field_value_parts = []
        
        mention_count = len(user_mentions)
        if mention_count > USER_MENTION_MAX:
            truncated = mention_count - USER_MENTION_MAX
        else:
            truncated = 0
        
        field_value_parts.append('**Total:** ')
        field_value_parts.append(repr(mention_count))
        if truncated:
            field_value_parts.append('(')
            field_value_parts.append(repr(truncated))
            field_value_parts.append(' truncated')
        field_value_parts.append('\n')
        field_value_parts.append(SEPARATOR_LINE)
        field_value_parts.append('\n')
        
        index = 0
        limit = mention_count-truncated
        
        while True:
            user = user_mentions[index]
            index += 1
            
            if guild is None:
                nick = None
            else:
                try:
                    guild_profile = user.guild_profiles[guild]
                except KeyError:
                    nick = None
                else:
                    nick = guild_profile.nick
            
            field_value_parts.append('**')
            field_value_parts.append(repr(index))
            field_value_parts.append('.:** ')
            field_value_parts.append(user.full_name)
            field_value_parts.append(' ')
            if (nick is not None):
                field_value_parts.append('[')
                field_value_parts.append(nick)
                field_value_parts.append('] ')
            field_value_parts.append('(')
            field_value_parts.append(repr(author.id))
            field_value_parts.append(')')
            
            if index == limit:
                break
            
            field_value_parts.append('\n')
            continue
        
        field_value = ''.join(field_value_parts)
        
        embed.add_field('User mentions', field_value)
    
    if (role_mentions is not None):
        field_value_parts = []
        
        mention_count = len(role_mentions)
        if mention_count > ROLE_MENTION_MAX:
            truncated = mention_count - ROLE_MENTION_MAX
        else:
            truncated = 0
        
        field_value_parts.append('**Total:** ')
        field_value_parts.append(repr(mention_count))
        if truncated:
            field_value_parts.append('(')
            field_value_parts.append(repr(truncated))
            field_value_parts.append(' truncated')
        field_value_parts.append('\n')
        field_value_parts.append(SEPARATOR_LINE)
        field_value_parts.append('\n')
        
        index = 0
        limit = mention_count-truncated
        
        while True:
            role = role_mentions[index]
            index += 1
            
            field_value_parts.append('**')
            field_value_parts.append(repr(index))
            field_value_parts.append('.:** ')
            field_value_parts.append(role.name)
            field_value_parts.append(' (')
            field_value_parts.append(repr(role.id))
            field_value_parts.append(')')
            
            if index == limit:
                break
            
            field_value_parts.append('\n')
            continue
        
        field_value = ''.join(field_value_parts)
        
        embed.add_field('Role mentions', field_value)
    
    await client.message_create(CHANNEL__NEKO_DUNGEON_LOG, embed=embed, allowed_mentions=None)
