__all__ = ('TopGGClient', )

from hata.backend.utils import WeakReferer, imultidict, to_json, from_json
from hata.backend.futures import Task, sleep, Future
from hata.backend.headers import RETRY_AFTER, METHOD_GET, METHOD_POST, AUTHORIZATION, CONTENT_TYPE, USER_AGENT
from hata.backend.http import RequestCM
from hata.backend.event_loop import LOOP_TIME

from hata.discord.client import Client
from hata.discord.core import KOKORO
from hata.discord.http import LIBRARY_USER_AGENT

from .constants import JSON_KEY_POST_BOT_STATS_GUILD_COUNT, JSON_KEY_POST_BOT_STATS_SHARD_ID, \
    JSON_KEY_POST_BOT_STATS_SHARD_COUNT, JSON_KEY_WEEKEND_STATUS, QUERY_KEY_GET_BOTS_LIMIT, \
    QUERY_KEY_GET_BOTS_OFFSET, QUERY_KEY_GET_BOTS_SORT_BY, QUERY_KEY_GET_BOTS_SEARCH_QUERY, \
    QUERY_KEY_GET_BOTS_FIELDS, JSON_KEY_VOTED, QUERY_KEY_GET_USER_VOTE_USER_ID, RATE_LIMIT_GLOBAL_SIZE, \
    RATE_LIMIT_GLOBAL_RESET_AFTER, RATE_LIMIT_BOTS_SIZE, RATE_LIMIT_BOTS_RESET_AFTER, \
    RATE_LIMIT_GLOBAL_DEFAULT_DURATION
from .types import UserInfo, BotInfo, BotsQueryResult
from .bots_query import get_bots_query_sort_by_value, create_bots_query_search_value, BOTS_QUERY_FIELDS_VALUE
from .rate_limit_handling import RateLimitGroup, RateLimitHandler, StackedRateLimitHandler
from .exceptions import TopGGHttpException

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
    
    Raises
    ------
    TopGGHttpException
        Any exception raised by top.gg api.
    """
    try:
        await top_gg_client.post_bot_stats()
    except ConnectionError:
        return
    finally:
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
    _global_rate_limit_expires_at : `float`
        When the global rate limit expires in monotonic time.
    _headers : `imultidict`
        Request headers.
    _rate_limit_handler_global : ``RateLimitHandler``
        Rate limit handler applied to all rate limits.
    _rate_limit_handler_bots : ``RateLimitHandler``
        Rate limit handler applied to `/bots` endpoints.
    client_id : `int`
        The client's identifier.
    client_reference : ``WeakReferer`` to ``Client``
        Weakreference towards the wrapped bot.
    http : ``DiscordHTTPClient``
        Http client to do requests with.
    top_gg_token : `str`
        Top.gg api token.
    """
    __slots__ = ('__weakref__', '_auto_post_handler', '_auto_post_running', '_global_rate_limit_expires_at', '_headers',
        '_rate_limit_handler_bots', '_rate_limit_handler_global', 'client_id', 'client_reference', 'http', 'top_gg_token',)
    
    def __new__(cls, client, top_gg_token):
        """
        Creates a new top.gg client instance.
        
        Parameters
        ----------
        client : ``Client``
            The discord client.
        top_gg_token : `str`
            Top.gg api token.
        
        Raises
        ------
        RuntimeError
            If the client already has `top_gg_client` attribute.
        TypeError
            - If `client` is not ``Client`` instance.
            - If `top_gg_token` is not `str` instance.
        """
        if not isinstance(client, Client):
            raise TypeError(f'`client` can be `{Client.__class__.__name__}` instance, got '
                f'{client.__class__.__name__}.')
        
        if not isinstance(top_gg_token, str):
            raise TypeError(f'`top_gg_token` can be `str` instance, got {top_gg_token.__class__.__name__}.')
        
        if hasattr(client, 'top_gg_client'):
            raise RuntimeError(f'The client already has `top_gg_client` attribute; got {client!r}.')
        
        client_reference = WeakReferer(client)
        
        headers = imultidict()
        headers[USER_AGENT] = LIBRARY_USER_AGENT
        headers[AUTHORIZATION] = top_gg_token
        
        self = object.__new__(cls)
        self.client_reference = client_reference
        self._auto_post_handler = None
        self._auto_post_running = True
        self._headers = headers
        
        self.client_id = client.id
        self.http = client.http
        self.top_gg_token = top_gg_token
        
        self._global_rate_limit_expires_at = 0.0
        self._rate_limit_handler_global = RateLimitGroup(RATE_LIMIT_GLOBAL_SIZE, RATE_LIMIT_GLOBAL_RESET_AFTER)
        self._rate_limit_handler_bots = RateLimitGroup(RATE_LIMIT_BOTS_SIZE, RATE_LIMIT_BOTS_RESET_AFTER)
        
        client.top_gg_client = self
        client.events(start_auto_post, name='launch')
        client.events(stop_auto_post, name='shutdown')
        
        return self
    
    
    async def post_bot_stats(self):
        """
        Posts your guild & shard count.
        
        This method is a coroutine.
        
        Raises
        ------
        ConnectionError
            No internet connection.
        TopGGHttpException
            Any exception raised by top.gg api.
        """
        client = self.client_reference()
        if (client is not None):
            guild_count = len(client.guilds)
            
            shard_count = client.shard_count
            if shard_count < 1:
                shard_count = 1
            
            data = {
                JSON_KEY_POST_BOT_STATS_GUILD_COUNT: guild_count,
                JSON_KEY_POST_BOT_STATS_SHARD_COUNT: shard_count,
                JSON_KEY_POST_BOT_STATS_SHARD_ID: 0,
            }
            
            await self._post_bot_stats(data)
    
    
    async def get_weekend_status(self):
        """
        Gets weekend status from top.gg.
        
        This function is a coroutine.
        
        Returns
        -------
        weekend_status : `bool`
        
        Raises
        ------
        ConnectionError
            No internet connection.
        TopGGHttpException
            Any exception raised by top.gg api.
        """
        data = await self._get_weekend_status()
        return data[JSON_KEY_WEEKEND_STATUS]
    
    
    async def get_bot_voters(self):
        """
        Gets the last 1000 voters.
        
        This method is a coroutine.
        
        Returns
        -------
        voters : `list` of ``UserInfo``
        
        Raises
        ------
        ConnectionError
            No internet connection.
        TopGGHttpException
            Any exception raised by top.gg api.
        """
        user_datas = await self._get_bot_voters()
        return [UserInfo.from_data(user_data) for user_data in user_datas]
    
    
    async def get_bot_info(self):
        """
        Gets bot information and returns it.
        
        This method is a coroutine.
        
        Returns
        -------
        bot_info : ``BotInfo``
        
        Raises
        ------
        ConnectionError
            No internet connection.
        TopGGHttpException
            Any exception raised by top.gg api.
        """
        data = await self._get_bot_info()
        return BotInfo.from_data(data)
    
    
    async def get_bots(self, *, limit=50, offset=0, sort_by=None, search=None):
        """
        Gets information about multiple bots.
        
        This method is a coroutine.
        
        Parameters
        ----------
        limit : `int`, Optional (Keyword only)
            The amount of bots to query. Defaults to `50`.
        offset : `int`, Optional (Keyword only)
            Query offset. Defaults to `0`
        sort_by : `None` or `str`, Optional (Keyword only)
            Which field to sort by the bots. Defaults to `None`.
        search : `None` or `dict` of (`str`, `Any`) items, Optional (Keyword only)
            Fields an expected values to search for.
        
        Returns
        -------
        get_bots_result : ``BotsQueryResult``
        
        Raises
        ------
        LookupError
            - If `sort_by` refers to a not existent field.
            - If `search` contains a not existent field.
        ConnectionError
            No internet connection.
        TopGGHttpException
            Any exception raised by top.gg api.
        """
        if limit > 500:
            limit = 500
        
        query_sort_by_value = get_bots_query_sort_by_value(sort_by)
        query_search_value = create_bots_query_search_value(search)
        
        query_parameters = {
            QUERY_KEY_GET_BOTS_LIMIT: limit,
            QUERY_KEY_GET_BOTS_OFFSET: offset,
            QUERY_KEY_GET_BOTS_SORT_BY: query_sort_by_value,
            QUERY_KEY_GET_BOTS_SEARCH_QUERY: query_search_value,
            # QUERY_KEY_GET_BOTS_FIELDS: BOTS_QUERY_FIELDS_VALUE, # Defaults to all fields, so we just skip it
        }
        
        data = await self._get_bots(query_parameters)
        return BotsQueryResult.from_data(data)
    
    
    async def get_user_info(self, user_id):
        """
        Gets user info for the given user identifier.
        
        This method is a coroutine.
        
        Parameters
        ----------
        user_id : `int`
            The user's identifier to get.
        
        Returns
        -------
        user_info : ``UserInfo``
        
        Raises
        ------
        ConnectionError
            No internet connection.
        TopGGHttpException
            Any exception raised by top.gg api.
        """
        data = await self._get_user_info(user_id)
        return UserInfo.from_data(data)
    
    
    async def get_user_vote(self, user_id):
        """
        Returns whether the user voted in the last 12 hours.
        
        This method is a coroutine.
        
        Parameters
        ----------
        user_id : `int`
            The user's identifier.
        
        Returns
        -------
        voted : `bool`
        
        Raises
        ------
        ConnectionError
            No internet connection.
        TopGGHttpException
            Any exception raised by top.gg api.
        """
        data = await self._get_user_vote({QUERY_KEY_GET_USER_VOTE_USER_ID: user_id})
        return bool(data[JSON_KEY_VOTED])
    
    
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
        
        Raises
        ------
        ConnectionError
            No internet connection.
        TopGGHttpException
            Any exception raised by top.gg api.
        """
        return await self._request(
            METHOD_POST,
            f'{TOP_GG_ENDPOINT}/bots/stats',
            StackedRateLimitHandler(self._rate_limit_handler_bots, self._rate_limit_handler_global),
            data = data,
        )
    
    
    async def _get_weekend_status(self):
        """
        Gets weekend status from top.gg.
        
        This method is a coroutine.
        
        Returns
        -------
        response_data : `Any`
        
        Raises
        ------
        ConnectionError
            No internet connection.
        TopGGHttpException
            Any exception raised by top.gg api.
        """
        return await self._request(
            METHOD_GET,
            f'{TOP_GG_ENDPOINT}/weekend',
            RateLimitHandler(self._rate_limit_handler_global),
        )
    
    
    async def _get_bot_voters(self):
        """
        Gets the last 1000 voters.
        
        This method is a coroutine.
        
        Returns
        -------
        response_data : `Any`
        
        Raises
        ------
        ConnectionError
            No internet connection.
        TopGGHttpException
            Any exception raised by top.gg api.
        """
        return await self._request(
            METHOD_GET,
            f'{TOP_GG_ENDPOINT}/bots/{self.client_id}/votes',
            StackedRateLimitHandler(self._rate_limit_handler_bots, self._rate_limit_handler_global),
        )
    
    
    async def _get_bot_info(self):
        """
        Gets bot information and returns it.
        
        This method is a coroutine.
        
        Returns
        -------
        response_data : `Any`
        
        Raises
        ------
        ConnectionError
            No internet connection.
        TopGGHttpException
            Any exception raised by top.gg api.
        """
        return await self._request(
            METHOD_GET,
            f'{TOP_GG_ENDPOINT}/bots/{self.client_id}',
            StackedRateLimitHandler(self._rate_limit_handler_bots, self._rate_limit_handler_global),
        )
    
    
    async def _get_bots(self, query_parameters):
        """
        Gets information about multiple bots.
        
        This method is a coroutine.
        
        Parameters
        ----------
        query_parameters : `dict` of (`str`, `Any`) items
            Query parameters.
            
        Returns
        -------
        response_data : `Any`
        
        Raises
        ------
        ConnectionError
            No internet connection.
        TopGGHttpException
            Any exception raised by top.gg api.
        """
        return await self._request(
            METHOD_GET,
            f'{TOP_GG_ENDPOINT}/bots',
            StackedRateLimitHandler(self._rate_limit_handler_bots, self._rate_limit_handler_global),
            query_parameters = query_parameters,
        )
    
    
    async def _get_user_info(self, user_id):
        """
        Gets user info for the given user identifier.
        
        This method is a coroutine.
        
        Parameters
        ----------
        user_id : `int`
            The user's identifier to get.
            
        Returns
        -------
        response_data : `Any`
        
        Raises
        ------
        ConnectionError
            No internet connection.
        TopGGHttpException
            Any exception raised by top.gg api.
        """
        return await self._request(
            METHOD_GET,
            f'{TOP_GG_ENDPOINT}/users/{user_id}',
            RateLimitHandler(self._rate_limit_handler_global),
        )

    async def _get_user_vote(self, query_parameters):
        """
        Returns whether the user voted in the last 12 hours.
        
        This method is a coroutine.
        
        Parameters
        ----------
        query_parameters : `dict` of (`str`, `Any`) items
            Query parameters.
        
        Returns
        -------
        response_data : `Any`
        
        Raises
        ------
        ConnectionError
            No internet connection.
        TopGGHttpException
            Any exception raised by top.gg api.
        """
        return await self._request(
            METHOD_GET,
            f'{TOP_GG_ENDPOINT}/bots/{self.client_id}/check',
            RateLimitHandler(self._rate_limit_handler_global),
            query_parameters = query_parameters,
        )
    
    async def _request(self, method, url, rate_limit_handler, data=None, query_parameters=None):
        """
        Does a request towards top.gg API.
        
        This method is a coroutine.
        
        Parameters
        ----------
        method : `str`
            Http method.
        url : `str`
            Endpoint to do request towards.
        data : `None` or `Any`, Optional
            Json serializable data.
        rate_limit_handler : ``RateLimitHandlerBase`
            Rate limit handle to handle rate limit as.
        query_parameters : `None` or `Any`, Optional
            Query parameters
        
        Raises
        ------
        ConnectionError
            No internet connection.
        TopGGHttpException
            Any exception raised by top.gg api.
        """
        headers = self._headers.copy()
        
        if (data is not None):
            headers[CONTENT_TYPE] = 'application/json'
            data = to_json(data)
        
        try_again = 2
        while try_again > 0:
            global_rate_limit_expires_at = self._global_rate_limit_expires_at
            if global_rate_limit_expires_at > LOOP_TIME():
                future = Future(KOKORO)
                KOKORO.call_at(global_rate_limit_expires_at, Future.set_result_if_pending, future, None)
                await future
            
            async with rate_limit_handler.ctx():
                try:
                    async with RequestCM(self.http._request(method, url, headers, data, query_parameters)) as response:
                        response_data = await response.text(encoding='utf-8')
                except OSError as err:
                    if not try_again:
                        raise ConnectionError('Invalid address or no connection with Top.gg.') from err
                    
                    await sleep(0.5/try_again, KOKORO)
                    
                    try_again -= 1
                    continue
                
                response_headers = response.headers
                status = response.status
                
                content_type_headers = response_headers.get(CONTENT_TYPE, None)
                if (content_type_headers is not None) and content_type_headers.startswith('application/json'):
                    response_data = from_json(response_data)
                
                if 199 < status < 305:
                    return response_data
                
                # Are we rate limited?
                if status == 429:
                    try:
                        retry_after = headers[RETRY_AFTER]
                    except KeyError:
                        retry_after = RATE_LIMIT_GLOBAL_DEFAULT_DURATION
                    else:
                        try:
                            retry_after = float(retry_after)
                        except ValueError:
                            retry_after = RATE_LIMIT_GLOBAL_DEFAULT_DURATION
                    
                    self._global_rate_limit_expires_at = LOOP_TIME()+retry_after
                    await sleep(retry_after, KOKORO)
                    continue
                
                
                # Python casts sets to frozensets
                if (status in {400, 401, 402, 404}):
                    raise TopGGHttpException(response, response_data)
                
                if try_again and (status >= 500):
                    await sleep(10.0/try_again, KOKORO)
                    try_again -= 1
                    continue
                
                raise TopGGHttpException(response, response_data)
