__all__ = ('API_BASE_URL_MEEK_MOE', 'ImageHandlerMeekMoe', 'PROVIDER_MEEK_MOE')

from scarletio import copy_docs
from scarletio.web_common import URL

from ..image_detail import ImageDetailProvided

from .request_base import HTTP_CLIENT, ImageHandlerRequestBase


API_BASE_URL_MEEK_MOE = URL('https://api.meek.moe/')
PROVIDER_MEEK_MOE = 'meek.moe'


class ImageHandlerMeekMoe(ImageHandlerRequestBase):
    """
    Image handler requesting images from `waifu.pics`.
    
    Attributes
    ----------
    _cache : ``list<ImageDetailBase>``
        Additional requested image details.
    
    _request_task : ``None | Task<._request_loop>``
        Active request loop.
    
    _waiters : ``Deque<Future>``
        Waiter futures for image detail.
    
    _vocaloid_type : `str`
        The url to do request towards.
    """
    __slots__ = ('_vocaloid_type',)
    
    def __new__(cls, vocaloid_type):
        """
        Creates a meek.moe image handler.
        
        Parameters
        ----------
        vocaloid_type : `str`
            The vocaloid's type.
        """
        self = ImageHandlerRequestBase.__new__(cls)
        self._vocaloid_type = vocaloid_type
        return self
    
    
    @copy_docs(ImageHandlerRequestBase.__eq__)
    def __eq__(self, other):
        if type(self) is not type(other):
            return NotImplemented
        
        if self._vocaloid_type != other._vocaloid_type:
            return False
        
        return True
    
    
    @copy_docs(ImageHandlerRequestBase._produce_representation_middle)
    def _produce_representation_middle(self):
        yield ' vocaloid_type = '
        yield repr(self._vocaloid_type)
    
    
    @copy_docs(ImageHandlerRequestBase._request)
    async def _request(self):
        try:
            async with HTTP_CLIENT.get(API_BASE_URL_MEEK_MOE / self._vocaloid_type) as response:
                if response.status != 200:
                    return None
                
                data = await response.json()
        except TimeoutError:
            return None
        
        if not isinstance(data, dict):
            return None
        
        return [ImageDetailProvided(data['url']).with_provider(PROVIDER_MEEK_MOE)]
