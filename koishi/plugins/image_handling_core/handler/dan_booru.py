__all__ = (
    'API_BASE_URL_DAN_BOORU', 'ImageHandlerDanBooru', 'PROVIDER_DAN_BOORU',
    'get_autocompletion_suggestions_dan_booru',
)

from collections import OrderedDict, deque as Deque
from itertools import count
from json import JSONDecodeError
from random import shuffle

from hata import KOKORO
from scarletio import Future, IgnoreCaseMultiValueDictionary, copy_docs, from_json
from scarletio.web_common import BasicAuthorization, URL
from scarletio.web_common.headers import METHOD_GET, USER_AGENT

from ..constants import AUTOCOMPLETE_PAGE_SIZE, BLACKLISTED_TAGS, PAGE_SIZE, RETRIES_MAX
from ..helpers import get_next_page_index, join_tags, join_tags_raw
from ..image_detail import ImageDetailProvided

from .request_base import HTTP_CLIENT, ImageHandlerRequestBase

from config import DAN_BOORU_PASSWORD, DAN_BOORU_USER_ID


API_BASE_URL_DAN_BOORU = URL('https://danbooru.donmai.us/')
PROVIDER_DAN_BOORU = 'danbooru'

HEADERS = IgnoreCaseMultiValueDictionary()
HEADERS[USER_AGENT] = 'koishi'

DAN_BOORU_AUTHORIZATION = BasicAuthorization(DAN_BOORU_USER_ID, DAN_BOORU_PASSWORD)

DAB_BOORU_REQUEST_CACHE = OrderedDict()
DAN_BOORU_REQUEST_CACHE_SIZE_MAX = 400


RATE_LIMIT_HANDLERS = set()
RATE_LIMIT_QUEUE = Deque()
RATE_LIMIT_INTERVAL = 1.0
RATE_LIMIT_CONCURRENCY = 10
RATE_LIMIT_ID_COUNTER = iter(count(1))


async def dan_booru_rate_limit_handler():
    """
    Dan booru rate limit handler.
    
    This function is an iterable coroutine.
    
    Yields
    ------
    enter : `None`
    """
    identifier = next(RATE_LIMIT_ID_COUNTER)
    
    if len(RATE_LIMIT_HANDLERS) < RATE_LIMIT_CONCURRENCY:
        RATE_LIMIT_HANDLERS.add(identifier)
    
    else:
        future = Future(KOKORO)
        RATE_LIMIT_QUEUE.appendleft((identifier, future))
        try:
            await future
        except:
            _rotate_rate_limit_handler(identifier)
            raise
    
    try:
        yield
    finally:
        KOKORO.call_after(RATE_LIMIT_INTERVAL, _rotate_rate_limit_handler, identifier)


def _rotate_rate_limit_handler(identifier):
    """
    Rotates the rate limit handler out.
    
    Parameters
    ----------
    identifier : `int`
        The rate limit handler's identifier.
    """
    RATE_LIMIT_HANDLERS.discard(identifier)
    if not RATE_LIMIT_QUEUE:
        return
    
    identifier, future = RATE_LIMIT_QUEUE.pop()
    RATE_LIMIT_HANDLERS.add(identifier)
    future.set_result(None)


# https://danbooru.donmai.us/wiki_pages/help:api


def parse_dan_booru_total_entry_count(data):
    """
    Parses dan booru entry count data.
    
    Parameters
    ----------
    data : `None | dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    total_entry_count : `int`
    """
    if data is None:
        return 0
    
    try:
        return data['counts']['posts']
    except KeyError:
        return 0


def parse_dan_booru_image_details(data, tags_required, tags_banned):
    """
    Parses dan booru posts response.
    
    Parameters
    ----------
    data : `None | dict<str, object>`
        Data to parse from.
    
    tags_required : `None | frozenset<str>`
        Tags to enable.
    
    tags_banned : `None | frozenset<str>`
        Tags to disable.
    
    Returns
    -------
    image_details : ``None | list<ImageDetailProvided>``
    """
    if data is None:
        return None
    
    image_details = None
    
    for post in data:
        url = post.get('file_url', None)
        tags = post.get('tag_string', None)
        if (url is None) or (tags is None):
            continue
        
        tags = frozenset(tags.split())
        if tags & BLACKLISTED_TAGS:
            continue
        
        if (tags_banned is not None) and (tags & tags_banned):
            continue
        
        if (tags_required is not None) and (not (tags & tags_required)):
            continue
        
        if image_details is None:
            image_details = []
        
        image_details.append(ImageDetailProvided(url).with_provider(PROVIDER_DAN_BOORU).with_tags(tags))

    return image_details


async def do_dan_booru_request(endpoint, query):
    """
    Does a get request towards the dan-booru api.
    
    This function is a coroutine.
    
    Parameters
    ----------
    endpoint : `str`
        The endpoint to do request towards.
    
    query : `tuple<(str, str)>`
        The query in hashable form.
    
    Returns
    -------
    response_json : `None | dict<str, object>`
    """
    key = (endpoint, query)
    
    try:
        response_json = DAB_BOORU_REQUEST_CACHE[key]
    except KeyError:
        pass
    else:
        DAB_BOORU_REQUEST_CACHE.move_to_end(key)
        return response_json
    
    retries_left = RETRIES_MAX
    
    while True:
        try:
            async for _ in dan_booru_rate_limit_handler():
                async with HTTP_CLIENT.request2(
                    METHOD_GET,
                    API_BASE_URL_DAN_BOORU / endpoint,
                    authorization = DAN_BOORU_AUTHORIZATION,
                    headers = HEADERS,
                    query = dict(query),
                ) as response:
                    if response.status != 200:
                        return None
                    
                    data = await response.read()
        
        except ConnectionResetError:
            pass
        
        else:
            break
        
        retries_left -= 1
        if retries_left <= 0:
            break
    
    try:
        response_json = from_json(data)
    except JSONDecodeError:
        response_json = None
    
    DAB_BOORU_REQUEST_CACHE[key] = response_json
    if len(DAB_BOORU_REQUEST_CACHE) > DAN_BOORU_REQUEST_CACHE_SIZE_MAX:
        del DAB_BOORU_REQUEST_CACHE[next(iter(DAB_BOORU_REQUEST_CACHE))]
    
    return response_json


class ImageHandlerDanBooru(ImageHandlerRequestBase):
    """
    Image handler requesting images from `danbooru`.
    
    Attributes
    ----------
    _cache : ``list<ImageDetailBase>``
        Additional requested image details.
    
    _page : `int`
        The next page to request.
    
    _random_order : `bool`
        Whether images should be shown in random order.
    
    _request_task : ``None | Task<._request_loop>``
        Active request loop.
    
    _tags_banned : `None | frozenset<str>`
        Additionally banned tags for filtering.
    
    _tags_required : `None | frozenset<str>`
        Additional required tags for filtering.
    
    _tags_joined : `str`
        The joined tags to request.
    
    _tags_joined_raw : `str`
        The joined tags to request without extra filtering tags added.
    
    _waiters : ``Deque<Future>``
        Waiter futures for image detail.
    """
    __slots__ = ('_page', '_random_order', '_tags_banned', '_tags_joined', '_tags_joined_raw', '_tags_required')
    
    def __new__(cls, tags_required, tags_banned, tags_requested, random_order):
        """
        Creates a dan-booru image handler.
        
        Parameters
        ----------
        tags_required : `None | frozenset<str>`
            Tags to enable.
        
        tags_banned : `None | frozenset<str>`
            Tags to disable.
        
        tags_requested : `set<(bool, str)>`
            The requested tags.
        
        random_order : `bool`
            Whether images should be shown in random order.
        """
        tags_joined = join_tags(tags_required, tags_banned, tags_requested)
        tags_joined_raw = join_tags_raw(tags_required, tags_banned, tags_requested)
        
        self = ImageHandlerRequestBase.__new__(cls)
        self._page = 0
        self._random_order = random_order
        self._tags_joined = tags_joined
        self._tags_joined_raw = tags_joined_raw
        self._tags_banned = tags_banned
        self._tags_required = tags_required
        return self
    
    
    @copy_docs(ImageHandlerRequestBase.__eq__)
    def __eq__(self, other):
        if type(self) is not type(other):
            return NotImplemented
        
        if self._random_order != other._random_order:
            return False
        
        if self._tags_joined != other._tags_joined:
            return False
        
        return True
    
    
    @copy_docs(ImageHandlerRequestBase._produce_representation_middle)
    def _produce_representation_middle(self):
        yield ' random_order = '
        yield repr(self._random_order)
        
        yield ', tags_joined = '
        yield repr(self._tags_joined)
    
    
    @copy_docs(ImageHandlerRequestBase._request)
    async def _request(self):
        response_json = await do_dan_booru_request(
            'counts/posts.json',
            (
                ('tags', self._tags_joined),
            ),
        )
        total_entry_count = parse_dan_booru_total_entry_count(response_json)
        if not total_entry_count:
            return None
        
        response_json = await do_dan_booru_request(
            'posts.json',
            (
                ('limit', str(PAGE_SIZE)),
                ('page', str(self._page)),
                ('tags', self._tags_joined_raw),
            ),
        )
        
        image_details = parse_dan_booru_image_details(response_json, self._tags_required, self._tags_banned)
        self._page = get_next_page_index(self._page, total_entry_count, self._random_order)
        
        if (image_details is None):
            return
        
        if self._random_order:
            shuffle(image_details)
        
        return image_details


async def get_autocompletion_suggestions_dan_booru(query, tags_banned):
    """
    Gets auto completion suggestions for dan booru queries.
    
    This function is a coroutine.
    
    Parameters
    ----------
    query : `str`
        String to query for.
    
    tags_banned : `None | frozenset<str>`
        Tags to disable.
    
    Returns
    -------
    suggestions : `None | list<(str, str)>`
    """
    response_json = await do_dan_booru_request(
        'autocomplete.json',
        (
            ('search[query]', query),
            ('search[type]', 'tag_query'),
            ('limit', str(AUTOCOMPLETE_PAGE_SIZE)),
        ),
    )
    
    if (response_json is None):
        return None
    
    suggestions = None
    
    for element in response_json:
        element_type = element['type']
        
        if element_type == 'tag-word':
            tag_suggestion = element['tag']
            
            value = tag_suggestion['name']
            if value in BLACKLISTED_TAGS:
                continue
            
            if (tags_banned is not None) and (value in tags_banned):
                continue
            
            count = tag_suggestion['post_count']
            name = f'{value} ({count})'
        
        elif element_type == 'static':
            name = value = element['value']
        
        else:
            continue
        
        if suggestions is None:
            suggestions = []
        
        suggestions.append((name, value))
    
    return suggestions
