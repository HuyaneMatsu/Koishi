from hata import Client
from hata.backend.headers import CONTENT_TYPE
from hata import imultidict, un_map_pack, Task, KOKORO, WaitTillAll, sanitize_mentions, Embed

from hata.ext.slash import abort

SLASH_CLIENT: Client

WAIFU_API_BASE_URL = 'https://api.waifu.pics'

HEADERS = imultidict()
HEADERS[CONTENT_TYPE] = 'application/json'

SFW_WAIFUS = [
    'waifu',
    'neko',
    'shinobu',
    'megumin',
]

NSFW_WAIFUS = [
    'waifu',
    'neko',
    'trap',
]


WAIFU_CACHE_BY_KEY = {
    **un_map_pack(((waifu_type, True), []) for waifu_type in SFW_WAIFUS),
    **un_map_pack(((waifu_type, False), []) for waifu_type in NSFW_WAIFUS),
}


async def request_image(client, endpoint, safe, cache):
    url = f'{WAIFU_API_BASE_URL}/many/{"" if safe else "n"}sfw/{endpoint}'
    async with client.http.post(url, headers=HEADERS, data=b'{}') as response:
        if response.status == 200:
            data = await response.json()
        else:
            data = None
    
    if (data is not None):
        try:
            files = data['files']
        except KeyError:
            pass
        else:
            cache.extend(files)
            
            if cache:
                return cache.pop()


async def get_waifu_image(client, event, endpoint, safe, cache):
    if cache:
        return cache.pop()
    
    acknowledge_task = Task(client.interaction_application_command_acknowledge(event), KOKORO)
    request_task = Task(request_image(client, endpoint, safe, cache), KOKORO)
    
    await WaitTillAll([acknowledge_task, request_task], KOKORO)
    
    try:
        acknowledge_task.result()
    except:
        request_task.cancel()
        raise
    
    return request_task.result()

WAIFU = SLASH_CLIENT.interactions(None,
    name = 'Waifu',
    description = 'Waifu pictures!',
    is_global = True,
)

@WAIFU.interactions(is_default=True)
async def sfw(client, event,
        type_ : (SFW_WAIFUS, 'Waifu type!') = SFW_WAIFUS[0],
            ):
    """Safe working waifu."""
    guild_id = event.guild_id
    if not guild_id:
        abort('Guild only command')
    
    url = await get_waifu_image(client, event, type_, True, WAIFU_CACHE_BY_KEY[(type_, True)])
    if url is None:
        abort('*Could not get any images, please try again later.*')
    
    return url


@WAIFU.interactions
async def nsfw(client, event,
        type_ : (NSFW_WAIFUS, 'Waifu type!') = NSFW_WAIFUS[0],
            ):
    """Waifu with extras!"""
    guild_id = event.guild_id
    if not guild_id:
        abort('Guild only command')
    
    if not event.channel.nsfw:
        abort('Nsfw channel only!')
    
    url = await get_waifu_image(client, event, type_, False, WAIFU_CACHE_BY_KEY[(type_, False)])
    if url is None:
        abort('*Could not get any images, please try again later.*')
    
    return url


class Action:
    __slots__ = ('cache', 'name', 'verb')
    def __init__(self, name, verb):
        self.name = name
        self.verb = verb
        self.cache = []
    
    async def __call__(self, client, event,
            message : ('str', 'Additional message to send?') = None,
                ):
        guild_id = event.guild_id
        if not guild_id:
            abort('Guild only command')
        
        url = await get_waifu_image(client, event, self.name, True, self.cache)
        if url is None:
            abort('*Could not get any images, please try again later.*')
        
        user = event.user
        try:
            guild_profile = user.guild_profiles[guild_id]
        except KeyError:
            user_name = user.name
        else:
            user_name = guild_profile.nick
            if (user_name is None):
                user_name = user.name
        
        
        if message is None:
            try:
                guild_profile = client.guild_profiles[guild_id]
            except KeyError:
                client_name = client.name
            else:
                client_name = guild_profile.nick
                if (client_name is None):
                    client_name = client.name
            
            first_word = client_name
            last_word = user_name
        
        else:
            message = sanitize_mentions(message, event.guild)
            # Security goes brrr
            if len(message) > 200:
                message = message[:200] + '...'
            
            first_word = user_name
            last_word = message
        
        title = f'{first_word} {self.verb} {last_word}.'
        
        return Embed(title, color=(event.id>>22)&0xffffff).add_image(url)


for action_name, action_verb, action_description in (
        ('pat', 'pats', 'Do you like pats as well?'),
        ('kiss', 'kisses', 'If you really really like your onee, give her a kiss <3'),
        ('hug', 'hugs', 'Huh.. Huggu? HUGG YOUUU!!!'),
        ('cuddle', 'cuddles', 'Come here, you little qtie pie.'),
        ('lick', 'licks', 'Licking is a favored activity of cat girls.'),
        ('poke', 'pokes', 'It hurts!'),
        ('slap', 'slap', 'Slapping others is not nice.'),
        ('smug', 'smugs', 'SMug face.'),
        ('bully', 'bullies', 'No Bully!'),
        ('cry', 'cries', 'THe saddest.'),
        ('yeet', 'yeets', 'Yeet!'),
        ('blush', 'blushes', 'Oh.'),
        ('smile', 'smiles', 'Oh, really?'),
        ('wave', 'waves', 'Flap flap'),
        ('highfive', 'highfives', 'Lets go boiz!'),
        ('handhold', 'holds hand', 'Lewd!!'),
        ('nom', 'noms', 'Feed your loli, or else'),
        ('bite', 'bites', 'Vampy.'),
        ('glomp', 'glomps', 'You can rn, but you cant hide!'),
        ('kill', 'murders', 'Finally, some action.'),
        ('happy', 'is happy for', 'If you are happy, clap your..'),
        ('wink', 'winks', 'Ara-ara'),
        ('dance', 'dances', 'Dancy, dancy.'),
        ('cringe', 'cringes', 'Cringe, run!'),
            ):
    SLASH_CLIENT.interactions(
        Action(action_name, action_verb),
        name = action_name,
        description = action_description,
        is_global = True,
    )

del action_name, action_verb, action_description
