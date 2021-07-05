import os
from random import randint

from hata import ERROR_CODES, BUILTIN_EMOJIS, CancelledError, Task, sleep, InvalidStateError, any_to_any, Color, \
    Embed, DiscordException, ReuBytesIO, LOOP_TIME, Client, KOKORO, future_or_timeout, Future, InteractionEvent

from hata.ext.command_utils import GUI_STATE_READY, GUI_STATE_SWITCHING_PAGE, GUI_STATE_CANCELLING, \
    GUI_STATE_CANCELLED, GUI_STATE_SWITCHING_CTX, Timeouter
from hata.ext.slash import abort

from bot_utils.shared import PATH__KOISHI
from PIL import Image as PIL

FONT = PIL.font(os.path.join(PATH__KOISHI, 'library', 'Kozuka.otf'), 90)
FONT_COLOR = (162, 61, 229)

del os

def draw(buffer, text):
    image = PIL.new('RGBA', FONT.getsize(text), (0, 0, 0, 0))
    image.draw().text((0,0), text, fill=FONT_COLOR, font=FONT)
    image.save(buffer, 'png')
    buffer.seek(0)
    return buffer

ACTIVE_GAMES = {}
CIRCLE_TIME = 60.
KANAKO_COLOR = Color.from_tuple(FONT_COLOR)

SLASH_CLIENT : Client
KANAKO = SLASH_CLIENT.interactions(None,
    name = 'kanako',
    description = 'Start a hiragana or a katakana quiz!',
    is_global = True,
)

@KANAKO.interactions
async def create_(client, event,
        map_ : ([('hiragana', 'hiragana'), ('katakana', 'katakana')], 'Choose a map to play!') = 'hiragana',
        length : ('int', 'The amount of questions.') = 20,
        possibilities : ([('0', 0), ('3', 3), ('4', 4), ('5', 5)], 'Amount of possibilities to chose from.') = 5,
            ):
    """Create a new game!"""
    guild = event.guild
    if guild is None:
        abort('Guild only command')
    
    if guild not in client.guild_profiles:
        abort('I must be in the guild to execute this command.')
    
    permissions = event.channel.cached_permissions_for(client)
    if (not permissions.can_send_messages) or (not permissions.can_add_reactions):
        abort('I need `send messages` and `add reactions` permission to execute this command.')
    
    game = ACTIVE_GAMES.get(event.channel.id, None)

    if game is None:
        if length < 10:
            length = 10
        else:
            map_length = len(MAPS[map_])
            if length > map_length:
                length = map_length
        
        game = KanakoJoinWaiter(client, event, map_, length, possibilities)
        
        embed = game.get_information()
        embed.title = 'Game successfully created'
        return embed
    
    description = 'There is already an active game at the channel.'
    if isinstance(game, KanakoJoinWaiter):
        description += '\n use **/kanako join** to join into it'
    
    return Embed(None, description, color=KANAKO_COLOR)

@KANAKO.interactions
async def start_(client, event):
    """Starts the current game."""
    game = ACTIVE_GAMES.get(event.channel.id, None)
    if game is None:
        abort('There is no active game at the channel.')
    
    if isinstance(game, KanakoRunner):
        abort('The game is already started, oof.')
    
    return game.start_user(event.user)

@KANAKO.interactions
async def info(client, event):
    """Shows information about the current game."""
    game = ACTIVE_GAMES.get(event.channel.id, None)
    if game is None:
        abort('There is no active game at the channel.')
    
    return game.get_information()

@KANAKO.interactions
async def join(client, event):
    """Join to the currently active game inside of the channel!"""
    game = ACTIVE_GAMES.get(event.channel.id, None)
    if game is None:
        abort('There is nothing to join into at the channel.')
    
    if isinstance(game, KanakoRunner):
        abort('The game is already started, oof.')
    
    return Embed(None, game.join_user(event.user), color=KANAKO_COLOR)

@KANAKO.interactions
async def leave(client, event):
    """Leave from the current game, pls no."""
    game = ACTIVE_GAMES.get(event.channel.id, None)
    if game is None:
        abort('Nothing to leave from.')
    
    return Embed(None, game.leave_user(event.user), color=KANAKO_COLOR)

@KANAKO.interactions
async def cancel_(client, event):
    """Cancels the current game, pls no."""
    game = ACTIVE_GAMES.get(event.channel.id, None)
    if game is None:
        description = 'Nothing to cancel.'
    elif isinstance(game, KanakoRunner):
        description = game.leave_user(event.user)
    else:
        description = game.cancel_user(event.user)
    
    return Embed(None, description, color=KANAKO_COLOR)

@KANAKO.interactions
async def show_map(client, event,
        map_ : ([('hiragana', 'hiragana'), ('katakana', 'katakana')], 'Choose a map to display!')
            ):
    """Shows the selected map!"""
    permissions = event.channel.cached_permissions_for(client)
    if (not permissions.can_send_messages) or (not permissions.can_add_reactions):
        abort('I need `send messages` and `add reactions` permission to execute this command.')
    
    pages = MAP_SHOWCASES[map_]
    await KanakoPagination(client, event, pages)

_pairsK = ('k', 'g', 's', 'z', 'c', 't', 'd', 'f', 'h', 'b', 'p', 'n', 'm', 'y', 'r', 'w', 'j',)
_pairsKx = {
    'k': ('k', 'g'),
    'g': ('k', 'g'),
    's': ('s', 'z', 'c'),
    'z': ('s', 'z', 'c'),
    'c': ('s', 'z', 'c'),
    't': ('t', 'd'),
    'd': ('t', 'd'),
    'f': ('f', 'h', 'b', 'p'),
    'h': ('f', 'h', 'b', 'p'),
    'b': ('f', 'h', 'b', 'p'),
    'p': ('f', 'h', 'b', 'p')
        }
_pairsD = ('a', 'i', 'e', 'o', 'u')
_hiragana = [
    ('あ', 'a'), ('い', 'i'), ('う', 'u'), ('え', 'e'), ('お', 'o'),
    ('か', 'ka'), ('き', 'ki'), ('く', 'ku'), ('け', 'ke'), ('こ', 'ko'),
    ('が', 'ga'), ('ぎ', 'gi'), ('ぐ', 'gu'), ('げ', 'ge'), ('ご', 'go'),
    ('さ', 'sa'), ('し', 'shi'), ('す', 'su'), ('せ', 'se'), ('そ', 'so'),
    ('ざ', 'za'), ('じ', 'ji'), ('ず', 'zu'), ('ぜ', 'ze'), ('ぞ', 'zo'),
    ('た', 'ta'), ('ち', 'chi'), ('つ', 'tsu'), ('て', 'te'), ('と', 'to'),
    ('だ', 'da'), ('ぢ', 'ji'), ('づ', 'zu'), ('で', 'de'), ('ど', 'do'),
    ('な', 'na'), ('に', 'ni'), ('ぬ', 'nu'), ('ね', 'ne'), ('の', 'no'),
    ('は', 'ha'), ('ひ', 'hi'), ('ふ', 'fu'), ('へ', 'he'), ('ほ', 'ho'),
    ('ば', 'ba'), ('び', 'bi'), ('ぶ', 'bu'), ('べ', 'be'), ('ぼ', 'bo'),
    ('ぱ', 'pa'), ('ぴ', 'pi'), ('ぷ', 'pu'), ('ぺ', 'pe'), ('ぽ', 'po'),
    ('ま', 'ma'), ('み', 'mi'), ('む', 'mu'), ('め', 'me'), ('も', 'mo'),
    ('ら', 'ra'), ('り', 'ri'), ('る', 'ru'), ('れ', 're'), ('ろ', 'ro'),
    ('わ', 'wa'), ('ゐ', 'wi'), ('ゔ', 'vu'), ('ゑ', 'we'), ('を', 'wo'),
    ('や', 'ya'), ('ゆ', 'yu'), ('よ', 'yo'),
    ('ん', 'n'),
    ('きゃ', 'kya'), ('きゅ', 'kyu'), ('きょ', 'kyo'),
    ('ぎゃ', 'gya'), ('ぎゅ', 'gyu'), ('ぎょ', 'gyo'),
    ('しゃ', 'sha'), ('しゅ', 'shu'), ('しょ', 'sho'),
    ('じゃ', 'ja'), ('じゅ', 'ju'), ('じょ', 'jo'),
    ('ちゃ', 'cha'), ('ちゅ', 'chu'), ('ちょ', 'cho'),
    ('ぢゃ', 'ja'), ('ぢゅ', 'ju'), ('ぢょ', 'jo'),
    ('にゃ', 'nya'), ('にゅ', 'nyu'), ('にょ', 'nyo'),
    ('ひゃ', 'hya'), ('ひゅ', 'hyu'), ('ひょ', 'hyo'),
    ('びゃ', 'bya'), ('びゅ', 'byu'), ('びょ', 'byo'),
    ('ぴゃ', 'pya'), ('ぴゅ', 'pyu'), ('ぴょ', 'pyo'),
    ('みゃ', 'mya'), ('みゅ', 'myu'), ('みょ', 'myo'),
    ('りゃ', 'rya'), ('りゅ', 'ryu'), ('りょ', 'ryo'),
        ]
_katakana = [
    ('ア', 'a'), ('イ', 'i'), ('ウ', 'u'), ('エ', 'e'), ('オ', 'o'),
    ('カ', 'ka'), ('キ', 'ki'), ('ク', 'ku'), ('ケ', 'ke'), ('コ', 'ko'),
    ('ガ', 'ga'), ('ギ', 'gi'), ('グ', 'gu'), ('ゲ', 'ge'), ('ゴ', 'go'),
    ('サ', 'sa'), ('シ', 'shi'), ('ス', 'su'), ('セ', 'se'), ('ソ', 'so'),
    ('ザ', 'za'), ('ジ', 'ji'), ('ズ', 'zu'), ('ゼ', 'ze'), ('ゾ', 'zo'),
    ('タ', 'ta'), ('チ', 'chi'), ('ツ', 'tsu'), ('テ', 'te'), ('ト', 'to'),
    ('ダ', 'da'), ('ヂ', 'ji'), ('ヅ', 'zu'), ('デ', 'de'), ('ド', 'do'),
    ('ナ', 'na'), ('ニ', 'ni'), ('ヌ', 'nu'), ('ネ', 'ne'), ('ノ', 'no'),
    ('ハ', 'ha'), ('ヒ', 'hi'), ('フ', 'fu'), ('ヘ', 'he'), ('ホ', 'ho'),
    ('バ', 'ba'), ('ビ', 'bi'), ('ブ', 'bu'), ('ベ', 'be'), ('ボ', 'bo'),
    ('パ', 'pa'), ('ピ', 'pi'), ('プ', 'pu'), ('ペ', 'pe'), ('ポ', 'po'),
    ('マ', 'ma'), ('ミ', 'mi'), ('ム', 'mu'), ('メ', 'me'), ('モ', 'mo'),
    ('ラ', 'ra'), ('リ', 'ri'), ('ル', 'ru'), ('レ', 're'), ('ロ', 'ro'),
    ('ワ', 'wa'), ('ヸ', 'wi'), ('ヴ', 'vu'), ('ヹ', 'we'), ('ヲ', 'wo'),
    ('ヤ', 'ya'), ('ュ', 'yu'), ('ョ', 'yo'),
    ('ン', 'n'),
    ('キャ', 'kya'), ('キュ', 'kyu'), ('キョ', 'kyo'),
    ('ギャ', 'gya'), ('ギュ', 'gyu'), ('ギョ', 'gyo'),
    ('シャ', 'sha'), ('シュ', 'shu'), ('ショ', 'sho'),
    ('ジャ', 'ja'), ('ジュ', 'ju'), ('ジョ', 'jo'),
    ('チャ', 'cha'), ('チュ', 'chu'), ('チョ', 'cho'),
    ('ヂャ', 'ja'), ('ヂュ', 'ju'), ('ヂョ', 'jo'),
    ('ニャ', 'nya'), ('ニュ', 'nyu'), ('ニョ', 'nyo'),
    ('ヒャ', 'hya'), ('ヒュ', 'hyu'), ('ヒョ', 'hyo'),
    ('ビャ', 'bya'), ('ビュ', 'byu'), ('ビョ', 'byo'),
    ('ピャ', 'pya'), ('ピュ', 'pyu'), ('ピョ', 'pyo'),
    ('ミャ', 'mya'), ('ミュ', 'myu'), ('ミョ', 'myo'),
    ('リャ', 'rya'), ('リュ', 'ryu'), ('リョ', 'ryo'),
        ]

MAPS = {'hiragana':_hiragana, 'katakana':_katakana}

def render_showcase(name,map_):
    result = []
    element_index = 0
    element_limit = len(map_)
    
    page_index = 1
    page_limit = (element_limit+29)//30

    field_text = []
    
    while True:
        if page_index > page_limit:
            break
        
        embed = Embed(name.capitalize(), '',KANAKO_COLOR)
        embed.add_footer(f'page {page_index} / {page_limit}')
        
        for _ in range(((element_limit%30)+9)//10 if page_index==page_limit else 3):
            field_index_limit = element_index+10
            if field_index_limit > element_limit:
                field_index_limit = element_limit
            
            while element_index<field_index_limit:
                element = map_[element_index]
                element_index += 1
                field_text.append(f'{element_index}.: **{element[0]} - {element[1]}**')

            embed.add_field(f'{element_index-9} - {element_index}', '\n'.join(field_text),inline=True)
            field_text.clear()
            
        result.append(embed)
        page_index += 1

    return result

MAP_SHOWCASES = {name:render_showcase(name, map_) for name,map_ in MAPS.items()}

class HistoryElement:
    __slots__ = ('answer', 'answers', 'options', 'question',)

class KanakoJoinWaiter:
    __slots__ = ('client', 'channel', 'users', 'map_name', 'length', 'possibilities', 'cancelled', 'waiter',)
    def __new__(cls, client, event, map_name, length, possibilities):
        self = object.__new__(cls)
        self.client = client
        self.channel = event.channel
        self.users = [event.user]
        
        self.map_name = map_name
        self.length = length
        self.possibilities = possibilities
        
        self.cancelled = False
        self.waiter = waiter = Future(KOKORO)
        future_or_timeout(waiter, 300.0)
        
        Task(self.start_waiting(), KOKORO)
        ACTIVE_GAMES[event.channel.id] = self
        
        return self
    
    async def start_waiting(self):
        try:
            await self.waiter
        except TimeoutError:
            timeout = True
        else:
            timeout = False
        finally:
            channel_id = self.channel.id
            if ACTIVE_GAMES[channel_id] is self:
                del ACTIVE_GAMES[channel_id]
        
        if self.cancelled:
            return
        
        if timeout:
            embed = Embed('Timeout occurred', 'Kanako game cancelled!', color=KANAKO_COLOR)
            client = self.client
            try:
                await self.client.message_create(self.channel, embed=embed)
            except BaseException as err:
                if isinstance(err, ConnectionError):
                    return
                
                if isinstance(err, DiscordException):
                    if err.code in (
                            ERROR_CODES.unknown_channel, # channel deleted
                            ERROR_CODES.missing_access, # client removed
                            ERROR_CODES.missing_permissions, # permissions changed meanwhile
                                ):
                        return
                
                await client.events.error(client, f'{self.__class__.__name__}.start_waiting', err)
                return
            
            return
        
        KanakoRunner(self)
    
    def get_information(self):
        return Embed(
            'Game information:',
            f'Map : {self.map_name}\n'
            f'Game length : {self.length}\n'
            f'Possibilities : {self.possibilities}\n'
            f'State : Ready to start!',
            color=KANAKO_COLOR)
    
    def join_user(self, user):
        users = self.users
        if user in users:
            description =  'You are already at the game'
        else:
            description = 'You successfully joined to the current game.'
            users.append(user)
            
            if len(users) == 10:
                description += '\n The game is full, starting.'
                self.waiter.set_result_if_pending(None)
        
        return description
    
    
    def leave_user(self, user):
        users = self.users
        try:
            index = users.index(user)
        except ValueError:
            description = 'You are not in the game.'
        else:
            if index == 0:
                if len(users) == 1:
                    self.cancelled = True
                    self.waiter.set_result_if_pending(None)
                    description = 'Game cancelled'
                else:
                    del users[0]
                    description = f'Left the game.\nLeadership given to { users[0].full_name}.'
            else:
                del users[0]
                description = 'Left the game.'
        
        return description

    
    def cancel_user(self, user):
        users = self.users
        leaders = users[0]
        if user is leaders:
            self.cancelled = True
            self.waiter.set_result_if_pending(None)
            description = 'Game cancelled'
        else:
            description = f'Only the leader can cancel the game: {leaders.full_name}'
        
        return description
    
    def start_user(self, user):
        users = self.users
        leaders = users[0]
        if user is leaders:
            self.waiter.set_result_if_pending(None)
            description = 'Game started'
        else:
            description = f'Only the leader can start the game: {leaders.full_name}'
        
        return description

class KanakoRunner:
    __slots__ = ('client', 'channel', 'users', 'map_name', 'length', 'possibilities', 'cancelled', 'waiter', 'history',
        'answers', 'map', 'romajis', 'options')
    def __new__(cls, join_waiter):
        self = object.__new__(cls)
        self.client = client = join_waiter.client
        self.channel = channel = join_waiter.channel
        self.users = join_waiter.users
        
        self.map_name = map_name = join_waiter.map_name
        self.length = join_waiter.length
        self.possibilities = possibilities = join_waiter.possibilities
        
        self.cancelled = False
        self.waiter = None
        
        self.history = []
        self.answers = {}
        
        full_map = MAPS[map_name].copy()
        limit = len(full_map)-1
        
        self.map = map_ = [full_map.pop(randint(0, limit)) for limit in range(limit, limit-self.length, -1)]
        if possibilities:
            romajis = {element[1] for element in map_}
        else:
            romajis = None
        
        self.romajis = romajis
        self.options = None
        
        ACTIVE_GAMES[channel.id] = self
        client.events.message_create.append(channel, self)
        Task(self.runner(), KOKORO)
        return self
    
    def generate_options(self, answer):
        result = [answer]
        target = answer
        ignore = [element.answer for element in self.history[-4:]]
        ignore.append(answer)
        chances = {romaji:randint(0,2) for romaji in self.romajis if romaji not in ignore}
        del ignore
        
        counter = 1
        while True:
            ln = len(target)
            if ln == 3 or 'j' in target:
                for key in chances:
                    if len(key) == 3 or 'j' in target:
                        chances[key] += 2
            else:
                for key in chances:
                    if len(key) in (1, 2) and 'j' not in target:
                        chances[key] += 1
            
            if target != 'n':
                for charD in target:
                    if charD in _pairsD:
                        break
                
                for charK in target:
                    if charK in _pairsK:
                        break
                
                chars = _pairsKx.get(key, None)
                
                if chars is None:
                    for key in chances:
                        if len(key) != ln:
                            continue
                        if charD in key:
                            chances[key] += 1
                        if charK in key:
                            chances[key] += 1
                else:
                    for key in chances:
                        if len(key)!=ln:
                            continue
                        if charD in key:
                            chances[key] += 1
                        if charK in key:
                            chances[key] += 1
                        if any_to_any(chars, key):
                            chances[key] += 1
            
            goods = []
            maximal = 1
            for key, value in chances.items():
                if value < maximal:
                    continue
                if value > maximal:
                    goods.clear()
                    maximal = value
                goods.append(key)
            
            target = goods[randint(0, len(goods)-1)]
            result.append(target)

            counter += 1
            if counter == self.possibilities:
                break
            
            del chances[target]
            
            for key in chances:
                chances[key] = randint(0,2)
            
        return [result.pop(randint(0, limit)) for limit in range(self.possibilities-1, -1, -1)]
    
    async def runner(self):
        client = self.client
        channel = self.channel
        answers = self.answers
        buffer = ReuBytesIO()
        embed = Embed(color=KANAKO_COLOR).add_image('attachment://guess_me.png').add_footer('')
        
        time_till_notify = CIRCLE_TIME-10
        
        for index, (question, answer) in enumerate(self.map, 1):
            embed.footer.text = f'{index} / {len(self.map)}'
            if self.possibilities:
                self.options = self.generate_options(answer)
                embed.description = '\n'.join([f'**{index}.: {value}**' for index, value in enumerate(self.options, 1)])
            
            try:
                await client.message_create(channel, embed=embed, file=('guess_me.png', draw(buffer, question)))
            except BaseException as err:
                self.cancel()
                if isinstance(err, ConnectionError):
                    return
                
                if isinstance(err, DiscordException):
                    if err.code in (
                            ERROR_CODES.unknown_channel, # channel deleted
                            ERROR_CODES.missing_access, # client removed
                            ERROR_CODES.missing_permissions, # permissions changed meanwhile
                                ):
                        return
                
                await client.events.error(client, f'{self.__class__.__name__}.runner', err)
                return
            
            circle_start = LOOP_TIME()
            self.waiter = waiter = Future(KOKORO)
            future_or_timeout(waiter, time_till_notify)
            
            try:
                await waiter
            except TimeoutError:
                Task(self.notify_late_users(), KOKORO)
                
                self.waiter = waiter = Future(KOKORO)
                future_or_timeout(waiter, 10)
                
                try:
                    await waiter
                except TimeoutError:
                    leavers = []
                    
                    users = self.users
                    
                    for index in reversed(range(len(users))):
                        user = users[index]
                        if user in answers:
                            continue
                        
                        leavers.append(user)
                        del users[index]
                        
                        for element in self.history:
                            del element.answers[index]
                    
                    if len(self.users) == 0:
                        self.cancel()
                        embed = Embed(None, 'No-one gave answer in time, cancelling the game.', color=KANAKO_COLOR)
                    else:
                        embed = Embed(None, '\n'.join(['Users timed out:', *(user.full_name for user in leavers)]),
                            color=KANAKO_COLOR)
                    
                    try:
                        await client.message_create(channel, embed=embed)
                    except BaseException as err:
                        self.cancel()
                        if isinstance(err, ConnectionError):
                            return
                        
                        if isinstance(err, DiscordException):
                            if err.code in (
                                    ERROR_CODES.unknown_channel, # channel deleted
                                    ERROR_CODES.missing_access, # client removed
                                    ERROR_CODES.missing_permissions, # permissions changed meanwhile
                                        ):
                                return
                        
                        await client.events.error(client, f'{self.__class__.__name__}.runner', err)
                        return
            
            if self.cancelled:
                return
            
            self.waiter = None
            
            element = HistoryElement()
            element.question= question
            element.answer  = answer
            element.options = self.options
            element.answers = [(value[0], value[1]-circle_start) for value in (answers[user.id] for user in self.users)]
            self.history.append(element)
            
            answers.clear()
            
            embed.title = f'Last answer: {answer}'
        
        self.cancel()
        
        embed = Embed(embed.title, color=KANAKO_COLOR)
        try:
            await client.message_create(channel, embed=embed)
        except BaseException as err:
            self.cancel()
            if isinstance(err, ConnectionError):
                return
            
            if isinstance(err, DiscordException):
                if err.code in (
                        ERROR_CODES.unknown_channel, # channel deleted
                        ERROR_CODES.missing_access, # client removed
                        ERROR_CODES.missing_permissions, # permissions changed meanwhile
                            ):
                    return
            
            await client.events.error(client, f'{self.__class__.__name__}.runner', err)
            return
        
        await GameStatistics(self)
    
    def cancel(self):
        if self.cancelled:
            return
        
        self.cancelled = True
        
        channel = self.channel
        self.client.events.message_create.remove(self.channel, self)
        
        channel_id = channel.id
        if ACTIVE_GAMES[channel_id] is self:
            del ACTIVE_GAMES[channel_id]
        
        waiter = self.waiter
        if (waiter is not None):
            waiter.set_result_if_pending()
    
    async def __call__(self, client, message):
        if message.author not in self.users:
            return
        
        waiter = self.waiter
        if (waiter is None):
            return
        
        if waiter.done():
            return
        
        if len(message.content) > 4:
            return
        
        if message.author.id in self.answers:
            return
        
        content = message.content.strip().lower()
        if self.possibilities:
            if content not in self.options:
                try:
                    index=int(content)
                except ValueError:
                    return
                else:
                    if index < 1 or index > self.possibilities:
                        return
                    index -= 1
                    content = self.options[index]
        
        self.answers[message.author.id] = (content, LOOP_TIME())
       
        if len(self.answers) == len(self.users):
            self.waiter.set_result_if_pending(None)
        
        try:
            await self.client.message_delete(message)
        except BaseException as err:
            self.cancel()
            if isinstance(err, ConnectionError):
                return
            
            if isinstance(err, DiscordException):
                if err.code in (
                        ERROR_CODES.unknown_message, # message deleted
                        ERROR_CODES.unknown_channel, # channel deleted
                        ERROR_CODES.missing_access, # client removed
                        ERROR_CODES.missing_permissions, # permissions changed meanwhile
                            ):
                    return
            
            await client.events.error(client, f'{self.__class__.__name__}.__call__', err)
            return
    
    
    async def notify_late_users(self):
        embed = Embed('Hurry! Only 10 seconds left!',
            '\n'.join([user.full_name for user in self.users if user.id not in self.answers]),
            color = KANAKO_COLOR)
        
        client = self.client
        try:
            await self.client.message_create(self.channel, embed=embed)
        except BaseException as err:
            self.cancel()
            if isinstance(err, ConnectionError):
                return
            
            if isinstance(err, DiscordException):
                if err.code in (
                        ERROR_CODES.unknown_channel, # channel deleted
                        ERROR_CODES.missing_access, # client removed
                        ERROR_CODES.missing_permissions, # permissions changed meanwhile
                            ):
                    return
            
            await client.events.error(client, f'{self.__class__.__name__}.notify_late_users', err)
            return
    
    def leave_user(self, user):
        users = self.users
        try:
            index = users.index(user)
        except ValueError:
            description = 'You are not part of the game.'
        else:
            if len(users) == 1:
                self.cancel()
                
                description = 'No more users in the game, cancelling.'
            else:
                description = f'{user.full_name} left the game.'
                del users[index]
                for element in self.history:
                    del element.answers[index]
                
                answers = self.answers
                try:
                    del answers[user.id]
                except KeyError:
                    pass
                else:
                    if len(answers) == len(users):
                        waiter = self.waiter
                        if (waiter is not None):
                            self.waiter.set_result_if_pending(None)
        
        return description


class GameStatistics:
    __slots__ = ('cache', 'source',)
    
    def __len__(self):
        return len(self.cache)
    
    def __new__(cls,source):
        self = object.__new__(cls)
        self.source = source
        self.cache = [None for _ in range((len(self.source.history)+9)//10+1)]
        self.create_page_0()
        #we return a coro, so it is valid ^.^
        return KanakoPagination(source.client, source.channel, self)

    def create_page_0(self):
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
                value, time = answers[index]
                if value == answer:
                    win_counts[index] += 1
                    win_times[index].append(time)
                    if time < first_time:
                        first_time = time
                        first_index = index
                        first_won = True
                else:
                    lose_counts[index] += 1
                    lose_times[index].append(time)
                    if time < first_time:
                        first_time = time
                        first_index = index
                        first_won = False
                        
            if first_time != CIRCLE_TIME:
                if first_won:
                    win_firsts[first_index] += 1
                else:
                    lose_firsts[first_index] += 1

        win_medians = [value[len(value)//2] if value else CIRCLE_TIME for value in win_times]
        lose_medians = [value[len(value)//2] if value else CIRCLE_TIME for value in lose_times]
        
        embed = Embed('Statistics', color=KANAKO_COLOR)
        
        for index, user in enumerate(self.source.users):
            win_count = win_counts[index]
            lose_count = lose_counts[index]
            win_median = win_medians[index]
            lose_median = lose_medians[index]
            win_first = win_firsts[index]
            lose_first = lose_firsts[index]

            total = float(win_count)
            total += (((2**.5)-1.)-((((CIRCLE_TIME+win_median)/CIRCLE_TIME)**.5)-1.))*win_count
            total += win_first/5.
            total -= (((2**.5)-1.)-((((CIRCLE_TIME+lose_median)/CIRCLE_TIME)**.5)-1.))*lose_count*2.
            total -= lose_first/2.5
            
            embed.add_field(f'{user:f} :',
                f'Correct answers : {win_count}\n'
                f'Bad answers : {lose_count}\n'
                f'Good answer time median : {win_median:.2f} s\n'
                f'Bad answer time median : {lose_median:.2f} s\n'
                f'Answered first: {win_first} GOOD / {lose_first} BAD\n'
                f'Rated : {total:.2f}'
                    )
        
        embed.add_footer(f'Page 1 /  {len(self.cache)}')
        
        self.cache[0] = embed

    def __getitem__(self,index):
        page = self.cache[index]
        if page is None:
            return self.create_page(index)
        return page

    def create_page(self,index):
        end = index*10
        start = end-9
        if end > len(self.source.history):
            end = len(self.source.history)

        shard = []
        embed = Embed('Statistics',f'{start} - {end}', color=KANAKO_COLOR)
        
        add_options = self.source.possibilities
        
        for question_index,element in enumerate(self.source.history[start-1:end],start):
            shard.append('```diff')
            if add_options:
                shard.append('\n')
                shard.append(', '.join([f'{index}. : {option}' for index, option in enumerate(element.options, 1)]))
            for user_index, user in enumerate(self.source.users):
                value,time=element.answers[user_index]
                shard.append(f'\n{"+" if element.answer==value else "-"} {user:f} : {value} ( {time:.2f} s )')
            shard.append('\n```')
            embed.add_field(f'{question_index}.: {element.question} - {element.answer}', ''.join(shard))
            shard.clear()
        
        embed.add_footer(f'Page {index+1} / {len(self.cache)}')
        
        self.cache[index] = embed
        return embed

class KanakoPagination:
    LEFT2   = BUILTIN_EMOJIS['rewind']
    LEFT    = BUILTIN_EMOJIS['arrow_backward']
    RIGHT   = BUILTIN_EMOJIS['arrow_forward']
    RIGHT2  = BUILTIN_EMOJIS['fast_forward']
    RESET   = BUILTIN_EMOJIS['arrows_counterclockwise']
    EMOJIS  = (LEFT2, LEFT, RIGHT, RIGHT2, RESET)
    
    __slots__ = ('canceller', 'channel', 'client', 'message', 'page', 'pages', '_task_flag', '_timeouter')
    
    async def __new__(cls, client, event_or_channel, pages):
        if isinstance(event_or_channel, InteractionEvent):
            target_channel = event_or_channel.channel
            is_interaction = True
        else:
            target_channel = event_or_channel
            is_interaction = False
        
        self = object.__new__(cls)
        self.client = client
        self.channel = target_channel
        self.pages = pages
        self.page = 0
        self.canceller = cls._canceller
        self._task_flag = GUI_STATE_READY
        self._timeouter = None
        self.message = None
        
        
        if is_interaction:
            if event_or_channel.is_unanswered():
                await client.interaction_application_command_acknowledge(event_or_channel)
            
            message = await client.interaction_followup_message_create(event_or_channel, embed=pages[0])
        
        else:
            message = await client.message_create(target_channel, embed=pages[0])
        
        self.message = message
        
        if not target_channel.cached_permissions_for(client).can_add_reactions:
            return self
        
        if len(pages)>1:
            for emoji in self.EMOJIS:
                await client.reaction_add(message,emoji)
        
        
        client.events.reaction_add.append(message, self)
        client.events.reaction_delete.append(message, self)
        self._timeouter = Timeouter(self, timeout=150)
        return self
    
    async def __call__(self, client, event):
        if event.user.is_bot or (event.emoji not in self.EMOJIS):
            return
        
        message = self.message
        
        if (event.delete_reaction_with(client) == event.DELETE_REACTION_NOT_ADDED):
            return
        
        task_flag = self._task_flag
        if task_flag != GUI_STATE_READY:
            # ignore GUI_STATE_SWITCHING_PAGE, GUI_STATE_CANCELLED and GUI_STATE_SWITCHING_CTX
            return
        
        emoji = event.emoji
        while True:
            if emoji is self.LEFT:
                page = self.page-1
                break
                
            if emoji is self.RIGHT:
                page = self.page+1
                break
                
            if emoji is self.RESET:
                page = 0
                break
                
            if emoji is self.LEFT2:
                page = self.page-10
                break
                
            if emoji is self.RIGHT2:
                page = self.page+10
                break
                
            return
        
        if page < 0:
            page = 0
        elif page >= len(self.pages):
            page = len(self.pages)-1
        
        if self.page == page:
            return

        self.page = page
        self._task_flag = GUI_STATE_SWITCHING_PAGE
        try:
            await client.message_edit(message, embed=self.pages[page])
        except BaseException as err:
            self._task_flag = GUI_STATE_CANCELLED
            self.cancel()
            
            if isinstance(err, ConnectionError):
                # no internet
                return
            
            if isinstance(err, DiscordException):
                if err.code in (
                        ERROR_CODES.missing_access, # client removed
                        ERROR_CODES.unknown_message, # message already deleted
                            ):
                    return
            
            # We definitely do not want to silence `ERROR_CODES.invalid_form_body`
            await client.events.error(client, f'{self!r}.__call__', err)
            return
        
        self._task_flag=GUI_STATE_READY
        
        self._timeouter.set_timeout(10)
    
    async def _canceller(self, exception):
        client = self.client
        message = self.message
        
        client.events.reaction_add.remove(message, self)
        client.events.reaction_delete.remove(message, self)
        
        if self._task_flag == GUI_STATE_SWITCHING_CTX:
            # the message is not our, we should not do anything with it.
            return

        self._task_flag = GUI_STATE_CANCELLED
        
        if exception is None:
            return
        
        if isinstance(exception, TimeoutError):
            if self.channel.cached_permissions_for(client).can_manage_messages:
                try:
                    await client.reaction_clear(message)
                except BaseException as err:
                    
                    if isinstance(err, ConnectionError):
                        # no internet
                        return
                    
                    if isinstance(err,DiscordException):
                        if err.code in (
                                ERROR_CODES.missing_access, # client removed
                                ERROR_CODES.unknown_message, # message deleted
                                ERROR_CODES.missing_permissions, # permissions changed meanwhile
                                    ):
                            return
                    
                    await client.events.error(client,f'{self!r}._canceller',err)
                    return
            return
        
        timeouter = self._timeouter
        if timeouter is not None:
            self._timeouter = None
            timeouter.cancel()
        #we do nothing
    
    def cancel(self, exception=None):
        canceller = self.canceller
        if canceller is None:
            return
        
        self.canceller = None
        
        timeouter = self._timeouter
        if timeouter is not None:
            self._timeouter = None
            timeouter.cancel()
        
        return Task(canceller(self, exception), KOKORO)


del BUILTIN_EMOJIS
del Color
