# -*- coding: utf-8 -*-
import re, sys

from bs4 import BeautifulSoup

from hata import Color, Task, Embed, KOKORO, eventlist
from hata.ext.commands import ChooseMenu, Pagination, Command
from hata.discord.utils import from_json, chunkify
from hata.ext.patchouli import map_module, MAPPED_OBJECTS, QualPath, FolderedUnit, search_paths

from bot_utils.shared import SATORI_HELP_COLOR

WORDMATCH_RP = re.compile('[^a-zA-z0-9]+')
WIKI_COLOR = Color.from_rgb(48, 217, 255)

DOCS_COMMANDS = eventlist(type_=Command)

def setup(lib):
    Satori.commands.extend(DOCS_COMMANDS)

def teardown(lib):
    Satori.commands.unextend(DOCS_COMMANDS)

map_module('hata')

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
        index +=1
        embed.add_footer(f'Page: {index}/{limit}.')
        
        if index == limit:
            break
    
    pages[0].url = url
    return pages


async def docs_selecter(client, channel, message, name, path):
    unit = MAPPED_OBJECTS[path]
    chunks = unit.embed_sized
    
    title_parts = []
    path = unit.path - unit.name
    if path:
        title_parts.append('*')
        title_parts.append(str(path))
        title_parts.append('*.')
    
    title_parts.append('**')
    title_parts.append(unit.name)
    title_parts.append('**')
    
    title = ''.join(title_parts).replace('_', '\_')
    
    if chunks is None:
        embeds = [Embed(title, '*The given object has no description included*', color=WIKI_COLOR)]
    else:
        embeds = [Embed(title, chunk, color=WIKI_COLOR) for chunk in chunks]
    
    await Pagination(client, channel, embeds, message=message)

async def docs_help(client, message):
    prefix = client.command_processer.get_prefix_for(message)
    return Embed('docs', (
        'Searchers the given term in hata docs.\n'
        f'Usage: `{prefix}docs <search_for>`'
            ), color=SATORI_HELP_COLOR)

async def docs(client, message, search_for:str=None):
    if (search_for is None) or (len(search_for) < 4):
        await docs_help(client, message)
        return
    
    paths = search_paths(search_for)
    
    if not paths:
        embeds = [Embed(f'No search result for: `{search_for}`', color=WIKI_COLOR)]
        await Pagination(client, message.channel, embeds)
        return
    
    results = []
    
    for path in paths:
        name = str(path).replace('_', '\_')
        results.append((name, path))
    
    embed = Embed(title=f'Search results for `{search_for}`', color=WIKI_COLOR)
    await ChooseMenu(client, message.channel, results, docs_selecter, embed=embed, prefix='@')

DOCS_COMMANDS(docs, description=docs_help, aliases=['d'])


async def list_docs_selecter(client, channel, message, name, path):
    unit = MAPPED_OBJECTS[path]
    lines = []
    for name in unit.references:
        name = name.replace('_', '\_')
        lines.append('**¤** '+name)
    
    chunks = chunkify(lines)
    
    title_parts = []
    path = unit.path - unit.name
    if path:
        title_parts.append('*')
        title_parts.append(str(path))
        title_parts.append('*.')
    
    title_parts.append('**')
    title_parts.append(unit.name)
    title_parts.append('**')
    
    title = ''.join(title_parts).replace('_', '\_')
    
    if chunks is None:
        embeds = [Embed(title, '*The object has no attributes*', color=WIKI_COLOR)]
    else:
        embeds = [Embed(title, chunk, color=WIKI_COLOR) for chunk in chunks]
    
    await Pagination(client, channel, embeds, message=message)

async def list_docs_help(client, message):
    prefix = client.command_processer.get_prefix_for(message)
    return Embed('list-docs', (
        'Searchers the given type or module in hata docs.\n'
        f'Usage: `{prefix}list-docs <search_for>`'
            ), color=SATORI_HELP_COLOR)

async def list_docs(client, message, search_for:str=None):
    if (search_for is None) or (len(search_for)<4):
        await list_docs_help(client, message)
        return
    
    paths = search_paths(search_for)
    
    if not paths:
        embeds = [Embed(f'No search result for: `{search_for}`', color=WIKI_COLOR)]
        await Pagination(client, message.channel, embeds)
        return
    
    results = []
    
    for path in paths:
        name = str(path).replace('_', '\_')
        results.append((name, path))
    
    embed = Embed(title=f'Search results for `{search_for}`', color=WIKI_COLOR)
    await ChooseMenu(client, message.channel, results, list_docs_selecter, embed=embed, prefix='@')

DOCS_COMMANDS(list_docs, description=list_docs_help, aliases=['lsd'])
