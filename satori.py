from hata import eventlist,DiscordException,sleep,Embed
from random import random
from hata.py_hdrs import METH_GET
from hata.others import from_json
from bs4 import BeautifulSoup,Tag
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

WORDMATCH_RP    = re.compile('[^a-zA-z0-9]*')

class QueryResult(list):
    __slots__=()
    def __init__(self,words,raw_data):
        if len(raw_data)<30:
            return

        json_data=from_json(raw_data)
        if len(json_data)!=4:
            return

        if len(json_data[1])==1:
            self.append((json_data[1][0],json_data[3][0],),)
            return

        title_max_len=0
        for word in words:
            title_max_len+=len(word)
        title_max_len<<=1

        for index in range(len(words)):
            words[index]=words[index].lower()

        for title,url in zip(json_data[1],json_data[3]):
            if len(title)>title_max_len:
                continue

            lower_title=title.lower()
            for word in words:
                if word in lower_title:
                    continue
                else:
                    break
            else:
                continue

            self.append((title,url,),)

        found=len(self)
        if found==0:
            self.append((json_data[1][0],json_data[3][0],),)
            return

        if found==1:
            return

        self.sort(key=lambda item:len(item[0]))


@commands
async def wiki(client,message,content):
    await client.message_create(message.channel,'Work in progress..')
    return
    
##    if not content:
##        await client.message_create(message.channel,'No content passed')
##        return
##
##    words=WORDMATCH_RP.split(content)
##    search_for=' '.join(words)
##
##    async with client.http.request_(METH_GET,
##            'https://en.touhouwiki.net/api.php?action=opensearch&search='
##            f'{search_for}&limit=25&redirects=resolve&format=json&utf8',) as response:
##        response_data = await response.text()
##
##    result=QueryResult(words,response_data)
##
##    found=len(result)
##    if found==0:
##        await client.message_create(message.channel,'Nothing found')
##        return
##
##    if found==1:
##        await TouhouWikiPage(client,message,QueryResult[0],None)
##        return
##
##    await TouhouWikiChooseMenu(QueryResult)
##
##class TouhouWikiPage(object):
##    async def __new__(cls,client,message,result,to_edit):
##        async with client.reqeust_(METH_GET,result[1]) as response:
##            response_data = await response.txt()
##        soup=BeautifulSoup(response_data,'html')
##        block=soup.find_all('div',class_='mw-parser-output')[2]
##        last=[]
##        contents=[(None,last),]
##        for element in block.findAll(('span','h3'),):
##            if type(element) is Tag:
##                text=element.findChild('span').text
##                last=[]
##                contents.append((text,last),)
##            else:
##                text=element.text
##                last.append(text)
##
##        del last
##
##        title=result[0]
##        pages=[]
##        collected=[]
##        collected_len=0
##        collected_from_topic=0
##        for name,blocks in contents:
##            if name is None:
##                embed_title=name
##            else:
##                embed_title=f'{title} / {name}'
##
##            for block in blocks:
##                ln=len(block)
##                if collected_len+ln>5000:
##                    text=
##                    pages.append(Embed(embed_title,
