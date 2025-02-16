__all__ = ('AttachmentStream',)

from scarletio import RichAttributeErrorBaseType


class AttachmentStream(RichAttributeErrorBaseType):
    """
    Streams an attachment.
    
    Parameters
    ----------
    done : `bool`
        Whether streaming is done.
    
    http_client : ``HTTPClient``
        http client.
    
    payload_iterator : ``CoroutineGenerator``
        Iterator over a payload stream.
    
    url : `str`
        The streamed url as a string.
    """
    __slots__ = ('done', 'http_client', 'payload_iterator', 'url')
    
    def __new__(cls, url, http_client):
        self = object.__new__(cls)
        self.done = False
        self.http_client = http_client
        self.payload_iterator = None
        self.url = url
        return self
    
    
    def __aiter__(self):
        """
        Starts async iterating over the payload stream.
        
        Returns
        -------
        self : `self`
        """
        self.payload_iterator = None
        self.done = False
        return self
    
    
    async def __anext__(self):
        """
        Steps the payload stream returning the next chunk.
        
        Returns
        -------
        chunk : `bytes | memoryview`
            The next chunk of data.
        
        Raises
        ------
        StopAsyncIteration
        """
        if self.done:
            raise StopAsyncIteration()
        
        payload_iterator = self.payload_iterator
        if (payload_iterator is None):
            response = await self.http_client.get(self.url)
            payload_stream = response.payload_stream
            if payload_stream is None:
                self.done = True
                raise StopAsyncIteration()
            
            payload_iterator = payload_stream.__aiter__()
            self.payload_iterator = payload_iterator
        
        try:
            chunk = await payload_iterator.asend(None)
        except:
            self.done = True
            self.payload_iterator = None
            raise

        return chunk
    
    
    def __repr__(self):
        """Returns repr(self)."""
        repr_parts = ['<', type(self).__name__]
        
        # url
        repr_parts.append(' url = ')
        repr_parts.append(repr(self.url))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
