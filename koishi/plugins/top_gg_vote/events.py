__all__ = ()

from sys import modules

from ...bot_utils.external_event_types import EXTERNAL_EVENT_TYPE_TOP_GG_VOTE

from ..external_events import add_handler, remove_handler

from .top_gg_vote import handle_top_gg_vote


def setup(module):
    """
    Called after the module is loaded.
    
    Parameters
    ----------
    module : ``ModuleType``
        This module.
    """
    if 'vampytest' not in modules:
        add_handler(EXTERNAL_EVENT_TYPE_TOP_GG_VOTE, handle_top_gg_vote)


def teardown(module):
    """
    Called after the module is unloaded.
    
    Parameters
    ----------
    module : ``ModuleType``
        This module.
    """
    if 'vampytest' not in modules:
        remove_handler(EXTERNAL_EVENT_TYPE_TOP_GG_VOTE, handle_top_gg_vote)
