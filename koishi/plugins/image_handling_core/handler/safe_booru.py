__all__ = (
    'API_BASE_URL_SAFE_BOORU', 'ImageHandlerSafeBooru', 'PROVIDER_SAFE_BOORU',
    'get_autocompletion_suggestions_safe_booru'
)

from json import JSONDecodeError
from random import shuffle

from scarletio import copy_docs, from_json
from scarletio.web_common import URL

from ....bot_utils.tools import BeautifulSoup

from ..constants import BLACKLISTED_TAGS, RETRIES_MAX
from ..helpers import get_next_page_index, join_tags
from ..image_detail import ImageDetailProvided

from .request_base import ImageHandlerRequestBase, HTTP_CLIENT


API_BASE_URL_SAFE_BOORU = URL('https://safebooru.org/')
PROVIDER_SAFE_BOORU = 'safebooru'


def parse_safe_booru_response(data):
    """
    Parses safe booru response.
    
    Parameters
    ----------
    data : `bytes`
        Data to parse.
    
    Returns
    -------
    total_entry_count_and_image_details : ``(int, None | list<ImageDetailProvided>)``
    """
    soup = BeautifulSoup(data, 'lxml')
    posts = soup.find('posts')
    
    # Bad structure ?
    if posts is None:
        return 0, None
    
    image_details = None
    
    # Process data
    for post in soup.find_all('post'):
        url = post.get('file_url')
        tags = post.get('tags')
        if (url is None) or (tags is None):
            continue
        
        tags = frozenset(tags.split())
        if tags & BLACKLISTED_TAGS:
            continue
        
        if image_details is None:
            image_details = []
        
        image_details.append(ImageDetailProvided(url).with_provider(PROVIDER_SAFE_BOORU).with_tags(tags))

    return int(posts['count']), image_details


class ImageHandlerSafeBooru(ImageHandlerRequestBase):
    """
    Image handler requesting images from `safebooru`.
    
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
    
    _tags_joined : `str`
        The joined tags to request.
    
    _waiters : ``Deque<Future>``
        Waiter futures for image detail.
    """
    __slots__ = ('_page','_random_order', '_tags_joined')
    
    def __new__(cls, tags_required, tags_banned, tags_requested, random_order):
        """
        Creates a safe-booru image handler.
        
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
        joined_tags = join_tags(tags_required, tags_banned, tags_requested)
        
        self = ImageHandlerRequestBase.__new__(cls)
        self._page = 0
        self._random_order = random_order
        self._tags_joined = joined_tags
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
        retries_left = RETRIES_MAX
        
        while True:
            try:
                async with HTTP_CLIENT.get(
                    API_BASE_URL_SAFE_BOORU / 'index.php',
                    query = {
                        'pid': self._page,
                        'page': 'dapi',
                        's': 'post',
                        'q': 'index',
                        'tags': self._tags_joined,
                    },
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
                return None
        
        
        total_entry_count, image_details = parse_safe_booru_response(data)
        self._page = get_next_page_index(self._page, total_entry_count, self._random_order)
        
        if (image_details is None):
            return
        
        if self._random_order:
            shuffle(image_details)
        
        return image_details


def _unquote_tag_safe_booru(tag):
    """
    Unquotes a safe-booru tag.
    
    Parameters
    ----------
    tag : `str`
        The tag to process.
    
    Returns
    -------
    raw_tag : `str`
    """
    return tag.replace('&#039', '\'')


async def get_autocompletion_suggestions_safe_booru(query, tags_banned):
    """
    Gets auto completion suggestions for safe booru queries.
    
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
    async with HTTP_CLIENT.get(
        API_BASE_URL_SAFE_BOORU / 'autocomplete.php',
        query = {
            'q': query,
        },
    ) as response:
        if response.status != 200:
            return None
        
        data = await response.read()
    
    try:
        response_json = from_json(data)
    except JSONDecodeError:
        return None
    
    suggestions = None
    
    for element in response_json:
        value = _unquote_tag_safe_booru(element['value'])
        if value in BLACKLISTED_TAGS:
            continue
        
        if (tags_banned is not None) and (value in tags_banned):
            continue
        
        if suggestions is None:
            suggestions = []
        
        suggestions.append((_unquote_tag_safe_booru(element['label']), value))
    
    return suggestions
