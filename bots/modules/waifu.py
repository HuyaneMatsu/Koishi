# -*- coding: utf-8 -*-
from hata import Client, Embed
from hata.backend.headers import CONTENT_TYPE
from hata import imultidict

SLASH_CLIENT : Client

WAIFU_API_BASE_URL = 'https://waifu.pics/api'

HEADERS = imultidict()
HEADERS[CONTENT_TYPE] = 'application/json'

WAIFU_CACHE_BY_KEY = {}

ACTIONS = [
    'pat',
    'kiss',
    'hug',
    'cuddle',
    'lick',
    'poke',
    'slap',
    'smug',
    'bully',
    'cry',
    'yeet',
    'blush',
    'smile',
    'wave',
    'highfive',
    'handhold',
    'nom',
    'bite',
    'glomp',
    'kill',
    'happy',
    'wink',
    'dance',
    'cringe',
        ]

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

async def get_waifu_image(client, event, endpoint, safe):
    guild = event.guild
    if guild is None:
        yield Embed('Error', 'Guild only command.')
        return
    
    if guild not in client.guild_profiles:
        yield Embed('Error', 'I must be in the guild execute this command.')
        return
    
    if (not safe) and (not event.channel.nsfw):
        yield Embed('Ohoho', 'Nsfw channel only!')
        return
    
    key = (endpoint, safe)
    try:
        cache = WAIFU_CACHE_BY_KEY[key]
    except KeyError:
        cache = WAIFU_CACHE_BY_KEY[key] = []
    else:
        if cache:
            yield cache.pop()
            return
    
    yield
    
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
                yield cache.pop()
                return
    
    yield '*Could not get any images, please try again later.*'
    return


@SLASH_CLIENT.interactions(description='Uwaaaaa!!', is_global=True)
async def action(client, event,
        action : ([(x, x) for x in ACTIONS], 'What should I do?'),
            ):
    """Please do nice things."""
    return get_waifu_image(client, event, action, True)


WAIFU = SLASH_CLIENT.interactions(None,
    name = 'Waifu',
    description = 'Waifu pictures!',
    is_global = True,
        )

@WAIFU.interactions(is_default=True)
async def sfw(client, event,
        type_ : ([(x, x) for x in SFW_WAIFUS], 'Waifu type!') = SFW_WAIFUS[0],
            ):
    """Safe working waifu."""
    return get_waifu_image(client, event, type_, True)


@WAIFU.interactions
async def nsfw(client, event,
        type_ : ([(x, x) for x in NSFW_WAIFUS], 'Waifu type!') = NSFW_WAIFUS[0],
            ):
    """Waifu with extras!"""
    return get_waifu_image(client, event, type_, False)
