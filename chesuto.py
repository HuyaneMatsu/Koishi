# -*- coding: utf-8 -*-
import sys, os, re
from array import array as Array
from random import random
import json

if __name__=='__main__':
    sys.path.append(os.path.abspath('..'))

from hata.emoji import Emoji,BUILTIN_EMOJIS
from hata.futures import Task,Future,CancelledError,sync_Lock,current_thread
from hata.events import Cooldown, wait_for_message
from hata.events_compiler import ContentParser
from hata.exceptions import DiscordException
from hata.embed import Embed
from hata.dereaddons_local import asyncinit
from hata.role import Role
from hata.dereaddons_local import alchemy_incendiary,_spaceholder
from hata.color import Color
from tools import CooldownHandler

CHESUTO_COLOR=Color.from_rgb(73,245,73)

if sys.implementation.name=='cpython':
    #on cpython bisect is 4~ times faster.
    import bisect
    _relativeindex=bisect.bisect_left
    del bisect

else:
    def _relativeindex(array,value):
        bot=0
        top=len(array)
        while True:
            if bot<top:
                half=(bot+top)>>1
                if array[half]<value:
                    bot=half+1
                else:
                    top=half
                continue
            break
        return bot

#each added move is from 3 elements for a total of 24 bits:
# x coordinate 1st 8 bit
# y coordinate middle 8 bit
# what u can do there last 8 bit
#   0b00000001 <- can move
#   0b00000010 <- could move
#   0b00000100 <- can hit
#   0b00001000 <- could hit
#   0b00010000 <- can special
#   0b00100000 <- could special

class Puppet_meta(object):
    __slots__=['generate_moves', 'name', 'outlooks']
    def __init__(self,name,generate_moves,outlooks):
        self.name=name
        self.generate_moves=generate_moves
        self.outlooks=outlooks
        if getattr(type(self),name,_spaceholder) is None:
            setattr(type(self),name,self)
            return
        raise ValueError('Invalid name')
    
    rook    = None
    knight  = None
    bishop  = None
    queen   = None
    king    = None
    pawn    = None
    

def rook_moves(self,field):
    position=self.position
    y,x=divmod(position,8)
    moves=self.moves

    for dim_i,v_diff,pos_diff,v_limit in (
            (0,-1,-1,0),
            (1,-1,-8,0),
            (0,+1,+1,7),
            (1,+1,+8,7),
                ):

        local_pos=position
        if dim_i:
            local_v=y
        else:
            local_v=x
        while True:
            if local_v==v_limit:
                break
            local_v+=v_diff
            local_pos+=pos_diff
            other=field[local_pos]
            if other is None:
                can_do=0b00001011 #free
            elif self.side==other.side:
                can_do=0b00001010 #could hit
            else:
                can_do=0b00001111 #hit
                
            if dim_i:
                moves.append((x<<16)|(local_v<<8)|can_do) 
            else:
                moves.append((local_v<<16)|(y<<8)|can_do)

            if can_do!=0b00001011:
                break

    #TODO: add castling

def rook_pierce(self,target,field):
    position=self.position
    y,x=divmod(position,8)

    other_y,other_x=divmod(target.position,8)
    if y!=other_y:
        dim_i=1
        if y>other_y:
            v_limit = 7
            v_diff  = 1
            pos_diff= 8
        else:
            v_limit = 0
            v_diff  =-1
            pos_diff=-8
        local_v=y+pos_diff
    else:
        dim_i=0
        if x>other_x:
            v_limit = 7
            v_diff  = 1
            pos_diff= 1
        else:
            v_limit = 0
            v_diff  =-1
            pos_diff=-1
        local_v=x+pos_diff

    moves=[]
    local_pos=position+pos_diff
    
    found=False
    while True:
        other=field[local_pos]
        if other is None:
            if dim_i:
                moves.append((x<<16)|(local_v<<8)) 
            else:
                moves.append((local_v<<16)|(y<<8))
        else:
            if not found:
                found=True
                continue

            if other.meta is Puppet_meta.king:
                return moves
            return
        
        if local_v==v_limit:
            return
        local_v+=v_diff
        local_pos+=pos_diff


        
def knight_moves(self,field):
    position=self.position
    y,x=divmod(position,8)
    moves=self.moves

    for x_diff,y_diff,pos_diff in (
            (-1,-2,-17),
            (+1,-2,-15),
            (+2,-1, -6),
            (+2,+1,+10),
            (+1,+2,+17),
            (-1,+2,+15),
            (-2,+1, +6),
            (-2,-1,-10),
                ):

        local_x=x+x_diff
        local_y=y+y_diff
        if local_x<0 or local_x>7 or local_y<0 or local_y>7:
            continue

        other=field[position+pos_diff]
        if other is None:
            can_do=0b00001011 #free
        elif self.side==other.side:
            can_do=0b00001010 #could hit
        else:
            other.killers.append(self)
            can_do=0b00001111 #hit
        moves.append((local_x<<16)|(local_y<<8)|can_do) 

        if can_do!=0b00001011:
            break

def bishop_moves(self,field):
    position=self.position
    y,x=divmod(position,8)
    moves=self.moves

    for x_diff,y_diff,pos_diff,x_limit,y_limit in (
            (-1,-1,-9,0,0),
            (+1,-1,-7,7,0),
            (+1,+1,+9,7,7),
            (-1,+1,+7,0,7),
                ):
        local_x=x
        local_y=y
        local_pos=position

        while True:
            if local_x==x_limit or local_y==y_limit:
                break
            local_x+=x_diff
            local_y+=y_diff
            local_pos+=pos_diff

            other=field[local_pos]
            if other is None:
                can_do=0b00001011 #free
            elif self.side==other.side:
                can_do=0b00001010 #could hit
            else:
                other.killers.append(self)
                can_do=0b00001111 #hit
                
            moves.append((local_x<<16)|(local_y<<8)|can_do)

            if can_do!=0b00001011:
                break

def queen_moves(self,field):
    position=self.position
    y,x=divmod(position,8)
    moves=self.moves

    for x_diff,y_diff,pos_diff,x_limit,y_limit in (
            (-1,-1,-9,0,0),
            ( 0,-1,-8,8,0),
            (+1,-1,-7,7,0),
            (+1, 0,+1,7,8),
            (+1,+1,+9,7,7),
            ( 0,+1,+8,8,7),
            (-1,+1,+7,0,7),
            (-1, 0,-1,0,8),
                ):
        
        local_x=x
        local_y=y
        local_pos=position
        while True:
            if local_x==x_limit or local_y==y_limit:
                break
            local_x+=x_diff
            local_y+=y_diff
            local_pos+=pos_diff

            other=field[local_pos]
            if other is None:
                can_do=0b00001011 #free
            elif self.side==other.side:
                can_do=0b00001010 #could hit
            else:
                other.killers.append(self)
                can_do=0b00001111 #hit
            moves.append((local_x<<16)|(local_y<<8)|can_do)

            if can_do!=0b00001011:
                break
            break

def king_moves(self,field):
    position=self.position
    y,x=divmod(position,8)
    moves=self.moves

    for x_diff,y_diff,pos_diff,x_limit,y_limit in (
            (-1,-1,-9,0,0),
            ( 0,-1,-8,8,0),
            (+1,-1,-7,7,0),
            (+1, 0,+1,7,8),
            (+1,+1,+9,7,7),
            ( 0,+1,+8,8,7),
            (-1,+1,+7,0,7),
            (-1, 0,-1,0,8),
                ):
        
        if x==x_limit or y==y_limit:
            continue
        
        local_x=x+x_diff
        local_y=y+y_diff
        local_pos=position+pos_diff

        other=field[local_pos]
        if other is None:
            can_do=0b00001011 #free
        elif self.side==other.side:
            can_do=0b00001010 #could hit
        else:
            other.killers.append(self)
            can_do=0b00001111 #hit
        
        moves.append((local_x<<16)|(local_y<<8)|can_do)

    #TODO : add castling

def pawn_moves(self,field):
    position=self.position
    y,x=divmod(position,8)
    moves=self.moves

    if self.side:
        other=field[position+8]
        if y==6:
            can_do=0b00110011 if other is None else 0b00100010
            moves.append((x<<16)|(7<<8)|can_do) #evolve

            if x>0:
                other=field[position+7]
                if other is None or self.side==other.side:
                    can_do=0b00101000 #could hit
                else:
                    moves.killers.append(self)
                    can_do=0b00111101 #hit
                moves.append(((x-1)<<16)|(7<<8)|can_do)
                    
            if x<7:
                other=field[position+9]
                if other is None or self.side==other.side:
                    can_do=0b00101000 #could hit
                else:
                    other.killers.append(self)
                    can_do=0b00111101 #hit
                moves.append(((x+1)<<16)|((y+1)<<8)|can_do)
        else:
            can_do=0b00000011 if other is None else 0b00000010
            moves.append((x<<16)|((y+1)<<8)|can_do) #general forward
            if other is None and not self.moved and y<2:
                other=field[position+16]
                can_do=0b00000011 if other is None else 0b00000010
                moves.append((x<<16)|((y+2)<<8)|can_do) #double on default position

            if x>0:
                other=field[position+7]
                if other is None or self.side==other.side:
                    can_do=0b00001000 #could hit
                else:
                    moves.killers.append(self)
                    can_do=0b00001101 #hit
                moves.append(((x-1)<<16)|((y+1)<<8)|can_do)
                    
            if x<7:
                other=field[position+9]
                if other is None or self.side==other.side:
                    can_do=0b00001000 #could hit
                else:
                    other.killers.append(self)
                    can_do=0b00001101 #can hit
                moves.append(((x+1)<<16)|((y+1)<<8)|can_do)
    else:
        other=field[position-8]
        if y==1:
            can_do=0b00110011 if other is None else 0b00100010
            moves.append((x<<8)|can_do) #evolve

            if x>0:
                other=field[position-9]
                if other is None or self.side==other.side:
                    can_do=0b00101000 #could hit
                else:
                    other.killers.append(self)
                    can_do=0b00111101 #hit
                moves.append(((x-1)<<16)|can_do)
                
            if x<7:
                other=field[position-7]
                if other is None or self.side==other.side:
                    can_do=0b00001000 #could hit
                else:
                    other.killers.append(self)
                    can_do=0b00001101 #hit
                moves.append(((x+1)<<16)|((y-1)<<8)|can_do)
                    
        else:
            can_do=0b00000011 if other is None else 0b00000010
            moves.append((x<<16)|((y-1)<<8)|can_do) #general forward
            if other is None and not self.moved and y>5:
                other=field[position-16]
                can_do=0b00000011 if other is None else 0b00000010
                moves.append((x<<16)|((y-2)<<8)|can_do) #double on default position
                
            if x>0:
                other=field[position-9]
                if other is None or self.side==other.side:
                    can_do=0b00001000 #could hit
                else:
                    other.killers.append(self)
                    can_do=0b00001101 #hit
                moves.append(((x-1)<<16)|((y-1)<<8)|can_do)
            
            if x<7:
                other=field[position-7]
                if other is None or self.side==other.side:
                    can_do=0b00001000 #could hit
                else:
                    other.killers.append(self)
                    can_do=0b00001101 #hit
                moves.append(((x+1)<<16)|((y-1)<<8)|can_do)

def check_king_moves(player,others,field):
    king=player.king
    moves=king.moves
    for index in reversed(range(len(moves))):
        element=moves[index]
        if element&0b00000001:
            binary_pos=element&0xffff00
            
            other_index=0
            other_limit=len(others)
            other_moves=others[0].moves
            move_index=0
            move_limit=len(other_moves)
            
            while True:
                if move_index<move_limit:
                    move=other_moves[move_index]
                    if move&0xffff00==binary_pos and move&0b00001000:
                        del moves[index]
                        break
                    move_index=move_index+1
                    continue

                other_index=other_index+1
                if other_index==other_limit:
                    break
                other_moves=others[other_index].moves
                move_index=0
                move_limit=len(other_moves)

    position=king.position
    x,y=divmod(position,8)
    if len(king.killers)==0:
        moves=[]
        found=None
        for x_diff,y_diff,pos_diff,x_limit,y_limit in (
                (-1,-1,-9,0,0),
                ( 0,-1,-8,8,0),
                (+1,-1,-7,7,0),
                (+1, 0,+1,7,8),
                (+1,+1,+9,7,7),
                ( 0,+1,+8,8,7),
                (-1,+1,+7,0,7),
                (-1, 0,-1,0,8),
                    ):
            
            local_x=x
            local_y=y
            local_pos=position
            while True:
                if local_x==x_limit or local_y==y_limit:
                    break
                local_x+=x_diff
                local_y+=y_diff
                local_pos+=pos_diff
                
                if found is None:
                    other=field[local_pos]
                    #empty
                    if other is None:
                        moves.append((local_x<<16)|(local_y<<8))
                        continue
                    #same side
                    if king.side==other.side:
                        found=other
                        continue
                    #enemy:
                    break

                #empty
                if other is None:
                    moves.append((local_x<<16)|(local_y<<8))
                    continue
                #same side
                if king.side==other.side:
                   break
                #enemy!
                if other.meta is not Puppet_meta.queen:
                    if x_diff==0 or y_diff==0: #front
                        if other.meta is not Puppet_meta.rook:
                            break
                    else: #size
                        if other.meta is not Puppet_meta.bishop:
                            break

                other_moves=found.moves
                for index in reversed(range(len(other_moves))):
                    move=other_moves[index]
                    if move&0xffff00 not in moves:
                        del move[index]

            moves.clear()
        return
    
    if len(king.killers)==1:
        killer=king.killers[0]
            
        if killer.meta in (Puppet_meta.rook,Puppet_meta.bishop,Puppet_meta.queen):
            local_y,  local_x=divmod(position,8)
            killer_y,killer_x=divmod(killer.position,8)
            pos_diff=0
            if   local_x>killer_x:
                x_diff=-1
                pos_diff=pos_diff-1
            elif local_x<killer_x:
                x_diff=+1
                pos_diff=pos_diff+1
            else:
                x_diff= 0
            if   local_y>killer_y:
                y_diff=-1
                pos_diff=pos_diff-8
            elif local_y<killer_y:
                y_diff=+1
                pos_diff=pos_diff+8
            else:
                y_diff= 0

            local_pos=position
            moves=[]
            while True:
                local_pos=local_pos+pos_diff
                other=field[local_pos]

                if other is not None:
                    break
                
                local_x=local_x+x_diff
                local_y=local_y+y_diff
                moves.append((local_x<<16)|(local_y<<8))
            
            if moves:
                killer_pos=(killer_x<<16)|(killer_y<<8)
                
                for puppet in player.puppets:
                    if puppet is king:
                        continue
                    other_moves=puppet.moves
                    for index in reversed(range(len(other_moves))):
                        move=other_moves[index]
                        partial_move=move&0xffff00
                        if partial_move in moves:
                            continue

                        if partial_move==killer_pos and move&0b00000100:
                            continue
                        
                        del move[index]
                return

        killers=killer.killers
        killer_pos=killer.position
        killer_pos=((killer_pos&0b00000111)<<16)|((killer_pos&0b00111000)<<5)
        if killers:
            for puppet in player.puppets:
                if puppet is king:
                    continue
                if puppet in killers:
                    other_moves=puppet.moves
                    for move in other_moves:
                        if move&0xffff00==killer_pos:
                            break
                    else:
                        continue
                    
                    other_moves.clear()
                    other_moves.append(move)
                    continue
                
                puppet.moves.clear()
        return
    
    for puppet in player.puppets:
        if puppet is king:
            continue
        puppet.moves.clear()

Puppet_meta('rook',     rook_moves,     (
    Emoji.precreate(604652042635706416,name='a0').as_emoji,
    Emoji.precreate(604657343950487562,name='a1').as_emoji,
    Emoji.precreate(604652042669129788,name='a2').as_emoji,
    Emoji.precreate(604652042652483591,name='a3').as_emoji,
        ))
            
Puppet_meta('knight',   knight_moves,   (
    Emoji.precreate(604652042350362625,name='a4').as_emoji,
    Emoji.precreate(604652042413146113,name='a5').as_emoji,
    Emoji.precreate(604652042853548042,name='a6').as_emoji,
    Emoji.precreate(604652042740301835,name='a7').as_emoji,
        ))
    
Puppet_meta('bishop',   bishop_moves,   (
    Emoji.precreate(604652042694426634,name='a8').as_emoji,
    Emoji.precreate(604652042715398144,name='a9').as_emoji,
    Emoji.precreate(604652042253762571,name='aa').as_emoji,
    Emoji.precreate(604652042581180425,name='ab').as_emoji,
        ))

Puppet_meta('queen',    queen_moves,    (
    Emoji.precreate(604657915038793728,name='ac').as_emoji,
    Emoji.precreate(604657914820558849,name='ad').as_emoji,
    Emoji.precreate(604652042732175390,name='ae').as_emoji,
    Emoji.precreate(604652042639638550,name='af').as_emoji,
        ))
    
Puppet_meta('king',     king_moves,     (
    Emoji.precreate(604658587117027328,name='ag').as_emoji,
    Emoji.precreate(604658587121221642,name='ah').as_emoji,
    Emoji.precreate(604652042790895616,name='ai').as_emoji,
    Emoji.precreate(604658586978746378,name='aj').as_emoji,
        ))
    
Puppet_meta('pawn',     pawn_moves,     (
    Emoji.precreate(604652042656677918,name='ak').as_emoji,
    Emoji.precreate(604652042731913216,name='al').as_emoji,
    Emoji.precreate(604652042702815313,name='am').as_emoji,
    Emoji.precreate(604652042484711424,name='an').as_emoji,
        ))
    
del rook_moves
del knight_moves
del bishop_moves
del queen_moves
del king_moves
del pawn_moves

EMPTY_TILE=(
    Emoji.precreate(604652042639900672,name='ao').as_emoji,
    Emoji.precreate(604652044246188065,name='ap').as_emoji,
        )

NUMBERS=(
    Emoji.precreate(604698116427350016,name='aq').as_emoji,
    Emoji.precreate(604698116444258469,name='ar').as_emoji,
    Emoji.precreate(604698116431675406,name='as').as_emoji,
    Emoji.precreate(604698116444258475,name='at').as_emoji,
    Emoji.precreate(604698116226285589,name='au').as_emoji,
    Emoji.precreate(604698116578476149,name='av').as_emoji,
    Emoji.precreate(604698116448452674,name='aw').as_emoji,
    Emoji.precreate(604698116494590202,name='ax').as_emoji,
        )

LETTERS=(
    Emoji.precreate(604698116129816586,name='ay').as_emoji,
    Emoji.precreate(604698116675076106,name='az').as_emoji,
    Emoji.precreate(604698116482007194,name='aA').as_emoji,
    Emoji.precreate(604698116435738625,name='aB').as_emoji,
    Emoji.precreate(604698116163371009,name='aC').as_emoji,
    Emoji.precreate(604698116490264586,name='aD').as_emoji,
    Emoji.precreate(604698116548984832,name='aE').as_emoji,
    Emoji.precreate(604698116540596252,name='aF').as_emoji,
        )

EDGE=Emoji.precreate(604698116658167808,name='aG').as_emoji

class Puppet(object):
    __slots__=['effects', 'meta', 'moved', 'position', 'side','moves','killers']
    def __init__(self,meta,position,side):
        self.meta       = meta
        self.position   = position
        self.side       = side
        self.effects    = []
        self.moved      = [] #needs for special checks
        self.moves      = []
        self.killers    = []

    def update(self,field):
        for effect in self.effects:
            effect.apply(self)

        self.moves.clear()
        self.killers.clear()
        
        self.meta.generate_moves(self,field)

    def __repr__(self):
        return f'<{("light","dark")[self.side]} {self.meta.name} effetcts=[{", ".join([repr(effect) for effect in self.effects])}]>'

COMMAND_RP=re.compile('[ \-]*([a-z]+)[ \-]+',re.I)
MOVE_RP=re.compile('([a-h])([1-8])[ \-]*([a-h])([1-8])[ \-]*',re.I)

class ChesutoBackend(object):
    __slots__=['client', 'field','players', 'channel', 'next']
    def __init__(self,client,channel,player_0,player_1):
        self.client=client
        self.channel=channel

        self.field=[
            Puppet(Puppet_meta.rook,    0,  1),
            Puppet(Puppet_meta.knight,  1,  1),
            Puppet(Puppet_meta.bishop,  2,  1),
            Puppet(Puppet_meta.queen,   3,  1),
            Puppet(Puppet_meta.king,    4,  1),
            Puppet(Puppet_meta.bishop,  5,  1),
            Puppet(Puppet_meta.knight,  6,  1),
            Puppet(Puppet_meta.rook,    7,  1),
            *(Puppet(Puppet_meta.pawn,  pos,1) for pos in range(8,16)),
            *(None for _ in range(16,48)),
            *(Puppet(Puppet_meta.pawn,  pos,0) for pos in range(48,56)),
            Puppet(Puppet_meta.rook,    56, 0),
            Puppet(Puppet_meta.knight,  57, 0),
            Puppet(Puppet_meta.bishop,  58, 0),
            Puppet(Puppet_meta.queen,   59, 0),
            Puppet(Puppet_meta.king,    60, 0),
            Puppet(Puppet_meta.bishop,  61, 0),
            Puppet(Puppet_meta.knight,  62, 0),
            Puppet(Puppet_meta.rook,    63, 0),
                ]

        self.players=(player_0(self,0),player_1(self,1))
        
        Task(self.initial_messages(),client.loop)

    async def initial_messages(self):
        client=self.client
        dms_disabled=[]
        player1,player2=self.players
        
        embed=Embed('',self.render(),color=CHESUTO_COLOR)
        embed.add_footer('It is your turn now!')
        
        try:
            await client.message_create(player1.channel,embed=embed)
        except DiscordException:
            dms_disabled.append(player1.user)

        embed.add_footer('It is your opponents turn!')
        
        try:
            await client.message_create(player2.channel,embed=embed)
        except DiscordException:
            dms_disabled.append(player2.user)

        if dms_disabled:
            if len(dms_disabled)==2:
                disabled_text=f'{dms_disabled[0]:f} and {dms_disabled[1]:f} has dms disabled'
            else:
                disabled_text='{dms_disabled[0]:f} has dms disabled'

            try:
                await client.message_create(self.channel,
                    embed=Embed('Could not start the game.',disabled_text,color=CHESUTO_COLOR))
            except DiscordException:
                pass
            return

        return #TODO

        event=client.events.message_create
        for player in self.players:
            event.append(self,player.channel)

        self.next=0
        self.update_puppets()

    def __call__(self,message):
        next_=self.next
        player=self.players[next_]
        if message.author!=player.user:
            return #the other user

        content=message.content
        parsed=COMMAND_RP.match(content)
        if parsed is None:
            return # no command detected
        command=parsed.group(1).lower()
        if command=='move':
            parsed=MOVE_RP.match(message.content,parsed.end())
            if parsed is None:
                return #invalid move
            source_x,source_y,target_x,target_y=parsed.groups()
            source_x=ord(source_x)-65
            if source_x>8:
                source_x=source_x-32
            source_y=56-ord(source_y)
            target_x=ord(target_x)-65
            if source_x>8:
                source_x=source_x-32
            target_y=56-ord(target_y)

            source_pos=(source_y<<3)|source_x
            source_puppet=self.field[source_pos]
            if source_puppet is None:
                return #nothing to move
            if source_puppet.side!=next_:
                return #not your
            target_rel_pos=(target_x<<16)|(target_y<<8)
            for move in source_puppet.moves:
                if move&0xffff00==target_rel_pos:
                    break
            else:
                return # we cannot move there
            target_pos=(target_y<<3)|target_x
            target_puppet=self.field[target_pos]

            source_puppet.position=target_pos
            source_puppet.moves.append((source_pos,target_pos,),)
            self.field[source_pos]=None
            self.field[target_pos]=target_puppet
            if target_puppet is not None:
                self.players[next_^1].puppets.remove(target_puppet)

            self.update_puppets()



        return


        
    def check(self,player,x,y):
        puppet=self.field[x+(y<<3)]
        if puppet is not None:
            return puppet.moves,puppet.killers

        binary_pos=(x<<16)+(y<<8)
        moves=[]
        killers=[]
        player2=self.players[player.side^1]

        for puppet_ in player.puppets:
            for move in puppet_.moves:
                if move&0xffff00==binary_pos and move&0b00000001:
                    position=puppet_.position
                    moves.append(((position&0b00000111)<<16)|((position&0b00111000)<<5)|0b00000001)
        for puppet_ in player2.puppets:
            for move in puppet_.moves:
                if move&0xffff00==binary_pos and move&0b00001000:
                    killers.append(puppet_)

        return moves,killers
            
    def update_puppets(self):
        field=self.field
        players=self.players
        for player in players:
            for puppet in player.puppets:
                puppet.update(field)
                
        check_king_moves(players[0],players[1],field)
        check_king_moves(players[1],players[0],field)

    def __repr__(self):
        result=[]
        
        line=['|---' for _ in range(8)]
        line.append('|\n')
        line_breaker=''.join(line)
        line.clear()
        
        field=self.field
        for y in range(0,64,8):
            result.append(line_breaker)
            
            for pos in range(y,y+8):
                line.append('|')
                puppet=field[pos]
                if puppet is None:
                    line.append('   ')
                else:
                    line.append(f'{("B","D")[puppet.side]}{puppet.meta.name[:2]}')
            line.append('|\n')
            
            result.append(''.join(line))
            line.clear()

        result.append(line_breaker)
        return ''.join(result)
    
    def render(self):
        field=self.field
        result=[]
        position=0
        color=0
        while True:
            limit=position+8
            while True:
                puppet=field[position]
                if puppet is None:
                    result.append(EMPTY_TILE[color])
                else:
                    result.append(puppet.meta.outlooks[color|(puppet.side<<1)])
                position=position+1
                if position==limit:
                    break
                color=color^1
            result.append(NUMBERS[8-(position>>3)])
            result.append('\n')
            if position==64:
                break
            
        result.extend(LETTERS)
        result.append(EDGE)
        return ''.join(result)
            
class ChesutoPlayer(object):
    __slots__=['backend', 'channel', 'puppets', 'side', 'user', 'king', 'in_check']
    def __init__(self,user,channel):
        self.user=user
        self.channel=channel
        self.in_check=False
        
    def __call__(self,backend,side):
        self.backend=backend
        self.side=side
        
        if side:
            self.king   =backend.field[4]
            self.puppets=backend.field[:16]
        else:
            self.king   =backend.field[60]
            self.puppets=backend.field[48:]
        return self

class Rarity():
    count=0
    values=[]
    by_name={}
    __slots__=['index', 'name',]
    def __init__(self,name):
        self.name=name
        index=self.count
        self.index=index
        type(self).count=index+1
        self.values.append(self)
        self.by_names[name]=self
        
    def __str__(self):
        return self.name

    def __repr__(self):
        return f'{self.__class__.__name__}(name={self.name}, index={self.index})'

    def __gt__(self,other):
        return self.index>other.index
    def __ge__(self,other):
        return self.index>=other.index
    def __eq__(self,other):
        return self.index==other.index
    def __ne__(self,other):
        return self.index!=other.index
    def __le__(self,other):
        return self.index<=other.index
    def __lt__(self,other):
        return self.index<other.index

    def __hash__(self):
        return self.index

Rarity('Common'),
Rarity('Uncommon'),
Rarity('Rare'),
Rarity('Legendary'),
Rarity('Mythic'),

CARDS_by_id={}
CARDS_by_name={}
EFFECTS={}

class Card():
    __slots__=['acquirable', 'description', 'effect', 'effectname', 'id', 'name', 'rarity', 'token']
    def __init__(self,acquirable,description,effectname,id_,name,rarity,token):
        self.id         = id_
        self.name       = name
        self.description= description
        self.rarity     = rarity
        self.acquirable = acquirable
        self.token      = token
        self.effectname = effectname
        self.effect     = EFFECTS.get(effectname)
        CARDS_by_id[id_]= self
        CARDS_by_name[name.lower()]=self

    def __hash__(self):
        return self.id

    FILENAME='CHESUTO.json'
    FILELOCK=sync_Lock()

    @classmethod
    async def dump_cards(cls,loop):
        card_datas=[]
        for card in CARDS_by_id.values():
            card_data={}
            card_data['acquirable'] = card.acquirable
            card_data['description']= card.description
            card_data['effectname'] = card.effectname
            card_data['id']         = card.id
            card_data['name']       = card.name
            card_data['rarity']     = card.rarity.index
            card_data['token']      = card.token
            card_datas.append(card_data)
        
        await loop.run_in_executor(alchemy_incendiary(cls._dump_cards,(card_datas,),),)
            
    @classmethod
    def _dump_cards(cls,card_datas):
        with cls.FILELOCK:
            with open(cls.FILENAME,'w') as file:
                json.dump(card_datas,file,indent=4)

    @classmethod
    async def load_cards(cls,loop):
        if CARDS_by_id:
            future=Future()
            future.set_result(None)
            return future
        
        cards_data = await loop.run_in_executor(cls._load_cards)
        exception=None
        while True:
            if type(cards_data) is str:
                exception=cards_data
                break

            if type(cards_data) is not list:
                exception=f'Expected type \'list\' for \'cards_data\', got \'{carsd_data.__class__.__name__}\''
                break

            break

        if exception is not None:
            sys.stderr.write(f'Exception at loading cards:\n{exception}\n')
            return
            
        for card_data in cards_data:
            while True:
                if type(card_data) is not dict:
                    exception=f'Expcted type \'dict\' for \'card_data\', got \'{card_data.__class__.__name__}\''
                    break
                
                try:
                    acquirable=card_data['acquirable']
                except KeyError:
                    exception='No \'acquirable\' key'
                    break
                
                if type(acquirable) is not bool:
                    exception=f'Expected type \'bool\' for \'acquirable\', got \'{acquirable.__class__.__name__}\''
                    break
                
                try:
                    description=card_data['description']
                except KeyError:
                    exception='No \'description\' key'
                    break

                if type(description) is not str:
                    exception=f'Expected type \'str\' for \'description\', got \'{description.__class__.__name__}\''
                    break

                try:
                    effectname=card_data['effectname']
                except KeyError:
                    exception='No \'effectname\' key'
                    break

                if type(effectname) is not str:
                    exception=f'Expected type \'str\' for \'effectname\', got \'{effectname.__class__.__name__}\''
                    break
                    
                try:
                    id_=card_data['id']
                except KeyError:
                    excception='No \'id\' key'
                    break
                
                if type(id_) is not int:
                    exception=f'Expected type \'int\' for \'id\', got \'{id_.__class__.__name__}\''
                    break
                
                try:
                    name=card_data['name']
                except KeyError:
                    exception='No \'name\' key'
                    break

                if type(name) is not str:
                    exception=f'Expected type \'str\' for \'name\', got \'{name.__class__.__name__}\''
                    break
                    
                try:
                    rarity=card_data['rarity']
                except KeyError:
                    exception='No \'rarity\' key'
                    break

                if type(rarity) is not int:
                    exception=f'Expected type \'int\' for \'rarity\', got \'{rarity.__class__.__name__}\''
                    break

                try:
                    rarity=Rarity.values[rarity]
                except IndexError:
                    exception=f'No such \'rarity\' index: {rarity}'
                    break

                try:
                    token=card_data['token']
                except KeyError:
                    exception='No \'token\' key'
                    break
                
                if type(token) is not bool:
                    exception=f'Expected type \'bool\' for \'token\', got \'{token.__class__.__name__}\''
                    break
                
                break

            if exception is None:
                Card(acquirable,description,effectname,id_,name,rarity,token)
                continue

            sys.stderr.write(f'Exception at loading cards:\n{exception}\n At data part:\n{card_data}\n')
            exception=None
            continue

    @classmethod
    def _load_cards(cls):
        with cls.FILELOCK:
            try:
                with open(cls.FILENAME,'r') as file:
                    cards_data=json.load(file)
            except FileNotFoundError:
                return 'file not found'
            except OSError as err:
                return err.strerror
            else:
                return cards_data
            

        
CARDS_ROLE=Role.precreate(598708907816517632)

class check_user_and_ln():
    __slots__=['user', 'ln_limits']
    def __init__(self,user,ln_limits):
        self.user=user
        self.ln_limits=ln_limits
    def __call__(self,message):
        if message.author!=self.user:
            return False
        ln_limits=self.ln_limits
        ln=len(message.content)
        return ln_limits[0]<ln<ln_limits[1]

YES_RP=re.compile('1|yes|ye|y|hai|',re.I)
NO_RP=re.compile('2|nope|nop|no|n',re.I)
CANCEL_RP=re.compile('cancel',re.I)

class check_user_and_ync():
    __slots__=['user']
    def __init__(self,user):
        self.user=user
    def __call__(self,message):
        if message.author!=self.user:
            return False
        content=message.content
        if YES_RP.fullmatch(content) is not None:
            return 1
        if NO_RP.fullmatch(content) is not None:
            return 0
        if CANCEL_RP.fullmatch(content) is not None:
            return 2
        
        return False

class check_user_and_rarity():
    __slots__=['user']
    def __init__(self,user):
        self.user=user
    def __call__(self,message):
        if message.author!=self.user:
            return False
        try:
            rarity=Rarity.by_name[message.content.title()]
        except KeyError:
            return False
        return rarity

class check_user_and_tf():
    __slots__=['user']
    def __init__(self,user):
        self.user=user
    def __call__(self,message):
        if message.author!=self.user:
            return False
        content=message.content.lower()
        if content=='true':
            return 1
        if content=='false':
            return 0
        return False

EN_RP=re.compile('([a-z][a-z_0-9]{2,})',re.I)

class check_user_and_en():
    __slots__=['user']
    def __init__(self,user):
        self.user=user
    def __call__(self,message):
        if message.author!=self.user:
            return False
        content=message.content.lower()
        ln=len(content)
        if ln<3 or ln>32:
            return False
        if EN_RP.fullmatch(content) is None:
            return False
        return content


async def create_card(client,message,content):
    while True:
        try:
            profile=message.author.guild_profiles[CARDS_ROLE.guild]
        except KeyError:
            pass
        else:
            if CARDS_ROLE in profile.roles:
                break
        await client.message_create(message.channel,'You do not have permission to use this command')
        return

    channel=message.channel
    user=message.author
    
    card=object.__new__(Card)
    card.id=message.id
    
    while True:
        await client.message_create(channel,'Please enter the `name` of your card.\nLenght: 3-100')
        
        try:
            message = await wait_for_message(client,channel,check_user_and_ln(user,(2,101),),300.)
        except TimeoutError:
            await client.message_create(channel,'Timeout occured, card adding cancelled')
            return
        
        value=message.content
        await client.message_create(channel,f'Inputted name:\n```\n{value}\n```\nIs it correct?\nYes / No / Cancel')
        
        try:
            message,correct = await wait_for_message(client,channel,check_user_and_ync(user),300.)
        except TimeoutError:
            await client.message_create(channel,'Timeout occured, card adding cancelled')
            return
        
        if correct==0:
            continue
        if correct==1:
            break
        return

    card.name=value

    while True:
        await client.message_create(channel,'Please enter the `description` of your card.\nLenght: 3-1000')
        
        try:
            message = await wait_for_message(client,channel,check_user_and_ln(user,(2,1001),),300.)
        except TimeoutError:
            await client.message_create(channel,'Timeout occured, card adding cancelled')
            return
        
        value=message.content
        await client.message_create(channel,f'Inputted description:\n```\n{value}\n```\nIs it correct?\nYes / No / Cancel')
        
        try:
            message,correct = await wait_for_message(client,channel,check_user_and_ync(user),300.)
        except TimeoutError:
            await client.message_create(channel,'Timeout occured, card adding cancelled')
            return
        
        if correct==0:
            continue
        if correct==1:
            break
        return

    card.description=value

    while True:
        await client.message_create(channel,'Please enter the `acquirable` of your card.\nTrue / False')
        
        try:
            message,value = await wait_for_message(client,channel,check_user_and_tf(user),300.)
        except TimeoutError:
            await client.message_create(channel,'Timeout occured, card adding cancelled')
            return

        value=(False,True)[value]
        
        await client.message_create(channel,f'Inputted acquirable:\n```\n{value}\n```\nIs it correct?\nYes / No / Cancel')
        
        try:
            message,correct = await wait_for_message(client,channel,check_user_and_ync(user),300.)
        except TimeoutError:
            await client.message_create(channel,'Timeout occured, card adding cancelled')
            return
        
        if correct==0:
            continue
        if correct==1:
            break
        return

    card.acquirable=value
    
    while True:
        await client.message_create(channel,'Please enter the `token` of your card.\nTrue / False')
        
        try:
            message,value = await wait_for_message(client,channel,check_user_and_tf(user),300.)
        except TimeoutError:
            await client.message_create(channel,'Timeout occured, card adding cancelled')
            return

        value=(False,True)[value]
        
        await client.message_create(channel,f'Inputted token:\n```\n{value}\n```\nIs it correct?\nYes / No / Cancel')
        
        try:
            message,correct = await wait_for_message(client,channel,check_user_and_ync(user),300.)
        except TimeoutError:
            await client.message_create(channel,'Timeout occured, card adding cancelled')
            return
        
        if correct==0:
            continue
        if correct==1:
            break
        return

    card.token=value

    while True:
        await client.message_create(channel,'Please enter the `effectname` of your card.\nLenght: 3-32')
        
        try:
            message,value = await wait_for_message(client,channel,check_user_and_en(user),300.)
        except TimeoutError:
            await client.message_create(channel,'Timeout occured, card adding cancelled')
            return
        
        await client.message_create(channel,f'Inputted effectname:\n```\n{value}\n```\nIs it correct?\nYes / No / Cancel')
        
        try:
            message,correct = await wait_for_message(client,channel,check_user_and_ync(user),300.)
        except TimeoutError:
            await client.message_create(channel,'Timeout occured, card adding cancelled')
            return
        
        if correct==0:
            continue
        if correct==1:
            break
        return

    card.effectname=value
    card.effect=EFFECTS.get(value)

    while True:
        await client.message_create(channel,'Please enter the `rarity` of your card.')
        
        try:
            message,value = await wait_for_message(client,channel,check_user_and_rarity(user),300.)
        except TimeoutError:
            await client.message_create(channel,'Timeout occured, card adding cancelled')
            return
        
        await client.message_create(channel,f'Inputted rarity:\n```\n{value}\n```\nIs it correct?\nYes / No / Cancel')
        
        try:
            message,correct = await wait_for_message(client,channel,check_user_and_ync(user),300.)
        except TimeoutError:
            await client.message_create(channel,'Timeout occured, card adding cancelled')
            return
        
        if correct==0:
            continue
        if correct==1:
            break
        return

    card.rarity=value

    embed=Embed('Do it?',color=CHESUTO_COLOR)
    embed.add_field('name',         card.name)
    embed.add_field('description',  card.description)
    embed.add_field('acquirable',   str(card.acquirable))
    embed.add_field('token',        str(card.token))
    embed.add_field('effectname',   card.effectname)
    embed.add_field('rarity',       str(card.rarity))
    embed.add_footer('Yes / No / Cancel')
    
    await client.message_create(channel,embed=embed)
    
    try:
        message,correct = await wait_for_message(client,channel,check_user_and_ync(user),300.)
    except TimeoutError:
        await client.message_create(channel,'Timeout occured, card adding cancelled')
        return

    if correct==0 or correct==2:
        return

    CARDS_by_id[card.id]=card
    CARDS_by_name[card.name.lower()]=card

    await Card.dump_cards(client.loop)
    await client.message_create(message.channel,'Card successfully created and saved')

async def showcard(client,message,content):
    if not 2<len(content)<101:
        return
    try:
        card=CARDS_by_name[content.lower()]
    except KeyError:
        return
    embed=Embed(color=CHESUTO_COLOR)
    embed.add_field('Name',card.name,inline=True)
    embed.add_field('Rarity',card.rarity.name,inline=True)
    embed.add_field('Description',card.description)
    await client.message_create(message.channel,embed=embed)
    
class CardRandomizer():
    __slots__=['array', 'elements', 'references']
    def __init__(self,cards,rarity_weights):
        sorted_by_rarity={}
        for card in cards:
            rarity=card.rarity
            try:
                elements=sorted_by_rarity[rarity]
            except KeyError:
                sorted_by_rarity[rarity]=elements=[]
            elements.append(card)
        
        #filter out useless cases
        for rarity,elements in sorted_by_rarity.items():
            if elements:
                continue
            try:
                del rarity_weights[rarity]
            except KeyError:
                pass

        for rarity,weight in rarity_weights.items():
            if weight:
                continue
            try:
                del sorted_by_rarity[rarity]
            except KeyError:
                pass

        total_weight={}
        total_weight_sum=0
        for rarity,elements in sorted_by_rarity.items():
            weight_sum=len(elements)*rarity_weights[rarity]
            total_weight_sum+=weight_sum
            total_weight[rarity]=weight_sum
        
        self.array=array=Array('f')
        self.elements=elements=[]
        self.references=references={}
        last=0.
        index=0
        for rarity in rarity_weights:
            self.array.append(last)
            last=last+(total_weight/total_weight[rarity])
            self.elements.append(sorted_by_rarity[rarity])
            references[rarity]=index
            index=index+1

    def poll(self):
        index=_relativeindex(self.array,random())
        elements=self.elements[index]
        index=(random()*elements.__len__()).__int__()
        return elements[index]

    def poll_from(self,rarity):
        index=self.references[rarity]
        elements=self.elements[index]
        index=(random()*elements.__len__()).__int__()
        return elements[index]

class ChesutoSystemShard():
    __slots__=['embed','emojis','waiter_message','waiter_reaction','_waiter_flag']
    def __init__(self,embed,emojis,waiter_message,waiter_reaction):
        self.embed=embed
        self.emojis=emojis
        self.waiter_message=waiter_message
        self.waiter_reaction=waiter_reaction
        self._waiter_flag=((waiter_message is not None)<<1)+(waiter_reaction is not None)

    async def just_init(self,parent):
        client=parent.client
        embed=self.embed
        try:
            message = await client.message_create(parent.channel,embed=embed)
        except DiscordException:
            return None

        emojis=self.emojis
        if emojis is not None:
            try:
                if type(emojis) is Emoji:
                    await client.reaction_add(message,emojis)
                else:
                    for emoji in emojis:
                        await client.reaction_add(message,emoji)
            except DiscordException:
                del ACTIVE_LOBBIES[parent.user.id]
                return None
        
        parent.embed=embed
        parent.emojis=emojis
        return message

    def just_wait(self,parent):
        return self._waiter_tasks[self._waiter_flag](self,parent)
        
    async def __call__(self,parent,embed=None):
        if embed is None:
            embed=self.embed

        client=parent.client
        message=parent.message
        
        if parent.emojis is not None:
            try:
                await client.reaction_clear(message)
            except DiscordException:
                del ACTIVE_LOBBIES[parent.user.id]
                return None
        
        try:
            await client.message_edit(message,embed=embed)
        except DiscordException:
            del ACTIVE_LOBBIES[parent.user.id]
            return None
        
        emojis=self.emojis
        if emojis is not None:
            try:
                if type(emojis) is Emoji:
                    await client.reaction_add(message,emojis)
                else:
                    for emoji in emojis:
                        await client.reaction_add(message,emoji)
            except DiscordException:
                del ACTIVE_LOBBIES[parent.user.id]
                return None

        parent.embed=embed
        parent.emojis=emojis
       
        return await self._waiter_tasks[self._waiter_flag](self,parent)
    
    async def _0b00(self,parent):
        while True:
            try:
                result = await parent.future
            except CancelledError:
                continue
            else:
                return result
            finally:
                parent.future.clear()

    async def _0b01(self,parent):
        waiter_reaction=MethodLike(self.waiter_reaction,parent)

        while True:
            client=parent.client
            message=parent.message
            client.events.reaction_add.append(waiter_reaction,message)
            try:
                result = await parent.future
            except CancelledError:
                continue
            else:
                return result
            finally:
                parent.future.clear()
                client.events.reaction_add.remove(waiter_reaction,message)
        
    async def _0b10(self,parent):
        waiter_message=MethodLike(self.waiter_message,parent)

        while True:
            client=parent.client
            channel=parent.channel
            client.events.message_create.append(waiter_message,channel)
            try:
                result = await parent.future
            except CancelledError:
                continue
            else:
                return result
            finally:
                parent.future.clear()
                client.events.message_create.remove(waiter_message,channel)

    
    async def _0b11(self,parent):
        waiter_message=MethodLike(self.waiter_message,parent)
        waiter_reaction=MethodLike(self.waiter_reaction,parent)

        while True:
            client=parent.client
            channel=parent.channel
            message=parent.message
            client.events.message_create.append(waiter_message,channel)
            client.events.reaction_add.append(waiter_reaction,message)
            try:
                result = await parent.future
            except CancelledError:
                continue
            else:
                return result
            finally:
                parent.future.clear()
                client.events.message_create.remove(waiter_message,channel)
                client.events.reaction_add.remove(waiter_reaction,message)
    
    _waiter_tasks=(_0b00,_0b01,_0b10,_0b11)
    del _0b00, _0b01, _0b10, _0b11

class MethodLike():
    __slots__=['func','parent']
    def __init__(self,func,parent):
        self.func=func
        self.parent=parent
    
    def __call__(self,*args):
        return self.func(self.parent,*args)

    def __eq__(self,other):
        return (self is other)

    def __ne__(self,other):
        return (self is not other)

        
ACTIVE_LOBBIES={}

EMOJI_1=BUILTIN_EMOJIS['one']
EMOJI_2=BUILTIN_EMOJIS['two']
EMOJI_3=BUILTIN_EMOJIS['three']
EMOJI_4=BUILTIN_EMOJIS['four']
EMOJIS_1_4=[EMOJI_1,EMOJI_2,EMOJI_3,EMOJI_4]
EMOJI_CHECK=BUILTIN_EMOJIS['white_check_mark']
EMOJI_X=BUILTIN_EMOJIS['x']
EMOJIS_CHECK_X=[EMOJI_CHECK,EMOJI_X]
EMOJI_TU=BUILTIN_EMOJIS['thumbup_skin_tone_2']
EMOJI_TD=BUILTIN_EMOJIS['thumbdown_skin_tone_2']
EMOJIS_T_X=[EMOJI_TU,EMOJI_TD,EMOJI_X]
    
async def chesuto_lobby(client,message,content):
    channel=message.channel
    if channel.guild is None: #guild only command
        return
    permissions=message.channel.cached_permissions_for(client)
    if not (permissions.can_add_reactions and permissions.can_use_external_emojis and permissions.can_manage_messages):
        await client.message_create(channel,embed=Embed(
            'Permissions denied',
            'I have not all permissions to start a lobby at this channel.',
            color=CHESUTO_COLOR,))
        return

    user=message.author

    try:
        lobby=ACTIVE_LOBBIES[user.id]
    except KeyError:
        await ChesutoWinSystem(client,channel,user)
    else:
        await lobby.switch_context(client,channel)
        
    
class ChesutoWinSystem(metaclass=asyncinit):
    __slots__=['client','channel','message','user','future','embed','emojis']
    async def __init__(self,client,channel,user):
        self.client=client
        self.channel=channel
        self.user=user
        
        message = await self.shard_menu.just_init(self)
        if message is None:
            return
        
        self.message=message
        self.future=Future(client.loop)
        Task(self.win_menu_initial(),client.loop)
        ACTIVE_LOBBIES[user.id]=self

    async def switch_context(self,client,channel):
        embed=self.embed
        try:
            message = await client.message_create(channel,embed=embed)
        except DiscordException:
            return

        emojis=self.emojis
        if emojis is not None:
            try:
                if type(emojis) is Emoji:
                    await client.reaction_add(message,emojis)
                else:
                    for emoji in emojis:
                        await client.reaction_add(message,emoji)
            except DiscordException:
                return

        self.client=client
        self.message=message
        self.channel=channel
        self.future.cancel()

    async def shard_menu_rw(self,emoji,user):
        if (user!=self.user) or (emoji not in EMOJIS_1_4):
            return
        self.future.set_result(emoji)
        
    shard_menu=ChesutoSystemShard(
        Embed(
            'You\'re in the lobby now, select one of the listed choices',
            '1. Wait in a room for battles\n'
            '2. Edit your current deck\n'
            '3. Open packs\n'
            '4. Cancel\n',
            color=CHESUTO_COLOR,
                ),
        EMOJIS_1_4,
        None,
        shard_menu_rw,
            )

    del shard_menu_rw
    
    async def win_menu_initial(self):
        result = await self.shard_menu.just_wait(self)
        if result is None:
            return
        
        if result is EMOJI_1:
            Task(self.win_room_1(),self.client.loop)
            return

        await self.client.message_create(self.channel,'nothing set to go to')
        del ACTIVE_LOBBIES[self.user.id]
        
    async def win_menu(self):
        result = await self.shard_menu(self)
        if result is None:
            return
        
        if result is EMOJI_1:
            Task(self.win_room_1(),self.client.loop)
            return

        await self.client.message_create(self.channel,'nothing set to go to')
        del ACTIVE_LOBBIES[self.user.id]

    async def shard_room_1_rw(self,emoji,user):
        if user.is_bot:
            return
        if (user!=self.user):
            if (emoji is EMOJI_CHECK):
                self.future.set_result(user)
            return
        if (emoji is EMOJI_X):
            self.future.set_result(emoji)

    shard_room_1=ChesutoSystemShard(
        None,
        EMOJIS_CHECK_X,
        None,
        shard_room_1_rw,
            )

    del shard_room_1_rw
    
    async def win_room_1(self):
        embed=Embed(f'{self.user:f}\'s room',
            f'Join with reacting with {EMOJI_CHECK:e}',
            color=CHESUTO_COLOR,)
        result = await self.shard_room_1(self,embed)
        if result is None:
            return

        if result is EMOJI_X:
            Task(self.win_menu(),self.client.loop)
            return

        Task(self.win_room_2(result),self.client.loop)

    async def shard_room_2_rw(self,emoji,user):
        if (user!=self.user) or (emoji not in EMOJIS_T_X):
            return
        self.future.set_result(emoji)
    
    shard_room_2=ChesutoSystemShard(
        None,
        EMOJIS_T_X,
        None,
        shard_room_2_rw,
            )

    del shard_room_2_rw

    async def win_room_2(self,user):
        embed=Embed(f'{self.user:f}\'s room',
            f'{user:f} joined your room, do you want to fight against this player?',
            color=CHESUTO_COLOR)
        result = await self.shard_room_2(self,embed)
        if result is None:
            return

        client=self.client
        
        if result is EMOJI_X:
            Task(self.win_menu(),client.loop)
            return

        if result is EMOJI_TD:
            Task(self.win_room_1(),client.loop)
            return
        
        channel = await client.channel_private_create(self.user)
        player1=ChesutoPlayer(self.user,channel)
        channel = await client.channel_private_create(user)
        player2=ChesutoPlayer(user,channel)
        ChesutoBackend(client,self.channel,player1,player2)
        del ACTIVE_LOBBIES[self.user.id]

        
from hata.client_core import KOKORO
KOKORO.create_task_threadsafe(Card.load_cards(KOKORO))
del KOKORO

del Color
        
