__all__ = ('ImageHandlerWaifuPics', )

from scarletio import IgnoreCaseMultiValueDictionary, copy_docs
from scarletio.web_common.headers import CONTENT_TYPE

from ...user_settings import PREFERRED_IMAGE_SOURCE_WAIFU_PICS

from ..image_detail import ImageDetailProvided

from .request_base import ImageHandlerRequestBase


WAIFU_API_BASE_URL = 'https://api.waifu.pics'
PROVIDER = 'waifu.pics'

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
    _cache : `list` of ``ImageDetailBase``
        Additional requested card details.
    _waiters : `Deque` of ``Future``
        Waiter futures for card detail.
    _request_task : `None`, ``Task`` of ``._request_loop``
        Active request loop.
    _url : `str`
        The url to do request towards.
    """
    __slots__ = ('_url',)
    
    def __new__(cls, waifu_type, nsfw):
        """
        Parameters
        ----------
        waifu_type : `str`
            The waifu's type.
        nsfw : `bool`
            Ara ara.
        """
        self = ImageHandlerRequestBase.__new__(cls)
        self._url = f'{WAIFU_API_BASE_URL}/many/{"n" if nsfw else ""}sfw/{waifu_type}'
        return self
    
    
    @copy_docs(ImageHandlerRequestBase.__eq__)
    def __eq__(self, other):
        if type(self) is not type(other):
            return NotImplemented
        
        if self._url != other._url:
            return False
        
        return True
    
    
    @copy_docs(ImageHandlerRequestBase._request)
    async def _request(self, client):
        try:
            async with client.http.post(self._url, headers = HEADERS, data = DATA) as response:
                if response.status != 200:
                    data = None
                
                elif 'json' not in response.headers.get(CONTENT_TYPE, '').casefold():
                    data = None
                
                else:
                    data = await response.json()
        except TimeoutError:
            data = None
        
        return data
    
    
    @copy_docs(ImageHandlerRequestBase._process_data)
    def _process_data(self, data):
        if not isinstance(data, dict):
            return
        
        try:
            urls = data['files']
        except KeyError:
            return None
        
        return [ImageDetailProvided(url).with_provider(PROVIDER) for url in urls if url not in BLACKLIST]

    
    @copy_docs(ImageHandlerRequestBase.get_image_source)
    def get_image_source(self):
        return PREFERRED_IMAGE_SOURCE_WAIFU_PICS
