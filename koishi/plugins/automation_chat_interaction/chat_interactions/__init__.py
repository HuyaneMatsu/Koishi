from .mention_mirror import *
from .nani import *
from .owo import *
from .roblox import *


__all__ = (
    'CHAT_INTERACTIONS',
    
    *mention_mirror.__all__,
    *nani.__all__,
    *owo.__all__,
    *roblox.__all__,
)

from .mention_mirror import CHAT_INTERACTION as CHAT_INTERACTION_MENTION_MIRROR
from .nani import CHAT_INTERACTION as CHAT_INTERACTION_NANI
from .owo import CHAT_INTERACTION as CHAT_INTERACTION_OWO
from .roblox import CHAT_INTERACTION as CHAT_INTERACTION_ROBLOX


CHAT_INTERACTIONS = (
    CHAT_INTERACTION_MENTION_MIRROR,
    CHAT_INTERACTION_NANI,
    CHAT_INTERACTION_OWO,
    CHAT_INTERACTION_ROBLOX,
)
