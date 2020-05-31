# -*- coding: utf-8 -*-
import re, sys
from random import random

from bs4 import BeautifulSoup

from hata import DiscordException, sleep, Embed, Color, Task, ERROR_CODES, BUILTIN_EMOJIS
from hata.discord.others import from_json
from hata.ext.commands import setup_ext_commands, Pagination, ChooseMenu

from shared import SATORI_PREFIX

setup_ext_commands(Satori,SATORI_PREFIX)

@Satori.commands
async def invalid_command(client,message,command,content):
    guild=message.guild
    if guild is None:
        try:
            await client.message_create(message.channel,
                'Eeh, what should I do, what should I do?!?!')
        except BaseException as err:
            
            if isinstance(err,ConnectionError):
                # no internet
                return
            
            if isinstance(err,DiscordException):
                if err.code in (
                        ERROR_CODES.invalid_access, # client removed
                        ERROR_CODES.cannot_send_message_to_user, # dm disabled
                            ):
                    return
            
            await client.events.error(client,'invalid_command',err)
            return
        return
    
    if (Koishi in guild.clients) and message.channel.cached_permissions_for(Koishi).can_send_messages:
        try:
            command=Koishi.command_processer.commands[command]
        except KeyError:
            pass
        else:
            if command.category.name=='TOUHOU':
                await client.typing(message.channel)
                await sleep(2.0,client.loop)
                await client.message_create(message.channel,f'Lemme ask my Sister, {Koishi.name_at(guild)}.')
                await Koishi.typing(message.channel)
                await sleep((random()*2.)+1.0,client.loop)
                await command(Koishi,message,content)
                return
    
    await client.message_create(message.channel,'I have no idea, hmpff...')

WORDMATCH_RP    = re.compile('[^a-zA-z0-9]+')
WIKI_COLOR      = Color.from_rgb(48,217,255)

@Satori.commands
async def wiki(client,message,content):
    if not content:
        await client.message_create(message.channel,embed=Embed(
            'No result',
            'Nothing was passed to search for.',
            color=WIKI_COLOR))
        return
    
    words=WORDMATCH_RP.split(content)
    search_for=' '.join(words)
    
    # this takes a while, lets type a little.
    Task(client.typing(message.channel),client.loop)
    
    async with client.http.get(
            'https://en.touhouwiki.net/api.php?action=opensearch&search='
            f'{search_for}&limit=25&redirects=resolve&format=json&utf8',) as response:
        response_data = await response.text()
    
    while True:
        if len(response_data)<30:
            results=None
            break
        
        json_data=from_json(response_data)
        if len(json_data)!=4:
            results=None
            break
        
        results=list(zip(json_data[1],json_data[3]))
        results.sort(key=lambda item:len(item[0]))
        break
    
    if (results is None) or (not results):
        await client.message_create(message.channel,embed=Embed(
            'No result',
            f'No search result for: `{search_for}`',
            color=WIKI_COLOR))
        return
    
    embed = Embed(title=f'Search results for `{search_for}`',color=WIKI_COLOR)
    await ChooseMenu(client, message.channel, results, wiki_page_selected, embed=embed, prefix='>>')

async def wiki_page_selected(client, channel, message, title, url):
    pages = await download_wiki_page(client, title, url)
    await Pagination(client, channel, pages, timeout=600.0, message=message)

async def download_wiki_page(client, title_, url):
    async with client.http.get(url) as response:
        response_data = await response.text()
    soup=BeautifulSoup(response_data,'html.parser')
    block=soup.find_all('div',class_='mw-parser-output')[2]
    
    last=[]
    title_parts=[title_]
    
    contents=[(None,last),]
    
    for element in block.contents:
        element_name=element.name
        if element_name is None:
            continue #linebreak

        if element_name=='dl':
            for element in element.contents:
                element_name=element.name
                if element_name=='dt':
                    # sub sub sub title
                    last.append(f'**{element.text}**\n')
                    continue
                
                if element_name=='dd':
                    # check links
                    subs = element.findAll(recursive=False)
                    # if len(1)==1, then it might be a div
                    if len(subs)==1:
                        sub=subs[0]
                        # is it div?
                        if sub.name=='div':
                            classes=sub.attrs.get('class')
                            # is it main article link?
                            if (classes is not None) and ('mainarticle' in classes):
                                sub=sub.find('a')
                                url_=sub.attrs['href']
                                title=sub.attrs['title']
                                text=f'*Main article: [{title}](https://en.touhouwiki.net{url_})*\n'
                                last.append(text)
                                continue

                    text=element.text
                    if text.startswith('"') and text.endswith('"'):
                        text=f'*{text}*\n'
                    else:
                        text=text+'\n'
                    
                    last.append(text)
                    continue
                
                # rest is just linebreak
                continue
                
            continue
        
        if element_name=='table':
            continue #sideinfo
        
        if element_name=='p':
            text=element.text
            last.append(text)
            continue
        
        if element_name=='h2':
            element=element.findChild('span')
            text=element.text
            del title_parts[1:]
            title_parts.append(text)
            last=[]
            contents.append((' / '.join(title_parts),last),)
            continue
        
        if element_name=='h3':
            element=element.find('span',class_='mw-headline')
            text=element.text
            del title_parts[2:]
            title_parts.append(text)
            last=[]
            contents.append((' / '.join(title_parts),last),)
            continue
        
        if element_name=='div':
            
            if title_parts[-1]=='References': #keep reference
                for index,element in enumerate(element.findAll('span',class_='reference-text'),1):
                
                    # check for error message from the wiki
                    subs=element.findAll(recursive=False)
                    for index_ in range(len(subs)):
                        sub=subs[index_]
                        classes=sub.attrs.get('class')
                        if (classes is not None) and ('error' in classes):
                            errored=True
                            break
                    else:
                        errored=False
                    
                    if errored:
                        if index_==0:
                            continue
                        
                        # `[n]`-s are missing, lets put them back
                        parts=['[',index.__str__(),']']
                        for index_ in range(index_):
                            parts.append(' ')
                            parts.append(subs[index_].text)
                        
                        parts.append('\n')
                        text=''.join(parts)
                        # unallocate
                        del parts
                    else:
                        # `[n]`-s are missing, lets put them back
                        text=f'[{index}] {element.text}\n'
                    
                    last.append(text)
                
                continue
            
            #keep main article
            
            classes=element.attrs.get('class')
            if (classes is not None) and ('mainarticle' in classes):
                sub=element.find('a')
                url_=sub.attrs['href']
                title=sub.attrs['title']
                text=f'*Main article: [{title}](https://en.touhouwiki.net{url_})*\n'
                last.append(text)
                
                continue
            
            continue
        
        if element_name=='ul':
            continue #spellcard table?
        
        sys.stderr.write('Unhandled element at `TouhouWikiPage.__new__` : ')
        sys.stderr.write(repr(element))
        sys.stderr.write('\n')
        
    del last
    
    title=title_
    pages=[]
    
    sections=[]
    collected=[]
    for name,blocks in contents:
        limit=len(blocks)
        if limit==0:
            continue
        section_ln=0
        index=0
        
        while True:
            block=blocks[index]
            
            if (block.startswith('**') and block.endswith('**\n')):
                if section_ln>900:
                    sections.append('\n'.join(collected))
                    collected.clear()
                    collected.append(block)
                    section_ln=len(block)
                else:
                    section_ln=section_ln+len(block)
                    collected.append(block)
                
                index=index+1
                if index==limit:
                    if collected:
                        sections.append('\n'.join(collected))
                        collected.clear()
                    break
                
                continue
            
            if section_ln+len(block)>1980:
            
                if section_ln>1400:
                    collected.append('...')
                    sections.append('\n'.join(collected))
                    collected.clear()
                    collected.append('...')
                    collected.append(block)
                    section_ln=len(block)
                
                else:
                    max_ln=1900-section_ln
                    break_point=block.find(' ',max_ln)
                    if break_point==-1 or break_point+80>max_ln:
                        #too long word (lol category)
                        pre_part=block[:max_ln]+' ...'
                        post_part='... '+block[max_ln:]
                    else:
                        #space found, brake next to it
                        pre_part=block[:break_point]+' ...'
                        post_part='...'+block[break_point:]
                    
                    index=index+1
                    blocks.insert(index,post_part)
                    limit=limit+1
                    collected.append(pre_part)
                    sections.append('\n'.join(collected))
                    collected.clear()
                    section_ln=0
                    continue
            
            else:
                section_ln=section_ln+len(block)
                collected.append(block)
            
            index=index+1
            if index==limit:
                if collected:
                    sections.append('\n'.join(collected))
                    collected.clear()
                break
        
        limit=len(sections)
        if limit<2:
            if name is None:
                embed_title=title
            else:
                embed_title=name
            embed_content=sections[0]
            pages.append(Embed(embed_title,embed_content,color=WIKI_COLOR))
        else:
            index=0
            while True:
                embed_content=sections[index]
                index=index+1
                if name is None:
                    embed_title=f'{title} ({index} / {limit})'
                else:
                    embed_title=f'{name} ({index} / {limit})'
                pages.append(Embed(embed_title,embed_content,color=WIKI_COLOR))
                if index==limit:
                    break
        
        sections.clear()
    
    index=0
    limit=len(pages)
    while True:
        embed=pages[index]
        index=index+1
        embed.add_footer(f'Page: {index}/{limit}.')
        
        if index==limit:
            break
    
    pages[0].url=url
    return pages

TRANSFORMATIONS = {
    ' ':' ',
    '#':BUILTIN_EMOJIS['hash'].as_emoji,
    '*':BUILTIN_EMOJIS['asterisk'].as_emoji,
    '0':BUILTIN_EMOJIS['zero'].as_emoji,
    '1':BUILTIN_EMOJIS['one'].as_emoji,
    '2':BUILTIN_EMOJIS['two'].as_emoji,
    '3':BUILTIN_EMOJIS['three'].as_emoji,
    '4':BUILTIN_EMOJIS['four'].as_emoji,
    '5':BUILTIN_EMOJIS['five'].as_emoji,
    '6':BUILTIN_EMOJIS['six'].as_emoji,
    '7':BUILTIN_EMOJIS['seven'].as_emoji,
    '8':BUILTIN_EMOJIS['eight'].as_emoji,
    '9':BUILTIN_EMOJIS['nine'].as_emoji,
        }
    
for char in range(ord('a'),ord('z')+1):
    emoji=BUILTIN_EMOJIS['regional_indicator_'+chr(char)].as_emoji
    TRANSFORMATIONS[chr(char)]=emoji
    TRANSFORMATIONS[chr(char-32)]=emoji

del char, emoji

@Satori.commands
async def emojify(client, message, content):
    if not content:
        return
    
    if len(content)>80:
        await client.message_create(message.channel,'Message too long')
        return
    
    result=[]
    for char in content:
        try:
            emoji=TRANSFORMATIONS[char]
        except KeyError:
            pass
        else:
            result.append(emoji)

        continue
    
    result='\u200b'.join(result)
    # If the message is empty, we will check that anyways
    await client.message_create(message.channel,result)
    return


