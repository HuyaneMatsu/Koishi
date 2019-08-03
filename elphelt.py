from hata.parsers import eventlist
from hata.events import cooldown
from tools import cooldown_handler
from random import random
import re
from hata.others import filter_content
from tools import smart_join
from hata.emoji import BUILTIN_EMOJIS

commands=eventlist()

@commands
@cooldown(30.,'user',handler=cooldown_handler())
async def ping(client,message,content):
    await client.message_create(message.channel,f'{int(client.gateway.kokoro.latency*1000.)} ms')

DECK_LINE_RP=re.compile('(\d+) *(.*?) *\n?')

USER_CARDS={}

class Card_cont(dict):
    __slots__=['_total_ln']
    
    def __init__(self):
        self._total_ln=0
    
    def __len__(self):
        return self._total_ln
    
    def append(self,name,times):
        if times:
            self[name]=self.get(name,0)+times
            self._total_ln+=times
            
    def append_1(self,name):
        self[name]=self.get(name,0)+1
        self._total_ln+=1
        
    def pop_random(self):
        index=int(random()*self._total_ln)
        for name,times in self.items():
            index-=times
            if index<1:
                times-=1
                if times:
                    self[name]=times
                else:
                    del self[name]
                self._total_ln-=1
                return name
    
    def pop_1(self,name):
        amount=self.get(name,0)
        if amount==0:
            return False
        self._total_ln-=1
        if amount==1:
            del self[name]
            return True
        self[name]+=amount
        return True
        

class DaH(object): #deck and hand
    __slots__=['deck','hand']
    def __init__(self,deck):
        self.deck=deck
        self.hand=Card_cont()
    
    def draw(self):
        card=self.deck.pop_random()
        if card is not None:
            self.hand.append_1(card)
        return card

    def render_hand(self):
        cont=self.hand
        if cont:
            return '\n'.join([f'{times} {name}' for name,times in self.hand.items()])
        else:
            return '*empty*'
    
@commands
async def inputdeck(client,message,content):
    result=Card_cont()
    lines=message.content.splitlines()
    for index in range(1,len(lines)):
        line=lines[index]
        parsed=DECK_LINE_RP.fullmatch(line)
        if parsed is None:
            await client.message_create(message.channel,f'Could not parse line {index} :\n\'{line}\'')
            return
        times,name=parsed.groups()
        result.append(name,int(times))
    
    USER_CARDS[message.author.id]=DaH(result)
    
    await client.message_create(message.channel,'Deck created!')

@commands
async def addcard(client,message,content):
    user_cards=USER_CARDS.get(message.author.id)
    if user_cards is None:
        await client.message_create(message.channel,'You do not have a deck added.')
        return
    if not content:
        await client.message_create(message.channel,'Write what you want to add after the command, no linebreaks either.')
        return
    user_cards.deck.append_1(content)
    await client.message_create(message.channel,BUILTIN_EMOJIS['ok_hand_skin_tone_1'].as_emoji)
    
@commands
async def draw(client,message,content):
    user_cards=USER_CARDS.get(message.author.id)
    if user_cards is None:
        await client.message_create(message.channel,'You do not have a deck added.')
        return
    content=filter_content(content)
    if content:
        try:
            amount=int(content[0])
        except ValueError:
            amount=1
        else:
            if amount<1:
                await client.message_create(message.channel,'questionable amount')
                return
    else:
        amount=1
    
    result=['You draw:']

    for index in range(amount):
        card=user_cards.draw()
        if card is None:
            if index:
                result[0]=f'You tried to draw {amount} of cards, but there was only {index} at your deck left\nYou draw:'
            else:
                result[0]='You do not have anymore cards at your deck :c'
            break
        result.append(card)

    await client.message_create(message.channel,smart_join(result))

@commands
async def showhand(client,message,content):
    user_cards=USER_CARDS.get(message.author.id)
    if user_cards is None:
        text='You do not have a deck added.'
    else:
        text=user_cards.render_hand()
    
    await client.message_create(message.channel,text)

@commands
async def cancelsimulation(client,message,content):
    USER_CARDS.pop(message.author.id,None)
    await client.message_create(message.channel,'o7')

@commands
async def usecard(client,message,content):
    user_cards=USER_CARDS.get(message.author.id)
    if user_cards is None:
        await client.message_create(message.channel,'You do not have a deck added.')
        return
    
    content=content.strip()
    drawed=user_cards.hand.pop_1(content)
    if drawed:
        text=f'You successfully used up `{content}`.'
    else:
        text=f'You have no `{content}` at your hand'
    await client.message_create(message.channel,text)
    
del re
