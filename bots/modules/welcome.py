from scarletio import Task, sleep
from hata import Client, Sticker, KOKORO, Emoji, parse_emoji
from bot_utils.constants import GUILD__SUPPORT, CHANNEL__SUPPORT__SYSTEM
from random import random, choice

Satori: Client
Koishi: Client

STICKER__WELCOME = Sticker.precreate(914216876819767347)

WELCOME_EMOJI_ANIMATED = Emoji.precreate(648173118392762449)
WELCOME_EMOJI_STATIC = Emoji.precreate(767445550378254366)
WELCOME_EMOJI_ALTERNATIVE = Emoji.precreate(772496201642934272)


async def auto_welcome_interaction_0():
    await Koishi.typing(CHANNEL__SUPPORT__SYSTEM)
    await sleep(0.5 + random() * 2.0)
    await Koishi.message_create(CHANNEL__SUPPORT__SYSTEM, f'Welcome to KW!')

async def auto_welcome_interaction_1():
    await Koishi.typing(CHANNEL__SUPPORT__SYSTEM)
    await sleep(1.0 + random() * 2.0)
    await Koishi.message_create(CHANNEL__SUPPORT__SYSTEM, f'Welcome to KW {WELCOME_EMOJI_STATIC}')


async def auto_welcome_interaction_2():
    await Koishi.typing(CHANNEL__SUPPORT__SYSTEM)
    await sleep(1.0 + random() * 1.0)
    await Koishi.message_create(CHANNEL__SUPPORT__SYSTEM, f'Welcome to KW')
    await sleep(0.5 + random() * 1.0)
    await Koishi.message_create(CHANNEL__SUPPORT__SYSTEM, WELCOME_EMOJI_ANIMATED)


async def auto_welcome_interaction_3():
    await Koishi.typing(CHANNEL__SUPPORT__SYSTEM)
    await sleep(1.0 + random() * 1.0)
    await Koishi.message_create(CHANNEL__SUPPORT__SYSTEM, f'Welcome to KW')
    await sleep(0.5 + random() * 1.0)
    await Koishi.message_create(CHANNEL__SUPPORT__SYSTEM, WELCOME_EMOJI_STATIC)


async def auto_welcome_interaction_4():
    await Koishi.typing(CHANNEL__SUPPORT__SYSTEM)
    await sleep(1.0 + random() * 2.0)
    await Koishi.message_create(CHANNEL__SUPPORT__SYSTEM, f'Welcome qtie!')
    await sleep(0.5 + random() * 1.0)
    await Koishi.message_create(CHANNEL__SUPPORT__SYSTEM, WELCOME_EMOJI_ALTERNATIVE)


AUTO_WELCOME_INTERACTIONS = [
    auto_welcome_interaction_0,
    auto_welcome_interaction_1,
    auto_welcome_interaction_2,
    auto_welcome_interaction_3,
    auto_welcome_interaction_4,
]


class WelcomeState:
    __slots__ = ('users', 'auto_welcome_handle', 'last_join', 'welcome_count')
    
    def __init__(self):
        self.users = set()
        self.auto_welcome_handle = None
        self.welcome_count = 0
    
    
    def cancel(self):
        auto_welcome_handle = self.auto_welcome_handle
        if (auto_welcome_handle is not None):
            self.auto_welcome_handle = None
            auto_welcome_handle.cancel()
        
        self.users.clear()
        self.welcome_count = 0
    
    
    def maybe_start_auto_welcome_handler(self):
        auto_welcome_handle = self.auto_welcome_handle
        if (auto_welcome_handle is None):
            self.auto_welcome_handle = KOKORO.call_later(
                900.0 * random(),
                call_auto_welcome,
                [user.id for user in self.users],
            )
    
    
    def call_auto_welcome(self, user_ids):
        for user in self.users:
            if user.id in user_ids:
                self.cancel()
                Task(self.auto_welcome(), KOKORO)
    
    
    async def auto_welcome(self):
        await choice(AUTO_WELCOME_INTERACTIONS)
    
    
    def feed_user(self, user):
        self.users.add(user)
        self.maybe_start_auto_welcome_handler()
    
    
    def take_user(self, user):
        users = self.users
        try:
            users.remove(user)
        except KeyError:
            pass
        else:
            if not users:
                self.cancel()
    
    
    async def feed_message(self, message):
        if not self.users:
            return
        
        if message.author.is_bot:
            return
        
        if message.has_sticker():
            self.cancel()
            return
        
        content = message.content
        if content is None:
            return
        
        emoji = parse_emoji(content)
        if (emoji is not None) and 'wave' in emoji.name.casefold():
            self.welcome_count += 1
        else:
            if 'welcome' in content.casefold():
                self.welcome_count += 1
        
        if random() * self.welcome_count ** 0.5 >= 1.4:
            self.cancel()
            await Koishi.typing(CHANNEL__SUPPORT__SYSTEM)
            await sleep(0.5 + random() * 2.5)
            await Koishi.message_create(CHANNEL__SUPPORT__SYSTEM, sticker=STICKER__WELCOME)


WELCOME_STATE = WelcomeState()


@Satori.events
async def guild_user_add(client, guild, user):
    if guild is not GUILD__SUPPORT:
        return
    
    
    WELCOME_STATE.feed_user(user)


@Satori.events
async def guild_user_delete(client, guild, user):
    if guild is not GUILD__SUPPORT:
        return
    
    WELCOME_STATE.take_user(user)


async def welcome_counter(client, message):
    await WELCOME_STATE.feed_message(message)


def call_auto_welcome(user_ids):
    WELCOME_STATE.call_auto_welcome(user_ids)


def setup(lib):
    Satori.events.message_create.append(CHANNEL__SUPPORT__SYSTEM, welcome_counter)


def teardown(lib):
    Satori.events.message_create.remove(CHANNEL__SUPPORT__SYSTEM, welcome_counter)
    WELCOME_STATE.cancel()
