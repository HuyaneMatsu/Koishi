__all__ = ('ImageHandlerBooru',)

from random import random, shuffle
from math import ceil, floor

from scarletio import copy_docs
from scarletio.web_common import quote

from ....bot_utils.tools import BeautifulSoup

from ..image_detail import ImageDetail

from .request_base import ImageHandlerRequestBase


PAGE_SIZE = 100
RETRIES_MAX = 5

def make_url(api_endpoint, required_tags, banned_tags, requested_tags):
    """
    Builds a booru url from the given details.
    
    Parameters
    ----------
    api_endpoint : `str`
        Base url of the service.
    required_tags : `None`, `frozenset` of `str`
        Tags to always extend `tags` with.
    banned_tags : `None`, `frozenset` of `str`
        tags to remove from `tags`.
    requested_tags : `set` of `str`
        Tags to request.
    
    Returns
    -------
    url : `str`
    """
    url_parts = [api_endpoint, '/index.php?page=dapi&s=post&q=index&tags=']
    is_tag_first = True
    
    for tag in requested_tags:
        if tag not in banned_tags:
            if is_tag_first:
                is_tag_first = False
            else:
                url_parts.append('+')
            url_parts.append(quote(tag))
    
    if (required_tags is not None):
        for tag in required_tags:
            if (tag not in requested_tags):
                if is_tag_first:
                    is_tag_first = False
                else:
                    url_parts.append('+')
                url_parts.append(quote(tag))
    
    for tag in banned_tags:
        if is_tag_first:
            is_tag_first = False
        else:
            url_parts.append('+')
        url_parts.append('-')
        url_parts.append(quote(tag))
    
    return ''.join(url_parts)


def booru_post_parser_generic(post):
    """
    Parses a generic booru post.
    
    Parameters
    ----------
    post : ``BeautifulSoup``
        Response post.
    
    Returns
    -------
    file_url : `str`
    tags : `str`
    """
    return post.get('file_url'), post.get('tags')


def booru_post_parser_gel(post):
    """
    Parses a gebbooru post.
    
    Parameters
    ----------
    post : ``BeautifulSoup``
        Response post.
    
    Returns
    -------
    file_url : `str`
    tags : `str`
    """
    return post.find('file_url').string, post.find('tags').string



def get_post_parser(api_endpoint):
    """
    Gets the post parser of the given endpoint.
    
    Parameters
    ----------
    api_endpoint : `str`
        Base url of the service.
    
    Returns
    -------
    post_parser : `FunctionType`
    """
    if 'gelbooru.com' in api_endpoint:
        return booru_post_parser_gel
    
    return booru_post_parser_generic


class ImageHandlerBooru(ImageHandlerRequestBase):
    """
    Image handler requesting images from `waifu.pics`.
    
    Attributes
    ----------
    _cache : `list` of ``ImageDetail``
        Additional requested card details.
    _waiters : `Deque` of ``Future``
        Waiter futures for card detail.
    _request_task : `None`, ``Task`` of ``._request_loop``
        Active request loop.
    _page : `int`
        The next page to request.
    _post_parser : `FunctionType`
        Function type to use to parse a post. Different services might have different post format.
    _provider : `str`
        Specific provider added to image details.
    _random_order : `bool`
        Whether images should be shown in random order.
    _url : `str`
        The url to do request towards.
    """
    __slots__ = ('_page', '_post_parser', '_provider', '_random_order', '_url',)
    
    def __new__(cls, provider, api_endpoint, required_tags, banned_tags, requested_tags, random_order):
        """
        Creates a booru image handler.
        
        Parameters
        ----------
        provider : `str`
            Specific provider added to image details.
        api_endpoint : `str`
            Base url of the service.
        required_tags : `None`, `frozenset` of `str`
            Tags to always extend `tags` with.
        banned_tags : `None`, `frozenset` of `str`
            tags to remove from `tags`.
        requested_tags : `set` of `str`
            Tags to request.
        random_order : `bool`
            Whether images should be shown in random order.
        """
        url = make_url(api_endpoint, required_tags, banned_tags, requested_tags)
        post_parser = get_post_parser(api_endpoint)
        self = ImageHandlerRequestBase.__new__(cls)
        self._page = 0
        self._post_parser = post_parser
        self._provider = provider
        self._random_order = random_order
        self._url = url
        return self
    
    
    @copy_docs(ImageHandlerRequestBase._request)
    async def _request(self, client):
        retries_left = RETRIES_MAX
        
        while True:
            try:
                async with client.http.get(f'{self._url}&pid={self._page}') as response:
                    if response.status == 200:
                        data = await response.read()
                    else:
                        data = None
            
            except ConnectionResetError:
                pass
            
            else:
                return data
            
            retries_left -= 1
            if retries_left <= 0:
                break
    
    
    @copy_docs(ImageHandlerRequestBase._process_data)
    def _process_data(self, data):
        soup = BeautifulSoup(data, 'lxml')
        
        random_order = self._random_order
        
        posts = soup.find('posts')
        # Bad structure ?
        if posts is None:
            return None
        
        # Increment page index
        total = int(posts['count'])
        
        page = self._page
        
        if random_order:
            page_count = ceil((total + PAGE_SIZE) / PAGE_SIZE) - 1
            if page_count <= 1:
                page = 0
            
            else:
                new_page = floor(page_count * random() ** 2)
                if page != new_page:
                    page = new_page
                
                elif new_page == page_count:
                    page = new_page - 1
                
                else:
                    page = new_page + 1
        
        else:
            page += 1
            leftover = total - page * PAGE_SIZE
            if leftover <= 0:
                page = 0
        
        self._page = page
        
        image_details = []
        # Process data
        post_parser = self._post_parser
        for post in soup.find_all('post'):
            url, tags = post_parser(post)
            if (url is not None) and (tags is not None):
                image_details.append(ImageDetail(url, frozenset(tags.split()), self._provider))
        
        if random_order:
            shuffle(image_details)
        
        return image_details
