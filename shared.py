import pers_data

import models
from hata import modulize
from hata.events import prefix_by_guild

KOISHI_PREFIX=prefix_by_guild(pers_data.KOISHI_PREFIX,models.DB_ENGINE,models.PREFIX_TABLE,models.pefix_model)
SATORI_PREFIX = pers_data.SATORI_PREFIX
FLAN_PREFIX = pers_data.FLAN_PREFIX

@modulize
class FI_NO:
    ADMIN = 1
    INVITE = 2
    BAN = 3
    MANAGE_MESSAGES = 4
    MANAGE_CHANNEL = 5
    AUDIT_LOGS = 6
    
    GUILD_OWNER = 100
    OWNER = 101
