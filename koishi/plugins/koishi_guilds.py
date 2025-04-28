__all__ = ()

from re import compile as re_compile, escape as re_escape, I as re_ignore_case, U as re_unicode
from scarletio import LOOP_TIME, Task
from hata import KOKORO, DiscordException, ERROR_CODES, InviteTargetType, Embed, ICON_TYPE_NONE, elapsed_time, \
    Permission, Emoji
from hata.ext.plugin_loader import require
from hata.ext.slash import abort

from ..bot_utils.constants import GUILD__SUPPORT
from ..bots import MAIN_CLIENT

require('hey_mister')

CACHING_INTERVAL = 8 * 60.0 * 60.0 # 8 hour
GUILD_PER_PAGE = 5


PATTERN = re_compile(
    '|'.join(
        re_escape(value) for value in (
            'komeiji', 'koishi', '古明地', 'こいし', 'kkhta'
        )
    ),
    re_ignore_case | re_unicode,
)


GUILD_CACHE = []
EMBED_CACHE = {}
EMBED_BUILDER_TASKS = {}


def clear_cache():
    GUILD_CACHE.clear()
    EMBED_CACHE.clear()
    EMBED_BUILDER_TASKS.clear()


def cache_guilds():
    guilds = []
    
    for guild in MAIN_CLIENT.guilds:
        if guild.owner_id not in GUILD__SUPPORT.users:
            continue
        
        if PATTERN.search(guild.name) is None:
            continue
        
        guilds.append(guild)
    
    
    guilds.sort()
    
    
    guild_chunk = []
    guild_chunk_length = 0
    
    for guild in guilds:
        guild_chunk.append(guild)
        guild_chunk_length += 1
        
        if guild_chunk_length == GUILD_PER_PAGE:
            GUILD_CACHE.append(guild_chunk.copy())
            guild_chunk.clear()
            guild_chunk_length = 0
    
    if guild_chunk_length:
        GUILD_CACHE.append(guild_chunk.copy())


def get_embed(page):
    try:
        return EMBED_CACHE[page]
    except KeyError:
        pass
    
    if (page < 1) or (page > len(GUILD_CACHE)):
        abort(f'Page index out of expected range: [1, {len(GUILD_CACHE)}]')
    
    return build_embed(page)


async def build_embed(page):
    yield
    
    task = EMBED_BUILDER_TASKS.get(page, None)
    if task is None:
        task = Task(KOKORO, build_embed_task(page))
        EMBED_BUILDER_TASKS[page] = task
        
        embeds = None
        try:
            embeds = await task
        
        finally:
            if EMBED_BUILDER_TASKS.get(page, None) is task:
                del EMBED_BUILDER_TASKS[page]
                
                if embeds is not None:
                    EMBED_CACHE[page] = embeds
    else:
        embeds = await task
    
    yield embeds


async def build_embed_task( page):
    guilds = GUILD_CACHE[page - 1]
    
    embeds = []
    
    for guild in guilds:
        embed = await build_guild_embed(guild)
        embeds.append(embed)
    
    embeds[-1].add_footer(f'Page {page} out of {len(GUILD_CACHE)}')
    
    return embeds


async def build_guild_embed(guild):
    invite_url = await try_get_invite_url_of(guild)
    
    approximate_user_count = guild.approximate_user_count
    if approximate_user_count == 0:
        await MAIN_CLIENT.guild_get(guild)
        approximate_user_count = guild.approximate_user_count
    
    if invite_url is None:
        description = None
    else:
        vanity_code = guild.vanity_code
        if vanity_code is None:
            description = f'[Join {guild.name}!]({invite_url})'
        else:
            description = f'[Join discord.gg/{vanity_code}!]({invite_url})'
    
    embed = Embed(
        guild.name,
        description,
        color  = (guild.icon_hash & 0xFFFFFF if (guild.icon_type is ICON_TYPE_NONE) else (guild.id >> 22) & 0xFFFFFF),
    ).add_thumbnail(
        guild.icon_url_as(size = 128),
    )
    
    guild_description = guild.description
    if (guild_description is not None):
        embed.add_field(
            'Description',
            (
                f'```\n'
                f'{guild_description}\n'
                f'```'
            ),
        )
    
    embed.add_field(
        'Users',
        (
            f'```\n'
            f'{approximate_user_count}\n'
            f'```'
        ),
        inline = True,
    ).add_field(
        'Online users',
        (
            f'```\n'
            f'{guild.approximate_online_count}\n'
            f'```'
        ),
        inline = True,
    ).add_field(
        'Age',
        (
            f'```\n'
            f'{elapsed_time(guild.created_at)}\n'
            f'```'
        ),
    ).add_field(
        'Boost level',
        (
            f'```\n'
            f'{guild.boost_level}\n'
            f'```'
        ),
        inline = True,
    ).add_field(
        'Emojis',
        (
            f'```\n'
            f'{len(guild.emojis)}\n'
            f'```'
        ),
        inline = True,
    ).add_field(
        'Stickers',
        (
            f'```\n'
            f'{len(guild.stickers)}\n'
            f'```'
        ),
        inline = True,
    )
    
    return embed


async def try_get_invite_url_of(guild):
    invite_url = guild.vanity_url
    if (invite_url is not None):
        return invite_url
    
    if not guild.cached_permissions_for(MAIN_CLIENT).create_instant_invite:
        return None
    
    
    try:
        invites = await MAIN_CLIENT.invite_get_all_guild(guild)
    except ConnectionError:
        raise
    
    except DiscordException as err:
        if err.code in (
            ERROR_CODES.missing_access, # client removed
            ERROR_CODES.missing_permissions, # permissions changed meanwhile
            ERROR_CODES.unknown_guild, # guild deleted
        ):
            return None
        
        raise
    
    
    for invite in invites:
        if invite.inviter is not MAIN_CLIENT:
            continue
        
        if invite.type is not InviteTargetType.none:
            continue
        
        max_age = invite.max_age
        if (max_age is not None) and (max_age > 0):
            continue
        
        max_uses = invite.max_uses
        if (max_uses is None) or (max_uses > 0):
            continue
        
        return invite.url
    
    return None


@MAIN_CLIENT.interactions(is_global = True)
class koi_guilds:
    NEXT_CACHE_AT = 0.0
    
    async def __new__(cls, page: ('number', 'Page') = 1):
        if cls.should_recache():
            clear_cache()
            cache_guilds()
        
        return get_embed(page)
    
    
    @classmethod
    def should_recache(cls):
        now = LOOP_TIME()
        if cls.NEXT_CACHE_AT < now:
            cls.NEXT_CACHE_AT = now + CACHING_INTERVAL
            return True
        
        return False


EMOJI_KOISHI_DERP = Emoji.precreate(772498743378575403)


@MAIN_CLIENT.interactions(
    is_global = True,
    required_permissions = Permission().update_by_keys(administrator = True),
)
async def koi_guilds_how_to(client, event):
    """How to become the best koi guild!"""
    return Embed(
        'The four steps of becoming a Koishi guild!',
    ).add_field(
        'Step 1 | Koishi',
        'The guild must be named after Koishi or a related topic!',
    ).add_field(
        'Step 2 | Security',
        'To avoid name abuse, each Koishi guild owner is required to join my support server.\n'
    ).add_field(
        'Step 3 | Invite (Optional)',
        (
            f'For invite to show up, the guid must have either vanity invite, or an invite must be created with the '
            f'{client.name_at(event.guild_id)}\'s `/invite-create` command.'
        )
    ).add_field(
        'Step 4 | Description (Optional)',
        'After enabling the community feature in the guild, you will be able to set guild description.',
    ).add_footer(
        'If the changes are not showing up instantly, do not worry! The command is updated periodically!'
    )


@MAIN_CLIENT.interactions(
    guild = GUILD__SUPPORT,
    required_permissions = Permission().update_by_keys(administrator = True),
)
async def koi_guilds_recache():
    cache_guilds()
    return 'cache updated'
