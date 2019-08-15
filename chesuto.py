# -*- coding: utf-8 -*-
import sys, os
sys.path.append(os.path.abspath('..'))

from hata.emoji import Emoji
from hata.futures import Task
from hata.events import cooldown
from hata.events_compiler import content_parser
from hata.exceptions import DiscordException

from tools import cooldown_handler

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
        setattr(type(self),name,self)

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

class chesuto_backend(object):
    __slots__=['client', 'field','players']
    def __init__(self,client,player_0,player_1):
        self.client=client()

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
        self.update_puppets()
        Task(self.run(),client.loop)

    def run(self):
        pass

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
            
class chesuto_player(object):
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

WAITERS={}

class chesuto_waiter():
    __slots__=['channel', 'client', 'user', 'timeout_handle', 'waiter']
    def __init__(self,client,channel,user):
        self.client=client
        self.channel=channel
        self.user=user
        self.waiter=client.loop.call_later(300.,self.at_timeout)

    def at_timeout(self):
        channel=self.channel
        del WAITERS[self.user.id]
        client=self.client
        Task(client.message_create(channel,f'{self.user:m} timeout'),client.loop)

    def reset_waiter(self,channel):
        self.channel=channel
        self.waiter.cancel()
        self.waiter=self.client.loop.call_later(300.,self.at_timeout)

@cooldown(60.,'user',handler=cooldown_handler())
async def chesuto_wait(client,message,content):
    channel=message.channel
    user=message.author
    try:
        game_waiter=WAITERS[user.id]
    except KeyError:
        WAITERS[user.id]=chesuto_waiter(client,channel,user)
        return

    game_waiter.reset_waiter(channel)
    await client.message_create(channel,'Your waiter is reseted')
    return

@cooldown(15.,'user',handler=cooldown_handler())
@content_parser('user')
async def chesuto_fight(client,message,user):
    if message.author is user:
        return
    try:
        game_waiter=WAITERS[user.id]
    except KeyError:
        pass
    else:
        if game_waiter.channel is message.channel:
            game_waiter.waiter.cancel()
            channel = await client.channel_privtae_create(user)
            player1=chesuto_player(user,channel)
            channel = await client.channel_private_create(message.author)
            player2=chesuto_player(message.author,channel)
            chesuto_backend(client,player1,player2)
            return
    await client.message_create(message.channel,f'{user:f} is not waiiting, or nto at this channel.')