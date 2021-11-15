__all__ = ('TopGGClient', )

from hata.backend.utils import WeakReferer
from hata.backned.futures import Task
from hata.backend.headers import DATE, METHOD_PATCH, METHOD_GET, METHOD_DELETE, METHOD_POST, METHOD_PUT, \
    AUTHORIZATION, CONTENT_TYPE

from hata.discord.client import Client
from hata.discord.core import KOKORO

from .constants import JSON_KEY_BOT_STATS_GUILD_COUNT, JSON_KEY_BOT_STATS_SHARD_ID, JSON_KEY_BOT_STATS_SHARD_COUNT, \
    JSON_KEY_WEEKEND_STATUS
from .types import UserInfo, BotInfo

AUTO_POST_INTERVAL = 1800.0

TOP_GG_ENDPOINT = 'https://top.gg/api'

async def start_auto_post(client):
    """
    Client launch event handler starting auto post.
    
    This method is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
    """
    top_gg_client = client.top_gg_client
    
    # update client is if required
    top_gg_client.client_id = client.client_id
    
    # Do not post initially, we might not have all the guilds loaded yet.
    if top_gg_client._auto_post_running:
        top_gg_client._auto_post_handler = KOKORO.call_later(
            AUTO_POST_INTERVAL,
            trigger_auto_post,
            WeakReferer(top_gg_client),
        )


async def stop_auto_post(client):
    """
    Client disconnect event handler, which stops auto posting.
    
    This method is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
    """
    top_gg_client = client.top_gg_client
    
    top_gg_client._auto_post_running = False
    
    auto_post_handler = top_gg_client._auto_post_handler
    if (auto_post_handler is not None):
        top_gg_client._auto_post_handler = None
        auto_post_handler.cancel()


def trigger_auto_post(top_gg_client_reference):
    """
    Triggers an auto post.
    
    Parameters
    ----------
    top_gg_client_reference : ``WeakReferer`` to ``TopGGClient``
        Weak reference to the top.gg client.
    """
    top_gg_client = top_gg_client_reference()
    if (top_gg_client is not None):
        Task(do_auto_post(top_gg_client, top_gg_client_reference), KOKORO)


async def do_auto_post(top_gg_client, top_gg_client_reference):
    """
    Does an auto post.
    
    This method is a coroutine.
    
    Parameters
    ----------
    top_gg_client : ``TopGGClient``
        The top.gg client.
    top_gg_client_reference : ``WeakReferer`` to ``TopGGClient``
        Weak reference to the top.gg client.
    """
    await top_gg_client.post_bot_stats()
    
    if top_gg_client._auto_post_running:
        top_gg_client._auto_post_handler = KOKORO.call_later(
            AUTO_POST_INTERVAL,
            trigger_auto_post,
            top_gg_client_reference,
        )


class TopGGClient:
    """
    Represents a client connection towards top.gg.
    
    Attributes
    ----------
    _auto_post_handler : `None` or ``TimerHandle``
        Handle to repeat the auto poster.
    _auto_post_running : `bool`
        Whether auto posting is still running.
    client_id : `int`
        The client's identifier.
    client_reference : ``WeakReferer`` to ``Client``
        Weakreference towards the wrapped bot.
    http : ``DiscordHTTPClient``
        Http client to do requests with.
    """
    __slots__ = ('__weakref__', '_auto_post_handler', '_auto_post_running', 'client_id', 'client_reference', 'http', )
    
    def __new__(cls, client):
        """
        Creates a new top.gg client instance.
        
        Parameters
        ----------
        client : ``Client``
            The discord client.
        """
        if not isinstance(client, Client):
            raise TypeError(f'`client` can be `{Client.__class__.__name__}` instance, got '
                f'{client.__class__.__name__}.')
        
        client_reference = WeakReferer(client)
        
        self = object.__new__(cls)
        self.client_reference = client_reference
        self._auto_post_handler = None
        self._auto_post_running = True
        
        self.client_id = client.id
        self.http = client.http
        
        client.top_gg_client = self
        client.events(start_auto_post, name='launch')
        client.events(stop_auto_post, name='disconnect')
        
        return self
    
    
    async def post_bot_stats(self):
        """
        Posts your guild & shard count.
        
        This method is a coroutine.
        """
        client = self.client_reference()
        if (client is not None):
            guild_count = len(client.guilds)
            
            shard_count = client.shard_count
            if shard_count < 1:
                shard_count = 1
            
            data = {
                JSON_KEY_BOT_STATS_GUILD_COUNT: guild_count,
                JSON_KEY_BOT_STATS_SHARD_COUNT: shard_count,
                JSON_KEY_BOT_STATS_SHARD_ID: 0,
            }
            
            await self._post_bot_stats(data)
    
    
    async def get_weekend_status(self):
        """
        Gets weekend status from top.gg.
        
        This function is a coroutine.
        
        Returns
        -------
        weekend_status : `bool`
        """
        data = await self._get_weekend_status()
        return data[JSON_KEY_WEEKEND_STATUS]
    
    
    def get_bot_voters(self):
        """
        Gets the last 1000 voters.
        
        This method is a coroutine.
        
        Returns
        -------
        voters : `list` of ``UserInfo``
        """
        user_datas = await self._get_bot_voters()
        return [UserInfo.from_data(user_data) for user_data in user_datas]
    
    
    async def bet_bot_info(self):
        """
        Gets bot information and returns it.
        
        This method is a coroutine.
        
        Returns
        -------
        bot_info : ``BotInfo``
        """
        data = await self._get_bot_info()
        return BotInfo.from_data(data)
    
    
    async def _post_bot_stats(self, data):
        """
        Posts bot stats to top.gg.
        
        This method is a coroutine.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Bot stats.
        
        Returns
        -------
        response_data : `Any`
        """
        return await self._request(
            METHOD_POST,
            f'{TOP_GG_ENDPOINT}/bots/stats',
            data,
        )
    
    
    async def _get_weekend_status(self):
        """
        Gets weekend status from top.gg.
        
        This method is a coroutine.
        
        Returns
        -------
        response_data : `Any`
        """
        return await self._request(
            METHOD_GET,
            f'{TOP_GG_ENDPOINT}/weekend',
            None,
        )
    
    
    async def _get_bot_voters(self):
        """
        Gets the last 1000 voters.
        
        This method is a coroutine.
        
        Returns
        -------
        response_data : `Any`
        """
        return await self._request(
            METHOD_GET,
            f'{TOP_GG_ENDPOINT}/bots/{self.client_id}/votes',
            None,
        )
        