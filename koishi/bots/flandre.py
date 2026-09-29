__all__ = ('Flandre',)

from hata import Activity, Client, IntentFlag

import config


Flandre = Client(
    config.FLANDRE_TOKEN,
    client_id = config.FLANDRE_ID,
    activity = Activity('in the basement.'),
    should_request_users = False,
    intents = IntentFlag().update_by_keys(
        guild_presences = False,
    ),
    application_id = config.FLANDRE_ID,
    extensions = ('slash',),
)
