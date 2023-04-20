__all__ = ()

import config

if config.MARISA_MODE:
    from .marisa import *
    
    
    COMMAND_CLIENT = Marisa
    SLASH_CLIENT = Marisa
    MAIN_CLIENT = Marisa
    
    __all__ = (
        'COMMAND_CLIENT',
        'MAIN_CLIENT',
        'SLASH_CLIENT',
        *marisa.__all__,
    )
    

else:
    from .flan import *
    from .koishi import *
    from .nitori import *
    from .renes import *
    from .satori import *
    
    
    COMMAND_CLIENT = Satori
    SLASH_CLIENT = Koishi
    MAIN_CLIENT = Koishi
    
    __all__ = (
        'COMMAND_CLIENT',
        'MAIN_CLIENT',
        'SLASH_CLIENT',
        *flan.__all__,
        *koishi.__all__,
        *nitori.__all__,
        *renes.__all__,
        *satori.__all__
    )
