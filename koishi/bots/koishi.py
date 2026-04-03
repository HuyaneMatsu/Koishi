__all__ = ('Koishi',)

from hata import Activity, Client, IntentFlag

import config


Koishi = Client(
    config.KOISHI_TOKEN,
    secret = config.KOISHI_SECRET,
    client_id = config.KOISHI_ID,
    activity = Activity('with Kokoro'),
    shard_count = 2,
    should_request_users = False,
    intents = IntentFlag().update_by_keys(
        guild_users = True, # We need this
        guild_presences = True, # Now this too, :KoishiFail:
        _17 = 1,
        _18 = 1,
        _19 = 1,
        _21 = 1, # Gonna catch them all
        _24 = 1,
        _25 = 1,
        _26 = 1,
        _27 = 1,
        _28 = 1,
    ),
    application_id = config.KOISHI_ID,
    extensions = ('slash', 'top_gg'),
    top_gg_token = config.KOISHI_TOP_GG_TOKEN,
)
