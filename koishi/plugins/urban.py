__all__ = ()

from hata import Embed, Color, DATETIME_FORMAT_CODE, BUILTIN_EMOJIS
from hata.discord.utils import timestamp_to_datetime
from hata.ext.slash import abort
from scarletio.web_common import quote

from ..bots import MAIN_CLIENT


URBAN_DICTIONARY_API_URL = 'https://api.urbandictionary.com/v0/define'
URBAN_DICTIONARY_SEARCH_URL = 'https://www.urbandictionary.com/define.php?term='
# Response structure
# https://github.com/NightfallAlicorn/urban - dictionary#definitionobject


URBAN_COLOR = Color.from_rgb(207, 123, 87)

EMOJI_THUMBS_UP = BUILTIN_EMOJIS['thumbsup']
EMOJI_THUMBS_DOWN = BUILTIN_EMOJIS['thumbsdown']


def embrace_urban_markdown(text, text_length_limit):
    string_parts = []
    
    index = 0
    start_index = 0
    while True:
        link_start_index = text.find('[', index)
        if link_start_index == -1:
            if start_index == 0:
                string_parts.append(text)
            elif start_index != len(text):
                string_parts.append(text[start_index:])
            
            break
        
        if link_start_index and text[link_start_index - 1] == '\\':
            index = link_start_index + 1
            continue
        
        # add pre link.
        string_parts.append(text[start_index:link_start_index])
        
        # set position
        link_start_index = link_start_index + 1
        
        while True:
            link_end_index = text.find(']', index)
            if link_end_index == -1:
                break
            
            if text[link_end_index - 1] == '\\':
                index = link_end_index + 1
                continue
            
            link_content = text[link_start_index:link_end_index]
            string_parts.append(('[', link_content,'](', URBAN_DICTIONARY_SEARCH_URL, quote(link_content),')'))
            
            start_index = index = link_end_index + 1
            break
        
        # never ended link
        if link_end_index == -1:
            string_parts.append(text[link_start_index:])
            break
    
    string_parts_connectible = []
    for part in string_parts:
        if isinstance(part, str):
            part_length = len(part)
            
            text_length_limit -= part_length
            if text_length_limit < 0:
                string_parts_connectible.append(part[:text_length_limit])
                string_parts_connectible.append('...')
                break
            
            string_parts_connectible.append(part)
        
        else:
            part_length = 0
            for sub_part in part:
                part_length += len(sub_part)
            
            text_length_limit -= part_length
            
            if text_length_limit < 0:
                break
            
            string_parts_connectible.extend(part)
            continue
    
    return ''.join(string_parts_connectible)


@MAIN_CLIENT.interactions(is_global = True)
async def urban(
    client,
    event,
    term: ('str', 'The term to search'),
):
    """Finds the most accurate definition of the given term | Nsfw channel only"""
    
    channel = event.channel
    if (channel is None) or (not channel.nsfw):
        abort('Command only allowed in nsfw channels.')
    
    async with client.http.get(URBAN_DICTIONARY_API_URL, params={'term': term}) as response:
        if response.status != 200:
            abort(f'Something went wrong: status = {response.status!r} reason = {response.reason!r}.')
        
        data = await response.json()
    
    results = data.get('list', None)
    
    if (results is None) or (not results):
        return Embed(None, 'Could not find anything matching your term.', URBAN_COLOR)
    
    result = results[0]
    
    # Create base embed
    word = result['word']
    definition = result['definition']
    url = result['permalink']
    
    definition = embrace_urban_markdown(definition, 2000)
    
    embed = Embed(word, definition, url = url, color = URBAN_COLOR)
    
    # Add example
    example = result['example']
    
    if example:
        example = embrace_urban_markdown(example, 1000)
        
        embed.add_field('Example', example)
    
    # Add votes
    thumbs_up_count = result['thumbs_up']
    thumbs_down_count = result['thumbs_down']
    
    embed.add_field(
        EMOJI_THUMBS_UP.as_emoji,
        (
            f'```\n'
            f'{thumbs_up_count}\n'
            f'```'
        ),
        inline = True,
    ).add_field(
        EMOJI_THUMBS_DOWN.as_emoji,
        (
            f'```\n'
            f'{thumbs_down_count}\n'
            f'```'
        ),
        inline = True,
    )
    
    # Add footer
    author = result['author']
    created_at = timestamp_to_datetime(result['written_on'])
    
    if len(author) > 100:
        author = author[:100]+'...'
    
    embed.add_footer(f'By {author} at {created_at:{DATETIME_FORMAT_CODE}}')
    
    return embed
