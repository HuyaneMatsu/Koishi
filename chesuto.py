# -*- coding: utf-8 -*-
import sys
import json
from hata.emoji import Emoji
from hata.futures import SyncLock
from hata.dereaddons_local import alchemy_incendiary

# Emojis are not used, but we will keep them for a time now

# Rook
#Emoji.precreate(604652042635706416,name='a0').as_emoji
#Emoji.precreate(604657343950487562,name='a1').as_emoji
#Emoji.precreate(604652042669129788,name='a2').as_emoji
#Emoji.precreate(604652042652483591,name='a3').as_emoji

# Knight
#Emoji.precreate(604652042350362625,name='a4').as_emoji
#Emoji.precreate(604652042413146113,name='a5').as_emoji
#Emoji.precreate(604652042853548042,name='a6').as_emoji
#Emoji.precreate(604652042740301835,name='a7').as_emoji

# Bishop
#Emoji.precreate(604652042694426634,name='a8').as_emoji,
#Emoji.precreate(604652042715398144,name='a9').as_emoji,
#Emoji.precreate(604652042253762571,name='aa').as_emoji,
#Emoji.precreate(604652042581180425,name='ab').as_emoji,

# Queen
#Emoji.precreate(604657915038793728,name='ac').as_emoji
#Emoji.precreate(604657914820558849,name='ad').as_emoji
#Emoji.precreate(604652042732175390,name='ae').as_emoji
#Emoji.precreate(604652042639638550,name='af').as_emoji

# King
#Emoji.precreate(604658587117027328,name='ag').as_emoji
#Emoji.precreate(604658587121221642,name='ah').as_emoji
#Emoji.precreate(604652042790895616,name='ai').as_emoji
#Emoji.precreate(604658586978746378,name='aj').as_emoji

# Pawn
#Emoji.precreate(604652042656677918,name='ak').as_emoji
#Emoji.precreate(604652042731913216,name='al').as_emoji
#Emoji.precreate(604652042702815313,name='am').as_emoji
#Emoji.precreate(604652042484711424,name='an').as_emoji


# Empty tiles
#Emoji.precreate(604652042639900672,name='ao').as_emoji
#Emoji.precreate(604652044246188065,name='ap').as_emoji

# Numbers
#Emoji.precreate(604698116427350016,name='aq').as_emoji
#Emoji.precreate(604698116444258469,name='ar').as_emoji
#Emoji.precreate(604698116431675406,name='as').as_emoji
#Emoji.precreate(604698116444258475,name='at').as_emoji
#Emoji.precreate(604698116226285589,name='au').as_emoji
#Emoji.precreate(604698116578476149,name='av').as_emoji
#Emoji.precreate(604698116448452674,name='aw').as_emoji
#Emoji.precreate(604698116494590202,name='ax').as_emoji

# Letters
#Emoji.precreate(604698116129816586,name='ay').as_emoji
#Emoji.precreate(604698116675076106,name='az').as_emoji
#Emoji.precreate(604698116482007194,name='aA').as_emoji
#Emoji.precreate(604698116435738625,name='aB').as_emoji
#Emoji.precreate(604698116163371009,name='aC').as_emoji
#Emoji.precreate(604698116490264586,name='aD').as_emoji
#Emoji.precreate(604698116548984832,name='aE').as_emoji
#Emoji.precreate(604698116540596252,name='aF').as_emoji

# Edge
#Emoji.precreate(604698116658167808,name='aG').as_emoji

class Rarity(object):
    INSTANCES = [NotImplemented] * 6
    BY_NAME   = {}
    __slots__=('index', 'name',)
    
    def __init__(self,index,name):
        self.index=index
        self.name=name
        
        self.INSTANCES[index]=self
        self.BY_NAME[name]=self

    def __str__(self):
        return self.name

    def __repr__(self):
        return f'{self.__class__.__name__}(name={self.name}, index={self.index})'

    def __gt__(self,other):
        if type(self) is not type(other):
            return NotImplemented
        
        return self.index>other.index
    
    def __ge__(self,other):
        if type(self) is not type(other):
            return NotImplemented
        
        return self.index>=other.index
        
    def __eq__(self,other):
        if type(self) is not type(other):
            return NotImplemented
        
        return self.index==other.index
    
    def __ne__(self,other):
        if type(self) is not type(other):
            return NotImplemented
        
        return self.index!=other.index
        
    def __le__(self,other):
        if type(self) is not type(other):
            return NotImplemented
        
        return self.index<=other.index
        
    def __lt__(self,other):
        if type(self) is not type(other):
            return NotImplemented
        
        return self.index<other.index
    
    def __hash__(self):
        return self.index
    
    token       = NotImplemented
    common      = NotImplemented
    uncommon    = NotImplemented
    rare        = NotImplemented
    legendary   = NotImplemented
    mythic      = NotImplemented

Rarity.token    = Rarity(0,'Token',)
Rarity.common   = Rarity(1,'Common')
Rarity.uncommon = Rarity(2,'Uncommon')
Rarity.rare     = Rarity(3,'Rare')
Rarity.legendary= Rarity(4,'Legendary')
Rarity.mythic   = Rarity(5,'Mythic')

CARDS_BY_ID={}
CARDS_BY_NAME={}

class Card(object):
    __slots__=('description', 'id', 'name', 'rarity')
    def __init__(self,description,id_,name,rarity):
        self.id         = id_
        self.name       = name
        self.description= description
        self.rarity     = rarity
        CARDS_BY_ID[id_]= self
        CARDS_BY_NAME[name.lower()]=self

    def __hash__(self):
        return self.id

    FILENAME='CHESUTO.json'
    FILELOCK=SyncLock()
    
    @classmethod
    def update(cls,description,id_,name,rarity):
        lower_name=name.lower()
        try:
            card=CARDS_BY_NAME[lower_name]
        except KeyError:
            Card(True,description,id_,name,rarity)
            return True
        
        card.description=description
        card.name=name
        card.rarity=rarity
        return False
    
    @classmethod
    async def dump_cards(cls,loop):
        card_datas=[]
        for card in CARDS_BY_ID.values():
            card_data={}
            card_data['description']= card.description
            card_data['id']         = card.id
            card_data['name']       = card.name
            card_data['rarity']     = card.rarity.index
            card_datas.append(card_data)
        
        await loop.run_in_executor(alchemy_incendiary(cls._dump_cards,(card_datas,),),)
            
    @classmethod
    def _dump_cards(cls,card_datas):
        with cls.FILELOCK:
            with open(cls.FILENAME,'w') as file:
                json.dump(card_datas,file,indent=4)

    @classmethod
    def load_cards(cls):

        try:
            with open(cls.FILENAME,'r') as file:
                cards_data=json.load(file)
        except FileNotFoundError:
            exception='file not found'
        except OSError as err:
            exception=err.strerror
        else:
            if type(cards_data) is list:
                exception=None
            else:
                exception=f'Expected type \'list\' for \'cards_data\', got \'{cards_data.__class__.__name__}\''

        if exception is not None:
            sys.stderr.write(f'Exception at loading cards:\n{exception}\n')
            return
            
        for card_data in cards_data:
            while True:
                if type(card_data) is not dict:
                    exception=f'Expcted type \'dict\' for \'card_data\', got \'{card_data.__class__.__name__}\''
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
                    id_=card_data['id']
                except KeyError:
                    exception='No \'id\' key'
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
                    rarity=Rarity.INSTANCES[rarity]
                except IndexError:
                    exception=f'No such \'rarity\' index: {rarity}'
                    break
                
                break

            if exception is None:
                Card(description,id_,name,rarity)
                continue
            
            sys.stderr.write(f'Exception at loading cards:\n{exception}\n At data part:\n{card_data}\n')
            exception=None
            continue

Card.load_cards()
