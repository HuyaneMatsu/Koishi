__all__ = ('exclude_handler_types',)

from .handler import ImageHandlerGroup


def _exclude_handler_types(handler, handler_types_to_exclude):
    """
    Returns `None` if the given handler type is excluded.
    
    Parameters
    ----------
    handler : ``ImageHandlerBase``
        Handler to exclude from.
    
    handler_types_to_exclude : ``tuple<type<ImageHandlerBase>>``
        Handler types to exclude.
    
    Returns
    -------
    handler : ``None | ImageHandlerBase``
    """
    return None if isinstance(handler, handler_types_to_exclude) else handler


def _exclude_handler_types_from_group(handler, handler_types_to_exclude):
    """
    Exclude handlers of the given group handler.
    
    Parameters
    ----------
    handler : ``ImageHandlerGroup``
        Handler to exclude from.
    
    handler_types_to_exclude : ``tuple<type<ImageHandlerBase>>``
        Handler types to exclude.
    
    Returns
    -------
    handler : ``None | ImageHandlerBase``
    """
    handlers_filtered = []
    handlers_unfiltered = handler._handlers
    for sub_handler in handlers_unfiltered:
        sub_handler = _exclude_handler_types(sub_handler, handler_types_to_exclude)
        if (sub_handler is not None):
            handlers_filtered.append(sub_handler)
    
    handlers_length = len(handlers_filtered)
    if handlers_length == 0:
        handler = None
    
    elif handlers_length == 1:
        handler = handlers_filtered[0]
    
    elif handlers_length == len(handlers_unfiltered):
        pass
    
    else:
        handler = type(ImageHandlerGroup)(*handlers_unfiltered)
    
    return handler


def exclude_handler_types(handler, handler_types_to_exclude):
    """
    Returns a new handler excluding the given handler types from itself.
    
    Parameters
    ----------
    handler : ``ImageHandlerBase``
        Handler to exclude from.
    
    handler_types_to_exclude : ``tuple<type<ImageHandlerBase>>``
        Handler types to exclude.
    
    Returns
    -------
    handler : ``None | ImageHandlerBase``
    """
    return (_exclude_handler_types_from_group if isinstance(handler, ImageHandlerGroup) else _exclude_handler_types)(
        handler, handler_types_to_exclude
    )
