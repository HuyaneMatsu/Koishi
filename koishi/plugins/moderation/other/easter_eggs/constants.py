__all__ = ()

from datetime import timedelta as TimeDelta

from hata import AuditLogEntryType, Color


IMAGE_URL_NAZRIN = (
    'https://cdn.discordapp.com/attachments/568837922288173058/1258766702179782677/kyouko-nazrin-silencing.png'
)
IMAGE_URL_ORIN = (
    'https://cdn.discordapp.com/attachments/568837922288173058/1239516656099790868/orin-body-collecting.png'
)

COLOR_NAZRIN = Color(0xbFA9C4)
COLOR_ORIN = Color(0x9E4D4C)

ENTRY_TYPES_ORIN = (AuditLogEntryType.user_ban_add, AuditLogEntryType.user_kick)
AUDIT_LOG_INTERVA_ORIN = TimeDelta(days = 7)

TIMEOUT_DURATION_MIN_NAZRIN = TimeDelta(days = 7, seconds = 1)
