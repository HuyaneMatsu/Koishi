from scarletio import Task, sleep
from hata import Client, Sticker, KOKORO, Emoji, parse_emoji, Guild
from bot_utils.constants import GUILD__SUPPORT, CHANNEL__SUPPORT__SYSTEM
from hata.ext.slash import Button
from random import random, choice

Satori: Client
Koishi: Client

WELCOME_GUILD = Guild.precreate(580138631205748813)


CUSTOM_ID_WELCOME = 'welcome.create_response_message'

BUTTON_WELCOME = Button(
    'Welcome them',
    custom_id = CUSTOM_ID_WELCOME
)

@Satori.events
async def guild_user_add(client, guild, user):
    if guild is not WELCOME_GUILD:
        return
    
    system_channel_id = guild.system_channel_id
    if not system_channel_id:
        return
    
    await Koishi.message_create(
        system_channel_id,
        f'{user:f} just joined {guild}!',
        components = BUTTON_WELCOME,
    )


@Koishi.interactions(custom_id=CUSTOM_ID_WELCOME)
async def welcome_user(client, event):
    await client.interaction_response_message_create(event, 'Welcome')
