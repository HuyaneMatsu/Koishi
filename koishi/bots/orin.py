__all__ = ('Orin',)

from hata import Client, IntentFlag, Status

import config


Orin = Client(
    config.ORIN_TOKEN,
    client_id = config.ORIN_ID,
    status = Status.dnd,
    should_request_users = False,
    intents = IntentFlag().update_by_keys(
        guild_presences = False,
    ),
    application_id = config.ORIN_ID,
    extensions = ('slash',),
)
