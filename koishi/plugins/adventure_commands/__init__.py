from .component_building import *
from .constants import *
from .content_building import *
from .custom_ids import *
from .duration_suggesting import *
from .goal_item_suggesting import *
from .interactions import *
from .location_suggesting import *
from .notifications import *
from .target_suggesting import *


__all__ = (
    *component_building.__all__,
    *constants.__all__,
    *content_building.__all__,
    *custom_ids.__all__,
    *duration_suggesting.__all__,
    *goal_item_suggesting.__all__,
    *interactions.__all__,
    *location_suggesting.__all__,
    *notifications.__all__,
    *target_suggesting.__all__,
)


from ..adventure_core import set_adventure_action_notifier, set_adventure_return_notifier


def setup(module):
    """
    Called when the plugin is loaded. Sets notifiers.
    """
    set_adventure_action_notifier(adventure_action_notifier)
    set_adventure_return_notifier(adventure_return_notifier)


def teardown(module):
    """
    Called when the plugin is unloaded. Removes the notifiers.
    """
    set_adventure_action_notifier(None)
    set_adventure_return_notifier(None)
