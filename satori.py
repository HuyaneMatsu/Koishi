import re, sys
from random import random

from bs4 import BeautifulSoup

from hata import eventlist, DiscordException, sleep, Embed, Color, Task,    \
    BUILTIN_EMOJIS
from hata.py_hdrs import METH_GET
from hata.others import from_json
from hata.events import multievent, Pagination, Timeouter, GUI_STATE_READY, \
    GUI_STATE_SWITCHING_PAGE, GUI_STATE_CANCELLING, GUI_STATE_CANCELLED,    \
    GUI_STATE_SWITCHING_CTX


Koishi=NotImplemented

commands=eventlist()

@commands
async def invalid_command(client,message,command,content):
    guild=message.guild
    if guild is None:
        try:
            await client.message_create('Eeh, what should I do, what should I do?!?!')
        except DiscordException:
            pass
        return
    
    if (guild in Koishi.guild_profiles) and message.channel.cached_permissions_for(Koishi).can_send_messages:
        try:
            needs_content,command=Koishi.events.message_create.commands[command]
        except KeyError:
            pass
        else:
            await client.typing(message.channel)
            await sleep(2.0,client.loop)
            await client.message_create(message.channel,f'Lemme ask my Sister, {Koishi.name_at(guild)}.')
            await Koishi.typing(message.channel)
            await sleep((random()*2.)+1.0,client.loop)
            if needs_content:
                await command(Koishi,message,content)
            else:
                await command(Koishi,message)
            return
    
    await client.message_create(message.channel,'I have no idea, hmpff...')

WORDMATCH_RP    = re.compile('[^a-zA-z0-9]+')
WIKI_COLOR      = Color.from_rgb(48,217,255)

@commands
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
    
    async with client.http.request_(METH_GET,
            'https://en.touhouwiki.net/api.php?action=opensearch&search='
            f'{search_for}&limit=25&redirects=resolve&format=json&utf8',) as response:
        response_data = await response.text()
    
    results=[]
    while True:
        if len(response_data)<30:
            break

        json_data=from_json(response_data)
        if len(json_data)!=4:
            break

        for element in zip(json_data[1],json_data[3]):
            results.append(element)

        results.sort(key=lambda item:len(item[0]))
        break
    
    found=len(results)
    if found==0:
        await client.message_create(message.channel,embed=Embed(
            'No result',
            f'No search result for: `{search_for}`',
            color=WIKI_COLOR))
        return
    
    if found==1:
        pages = await download_wiki_page(client,results[0])
        await Pagination(client,message.channel,pages,timeout=600.0)
        return
    
    await TouhouWikiChooseMenu(client,message.channel,search_for,results)


class TouhouWikiChooseMenu(object):
    UP      = BUILTIN_EMOJIS['arrow_up_small']
    DOWN    = BUILTIN_EMOJIS['arrow_down_small']
    SELECT  = BUILTIN_EMOJIS['ok']
    CANCEL  = BUILTIN_EMOJIS['x']
    EMOJIS  = (UP,DOWN,SELECT,CANCEL)
    
    __slots__ = ('canceller', 'channel', 'client', 'embed', 'message', 'page',
        'results', 'task_flag', 'timeouter')
    
    async def __new__(cls,client,channel,search_for,results):
        self=object.__new__(cls)
        self.client=client
        self.channel=channel
        self.results=results
        
        self.page=0
        self.canceller=cls._canceller
        self.task_flag=GUI_STATE_READY
        self.timeouter=None
        
        self.embed=Embed(title=f'Search results for `{search_for}`',color=WIKI_COLOR)
        
        try:
            message = await client.message_create(channel,embed=self.render_embed())
        except DiscordException:
            self.message=None
            raise
        
        self.message=message
        
        if not channel.cached_permissions_for(client).can_add_reactions:
            return self
        
        message.weakrefer()
        for emoji in self.EMOJIS:
            await client.reaction_add(message,emoji)
        
        self.timeouter=Timeouter(client.loop,self,timeout=300.0)
        client.events.reaction_add.append(self,message)
        client.events.reaction_delete.append(self,message)
        return self
    
    def render_embed(self):
        lines=[]
        results=self.results
        page=self.page
        index=0
        limit=len(results)
        while True:
            element=results[index]
            title=element[0]
            if index==page:
                lines.append(f'**>>** **{title}**\n')
            else:
                lines.append(f'>> {title}\n')
            index=index+1
            if index==limit:
                break
        
        embed=self.embed
        embed.description=''.join(lines)
        return embed
    
    async def __call__(self,client,emoji,user):
        if user.is_bot or (emoji not in self.EMOJIS):
            return
        
        client=self.client
        message=self.message
        can_manage_messages=self.channel.cached_permissions_for(client).can_manage_messages
        
        if can_manage_messages:
            if not message.did_react(emoji,user):
                return
            Task(self.reaction_remove(client,message,emoji,user),client.loop)
        
        task_flag=self.task_flag
        if task_flag!=GUI_STATE_READY:
            if task_flag==GUI_STATE_SWITCHING_PAGE:
                if emoji is self.CANCEL:
                    task_flag=GUI_STATE_CANCELLING
                return
            
            # ignore GUI_STATE_CANCELLED and GUI_STATE_SWITCHING_CTX
            return
        
        while True:
            if emoji is self.UP:
                page=self.page-1
                break
            
            if emoji is self.DOWN:
                page=self.page+1
                break
            
            if emoji is self.CANCEL:
                self.task_flag=GUI_STATE_CANCELLED
                try:
                    await client.message_delete(message)
                except DiscordException:
                    pass
                self.cancel()
                return
            
            if emoji is self.SELECT:
                self.task_flag=GUI_STATE_SWITCHING_CTX
                if self.channel.cached_permissions_for(client).can_manage_messages:
                    await client.reaction_clear(message)
                else:
                    for emoji in self.EMOJIS:
                        await client.reaction_delete_own(message,emoji)
                
                self.cancel()
                pages = await download_wiki_page(client,self.results[self.page])
                await client.message_edit(message,embed=pages[0])
                await Pagination(client,message.channel,pages,timeout=600.0,message=message)
                return
            
            return
        
        if page<0:
            page=0
        elif page>=len(self.results):
            page=len(self.results)-1
        
        if self.page==page:
            return
        
        self.page=page
        self.task_flag=GUI_STATE_SWITCHING_PAGE
        try:
            await client.message_edit(message,embed=self.render_embed())
        except DiscordException:
            self.task_flag=GUI_STATE_CANCELLED
            self.cancel()
            return

        if self.task_flag==GUI_STATE_CANCELLING:
            self.task_flag=GUI_STATE_CANCELLED
            if can_manage_messages:
                try:
                    await client.message_delete(message)
                except DiscordException:
                    pass
            self.cancel()
            return
        
        self.task_flag=GUI_STATE_READY
        
        timeouter=self.timeouter
        if timeouter.timeout<240.:
            timeouter.timeout+=30.
    
    @staticmethod
    async def reaction_remove(client,message,emoji,user):
        try:
            await client.reaction_delete(message,emoji,user)
        except DiscordException:
            pass
    
    async def _canceller(self,exception,):
        client=self.client
        message=self.message
        
        client.events.reaction_add.remove(self,message)
        client.events.reaction_delete.remove(self,message)
        
        if self.task_flag==GUI_STATE_SWITCHING_CTX:
            # the message is not our, we should not do anything with it.
            return

        self.task_flag=GUI_STATE_CANCELLED
        
        if exception is None:
            return
        
        if isinstance(exception,TimeoutError):
            if self.channel.cached_permissions_for(client).can_manage_messages:
                try:
                    await client.reaction_clear(message)
                except DiscordException:
                    pass
            return
        
        timeouter=self.timeouter
        if timeouter is not None:
            timeouter.cancel()
        #we do nothing
    
    def cancel(self):
        canceller=self.canceller
        if canceller is None:
            return
        
        self.canceller=None
        
        timeouter=self.timeouter
        if timeouter is not None:
            timeouter.cancel()
        
        return Task(canceller(self,None),self.client.loop)

async def download_wiki_page(client,result):
    async with client.http.request_(METH_GET,result[1]) as response:
        response_data = await response.text()
    soup=BeautifulSoup(response_data,'html.parser')
    block=soup.find_all('div',class_='mw-parser-output')[2]

    last=[]
    title_parts=[result[0]]

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
                                url=sub.attrs['href']
                                title=sub.attrs['title']
                                text=f'*Main article: [{title}](https://en.touhouwiki.net{url})*\n'
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
                url=sub.attrs['href']
                title=sub.attrs['title']
                text=f'*Main article: [{title}](https://en.touhouwiki.net{url})*\n'
                last.append(text)
                
                continue
            
            continue
        
        if element_name=='ul':
            continue #spellcard table?
        
        sys.stderr.write('Unhandled element at `TouhouWikiPage.__new__` : ')
        sys.stderr.write(element.__repr__())
        sys.stderr.write('\n')
        
    del last
    
    title=result[0]
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
    
    pages[0].url=result[1]
    
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

@commands
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


