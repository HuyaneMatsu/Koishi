__all__ = ('ImageHandlerMeekMoe', )

from scarletio import copy_docs

from ..image_detail import ImageDetail

from .request_base import ImageHandlerRequestBase


MEEK_API_BASE_URL = 'https://api.meek.moe'
PROVIDER = 'meek.moe'


class ImageHandlerMeekMoe(ImageHandlerRequestBase):
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
    _url : `str`
        The url to do request towards.
    """
    __slots__ = ('_url',)
    
    def __new__(cls, vocaloid_type):
        """
        Parameters
        ----------
        vocaloid_type : `str`
            The vocaloid's type.
        """
        self = ImageHandlerRequestBase.__new__(cls)
        self._url = f'{MEEK_API_BASE_URL}/{vocaloid_type}'
        return self
    
    
    @copy_docs(ImageHandlerRequestBase._request)
    async def _request(self, client):
        async with client.http.get(self._url) as response:
            if response.status == 200:
                data = await response.json()
            else:
                data = None
        
        return data
    
    
    @copy_docs(ImageHandlerRequestBase._process_data)
    def _process_data(self, data):
        if not isinstance(data, dict):
            return
        
        return [ImageDetail(data['url'], None, PROVIDER)]
