__all__ = ('BotInfo', 'BotStats',)

from hata.utils import timestamp_to_datetime
from hata.bases import IconSlot, Slotted
from hata.http import urls as module_urls

# bot info constants
from .constants import JSON_KEY_BOT_INFO_ID, JSON_KEY_BOT_INFO_NAME, JSON_KEY_BOT_INFO_DISCRIMINATOR_STRING, \
    JSON_KEY_BOT_INFO_AVATAR_BASE64, JSON_KEY_BOT_INFO_BANNER_URL, JSON_KEY_BOT_INFO_PREFIX, \
    JSON_KEY_BOT_INFO_SHORT_DESCRIPTION, JSON_KEY_BOT_INFO_LONG_DESCRIPTION, JSON_KEY_BOT_INFO_TAG_ARRAY, \
    JSON_KEY_BOT_INFO_WEBSITE_URL, JSON_KEY_BOT_INFO_SUPPORT_SERVER_INVITE_URL, JSON_KEY_BOT_INFO_GITHUB_URL, \
    JSON_KEY_BOT_INFO_OWNER_ID_ARRAY, JSON_KEY_BOT_INFO_FEATURED_GUILD_ID_ARRAY, JSON_KEY_BOT_INFO_INVITE_URL, \
    JSON_KEY_BOT_INFO_CERTIFIED_AT, JSON_KEY_BOT_INFO_IS_CERTIFIED, JSON_KEY_BOT_INFO_VANITY_URL, \
    JSON_KEY_BOT_INFO_UPVOTES, JSON_KEY_BOT_INFO_UPVOTES_MONTHLY, JSON_KEY_BOT_INFO_UP_DONATE_BOT_GUILD_ID

# bot stats constants
from .constants import JSON_KEY_BOT_STATS_GUILD_COUNT, JSON_KEY_BOT_STATS_GUILD_COUNT_PER_SHARD_ARRAY, \
    JSON_KEY_BOT_STATS_SHARD_ID, JSON_KEY_BOT_STATS_SHARD_COUNT


class BotInfo(metaclass=Slotted):
    """
    Representing information about a bot.
    
    Attributes
    ----------
    avatar_hash : `int`
        The bot's avatar hash.
    avatar_type : ``IconType``
        The bot's avatar's type.
    banner_url : `None` or `str`
        Url for the bot's banner image.
    certified_at : `None` or `datetime`
        When the bot was approved. Set as `None` if was not yet.
    discriminator : `int`
        The bot's discriminator.
    donate_bot_guild_id : `int`
        The guild id for the donatebot setup(?).
    featured_guild_ids : `None` or `tuple` of `int`
        The featured guild's identifiers on the bot's page.
    github_url : `None` or `str`
        Link to the github repo of the bot.
    id : `int`
        The bot's identifier.
    invite_url : `None` or `str`
        Custom bot invite url.
    long_description : `str`
        The long description of the bot.
    name : `str`
        The name of the bot.
    owner_id : `int
        The bot's main owner's identifier.
    owner_ids : `tuple` of `int`
        The bot's owners' identifiers.
    prefix : `str`
        Prefix of the bot.
    short_description : `str`
        The short description of the bot.
    support_server_invite_url : `None` or `str`
        Url to the bot's support server.
    tags : `None` or `tuple` of `str`
        The tags of the bot.
    upvotes : `int`
        The amount of upvotes the bot has.
    upvotes_monthly : `int`
        The amount of upvotes the bot has this month.
    vanity_url : `None` or `str`
        Vanity url of the bot.
    website_url : `None` or `str`
        The website url of the bot.
    """
    __slots__ = ('banner_url', 'certified_at', 'discriminator', 'donate_bot_guild_id', 'featured_guild_ids',
        'github_url', 'id', 'invite_url', 'long_description', 'name', 'owner_id', 'owner_ids', 'prefix',
        'short_description', 'support_server_invite_url', 'tags', 'upvotes', 'upvotes_monthly', 'vanity_url',
        'website_url')
    
    avatar = IconSlot(
        'avatar',
        JSON_KEY_BOT_INFO_AVATAR_BASE64,
        module_urls.user_avatar_url,
        module_urls.user_avatar_url_as,
    )
    
    @classmethod
    def from_data(cls, data):
        """
        Creates a new bot info instance.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Deserialized bot info data.
        
        Returns
        -------
        self : ``BotInfo``
        """
        self = object.__new__(cls)
        
        # avatar_hash & avatar_type
        self._set_avatar(data)
        
        # banner_url
        self.banner_url = data.get(JSON_KEY_BOT_INFO_BANNER_URL, None)
        
        # certified_at
        if data.get(JSON_KEY_BOT_INFO_IS_CERTIFIED, False):
            certified_at = timestamp_to_datetime(data[JSON_KEY_BOT_INFO_CERTIFIED_AT])
        else:
            certified_at = None
        self.certified_at = certified_at
        
        # discriminator
        self.discriminator = int(data[JSON_KEY_BOT_INFO_DISCRIMINATOR_STRING])
        
        # donate_bot_guild_id
        self.donate_bot_guild_id = int(data[JSON_KEY_BOT_INFO_UP_DONATE_BOT_GUILD_ID])
        
        # featured_guild_ids
        featured_guild_ids = data.get(JSON_KEY_BOT_INFO_FEATURED_GUILD_ID_ARRAY, None)
        if (featured_guild_ids is None) or (not featured_guild_ids):
            featured_guild_ids = None
        else:
            featured_guild_ids = tuple(sorted(int(guild_id) for guild_id in featured_guild_ids))
        self.featured_guild_ids = featured_guild_ids
        
        # github_url
        self.github_url = data.get(JSON_KEY_BOT_INFO_GITHUB_URL, None)
        
        # id
        self.id = int(data[JSON_KEY_BOT_INFO_ID])
        
        # invite_url
        self.invite_url = data.get(JSON_KEY_BOT_INFO_INVITE_URL, None)
        
        # long_description
        self.long_description = data[JSON_KEY_BOT_INFO_LONG_DESCRIPTION]
        
        # name
        self.name = data[JSON_KEY_BOT_INFO_NAME]
        
        # owner_id & owner_ids
        owner_ids = data[JSON_KEY_BOT_INFO_OWNER_ID_ARRAY]
        self.owner_id = int(owner_ids[0])
        self.owner_ids = tuple(sorted(int(owner_id) for owner_id in owner_ids))
        
        # prefix
        self.prefix = data[JSON_KEY_BOT_INFO_PREFIX]
        
        # short_description
        self.short_description = data[JSON_KEY_BOT_INFO_SHORT_DESCRIPTION]
        
        # support_server_invite_url
        self.support_server_invite_url = data.get(JSON_KEY_BOT_INFO_SUPPORT_SERVER_INVITE_URL, None)
        
        # tags
        self.tags = tuple(sorted(data[JSON_KEY_BOT_INFO_TAG_ARRAY]))
        
        # upvotes
        self.upvotes = data[JSON_KEY_BOT_INFO_UPVOTES]
        
        # upvotes_monthly
        self.upvotes_monthly = data[JSON_KEY_BOT_INFO_UPVOTES_MONTHLY]
        
        # vanity_url
        self.vanity_url = data.get(JSON_KEY_BOT_INFO_VANITY_URL, None)
        
        # website_url
        self.website_url = data.get(JSON_KEY_BOT_INFO_WEBSITE_URL, None)
        
        return self
    
    
    def __repr__(self):
        """Returns the bot info's representation."""
        return f'<{self.__class__.__name__} id={self.id} name={self.name}>'


class BotStats:
    """
    Contains a listed bot's stats.
    
    Attributes
    ----------
    guild_count : `int`
        The amount of guilds the bot is in. Defaults to `-1`.
    guild_count_per_shard : `tuple` of `int`
        The amount of guilds per shards. Can be empty.
    shard_count : `int`
        The amount of shards the bot has. Defaults to `-1`.
    shard_id : `int`
        The shard ID to post as (?). Defaults to `-1`.
    """
    __slots__ = ('guild_count', 'guild_count_per_shard', 'shard_count', 'shard_id')
    
    @classmethod
    def from_data(cls, data):
        """
        Creates a new bot stats instance.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Deserialized bot stats data.
        
        Returns
        -------
        self : ``BotStats``
        """
        self = object.__new__(cls)
        
        # guild_count
        self.guild_count = data.get(JSON_KEY_BOT_STATS_GUILD_COUNT, -1)
        
        # guild_count_per_shard
        try:
            guild_count_per_shard = data[JSON_KEY_BOT_STATS_GUILD_COUNT_PER_SHARD_ARRAY]
        except KeyError:
            guild_count_per_shard = ()
        self.guild_count_per_shard = guild_count_per_shard
        
        # shard_count
        self.shard_count = data.get(JSON_KEY_BOT_STATS_SHARD_COUNT, -1)
        
        # shard_id
        self.shard_id = data.get(JSON_KEY_BOT_STATS_SHARD_ID, -1)
        
        return self
    
    
    def __repr__(self):
        """Returns the bot stats' representation."""
        return f'<{self.__class__.__name__}>'
