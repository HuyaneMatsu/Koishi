# -*- coding: utf-8 -*-
from itertools import chain

from hata.events_compiler import content_parser
from hata.embed import Embed,Embed_field,Embed_footer
from hata.color import Color
from hata.exceptions import Forbidden,HTTPException
from help_handler import HELP
from hata.emoji import BUILTIN_EMOJIS,Emoji
from hata.futures import Future,CancelledError


#:-> @ <-:#}{#:-> @ <-:#{ command }#:-> @ <-:#}{#:-> @ <-:#

DS_GAMES={}
STAGES={}

@content_parser('str, default="\'\'"',
                'str, default="\'\'"',)
async def ds_manager(self,message,command,stage):
    while True:
        if not (0<len(command)<10):
            embed=HELP['ds']
            break

        command=command.lower()

        if command=='stages':
            return show_stages(self,message.channel)
        
        game=DS_GAMES.get(message.author.id)

        if command=='cancel':
            if game is None:
                embed=Embed('','You do not have an active game to cancel :c')
                break
            return await game.cancel()

        if command=='create':
            if game is None:
                try:
                    stage=STAGES[stage]
                except KeyError:
                    embed=Embed('',f'Unknown stage name : {stage}')
                    break

                return ds_game(self,message.channel,message.author,stage)

            else:
                embed=Embed('','You already have an active game, first cancel it to create a new one.')
                break
            
        if command=='renew':
            if game is None:
                embed=Embed('','You do not have an active game!')
                break
            else:
                return await game.renew(message.channel)

        embed=HELP['ds']
        break
        

    await self.message_create(message.channel,embed=embed)

#:-> @ <-:#}{#:-> @ <-:#{ backend }#:-> @ <-:#}{#:-> @ <-:#

class ds_game:
    
    NORTH=BUILTIN_EMOJIS['arrow_up_small']
    EAST=BUILTIN_EMOJIS['arrow_right']
    SOUTH=BUILTIN_EMOJIS['arrow_down']
    WEST=BUILTIN_EMOJIS['arrow_left']
    emojis_b1=(WEST,NORTH,SOUTH,EAST)
    
    BACK=BUILTIN_EMOJIS['leftwards_arrow_with_hook']
    RESET=BUILTIN_EMOJIS['arrows_counterclockwise']
    CANCEL=BUILTIN_EMOJIS['x']
    emojis_b2=(BACK,RESET,CANCEL)
    
    __slots__=['client', 'user', 'channel', 'target', 'task', 'stage']
    
    def __init__(self,client,channel,user,stage):
        DS_GAMES[user.id]=self
        self.client=client
        self.user=user
        self.channel=channel
        self.target=None
        self.stage=stage_solvable(stage)
        self.task=Future(client.loop)
        client.loop.create_task(self.start())
        
    async def start(self):
        client=self.client
        try:
            self.target = await client.message_create(self.channel,embed=self.render())
            for reaction in chain(self.emojis_b1,(self.stage.source.emoji,),self.emojis_b2):
                await client.reaction_add(self.target,reaction)
        except (Forbidden,HTTPException):
            try:
                if self.target is not None:
                    await client.message_create(self.channel,'',Embed('','Error meanwhile initializing'))
            except (Forbidden,HTTPException):
                pass
            del DS_GAMES[self.user.id]
        else:
            self.task.set_result(None)
            self.target.weakrefer()
            client.events.reaction_add.append(self)
            client.events.reaction_delete.append(self)
    
    async def __call__(self,args):
        if self.task.pending() or args[1] is not self.user:
            return

        emoji=args[0]

        while True:
            if emoji is self.WEST:
                if self.stage.move_west():
                    break
                return
            
            if emoji is self.NORTH:
                if self.stage.move_north():
                    break
                return

            if emoji is self.SOUTH:
                if self.stage.move_south():
                    break
                return

            if emoji is self.EAST:
                if self.stage.move_east():
                     break
                return
            
            if emoji is self.stage.source.emoji:
                if self.stage.activate_skill():
                    break
                return

            if emoji is self.BACK:
                if self.stage.back():
                    break

            if emoji is self.RESET:
                if self.stage.reset():
                    break

            if emoji is self.CANCEL:
                return await self.cancel()

            return

        self.task.clear()
        
        try:
            if self.stage.done():
                del DS_GAMES[self.user.id]
                embed=self.render_done()
            else:
                embed=self.render()
            await self.client.message_edit(self.target,embed=embed)
        except (Forbidden,HTTPException):
            return self.client.loop.create_task(self.cancel())
        finally:
            self.task.set_result(None)
                    
                    
    async def cancel(self):
        try:
            del DS_GAMES[self.user.id]
        except KeyError:
            return #already cancelled
        
        if self.task.pending():
            await self.task

        client=self.client
        
        client.events.reaction_add.remove(self)
        client.events.reaction_delete.remove(self)
        
        try:
            await client.message_create(self.channel,'',Embed('','Game cancelled'))
        except (Forbidden,HTTPException):
            pass

    async def renew(self,channel):
        if self.task.pending():
            await self.task

        client=self.client
        
        self.task.clear()
        
        try:
            target = await client.message_create(channel,embed=self.render())
            for reaction in chain(self.emojis_b1,(self.stage.source.emoji,),self.emojis_b2):
                await client.reaction_add(target,reaction)
        except (Forbidden,HTTPException):
            try:
                if self.target is not None:
                    await client.message_create(channel,'',Embed('','Error meanwhile initializing'))
            except (Forbidden,HTTPException):
                pass
            return
        else:
            client.events.reaction_add.remove(self)
            client.events.reaction_delete.remove(self)

            target.weakrefer()
            self.target=target
            self.channel=channel
            
            client.events.reaction_add.append(self)
            client.events.reaction_delete.append(self)
        finally:
            self.task.set_result(None)
        
    def render_done(self):
        stage=self.stage
        best=stage.source.best
        steps=len(stage.history)

        for raiting in 'SABCDE':
            if steps<=best:
                break
            best=best*1.2+2.
            
        embed=Embed(f'{stage.source.name} finished with {steps} steps with {raiting} raiting!',stage.render())
        embed.footer=Embed_footer(f'steps : {len(stage.history)}')

        return embed
    
    def render(self):
        stage=self.stage
        
        title_parts=[stage.source.name]
        if stage.has_skill:
            title_parts.append(stage.source.emoji.as_emoji)
            if stage.next_skill:
                title_parts.append('READY')
            
        embed=Embed(' '.join(title_parts),stage.render())
        embed.footer=Embed_footer(f'steps : {len(stage.history)}')

        return embed
    
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


YOU         = 0b0000011100000000
YOU_N       = 0b0000010000000000
YOU_E       = 0b0000010100000000
YOU_S       = 0b0000011000000000
YOU_W       = 0b0000011100000000

UN_FLOOR    = 0b0000010000000001
UE_FLOOR    = 0b0000010100000001
US_FLOOR    = 0b0000011000000001
UW_FLOOR    = 0b0000011100000001

UN_TARGET   = 0b0000010000000010
UE_TARGET   = 0b0000010100000010
US_TARGET   = 0b0000011000000010
UW_TARGET   = 0b0000011100000010

UN_OBJECT_P = 0b0000010000000011
UE_OBJECT_P = 0b0000010100000011
US_OBJECT_P = 0b0000011000000011
UW_OBJECT_P = 0b0000011100000011

UN_HOLE_P   = 0b0000010000000100
UE_HOLE_P   = 0b0000010100000100
US_HOLE_P   = 0b0000011000000100
UW_HOLE_P   = 0b0000011100000100

WALL        = 0b1111100000000000

NOTHING     = 0b0000100000000000
WALL_N      = 0b0001000000000000
WALL_E      = 0b0001100000000000
WALL_S      = 0b0010000000000000
WALL_W      = 0b0010100000000000
WALL_A      = 0b0011000000000000
WALL_SE     = 0b0011100000000000
WALL_SW     = 0b0100000000000000

UNPUSHABLE  = 0b1111100011000000

class history_element:
    __slots__=['changes', 'position', 'was_skill']
    
    def __init__(self,position,was_skill,changes):
        self.position=position
        self.was_skill=was_skill
        self.changes=changes
        
class stage_sourse:
    __slots__=['activate_skill', 'best', 'emoji', 'map', 'name', 'size',
        'start', 'style', 'targets', 'use_skill']
    
    def __init__(self,name,style,map_,targets,activate_skill,use_skill,size,start,best,emoji):
        STAGES[name]=self
        self.name=name
        self.style=style
        self.map=map_
        self.targets=targets
        self.activate_skill=activate_skill
        self.use_skill=use_skill
        self.size=size
        self.start=start
        self.best=best
        self.emoji=emoji
        
class stage_solvable:
    __slots__=['has_skill', 'history', 'map', 'next_skill', 'position',
        'source']
    
    def __init__(self,source):
        self.source=source
        self.map=source.map.copy()
        self.position=source.start
        self.history=[]
        self.has_skill=True
        self.next_skill=False
        
    def done(self):
        targets=self.source.targets
        for tile in self.map:
            if tile==BOX_TARGET:
                targets-=1
                if targets==0:
                    return True
        
        return False

    def move_north(self):
        return self.move(-self.source.size,YOU_N)

    def move_east(self):
        return self.move(1,YOU_E)

    def move_south(self):
        return self.move(self.source.size,YOU_S)

    def move_west(self):
        return self.move(-1,YOU_W)
            
    def move(self,direction,align):
        if self.next_skill:
            self.next_skill=False
            return self.source.use_skill(self,direction,align)
        
        map_=self.map
        position=self.position

        actual_tile=map_[position]
        target_tile=map_[position+direction]
        
        if target_tile&UNPUSHABLE:
            if actual_tile&YOU==align:
                return False
            else:
                map_[position]=actual_tile&PASSABLE|align
                return True
        
        if target_tile&PASSABLE:
            self.history.append(history_element(position,False,((position,actual_tile),(position+direction,target_tile))))
            
            map_[position]=actual_tile&PASSABLE
            self.position=position=position+direction
            map_[position]=target_tile|align
            
            return True

        after_tile=map_[position+(direction<<1)]

        if target_tile&PUSHABLE and after_tile&(PASSABLE|HOLE_U):
            self.history.append(history_element(self.position,False,((position,actual_tile),(position+direction,target_tile),(position+(direction<<1),after_tile))))
            
            map_[position]=actual_tile&PASSABLE
            self.position=position=position+direction
            map_[position]=(target_tile>>3)|align
            map_[position+direction]=after_tile<<3

            return True
        
        return False

    def activate_skill(self):
        return self.source.activate_skill(self)

    def render(self):
        style=self.source.style
        result=[]
        map_=self.map
        limit=len(map_)
        step=self.source.size
        
        start=0
        while start<limit:
            end=start+step
            result.append(''.join([style[element] for element in map_[start:end]]))
            start=end

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

        self.position=self.source.position
        self.map=self.source.map.copy()
        self.has_skill=True

        return True

REIMU_STYLE = {
    FLOOR       : Emoji.precreate(568838448027533333,name='FLOOR').as_emoji,
    TARGET      : Emoji.precreate(568838476884082718,name='TARGET').as_emoji,
    OBJECT_P    : Emoji.precreate(568838460434284574,name='NOTHING').as_emoji,
    BOX         : Emoji.precreate(568838416406544395,name='BOX').as_emoji,
    BOX_TARGET  : Emoji.precreate(568838435759063068,name='BOX_TARGET').as_emoji,
    BOX_HOLE    : Emoji.precreate(568838460434284574,name='NOTHING').as_emoji,
    HOLE_U      : Emoji.precreate(568838460434284574,name='NOTHING').as_emoji,
    OBJECT_U    : Emoji.precreate(568838460434284574,name='NOTHING').as_emoji,
    UN_FLOOR    : Emoji.precreate(403585482686070795,name='reimulewd').as_emoji,
    UE_FLOOR    : Emoji.precreate(403585482686070795,name='reimulewd').as_emoji,
    US_FLOOR    : Emoji.precreate(403585482686070795,name='reimulewd').as_emoji,
    UW_FLOOR    : Emoji.precreate(403585482686070795,name='reimulewd').as_emoji,
    UN_TARGET   : Emoji.precreate(403585482686070795,name='reimulewd').as_emoji,
    UE_TARGET   : Emoji.precreate(403585482686070795,name='reimulewd').as_emoji,
    US_TARGET   : Emoji.precreate(403585482686070795,name='reimulewd').as_emoji,
    UW_TARGET   : Emoji.precreate(403585482686070795,name='reimulewd').as_emoji,
    UN_OBJECT_P : Emoji.precreate(403585482686070795,name='reimulewd').as_emoji,
    UE_OBJECT_P : Emoji.precreate(403585482686070795,name='reimulewd').as_emoji,
    US_OBJECT_P : Emoji.precreate(403585482686070795,name='reimulewd').as_emoji,
    UW_OBJECT_P : Emoji.precreate(403585482686070795,name='reimulewd').as_emoji,
    UN_HOLE_P   : Emoji.precreate(403585482686070795,name='reimulewd').as_emoji,
    UE_HOLE_P   : Emoji.precreate(403585482686070795,name='reimulewd').as_emoji,
    US_HOLE_P   : Emoji.precreate(403585482686070795,name='reimulewd').as_emoji,
    UW_HOLE_P   : Emoji.precreate(403585482686070795,name='reimulewd').as_emoji,
    NOTHING     : Emoji.precreate(568838460434284574,name='NOTHING').as_emoji,
    WALL_N      : Emoji.precreate(568838500669980712,name='WALL_N').as_emoji,
    WALL_E      : Emoji.precreate(568838488464687169,name='WALL_E').as_emoji,
    WALL_S      : Emoji.precreate(568838546853462035,name='WALL_S').as_emoji,
    WALL_W      : Emoji.precreate(568838580278132746,name='WALL_W').as_emoji,
    WALL_A      : Emoji.precreate(568838460434284574,name='NOTHING').as_emoji,
    WALL_SE     : Emoji.precreate(568838557318250499,name='WALL_SE').as_emoji,
    WALL_SW     : Emoji.precreate(568838569087598627,name='WALL_SW').as_emoji,
        }

def REIMU_SKILL_ACTIVATE(self):
    if not self.has_skill:
        return False

    size=self.source.size
    position=self.position
    map_=self.map
    
    for direction in (-size,1,size,-1):
        target_tile=map_[position+direction]
        
        if not target_tile&(PUSHABLE|SPECIAL):
            continue
        
        after_tile=map_[position+(direction<<1)]

        if not after_tile&PASSABLE:
            continue
        
        self.next_skill=True
        return True
    
    return False
    
def REIMU_SKILL_USE(self,direction,align):
    map_=self.map
    position=self.position
    
    target_tile=map_[position+direction]
    
    if not target_tile&(PUSHABLE|SPECIAL):
        return False
    
    after_tile=map_[position+(direction<<1)]

    if not after_tile&PASSABLE:
        return False

    actual_tile=map_[position]
    self.history.append(history_element(position,True,((position,actual_tile),(position+(direction<<1),after_tile))))
    
    map_[position]=actual_tile&PASSABLE
    self.position=position=position+(direction<<1)

    map_[position]=after_tile|align
    self.has_skill=False
    
    return True

MAP_LAYOUT_C1_T_1 = [
    WALL_W,     WALL_N,     WALL_N,     WALL_N,     WALL_N,     WALL_N,     WALL_E,
    WALL_W,     FLOOR,      FLOOR,      FLOOR,      FLOOR,      TARGET,     WALL_E,
    WALL_W,     FLOOR,      FLOOR,      FLOOR,      FLOOR,      FLOOR,      WALL_E,
    WALL_W,     FLOOR,      FLOOR,      BOX,        FLOOR,      FLOOR,      WALL_E,
    WALL_W,     FLOOR,      US_FLOOR,   FLOOR,      FLOOR,      FLOOR,      WALL_E,
    WALL_W,     FLOOR,      FLOOR,      FLOOR,      FLOOR,      FLOOR,      WALL_E,
    NOTHING,    WALL_S,     WALL_S,     WALL_S,     WALL_S,     WALL_S,     NOTHING,
        ]

stage_sourse('C1_T_1',REIMU_STYLE,MAP_LAYOUT_C1_T_1,1,REIMU_SKILL_ACTIVATE,REIMU_SKILL_USE,7,30,7,Emoji.precreate(403585482686070795))

del MAP_LAYOUT_C1_T_1
