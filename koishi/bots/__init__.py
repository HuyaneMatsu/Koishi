__all__ = (
    'COMMAND_CLIENT',
    'MAIN_CLIENT',
    'SLASH_CLIENT',
)

import sys

import config


if 'vampytest' in sys.modules:
    LOAD_MARISA = True
    LOAD_KOISHI = True
else:
    LOAD_MARISA = config.MARISA_MODE
    LOAD_KOISHI = not config.MARISA_MODE


if LOAD_KOISHI:
    from .flan import *
    from .koishi import *
    from .nitori import *
    from .renes import *
    from .satori import *
    
    
    COMMAND_CLIENT = Satori
    SLASH_CLIENT = Koishi
    MAIN_CLIENT = Koishi
    
    __all__ = (
        *__all__,
        *flan.__all__,
        *koishi.__all__,
        *nitori.__all__,
        *renes.__all__,
        *satori.__all__
    )


if LOAD_MARISA:
    from .marisa import *
    from .sakuya import *
    
    
    COMMAND_CLIENT = Marisa
    SLASH_CLIENT = Marisa
    MAIN_CLIENT = Marisa
    
    __all__ = (
        *__all__,
        *marisa.__all__,
        *sakuya.__all__,
    )
