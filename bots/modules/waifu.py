__all__ = ()

from itertools import chain
from random import random

from hata import Client, BUILTIN_EMOJIS
from scarletio.web_common.headers import CONTENT_TYPE
from hata import Embed, KOKORO, Emoji
from scarletio import IgnoreCaseMultiValueDictionary, Task, WaitTillAll
from hata.ext.slash import abort, InteractionResponse, Button

SLASH_CLIENT: Client

WAIFU_API_BASE_URL = 'https://api.waifu.pics'
PROVIDER_FOOTER = 'Images provided by waifu.pics'
EMOJI_FLUSHED = Emoji.precreate(965960651853926480)

HEADERS = IgnoreCaseMultiValueDictionary()
HEADERS[CONTENT_TYPE] = 'application/json'

SFW_WAIFUS = [
    'waifu',
    'neko',
    'awoo',
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

EMOJI_NEW = BUILTIN_EMOJIS['arrows_counterclockwise']
ERROR_MESSAGE_NO_WAIFU = '*Could not get any images, please try again later.*'


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

async def get_waifu_image(client, event, endpoint, safe, cache, is_component, acknowledge_message, allowed_mentions):
    if cache:
        return cache.pop()
    
    if is_component:
        coroutine = client.interaction_component_acknowledge(event, wait=False)
    elif (acknowledge_message is None):
        coroutine = client.interaction_application_command_acknowledge(event, wait=False)
    else:
        coroutine = client.interaction_response_message_create(
            event, acknowledge_message, allowed_mentions = allowed_mentions
        )
    
    acknowledge_task = Task(coroutine, KOKORO)
    request_task = Task(request_image(client, endpoint, safe, cache), KOKORO)
    
    await WaitTillAll([acknowledge_task, request_task], KOKORO)
    
    try:
        acknowledge_task.result()
    except:
        request_task.cancel()
        raise
    
    return request_task.result()


@SLASH_CLIENT.interactions(is_global=True)
async def waifu_sfw(client, event,
    type_ : (SFW_WAIFUS, 'Waifu type!') = SFW_WAIFUS[0],
):
    """Safe working waifu."""
    guild_id = event.guild_id
    if not guild_id:
        abort('Guild only command')
    
    url = await get_waifu_image(client, event, type_, True, WAIFU_CACHE_BY_KEY[(type_, True)], False, None, None)
    if url is None:
        abort(ERROR_MESSAGE_NO_WAIFU)
    
    return InteractionResponse(
        embed = Embed('link', url=url).add_image(url).add_footer(PROVIDER_FOOTER),
        components = Button(
            emoji = EMOJI_NEW,
            custom_id = f'waifu.sfw.{type_}',
        )
    )


@SLASH_CLIENT.interactions(is_global=True, nsfw=True)
async def waifu_nsfw(client, event,
    type_ : (NSFW_WAIFUS, 'Waifu type!') = NSFW_WAIFUS[0],
):
    """Waifu with extras!"""
    guild_id = event.guild_id
    if not guild_id:
        abort('Guild only command')
    
    channel = event.channel
    if (channel is None) or (not getattr(channel, 'nsfw', False)):
        abort('Nsfw channel only!')
    
    url = await get_waifu_image(client, event, type_, False, WAIFU_CACHE_BY_KEY[(type_, False)], False, None, None)
    if url is None:
        abort(ERROR_MESSAGE_NO_WAIFU)
    
    return InteractionResponse(
        embed = Embed('link', url=url).add_image(url).add_footer(PROVIDER_FOOTER),
        components = Button(
            emoji = EMOJI_NEW,
            custom_id = f'waifu.nsfw.{type_}',
        )
    )


class NewWaifu:
    __slots__ = ('get_waifu_parameters', )
    
    def __init__(self, key, cache):
        self.get_waifu_parameters = (*key, cache, True)
    
    async def __call__(self, client, event):
        if event.user is not event.message.interaction.user:
            return
        
        url = await get_waifu_image(client, event, *self.get_waifu_parameters, None, None)
        if url is None:
            source_embed = event.message.embed
            if source_embed is None:
                # Should not happen
                embed = Embed(None, ERROR_MESSAGE_NO_WAIFU).add_footer(PROVIDER_FOOTER)
            else:
                embed = Embed(source_embed.title, ERROR_MESSAGE_NO_WAIFU, url=source_embed.description)
                embed.image = source_embed.image
                embed.add_footer(PROVIDER_FOOTER)
        
        else:
            embed = Embed('link', url=url).add_image(url).add_footer(PROVIDER_FOOTER)
        
        return embed

for key, cache in WAIFU_CACHE_BY_KEY.items():
    SLASH_CLIENT.interactions(
        NewWaifu(key, cache),
        custom_id = f'waifu.{"" if key[1] else "n"}sfw.{key[0]}',
    )

del key, cache

def build_response_and_allowed_users(client, event, verb, input_users):
    users = set()
    for user in input_users:
        if user is not None:
            users.add(user)
    
    users.discard(event.user)
    try:
        users.remove(client)
    except KeyError:
        client_in_users = False
    else:
        client_in_users = True
    
    users = [*users]
    
    response_parts = ['> ']
    
    user_count = len(users)
    if (user_count == 0) and (not client_in_users):
        response_parts.append(client.mention)
    else:
        response_parts.append(event.user.mention)
    
    response_parts.append(' ')
    response_parts.append(verb)
    response_parts.append(' ')
    
    if user_count == 0:
        if client_in_users:
            if random() > 0.5:
                response_parts.append('me ')
                response_parts.append(EMOJI_FLUSHED.as_emoji)
            else:
                response_parts.append(client.mention)
        else:
            response_parts.append(event.user.mention)
    
    elif user_count == 1 and not client_in_users:
            response_parts.append(users[0].mention)
    
    else:
        for user in users[: - (2 - client_in_users)]:
            response_parts.append(user.mention)
            response_parts.append(', ')
        
        response_parts.append(users[- (2 - client_in_users)].mention)
        response_parts.append(' and ')
        
        if client_in_users:
            if random() > 0.5:
                response_parts.append('me ')
                response_parts.append(EMOJI_FLUSHED.as_emoji)
            else:
                response_parts.append(client.mention)
        else:
            response_parts.append(users[-1].mention)
    
    response = ''.join(response_parts)
    
    return response, users


class Action:
    __slots__ = ('cache', 'name', 'verb')
    def __init__(self, name, verb):
        self.name = name
        self.verb = verb
        self.cache = []
    
    async def __call__(
        self, client, event,
        user_00: ('user', 'Select someone.', 'user-1') = None,
        user_01: ('user', 'Select someone', 'user-2') = None,
        user_02: ('user', 'Select someone', 'user-3') = None,
        user_03: ('user', 'Select someone', 'user-4') = None,
        user_04: ('user', 'Select someone', 'user-5') = None,
        user_05: ('user', 'Select someone', 'user-6') = None,
        user_06: ('user', 'Select someone', 'user-7') = None,
        user_07: ('user', 'Select someone', 'user-8') = None,
        user_08: ('user', 'Select someone', 'user-9') = None,
        user_09: ('user', 'Select someone', 'user-10') = None,
        user_10: ('user', 'Select someone', 'user-11') = None,
        user_11: ('user', 'Select someone', 'user-12') = None,
        user_12: ('user', 'Select someone', 'user-13') = None,
        user_13: ('user', 'Select someone', 'user-14') = None,
        user_14: ('user', 'Select someone', 'user-15') = None,
        user_15: ('user', 'Select someone', 'user-16') = None,
        user_16: ('user', 'Select someone', 'user-17') = None,
        user_17: ('user', 'Select someone', 'user-18') = None,
        user_18: ('user', 'Select someone', 'user-19') = None,
        user_19: ('user', 'Select someone', 'user-20') = None,
        user_20: ('user', 'Select someone', 'user-21') = None,
        user_21: ('user', 'Select someone', 'user-22') = None,
        user_22: ('user', 'Select someone', 'user-23') = None,
        user_23: ('user', 'Select someone', 'user-24') = None,
        user_24: ('user', 'Select someone', 'user-25') = None,
    ):
        guild_id = event.guild_id
        if not guild_id:
            abort('Guild only command')
        
        response, allowed_mentions = build_response_and_allowed_users(
            client, event, self.verb,
            (
                user_00, user_01, user_02, user_03, user_04, user_05, user_06, user_07, user_08, user_09,
                user_10, user_11, user_12, user_13, user_14, user_15, user_16, user_17, user_18, user_19,
                user_20, user_21, user_22, user_23, user_24
            )
        )
        
        try:
            url = await get_waifu_image(client, event, self.name, True, self.cache, False, response, allowed_mentions)
        except TimeoutError:
            embed = Embed(None, '*Did not get response in time, please try again later.*')
        
        else:
            if url is None:
                embed = Embed(None, '*Could not get any images, please try again later.*')
            
            else:
                embed = Embed(
                    color = (event.id >> 22) & 0xffffff
                ).add_image(
                    url,
                ).add_footer(
                    PROVIDER_FOOTER,
                )
        
        if event.is_unanswered():
            await client.interaction_response_message_create(
                event, response, embed = embed, allowed_mentions = allowed_mentions
            )
            
        else:
            await client.interaction_response_message_edit(
                event, response, embed = embed, allowed_mentions = allowed_mentions
            )


for action_name, action_verb, action_description in (
    ('pat', 'pats', 'Do you like pats as well?'),
    ('kiss', 'kisses', 'If you really really like your onee, give her a kiss <3'),
    ('hug', 'hugs', 'Huh.. Huggu? HUGG YOUUU!!!'),
    ('cuddle', 'cuddles', 'Come here, you little qtie pie.'),
    ('lick', 'licks', 'Licking is a favored activity of cat girls.'),
    ('poke', 'pokes', 'It hurts!'),
    ('slap', 'slaps', 'Slapping others is not nice.'),
    ('smug', 'smugs at', 'Smug face.'),
    ('bully', 'bullies', 'No Bully!'),
    ('cry', 'cries because of', 'The saddest.'),
    ('yeet', 'yeets', 'Yeet!'),
    ('blush', 'blushes at', 'Oh.'),
    ('smile', 'smiles at', 'Oh, really?'),
    ('wave', 'waves at', 'Flap flap'),
    ('highfive', 'highfives', 'Lets go boiz!'),
    ('handhold', 'holds hands of', 'Lewd!!'),
    ('nom', 'noms', 'Feed your nekogirl, or else'),
    ('bite', 'bites', 'Vampy.'),
    ('glomp', 'glomps', 'You can run, but you cant hide!'),
    ('kill', 'murders', 'Finally, some action.'),
    ('happy', 'is happy for', 'If you are happy, clap your..'),
    ('wink', 'winks at', 'Ara-ara'),
    ('dance', 'dancing with', 'Dancy, dancy.'),
    ('cringe', 'cringes at', 'Cringe, run!'),
    ('kick', 'kicks', 'Kicks butt!')
):
    SLASH_CLIENT.interactions(
        Action(action_name, action_verb),
        name = action_name,
        description = action_description,
        is_global = True,
    )

del action_name, action_verb, action_description
