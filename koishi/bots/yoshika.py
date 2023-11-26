__all__ = ('Yoshika',)

from hata import Activity, Client, IntentFlag

import config


Yoshika = Client(
    config.YOSHIKA_TOKEN,
    activity = Activity('dead'),
    application_id = config.YOSHIKA_ID,
    client_id = config.YOSHIKA_ID,
    extensions = ('slash',),
    intents = IntentFlag().update_by_keys(), # no changes
    should_request_users = False,
)
