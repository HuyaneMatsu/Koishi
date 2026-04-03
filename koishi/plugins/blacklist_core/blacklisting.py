__all__ = ()

from .queries import is_user_id_in_blacklist

from hata.ext.slash import Slasher


async def blacklisted_call(slasher, client, event):
    """
    Assigned as `Slasher.__call__` to first check whether the user is blacklisted or nah.
    
    This function is a coroutine.
    
    Parameters
    ----------
    slasher : ``Slasher``
        Interaction processor.
    client : ``Client``
        The client who received the event.
    event : ``InteractionEvent``
        The received interaction event.
    """
    if not is_user_id_in_blacklist(event.user_id):
        await slasher._original__call__(client, event)


def setup(module):
    """
    Called when the plugin is loaded. Replaces ``Slasher.__call__`` with ``blacklisted_call``.
    
    Parameters
    ----------
    module : ``ModuleType``
        This module.
    """
    if getattr(Slasher, '_original__call__', None) is None:
        Slasher._original__call__ = Slasher.__call__
    Slasher.__call__ = blacklisted_call


def teardown(module):
    """
    Called when the plugin is unloaded. Resets ``Slasher.__call__``.
    
    Parameters
    ----------
    module : ``ModuleType``
        This module.
    """
    original_call = getattr(Slasher, '_original__call__', None)
    if original_call is not None:
        Slasher.__call__ = original_call
