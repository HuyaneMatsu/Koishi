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
    
    NORTH=BUILTIN_EMOJIS['arrow_up']
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
    
    async def __call__(self,args):
        if args[1] is not self.user:
            return

        emoji=args[0]
        
        if self.task.pending() and (emoji in self.emojis_b1 or emoji in self.emojis_b2 or emoji is self.stage.source.emoji):
            return self.client.loop.create_task(self.reaction_remove(emoji))

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
                return await self.cancel()

            return

        if not result:
            return self.client.loop.create_task(self.reaction_remove(emoji))
        
        self.task.clear()

        self.client.loop.create_task(self.reaction_remove(emoji))
        
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

            target.weakrefer()
            self.target=target
            self.channel=channel
            
            client.events.reaction_add.append(self)
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

    async def reaction_remove(self,emoji):
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
        
class stage_sourse:
    CHARS={}
    __slots__=['activate_skill', 'best', 'emoji', 'map', 'name', 'size',
        'start', 'style', 'targets', 'use_skill']
    
    def __init__(self,header,map_):
        self.name=header[0]
        
        char=self.CHARS[header[1]]
        
        self.style=char[0]
        self.activate_skill=char[1]
        self.use_skill=char[2]
        self.emoji=char[3]
        
        self.targets=int(header[2])
        self.size=int(header[3])
        self.start=int(header[4])
        self.best=int(header[5])
        
        self.map=map_.copy()

        STAGES[self.name]=self
        
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
        return self.move(-self.source.size,CHAR_N)

    def move_east(self):
        return self.move(1,CHAR_E)

    def move_south(self):
        return self.move(self.source.size,CHAR_S)

    def move_west(self):
        return self.move(-1,CHAR_W)
            
    def move(self,step,align):
        if self.next_skill:
            self.next_skill=False
            return self.source.use_skill(self,step,align)
        
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

NOTHING_EMOJI=Emoji.precreate(568838460434284574,name='NOTHING')

REIMU_STYLE = {
    FLOOR                       : Emoji.precreate(574211101638656010,name='C1F').as_emoji,
    TARGET                      : Emoji.precreate(574234087645249546,name='C1T').as_emoji,
    OBJECT_P                    : NOTHING_EMOJI.as_emoji,
    HOLE_P                      : Emoji.precreate(574202754134835200,name='C1HP').as_emoji,
    BOX                         : Emoji.precreate(574212211434717214,name='C1B').as_emoji,
    BOX_TARGET                  : Emoji.precreate(574213002190913536,name='C1BT').as_emoji,
    BOX_HOLE                    : Emoji.precreate(574212211434717214,name='C1BOX').as_emoji,
    BOX_OBJECT                  : NOTHING_EMOJI.as_emoji,
    HOLE_U                      : Emoji.precreate(574187906642477066,name='C1HU').as_emoji,
    OBJECT_U                    : NOTHING_EMOJI.as_emoji,
    CHAR_N|FLOOR                : Emoji.precreate(574214258871500800,name='C1CNFHR').as_emoji,
    CHAR_E|FLOOR                : Emoji.precreate(574213472347226114,name='C1CEFHR').as_emoji,
    CHAR_S|FLOOR                : Emoji.precreate(574220751662612502,name='C1CSFHR').as_emoji,
    CHAR_W|FLOOR                : Emoji.precreate(574218036156825629,name='C1CWFHR').as_emoji,
    CHAR_N|TARGET               : Emoji.precreate(574249292496371732,name='C1CNTHR').as_emoji,
    CHAR_E|TARGET               : Emoji.precreate(574249292026478595,name='C1CETHR').as_emoji,
    CHAR_S|TARGET               : Emoji.precreate(574249292261490690,name='C1CSTHR').as_emoji,
    CHAR_W|TARGET               : Emoji.precreate(574249292487720970,name='C1CWTHR').as_emoji,
    CHAR_N|OBJECT_P             : NOTHING_EMOJI.as_emoji,
    CHAR_E|OBJECT_P             : NOTHING_EMOJI.as_emoji,
    CHAR_S|OBJECT_P             : NOTHING_EMOJI.as_emoji,
    CHAR_W|OBJECT_P             : NOTHING_EMOJI.as_emoji,
    CHAR_N|HOLE_P               : Emoji.precreate(574249293662388264,name='C1CNHPHR').as_emoji,
    CHAR_E|HOLE_P               : Emoji.precreate(574249291074240523,name='C1CEHPHR').as_emoji,
    CHAR_S|HOLE_P               : Emoji.precreate(574249291145543681,name='C1CSHPHR').as_emoji,
    CHAR_W|HOLE_P               : Emoji.precreate(574249292957614090,name='C1CWHPHR').as_emoji,
    NOTHING                     : NOTHING_EMOJI.as_emoji,
    WALL_N                      : Emoji.precreate(568838500669980712,name='C1WN').as_emoji,
    WALL_E                      : Emoji.precreate(568838488464687169,name='WE').as_emoji,
    WALL_S                      : Emoji.precreate(568838546853462035,name='WS').as_emoji,
    WALL_W                      : Emoji.precreate(568838580278132746,name='WW').as_emoji,
    WALL_N|WALL_E|WALL_S|WALL_W : NOTHING_EMOJI.as_emoji,
    WALL_S|WALL_E               : Emoji.precreate(568838557318250499,name='WSE').as_emoji,
    WALL_S|WALL_W               : Emoji.precreate(568838569087598627,name='WSW').as_emoji,
    WALL_N|WALL_E               : Emoji.precreate(574312331849498624,name='WNE').as_emoji,
    WALL_N|WALL_W               : Emoji.precreate(574312332453216256,name='WNW').as_emoji,
        }

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

stage_sourse.CHARS['REIMU']=(REIMU_STYLE,REIMU_SKILL_ACTIVATE,REIMU_SKILL_USE,Emoji.precreate(574307645347856384,name='REIMU'))

del REIMU_STYLE
del REIMU_SKILL_ACTIVATE
del REIMU_SKILL_USE


def SUKAARETTO_SKILL_ACTIVATE(self):
    size=self.source.size
    position=self.position
    map_=self.map
    
    for step in (-size,1,size,-1):
        target_tile=map_[position+step]
        
        if target_tile==OBJECT_U:
            return True
    
    return False

def SUKAARETTO_SKILL_USE(self,step,align):
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

def loader(filename):
    import re
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
        'WALL_A'    : WALL_N|WALL_E|WALL_S|WALL_W,
        'WALL_SE'   : WALL_S|WALL_E,
        'WALL_SW'   : WALL_S|WALL_W,
        'WALL_NE'   : WALL_N|WALL_E,
        'WALL_NW'   : WALL_N|WALL_W,
            }

    STATE=0
    map_=[]
    
    with open(filename,'r') as file:
        for line in file:
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
                    stage_sourse(header,map_)
                    map_.clear()
                    STATE=0
                continue
        
        if map_:
            stage_sourse(header,map_)
                
loader('ds.txt')
