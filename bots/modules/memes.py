from hata import Client, Embed, BUILTIN_EMOJIS, Lock, KOKORO, DiscordException, ERROR_CODES, WebhookType, Emoji
from hata.ext.slash import abort, Button, Row, InteractionResponse

SLASH_CLIENT : Client

EMOJI_NEW = BUILTIN_EMOJIS['arrows_counterclockwise']

CUSTOM_ID_GOOD_ANIME_MEMES = 'memes.good_anime_memes.new'

BUTTON_NEW_GOOD_ANIME_MEMES = Button(
    emoji = EMOJI_NEW,
    custom_id = CUSTOM_ID_GOOD_ANIME_MEMES,
)

COMPONENTS_GOOD_ANIME_MEMES = Row(
    BUTTON_NEW_GOOD_ANIME_MEMES,
)

class MemeLock:
    __slots__ = ('last_meme_after', 'queue', 'url', 'lock')
    
    def __init__(self, url):
        self.last_meme_after = None
        self.queue = []
        self.url = url
        self.lock = Lock(KOKORO)

MEME_LOCK_GOOD_ANIME_MEMES = MemeLock('https://www.reddit.com/r/goodanimemes.json')

async def get_memes(meme_lock):
    lock = meme_lock.lock
    if lock.locked():
        await lock
        return
    
    async with lock:
        after = meme_lock.last_meme_after
        if after is None:
            after = ''
        
        async with SLASH_CLIENT.http.get(
            meme_lock.url,
            params = {
                'limit': 100,
                'after': after,
            },
        ) as response:
            
            json = await response.json()
        
        for meme_children in json['data']['children']:
            meme_children_data = meme_children['data']
            if meme_children_data.get('is_self', False) or \
                    meme_children_data.get('is_video', False) or \
                    meme_children_data.get('over_18', False):
                continue
            
            url = meme_children_data['url']
            if url.startswith('https://www.reddit.com/gallery/'):
                continue
            
            meme_lock.queue.append((meme_children_data['title'], url))
        
        meme_lock.last_meme_after = json['data'].get(after, None)


async def get_meme(meme_lock):
    meme_queue = meme_lock.queue
    if meme_queue:
        return meme_queue.pop()
    
    await get_memes(meme_lock)
    
    if meme_queue:
        return meme_queue.pop()
    
    return None


@SLASH_CLIENT.interactions(is_global=True, name='meme')
async def meme_(client, event):
    """Shows a meme."""
    if not event.guild_id:
        abort('Guild only command.')
    
    meme = await get_meme(MEME_LOCK_GOOD_ANIME_MEMES)
    if meme is None:
        abort('No memes for now.')
    
    title, url = meme
    embed = Embed(title, url=url).add_image(url)
    
    return InteractionResponse(embed=embed, components=COMPONENTS_GOOD_ANIME_MEMES)


@SLASH_CLIENT.interactions(custom_id=CUSTOM_ID_GOOD_ANIME_MEMES)
async def send_new_good_anime_meme():
    meme = await get_meme(MEME_LOCK_GOOD_ANIME_MEMES)
    if meme is None:
        embed = Embed(
            'Sad panda is sad',
            'No more memes have been found.\n'
            'Please try again later.'
        )
    else:
        title, url = meme
        embed = Embed(title, url=url).add_image(url)
    
    return embed
