__all__ = ()

import sys
from re import compile as re_compile

from hata import Embed, Color, Client
from hata.ext.command_utils import ChooseMenu, Pagination
from scarletio import from_json
from hata.ext.slash import abort
from hata.discord.http import LIBRARY_USER_AGENT
from scarletio.web_common.headers import USER_AGENT, CONTENT_TYPE
from hata.ext.plugin_loader import require

from bot_utils.tools import BeautifulSoup

# Touhou wiki blocks us, so this is always disabled
require(TOUHOU_WIKI_ENABLED=True)

WORD_MATCH_RP = re_compile('[^a-zA-z0-9]+')

HEADERS = {USER_AGENT: LIBRARY_USER_AGENT}

TOUHOU_WIKI_COLOR = Color.from_html('#138a50')

def touhou_wiki_result_sort_key(item):
    return len(item[0])

SLASH_CLIENT: Client

@SLASH_CLIENT.interactions(is_global = True)
async def touhou_wiki(client, event,
    search_for : ('str', 'Search term'),
):
    """Searches the given query in touhou wiki."""
    guild = event.guild
    if guild is None:
        abort('Guild only command')
    
    if (client.get_guild_profile_for(guild) is None):
        abort('I must be in the guild to execute this command.')
    
    words = WORD_MATCH_RP.split(search_for)
    search_for = ' '.join(words)
    
    yield
    
    async with client.http.get(
        f'https://en.touhouwiki.net/api.php?action=opensearch&search={search_for}&limit=25&redirects=resolve&'
        f'format=json&utf8',
        headers = HEADERS
    ) as response:
        response_data = await response.read()
        response_headers = response.headers
    
    content_type_header = response_headers.get(CONTENT_TYPE, None)
    if (content_type_header is not None) and content_type_header.startswith('application/json'):
        json_data = from_json(response_data)
        
        results = list(zip(json_data[1], json_data[3]))
        results.sort(key = touhou_wiki_result_sort_key)
    
    else:
        results = None
    
    if (results is None) or (not results):
        yield Embed(
            'No result',
            f'No search result for: `{search_for}`',
            color = TOUHOU_WIKI_COLOR,
        )
        return
    
    embed = Embed(f'Search results for `{search_for}`', color = TOUHOU_WIKI_COLOR)
    await ChooseMenu(client, event, results, wiki_page_selected, embed = embed, prefix = '>>')

async def wiki_page_selected(client, channel, message, title, url):
    pages = await download_wiki_page(client, title, url)
    await Pagination(client, channel, pages, timeout = 600.0, message = message)


async def download_wiki_page(client, title_, url):
    async with client.http.get(url, headers=HEADERS) as response:
        response_data = await response.text()
    soup = BeautifulSoup(response_data, 'html.parser')
    
    block = soup.find_all('div', class_='mw-parser-output')[2]
    
    last = []
    title_parts = [title_]
    
    contents = [(None, last),]
    
    for element in block.contents:
        element_name = element.name
        if element_name is None:
            continue #linebreak
        
        if element_name == 'dl':
            for element in element.contents:
                element_name = element.name
                if element_name == 'dt':
                    # sub sub sub title
                    last.append(f'**{element.text}**\n')
                    continue
                
                if element_name == 'dd':
                    # check links
                    subs = element.findAll(recursive=False)
                    # if len(1)==1, then it might be a div
                    if len(subs) == 1:
                        sub = subs[0]
                        # is it div?
                        if sub.name == 'div':
                            classes = sub.attrs.get('class')
                            # is it main article link?
                            if (classes is not None) and ('mainarticle' in classes):
                                sub = sub.find('a')
                                url_ = sub.attrs['href']
                                title = sub.attrs['title']
                                text = f'*Main article: [{title}](https://en.touhouwiki.net{url_})*\n'
                                last.append(text)
                                continue
                    
                    text = element.text
                    if text.startswith('"') and text.endswith('"'):
                        text = f'*{text}*\n'
                    else:
                        text = text+'\n'
                    
                    last.append(text)
                    continue
                
                # rest is just linebreak
                continue
                
            continue
        
        if element_name == 'table':
            continue # side info
        
        if element_name == 'p':
            text = element.text
            last.append(text)
            continue
        
        if element_name == 'h2':
            element = element.findChild('span')
            text = element.text
            del title_parts[1:]
            title_parts.append(text)
            last = []
            contents.append((' / '.join(title_parts), last),)
            continue
        
        if element_name == 'h3':
            element = element.find('span', class_='mw-headline')
            text = element.text
            del title_parts[2:]
            title_parts.append(text)
            last = []
            contents.append((' / '.join(title_parts), last),)
            continue
        
        if element_name == 'div':
            
            if title_parts[-1] == 'References': #keep reference
                for index, element in enumerate(element.findAll('span', class_='reference-text'), 1):
                
                    # check for error message from the wiki
                    subs = element.findAll(recursive=False)
                    for index_ in range(len(subs)):
                        sub = subs[index_]
                        classes = sub.attrs.get('class')
                        if (classes is not None) and ('error' in classes):
                            errored = True
                            break
                    else:
                        errored = False
                    
                    if errored:
                        if index_ == 0:
                            continue
                        
                        # `[n]`-s are missing, lets put them back
                        parts=['[', str(index), ']']
                        for index_ in range(index_):
                            parts.append(' ')
                            parts.append(subs[index_].text)
                        
                        parts.append('\n')
                        text = ''.join(parts)
                        # unallocate
                        del parts
                    else:
                        # `[n]`-s are missing, lets put them back
                        text = f'[{index}] {element.text}\n'
                    
                    last.append(text)
                
                continue
            
            #keep main article
            
            classes = element.attrs.get('class')
            if (classes is not None) and ('mainarticle' in classes):
                sub = element.find('a')
                url_ = sub.attrs['href']
                title = sub.attrs['title']
                text = f'*Main article: [{title}](https://en.touhouwiki.net{url_})*\n'
                last.append(text)
                
                continue
            
            continue
        
        if element_name == 'ul':
            continue # spell card table?
        
        sys.stderr.write('Unhandled element at `TouhouWikiPage.__new__` : ')
        sys.stderr.write(repr(element))
        sys.stderr.write('\n')
        
    del last
    
    title = title_
    pages = []
    
    sections = []
    collected = []
    for name, blocks in contents:
        limit = len(blocks)
        if limit == 0:
            continue
        section_ln = 0
        index = 0
        
        while True:
            block = blocks[index]
            
            if (block.startswith('**') and block.endswith('**\n')):
                if section_ln > 900:
                    sections.append('\n'.join(collected))
                    collected.clear()
                    collected.append(block)
                    section_ln = len(block)
                else:
                    section_ln=section_ln + len(block)
                    collected.append(block)
                
                index +=1
                if index == limit:
                    if collected:
                        sections.append('\n'.join(collected))
                        collected.clear()
                    break
                
                continue
            
            if section_ln + len(block)>1980:
            
                if section_ln > 1400:
                    collected.append('...')
                    sections.append('\n'.join(collected))
                    collected.clear()
                    collected.append('...')
                    collected.append(block)
                    section_ln = len(block)
                
                else:
                    max_ln = 1900 - section_ln
                    break_point = block.find(' ', max_ln)
                    if break_point == -1 or break_point + 80 > max_ln:
                        # too long word (lol category)
                        pre_part = block[:max_ln]+' ...'
                        post_part = '... ' + block[max_ln:]
                    else:
                        # space found, brake next to it
                        pre_part = block[:break_point]+' ...'
                        post_part = '...' + block[break_point:]
                    
                    index += 1
                    blocks.insert(index, post_part)
                    limit += 1
                    collected.append(pre_part)
                    sections.append('\n'.join(collected))
                    collected.clear()
                    section_ln = 0
                    continue
            
            else:
                section_ln=section_ln + len(block)
                collected.append(block)
            
            index += 1
            if index == limit:
                if collected:
                    sections.append('\n'.join(collected))
                    collected.clear()
                break
        
        limit = len(sections)
        if limit < 2:
            if name is None:
                embed_title = title
            else:
                embed_title = name
            embed_content = sections[0]
            pages.append(Embed(embed_title, embed_content, color = TOUHOU_WIKI_COLOR))
        else:
            index = 0
            while True:
                embed_content = sections[index]
                index += 1
                if name is None:
                    embed_title = f'{title} ({index} / {limit})'
                else:
                    embed_title = f'{name} ({index} / {limit})'
                pages.append(Embed(embed_title, embed_content, color = TOUHOU_WIKI_COLOR))
                if index == limit:
                    break
        
        sections.clear()
    
    index = 0
    limit = len(pages)
    while True:
        embed = pages[index]
        index += 1
        embed.add_footer(f'Page: {index}/{limit}.')
        
        if index == limit:
            break
    
    pages[0].url = url
    return pages
