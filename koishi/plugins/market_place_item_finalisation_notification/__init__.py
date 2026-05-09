from .component_building import *
from .looping import *
from .notifier import *
from .queries import *


__all__ = (
    *component_building.__all__,
    *looping.__all__,
    *notifier.__all__,
    *queries.__all__,
)


# Begin looping

from ...bots import MAIN_CLIENT


@MAIN_CLIENT.events
async def ready(client):
    REMINDER_LOOPER.start()


@MAIN_CLIENT.events
async def shutdown(client):
    REMINDER_LOOPER.stop()
