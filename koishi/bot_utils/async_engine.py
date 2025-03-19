from .models import DATABASE_NAME
from sqlalchemy import create_engine

from hata.ext.kokoro_sqlalchemy import KOKORO_STRATEGY

if (DATABASE_NAME is None):
    DB_ENGINE = None

else:
    from . import models as module_models
    if module_models.DB_ENGINE is not None:
        
        DB_ENGINE = create_engine(
            DATABASE_NAME, max_overflow = -1, pool_size = 50, strategy = KOKORO_STRATEGY, single_worker = False
        )
        module_models.DB_ENGINE = DB_ENGINE
