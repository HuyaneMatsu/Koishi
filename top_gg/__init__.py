from .bots_query import *
from .client import *
from .constants import *
from .exceptions import *
from .rate_limit_handling import *
from .types import *

__all__ = (
    'setup_ext_top_gg',
    *bots_query.__all__,
    *client.__all__,
    *constants.__all__,
    *exceptions.__all__,
    *rate_limit_handling.__all__,
    *types.__all__,
)

# Implement setup function

from .client import _start_auto_post, _stop_auto_post

def setup_ext_top_gg(client, *args, **kwargs):
    """
    Setups the top.gg extension on client.
    
    Note, that this function can be called on a client only once.
    
    Parameters
    ----------
    client : ``Client``
        The client to setup the extension on.

    **kwargs : Keyword parameters
        Additional keyword parameter to be passed to the created ``Slasher``.
    **kwargs : Keyword parameters
        Additional keyword parameter to be passed to the created ``Slasher``.
    
    Other Parameters
    ----------------
    top_gg_token : `str`
        Top.gg api token.
    
    Returns
    -------
    top_gg_client : ``Slasher``
        Top gg client added to the client.
    
    Raises
    ------
    RuntimeError
        If the client has an attribute set what the top.gg client would use.
    TypeError
        - If `client` is not ``Client`` instance.
        - If `top_gg_token` is not `str` instance.
    """
    if hasattr(client, 'top_gg_client'):
        raise RuntimeError(f'The client already has `top_gg_client` attribute; got {client!r}.')
    
    top_gg_client = TopGGClient(client, *args, **kwargs)
    
    client.top_gg_client = top_gg_client
    client.events(_start_auto_post, name='launch')
    client.events(_stop_auto_post, name='shutdown')
    
    return top_gg_client

# Register extension

from hata.ext import register_library_extension, register_setup_function

register_library_extension('HuyaneMatsu.top_gg')

register_setup_function(
    'HuyaneMatsu.top_gg',
    setup_ext_top_gg,
    (
        'top_gg_token',
    ),
    None,
)
