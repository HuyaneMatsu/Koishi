# -*- coding: utf-8 -*-
import re, random, time, asyncio

from discord_uwu.dereaddons_local import inherit

from discord_uwu.events import waitfor_wrapper,wait_and_continue,bot_reaction_waitfor
from discord_uwu.others import filter_content,is_user_mention
from discord_uwu.futures import wait_one,CancelledError,wait_more,future_or_timeout
from discord_uwu.emoji import BUILTIN_EMOJIS
from discord_uwu.embed import Embed,Embed_footer,Embed_author
from discord_uwu.exceptions import Forbidden,HTTPException

@inherit(bot_reaction_waitfor)
class bot_reaction_delete_waitfor:
    __slots__=['__name__', 'waitfors']
    def __init__(self):
        self.__name__='reaction_delete'
        self.waitfors={}

del inherit

OCEAN=BUILTIN_EMOJIS['ocean'].as_emoji

LINE_X_LEAD=''.join([ \
    BUILTIN_EMOJIS['black_large_square'].as_emoji,
    BUILTIN_EMOJIS['one'].as_emoji,
    BUILTIN_EMOJIS['two'].as_emoji,
    BUILTIN_EMOJIS['three'].as_emoji,
    BUILTIN_EMOJIS['four'].as_emoji,
    BUILTIN_EMOJIS['five'].as_emoji,
    BUILTIN_EMOJIS['six'].as_emoji,
    BUILTIN_EMOJIS['seven'].as_emoji,
    BUILTIN_EMOJIS['eight'].as_emoji,
    BUILTIN_EMOJIS['nine'].as_emoji,
    BUILTIN_EMOJIS['keycap_ten'].as_emoji,
        ])

LINE_Y_LEAD=( \
    BUILTIN_EMOJIS['regional_indicator_a'].as_emoji,
    BUILTIN_EMOJIS['regional_indicator_b'].as_emoji,
    BUILTIN_EMOJIS['regional_indicator_c'].as_emoji,
    BUILTIN_EMOJIS['regional_indicator_d'].as_emoji,
    BUILTIN_EMOJIS['regional_indicator_e'].as_emoji,
    BUILTIN_EMOJIS['regional_indicator_f'].as_emoji,
    BUILTIN_EMOJIS['regional_indicator_g'].as_emoji,
    BUILTIN_EMOJIS['regional_indicator_h'].as_emoji,
    BUILTIN_EMOJIS['regional_indicator_i'].as_emoji,
    BUILTIN_EMOJIS['regional_indicator_j'].as_emoji,
        )

SHIP_VALUES=( \
    OCEAN,
    BUILTIN_EMOJIS['motorboat'].as_emoji,
    BUILTIN_EMOJIS['sailboat'].as_emoji,
    BUILTIN_EMOJIS['ferry'].as_emoji,
    BUILTIN_EMOJIS['cruise_ship'].as_emoji,
    BUILTIN_EMOJIS['cyclone'].as_emoji,
    BUILTIN_EMOJIS['fireworks'].as_emoji,
        )

HIDDEN_VALUES=( \
    OCEAN,
    OCEAN,
    OCEAN,
    OCEAN,
    OCEAN,
    BUILTIN_EMOJIS['cyclone'].as_emoji,
    BUILTIN_EMOJIS['fireworks'].as_emoji,
        )

SWITCH=BUILTIN_EMOJIS['arrows_counterclockwise']

def render_map(data,values):
    
    result=[LINE_X_LEAD]
    line=[]
    y=0
    while True:
        x=0
        line.append(LINE_Y_LEAD[y])
        while True:
            line.append(values[data[x+y*10]])
            x+=1
            if x==10:
                break
        result.append(''.join(line))
        line.clear()
        y+=1
        if y==10:
            break

    return result

POS_PATTERN_0=re.compile('^([\d]{1,2}|[a-jA-J]{1}) *[/]{0,1} *([\d]{1,2}|[a-jA-J]{1}) +([1-4]) *([\|-]{0,1})$')
POS_PATTERN_1=re.compile('^([\d]{1,2}|[a-jA-J]{1}) *[/]{0,1} *([\d]{1,2}|[a-jA-J]{1})$')


class wait_on_reply:
    __slots__=['guild', 'source', 'target']
    def __init__(self,guild,source,target):
        self.guild=guild
        self.source=source
        self.target=target
    def __call__(self,message):
        if message.author is not self.target:
            return False
        
        content=filter_content(message.content)
        
        if len(content)!=2 or content[0].lower()!='accept':
            return False

        content=content[1]

        if is_user_mention(content) and message.mentions:
            user=message.mentions[0]
        else:
            user=self.guild.get_user(content)

        return self.source is user

class active_request:
    __slots__=['future', 'hash', 'source', 'target']
    def __init__(self,source,target):
        self.source=source
        self.target=target
        self.hash=(source.id>>1)+(target.id>>1)
    def __hash__(self):
        return self.hash
    def __eq__(self,other):
        return self.hash==other.hash
    def __ne__(self,other):
        return self.hash!=other.hash
    
class battle_manager:
    __slots__=['games','requesters','requests']
    def __init__(self):
        self.games={}
        self.requesters=set()
        self.requests={}
    async def __call__(self,client,message,content):
        text=''
        while True:
            guild=message.guild
            if guild is None:
                text='You can start game only from a guild'
                break

            source=message.author
            
            if source in self.games:
                text='You cant start a game, if you are in 1 already'
                break
            
            if source in self.requesters:
                text='You can have only one active request'
                break
            
            if not content:
                text='Missing argument WHO'
                break
            
            target=None   
            if message.mentions:
                target=message.mentions[0]
            else:
                target=guild.get_user(content)
                if target is None:
                    text='Could not find that user'
                    break

            if target is source:
                text='Say 2 and easier.'
                break

            if target is client:
                text='NO AI opponent yet!'
                break
            
            if target in self.games:
                text='The user is already in game'
                break

            
            request=active_request(source,target)
            
            is_reversed=self.requests.get(request,None)

            if is_reversed is not None:
                is_reversed.future.set_result(message)
                return

            self.requests[request]=request
            
            self.requesters.add(source)
            
            channel=message.channel
            private = await client.channel_private_create(target)
            
            await client.message_create(channel,f'Waiting on {target:f}\'s reply here and at here dm.\nType:"accept name/mention" to accept')
            
            
            future=request.future=wait_one(client.loop)
            case=wait_on_reply(guild,source,target)
            event=client.events.message_create
            
            wrapper1=waitfor_wrapper(client,wait_and_continue(future,case,channel,event),300.)
            wrapper2=waitfor_wrapper(client,wait_and_continue(future,case,private,event),300.)
            
            try:
                result=await future
            except TimeoutError:
                try:
                    self.requesters.remove(source)
                    text=f'The request from {source:f} timed out'
                except KeyError:
                    pass
                break
            finally:
                try:
                    del self.requests[request]
                except KeyError:
                    pass
                
            
            wrapper1.cancel()
            wrapper2.cancel()

            try:
                self.requesters.remove(source)
            except KeyError:
                text='The requester is already in a game'
                break
            
            if target in self.games:
                text='You already accepted a game'
                break

            try:
                self.requesters.remove(target)
                await client.message_create(channel,f'Request from {target:f} got cancelled')
            except KeyError:
                pass
                
            game=battleships_game(self,client,source,target,private)
            break

        if text:
            await client.message_create(message.channel,text)
            
class ship_type:
    __slots__=['size','parts_left']
    def __init__(self,size):
        self.size=size
        self.parts_left=size

class user_profile:
    __slots__=['channel', 'client', 'data', 'last_switch', 'other', 'page',
        'process', 'ship_positions', 'ships_left', 'state', 'target', 'text',
        'user', 'won']
    ships=[2,4,3,2]
    def __init__(self,user,client):
        self.user=user
        self.client=client
        self.ships_left=self.ships.copy()
        self.ship_positions={}
        self.data=[0 for x in range(100)]
        self.text=''
        #we set channel and other from outside

    async def process_state_0(self,new,text):
        client=self.client
        if new:
            if text is not None:
                self.text=text
            self.target = await client.message_create(self.channel,embed=self.render_state_0())
        else:
            if self.text==text:
                #we do nothing
                pass
            else:
                self.text=text
                await client.message_edit(self.target,embed=self.render_state_0())

    async def process_state_1(self,new,text):
        client=self.client

        if text is not None:
            self.text=text
                
        if new:
            client.events.reaction_add.remove(self)
            client.events.reaction_delete.remove(self)

            self.target = await client.message_create(self.channel,embed=self.render_state_1())
            client.loop.create_task(client.reaction_add(self.target,SWITCH))
            
            client.events.reaction_add.append(self)
            client.events.reaction_delete.append(self)
        else:
            await client.message_edit(self.target,embed=self.render_state_1())

        self.last_switch=0.

    async def set_state_0(self):
        self.process=self.process_state_0
        
        self.text='Good luck!'
        self.target = await self.client.message_create(self.channel,embed=self.render_state_0())
        
    async def set_state_1(self,starts):
        self.process=self.process_state_1
        self.text=''
        self.state=starts
        
        if starts:
            self.page=1
        else:
            self.page=0
        
        client=self.client
        
        self.target = await client.message_create(self.channel,embed=self.render_state_1())
        client.loop.create_task(client.reaction_add(self.target,SWITCH))
        
        client.events.reaction_add.append(self)
        client.events.reaction_delete.append(self)

        self.last_switch=0.
        

    async def set_state_2(self,state,text):
        self.process=None
        
        self.state=state
        self.text=text
        
        client=self.client

        client.events.reaction_add.remove(self)
        client.events.reaction_delete.remove(self)
        
        self.target = await client.message_create(self.channel,embed=self.render_state_2())
        client.loop.create_task(client.reaction_add(self.target,SWITCH))

        client.events.reaction_add.append(self)
        client.events.reaction_delete.append(self)
        
        self.last_switch=0.
        
    async def __call__(self,args):
        user,emoji=args
        now=time.time()
        if now<self.last_switch+1.2:
            return
        self.last_switch=now
        self.page^=1

        if self.process is None:
            embed=self.render_state_2()
        else:
            embed=self.render_state_1()
        
        await self.client.message_edit(self.target,embed=embed)


    def cancel(self):
        client=self.client
        if self.process is None:
            client.loop.create_task(self.cancel_later())
            return

        del self.other
        if self.process.__func__ is type(self).process_state_1:
            client.events.reaction_add.remove(self)
            client.events.reaction_delete.remove(self)
        
    async def cancel_later(self):
        client=self.client
        await asyncio.sleep(300.,client.loop)
        client.events.reaction_add.remove(self)
        client.events.reaction_delete.remove(self)
        del self.other


    def render_state_0(self):
        other=self.other
        text=['''
            Type "new" to show this message up again.
            Type "A-J" "1-10" "1-3" <- or | (default(|)> to place a ship down.'
            "1-3" stands for size, "-" and "|" stands for shape.'
            It always places the ship right-down from the source coordinate'
            ''']
        text.extend(render_map(self.data,SHIP_VALUES))
        embed=Embed('','\n'.join(text))
        embed.author=Embed_author(other.user.avatar_url_as(size=64),f'vs.: {other.user:f}')
        
        text.clear()
        if sum(self.ships_left):
            sub_text=[]
            for size,amount in enumerate(self.ships_left,1):
                if amount:
                    sub_text.append(f'{amount} size {size}')
            text.append(', '.join(sub_text))
            text.append(' ship is left to place. ')
        text.append(self.text)
        embed.footer=Embed_footer(''.join(text))
        return embed

    def render_state_1(self):
        other=self.other
        text=[]
        if self.state:
            text.append('**It is your turn!**')
        else:
            text.append('**It is your opponent\'s turn!**')
        
        text.append('''
            Type "new" to show this message up again.'
            Type "A-J" "1-10" to torpedo a ship.'
            If you hit your opponent, then it is your turn again.'
            ''',)

        if self.page:
            text.append('**Your opponents ship:**')
            text.extend(render_map(other.data,HIDDEN_VALUES))
            footer=f'Your opponent has {sum(other.ships_left)} ships left on {len(other.ship_positions)} tiles. {self.text}'
        else:
            text.append('**Your ships:**')
            text.extend(render_map(self.data,SHIP_VALUES))
            footer=f'You have {sum(self.ships_left)} ships left on {len(self.ship_positions)} tiles. {self.text}'

        embed=Embed('','\n'.join(text))
        embed.author=Embed_author(other.user.avatar_url_as(size=64),f'vs.: {other.user:f}')
        embed.footer=Embed_footer(footer)
        return embed

    def render_state_2(self):
        other=self.other
        text=[]
        if self.state:
            text.append('**You won!**\n')
        else:
            text.append('**You lost :cry:**\n')
            
        if self.page:
            text.append('Your opponent\'s ships:')
            text.extend(render_map(other.data,SHIP_VALUES))
        else:
            text.append('Your ships:')
            text.extend(render_map(self.data,SHIP_VALUES))
                
        embed=Embed('','\n'.join(text))
        embed.author=Embed_author(other.user.avatar_url_as(size=64),f'vs.: {other.user:f}')
        embed.footer=Embed_footer(self.text)
        return embed

class battleships_game:
    __slots__=['actual', 'client', 'future', 'manager', 'player1', 'player2',
        'process', 'target']
    def __init__(self,manager,client,user1,user2,channel2):

        manager.games[user1]=self
        manager.games[user2]=self

        self.manager=manager
        self.client=client

        self.player1=user_profile(user1,client)
        self.player2=user_profile(user2,client)
        self.player2.channel=channel2

        self.client.loop.create_task(self.start())

    #compability
    async def start(self):
        try:
            client=self.client
            loop=client.loop

            player1=self.player1
            player2=self.player2

            player1.other=player2
            player2.other=player1
            
            #creating missing channel
            player1.channel = await client.channel_private_create(player1.user)

            #adding channels to the event to notify us
            self.target=player1.channel
            client.events.message_create.append(self)
            self.target=player2.channel
            client.events.message_create.append(self)
            
            #game starts            
            self.future=wait_more(loop,2)
            future_or_timeout(self.future,300.)

            #startup
            self.process=self.process_state_0
            loop.create_task(player1.set_state_0())
            loop.create_task(player2.set_state_0())
            
            try:
                await self.future
            except TimeoutError:
                if not self.future._result:
                    text1=text2='The time is over, both players timed out'
                elif player1 in self.future._result:
                    text1='The other player timed out'
                    text2='You timed out'
                else:
                    text1='You timed out'
                    text2='The other player timed out'
                loop.create_task(client.message_create(player1.channel,text1))
                loop.create_task(client.message_create(player2.channel,text2))
                return

            self.process=self.process_state_1
            player1.ships_left[:]=user_profile.ships
            player2.ships_left[:]=user_profile.ships

            if random.randint(0,1):
                self.actual=player1
            else:
                self.actual=player2
            
            await self.actual.set_state_1(True)
            await self.actual.other.set_state_1(False)
            

            while self.process is not None:
                self.future=wait_one(loop)
                future_or_timeout(self.future,300.)
                try:
                    result = await self.future
                except TimeoutError:

                    await self.actual.other.set_state_2(True,'Your opponent timed out!')
                    awaitself.actual.set_state_2(False,'You timed out!')
                    return
                
                if result:
                    self.actual=self.actual.other

                
        except (Forbidden,HTTPException):
            #what should i put here?
            pass
        finally:
            self.cancel()

    async def process_state_0(self,message):
        if message.author is self.player1.user:
            player=self.player1
        else:
            player=self.player2
        other=player.other

        while True:
            if sum(player.ships_left)==0:
                text='Waiting on the other player.'
                break
            result=re.match('^new$',message.content,re.I)
            if result is not None:
                text='new'
                break
            result=re.match(POS_PATTERN_0,message.content)
            if result is None:
                text='Bad input format'
                break
            result=result.groups()
            
            value=result[0]
            if value.isdigit():
                x=int(value)
                if x>10:
                    text='Bad input format.'
                    break
                x=x-1
                y=100
            else:
                x=100
                y=('abcdefghij').index(value.lower())

            value=result[1]
            if value.isdigit():
                if x!=100:
                    text='Dupe coordinate'
                    break
                x=int(value)
                if x>10:
                    text='Bad input format.'
                    break
                x=x-1
            else:
                if y!=100:
                    text='Dupe coordinate'
                    break
                y=('abcdefghij').index(value)

            size=int(result[2])
            if player.ships_left[size-1]==0:
                text='You do not have anymore ships from that size'
                break
            
            value=result[3]
            mode= (value!='-')

            text=''
            if mode:
                for n_y in range(y,y+size):
                    if n_y>9:
                        text=f'Can not set ship to {1+x}{chr(65+y)}, there is not enough space for it.'
                        break
                    if player.data[x+n_y*10]:
                        text=f'Can not set ship to {1+x}/{chr(65+y)}, because coordinate {1+x}/{chr(65+n_y)} is already used.'
                        break
            else:
                for n_x in range(x,x+size):
                    if n_x>9:
                        text=f'Can not set ship to {1+x}{chr(65+y)}, there is not enough space for it.'
                        break
                    if player.data[n_x+y*10]:
                        text=f'Can not set ship to {1+x}/{chr(65+y)}, because coordinate {n_x}/{chr(65+y)} is already used.'
                        break
                    

            if text:
                break
            
            ship=ship_type(size)
            cords=[]
            if mode:
                for n_y in range(y,y+size):
                    player.data[x+n_y*10]=size
                    player.ship_positions[x+(n_y<<4)]=ship
                    cords.append(f'{chr(65+n_y)}/{1+x}')
            else:
                for n_x in range(x,x+size):
                    player.data[n_x+y*10]=size
                    player.ship_positions[n_x+(y<<4)]=ship
                    cords.append(f'{chr(65+y)}/{n_x}')
                    
            player.ships_left[size-1]-=1

            if sum(player.ships_left)==0:
                self.future.set_result(player)
                text=f'You placed all of your ships at: {", ".join(cords)}; waiting on the other player.'
            else:
                text=f'You placed the ship succesfully at: {", ".join(cords)}.'

            break

        client=self.client

        if text=='new':
            await player.process(True,None)
            return
        if sum(player.ships_left)==sum(other.ships_left)==0:
            return
        await player.process(False,text)

    async def process_state_1(self,message):
        if self.actual is self.player1:
            player=self.player1
            other=self.player2
        else:
            player=self.player2
            other=self.player1

        client=self.client
        
        if message.author is not self.actual.user:
            result=re.match('^new$',message.content,re.I)
            if result is not None:
                await player.process(True,None)
            return

        data=other.data
        
        while True:
            result=re.match('^new$',message.content,re.I)
            if result is not None:
                text='new'
                break
            result=re.match(POS_PATTERN_1,message.content)
            if result is None:
                text='Bad input format'
                break
            result=result.groups()
        
            value=result[0]
            if value.isdigit():
                x=int(value)
                if x>10:
                    text='Bad input format.'
                    break
                x=x-1
                y=100
            else:
                x=100
                y=('abcdefghij').index(value.lower())

            value=result[1]
            if value.isdigit():
                if x!=100:
                    text='Dupe coordinate'
                    break
                x=int(value)
                if x>10:
                    text='Bad input format.'
                    break
                x=x-1
            else:
                if y!=100:
                    text='Dupe coordinate'
                    break
                y=('abcdefghij').index(value)

            value=data[x+y*10]
            if value in (5,6):
                text='That position is already shot'
                break

            text=''
            break
        
        if text:
            if text=='new':
                await player.process(True,None)                    
            else:
                await player.process(False,text)
            return

        if value==0:
            data[x+y*10]=5

            player.state=False
            other.state=True
                
            await player.process(False,'You missed!')
            await other.process(True,f'Your opponent shot {chr(65+y)}/{1+x}, it missed!\n')
            self.future.set_result(True)
            return

        del text
        
        data[x+y*10]=6
        ship=other.ship_positions.pop(x+(y<<4))
        ship.parts_left-=1
        if ship.parts_left==0:
            other.ships_left[ship.size-1]-=1
            if sum(other.ships_left):
                text1=f'You shot {chr(65+y)}/{1+x} and you sinked 1 of your opponents ships!\n'
                text2=f'Your opponent shot {chr(65+y)}/{1+x} and your ship sinked :c\n'
            else:
                self.process=None
                await player.set_state_2(True, \
                    f'You shot {chr(65+y)}/{1+x} and you sinked your opponents last ship!')
                await other.set_state_2(False, \
                    f'Your opponent shot {chr(65+y)}/{1+x} and your last ship sinked :c')
                self.future.set_result(False)
                return
        else:

            text1=f'You shot {chr(65+y)}/{1+x} and you hit a ship!'
            text2=f'Your opponent shot {chr(65+y)}/{1+x} and hit 1 of your ships!'

        player.state=True
        other.state=False
            
        await player.process(False,text1)
        await other.process(True,text2)
        self.future.set_result(False)
    
    async def __call__(self,args):
        await self.process(args[0])
        
    def cancel(self):
        #self.target=self.player2.channel
        event=self.client.events.message_create
        #self.target should be channel2
        event.remove(self)
        #now from the other channell
        self.target=self.player1.channel
        event.remove(self)
        
        del self.manager.games[self.player1.user]
        del self.manager.games[self.player2.user]

        self.player1.cancel()
        self.player2.cancel()
