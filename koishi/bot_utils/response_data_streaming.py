__all__ = ('create_http_stream_resource',)

from scarletio.streaming import ResourceStreamFunction


@ResourceStreamFunction
async def create_http_stream_resource(http_client, url):
    """
    Creates an http stream resource.
    
    This function is a coroutine generator.
    
    Parameters
    ----------
    http_client : ``HTTPClient``
        Http client to request the url with.
    
    url : `str`
        Url to request.
    """
    response = await http_client.get(url)
    payload_stream = response.payload_stream
    if (payload_stream is not None):
        async for chunk in payload_stream:
            yield chunk
