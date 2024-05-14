__all__ = (
    'COMMAND_CLIENT',
    'MAIN_CLIENT',
    'FEATURE_CLIENTS',
)

import sys

from hata import ClientWrapper

import config


if 'vampytest' in sys.modules:
    LOAD_MARISA = True
    LOAD_KOISHI = True
else:
    LOAD_MARISA = config.MARISA_MODE
    LOAD_KOISHI = not config.MARISA_MODE


if LOAD_KOISHI:
    from .cursed_sakuya import *
    from .flandre import *
    from .koishi import *
    from .nitori import *
    from .orin import *
    from .renes import *
    from .satori import *
    from .yoshika import *
    
    
    COMMAND_CLIENT = Satori
    MAIN_CLIENT = Koishi
    
    FEATURE_CLIENTS = ClientWrapper(
        CursedSakuya,
        Flandre,
        Koishi,
        Orin,
        Yoshika,
    )
    
    __all__ = (
        *__all__,
        *cursed_sakuya.__all__,
        *flandre.__all__,
        *koishi.__all__,
        *nitori.__all__,
        *orin.__all__,
        *renes.__all__,
        *satori.__all__,
        *yoshika.__all__,
    )


if LOAD_MARISA:
    from .marisa import *
    from .sakuya import *
    
    
    COMMAND_CLIENT = Marisa
    FEATURE_CLIENTS = ClientWrapper(Marisa)
    MAIN_CLIENT = Marisa
    
    __all__ = (
        *__all__,
        *marisa.__all__,
        *sakuya.__all__,
    )
