# -*- coding: utf-8 -*-
from itertools import chain
import re
from time import monotonic
    
from hata.events_compiler import content_parser
from hata.embed import Embed
from hata.color import Color
from hata.exceptions import Forbidden,HTTPException
from hata.emoji import BUILTIN_EMOJIS,Emoji
from hata.futures import Future,CancelledError
from hata.client_core import GC_process
from hata.futures import ensure_elsewhere

from help_handler import HELP
from models import DB_ENGINE,DS_TABLE,ds_model

DS_GAMES={}
STAGES=[]
CHARS=[]
COLORS=(0xa000c4,0x00cc03,0xffe502,0xe50016)

#:-> @ <-:#}{#:-> @ <-:#{ GC }#:-> @ <-:#}{#:-> @ <-:#

async def _keep_await(function,games):
    for game in games:
        await function(game)

def GC_games():
    limit=monotonic()-3600. #we delete after 1 hour
    to_delete=[]
    to_save=[]
    for game in DS_GAMES.values():
        if game.last<limit:
            to_delete.append(game)
        else:
            to_save.append(game)

    if to_delete:
        loop=to_delete[0].client.loop
        ensure_elsewhere(_keep_await(ds_game.cancel,to_delete),loop)

    if to_save:
        loop=to_save[0].client.loop
        ensure_elsewhere(_keep_await(ds_game.save_position,to_save),loop)

GC_process.functions.append(GC_games)

del GC_process
del GC_games

#:-> @ <-:#}{#:-> @ <-:#{ command }#:-> @ <-:#}{#:-> @ <-:#

@content_parser('str, default="\'\'"')
async def ds_manager(self,message,command):
    permissions=message.channel.permissions_for(self)
    if not permissions.can_send_messages:
        return
    
    while True:

        if not (0<=len(command)<10):
            embed=HELP['ds']
            break

        command=command.lower()

        game=DS_GAMES.get(message.author.id)
        
        if command=='':
            if not (permissions.can_add_reactions and permissions.can_external_emojis and permissions.can_manage_messages):
                embed=Embed('Permissions denied','I have not all permissions to start a game at this channel.')
                break
            
            if game is None:
                return ds_game(self,message.channel,message.author)
            else:
                return await game.renew(message.channel)
            
        if command=='rules':
            if permissions.can_external_emojis:
                embed=RULES_HELP
            else:
                embed=('Permissions denied','I have no permissions at this channel to render this message.')
            break
        
        embed=HELP['ds']
        break
        
    await self.message_create(message.channel,embed=embed)

#:-> @ <-:#}{#:-> @ <-:#{ backend }#:-> @ <-:#}{#:-> @ <-:#

class ds_game:

    WEST    = BUILTIN_EMOJIS['arrow_left']
    NORTH   = BUILTIN_EMOJIS['arrow_up']
    SOUTH   = BUILTIN_EMOJIS['arrow_down']
    EAST    = BUILTIN_EMOJIS['arrow_right']
    
    emojis_game_p1=(WEST,NORTH,SOUTH,EAST)
    
    BACK    = BUILTIN_EMOJIS['leftwards_arrow_with_hook']
    RESET   = BUILTIN_EMOJIS['arrows_counterclockwise']
    CANCEL  = BUILTIN_EMOJIS['x']
    
    emojis_game_p2=(BACK,RESET,CANCEL)

    UP      = BUILTIN_EMOJIS['arrow_up_small']
    DOWN    = BUILTIN_EMOJIS['arrow_down_small']
    UP2     = BUILTIN_EMOJIS['arrow_double_up']
    DOWN2   = BUILTIN_EMOJIS['arrow_double_down']
    LEFT    = BUILTIN_EMOJIS['arrow_backward']
    RIGHT   = BUILTIN_EMOJIS['arrow_forward']
    SELECT  = BUILTIN_EMOJIS['ok']
    
    emojis_menu=(UP,DOWN,UP2,DOWN2,LEFT,RIGHT,SELECT)
    
    __slots__ = ['call', 'cache', 'channel', 'client', 'data', 'last',
        'position', 'position_ori', 'stage', 'target', 'task', 'user']

    __async_call__ = True
    
    def __init__(self,client,channel,user):
        
        DS_GAMES[user.id]   = self
        self.client         = client
        self.user           = user
        self.channel        = channel
        self.target         = None
        self.stage          = None
        self.task           = Future(client.loop)
        self.call           = type(self).call_menu
        self.cache          = [None for _ in range(len(CHARS))]
        self.last           = monotonic()
        client.loop.create_task(self.start())
        
    async def start(self):

        async with DB_ENGINE.connect() as connector:
            result = await connector.execute(DS_TABLE.select(ds_model.user_id==self.user.id))
            stats = await result.fetchall()

        if stats:
            stats=stats[0]
            self.position=self.position_ori=stats.position
            self.data=bytearray(stats.data)
        else:
            self.position=0
            self.position_ori=-1
            self.data=bytearray(800)

        client=self.client
        loop=client.loop
        
        try:
            self.target = await client.message_create(self.channel,embed=self.render_menu())
            for emoji in self.emojis_menu:
                loop.create_task(client.reaction_add(self.target,emoji))
        except (Forbidden,HTTPException):
            try:
                if self.target is not None:
                    await client.message_create(self.channel,'',Embed('','Error meanwhile initializing'))
            except (Forbidden,HTTPException):
                pass
            del DS_GAMES[self.user.id]
        else:
            self.target.weakrefer()
            self.task.set_result(None)
            client.events.reaction_add.append(self)
            
    async def start_menu(self):
        self.stage=None
        
        client=self.client
        loop=client.loop
        try:
            loop.create_task(client.reaction_clear(self.target))
            for emoji in self.emojis_menu:
                loop.create_task(client.reaction_add(self.target,emoji))
            
            await client.message_edit(self.target,embed=self.render_menu())
        except (Forbidden,HTTPException):
            return loop.create_task(self.cancel())
        finally:
            self.last=monotonic()
            self.call=type(self).call_menu
            self.task.set_result(None)

    async def start_game(self):
        
        
        i1,rest=divmod(self.position,33)
        if rest<3:
            i2=0
            i3=rest
        else:
            i2,i3=divmod(rest+7,10)

        self.stage=stage_backend(STAGES[i1][i2][i3],self.value_from_position(self.position))

        client=self.client
        loop=client.loop  
        try:
            loop.create_task(client.reaction_clear(self.target))
            for emoji in chain(self.emojis_game_p1,(self.stage.source.emoji,),self.emojis_game_p2):
                loop.create_task(client.reaction_add(self.target,emoji))
            
            await client.message_edit(self.target,embed=self.render_game())
        except (Forbidden,HTTPException):
            return loop.create_task(self.cancel())
        finally:
            self.last=monotonic()
            self.call=type(self).call_game
            self.task.set_result(None)

    async def start_done(self):
        client=self.client
        loop=client.loop
        
        task=loop.create_task(self.save_done())
        
        try:
            loop.create_task(client.reaction_clear(self.target))
            loop.create_task(client.reaction_add(self.target,self.RESET))
            loop.create_task(client.reaction_add(self.target,self.CANCEL))
            
            await client.message_edit(self.target,embed=self.render_done())
        except (Forbidden,HTTPException):
            return loop.create_task(self.cancel())
        finally:
            await task
            self.last=monotonic()
            self.call=type(self).call_done
            self.task.set_result(None)

    @staticmethod
    async def default_coro():
        pass
    
    def __call__(self,emoji,user):
        if user is not self.user:
            return self.default_coro()

        return self.call(self,emoji)

    async def call_menu(self,emoji):
        if self.task.pending() and (emoji in self.emojis_menu):
            return self.client.loop.create_task(self.reaction_delete(emoji))
        
        while True:
            if emoji is self.UP:
                position_change=1
                break
            
            if emoji is self.DOWN:
                position_change=-1
                break
            
            if emoji is self.UP2:
                position_change=5
                break

            if emoji is self.DOWN2:
                position_change=-5
                break

            position_change=0
            if emoji is self.RIGHT:
                chapter_change=1
                break

            if emoji is self.LEFT:
                chapter_change=-1
                break

            if emoji is self.SELECT:
                if self.target.embeds[0].fields:
                    self.task.clear()
                    await self.start_game()
                else:
                    self.client.loop.create_task(self.reaction_delete(emoji))
                return
            
            return       

        self.client.loop.create_task(self.reaction_delete(emoji))
        
        position=self.position
        i1,rest=divmod(position,33)
        if rest<3:
            i2=0
            i3=rest
        else:
            i2,i3=divmod(rest+7,10)
        
        if position_change:
            cache=self.get_cache(i1)
            for actual_position,element in enumerate(cache):
                stage=element[0]
                if stage.difficulty==i2 and stage.level==i3:
                    break
            
            relative_position=actual_position+position_change
            if position_change<0:
                if relative_position<0:
                    relative_position=0
            else:
                if relative_position>=len(cache):
                    relative_position=len(cache)-1

            if actual_position==relative_position:
                return

            new_position=cache[relative_position][0].position
            
            if new_position==position:
                return
            
        else:
            relative_chapter=i1+chapter_change
            if relative_chapter<0 or relative_chapter>=len(STAGES):
                return

            cache=self.get_cache(relative_chapter)
            for target_position,element in enumerate(cache):
                stage=element[0]
                
                if stage.difficulty==i2:
                    relative_position=target_position
                    if stage.level==i3:
                        break
                elif stage.difficulty>i2:
                    break
            else:
                relative_position=target_position

            new_position=cache[relative_position][0].position

        self.position=new_position

        self.task.clear()

        try:
            await self.client.message_edit(self.target,embed=self.render_menu())
        except (Forbidden,HTTPException):
            return self.client.loop.create_task(self.cancel())
        finally:
            self.task.set_result(None)
    
    async def call_game(self,emoji):
        if self.task.pending() and (emoji in self.emojis_game_p1 or emoji in self.emojis_game_p2 or emoji is self.stage.source.emoji):
            return self.client.loop.create_task(self.reaction_delete(emoji))

        while True:
            if emoji is self.WEST:
                result=self.stage.move_west()
                break
            
            if emoji is self.NORTH:
                result=self.stage.move_north()
                break

            if emoji is self.SOUTH:
                result=self.stage.move_south()
                break

            if emoji is self.EAST:
                result=self.stage.move_east()
                break
            
            if emoji is self.stage.source.emoji:
                result=self.stage.activate_skill()
                break

            if emoji is self.BACK:
                result=self.stage.back()
                break

            if emoji is self.RESET:
                result=self.stage.reset()
                break

            if emoji is self.CANCEL:
                self.task.clear()
                return await self.start_menu()

            return

        client=self.client
        if not result:
            return client.loop.create_task(self.reaction_delete(emoji))
        
        self.task.clear()

        if self.stage.done():
            return await self.start_done()

        client.loop.create_task(self.reaction_delete(emoji))
        
        try:
            await self.client.message_edit(self.target,embed=self.render_game())
        except (Forbidden,HTTPException):
            return self.client.loop.create_task(self.cancel())
        finally:
            self.last=monotonic()
            self.task.set_result(None)

    async def call_done(self,emoji):
        if not (emoji is self.RESET or emoji is self.CANCEL):
            return

        self.client.loop.create_task(self.reaction_delete(emoji))
        
        if self.task.pending():
            return 

        self.task.clear()
        if emoji is self.RESET:
            self.position=self.stage.source.position
            await self.start_game()
        else:
            await self.start_menu()
        
    async def cancel(self):
        if self.task.pending():
            await self.save_position()
            return

        try:
            del DS_GAMES[self.user.id]
        except KeyError:
            return #already cancelled
        
        self.client.events.reaction_add.remove(self)

        await self.save_position()

    async def save_position(self):
        position=self.position
        if position==self.position_ori:
            return

        async with DB_ENGINE.connect() as connector:
            if self.position_ori<0:
                coro=DS_TABLE.insert(). \
                    values(user_id=self.user.id,position=position,data=self.data)
            else:
                coro=DS_TABLE.update(). \
                    values(position=position,data=self.data). \
                    where(ds_model.user_id==self.user.id)
            
            await connector.execute(coro)
        
        self.position_ori=position
        
    async def save_done(self):
        best_steps=self.stage.best
        position=self.position
        old_steps=self.value_from_position(position)

        if position%33!=32:
            relative_position=position+1
            i1,rest=divmod(relative_position,33)
            if rest<3:
                i2=0
                i3=rest
            else:
                i2,i3=divmod(rest+7,10)
                
            difficulities=STAGES[i1]
            if difficulities:
                levels=difficulities[i2]
                if i3<len(levels):
                    self.position=relative_position
        
        if old_steps!=best_steps:
            self.write_value(position,best_steps)
            self.cache[self.stage.source.chapter]=None
            return_=False
        else:
            return_=True
        
        if return_ and self.position==self.position_ori:
            return
        
        async with DB_ENGINE.connect() as connector:
            if self.position_ori<0:
                coro=DS_TABLE.insert(). \
                    values(user_id=self.user.id,position=self.position,data=self.data)
            else:
                coro=DS_TABLE.update(). \
                    values(position=self.position,data=self.data). \
                    where(ds_model.user_id==self.user.id)
            
            await connector.execute(coro)
    
        self.position_ori=self.position
      
    async def renew(self,channel):
        if self.task.pending():
            await self.task

        self.task.clear()

        client=self.client
        loop=client.loop
        try:
            if self.call is type(self).call_game:
                target = await client.message_create(channel,embed=self.render_game())
                for emoji in chain(self.emojis_game_p1,(self.stage.source.emoji,),self.emojis_game_p2):
                    loop.create_task(client.reaction_add(target,emoji))
            elif self.call is type(self).call_menu:
                target = await client.message_create(channel,embed=self.render_menu())
                for emoji in self.emojis_menu:
                    loop.create_task(client.reaction_add(target,emoji))
            else:
                target = await client.message_create(channel,embed=self.render_done())
                loop.create_task(client.reaction_add(target,self.RESET))
                loop.create_task(client.reaction_add(target,self.CANCEL))
                
        except (Forbidden,HTTPException):
            try:
                if self.target is not None:
                    await client.message_create(channel,'',Embed('','Error meanwhile initializing'))
            except (Forbidden,HTTPException):
                pass
            return
        else:
            try:
                await client.reaction_clear(self.target)
            except (Forbidden,HTTPException):
                pass
                
            client.events.reaction_add.remove(self)

            target.weakrefer()
            self.target=target
            self.channel=channel
            
            client.events.reaction_add.append(self)

        finally:
            self.last=monotonic()
            self.task.set_result(None)
        
    def render_done(self):
        stage=self.stage
        steps=stage.best

        rating=stage.source.rate(steps)
            
        embed=Embed(f'{stage.source.name} finished with {steps} steps with {rating} rating!',stage.render(),COLORS[stage.source.difficulty])
        embed.add_footer(f'steps : {len(stage.history)}, best : {stage.best}')
        embed.add_author(self.user.avatar_url_as('png',32),self.user.full_name)
        return embed
    
    def render_game(self):
        stage=self.stage
        
        title_parts=[stage.source.name]
        if stage.has_skill:
            title_parts.append(stage.source.emoji.as_emoji)
            if stage.next_skill:
                title_parts.append('READY')
            
        embed=Embed(' '.join(title_parts),stage.render(),COLORS[stage.source.difficulty])
        footer=f'steps : {len(stage.history)}'
        if stage.best:
            footer=f'{footer}, best : {stage.best}'
        embed.add_footer(footer)
        embed.add_author(self.user.avatar_url_as('png',32),self.user.full_name)
        return embed

    def get_cache(self,chapter,force=False):
        cache=self.cache[chapter]
        if cache is None:
            cache=self.cache[chapter]=[]
            force=True

        if not force:
            return cache

        cache.clear()
        
        difficulties=STAGES[chapter]

        additional=chapter*33

        levels=difficulties[0]
        for index in range(len(levels)):
            value=self.value_from_position(additional+index)
            cache.append((levels[index],value),)
            if value:
                continue
            break

        
        if len(cache)==len(levels) and cache[-1][1]:
            additional-=7
            for diff_index in range(1,4):
                additional+=10
                levels=difficulties[diff_index]
                for index in range(len(levels)):
                    value=self.value_from_position(additional+index)
                    cache.append((levels[index],value),)
                    if value:
                        continue
                    break

        return cache
    
    def render_menu(self):
        position=self.position
        i1,rest=divmod(position,33)
        if rest<3:
            i2=0
            i3=rest
        else:
            i2,i3=divmod(rest+7,10)

        value_middle=self.value_from_position(position)

        cache=self.get_cache(i1)

        embed=Embed(f'Chapter {chr(i1+49)}')
        embed.add_thumbnail(CHARS[i1][3].url)

        if len(cache)>1 or (i1==0) or self.value_from_position(i1*33-21):

            for target_index,element in enumerate(cache):
                stage=element[0]
                
                if stage.difficulty==i2 and stage.level==i3:
                    embed.color=COLORS[stage.difficulty]
                    break

            if target_index<3:
                to_render=cache[4::-1]
            elif target_index>len(cache)-3:
                to_render=cache[:-6:-1]
            else:
                to_render=cache[target_index+2:target_index-3:-1]
                
            for stage,steps in to_render:
                field_name=f'{("Tutorial","Easy","Normal","Hard")[stage.difficulty]} level {stage.level+1}'
                if steps==0:
                    field_value='No results recorded yet!'
                else:
                    field_value=f'rating {stage.rate(steps)}; steps : {steps}'


                if stage.difficulty==i2 and stage.level==i3:
                    field_name=f'**{field_name}**'
                    field_value=f'**{field_value}**'

                embed.add_field(field_name,field_value)
            
        else:
            embed.color=COLORS[0]
            embed.description=f'**You must finish chapter {chr(i1+48)} Easy 10 first.**'
        
        embed.add_author(self.user.avatar_url_as('png',32),self.user.full_name)
        return embed                     

    def value_from_position(self,position):
        position=position<<1
        return int.from_bytes(self.data[position:position+2],byteorder='big')

    def write_value(self,position,value):
        position=position<<1
        self.data[position:position+2]=value.to_bytes(2,byteorder='big')
                                       
    async def reaction_delete(self,emoji):
        try:
            await self.client.reaction_delete(self.target,emoji,self.user)
        except (Forbidden,HTTPException):
            pass

#:-> @ <-:#}{#:-> @ <-:#{ game }#:-> @ <-:#}{#:-> @ <-:#

PASSABLE    = 0b0000000000000111

FLOOR       = 0b0000000000000001
TARGET      = 0b0000000000000010
HOLE_P      = 0b0000000000000011
OBJECT_P    = 0b0000000000000100


PUSHABLE    = 0b0000000000111000

BOX         = 0b0000000000001000
BOX_TARGET  = 0b0000000000010000
BOX_HOLE    = 0b0000000000011000
BOX_OBJECT  = 0b0000000000100000


SPECIAL     = 0b0000000011000000

HOLE_U      = 0b0000000001000000
OBJECT_U    = 0b0000000010000000


CHAR        = 0b0000011100000000
CHAR_N      = 0b0000010000000000
CHAR_E      = 0b0000010100000000
CHAR_S      = 0b0000011000000000
CHAR_W      = 0b0000011100000000

##CN_FLOOR    = 0b0000010000000001
##CE_FLOOR    = 0b0000010100000001
##CS_FLOOR    = 0b0000011000000001
##CW_FLOOR    = 0b0000011100000001
##
##CN_TARGET   = 0b0000010000000010
##CE_TARGET   = 0b0000010100000010
##CS_TARGET   = 0b0000011000000010
##CW_TARGET   = 0b0000011100000010
##
##CN_OBJECT_P = 0b0000010000000011
##CE_OBJECT_P = 0b0000010100000011
##CS_OBJECT_P = 0b0000011000000011
##CW_OBJECT_P = 0b0000011100000011
##
##CN_HOLE_P   = 0b0000010000000100
##CE_HOLE_P   = 0b0000010100000100
##CS_HOLE_P   = 0b0000011000000100
##CW_HOLE_P   = 0b0000011100000100

WALL        = 0b1111100000000000

NOTHING     = 0b0000100000000000
WALL_N      = 0b0001000000000000
WALL_E      = 0b0010000000000000
WALL_S      = 0b0100000000000000
WALL_W      = 0b1000000000000000
##WALL_A      = 0b1111000000000000
##WALL_SE     = 0b0110000000000000
##WALL_SW     = 0b1100000000000000

UNPUSHABLE  = WALL|SPECIAL
BLOCKS_LOS  = WALL|PUSHABLE|OBJECT_U



class history_element:
    __slots__=['changes', 'position', 'was_skill']
    
    def __init__(self,position,was_skill,changes):
        self.position=position
        self.was_skill=was_skill
        self.changes=changes
        
class stage_source:
    __slots__=['best', 'chapter', 'char', 'difficulty', 'level', 'map',
        'size', 'start', 'targets']
    
    def __init__(self,header,map_):
        self.chapter=int(header[0])
        self.difficulty=int(header[1])
        self.targets=int(header[2])
        self.size=int(header[3])
        self.start=int(header[4])
        self.best=int(header[5])

        self.char=CHARS[self.chapter]
        
        self.map=map_.copy()

        level_cont=STAGES[self.chapter][self.difficulty]
        self.level=len(level_cont)
        level_cont.append(self)
        
    @property
    def style(self):
        return self.char[0]

    @property
    def activate_skill(self):
        return self.char[1]

    @property
    def use_skill(self):
        return self.char[2]

    @property
    def emoji(self):
        return self.char[3]
    
    def rate(self,steps):
        best=float(self.best) #stick using to one datatype
        for rating in ('S','A','B','C','D','E'):
            if steps<=best:
                break
            best=best*1.2+2.
        return rating

    @property
    def position(self):
        position=self.chapter*33+self.level
        if self.difficulty:
            return position-7+self.difficulty*10
        return position

    @property
    def name(self):
        return f'Chapter {chr(49+self.chapter)} {("Tutorial","Easy","Normal","Hard")[self.difficulty]} level {self.level+1}'

class stage_backend:
    __slots__=['best', 'has_skill', 'history', 'map', 'next_skill', 'position',
        'source']
    
    def __init__(self,source,best):
        self.source=source
        self.map=source.map.copy()
        self.position=source.start
        self.history=[]
        self.has_skill=True
        self.next_skill=False
        self.best=best
        
    def done(self):
        targets=self.source.targets
        for tile in self.map:
            if tile==BOX_TARGET:
                targets-=1
                if targets==0:
                    if self.best==0 or self.best>len(self.history):
                        self.best=len(self.history)
                    return True
        
        return False

    def move_north(self):
        return self.move(-self.source.size,CHAR_N)

    def move_east(self):
        return self.move(1,CHAR_E)

    def move_south(self):
        return self.move(self.source.size,CHAR_S)

    def move_west(self):
        return self.move(-1,CHAR_W)
            
    def move(self,step,align):
        if self.next_skill:
            result=self.source.use_skill(self,step,align)
            if result:
                self.next_skill=False
            return result
        
        map_=self.map
        position=self.position

        actual_tile=map_[position]
        target_tile=map_[position+step]
        
        if target_tile&UNPUSHABLE:
            return False
        
        if target_tile&PASSABLE:
            self.history.append(history_element(position,False,((position,actual_tile),(position+step,target_tile))))
            
            map_[position]=actual_tile&PASSABLE
            self.position=position=position+step
            map_[position]=target_tile|align
            
            return True

        after_tile=map_[position+(step<<1)]

        if target_tile&PUSHABLE and after_tile&(PASSABLE|HOLE_U):
            self.history.append(history_element(self.position,False,((position,actual_tile),(position+step,target_tile),(position+(step<<1),after_tile))))
            
            map_[position]=actual_tile&PASSABLE
            self.position=position=position+step
            map_[position]=(target_tile>>3)|align
            if after_tile&PASSABLE:
                map_[position+step]=after_tile<<3
            else:
                map_[position+step]=HOLE_P
            return True
        
        return False

    def activate_skill(self):
        if not self.has_skill:
            return False
        if self.source.activate_skill(self):
            self.next_skill=True
            return True
        return False
        

    def render(self):
        style=self.source.style
        result=[]
        map_=self.map
        limit=len(map_)
        step=self.source.size

        if limit<82:
            start=0
            while start<limit:
                end=start+step
                result.append(''.join([style[element] for element in map_[start:end]]))
                start=end
        else:
            start=1
            step=step-2
            while start<limit:
                end=start+step
                result.append(''.join([style[element] for element in map_[start:end]]))
                start=end+2
        
        return '\n'.join(result)

    def back(self):
        if self.next_skill:
            self.next_skill=False
            return True
        
        history=self.history
        if not history:
            return False
        
        element=history.pop(-1)
        map_=self.map
        self.position=element.position
        
        for position,value in element.changes:
            map_[position]=value

        if element.was_skill:
            self.has_skill=True
        return True

    def reset(self):
        history=self.history
        if not history:
            return False

        history.clear()

        self.position=self.source.start
        self.map=self.source.map.copy()
        self.has_skill=True

        return True

NOTHING_EMOJI=Emoji.precreate(568838460434284574,name='0Q')

DEFAULT_STYLE_PARTS = {
    NOTHING                     : NOTHING_EMOJI.as_emoji,
    WALL_E                      : Emoji.precreate(568838488464687169,name='0P').as_emoji,
    WALL_S                      : Emoji.precreate(568838546853462035,name='0N').as_emoji,
    WALL_W                      : Emoji.precreate(568838580278132746,name='0K').as_emoji,
    WALL_N|WALL_E|WALL_S|WALL_W : Emoji.precreate(578678249518006272,name='0X').as_emoji,
    WALL_E|WALL_S               : Emoji.precreate(568838557318250499,name='0M').as_emoji,
    WALL_S|WALL_W               : Emoji.precreate(568838569087598627,name='0L').as_emoji,
    WALL_N|WALL_E               : Emoji.precreate(574312331849498624,name='01').as_emoji,
    WALL_N|WALL_W               : Emoji.precreate(574312332453216256,name='00').as_emoji,
    WALL_N|WALL_E|WALL_S        : Emoji.precreate(578648597621506048,name='0R').as_emoji,
    WALL_N|WALL_S|WALL_W        : Emoji.precreate(578648597546139652,name='0S').as_emoji,
    WALL_N|WALL_S               : Emoji.precreate(578654051848421406,name='0T').as_emoji,
    WALL_E|WALL_W               : Emoji.precreate(578674409968238613,name='0U').as_emoji,
    WALL_N|WALL_E|WALL_W        : Emoji.precreate(578676096829227027,name='0V').as_emoji,
    WALL_E|WALL_S|WALL_W        : Emoji.precreate(578676650389274646,name='0W').as_emoji,
        }

REIMU_STYLE = {
    WALL_N                      : Emoji.precreate(580141387631165450,name='0O').as_emoji,
    FLOOR                       : Emoji.precreate(574211101638656010,name='0H').as_emoji,
    TARGET                      : Emoji.precreate(574234087645249546,name='0A').as_emoji,
    OBJECT_P                    : NOTHING_EMOJI.as_emoji,
    HOLE_P                      : Emoji.precreate(574202754134835200,name='0I').as_emoji,
    BOX                         : Emoji.precreate(574212211434717214,name='0G').as_emoji,
    BOX_TARGET                  : Emoji.precreate(574213002190913536,name='0F').as_emoji,
    BOX_HOLE                    : Emoji.precreate(574212211434717214,name='0G').as_emoji,
    BOX_OBJECT                  : NOTHING_EMOJI.as_emoji,
    HOLE_U                      : Emoji.precreate(574187906642477066,name='0J').as_emoji,
    OBJECT_U                    : NOTHING_EMOJI.as_emoji,
    CHAR_N|FLOOR                : Emoji.precreate(574214258871500800,name='0D').as_emoji,
    CHAR_E|FLOOR                : Emoji.precreate(574213472347226114,name='0E').as_emoji,
    CHAR_S|FLOOR                : Emoji.precreate(574220751662612502,name='0B').as_emoji,
    CHAR_W|FLOOR                : Emoji.precreate(574218036156825629,name='0C').as_emoji,
    CHAR_N|TARGET               : Emoji.precreate(574249292496371732,name='04').as_emoji,
    CHAR_E|TARGET               : Emoji.precreate(574249292026478595,name='07').as_emoji,
    CHAR_S|TARGET               : Emoji.precreate(574249292261490690,name='06').as_emoji,
    CHAR_W|TARGET               : Emoji.precreate(574249292487720970,name='05').as_emoji,
    CHAR_N|HOLE_P               : Emoji.precreate(574249293662388264,name='02').as_emoji,
    CHAR_E|HOLE_P               : Emoji.precreate(574249291074240523,name='09').as_emoji,
    CHAR_S|HOLE_P               : Emoji.precreate(574249291145543681,name='08').as_emoji,
    CHAR_W|HOLE_P               : Emoji.precreate(574249292957614090,name='03').as_emoji,
    CHAR_N|OBJECT_P             : NOTHING_EMOJI.as_emoji,
    CHAR_E|OBJECT_P             : NOTHING_EMOJI.as_emoji,
    CHAR_S|OBJECT_P             : NOTHING_EMOJI.as_emoji,
    CHAR_W|OBJECT_P             : NOTHING_EMOJI.as_emoji,
        }
REIMU_STYLE.update(DEFAULT_STYLE_PARTS)

def REIMU_SKILL_ACTIVATE(self):
    size=self.source.size
    position=self.position
    map_=self.map
    
    for step in (-size,1,size,-1):
        target_tile=map_[position+step]
        
        if not target_tile&(PUSHABLE|SPECIAL):
            continue
        
        after_tile=map_[position+(step<<1)]

        if not after_tile&PASSABLE:
            continue
        
        return True
    
    return False
    
def REIMU_SKILL_USE(self,step,align):
    map_=self.map
    position=self.position
    
    target_tile=map_[position+step]
    
    if not target_tile&(PUSHABLE|SPECIAL):
        return False
    
    after_tile=map_[position+(step<<1)]

    if not after_tile&PASSABLE:
        return False

    actual_tile=map_[position]
    self.history.append(history_element(position,True,((position,actual_tile),(position+(step<<1),after_tile))))
    
    map_[position]=actual_tile&PASSABLE
    self.position=position=position+(step<<1)

    map_[position]=after_tile|align
    self.has_skill=False
    
    return True

REIMU_EMOJI=Emoji.precreate(574307645347856384,name='REIMU')

CHARS.append((REIMU_STYLE,REIMU_SKILL_ACTIVATE,REIMU_SKILL_USE,REIMU_EMOJI),)

FURANDOORU_STYLE = {
        }

FURANDOORU_STYLE = {
    WALL_N                      : Emoji.precreate(580143707534262282,name='0X').as_emoji,
    FLOOR                       : Emoji.precreate(580150656501940245,name='0Y').as_emoji,
    TARGET                      : Emoji.precreate(580153111545511967,name='0b').as_emoji,
    OBJECT_P                    : Emoji.precreate(580163014045728818,name='0e').as_emoji,
    HOLE_P                      : Emoji.precreate(580159124466303001,name='0d').as_emoji,
    BOX                         : Emoji.precreate(580151963937931277,name='0a').as_emoji,
    BOX_TARGET                  : Emoji.precreate(580188214086598667,name='0f').as_emoji,
    BOX_HOLE                    : Emoji.precreate(580151963937931277,name='0a').as_emoji,
    BOX_OBJECT                  : Emoji.precreate(580151963937931277,name='0a').as_emoji,
    HOLE_U                      : Emoji.precreate(580156463888990218,name='0c').as_emoji,
    OBJECT_U                    : Emoji.precreate(580151385258065925,name='0Z').as_emoji,
    CHAR_N|FLOOR                : Emoji.precreate(580357693022142485,name='0g').as_emoji,
    CHAR_E|FLOOR                : Emoji.precreate(580357693093576714,name='0h').as_emoji,
    CHAR_S|FLOOR                : Emoji.precreate(580357693160685578,name='0i').as_emoji,
    CHAR_W|FLOOR                : Emoji.precreate(580357693152165900,name='0j').as_emoji,
    CHAR_N|TARGET               : Emoji.precreate(580357693018210305,name='0k').as_emoji,
    CHAR_E|TARGET               : Emoji.precreate(580357693085188109,name='0l').as_emoji,
    CHAR_S|TARGET               : Emoji.precreate(580357693181657089,name='0m').as_emoji,
    CHAR_W|TARGET               : Emoji.precreate(580357693361881089,name='0n').as_emoji,
    CHAR_N|HOLE_P               : Emoji.precreate(580357693324132352,name='0o').as_emoji,
    CHAR_E|HOLE_P               : Emoji.precreate(580357693072736257,name='0p').as_emoji,
    CHAR_S|HOLE_P               : Emoji.precreate(580357693131456513,name='0q').as_emoji,
    CHAR_W|HOLE_P               : Emoji.precreate(580357693366337536,name='0r').as_emoji,
    CHAR_N|OBJECT_P             : Emoji.precreate(580357693143777300,name='0s').as_emoji,
    CHAR_E|OBJECT_P             : Emoji.precreate(580357692711763973,name='0t').as_emoji,
    CHAR_S|OBJECT_P             : Emoji.precreate(580357693269606410,name='0u').as_emoji,
    CHAR_W|OBJECT_P             : Emoji.precreate(580357693387177984,name='0v').as_emoji,
        }
FURANDOORU_STYLE.update(DEFAULT_STYLE_PARTS)

def FURANDOORU_SKILL_ACTIVATE(self):
    size=self.source.size
    position=self.position
    map_=self.map
    
    for step in (-size,1,size,-1):
        target_tile=map_[position+step]
        
        if target_tile==OBJECT_U:
            return True
    
    return False

def FURANDOORU_SKILL_USE(self,step,align):
    map_=self.map
    position=self.position
    
    target_tile=map_[position+step]
    
    if target_tile!=OBJECT_U:
        return False

    actual_tile=map_[position]
    self.history.append(history_element(position,True,((position,actual_tile),(position+step,target_tile))))
    
    map_[position]=actual_tile&PASSABLE|align
    map_[position+step]=OBJECT_P
    self.has_skill=False
    
    return True

FURANDOORU_EMOJI=Emoji.precreate(575387120147890210,name='FURANDOORU')

CHARS.append((FURANDOORU_STYLE,FURANDOORU_SKILL_ACTIVATE,FURANDOORU_SKILL_USE,FURANDOORU_EMOJI),)

YUKARI_STYLE = {
        }

def YUKARI_SKILL_ACTIVATE(self):
    map_=self.map
    
    x_size=self.source.size
    y_size=len(map_)//x_size

    position=self.position
    y_position,x_position=divmod(position,x_size)

##    x_min=x_size*y_position
##    x_max=x_size*(y_position+1)-1
##    y_min=x_position
##    y_max=x_position+(x_size*(y_size-1))
    
    for step,limit in (
            (-1,x_size*y_position),
            (1,x_size*(y_position+1)-1),
            (-x_size,-x_size),
            (x_size,x_position+(x_size*(y_size-1))),
                 ):
        target_position=position+step
        if target_position==limit:
            continue
        if not map_[target_position]&BLOCKS_LOS:
            continue
        while True:
            target_position=target_position+step
            if target_position==limit:
                break
            target_tile=map_[target_position]
            if target_tile&BLOCKS_LOS:
                continue
            if target_tile&PASSABLE:
                return True
            break
    return False

def YUKARI_SKILL_USE(self,step,align):
    map_=self.map

    x_size=self.source.size
    y_size=len(map_)//x_size
    
    position=self.position
    y_position,x_position=divmod(position,x_size)

    if step>0:
        if step==1:
            limit=x_size*(y_position+1)-1
        else:
            limit=x_position+(x_size*(y_size-1))
    else:
        if step==-1:
            limit=x_size*y_position
        else:
            limit=-x_size

    target_position=position+step
    if target_position==limit:
        return False
    if not map_[target_position]&BLOCKS_LOS:
        return False
    while True:
        target_position=target_position+step
        if target_position==limit:
            return False
        target_tile=map_[target_position]
        if target_tile&BLOCKS_LOS:
            continue
        if target_tile&PASSABLE:
            break
        return False

    actual_tile=map_[position]
    self.history.append(history_element(position,True,((position,actual_tile),(target_position,target_tile))))
    
    map_[position]=actual_tile&PASSABLE
    self.position=target_position

    map_[target_position]=target_tile|align
    self.has_skill=False
    
    return True

YUKARI_EMOJI=Emoji.precreate(575389643424661505,name='YUKARI')

CHARS.append((YUKARI_STYLE,YUKARI_SKILL_ACTIVATE,YUKARI_SKILL_USE,YUKARI_EMOJI),)

RULES_HELP=Embed('Rules of Dungeon sweeper',
    'Your quest is to help our cute Touhou characters to put their stuffs on '
    'places, where they supposed be. Theese places are marked with an '
    f'{BUILTIN_EMOJIS["x"]:e} on the floor. Because our caharcters are lazy, '
    'the less steps required to sort their stuffs, makes them give you a'
    'better rating.\n'
    '\n'
    'You can move with the reactions under the embed, to activate your '
    'characters\' skill, or go back, reset the map or cancel the game:\n'
    f'{ds_game.WEST:e}{ds_game.NORTH:e}{ds_game.SOUTH:e}{ds_game.EAST:e}'
    f'{REIMU_EMOJI:e}{ds_game.BACK:e}{ds_game.RESET:e}{ds_game.CANCEL:e}\n'
    'You can show push boxes by moving towards them, but you cannot push '
    'more at the same time time or push into the wall:\n'
    f'{REIMU_STYLE[CHAR_E|FLOOR]}'
    f'{REIMU_STYLE[BOX]}'
    f'{REIMU_STYLE[FLOOR]}'
    f'{BUILTIN_EMOJIS["arrow_right"]:e}'
    f'{REIMU_STYLE[FLOOR]}'
    f'{REIMU_STYLE[CHAR_E|FLOOR]}'
    f'{REIMU_STYLE[BOX]}'
    '\n'
    'You can push the boxes into the holes to pass them, but be careful, you '
    'might lose too much boxes to finish the stages!\n'
    f'{REIMU_STYLE[CHAR_E|FLOOR]}'
    f'{REIMU_STYLE[BOX]}'
    f'{REIMU_STYLE[HOLE_U]}'
    f'{BUILTIN_EMOJIS["arrow_right"]:e}'
    f'{REIMU_STYLE[FLOOR]}'
    f'{REIMU_STYLE[CHAR_E|FLOOR]}'
    f'{REIMU_STYLE[HOLE_P]}'
    f'{BUILTIN_EMOJIS["arrow_right"]:e}'
    f'{REIMU_STYLE[FLOOR]}'
    f'{REIMU_STYLE[FLOOR]}'
    f'{REIMU_STYLE[CHAR_E|HOLE_P]}'
    '\n'
    f'{REIMU_STYLE[CHAR_E|FLOOR]}'
    f'{REIMU_STYLE[BOX]}'
    f'{REIMU_STYLE[HOLE_P]}'
    f'{BUILTIN_EMOJIS["arrow_right"]:e}'
    f'{REIMU_STYLE[FLOOR]}'
    f'{REIMU_STYLE[CHAR_E|FLOOR]}'
    f'{REIMU_STYLE[BOX_HOLE]}'
    '\n'
    'If you get a box on the it\'s desired place it\'s color will change:\n'
    f'{REIMU_STYLE[CHAR_E|FLOOR]}'
    f'{REIMU_STYLE[BOX]}'
    f'{REIMU_STYLE[TARGET]}'
    f'{BUILTIN_EMOJIS["arrow_right"]:e}'
    f'{REIMU_STYLE[FLOOR]}'
    f'{REIMU_STYLE[CHAR_E|FLOOR]}'
    f'{REIMU_STYLE[BOX_TARGET]}'
    '\n'
    'The game has 3 chapters. *(not 3 now and there will be more.)*'
    'Each chapter introduces a different charater to play with.',
    COLORS[0])
RULES_HELP.add_field(f'Chapter 1 {REIMU_EMOJI:e}',
    'Your character is Hakurei Reimu (博麗　霊夢), who needs some help at her '
    'basement to sort her *boxes* out.\n'
    'Reimu can jump over a box or hole.\n'
    f'{REIMU_STYLE[CHAR_E|FLOOR]}'
    f'{REIMU_STYLE[BOX]}'
    f'{REIMU_STYLE[FLOOR]}'
    f'{BUILTIN_EMOJIS["arrow_right"]:e}'
    f'{REIMU_STYLE[FLOOR]}'
    f'{REIMU_STYLE[BOX]}'
    f'{REIMU_STYLE[CHAR_E|FLOOR]}'
    '\n'
    f'{REIMU_STYLE[CHAR_E|FLOOR]:}'
    f'{REIMU_STYLE[HOLE_U]}'
    f'{REIMU_STYLE[FLOOR]}'
    f'{BUILTIN_EMOJIS["arrow_right"]:e}'
    f'{REIMU_STYLE[FLOOR]}'
    f'{REIMU_STYLE[HOLE_U]}'
    f'{REIMU_STYLE[CHAR_E|FLOOR]}'
        )
RULES_HELP.add_field(f'Chapter 2 {FURANDOORU_EMOJI:e}',
    'Your character is Scarlet Flandre (スカーレット・フランドール Sukaaretto '
    'Furandooru), who want to put her *bookshelves* on their desired place.\n'
    'Flandre can destroy absolutely anything and everything, and she will get '
    'rid of the pillars stuffs for you.\n'
    f'{FURANDOORU_STYLE[CHAR_E|FLOOR]}'
    f'{FURANDOORU_STYLE[OBJECT_U]}'
    f'{BUILTIN_EMOJIS["arrow_right"]:e}'
    f'{FURANDOORU_STYLE[CHAR_E|FLOOR]}'
    f'{FURANDOORU_STYLE[OBJECT_P]}'
    f'{BUILTIN_EMOJIS["arrow_right"]:e}'
    f'{FURANDOORU_STYLE[FLOOR]}'
    f'{FURANDOORU_STYLE[CHAR_E|OBJECT_P]}'
    '\n'
    f'{FURANDOORU_STYLE[CHAR_E|FLOOR]}'
    f'{FURANDOORU_STYLE[BOX]}'
    f'{FURANDOORU_STYLE[OBJECT_P]}'
    f'{BUILTIN_EMOJIS["arrow_right"]:e}'
    f'{FURANDOORU_STYLE[FLOOR]}'
    f'{FURANDOORU_STYLE[CHAR_E|FLOOR]}'
    f'{FURANDOORU_STYLE[BOX_OBJECT]}'
        )
RULES_HELP.add_field(f'Chapter 3 {YUKARI_EMOJI:e}',
    'Your character is Yakumo Yukari (八雲　紫). Her beddings needs some '
    'replacing at her home.\n'
    'Yukari can create gaps and travel trough them. She will open gap to the '
    'closest place straightforward, which is separated by a bedding or with '
    'wall from her.'
        )

def loader(filename):

    for _ in range(len(CHARS)):
        STAGES.append(([],[],[],[]),)
            
    PATTERN_HEADER=re.compile('[a-zA-Z0-9_]+')
    PATTERN_MAP=re.compile('[A-Z_]+')

    PATTERNS = {
        'FLOOR'     : FLOOR,
        'TARGET'    : TARGET,
        'BOX'       : BOX,
        'HOLE_U'    : HOLE_U,
        'OBJECT_U'  : OBJECT_U,
        'CN_FLOOR'  : CHAR_N|FLOOR,
        'CE_FLOOR'  : CHAR_E|FLOOR,
        'CS_FLOOR'  : CHAR_S|FLOOR,
        'CW_FLOOR'  : CHAR_W|FLOOR,
        'NOTHING'   : NOTHING,
        'WALL_N'    : WALL_N,
        'WALL_E'    : WALL_E,
        'WALL_S'    : WALL_S,
        'WALL_W'    : WALL_W,
        'WALL_HV'   : WALL_N|WALL_E|WALL_S|WALL_W,
        'WALL_SE'   : WALL_E|WALL_S,
        'WALL_SW'   : WALL_S|WALL_W,
        'WALL_NE'   : WALL_N|WALL_E,
        'WALL_NW'   : WALL_N|WALL_W,
        'WALL_HE'   : WALL_N|WALL_E|WALL_S,
        'WALL_HW'   : WALL_N|WALL_S|WALL_W,
        'WALL_H'    : WALL_N|WALL_S,
        'CN_TARGET' : CHAR_N|TARGET,
        'CE_TARGET' : CHAR_E|TARGET,
        'CS_TARGET' : CHAR_S|TARGET,
        'CW_TARGET' : CHAR_W|TARGET,
        'WALL_V'    : WALL_E|WALL_W,
        'WALL_NV'   : WALL_E|WALL_S|WALL_W,
        'WALL_SV'   : WALL_N|WALL_E|WALL_W,
            }

    STATE=0
    map_=[]
    
    with open(filename,'r') as file:
        for debug_index,line in enumerate(file,1):
            try:
                if STATE==0:
                    if len(line)>2:
                        header=re.findall(PATTERN_HEADER,line)
                        STATE=1
                    
                    continue
                
                if STATE==1:
                    if len(line)>2:
                        STATE=2
                    else:
                        continue
                    
                if STATE==2:
                    if len(line)>2:
                        map_.extend(PATTERNS[element] for element in re.findall(PATTERN_MAP,line))
                    else:
                        stage_source(header,map_)
                        map_.clear()
                        STATE=0
                    continue
                
            except KeyError as err:
                print(f'Exception at line {debug_index}:\n{err!r}')
                if STATE==2:
                    print(', '.join(re.findall(PATTERN_MAP,line)))
                map_.clear()
                break
                
        if map_:
            stage_source(header,map_)
                
loader('ds.txt')

del DEFAULT_STYLE_PARTS

del REIMU_STYLE
del REIMU_SKILL_ACTIVATE
del REIMU_SKILL_USE
del REIMU_EMOJI

del FURANDOORU_STYLE
del FURANDOORU_SKILL_ACTIVATE
del FURANDOORU_SKILL_USE
del FURANDOORU_EMOJI

del YUKARI_STYLE
del YUKARI_SKILL_ACTIVATE
del YUKARI_SKILL_USE
del YUKARI_EMOJI

async def _DS_modify_best(client,message,content):
    if message.author is not client.owner:
        return
    try:
        position=int(content)
    except ValueError:
        return

    i1,rest=divmod(position,33)
    if rest<3:
        i2=0
        i3=rest
    else:
        i2,i3=divmod(rest+7,10)
        
    best=STAGES[i1][i2][i3].best
        
    position=position<<1

    count=0
    
    async with DB_ENGINE.connect() as connector:
        result = await connector.execute(DS_TABLE.select())
        stats = await result.fetchall()
        for obj in stats:
            data=obj.data
            amount=int.from_bytes(data[position:position+2],byteorder='big')

            if amount==0:
                continue
            if amount>=best:
                continue
            
            data=bytearray(data)
            data[position:position+2]=best.to_bytes(2,byteorder='big')
        
            await connector.execute(DS_TABLE.update(). \
                values(data=data). \
                where(ds_model.user_id==obj.user_id))

            count+=1

    await client.message_create(message.channel,f'modified : {count}')
    
