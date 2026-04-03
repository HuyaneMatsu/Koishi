__all__ = ('Sakuya',)

from hata import Client, IntentFlag

import config


Sakuya = Client(
    config.SAKUYA_TOKEN,
    client_id = config.SAKUYA_ID,
    application_id = config.SAKUYA_ID,
    intents = IntentFlag().update_by_keys(message_content = False),
    extensions = ('slash',),
)
