from hata import Embed, KOKORO, ERROR_CODES, DiscordException
from hata.ext.slash.menus import Pagination
from scarletio import render_exception_into_async
from random import choice
from .constants import DEFAULT_CATEGORY_NAME

def category_name_rule(name):
    if name is None:
        name = DEFAULT_CATEGORY_NAME
    else:
        name = name.capitalize()
    
    return name


async def command_error(client, message, command, content, exception):
    into = [
        client.full_name,
        ' ignores an occurred exception at command ',
        repr(command),
        '\n\nMessage details:\nGuild: ',
        repr(message.guild),
        '\nChannel: ',
        repr(message.channel),
        '\nAuthor: ',
        message.author.full_name,
        ' (',
        repr(message.author.id),
        ')\nContent: ',
        repr(content),
        '\n```py\n'
    ]
    
    await render_exception_into_async(exception, into, loop=KOKORO)
    into.append('```')
    
    lines = ''.join(into).splitlines()
    into = None
    
    pages = []
    
    page_length = 0
    page_contents = []
    
    index = 0
    limit = len(lines)
    
    while True:
        if index == limit:
            embed = Embed(description = ''.join(page_contents))
            pages.append(embed)
            page_contents = None
            break
        
        line = lines[index]
        index = index + 1
        
        line_length = len(line)
        # long line check, should not happen
        if line_length > 500:
            line = line[:500]+'...\n'
            line_length = 504
        
        if page_length + line_length > 1997:
            if index == limit:
                # If we are at the last element, we don\'t need to shard up,
                # because the last element is always '```'
                page_contents.append(line)
                embed = Embed(description = ''.join(page_contents))
                pages.append(embed)
                page_contents = None
                break
            
            page_contents.append('```')
            embed = Embed(description = ''.join(page_contents))
            pages.append(embed)
            
            page_contents.clear()
            page_contents.append('```py\n')
            page_contents.append(line)
            
            page_length = 6 + line_length
            continue
        
        page_contents.append(line)
        page_length += line_length
        continue
    
    limit = len(pages)
    index = 0
    while index < limit:
        embed = pages[index]
        index += 1
        embed.add_footer(f'page {index}/{limit}')
    
    await Pagination(client, message.channel, pages)




ERROR_MESSAGES = (
    'Something went wrong, please try again later.',
    'Error occurred.',
    # ...
)

def random_error_message_getter():
    return choice(ERROR_MESSAGES)


async def send_embed_to(client, user_id, embed, components = None):
    try:
        user_channel = await client.channel_private_create(user_id)
    except ConnectionError:
        return
    
    try:
        await client.message_create(
            user_channel,
            embed = embed,
            allowed_mentions = None,
            components = components,
        )
    except ConnectionError:
        return
    
    except DiscordException as err:
        if err.code == ERROR_CODES.cannot_message_user:
            return
        
        raise
    
    return
