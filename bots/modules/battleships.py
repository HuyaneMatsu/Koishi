# -*- coding: utf-8 -*-
import re, time
from random import randint

from hata import Color, filter_content, is_user_mention, Future, FutureWM, future_or_timeout, sleep, Task, \
    DiscordException, BUILTIN_EMOJIS, Embed, KOKORO, ERROR_CODES, Client
from hata.ext.command_utils import WaitAndContinue, Closer
from hata.ext.commands_v2 import checks, configure_converter

BS_COLOR = Color.from_rgb(71, 130, 255)

OCEAN = BUILTIN_EMOJIS['ocean'].as_emoji

LINE_X_LEAD = ''.join([
    BUILTIN_EMOJIS['black_large_square'].as_emoji,
    BUILTIN_EMOJIS['one'].as_emoji,
    BUILTIN_EMOJIS['two'].as_emoji,
    BUILTIN_EMOJIS['three'].as_emoji,
    BUILTIN_EMOJIS['four'].as_emoji,
    BUILTIN_EMOJIS['five'].as_emoji,
    BUILTIN_EMOJIS['six'].as_emoji,
    BUILTIN_EMOJIS['seven'].as_emoji,
    BUILTIN_EMOJIS['eight'].as_emoji,
    BUILTIN_EMOJIS['nine'].as_emoji,
    BUILTIN_EMOJIS['keycap_ten'].as_emoji,
        ])

LINE_Y_LEAD = (
    BUILTIN_EMOJIS['regional_indicator_a'].as_emoji,
    BUILTIN_EMOJIS['regional_indicator_b'].as_emoji,
    BUILTIN_EMOJIS['regional_indicator_c'].as_emoji,
    BUILTIN_EMOJIS['regional_indicator_d'].as_emoji,
    BUILTIN_EMOJIS['regional_indicator_e'].as_emoji,
    BUILTIN_EMOJIS['regional_indicator_f'].as_emoji,
    BUILTIN_EMOJIS['regional_indicator_g'].as_emoji,
    BUILTIN_EMOJIS['regional_indicator_h'].as_emoji,
    BUILTIN_EMOJIS['regional_indicator_i'].as_emoji,
    BUILTIN_EMOJIS['regional_indicator_j'].as_emoji,
        )

SHIP_VALUES = (
    OCEAN,
    BUILTIN_EMOJIS['cruise_ship'].as_emoji,
    BUILTIN_EMOJIS['ferry'].as_emoji,
    BUILTIN_EMOJIS['speedboat'].as_emoji,
    OCEAN,
    BUILTIN_EMOJIS['cyclone'].as_emoji,
    BUILTIN_EMOJIS['fireworks'].as_emoji,
    BUILTIN_EMOJIS['boom'].as_emoji,
        )

HIDDEN_VALUES = (
    OCEAN,
    OCEAN,
    OCEAN,
    OCEAN,
    OCEAN,
    BUILTIN_EMOJIS['cyclone'].as_emoji,
    BUILTIN_EMOJIS['fireworks'].as_emoji,
    BUILTIN_EMOJIS['boom'].as_emoji,
        )

SWITCH = BUILTIN_EMOJIS['arrows_counterclockwise']

def render_map(data, values):
    
    result = [LINE_X_LEAD]
    line = []
    y = 0
    while True:
        x = 0
        line.append(LINE_Y_LEAD[y])
        while True:
            line.append(values[data[x+y*10]])
            x += 1
            if x == 10:
                break
        result.append(''.join(line))
        line.clear()
        y += 1
        if y == 10:
            break

    return result

POS_PATTERN_0 = re.compile('(\d{1,2}|[a-j]) */? *(\d{1,2}|[a-j]) +([1-4]) *x? *([1-4])', re.I)
POS_PATTERN_1 = re.compile('(\d{1,2}|[a-j]) */? *(\d{1,2}|[a-j])', re.I)
NEW_RP = re.compile('new', re.I)

class wait_on_reply:
    __slots__ = ('guild', 'source', 'target',)
    def __init__(self, guild, source, target):
        self.guild = guild
        self.source = source
        self.target = target
    
    def __call__(self, message):
        if message.author != self.target:
            return False
        
        content = filter_content(message.content)
        
        if len(content) != 2 or content[0].lower() != 'accept':
            return False
        
        content = content[1]
        
        if is_user_mention(content) and (message.user_mentions is not None):
            user = message.user_mentions[0]
        else:
            user = self.guild.get_user(content)
        
        return (self.source == user)

 
class active_request:
    __slots__ = ('future', 'hash', 'source', 'target',)
    def __init__(self, source, target):
        self.source = source
        self.target = target
        self.hash = (source.id>>1)+(target.id>>1)
    def __hash__(self):
        return self.hash
    def __eq__(self, other):
        return self.hash == other.hash
    def __ne__(self, other):
        return self.hash != other.hash
    
BS_GAMES = {}
BS_REQUESTERS = set()
BS_REQUESTS = {}

@configure_converter('user', everywhere=True)
async def battle_manager(client, message, target:'user'=None):
    text = None
    while True:
        if target is None:
            break
        
        guild = message.guild
        source = message.author
        
        if source in BS_GAMES:
            text = 'You cant start a game, if you are in 1 already'
            break
        
        if source in BS_REQUESTERS:
            text = 'You can have only one active request'
            break

        if target is source:
            text = 'Say 2 and easier.'
            break

        if target is client:
            text = 'NO AI opponent yet!'
            break
        
        if target in BS_GAMES:
            text = 'The user is already in game'
            break

        
        request = active_request(source, target)
        
        is_reversed = BS_REQUESTS.get(request, None)

        if is_reversed is not None:
            is_reversed.future.set_result(message)
            return

        BS_REQUESTS[request] = request
        
        BS_REQUESTERS.add(source)
        
        channel = message.channel
        private = await client.channel_private_create(target)
        
        await client.message_create(channel,
            f'Waiting on {target.full_name}\'s reply here and at dm.\nType:"accept name/mention" to accept')
        
        
        future = request.future = Future(KOKORO)
        check = wait_on_reply(guild, source, target)
        event = client.events.message_create
        
        waiter1 = WaitAndContinue(future, check, channel, event, 300.)
        waiter2 = WaitAndContinue(future, check, private, event, 300.)
        
        try:
            result = await future
        except TimeoutError:
            try:
                BS_REQUESTERS.remove(source)
            except KeyError:
                pass
            else:
                text = f'The request from {source.full_name} timed out'
                break
        finally:
            try:
                del BS_REQUESTS[request]
            except KeyError:
                pass

            for waiter in (waiter1, waiter2):
                waiter.cancel()

        try:
            BS_REQUESTERS.remove(source)
        except KeyError:
            text = 'The requester is already in a game'
            break
        
        if target in BS_GAMES:
            text = 'You already accepted a game'
            break

        try:
            BS_REQUESTERS.remove(target)
            await client.message_create(channel, f'Request from {target.full_name} got cancelled')
        except KeyError:
            pass
        
        battleships_game(client, source, target, private)
        text = f'Game between {source.full_name} and {target.full_name} begun.'
        break
    
    if text is None:
        embed = await bs_description(client, message)
        await Closer(client, message.channel, embed)
    else:
        await client.message_create(message.channel, text)

class ship_type:
    __slots__ = ('parts_left', 'size1', 'size2', 'type', 'x', 'y',)
    def __init__(self, x, y, size1, size2, type_):
        self.x = x
        self.y = y
        self.size1 = size1
        self.size2 = size2
        self.type = type_
        self.parts_left = size1*size2

    def __iter__(self):
        x_start = self.x
        x_end = x_start+self.size1
        y_start = self.y*10
        y_end = y_start+self.size2*10
        for n_x in range(x_start, x_end):
            for n_y in range(y_start, y_end, 10):
                yield n_x+n_y

class user_profile:
    __slots__ = ('channel', 'client', 'data', 'last_switch', 'message', 'other', 'page', 'process', 'ship_positions',
        'ships_left', 'state', 'text', 'user')
    ships = [0, 2, 1, 1]
    def __init__(self, user, client):
        self.user = user
        self.client = client
        self.ships_left = self.ships.copy()
        self.ship_positions = {}
        self.data = [0 for _ in range(100)]
        self.text = ''
        self.other = None
        self.process = None
        self.message = None
        self.state = False
        self.last_switch = 0.0
        #we set channel and other from outside
    
    async def process_state_0(self, new, text):
        client = self.client
        if new:
            if text is not None:
                self.text = text
            self.message = await client.message_create(self.channel, embed=self.render_state_0())
        else:
            if self.text != text:
                self.text = text
                await client.message_edit(self.message, embed=self.render_state_0())
    
    async def process_state_1(self, new, text):
        client = self.client
        
        if text is not None:
            self.text = text
        
        message = self.message
        if new:
            client.events.reaction_add.remove(message, self)
            client.events.reaction_delete.remove(message, self)
            
            message = await client.message_create(self.channel, embed=self.render_state_1())
            self.message = message
            Task(client.reaction_add(message, SWITCH), KOKORO)
            
            client.events.reaction_add.append(message, self)
            client.events.reaction_delete.append(message, self)
        else:
            await client.message_edit(message, embed=self.render_state_1())

        self.last_switch = 0.
    
    async def set_state_0(self):
        self.process = self.process_state_0
        
        self.text = 'Good luck!'
        self.message = await self.client.message_create(self.channel, embed=self.render_state_0())
        
    async def set_state_1(self, starts):
        self.process = self.process_state_1
        self.text = ''
        self.state = starts
        
        if starts:
            page = 1
        else:
            page = 0
        self.page = page
        
        client = self.client
        
        message = await client.message_create(self.channel, embed=self.render_state_1())
        self.message = message
        Task(client.reaction_add(self.message, SWITCH), KOKORO)
        
        client.events.reaction_add.append(message, self)
        client.events.reaction_delete.append(message, self)

        self.last_switch = 0.
        

    async def set_state_2(self, state, text):
        self.process = None
        
        self.state = state
        self.text = text
        
        client = self.client
        
        message = self.message
        client.events.reaction_add.remove(message, self)
        client.events.reaction_delete.remove(message, self)
        
        message = await client.message_create(self.channel, embed=self.render_state_2())
        self.message = message
        Task(client.reaction_add(message, SWITCH), KOKORO)
        
        client.events.reaction_add.append(message, self)
        client.events.reaction_delete.append(message, self)
        
        self.last_switch = 0.
    
    async def __call__(self, client, event):
        if event.user is client:
            return
        
        now = time.time()
        if now < self.last_switch+1.2:
            return
        self.last_switch = now
        self.page ^= 1

        if self.process is None:
            embed = self.render_state_2()
        else:
            embed = self.render_state_1()
        
        await self.client.message_edit(self.message, embed=embed)


    def cancel(self):
        client = self.client
        if self.process is None:
            Task(self.cancel_later(), KOKORO)
            return
        
        self.other = None
        if self.process.__func__ is type(self).process_state_1:
            client.events.reaction_add.remove(self.message, self)
            client.events.reaction_delete.remove(self.message, self)
        
    async def cancel_later(self):
        client = self.client
        await sleep(300., KOKORO)
        client.events.reaction_add.remove(self.message, self)
        client.events.reaction_delete.remove(self.message, self)
        self.other = None


    def render_state_0(self):
        other = self.other
        text = [
            'Type "new" to show this message up again.'
            'Type "A-J" "1-10" for coordinate.'
            'And "1-3" "1-3" for ship placement'
            'It always places the ship right-down from the source coordinate'
                ]
        text.extend(render_map(self.data, SHIP_VALUES))
        embed = Embed('', '\n'.join(text), 0x010101)
        embed.add_author(other.user.avatar_url_as(size=64), f'vs.: {other.user.full_name}')
        
        text.clear()
        if sum(self.ships_left):
            sub_text = []
            amount = self.ships_left[1]
            if amount:
                sub_text.append(f'{amount} size 1x3 ship left')
            amount = self.ships_left[2]
            if amount:
                sub_text.append(f'{amount} size 1x4 ship left')
            amount = self.ships_left[3]
            if amount:
                sub_text.append(f'{amount} size 2x2 ship left')
            text.append(', '.join(sub_text))
            text.append(' ship is left to place. ')
        text.append(self.text)
        embed.add_footer(''.join(text))
        return embed

    def render_state_1(self):
        other = self.other
        text = []
        if self.state:
            text.append('**It is your turn!**')
        else:
            text.append('**It is your opponent\'s turn!**')
        
        text.append(
            'Type "new" to show this message up again.'
            'Type "A-J" "1-10" to torpedo a ship.'
            'If you hit your opponent, then it is your turn again.',)

        if self.page:
            text.append('**Your opponents ship:**')
            text.extend(render_map(other.data, HIDDEN_VALUES))
            footer = f'Your opponent has {sum(other.ships_left)} ships left on {len(other.ship_positions)} tiles. {self.text}'
        else:
            text.append('**Your ships:**')
            text.extend(render_map(self.data, SHIP_VALUES))
            footer = f'You have {sum(self.ships_left)} ships left on {len(self.ship_positions)} tiles. {self.text}'

        embed = Embed('', '\n'.join(text), 0x010101)
        embed.add_author(other.user.avatar_url_as(size=64), f'vs.: {other.user:f}')
        embed.add_footer(footer)
        return embed

    def render_state_2(self):
        other = self.other
        text = []
        if self.state:
            text.append('**You won!**\n')
        else:
            text.append('**You lost :cry:**\n')
            
        if self.page:
            text.append('Your opponent\'s ships:')
            text.extend(render_map(other.data, SHIP_VALUES))
        else:
            text.append('Your ships:')
            text.extend(render_map(self.data, SHIP_VALUES))
        
        embed = Embed('', '\n'.join(text), 0x010101)
        embed.add_author(other.user.avatar_url_as(size=64), f'vs.: {other.user:f}')
        embed.add_footer(self.text)
        return embed

class battleships_game:
    __slots__ = ('actual', 'client', 'future', 'player1', 'player2', 'process',)
    def __init__(self, client, user1, user2, channel2):
        
        BS_GAMES[user1] = self
        BS_GAMES[user2] = self
        
        self.client = client
        
        self.player1 = user_profile(user1, client)
        self.player2 = user_profile(user2, client)
        self.player2.channel = channel2
        
        Task(self.start(), KOKORO)
    
    #compability
    async def start(self):
        client = self.client
        player1 = self.player1
        player2 = self.player2

        player1.other = player2
        player2.other = player1
        
        try:
            #creating missing channel
            player1.channel = await client.channel_private_create(player1.user)

            #adding channels to the event to notify us
            client.events.message_create.append(player1.channel, self)
            client.events.message_create.append(player2.channel, self)
            
            #game starts            
            self.future = FutureWM(KOKORO, 2)
            future_or_timeout(self.future, 300.)
            
            #startup
            self.process = self.process_state_0
            Task(player1.set_state_0(), KOKORO)
            Task(player2.set_state_0(), KOKORO)
            
            try:
                await self.future
            except TimeoutError:
                if sum(player1.ships_left) == 0:
                    text1 = 'The other player timed out'
                    text2 = 'You timed out'
                elif sum(player2.ships_left) == 0:
                    text1 = 'You timed out'
                    text2 = 'The other player timed out'
                else:
                    text1 = text2 ='The time is over, both players timed out'
                
                Task(client.message_create(player1.channel, text1), KOKORO)
                Task(client.message_create(player2.channel, text2), KOKORO)
                return
            
            self.process = self.process_state_1
            player1.ships_left[:] = user_profile.ships
            player2.ships_left[:] = user_profile.ships

            if randint(0, 1):
                self.actual = player1
            else:
                self.actual = player2
            
            await self.actual.set_state_1(True)
            await self.actual.other.set_state_1(False)
            
            
            while self.process is not None:
                self.future = Future(KOKORO)
                future_or_timeout(self.future, 300.)
                try:
                    result = await self.future
                except TimeoutError:

                    await self.actual.other.set_state_2(True, 'Your opponent timed out!')
                    await self.actual.set_state_2(False, 'You timed out!')
                    return
                
                if result:
                    self.actual = self.actual.other
        
        
        except BaseException as err:
            if isinstance(err, ConnectionError):
                return
            
            if isinstance(err, DiscordException) and err.code == ERROR_CODES.cannot_message_user:
                return
            
            await client.events.error(client, f'{self!r}.start', err)
        finally:
            self.cancel()
    
    async def process_state_0(self, message):
        if message.author is self.player1.user:
            player = self.player1
        else:
            player = self.player2
        other = player.other
        
        while True:
            if sum(player.ships_left) == 0:
                text = 'Waiting on the other player.'
                break
            
            result = NEW_RP.fullmatch(message.content)
            if result is not None:
                text = 'new'
                break
            
            result = POS_PATTERN_0.fullmatch(message.content)
            if result is None:
                text = 'Bad input format'
                break
            
            result = result.groups()
            
            value = result[0]
            if value.isdigit():
                x = int(value)
                if x > 10:
                    text='Bad input format.'
                    break
                x -= 1
                y = 100
            else:
                x = 100
                y = ('abcdefghij').index(value.lower())
            
            value = result[1]
            if value.isdigit():
                if x != 100:
                    text = 'Dupe coordinate'
                    break
                x = int(value)
                if x > 10:
                    text = 'Bad input format.'
                    break
                x -= 1
            else:
                if y != 100:
                    text = 'Dupe coordinate'
                    break
                y = ('abcdefghij').index(value)
            
            size1 = int(result[2])
            size2 = int(result[3])
            if (size1 == 1 and size2 == 3) or (size1 == 3 and size2 == 1):
                type_=1
            elif (size1 == 1 and size2 == 4) or (size1 == 4 and size2 == 1):
                type_ = 2
            elif (size1 == 2 and size2 == 2):
                type_ = 3
            else:
                text = 'Invalid ship size'
                break
            
            if player.ships_left[type_] == 0:
                text = 'You do not have anymore ships from that size'
                break
            
            
            text = ''
            
            x_start = x
            if x_start > 0:
                x_start -= 1
            
            x_end = x+size1
            if x_end > 10:
                text = 'There is not enough space to place that ship!'
                break
            elif x_end < 10:
                x_end += 1
            
            y_start = y*10
            if y_start > 0:
                y_start -= 10

            y_end = (y+size2)*10
            if y_end > 100:
                text = 'There is not enough space to place that ship!'
                break
            elif y_end < 100:
                y_end += 10

                
            data = player.data
            for n_x in range(x_start, x_end):
                for n_y in range(y_start, y_end, 10):
                    if data[n_x+n_y]:
                        text = (
                            f'Can not set ship to {1+x}/{chr(65+y)}, because coordinate {1+n_x}/{chr(65+n_y//10)} is '
                            'already used.'
                                )
                        break
            if text:
                break
            
            ship = ship_type(x, y, size1, size2, type_)
            cords = []
            
            x_start = x
            x_end = x+size1
            y_start = y*10
            y_end = (y+size2)*10
            for n_x in range(x_start, x_end):
                for n_y in range(y_start, y_end, 10):
                    cord = n_x+n_y
                    data[cord] = type_
                    player.ship_positions[cord] = ship
                    cords.append(f'{chr(65+n_y//10)}/{1+n_x}')
            
            player.ships_left[type_] -= 1
            
            if sum(player.ships_left) == 0:
                self.future.set_result(None)
                text = (
                    f'You placed all of your ships. Last ship placed at: {", ".join(cords)}; waiting on the other '
                    'player.'
                            )
            else:
                text = f'You placed the ship succesfully at: {", ".join(cords)}.'
            
            break
        
        if text == 'new':
            await player.process(True, None)
            return
        
        if sum(player.ships_left) == sum(other.ships_left) == 0:
            return
        
        await player.process(False, text)
    
    async def process_state_1(self, message):
        if self.actual is self.player1:
            player = self.player1
            other = self.player2
        else:
            player = self.player2
            other = self.player1
        
        if message.author is not self.actual.user:
            result = NEW_RP.fullmatch(message.content)
            if result is not None:
                await player.process(True, None)
            return

        data = other.data
        
        while True:
            result = NEW_RP.fullmatch(message.content)
            if result is not None:
                text = 'new'
                break
            
            result = POS_PATTERN_1.fullmatch(message.content)
            if result is None:
                text = 'Bad input format'
                break
            
            result = result.groups()
        
            value = result[0]
            if value.isdigit():
                x = int(value)
                if x > 10:
                    text = 'Bad input format.'
                    break
                x = x-1
                y = 100
            else:
                x = 100
                y = ('abcdefghij').index(value.lower())

            value = result[1]
            if value.isdigit():
                if x != 100:
                    text = 'Dupe coordinate'
                    break
                x = int(value)
                if x > 10:
                    text = 'Bad input format.'
                    break
                x = x-1
            else:
                if y != 100:
                    text = 'Dupe coordinate'
                    break
                y = ('abcdefghij').index(value)
            
            value = data[x+y*10]
            if value > 4:
                text='That position is already shot'
                break

            text = ''
            break
        
        if text:
            if text == 'new':
                await player.process(True, None)                    
            else:
                await player.process(False, text)
            return

        if value == 0:
            data[x+y*10] = 5

            player.state = False
            other.state = True
                
            await player.process(False, 'You missed!')
            await other.process(True, f'Your opponent shot {chr(65+y)}/{1+x}, it missed!\n')
            self.future.set_result(True)
            return
        
        del text
        
        data[x+y*10] = 6
        ship = other.ship_positions.pop(x+y*10)
        ship.parts_left -= 1
        if ship.parts_left == 0:
            other.ships_left[ship.type] -= 1
            for cord in ship:
                data[cord] = 7
            if sum(other.ships_left):
                text1 = f'You shot {chr(65+y)}/{1+x} and you sinked 1 of your opponents ships!\n'
                text2 = f'Your opponent shot {chr(65+y)}/{1+x} and your ship sinked :c\n'
            else:
                self.process = None
                await player.set_state_2(True,
                    f'You shot {chr(65+y)}/{1+x} and you sinked your opponents last ship!')
                await other.set_state_2(False,
                    f'Your opponent shot {chr(65+y)}/{1+x} and your last ship sinked :c')
                self.future.set_result(False)
                return
        else:

            text1 = f'You shot {chr(65+y)}/{1+x} and you hit a ship!'
            text2 = f'Your opponent shot {chr(65+y)}/{1+x} and hit 1 of your ships!'

        player.state = True
        other.state = False
            
        await player.process(False, text1)
        await other.process(True, text2)
        self.future.set_result(False)
    
    async def __call__(self, client, message):
        if message.author is client:
            return
        
        await self.process(message)
        
    def cancel(self):
        event = self.client.events.message_create
        event.remove(self, self.player1.channel)
        event.remove(self, self.player2.channel)
        
        del BS_GAMES[self.player1.user]
        del BS_GAMES[self.player2.user]

        self.player1.cancel()
        self.player2.cancel()

async def bs_description(command_context):
    return Embed('bs', (
        'Requests a battleship game with the given user.\n'
        f'Usage: `{command_context.prefix}bs *user*`'
        ), color=BS_COLOR).add_footer(
            'Guild only!')

COMMAND_CLIENT: Client
COMMAND_CLIENT.commands(battle_manager,
    name='bs',
    checks=checks.guild_only(),
    category='GAMES',
    description=bs_description,
        )
