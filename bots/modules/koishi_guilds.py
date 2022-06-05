__all__ = ()

from re import compile as re_compile, escape as re_escape, I as re_ignore_case, U as re_unicode
from scarletio import LOOP_TIME, Task
from hata import Client, KOKORO, DiscordException, ERROR_CODES, InviteTargetType, Embed
from hata.ext.slash import abort

SLASH_CLIENT: Client


CACHING_INTERVAL = 4 * 60.0 * 60.0 # 4 hour
GUILD_PER_PAGE = 10


PATTERN = re_compile(
    '|'.join(
        re_escape(value) for value in (
            'komeiji', 'koishi', '古明地', 'こいし', 'kkhta'
        )
    ),
    re_ignore_case | re_unicode,
)


@SLASH_CLIENT.interactions(is_global = True)
class koi_guilds:
    NEXT_CACHE_AT = 0.0
    GUILD_CACHE = []
    EMBED_CACHE = {}
    EMBED_BUILDER_TASKS = {}
    
    async def __new__(cls, page: ('number', 'Page') = 1):
        if cls.should_recache():
            cls.cache_guilds()
            cls.EMBED_CACHE.clear()
            cls.EMBED_BUILDER_TASKS.clear()
        
        return cls.get_embed(page)
    
    
    @classmethod
    def should_recache(cls):
        now = LOOP_TIME()
        if cls.NEXT_CACHE_AT < now:
            cls.NEXT_CACHE_AT = now + CACHING_INTERVAL
            return True
        
        return False
    
    
    @classmethod
    def cache_guilds(cls):
        guilds = []
        
        for guild in SLASH_CLIENT.guilds:
            if PATTERN.search(guild.name) is not None:
                guilds.append(guild)
        
        guilds.sort()
        
        
        GUILD_CACHE = cls.GUILD_CACHE
        GUILD_CACHE.clear()
        
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
        
    
    @classmethod
    def get_embed(cls, page):
        try:
            return cls.EMBED_CACHE[page]
        except KeyError:
            pass
        
        if (page < 1) or (page > len(cls.GUILD_CACHE)):
            abort(f'Page index out of expected range: [1, {len(cls.GUILD_CACHE)}]')
        
        return cls.build_embed(page)
    
    
    @classmethod
    async def build_embed(cls, page):
        yield
        
        EMBED_BUILDER_TASKS = cls.EMBED_BUILDER_TASKS
        task = EMBED_BUILDER_TASKS.get(page, None)
        if task is None:
            task = Task(cls.build_embed_task(page), KOKORO)
            EMBED_BUILDER_TASKS[page] = task
            
            embed = None
            try:
                embed = await task
            
            finally:
                if EMBED_BUILDER_TASKS.get(page, None) is task:
                    del EMBED_BUILDER_TASKS[page]
                    
                    if embed is not None:
                        cls.EMBED_CACHE[page] = embed
        else:
            embed = await task
        
        yield embed
    
    
    @classmethod
    async def build_embed_task(cls, page):
        guilds = cls.GUILD_CACHE[page - 1]
        
        description_parts = []
        
        for guild in guilds:
            invite_url = await cls.try_get_invite_url_of(guild)
            
            if invite_url is None:
                description_parts.append(guild.name)
            else:
                description_parts.append('[')
                description_parts.append(guild.name)
                description_parts.append('](')
                description_parts.append(invite_url)
                description_parts.append(')')
            
            description_parts.append('\n')
        
        description = ''.join(description_parts)
        description_parts = None
        
        return Embed(
            'Koishi guilds',
            description,
        ).add_footer(
            f'Page {page} out of {len(cls.GUILD_CACHE)}'
        )
    
    
    @classmethod
    async def try_get_invite_url_of(cls, guild):
        invite_url = guild.vanity_url
        if (invite_url is not None):
            return invite_url
        
        if not guild.cached_permissions_for(SLASH_CLIENT).can_create_instant_invite:
            return None
        
        
        try:
            invites = await SLASH_CLIENT.invite_get_all_guild(guild)
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
            if invite.inviter is not SLASH_CLIENT:
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
