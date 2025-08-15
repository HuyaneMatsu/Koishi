from .component_builders import *
from .custom_ids import *
from .duration_suggesting import *
from .interactions import *
from .location_suggesting import *
from .notifications import *
from .target_suggesting import *


__all__ = (
    *component_builders.__all__,
    *custom_ids.__all__,
    *duration_suggesting.__all__,
    *interactions.__all__,
    *location_suggesting.__all__,
    *notifications.__all__,
    *target_suggesting.__all__,
)


from ..adventure_core import set_adventure_return_notifier


def setup(module):
    """
    Called when the plugin is loaded. Sets notifiers.
    """
    set_adventure_return_notifier(adventure_return_notifier)


def teardown(module):
    """
    Called when the plugin is unloaded. Removes the notifiers.
    """
    set_adventure_return_notifier(None)
