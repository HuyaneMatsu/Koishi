__all__ = ()

from .action import Action

from .image_handlers import (
    IMAGE_HANDLER_BITE, IMAGE_HANDLER_BLUSH, IMAGE_HANDLER_BULLY, IMAGE_HANDLER_CRINGE, IMAGE_HANDLER_CRY,
    IMAGE_HANDLER_CUDDLE, IMAGE_HANDLER_DANCE, IMAGE_HANDLER_GLOMP, IMAGE_HANDLER_HAPPY, IMAGE_HANDLER_HIGHFIVE,
    IMAGE_HANDLER_HUG, IMAGE_HANDLER_KICK, IMAGE_HANDLER_KILL, IMAGE_HANDLER_KISS, IMAGE_HANDLER_LICK,
    IMAGE_HANDLER_NOM, IMAGE_HANDLER_PAT, IMAGE_HANDLER_POCKY, IMAGE_HANDLER_POCKY_SELF, IMAGE_HANDLER_POKE,
    IMAGE_HANDLER_SLAP, IMAGE_HANDLER_SMILE, IMAGE_HANDLER_SMUG, IMAGE_HANDLER_WAVE, IMAGE_HANDLER_WINK,
    IMAGE_HANDLER_YEET, IMAGE_HANDLE_HANDHOLD
)


ACTION_PAT = Action(
    IMAGE_HANDLER_PAT,
    'pats',
)

ACTION_KISS = Action(
    IMAGE_HANDLER_KISS,
    'kisses',
)

ACTION_HUG = Action(
    IMAGE_HANDLER_HUG,
    'hugs',
)

ACTION_CUDDLE = Action(
    IMAGE_HANDLER_CUDDLE,
    'cuddles',
)

ACTION_LICK = Action(
    IMAGE_HANDLER_LICK,
    'licks',
)

ACTION_POKE = Action(
    IMAGE_HANDLER_POKE,
    'pokes',
)

ACTION_SLAP = Action(
    IMAGE_HANDLER_SLAP,
    'slaps',
)

ACTION_SMUG = Action(
    IMAGE_HANDLER_SMUG,
    'smugs at',
)

ACTION_BULLY = Action(
    IMAGE_HANDLER_BULLY,
    'bullies',
)

ACTION_CRY = Action(
    IMAGE_HANDLER_CRY,
    'cries because of',
)

ACTION_YEET = Action(
    IMAGE_HANDLER_YEET,
    'yeets',
)

ACTION_BLUSH = Action(
    IMAGE_HANDLER_BLUSH,
    'blushes at',
)

ACTION_SMILE = Action(
    IMAGE_HANDLER_SMILE,
    'smiles at',
)

ACTION_WAVE = Action(
    IMAGE_HANDLER_WAVE,
    'waves at',
)

ACTION_HIGHFIVE = Action(
    IMAGE_HANDLER_HIGHFIVE,
    'highfives',
)

ACTION_HANDHOLD = Action(
    IMAGE_HANDLE_HANDHOLD,
    'holds hands of',
)

ACTION_NOM = Action(
    IMAGE_HANDLER_NOM,
    'noms',
)

ACTION_BITE = Action(
    IMAGE_HANDLER_BITE,
    'bites',
)

ACTION_GLOMP = Action(
    IMAGE_HANDLER_GLOMP,
    'glomps',
)

ACTION_KILL = Action(
    IMAGE_HANDLER_KILL,
    'murders',
)

ACTION_HAPPY = Action(
    IMAGE_HANDLER_HAPPY,
    'is happy for',
)

ACTION_WINK = Action(
    IMAGE_HANDLER_WINK,
    'winks at',
)

ACTION_DANCE = Action(
    IMAGE_HANDLER_DANCE,
    'dancing with',
)

ACTION_CRINGE = Action(
    IMAGE_HANDLER_CRINGE,
    'cringes at',
)

ACTION_KICK = Action(
    IMAGE_HANDLER_KICK,
    'kicks',
)

ACTION_POCKY = Action(
    IMAGE_HANDLER_POCKY,
    'pocky kisses',
    handler_self = IMAGE_HANDLER_POCKY_SELF,
)
