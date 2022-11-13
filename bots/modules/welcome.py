__all__ = ()

import re
from hata import Client, Guild, mention_user_by_id, Embed
from hata.ext.slash import Button, ButtonStyle
from random import choice

Satori: Client
Koishi: Client

WELCOME_GUILD = Guild.precreate(580138631205748813)

WELCOME_IMAGES = [
    'https://cdn.discordapp.com/attachments/648135460563976202/950293342690873414/FNFEfKbaIAELnJ8.jpg',
    'https://cdn.discordapp.com/attachments/648135460563976202/948308150853992498/koishi-0116.jpg',
    'https://cdn.discordapp.com/attachments/648135460563976202/945643679429832724/IMG_20220222_174454.jpg',
]

WELCOME_MESSAGES = [
    'Roses are red, also blue, {0} joined this server with Mr. Hat too',
    'Koooosh. {0} just landed.',
    '{0} just joined. Everyone, watch your back!',
    'Welcome, {0}. We hope you brought shrimp fry.',
    'Where’s {0}? RIGHT BEHIND YOU!',
    'Heart throbbing {0} showed up!',
    'It\'s a youkai! It\'s a fairy! Nevermind, it\'s just {0}.',
    'We\'ve been already behind you {0}',
    'It\'s {0}! Praise Mr. Unconsciousness! [T]/',
    'Always gonna love {0}. Always gonna remember {0}.',
    '{0} is here to stab and eat shrimp fry. And {0} is all out of shrimp fry.',
    '{0} is behind me... or are they?',
    '{0} just showed up. Hold my fishing rod.',
    'A lovely {0} chan appeared.',
    '{0} just joined. Can I get a croissant?',
    'Mr. Hat owner {0}',
    '{0} is here, as the Mr. Hat foretold.',
    '{0} just arrived. Seems adorable - please love.',
    'Moshi Moshi?. Is it {0} you\'re calling?',
    'The creature {0} showed up!',
    'Ready to stop thinking, {0}?',
    '{0} has joined the server! It\'s a fumo!',
    '{0} just joined the server - *staaaare*',
    '{0} just joined. Everyone, stop thinking!',
    'Welcome, {0}. Bring shrimp fry and croissant.',
    'Satoooori, {0} is here!',
    '{0} has arrived. The dinner just started.',
    'Welcome, {0}. Stay awhile and fish with us.',
    'Welcome {0}. Leave your Mr. Knife by the door.',
    '{0} joined. Mr. Hat helps them relax.',
    '{0} just arrived. Seems conscious - please nerf.',
    '{0} has joined the Extra stage.',
    'Hey! Listen! {0} has called!',
    '{0} hopped into the server. My face is butter!!',
    '{0} just flew into the server.',
    'Yay! {0} just landed.',
    '{0} joined. You must collect additional **P**ower items.',
]

@Satori.events
async def guild_user_add(client, guild, user):
    if guild is not WELCOME_GUILD:
        return
    
    system_channel_id = guild.system_channel_id
    if not system_channel_id:
        return
    
    await Koishi.message_create(
        system_channel_id,
        choice(WELCOME_MESSAGES).format(user.name),
        components = Button(
            'Welcome them!',
            custom_id = f'welcome.{user.id}.create_response_message',
            style = ButtonStyle.green,
        )
    )


@Koishi.interactions(custom_id = re.compile(f'welcome\.(\d+)\.create_response_message'))
async def welcome_user(client, event, user_id):
    yield
    
    channel_id = event.channel_id
    executor_webhook = await client.webhook_get_own_channel(channel_id)
    if (executor_webhook is None):
        executor_webhook = await client.webhook_create(channel_id, 'welcomer')
    
    await client.webhook_message_create(
        executor_webhook,
        mention_user_by_id(user_id),
        embed = Embed(color = 3092790).add_image(choice(WELCOME_IMAGES)),
        name = event.user.name_at(event.guild_id),
        avatar_url = event.user.avatar_url_at_as(event.guild_id, size = 4096)
    )
