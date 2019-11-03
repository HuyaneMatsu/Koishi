from hata import eventlist,DiscordException,sleep,Embed,Color,BUILTIN_EMOJIS,Task
from random import random
from hata.py_hdrs import METH_GET
from hata.others import from_json
from hata.events import waitfor_wrapper,multievent
from bs4 import BeautifulSoup
import re

Koishi=NotImplemented

commands=eventlist()

@commands
async def invalid_command(client,message,command,content):
    guild=message.guild
    if guild is None:
        try:
            await client.message_cretae('Eeh, what should i do, what should i do?!?!')
        except DiscordException:
            pass
        return

    if (guild in Koishi.guild_profiles) and message.channel.cached_permissions_for(Koishi).can_send_messages:
        try:
            command=Koishi.events.message_create.commands[command]
        except KeyError:
            pass
        else:
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
        await TouhouWikiPage(client,message.channel,results[0],None)
        return

    await TouhouWikiChooseMenu(client,message.channel,search_for,results)


class TouhouWikiChooseMenu(object):
    UP      = BUILTIN_EMOJIS['arrow_up_small']
    DOWN    = BUILTIN_EMOJIS['arrow_down_small']
    SELECT  = BUILTIN_EMOJIS['ok']
    CANCEL  = BUILTIN_EMOJIS['x']
    EMOJIS  = [UP,DOWN,SELECT,CANCEL]
    async def __new__(cls,client,channel,search_for,results):
        self=object.__new__(cls)
        self.page=0
        self.channel=channel
        self.cancel=cls._cancel
        self.task_flag=0
        self.results=results
        self.embed=Embed(title=f'Search results for `{search_for}`',color=WIKI_COLOR)

        message = await client.message_create(channel,embed=self.render_embed())
        if not channel.cached_permissions_for(client).can_add_reactions:
            return self

        message.weakrefer()
        for emoji in self.EMOJIS:
            await client.reaction_add(message,emoji)

        waitfor_wrapper(client,self,300.,multievent(client.events.reaction_add,client.events.reaction_delete),message,)
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

    async def __call__(self,wrapper,emoji,user):
        if user.is_bot or (emoji not in self.EMOJIS):
            return

        client=wrapper.client
        message=wrapper.target
        can_manage_messages=self.channel.cached_permissions_for(client).can_manage_messages

        if can_manage_messages:
            if not message.did_react(emoji,user):
                return
            Task(self.reaction_remove(client,message,emoji,user),client.loop)

        if self.task_flag:
            if self.task_flag!=1 and (emoji is self.CANCEL):
                self.task_flag=2
            return

        while True:
            if emoji is self.UP:
                page=self.page-1
                break
            if emoji is self.DOWN:
                page=self.page+1
                break
            if emoji is self.CANCEL:
                self.task_flag=3
                try:
                    await client.message_delete(message)
                except DiscordException:
                    pass
                return wrapper.cancel()
            if emoji is self.SELECT:
                self.task_flag=4
                if self.channel.cached_permissions_for(client).can_manage_messages:
                    await client.reaction_clear(message)
                else:
                    for emoji in self.EMOJIS:
                        await client.reaction_delete_own(message,emoji)

                await TouhouWikiPage(client,self.channel,self.results[self.page],message)
                return wrapper.cancel()
            return

        if page<0:
            page=0
        elif page>=len(self.results):
            page=len(self.results)-1

        if self.page==page:
            return

        self.page=page
        self.task_flag=1
        try:
            await client.message_edit(message,embed=self.render_embed())
        except DiscordException:
            self.task_flag=3
            return wrapper.cancel()
        else:
            if self.task_flag==2:
                self.task_flag=3
                if can_manage_messages:
                    try:
                        await client.message_delete(message)
                    except DiscordException:
                        pass
                return wrapper.cancel()
            else:
                self.task_flag=0

        if wrapper.timeout<240.:
            wrapper.timeout+=30.

    @staticmethod
    async def reaction_remove(client,message,emoji,user):
        try:
            await client.reaction_delete(message,emoji,user)
        except DiscordException:
            pass

    @staticmethod
    async def _cancel(self,wrapper,exception):
        if self.task_flag==4:
            #we gave the message to a different object
            #we do nothing
            return

        self.task_flag=3
        if exception is None:
            return
        if isinstance(exception,TimeoutError):
            client=wrapper.client
            if self.channel.cached_permissions_for(client).can_manage_messages:
                try:
                    await client.reaction_clear(wrapper.target)
                except DiscordException:
                    pass
            return
        #we do nothing

class TouhouWikiPage(object):
    LEFT2   = BUILTIN_EMOJIS['track_previous']
    LEFT    = BUILTIN_EMOJIS['arrow_backward']
    RIGHT   = BUILTIN_EMOJIS['arrow_forward']
    RIGHT2  = BUILTIN_EMOJIS['track_next']
    CROSS   = BUILTIN_EMOJIS['x']
    EMOJIS  = [LEFT2,LEFT,RIGHT,RIGHT2,CROSS]

    __slots__=('cancel', 'channel', 'page', 'pages', 'task_flag',)

    async def __new__(cls,client,channel,result,message):
        async with client.http.request_(METH_GET,result[1]) as response:
            response_data = await response.text()
        soup=BeautifulSoup(response_data,'html.parser',from_encoding='utf-8')
        block=soup.find_all('div',class_='mw-parser-output')[2]

        last=[]
        title_parts=[result[0]]

        contents=[(None,last),]

        for element in block.contents:
            element_name=element.name
            if element_name is None:
                continue #linebreak

            if element_name=='dl':
                continue #startnote

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
                element=element.findChild('span')
                text=element.text
                del title_parts[2:]
                title_parts.append(text)
                last=[]
                contents.append((' / '.join(title_parts),last),)
                continue

            if element_name=='div':
                if title_parts[-1]=='Reference': #keep reference
                    last.append(element.text)
                continue #listing?

            if element_name=='ul':
                continue #spellcard table?

            print(element)

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
                if section_ln+len(block)>5080:
                    if section_ln>3000:
                        collected.append('...')
                        sections.append('\n'.join(collected))
                        collected.clear()
                        collected.append('...')
                        collected.append(block)
                        section_ln=len(block)
                    else:
                        max_ln=5000-section_ln
                        break_point=block.find(' ',max_ln)
                        if break_point==-1 or break_point+80>max_ln:
                            #too long word (lol category)
                            pre_part=block[:max_ln]+' ...'
                            post_part='... '+block[max_ln]
                        else:
                            #space found, brake next to it
                            pre_part=block[:break_point]+' ...'
                            post_part='...'+block[break_point]
                        index=index+1
                        blocks.insert(index,post_part)
                        limit=limit+1
                        collected.append(pre_part)
                        sections.append('\n\n'.join(collected))
                        collected.clear()
                        section_ln=0
                        continue

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
                    embed_title=name
                else:
                    embed_title=f'{title} / {name}'
                embed_content=sections[0]
                pages.append(Embed(embed_title,embed_content,color=WIKI_COLOR))
            else:
                index=0
                while True:
                    embed_content=sections[index]
                    index=index+1
                    if name is None:
                        embed_title=f'name ({index} / {limit})'
                    else:
                        embed_title=f'{title} / {name} ({index} / {limit})'
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

        self=object.__new__(cls)
        self.pages=pages
        self.page=0
        self.channel=channel
        self.cancel=cls._cancel
        self.task_flag=0

        if message is None:
            message = await client.message_create(channel,pages[0])
            if not channel.cached_permissions_for(client).can_add_reactions:
                return self

            message.weakrefer()

        if len(self.pages)>1:
            for emoji in self.EMOJIS:
                await client.reaction_add(message,emoji)
        else:
            await client.reaction_add(message,self.CROSS)

        waitfor_wrapper(client,self,600.,multievent(client.events.reaction_add,client.events.reaction_delete),message,)
        return self


    async def __call__(self,wrapper,emoji,user):
        if user.is_bot or (emoji not in self.EMOJIS):
            return

        client=wrapper.client
        message=wrapper.target
        can_manage_messages=self.channel.cached_permissions_for(client).can_manage_messages

        if can_manage_messages:
            if not message.did_react(emoji,user):
                return
            Task(self.reaction_remove(client,message,emoji,user),client.loop)

        if self.task_flag:
            if self.task_flag!=1 and (emoji is self.CROSS):
                self.task_flag=2
            return

        while True:
            if emoji is self.LEFT:
                page=self.page-1
                break
            if emoji is self.RIGHT:
                page=self.page+1
                break
            if emoji is self.CROSS:
                self.task_flag=3
                try:
                    await client.message_delete(message)
                except DiscordException:
                    pass
                return wrapper.cancel()
            if emoji is self.LEFT2:
                page=0
                break
            if emoji is self.RIGHT2:
                page=len(self.pages)-1
                break
            return

        if page<0:
            page=0
        elif page>=len(self.pages):
            page=len(self.pages)-1

        if self.page==page:
            return

        self.page=page
        self.task_flag=1
        try:
            await client.message_edit(message,embed=self.pages[page])
        except DiscordException:
            self.task_flag=3
            return wrapper.cancel()
        else:
            if self.task_flag==2:
                self.task_flag=3
                if can_manage_messages:
                    try:
                        await client.message_delete(message)
                    except DiscordException:
                        pass
                return wrapper.cancel()
            else:
                self.task_flag=0

        if wrapper.timeout<240.:
            wrapper.timeout+=30.

    @staticmethod
    async def reaction_remove(client,message,emoji,user):
        try:
            await client.reaction_delete(message,emoji,user)
        except DiscordException:
            pass

    @staticmethod
    async def _cancel(self,wrapper,exception):
        self.task_flag=3
        if exception is None:
            return
        if isinstance(exception,TimeoutError):
            client=wrapper.client
            if self.channel.cached_permissions_for(client).can_manage_messages:
                try:
                    await client.reaction_clear(wrapper.target)
                except DiscordException:
                    pass
            return
        #we do nothing
