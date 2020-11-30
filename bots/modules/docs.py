# -*- coding: utf-8 -*-
import re, sys
from math import ceil

from bs4 import BeautifulSoup

from hata import Color, Task, Embed, KOKORO, eventlist
from hata.ext.commands import ChooseMenu, Pagination, Command, Closer
from hata.discord.utils import from_json, chunkify

from bot_utils.shared import SATORI_HELP_COLOR

WORDMATCH_RP = re.compile('[^a-zA-z0-9]+')
WIKI_COLOR = Color.from_rgb(48, 217, 255)
HATA_DOCS_BASE_URL = 'https://huyanematsu.pythonanywhere.com/docs/'
HATA_DOCS_SEARCH_API = HATA_DOCS_BASE_URL + 'api/v1/search'

DOCS_COMMANDS = eventlist(type_=Command)

def setup(lib):
    Satori.commands.extend(DOCS_COMMANDS)

def teardown(lib):
    Satori.commands.unextend(DOCS_COMMANDS)

async def wiki_description(client, message):
    prefix = client.command_processer.get_prefix_for(message)
    return Embed('wiki',
        'Tries to find the given term on the touhou wiki and then shows up the results to choose, or if only one thing '
        'was found, shows that instantly.\n'
        f'Usage: `{prefix}wiki *search-term*`',
        color=WIKI_COLOR)

@DOCS_COMMANDS(description=wiki_description)
async def wiki(client, message, content):
    if not content:
        await client.message_create(message.channel, embed=Embed(
            'No result',
            'Nothing was passed to search for.',
            color=WIKI_COLOR))
        return
    
    words = WORDMATCH_RP.split(content)
    search_for = ' '.join(words)
    
    # this takes a while, lets type a little.
    Task(client.typing(message.channel), KOKORO)
    
    async with client.http.get(
            'https://en.touhouwiki.net/api.php?action=opensearch&search='
            f'{search_for}&limit=25&redirects=resolve&format=json&utf8',) as response:
        response_data = await response.text()
    
    while True:
        if len(response_data) < 30:
            results = None
            break
        
        json_data = from_json(response_data)
        if len(json_data) != 4:
            results = None
            break
        
        results = list(zip(json_data[1], json_data[3]))
        results.sort(key=lambda item: len(item[0]))
        break
    
    if (results is None) or (not results):
        await client.message_create(message.channel, embed=Embed(
            'No result',
            f'No search result for: `{search_for}`',
            color=WIKI_COLOR))
        return
    
    embed = Embed(title=f'Search results for `{search_for}`', color=WIKI_COLOR)
    await ChooseMenu(client, message.channel, results, wiki_page_selected, embed=embed, prefix='>>')

async def wiki_page_selected(client, channel, message, title, url):
    pages = await download_wiki_page(client, title, url)
    await Pagination(client, channel, pages, timeout=600.0, message=message)

async def download_wiki_page(client, title_, url):
    async with client.http.get(url) as response:
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
            continue # sideinfo
        
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
                for index, element in enumerate(element.findAll('span', class_='reference-text'),1):
                
                    # check for error message from the wiki
                    subs = element.findAll(recursive=False)
                    for index_ in range(len(subs)):
                        sub = subs[index_]
                        classes=sub.attrs.get('class')
                        if (classes is not None) and ('error' in classes):
                            errored=True
                            break
                    else:
                        errored=False
                    
                    if errored:
                        if index_ == 0:
                            continue
                        
                        # `[n]`-s are missing, lets put them back
                        parts=['[', str(index), ']']
                        for index_ in range(index_):
                            parts.append(' ')
                            parts.append(subs[index_].text)
                        
                        parts.append('\n')
                        text=''.join(parts)
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
            continue # spellcard table?
        
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
                    section_ln=section_ln+len(block)
                    collected.append(block)
                
                index +=1
                if index == limit:
                    if collected:
                        sections.append('\n'.join(collected))
                        collected.clear()
                    break
                
                continue
            
            if section_ln+len(block)>1980:
            
                if section_ln > 1400:
                    collected.append('...')
                    sections.append('\n'.join(collected))
                    collected.clear()
                    collected.append('...')
                    collected.append(block)
                    section_ln = len(block)
                
                else:
                    max_ln = 1900-section_ln
                    break_point = block.find(' ', max_ln)
                    if break_point == -1 or break_point+80 > max_ln:
                        #too long word (lol category)
                        pre_part = block[:max_ln]+' ...'
                        post_part = '... '+block[max_ln:]
                    else:
                        #space found, brake next to it
                        pre_part = block[:break_point]+' ...'
                        post_part = '...'+block[break_point:]
                    
                    index +=1
                    blocks.insert(index, post_part)
                    limit +=1
                    collected.append(pre_part)
                    sections.append('\n'.join(collected))
                    collected.clear()
                    section_ln = 0
                    continue
            
            else:
                section_ln=section_ln+len(block)
                collected.append(block)
            
            index +=1
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
            pages.append(Embed(embed_title, embed_content, color=WIKI_COLOR))
        else:
            index = 0
            while True:
                embed_content=sections[index]
                index +=1
                if name is None:
                    embed_title = f'{title} ({index} / {limit})'
                else:
                    embed_title = f'{name} ({index} / {limit})'
                pages.append(Embed(embed_title, embed_content, color=WIKI_COLOR))
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

async def docs_help(client, message):
    prefix = client.command_processer.get_prefix_for(message)
    return Embed('docs', (
        'Searchers the given term in hata docs.\n'
        f'Usage: `{prefix}docs <search_for>`'
            ), color=SATORI_HELP_COLOR)

async def docs(client, message, search_for:str=None):
    if (search_for is None) or (len(search_for) < 4):
        embed = await docs_help(client, message)
        await Closer(client, message.channel, embed)
        return
    
    async with client.http.get(HATA_DOCS_SEARCH_API, params={'search_for': search_for}) as response:
        datas = await response.json()
    
    if not datas:
        embed = Embed(f'No search result for: `{search_for}`', color=WIKI_COLOR)
        await Closer(client, message.channel, embed)
        return
    
    sections = []
    section_parts = []
    for data in datas:
        section_parts.append('[**')
        name = data['name']
        section_parts.append(name)
        section_parts.append('**](')
        section_parts.append(HATA_DOCS_BASE_URL)
        url = data['url']
        section_parts.append(url)
        section_parts.append(') *')
        type_ = data['type']
        section_parts.append(type_)
        section_parts.append('*')
        preview = data.get('preview')
        if (preview is not None):
            section_parts.append('\n')
            section_parts.append(preview)
        
        section = ''.join(section_parts)
        sections.append(section)
        section_parts.clear()
    
    
    descriptions = []
    description_parts = []
    description_length = 0
    
    for section in sections:
        section_length = len(section)
        description_length += section_length
        if description_length > 2000:
            description = ''.join(description_parts)
            descriptions.append(description)
            description_parts.clear()
            
            description_parts.append(section)
            description_length = section_length
            continue
        
        if description_parts:
            description_parts.append('\n\n')
            description_length += 2
        
        description_parts.append(section)
        continue
    
    if description_parts:
        description = ''.join(description_parts)
        descriptions.append(description)
    
    
    title = f'Search results for guild `{search_for}`'
    
    embeds = []
    for index, description in enumerate(descriptions, 1):
        embed = Embed(title, description, color=WIKI_COLOR).add_footer(f'Page {index}/{len(descriptions)}')
        embeds.append(embed)
    
    await Pagination(client, message.channel, embeds)

DOCS_COMMANDS(docs, description=docs_help, aliases=['d'])

