# -*- coding: utf-8 -*-
from hata.events_compiler import ContentParser
from hata.futures import Future,CancelledError,InvalidStateError,Task
from random import randint
from hata.dereaddons_local import any_to_any,asyncinit
from time import monotonic
from hata.exceptions import DiscordException
from hata.emoji import BUILTIN_EMOJIS
from hata.events import waitfor_wrapper,multievent
from hata.color import Color
from hata.embed import Embed
from PIL import Image as PIL
from PIL.ImageDraw import ImageDraw
from PIL.ImageFont import truetype
import os
from hata.ios import ReuBytesIO
from help_handler import HELP

class ms_cache(object):
    __slots__=['parent', 'obj']

    def get_doc(self):
        return self.parent.klass.__doc__
    def set_doc(self,value):
        self.parent.klass.__doc__=value
    __doc__=property(get_doc,set_doc)
    del get_doc,set_doc

    def __init__(self,parent,obj):
        self.parent=parent
        self.obj=obj
        
    def __call__(self,*args,**kwargs):
        return self.parent.klass(self.obj,*args,**kwargs)
    
class methodsimulator(object):
    __slots__=['klass']
    
    def get_doc(self):
        return self.klass.__doc__
    def set_doc(self,value):
        self.klass.__doc__==value
    __doc__=property(get_doc,set_doc)
    del get_doc,set_doc
   
    def __init__(self,klass):
        self.klass=klass
        
    def __get__(self,obj,objtype=None):
        if obj is None:
            return self.klass
        return ms_cache(self,obj)

    def __set__(self,obj,value):
        raise AttributeError('can\'t set attribute')
    def __delete__(self,obj):
        raise AttributeError('can\'t delete attribute')

PIL.Image.draw=methodsimulator(ImageDraw)
PIL.font=truetype
del ImageDraw,truetype

FONT=PIL.font(os.path.join('library','Kozuka.otf'),90)
FONT_COLOR=(162,61,229)

del os

def draw(buffer,text):
    image=PIL.new('RGBA',FONT.getsize(text),(0,0,0,0))
    image.draw().text((0,0),text,fill=FONT_COLOR,font=FONT)
    image.save(buffer,'png')
    buffer.seek(0)
    return buffer

ACTIVE_GAMES={}
CIRCLE_TIME=60.
COLOR=Color.from_tuple(FONT_COLOR)

_pairsK=('k','g','s','z','c','t','d','f','h','b','p','n','m','y','r','w','j')
_pairsKx={'k':('k','g'),'g':('k','g'),'s':('s','z','c'),'z':('s','z','c'),'c':('s','z','c'),'t':('t','d'),'d':('t','d'),'f':('f','h','b','p'),'h':('f','h','b','p'),'b':('f','h','b','p'),'p':('f','h','b','p')}
_pairsD=('a','i','e','o','u')
_hiragana=[('あ','a'),('い','i'),('う','u'),('え','e'),('お','o'),('か','ka'),('き','ki'),('く','ku'),('け','ke'),('こ','ko'),('が','ga'),('ぎ','gi'),('ぐ','gu'),('げ','ge'),('ご','go'),('さ','sa'),('し','shi'),('す','su'),('せ','se'),('そ','so'),('ざ','za'),('じ','ji'),('ず','zu'),('ぜ','ze'),('ぞ','zo'),('た','ta'),('ち','chi'),('つ','tsu'),('て','te'),('と','to'),('だ','da'),('ぢ','ji'),('づ','zu'),('で','de'),('ど','do'),('な','na'),('に','ni'),('ぬ','nu'),('ね','ne'),('の','no'),('は','ha'),('ひ','hi'),('ふ','fu'),('へ','he'),('ほ','ho'),('ば','ba'),('び','bi'),('ぶ','bu'),('べ','be'),('ぼ','bo'),('ぱ','pa'),('ぴ','pi'),('ぷ','pu'),('ぺ','pe'),('ぽ','po'),('ま','ma'),('み','mi'),('む','mu'),('め','me'),('も','mo'),('ら','ra'),('り','ri'),('る','ru'),('れ','re'),('ろ','ro'),('わ','wa'),('ゐ','wi'),('ゔ','vu'),('ゑ','we'),('を','wo'),('や','ya'),('ゆ','yu'),('よ','yo'),('ん','n'),('きゃ','kya'),('きゅ','kyu'),('きょ','kyo'),('ぎゃ','gya'),('ぎゅ','gyu'),('ぎょ','gyo'),('しゃ','sha'),('しゅ','shu'),('しょ','sho'),('じゃ','ja'),('じゅ','ju'),('じょ','jo'),('ちゃ','cha'),('ちゅ','chu'),('ちょ','cho'),('ぢゃ','ja'),('ぢゅ','ju'),('ぢょ','jo'),('にゃ','nya'),('にゅ','nyu'),('にょ','nyo'),('ひゃ','hya'),('ひゅ','hyu'),('ひょ','hyo'),('びゃ','bya'),('びゅ','byu'),('びょ','byo'),('ぴゃ','pya'),('ぴゅ','pyu'),('ぴょ','pyo'),('みゃ','mya'),('みゅ','myu'),('みょ','myo'),('りゃ','rya'),('りゅ','ryu'),('りょ','ryo')]
_katakana=[('ア','a'),('イ','i'),('ウ','u'),('エ','e'),('オ','o'),('カ','ka'),('キ','ki'),('ク','ku'),('ケ','ke'),('コ','ko'),('ガ','ga'),('ギ','gi'),('グ','gu'),('ゲ','ge'),('ゴ','go'),('サ','sa'),('シ','shi'),('ス','su'),('セ','se'),('ソ','so'),('ザ','za'),('ジ','ji'),('ズ','zu'),('ゼ','ze'),('ゾ','zo'),('タ','ta'),('チ','chi'),('ツ','tsu'),('テ','te'),('ト','to'),('ダ','da'),('ヂ','ji'),('ヅ','zu'),('デ','de'),('ド','do'),('ナ','na'),('ニ','ni'),('ヌ','nu'),('ネ','ne'),('ノ','no'),('ハ','ha'),('ヒ','hi'),('フ','fu'),('ヘ','he'),('ホ','ho'),('バ','ba'),('ビ','bi'),('ブ','bu'),('ベ','be'),('ボ','bo'),('パ','pa'),('ピ','pi'),('プ','pu'),('ペ','pe'),('ポ','po'),('マ','ma'),('ミ','mi'),('ム','mu'),('メ','me'),('モ','mo'),('ラ','ra'),('リ','ri'),('ル','ru'),('レ','re'),('ロ','ro'),('ワ','wa'),('ヸ','wi'),('ヴ','vu'),('ヹ','we'),('ヲ','wo'),('ヤ','ya'),('ュ','yu'),('ョ','yo'),('ン','n'),('キャ','kya'),('キュ','kyu'),('キョ','kyo'),('ギャ','gya'),('ギュ','gyu'),('ギョ','gyo'),('シャ','sha'),('シュ','shu'),('ショ','sho'),('ジャ','ja'),('ジュ','ju'),('ジョ','jo'),('チャ','cha'),('チュ','chu'),('チョ','cho'),('ヂャ','ja'),('ヂュ','ju'),('ヂョ','jo'),('ニャ','nya'),('ニュ','nyu'),('ニョ','nyo'),('ヒャ','hya'),('ヒュ','hyu'),('ヒョ','hyo'),('ビャ','bya'),('ビュ','byu'),('ビョ','byo'),('ピャ','pya'),('ピュ','pyu'),('ピョ','pyo'),('ミャ','mya'),('ミュ','myu'),('ミョ','myo'),('リャ','rya'),('リュ','ryu'),('リョ','ryo')]

MAPS={'hiragana':_hiragana,'katakana':_katakana}

def render_showcase(name,map_):
    result=[]
    element_index=0
    element_limit=len(map_)
    
    page_index=1
    page_limit=(element_limit+29)//30

    field_text=[]
    
    while True:
        if page_index>page_limit:
            break
        embed=Embed(name.capitalize(),'',COLOR)
        embed.add_footer(f'page {page_index} / {page_limit}')
        
        for _ in range(((element_limit%30)+9)//10 if page_index==page_limit else 3):
            field_index_limit=element_index+10
            if field_index_limit>element_limit:
                field_index_limit=element_limit
            
            while element_index<field_index_limit:
                element=map_[element_index]
                element_index+=1
                field_text.append(f'{element_index}.: **{element[0]} - {element[1]}**')

            embed.add_field(f'{element_index-9} - {element_index}','\n'.join(field_text),inline=True)
            field_text.clear()
            
        result.append(embed)
        page_index+=1

    return result

MAP_showcases={name:render_showcase(name,map_) for name,map_ in MAPS.items()}

class history_element():
    __slots__=['answer', 'answers', 'options', 'question']

class kanako_game():
    __slots__=['amount', 'answers', 'client', 'history', 'map', 'map_name',
        'options', 'possibilities', 'romajis', 'running', 'channel', 'users',
        'waiter']
    def __init__(self,client,channel,user,map_name,amount,possibilities):
        self.client=client
        self.channel=channel
        self.users=[user]

        self.map_name=map_name
        self.amount=amount
        self.possibilities=possibilities
        
        self.running=False
        self.waiter=Future(client.loop)

        Task(self.start_waiting(),client.loop)
        
    async def start_waiting(self):
    
        try:
            await self.waiter.sleep(300.)
        except CancelledError:
            pass
        except InterruptedError:
            return self.cancel()
        else:
            return self.cancel()

        full_map=MAPS[self.map_name].copy()
        limit=len(full_map)-1
        
        self.map=[full_map.pop(randint(0,limit)) for limit in range(limit,limit-self.amount,-1)]
        if self.possibilities:
            self.romajis={element[1] for element in self.map}
        else:
            self.options=None
        
        self.history=[]
        self.answers={}
        self.running=True
        self.client.events.message_create.append(self,self.channel)
        
        Task(self.run(),self.client.loop)

    @property
    def info(self):
        return Embed(
            'Game information:',
            f'MAP : {self.map_name}\n'
            f'Question amount : {self.amount}\n'
            f'possibilities : {self.possibilities}\n'
            f'state : {("ready to start","running")[self.running]}',
            COLOR)
    
    def generate_options(self,answer):
        result=[answer]
        target=answer
        ignore=[element.answer for element in self.history[-4:]]
        ignore.append(answer)
        chances={romaji:randint(0,2) for romaji in self.romajis if romaji not in ignore}
        del ignore

        counter=1
        while True:
            ln=len(target)
            if ln==3 or 'j' in target:
                for key in chances:
                    if len(key)==3 or 'j' in target:
                        chances[key]+=2
            else:
                for key in chances:
                    if len(key) in (1,2) and 'j' not in target:
                        chances[key]+=1
                
            if target!='n':
                for charD in target:
                    if charD in _pairsD:
                        break

                for charK in target:
                    if charK in _pairsK:
                        break

                chars=_pairsKx.get(key,None)
                
                if chars is None:
                    for key in chances:
                        if len(key)!=ln:
                            continue
                        if charD in key:
                            chances[key]+=1
                        if charK in key:
                            chances[key]+=1
                else:
                    for key in chances:
                        if len(key)!=ln:
                            continue
                        if charD in key:
                            chances[key]+=1
                        if charK in key:
                            chances[key]+=1
                        if any_to_any(chars,key):
                            chances[key]+=1                           

            goods=[]
            maximal=1
            for key,value in chances.items():
                if value<maximal:
                    continue
                if value>maximal:
                    goods.clear()
                    maximal=value
                goods.append(key)
            
            target=goods[randint(0,len(goods)-1)]
            result.append(target)

            counter+=1
            if counter==self.possibilities:
                break
            
            del chances[target]
            
            for key in chances:
                chances[key]=randint(0,2)
            
        return [result.pop(randint(0,limit)) for limit in range(self.possibilities-1,-1,-1)]
            
    async def run(self):
        client=self.client
        channel=self.channel
        answers=self.answers
        buffer=ReuBytesIO()
        embed=Embed(color=COLOR)
        embed.add_image('attachment://guessme.png')
        embed.add_footer('')
        time_till_notify=CIRCLE_TIME-10
        
        for index,(question,answer) in enumerate(self.map,1):
            embed.footer.text=f'{index} / {len(self.map)}'
            if self.possibilities:
                self.options=self.generate_options(answer)
                embed.description='\n'.join([f'**{index}.: {value}**' for index,value in enumerate(self.options,1)])

            try:
                await client.message_create(channel,embed=embed,file=('guessme.png',draw(buffer,question)))
            except DiscordException:
                return self.cancel()
            
            circle_start=monotonic()
            self.waiter.clear()
            try:
                await self.waiter.sleep(time_till_notify)
                Task(self.send_or_except(
                    Embed('Hurry! Only 10 seconds left!',
                        '\n'.join([user.full_name for user in self.users if user.id not in answers]),
                        COLOR)),client.loop)
                self.waiter.clear()
                await self.waiter.sleep(10.)
                self.calculate_leavers()
            except CancelledError:
                pass
            except InterruptedError as err:
                return self.cancel()

            element=history_element()
            element.question= question
            element.answer  = answer
            element.options = self.options
            element.answers = [(value[0],value[1]-circle_start) for value in (answers[user.id] for user in self.users)]
            self.history.append(element)

            answers.clear()

            embed.title=f'Last answer: {answer}'

        await self.send_or_except(Embed(embed.title,'',COLOR))
            
        del ACTIVE_GAMES[channel.id]
        client.events.message_create.remove(self,self.channel)
        self.running=False

        await game_statistics(self)
    
    async def __call__(self,message):
        if message.author not in self.users or self.waiter.done() or message.author.id in self.answers or len(message.content)>4:
            return
        
        content=message.content.strip().lower()
        if self.possibilities:
            if content not in self.options:
                try:
                    index=int(content)
                except ValueError:
                    return
                else:
                    if index<1 or index>self.possibilities:
                        return
                    index-=1
                    content=self.options[index]
            
        self.answers[message.author.id]=(content,monotonic())
                                       
        if len(self.answers)==len(self.users):
            self.waiter.cancel_handles()
            self.waiter.cancel()
            
        try:
            await self.client.message_delete(message)
        except DiscordException:
            pass

    async def send_or_except(self,embed):
        try:
            await self.client.message_create(self.channel,embed=embed)
        except DiscordException:
            self.cacncel()
        
    def calculate_leavers(self):
        if self.answers:
            for user in self.users:
                if user.id not in self.answers:
                    self.remove(user)
            return
        raise InterruptedError
        
    def append(self,user):
        while True:
            if self.running:
                message='There is active game running, you cannot do that.'
                break
            if user in self.users:
                message='You are already at the game'
                break
            
            message='You succesfully joined to the current game.'
            self.users.append(user)
            
            if len(self.users)==10:
                message+=f'\n The game is full, starting.'
                self.waiter.cancel()
                
            break
        Task(self.client.message_create(self.channel,embed=Embed('',message,COLOR)),self.client.loop)
        
    def remove(self,user):
        while True:
            try:
                index=self.users.index(user)
            except ValueError:
                message='You are not part of the game.'
                break
            
            if len(self.users)==1:
                try:
                    self.waiter.set_exception(InterruptedError)
                except InvalidStateError:
                      self.waiter.add_done_callback(lambda future:setattr(future,'_exception',InterruptedError))
                return

            message=f'{user:f} left from the game.'
        
            if self.running:
                del self.users[index]
                for element in self.history:
                    del element.answers[index]
                if not self.answers.pop(user.id,'') and len(self.answers)==len(self.users)-1:
                    try:
                        self.future.set_result(None)
                    except InvalidStateError:
                        pass
            break
        Task(self.client.message_create(self.channel,embed=Embed('',message,COLOR)),self.client.loop)

    def cancel(self):
        client=self.client
        del ACTIVE_GAMES[self.channel.id]
        if self.running:
            client.events.message_create.remove(self,self.channel)
            self.running=False
        Task(client.message_create(self.channel,embed=Embed('','Game cancelled',COLOR)),client.loop)

class game_statistics(metaclass=asyncinit):
    __slots__=['cache', 'source']
    def __len__(self):
        return self.cache.__len__()
    def __init__(self,source):
        self.source=source
        self.cache=[None for _ in range((self.source.history.__len__()+9)//10+1)]
        self.createpage0()
        #we return a coro, so it is valid ^.^
        return embedination(source.client,source.channel,self)

    def createpage0(self):
        user_count  = len(self.source.users)
        win_counts  = [0 for _ in range(user_count)]
        lose_counts = win_counts.copy()
        win_firsts  = win_counts.copy()
        lose_firsts = win_counts.copy()
        win_times   = [[] for _ in range(user_count)]
        lose_times  = [[] for _ in range(user_count)]
    
        for element in self.source.history:
            answer=element.answer
            answers=element.answers
            first_time=CIRCLE_TIME
            first_index=0
            first_won=True
            for index in range(user_count):
                value,time=answers[index]
                if value==answer:
                    win_counts[index]+=1
                    win_times[index].append(time)
                    if time<first_time:
                        first_time=time
                        first_index=index
                        first_won=True
                else:
                    lose_counts[index]+=1
                    lose_times[index].append(time)
                    if time<first_time:
                        first_time=time
                        first_index=index
                        first_won=False
                        
            if first_time!=CIRCLE_TIME:
                if first_won:
                    win_firsts[first_index]+=1
                else:
                    lose_firsts[first_index]+=1

        win_medians=[value[len(value)//2] if value else CIRCLE_TIME for value in win_times]
        lose_medians=[value[len(value)//2] if value else CIRCLE_TIME for value in lose_times]
        
        embed=Embed('Statistics','',COLOR)
        
        for index,user in enumerate(self.source.users):
            win_count=win_counts[index]
            lose_count=lose_counts[index]
            win_median=win_medians[index]
            lose_median=lose_medians[index]
            win_first=win_firsts[index]
            lose_first=lose_firsts[index]

            total=float(win_count)
            total+=(((2**.5)-1.)-((((CIRCLE_TIME+win_median)/CIRCLE_TIME)**.5)-1.))*win_count
            total+=win_first/5.
            total-=(((2**.5)-1.)-((((CIRCLE_TIME+lose_median)/CIRCLE_TIME)**.5)-1.))*lose_count*2.
            total-=lose_first/2.5
            
            embed.add_field(f'{user:f} :',
                f'Correct answers : {win_count}\n'
                f'Bad answers : {lose_count}\n'
                f'Good answer time median : {win_median:.2f} s\n'
                f'Bad answer time median : {lose_median:.2f} s\n'
                f'Answered first: {win_first} GOOD / {lose_first} BAD\n'
                f'Raited : {total:.2f}'
                    )

        embed.add_footer(f'Page 1 /  {len(self.cache)}')
        
        self.cache[0]=embed

    def __getitem__(self,index):
        page=self.cache[index]
        if page is None:
            return self.create_page(index)
        return page

    def create_page(self,index):
        end=index*10
        start=end-9
        if end>len(self.source.history):
            end=len(self.source.history)

        shard=[]
        embed=Embed('Statistics',f'{start} - {end}',COLOR)
        
        add_options=self.source.possibilities
        
        for question_index,element in enumerate(self.source.history[start-1:end],start):
            shard.append('```diff')
            if add_options:
                shard.append('\n')
                shard.append(', '.join([f'{index}. : {option}' for index,option in enumerate(element.options,1)]))
            for user_index,user in enumerate(self.source.users):
                value,time=element.answers[user_index]
                shard.append(f'\n{"+" if element.answer==value else "-"} {user:f} : {value} ( {time:.2f} s )')
            shard.append('\n```')
            embed.add_field(f'{question_index}.: {element.question} - {element.answer}',''.join(shard))
            shard.clear()
        
        embed.add_footer(f'Page {index+1} /  {len(self.cache)}')

        self.cache[index]=embed
        return embed

@ContentParser('str, flags=g, default="\'\'"',
                'condition, default="index==limit"',
                'str, default="\'hiragana\'"',
                'int, default=20',
                'int, default=5',)
async def kanako_manager(client,message,command,*args):
    channel=message.channel

    try:
        game=ACTIVE_GAMES[channel.id]
    except KeyError:
        game=None
        
    command=command.lower()

    if command=='info':
        if game is None:
            embed=Embed('','There is no active game at the channel',COLOR)
        else:
            embed=game.info
            
    elif command=='create':
        embed=kanako_create(client,game,message,args)
        
    elif command=='join':
        if game is None:
            embed=Embed('','There is nothing to join into at the channel',COLOR)
        else:
            game.append(message.author)
            return
        
    elif command=='cancel':
        if game is None:
            embed=Embed('','There is no active message at the channel',COLOR)
        else:
            try:
                game.waiter.set_exception(InterruptedError)
            except InvalidStateError:
                  game.waiter.add_done_callback(lambda future:setattr(future,'_exception',InterruptedError))
            return
        
    elif command=='start':
        while True:
            if game is None:
                message='There is nothing to start at the channel'
                break

            if message.author is not game.users[0]:
                message='Only the oldest user at the game can start it!'
                break
            
            if game.running:
                message='You cannot do that, the game is already running'
                break

            game.waiter.cancel()
            return
        embed=Embed('',message,COLOR)
        
    elif command=='leave':
        if game is None:
            embed=Embed('','There is nothing to leave from at the channel',COLOR)
        else:
            game.remove(message.author)
            return
    else:
        try:
            pages=MAP_showcases[command]
            await embedination(client,channel,pages)
            return
        except KeyError:
            embed=HELP['kanako']
    
    await client.message_create(channel,embed=embed)

def kanako_create(client,game,message,args):
    if game is None:
        if args:
            map_name,amount,possibilities=args
            map_name=map_name.lower()
            text=''
            while True:
                try:
                    map_=MAPS[map_name]
                except KeyError:
                    text=f'Unknown map {map_name}'
                    break

                if amount<10 or amount>len(map_):
                    text=f'Invalid amount {amount}, it needs to be between 10, {len(map_)}'
                    break

                if possibilities not in (5,4,3,0):
                    text=f'Possibilites can be set to 5, 4, 3, 0, got {possibilities}'
                    break
                
                break
            
            if text:
                return Embed('',text,COLOR)

        else:
            map_name='hiragana'
            amount=20
            possibilities=5

        game=kanako_game(client,message.channel,message.author,map_name,amount,possibilities)
        
        ACTIVE_GAMES[message.channel.id]=game
        embed=game.info
        embed.title='Game succesfully created'
        return embed
    else:
        text='There is already an active game at the channel.'
        if not game.running:
            text+=f'\n use **{client.events.message_create.prefix(message)}kanako join** to join into it'
        return Embed('',text,COLOR)


class embedination(metaclass=asyncinit):
    LEFT2   = BUILTIN_EMOJIS['rewind']
    LEFT    = BUILTIN_EMOJIS['arrow_backward']
    RIGHT   = BUILTIN_EMOJIS['arrow_forward']
    RIGHT2  = BUILTIN_EMOJIS['fast_forward']
    RESET   = BUILTIN_EMOJIS['arrows_counterclockwise']
    emojis  = [LEFT2,LEFT,RIGHT,RIGHT2,RESET]
    
    __slots__=['cancel', 'channel', 'page', 'pages', 'task']
    async def __init__(self,client,channel,pages):
        self.pages=pages
        self.page=0
        self.channel=channel
        self.cancel=type(self)._cancel
        self.task=None

        message = await client.message_create(self.channel,embed=self.pages[0])
        message.weakrefer()
        
        if len(self.pages)>1:
            for emoji in self.emojis:
                await client.reaction_add(message,emoji)

        events=multievent(client.events.reaction_add,
                          client.events.reaction_delete)
        
        waitfor_wrapper(client,self,150.,events,message)

    async def __call__(self,wrapper,emoji,user):
        if self.task is not None or user.is_bot:
            return
        client=wrapper.client
        message=wrapper.target
        while True:
            if emoji is self.LEFT:
                page=self.page-1
                break
            if emoji is self.RIGHT:
                page=self.page+1
                break
            if emoji is self.RESET:
                page=0
                break
            if emoji is self.LEFT2:
                page=self.page-10
                break
            if emoji is self.RIGHT2:
                page=self.page+10
                break
            return
        
        if page<0:
            page=0
        elif page>=len(self.pages):
            page=len(self.pages)-1
        
        if self.page==page:
            return

        self.page=page

        wrapper.timeout+=10.

        try:
            self.task = Task(client.message_edit(message,embed=self.pages[page]),client.loop)
            await self.task
        except DiscordException:
            pass
        finally:
            self.task=None
    
    async def _cancel(self,wrapper,exception):
        client=wrapper.client
        if exception is None:
            return
        if isinstance(exception,TimeoutError):
            self.pages=None
            if self.channel.cached_permissions_for(client).can_manage_messages:
                try:
                    self.task=Task(client.reaction_clear(wrapper.target),client.loop)
                    await self.task
                except DiscordException:
                    pass
        
del BUILTIN_EMOJIS
del Color
del ContentParser
