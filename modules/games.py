from random import random, choice, randint

from hata import Color, Embed, eventlist, DiscordException, parse_emoji, CLIENTS, BUILTIN_EMOJIS, ERROR_CODES
from hata.ext.commands import Command, wait_for_message, ConverterFlag, Converter, wait_for_reaction

GAMES_COLOR = Color.from_rgb(148,0,211)
GAMES_COMMANDS = eventlist(type_=Command)

def setup(lib):
    Koishi.commands.extend(GAMES_COMMANDS)
    
def teardown(lib):
    Koishi.commands.unextend(GAMES_COMMANDS)


@GAMES_COMMANDS.from_class
class message_me:
    async def command(client,message):
        channel = await client.channel_private_create(message.author)
        try:
            await client.message_create(channel,'Love you!')
        except DiscordException as err:
            if err.code == ERROR_CODES.cannot_send_message_to_user:
                await client.message_create(message.channel,'Pls turn on private messages from this server!')
    
    category = 'GAMES'
    
    async def description(client,message):
        prefix = client.command_processer.get_prefix_for(message)
        embed=Embed('message_me',(
            'I ll send you something, from really deep of my heart.\n'
            f'Usage : `{prefix}message_me`'
            ),color=GAMES_COLOR)
        await client.message_create(message.channel,embed=embed)


@GAMES_COMMANDS.from_class
class dice:
    async def command(client,message,times:int = 1):
        if times<=0:
            text=f'{times} KEK'
        elif times>6:
            text='I have only 6 dices, sorry, no money for more. Sadpanda'
        else:
            result=0
            for x in range(times):
                result+=randint(1,6)
                
            if result<=2.5*times:
                luck_text=', better luck next time!'
            elif result>=5.5*times:
                luck_text=', so BIG,.. thats what she said... *cough*'
            else:
                luck_text=''
            text=f'Rolled {result}{luck_text}'
        
        await client.message_create(message.channel,text)
    
    category = 'GAMES'
    
    async def description(client,message):
        prefix = client.command_processer.get_prefix_for(message)
        embed=Embed('dice',(
            'I will throw some dice and tell you the sum.\n'
            f'Usage: `{prefix}dice <dice_count>`\n'
            '`dice_count` if optional, but I have only 6 dices...'
            ),color=GAMES_COLOR).add_footer(
                'I see you Yukari peeking there! You dice stealer!')
        await client.message_create(message.channel,embed=embed)


def check_message_for_emoji(message):
    parsed=parse_emoji(message.content)
    if parsed is None:
        return False
    return parsed

@GAMES_COMMANDS.from_class
class waitemoji:
    async def command(client,message):
        channel=message.channel
        
        message_to_delete = await client.message_create(channel,'Waiting!')
        
        try:
            _,emoji = await wait_for_message(client,channel,check_message_for_emoji,30.)
        except TimeoutError:
            return
        finally:
            await client.message_delete(message_to_delete)
        
        await client.message_create(channel,emoji.as_emoji*5)
    
    category = 'GAMES'
    
    async def description(client,message):
        prefix = client.command_processer.get_prefix_for(message)
        embed=Embed('waitemoji',(
            'After using this command, I ll wait some time for you to send '
            'an emoji at this channel. If you sent one, I ll send it back five '
            'times instead.\n'
            f'Usage : `{prefix}waitemoji`'
            ),color=GAMES_COLOR)
        await client.message_create(message.channel,embed=embed)


@GAMES_COMMANDS.from_class
class rate:
    async def command(client, message, target:Converter('user', flags=ConverterFlag.user_default.update_by_keys(everywhere=True), default_code='message.author')):
        if target in CLIENTS or client.is_owner(target):
            result=10
        else:
            result=target.id%11
        #nickname check
        await client.message_create(message.channel,f'I rate {target.name_at(message.guild)} {result}/10')
    
    category = 'GAMES'
    
    async def description(client,message):
        prefix = client.command_processer.get_prefix_for(message)
        embed=Embed('rate',(
            'Do you want me, to rate someone?\n'
            f'Usage: `{prefix}rate <user>`\n'
            'If no user is passed, I will rate you :3'
            ),color=GAMES_COLOR)
        await client.message_create(message.channel,embed=embed)


MINE_MINE_CLEAR = (
    BUILTIN_EMOJIS['white_large_square'].as_emoji,
    BUILTIN_EMOJIS['one'].as_emoji,
    BUILTIN_EMOJIS['two'].as_emoji,
    BUILTIN_EMOJIS['three'].as_emoji,
    BUILTIN_EMOJIS['four'].as_emoji,
    BUILTIN_EMOJIS['five'].as_emoji,
    BUILTIN_EMOJIS['six'].as_emoji,
    BUILTIN_EMOJIS['seven'].as_emoji,
    BUILTIN_EMOJIS['eight'].as_emoji,
    BUILTIN_EMOJIS['bomb'].as_emoji,
        )

MINE_MINE=tuple(f'||{e}||' for e in MINE_MINE_CLEAR)
MINE_CANCEL=BUILTIN_EMOJIS['anger']

class check_emoji_and_user(object):
    __slots__=('emoji', 'user',)
    def __init__(self,emoji,user):
        self.emoji=emoji
        self.user=user
    def __call__(self, message, emoji, user):
        return (self.emoji is emoji) and (self.user==user)

@GAMES_COMMANDS.from_class
class mine:
    async def command(client,message,word:str='',word2:str=''):
        text_mode=False
        amount=0
        
        if word:
            if word=='text':
                text_mode=True
                word=word2
            
            if word.isdigit():
                amount=int(word)
                if amount>24:
                    amount=24
                elif amount<8:
                    amount=8
        
        if amount==0:
            amount=12
        
        data=[0 for x in range(100)]
        
        while amount:
            x=randint(0,9)
            y=randint(0,9)
            position=x+y*10
    
            value=data[position]
            if value==9:
                continue
            
            local_count=0
    
            for c_x,c_y in ((-1,-1),(0,-1),(1,-1),(1,0),(1,1),(0,1),(-1,1),(-1,0)):
                local_x=x+c_x
                local_y=y+c_y
                if local_x!=10 and local_x!=-1 and local_y!=10 and local_y!=-1 and data[local_x+local_y*10]==9:
                    local_count+=1
            
            if local_count>3:
                continue
    
            for c_x,c_y in ((-1,-1),(0,-1),(1,-1),(1,0),(1,1),(0,1),(-1,1),(-1,0)):
                local_x=x+c_x
                local_y=y+c_y
                if local_x!=10 and local_x!=-1 and local_y!=10 and local_y!=-1:
                    local_position=local_x+local_y*10
                    local_value=data[local_position]
                    if local_value==9:
                        continue
                    data[local_position]=local_value+1
                    
            data[position]=9
            
            amount-=1
    
        result=[]
        result_sub=[]
        y=0
        while True:
            x=0
            while True:
                result_sub.append(MINE_MINE[data[x+y]])
                x+=1
                if x==10:
                    break
            result.append(''.join(result_sub))
            result_sub.clear()
            y+=10
            if y==100:
                break
        
        if text_mode:
            result.insert(0,'```')
            result.append('```')
        else:
            emoji=MINE_CANCEL
            user=message.author
        
        text='\n'.join(result)
        result.clear()
        
        message = await client.message_create(message.channel,text)
    
        if text_mode or (not message.channel.cached_permissions_for(client).can_add_reactions):
            return
        
        await client.reaction_add(message,emoji)
    
        try:
            await wait_for_reaction(client,message,check_emoji_and_user(emoji,user),1200.)
        except TimeoutError:
            return
        finally:
            await client.reaction_delete_own(message,emoji)
    
        y=0
        while True:
            x=0
            while True:
                result_sub.append(MINE_MINE_CLEAR[data[x+y]])
                x+=1
                if x==10:
                    break
            result.append(''.join(result_sub))
            result_sub.clear()
            y+=10
            if y==100:
                break
        text='\n'.join(result)
    
        await client.message_edit(message,text)

    category = 'GAMES'
    
    async def description(client,message):
        prefix = client.command_processer.get_prefix_for(message)
        embed=Embed('mine',(
            'I creates a minesweeper game.\n'
            'If you are mad already from failing, just click on the '
            f'{MINE_CANCEL.as_emoji} under the mine.\n'
            f'Usage : `{prefix}mine (text) <bomb_count>`\n'
            'By passing a `text` keyword, I will send the whole mine in a '
            'codeblock, allowing you, to simply copy-paste it.\n'
            'The default bomb count in 12, but you can change it between '
            '8 and 24.'
                ),color=GAMES_COLOR)
        await client.message_create(message.channel,embed=embed)


@GAMES_COMMANDS.from_class
class yuno:
    async def command(client,message):
        await client.message_create(message.channel,embed=Embed('YUKI YUKI YUKI!',
            '░░░░░░░░░░░▄▄▀▀▀▀▀▀▀▀▄▄░░░░░░░░░░░░░\n'
            '░░░░░░░░▄▀▀░░░░░░░░░░░░▀▄▄░░░░░░░░░░\n'
            '░░░░░░▄▀░░░░░░░░░░░░░░░░░░▀▄░░░░░░░░\n'
            '░░░░░▌░░░░░░░░░░░░░▀▄░░░░░░░▀▀▄░░░░░\n'
            '░░░░▌░░░░░░░░░░░░░░░░▀▌░░░░░░░░▌░░░░\n'
            '░░░▐░░░░░░░░░░░░▒░░░░░▌░░░░░░░░▐░░░░\n'
            '░░░▌▐░░░░▐░░░░▐▒▒░░░░░▌░░░░░░░░░▌░░░\n'
            '░░▐░▌░░░░▌░░▐░▌▒▒▒░░░▐░░░░░▒░▌▐░▐░░░\n'
            '░░▐░▌▒░░░▌▄▄▀▀▌▌▒▒░▒░▐▀▌▀▌▄▒░▐▒▌░▌░░\n'
            '░░░▌▌░▒░░▐▀▄▌▌▐▐▒▒▒▒▐▐▐▒▐▒▌▌░▐▒▌▄▐░░\n'
            '░▄▀▄▐▒▒▒░▌▌▄▀▄▐░▌▌▒▐░▌▄▀▄░▐▒░▐▒▌░▀▄░\n'
            '▀▄▀▒▒▌▒▒▄▀░▌█▐░░▐▐▀░░░▌█▐░▀▄▐▒▌▌░░░▀\n'
            '░▀▀▄▄▐▒▀▄▀░▀▄▀░░░░░░░░▀▄▀▄▀▒▌░▐░░░░░\n'
            '░░░░▀▐▀▄▒▀▄░░░░░░░░▐░░░░░░▀▌▐░░░░░░░\n'
            '░░░░░░▌▒▌▐▒▀░░░░░░░░░░░░░░▐▒▐░░░░░░░\n'
            '░░░░░░▐░▐▒▌░░░░▄▄▀▀▀▀▄░░░░▌▒▐░░░░░░░\n'
            '░░░░░░░▌▐▒▐▄░░░▐▒▒▒▒▒▌░░▄▀▒░▐░░░░░░░\n'
            '░░░░░░▐░░▌▐▐▀▄░░▀▄▄▄▀░▄▀▐▒░░▐░░░░░░░\n'
            '░░░░░░▌▌░▌▐░▌▒▀▄▄░░░░▄▌▐░▌▒░▐░░░░░░░\n'
            '░░░░░▐▒▐░▐▐░▌▒▒▒▒▀▀▄▀▌▐░░▌▒░▌░░░░░░░\n'
            '░░░░░▌▒▒▌▐▒▌▒▒▒▒▒▒▒▒▐▀▄▌░▐▒▒▌░░░░░░░\n'
            ,0xffafde,'https://www.youtube.com/watch?v=TaDAn_S_4Y8'))
    
    category = 'GAMES'
    
    async def description(client,message):
        embed=Embed('yuno',(
            'Your personal yandere.\n'
            'Good luck, I better leave now!'
                ),color=GAMES_COLOR)
        await client.message_create(message.channel,embed=embed)


@GAMES_COMMANDS.from_class
class command_random:
    async def command(client,message,v1 :int,v2:int=0):
        result=randint(v2,v1) if v1>v2 else randint(v1,v2)
        await client.message_create(message.channel,str(result))
    
    name = 'random'
    category = 'GAMES'
    
    async def description(client,message):
        prefix = client.command_processer.get_prefix_for(message)
        embed=Embed('random',(
            'Do you need some random numbers?\n'
            f'Usage: `{prefix}random *number_1* <number_2>`\n'
            'You should pass at least 1 number. The second is optinal and by '
            'default is `0`.'),color=GAMES_COLOR)
        await client.message_create(message.channel,embed=embed)


def generate_love_level():
    value = {
        'titles' : (
            f'{BUILTIN_EMOJIS["blue_heart"]:e} There\'s no real connection between you two {BUILTIN_EMOJIS["blue_heart"]:e}',
                ),
        'text' : (
            'The chance of this relationship working out is really low. You '
            'can get it to work, but with high costs and no guarantee of '
            'working out. Do not sit back, spend as much time together as '
            'possible, talk a lot with each other to increase the chances of '
            'this relationship\'s survival.'
                ),
            }

    for x in range(0,2):
        yield value

    value = {
        'titles' : (
            f'{BUILTIN_EMOJIS["blue_heart"]:e} A small acquaintance {BUILTIN_EMOJIS["blue_heart"]:e}',
                ),
        'text' : (
            'There might be a chance of this relationship working out somewhat '
            'well, but it is not very high. With a lot of time and effort '
            'you\'ll get it to work eventually, however don\'t count on it. It '
            'might fall apart quicker than you\'d expect.'
                ),
            }
    
    for x in range(2,6):
        yield value

    value = {
        'titles' : (
            f'{BUILTIN_EMOJIS["purple_heart"]:e} You two seem like casual friends {BUILTIN_EMOJIS["purple_heart"]:e}',
                ),
        'text' : (
            'The chance of this relationship working is not very high. You both '
            'need to put time and effort into this relationship, if you want it '
            'to work out well for both of you. Talk with each other about '
            'everything and don\'t lock yourself up. Spend time together. This '
            'will improve the chances of this relationship\'s survival by a lot.'
                ),
            }

    for x in range(6,21):
        yield value

    value = {
        'titles' : (
            f'{BUILTIN_EMOJIS["heartpulse"]:e} You seem like you are good friends {BUILTIN_EMOJIS["heartpulse"]:e}',
                ),
        'text' : (
            'The chance of this relationship working is not very high, but its '
            'not that low either. If you both want this relationship to work, '
            'and put time and effort into it, meaning spending time together, '
            'talking to each other etc., than nothing shall stand in your way.'
                ),
            }

    for x in range(21,31):
        yield value


    value = {
        'titles':(
            f'{BUILTIN_EMOJIS["cupid"]:e} You two are really close aren\'t you? {BUILTIN_EMOJIS["cupid"]:e}',
                ),
        'text' : (
            'Your relationship has a reasonable amount of working out. But do '
            'not overestimate yourself there. Your relationship will suffer '
            'good and bad times. Make sure to not let the bad times destroy '
            'your relationship, so do not hesitate to talk to each other, '
            'figure problems out together etc.'
                ),
            }

    for x in range(31,46):
        yield value
    
    value = {
        'titles' : (
            f'{BUILTIN_EMOJIS["heart"]:e} So when will you two go on a date? {BUILTIN_EMOJIS["heart"]:e}',
                ),
        'text' : (
            'Your relationship will most likely work out. It won\'t be perfect '
            'and you two need to spend a lot of time together, but if you keep '
            'on having contact, the good times in your relationship will '
            'outweigh the bad ones.'
                ),
            }

    for x in range(46,61):
        yield value

    value = {
        'titles' : (
            f'{BUILTIN_EMOJIS["two_hearts"]:e} Aww look you two fit so well together {BUILTIN_EMOJIS["two_hearts"]:e}',
                ),
        'text' : (
            'Your relationship will most likely work out well. Don\'t hesitate '
            'on making contact with each other though, as your relationship '
            'might suffer from a lack of time spent together. Talking with '
            'each other and spending time together is key.'
                ),
            }

    for x in range(61,86):
        yield value

    value = {
        'titles' : (
            f'{BUILTIN_EMOJIS["sparkling_heart"]:e} Love is in the air {BUILTIN_EMOJIS["sparkling_heart"]:e}',
            f'{BUILTIN_EMOJIS["sparkling_heart"]:e} Planned your future yet? {BUILTIN_EMOJIS["sparkling_heart"]:e}',
                ),
        'text' : (
            'Your relationship will most likely work out perfect. This '
            'doesn\'t mean thought that you don\'t need to put effort into it. '
            'Talk to each other, spend time together, and you two won\'t have '
            'a hard time.'
                ),
            }

    for x in range(86,96):
        yield value

    value = {
        'titles' : (
            f'{BUILTIN_EMOJIS["sparkling_heart"]:e} When will you two marry? {BUILTIN_EMOJIS["sparkling_heart"]:e}',
            f'{BUILTIN_EMOJIS["sparkling_heart"]:e} Now kiss already {BUILTIN_EMOJIS["sparkling_heart"]:e}',
                ),
        'text' : (
            'You two will most likely have the perfect relationship. But don\'t '
            'think that this means you don\'t have to do anything for it to '
            'work. Talking to each other and spending time together is key, '
            'even in a seemingly perfect relationship.'
                ),
            }

    for x in range(96,101):
        yield value

LOVE_VALUES=tuple(generate_love_level())
del generate_love_level

@GAMES_COMMANDS.from_class
class love:
    async def command(client,message,target:Converter('user',flags=ConverterFlag.user_default.update_by_keys(everywhere=True))):
        source=message.author
        if source is target:
            prefix = client.command_processer.get_prefix_for(message)
            embed=Embed('love',(
                'How much you two fit together?\n'
                f'Usage: `{prefix}user *user*`'
                ),color=GAMES_COLOR)
        else:
            percent=((source.id&0x1111111111111111111111)+(target.id&0x1111111111111111111111))%101
            element=LOVE_VALUES[percent]
            
            embed=Embed(
                choice(element['titles']),
                f'{source:f} {BUILTIN_EMOJIS["heart"]:e} {target:f} scored {percent}%!',
                0xad1457,
                    )
            embed.add_field('My advice:',element['text'])
    
        await client.message_create(message.channel,embed=embed)
    
    category = 'GAMES'
    
    async def description(client,message):
        prefix = client.command_processer.get_prefix_for(message)
        embed=Embed('love',(
            'How much you two fit together?'
            f'Usage: `{prefix}user *user*`\n'
            ),color=GAMES_COLOR)
        await client.message_create(message.channel,embed=embed)
    
    async def parser_failure_handler(client, message, command, content, args):
        prefix = client.command_processer.get_prefix_for(message)
        embed=Embed('love',(
            'How much you two fit together?'
            f'Usage: `{prefix}user *user*`\n'
            ),color=GAMES_COLOR)
        await client.message_create(message.channel,embed=embed)
