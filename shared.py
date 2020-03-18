import pers_data

import models
from hata.events import prefix_by_guild

KOISHI_PREFIX=prefix_by_guild(pers_data.KOISHI_PREFIX,models.DB_ENGINE,models.PREFIX_TABLE,models.pefix_model)
SATORI_PREFIX = pers_data.SATORI_PREFIX
FLAN_PREFIX = pers_data.FLAN_PREFIX
