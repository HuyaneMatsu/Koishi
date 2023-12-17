__all__ = ('CursedSakuya',)

from hata import Activity, ActivityType, Client, IntentFlag

import config


CursedSakuya = Client(
    config.CURSED_SAKUYA_TOKEN,
    client_id = config.CURSED_SAKUYA_ID,
    activity = Activity('All Max Mode....', activity_type = ActivityType.competing),
    should_request_users = False,
    intents = IntentFlag().update_by_keys(), # no changes
    application_id = config.CURSED_SAKUYA_ID,
    extensions = ('slash',),
)
