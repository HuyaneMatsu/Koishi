__all__ = ('add_handler', 'remove_handler')


HANDLERS = {}


def add_handler(event_type, handler):
    """
    Adds an external event handler.
    
    Parameters
    ----------
    event_type : `int`
        The event's type.
    
    handler : `CoroutineFunctionType`
        Handler to ensure when a related event is received.
    """
    HANDLERS[event_type] = handler


def remove_handler(event_type, handler):
    """
    Removes an external event handler.
    
    Parameters
    ----------
    event_type : `int`
        The event's type.
    
    handler : `CoroutineFunctionType`
        Handler to ensure when a related event is received.
    """
    if HANDLERS.get(event_type, None) is handler:
        del HANDLERS[event_type]
