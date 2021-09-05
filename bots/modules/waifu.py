from itertools import chain

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
    key: [] for key in chain(
        ((waifu_type, True) for waifu_type in SFW_WAIFUS),
        ((waifu_type, False) for waifu_type in NSFW_WAIFUS),
    )
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
            user : ('user', 'Who to hug?') = None,
                ):
        guild_id = event.guild_id
        if not guild_id:
            abort('Guild only command')
        
        url = await get_waifu_image(client, event, self.name, True, self.cache)
        if url is None:
            abort('*Could not get any images, please try again later.*')
        
        if user is None:
            hugger = client
            hugged = event.user
        else:
            hugger = event.user
            hugged = user
        
        title = f'{hugger:f} {self.verb} {hugged:f}.'
        
        return Embed(title, color=(event.id>>22)&0xffffff).add_image(url)


for action_name, action_verb, action_description in (
        ('pat', 'pats', 'Do you like pats as well?'),
        ('kiss', 'kisses', 'If you really really like your onee, give her a kiss <3'),
        ('hug', 'hugs', 'Huh.. Huggu? HUGG YOUUU!!!'),
        ('cuddle', 'cuddles', 'Come here, you little qtie pie.'),
        ('lick', 'licks', 'Licking is a favored activity of cat girls.'),
        ('poke', 'pokes', 'It hurts!'),
        ('slap', 'slaps', 'Slapping others is not nice.'),
        ('smug', 'smugs at', 'SMug face.'),
        ('bully', 'bullies', 'No Bully!'),
        ('cry', 'cries because of', 'THe saddest.'),
        ('yeet', 'yeets', 'Yeet!'),
        ('blush', 'blushes at', 'Oh.'),
        ('smile', 'smiles at', 'Oh, really?'),
        ('wave', 'waves at', 'Flap flap'),
        ('highfive', 'gives highfive for', 'Lets go boiz!'),
        ('handhold', 'holds hands of', 'Lewd!!'),
        ('nom', 'noms', 'Feed your loli, or else'),
        ('bite', 'bites', 'Vampy.'),
        ('glomp', 'glomps', 'You can rn, but you cant hide!'),
        ('kill', 'murders', 'Finally, some action.'),
        ('happy', 'is happy for', 'If you are happy, clap your..'),
        ('wink', 'winks at', 'Ara-ara'),
        ('dance', 'dancing with', 'Dancy, dancy.'),
        ('cringe', 'cringes at', 'Cringe, run!'),
            ):
    SLASH_CLIENT.interactions(
        Action(action_name, action_verb),
        name = action_name,
        description = action_description,
        is_global = True,
    )

del action_name, action_verb, action_description
