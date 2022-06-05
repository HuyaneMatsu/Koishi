__all__ = ()

from hata import Client, BUILTIN_EMOJIS
from hata import Embed, KOKORO
from scarletio import Task, WaitTillAll

from hata.ext.slash import InteractionResponse, Button

SLASH_CLIENT: Client

MEEK_API_URL = 'https://api.meek.moe/'
ERROR_MESSAGE_NO_VOCALOID = '*Could not get any images, please try again later.*'
PROVIDER_FOOTER = 'Images provided by meek.moe'

VOCALOID_CHARACTERS = {
    'Aoki': 'aoki',
    'Diva': 'diva',
    'Fukase': 'fukase',
    'Gumi': 'gumi',
    'IA': 'ia',
    'Kaito': 'kaito',
    'Len': 'len',
    'Lily': 'lily',
    'Luka': 'luka',
    'Mayu': 'mayu',
    'Meiko': 'meiko',
    'Miki': 'miki',
    'Miku': 'miku',
    'Rin': 'rin',
    'Teto': 'teto',
    'Una': 'una',
    'Yukari': 'yukari',
    'ZOLA': 'zola',
}

VOCALOID_CHARACTER_TO_FULL_NAME = {
    'aoki': 'Aoki Lapis',
    'diva': 'ProjectDiva',
    'fukase': 'Fukase',
    'gumi': 'Gumi',
    'ia': 'IA',
    'kaito': 'Kaito',
    'len': 'Kagamine Len',
    'lily': 'Lily',
    'luka': 'Megurine Luka',
    'mayu': 'Mayu',
    'meiko': 'Meiko',
    'miki': 'SFA2 Miki',
    'miku': 'Hatsune Miku',
    'rin': 'Kagamine Rin',
    'teto': 'Kasane Teto',
    'una': 'Otomachi Una',
    'yukari': 'Yuzuki Yukari',
    'zola': 'ZOLA',
}

ACKNOWLEDGE_APPLICATION_COMMAND_INTERACTION_FUNCTION = Client.interaction_application_command_acknowledge
ACKNOWLEDGE_COMPONENT_INTERACTION_FUNCTION = Client.interaction_component_acknowledge

EMOJI_NEW = BUILTIN_EMOJIS['arrows_counterclockwise']

async def request_image(client, endpoint):
    url = f'{MEEK_API_URL}{endpoint}'
    async with client.http.get(url)as response:
        if response.status == 200:
            data = await response.json()
            url = data['url']
        
        else:
            url = None
    
    return url


async def get_vocaloid_image(client, event, character, is_component):
    if is_component:
        acknowledge_function = ACKNOWLEDGE_COMPONENT_INTERACTION_FUNCTION
    else:
        acknowledge_function = ACKNOWLEDGE_APPLICATION_COMMAND_INTERACTION_FUNCTION
    
    acknowledge_task = Task(acknowledge_function(client, event), KOKORO)
    request_task = Task(request_image(client, character), KOKORO)
    
    await WaitTillAll([acknowledge_task, request_task], KOKORO)
    
    try:
        acknowledge_task.result()
    except:
        request_task.cancel()
        raise
    
    return request_task.result()


@SLASH_CLIENT.interactions(is_global=True)
async def vocaloid(
    client,
    event,
    character: (VOCALOID_CHARACTERS, 'Select a character!') = 'miku',
):
    url = await get_vocaloid_image(client, event,character, False)
    name = VOCALOID_CHARACTER_TO_FULL_NAME[character]
    
    if url is None:
        return Embed(name, ERROR_MESSAGE_NO_VOCALOID)
    

    return InteractionResponse(
        embed = Embed(name, url=url).add_image(url).add_footer(PROVIDER_FOOTER),
        components = Button(
            emoji = EMOJI_NEW,
            custom_id = f'vocaloid_image.meek_moe.{character}',
        )
    )

class NewVocaloid:
    __slots__ = ('character', 'name',)
    
    def __init__(self, character, name):
        self.character = character
        self.name = name
    
    async def __call__(self, client, event):
        if event.user is not event.message.interaction.user:
            return
        
        url = await get_vocaloid_image(client, event, self.character, True)
        
        if url is None:
            source_embed = event.message.embed
            if source_embed is None:
                # Should not happen
                embed = Embed(self.name, ERROR_MESSAGE_NO_VOCALOID).add_footer(PROVIDER_FOOTER)
            else:
                embed = Embed(source_embed.title, ERROR_MESSAGE_NO_VOCALOID, url=source_embed.url)
                embed.image = source_embed.image
                embed.add_footer(PROVIDER_FOOTER)
                
        else:
            embed = Embed(self.name, url=url).add_image(url).add_footer(PROVIDER_FOOTER)
        
        return embed

for vocaloid_character, vocaloid_name in VOCALOID_CHARACTER_TO_FULL_NAME.items():
    SLASH_CLIENT.interactions(
        NewVocaloid(vocaloid_character, vocaloid_name),
        custom_id = f'vocaloid_image.meek_moe.{vocaloid_character}',
    )

del vocaloid_character, vocaloid_name
