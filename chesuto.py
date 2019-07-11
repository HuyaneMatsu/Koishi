
#each added move is from 3 elements:
# x coordinate
# y coordinate
# what u can do there
#   0b000000 -> 6 digit yet
#   0b000001 <- can move
#   0b000010 <- could move
#   0b000100 <- can hit
#   0b001000 <- could hit
#   0b010000 <- can special
#   0b100000 <- could special

class Puppet_meta(object):
    __slots__=['generate_moves', 'name']
    def __init__(self,name):
        self.name=name
        setattr(type(self),name,self)

    def __call__(self,func):
        self.generate_moves=func

    #just to mention them
    rook    = None
    knight  = None
    bishop  = None
    queen   = None
    king    = None
    pawn    = None

@Puppet_meta('rook')
def rook_moves(self,field):
    position=self.position
    y,x=divmod(position,8)
    result=[]

    for dim_i,v_diff,pos_diff,v_limit in (
            (0,-1,-1,0),
            (1,-1,-8,0),
            (0,+1,+1,7),
            (1,+1,+8,7),
                ):

        local_pos=position
        if dim_1:
            local_v=y
        else:
            local_v=x
        while True:
            if local_v==v_limit:
                break
            local_v+=v_diff
            local_pos+=pos_diff
            if other is None:
                if dim_i:
                    result.append((x,local_v,0b001011),) #free
                else:
                    result.append((local_x,y,0b001011),) #free
                continue
            if self.side==other.side:
                if dim_i:
                    result.append((x,local_v,0b001010),) #could hit
                else:
                    result.append((local_x,y,0b001010),) #could hit
            else:
                if dim_i:
                    result.append((x,local_v,0b001110),) #hit
                else:
                    result.append((local_x,y,0b001110),) #hit
                other.killers.append(self)

            break

    #TODO: add castling
    return result

@Puppet_meta('knight')
def knight_move(self,field):
    position=self.position
    y,x=divmod(position,8)
    result=[]

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
        
        other=field[position-pos_diff]
        if other is None:
            result.append((local_x,local_y,0b001011),) #free
            continue

        if self.side==other.side:
            result.append((local_x,local_y,0b001010),) #could hit
        else:
            result.append((local_x,local_y,0b001110),) #hit
            other.killers.append(self)

    return result

@Puppet_meta('bishop')
def bishop_move(self,field):
    position=self.position
    y,x=divmod(position,8)
    result=[]

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
                result.append((local_x,local_y,0b001011),) #free
                continue

            if self.side==other.side:
                result.append((local_x,local_y,0b001010),) #could hit
            else:
                result.append((local_x,local_y,0b001110),) #hit
                other.killers.append(self)
            
            break

    return result

@Puppet_meta('queen')
def queen_move(self,field):
    position=self.position
    y,x=divmod(position,8)
    result=[]

    for dim_i,v_diff,pos_diff,v_limit in (
            (0,-1,-1,0),
            (1,-1,-8,0),
            (0,+1,+1,7),
            (1,+1,+8,7),
                ):

        local_pos=position
        if dim_1:
            local_v=y
        else:
            local_v=x
        while True:
            if local_v==v_limit:
                break
            local_v+=v_diff
            local_pos+=pos_diff
            if other is None:
                if dim_i:
                    result.append((x,local_v,0b001011),) #free
                else:
                    result.append((local_x,y,0b001011),) #free
                continue
            if self.side==other.side:
                if dim_i:
                    result.append((x,local_v,0b001010),) #could hit
                else:
                    result.append((local_x,y,0b001010),) #could hit
            else:
                if dim_i:
                    result.append((x,local_v,0b001110),) #hit
                else:
                    result.append((local_x,y,0b001110),) #hit
                other.killers.append(self)
            break

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
                result.append((local_x,local_y,0b001011),) #free
                continue

            if self.side==other.side:
                result.append((local_x,local_y,0b001010),) #could hit
            else:
                result.append((local_x,local_y,0b001110),) #hit
                other.killers.append(self)
            
            break

    return result

@Puppet_meta('king')
def king_move(self,field):
    position=self.position
    y,x=divmod(position,8)
    result=[]

    for x_diff,y_diff,pos_diff,x_limit,y_limit in (
            (-1,-1,-9,0,0),
            ( 0,-1,-8,8,0),
            (+1,-1,-7,7,0),
            (+1, 0,+1,7,8),
            (+1,+1,+9,7,7),
            ( 0,+1,+8,8,7)
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
            result.append((local_x,local_y,0b001011),) #free
            continue

        if self.side==other.side:
            result.append((local_x,local_y,0b001010),) #could hit
        else:
            result.append((local_x,local_y,0b001110),) #hit
            other.killers.append(self)
        
        continue

    #TODO : add castling
    #TODO : calculate unsteppable tiles
    return result


@Puppet_meta('pawn')
def pawn_moves(self,field):
    position=self.position
    y,x=divmod(position,8)
    result=[]

    if self.side:
        if field[position+8] is None:
            if y==1:
                result.append((x,0,0b110011),) #evolve
            else:
                result.append((x,y-1,0b000011),) #general forward
                if not self.moved and field[position-16] is None:
                    result.append((x,y-2,0b000011),) #double on default position

        if x>0:
            other=field[position+7]
            if other is None or self.side==other.side:
                result.append((x-1,y-1,0b001000),) #could hit
            else:
                result.append((x-1,y-1,0b001100),) #hit
                other.killers.append(self)
        
        if x<7:
            other=field[position+9]
            if other is None or self.side==other.side:
                result.append((x+1,y-1,0b001000),) #could hit
            else:
                result.append((x+1,y-1,0b001100),) #hit
                other.killers.append(self)
                
    else:
        if field[position-8] is None:
            if y==6:
                result.append((x,7,0b110011),) #evolve
            else:
                result.append((x,y-1,0b000011),) #general forward
                if not self.moved and field[position-16] is None:
                    result.append((x,y+2,0b000011),) #double on default position

        if x>0:
            other=field[position-9]
            if other is None or self.side==other.side:
                result.append((x-1,y-1,0b001000),) #could hit
            else:
                result.append((x-1,y-1,0b001100),) #hit
                other.killers.append(self)
        
        if x<7:
            other=field[position-7]
            if other is None or self.side==other.side:
                result.append((x+1,y-1,0b001000),) #could hit
            else:
                result.append((x+1,y-1,0b001100),) #hit
                other.killers.append(self)
    
    return result

def Puppet(object):
    __slots__=['effects', 'meta', 'moved', 'position', 'side']
    def __init__(self,meta,position,side):
        self.meta       = meta
        self.position   = position
        self.side       = side
        self.effects    = []
        self.moved      = False #needs for special checks
        self.moves      = []
        self.killers    = []

    def regenerate(self,field):
        for effect in self.effects:
            effect.apply(self)

        self.moves.clear()
        self.killers.clear()
        
        self.meta.generate_moves(self,field)


class chesuto_backend(object):
    __slots__=['field','players']
    def __init__(self,player_0,player_1):
        self.players=(player_0,player_1)
        
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
        
        def check(self,player,x,y):
            position=x+(y<<3)
            puppet=self.field[position]
            if puppet is not None:
                return puppet.moves,puppet.killers

            moves=[]
            killers=[]
            
            player2=self.players[not player.side]
            
            for puppet_ in player.puppets:
                for move in puppet.moves:
                    if move[2]&0b000001:
                        moves.append((x,y,0b000001),)
            for puppet_ in player2.puppets:
                for move in puppet.moves:
                    if move[2]&0b001000:
                        killers.append(puppet)

            return moves,killers   
            

    
class chesuto_player(object):
    __slots__=['backend', 'channel', 'puppets', 'side', 'user']
    def __init__(self,user,channel,backend,side):
        self.user=user
        self.channel=channel
        self.side=side
        self.backend=backend
        if side:
            self.puppets=backend.field[:16]
        else:
            self.puppets=backend.field[48:]

            


