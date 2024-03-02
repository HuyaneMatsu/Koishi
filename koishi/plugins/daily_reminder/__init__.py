from .builders import *
from .looping import *
from .queries import *
from .reminding import *
from .requests import *


__all__ = (
    *builders.__all__,
    *looping.__all__,
    *queries.__all__,
    *reminding.__all__,
    *requests.__all__,
)


# Begin looping

from ...bots import MAIN_CLIENT

@MAIN_CLIENT.events
async def ready(client):
    start_remind_loop()


@MAIN_CLIENT.events
async def shutdown(client):
    end_remind_loop()
