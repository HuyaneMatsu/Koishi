__all__ = ('API_BASE_URL_WAIFU_PICS', 'ImageHandlerWaifuPics', 'PROVIDER_WAIFU_PICS')

from scarletio import IgnoreCaseMultiValueDictionary, copy_docs
from scarletio.web_common import URL
from scarletio.web_common.headers import CONTENT_TYPE

from ...user_settings import PREFERRED_IMAGE_SOURCE_WAIFU_PICS

from ..image_detail import ImageDetailProvided

from .request_base import HTTP_CLIENT, ImageHandlerRequestBase


API_BASE_URL_WAIFU_PICS = URL('https://api.waifu.pics/')
PROVIDER_WAIFU_PICS = 'waifu.pics'

HEADERS = IgnoreCaseMultiValueDictionary()
HEADERS[CONTENT_TYPE] = 'application/json'
DATA = b'{}'


BLACKLIST = {
    # Explicit
    'https://i.waifu.pics/sqndUwO.gif',
    'https://i.waifu.pics/JxQolYt.gif',
    'https://i.waifu.pics/eKNeUOR.gif',
    
    # Holocringe
    'https://i.waifu.pics/tvSCzkl.gif',
    'https://i.waifu.pics/jFOkv3O.gif',
    'https://i.waifu.pics/GNw8eK7.gif',
    'https://i.waifu.pics/PCTp3I3.gif',
    
    # Bully looking sus
    'https://i.waifu.pics/MjULOe4.gif',
    
    # Glitchy
    'https://i.waifu.pics/j63gPVc.gif',
    
    # In touhou pool
    'https://i.waifu.pics/szHC1yJ.gif',
    
    # not well formed url
    'https://i.waifu.pics/OXM9FcR. - Episode 4 - Eurynome Disgusted Look.gif',
}


class ImageHandlerWaifuPics(ImageHandlerRequestBase):
    """
    Image handler requesting images from `waifu.pics`.
    
    Attributes
    ----------
    _cache : ``list<ImageDetailBase>``
        Additional requested image details.
    
    _request_task : ``None | Task<._request_loop>``
        Active request loop.
    
    _safe : `bool`
        Whether to request safe images.
    
    _waifu_type : `str`
        The url to do request towards.
    
    _waiters : ``Deque<Future>``
        Waiter futures for image detail.
    """
    __slots__ = ('_safe', '_waifu_type')
    
    def __new__(cls, waifu_type, safe):
        """
        Creates a waifu.pics image handler.
        
        Parameters
        ----------
        waifu_type : `str`
            The waifu's type.
        
        safe : `bool`
        Whether to request safe images.
        """
        self = ImageHandlerRequestBase.__new__(cls)
        self._safe = safe
        self._waifu_type = waifu_type
        return self
    
    
    @copy_docs(ImageHandlerRequestBase.__eq__)
    def __eq__(self, other):
        if type(self) is not type(other):
            return NotImplemented
        
        if self._safe != other._safe:
            return False
        
        if self._waifu_type != other._waifu_type:
            return False
        
        return True
    
    
    @copy_docs(ImageHandlerRequestBase._produce_representation_middle)
    def _produce_representation_middle(self):
        yield ' safe = '
        yield repr(self._safe)
        
        yield ', waifu_type = '
        yield repr(self._waifu_type)
    
    
    @copy_docs(ImageHandlerRequestBase._request)
    async def _request(self):
        try:
            async with HTTP_CLIENT.post(
                API_BASE_URL_WAIFU_PICS / 'many' / ('sfw' if self._safe else 'nsfw') / self._waifu_type,
                headers = HEADERS,
                data = DATA,
            ) as response:
                if response.status != 200:
                    return None
                
                if 'json' not in response.headers.get(CONTENT_TYPE, '').casefold():
                    return None
                
                data = await response.json()
        except TimeoutError:
            return None
        
        if not isinstance(data, dict):
            return None
        
        try:
            urls = data['files']
        except KeyError:
            return None
        
        return [ImageDetailProvided(url).with_provider(PROVIDER_WAIFU_PICS) for url in urls if url not in BLACKLIST]

    
    @copy_docs(ImageHandlerRequestBase.get_image_source)
    def get_image_source(self):
        return PREFERRED_IMAGE_SOURCE_WAIFU_PICS
