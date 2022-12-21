__all__ = ()

from hata import Client

from ...image_handler import ImageHandlerStatic, ImageHandlerWaifuPics
from ...touhou import TOUHOU_ACTION_POCKY_KISS, TOUHOU_ACTION_POCKY_KISS_SELF

from .action import Action


SLASH_CLIENT: Client


PAT = SLASH_CLIENT.interactions(
    Action(
        ImageHandlerWaifuPics('pat', False),
        'pats',
    ),
    name = 'pat',
    description = 'Do you like pats as well?',
    is_global = True,
)


KISS = SLASH_CLIENT.interactions(
    Action(
        ImageHandlerWaifuPics('kiss', False),
        'kisses',
    ),
    name = 'kiss',
    description = 'If you really really like your onee, give her a kiss <3',
    is_global = True,
)

HUG = SLASH_CLIENT.interactions(
    Action(
        ImageHandlerWaifuPics('hug', False),
        'hugs',
    ),
    name = 'hug',
    description = 'Huh.. Huggu? HUGG YOUUU!!!',
    is_global = True,
)

CUDDLE = SLASH_CLIENT.interactions(
    Action(
        ImageHandlerWaifuPics('cuddle', False),
        'cuddles',
    ),
    name = 'cuddle',
    description = 'Come here, you little qtie pie.',
    is_global = True,
)

LICK = SLASH_CLIENT.interactions(
    Action(
        ImageHandlerWaifuPics('lick', False),
        'licks',
    ),
    name = 'lick',
    description = 'Licking is a favored activity of neko girls.',
    is_global = True,
)

POKE = SLASH_CLIENT.interactions(
    Action(
        ImageHandlerWaifuPics('poke', False),
        'pokes',
    ),
    name = 'poke',
    description = 'It hurts!',
    is_global = True,
)

SLAP = SLASH_CLIENT.interactions(
    Action(
        ImageHandlerWaifuPics('slap', False),
        'slaps',
    ),
    name = 'slap',
    description = 'Slapping others is not nice.',
    is_global = True,
)

SMUG = SLASH_CLIENT.interactions(
    Action(
        ImageHandlerWaifuPics('smug', False),
        'smugs at',
    ),
    name = 'smug',
    description = 'Smug face.',
    is_global = True,
)

BULLY = SLASH_CLIENT.interactions(
    Action(
        ImageHandlerWaifuPics('bully', False),
        'bullies',
    ),
    name = 'bully',
    description = 'No Bully!',
    is_global = True,
)

CRY = SLASH_CLIENT.interactions(
    Action(
        ImageHandlerWaifuPics('cry', False),
        'cries because of',
    ),
    name = 'cry',
    description = 'The saddest.',
    is_global = True,
)

YEET = SLASH_CLIENT.interactions(
    Action(
        ImageHandlerWaifuPics('yeet', False),
        'yeets',
    ),
    name = 'yeet',
    description = 'Yeet!',
    is_global = True,
)

BLUSH = SLASH_CLIENT.interactions(
    Action(
        ImageHandlerWaifuPics('blush', False),
        'blushes at',
    ),
    name = 'blush',
    description = 'Oh.',
    is_global = True,
)

SMILE = SLASH_CLIENT.interactions(
    Action(
        ImageHandlerWaifuPics('smile', False),
        'smiles at',
    ),
    name = 'smile',
    description = 'Oh, really?',
    is_global = True,
)

WAVE = SLASH_CLIENT.interactions(
    Action(
        ImageHandlerWaifuPics('wave', False),
        'waves at',
    ),
    name = 'wave',
    description = 'Flap flap',
    is_global = True,
)

HIGHFIVE = SLASH_CLIENT.interactions(
    Action(
        ImageHandlerWaifuPics('highfive', False),
        'highfives',
    ),
    name = 'highfive',
    description = 'Lets go boiz!',
    is_global = True,
)

HANDHOLD = SLASH_CLIENT.interactions(
    Action(
        ImageHandlerWaifuPics('handhold', False),
        'holds hands of',
    ),
    name = 'handhold',
    description = 'Lewd!!',
    is_global = True,
)

NOM = SLASH_CLIENT.interactions(
    Action(
        ImageHandlerWaifuPics('nom', False),
        'noms',
    ),
    name = 'nom',
    description = 'Feed your fumo, or else',
    is_global = True,
)

BITE = SLASH_CLIENT.interactions(
    Action(
        ImageHandlerWaifuPics('bite', False),
        'bites',
    ),
    name = 'bite',
    description = 'Vampy.',
    is_global = True,
)

GLOMP = SLASH_CLIENT.interactions(
    Action(
        ImageHandlerWaifuPics('glomp', False),
        'glomps',
    ),
    name = 'glomp',
    description = 'You can run, but you cant hide!',
    is_global = True,
)

KILL = SLASH_CLIENT.interactions(
    Action(
        ImageHandlerWaifuPics('kill', False),
        'murders',
    ),
    name = 'kill',
    description = 'Finally, some action.',
    is_global = True,
)

HAPPY = SLASH_CLIENT.interactions(
    Action(
        ImageHandlerWaifuPics('happy', False),
        'is happy for',
    ),
    name = 'happy',
    description = 'If you are happy, clap your..',
    is_global = True,
)

WINK = SLASH_CLIENT.interactions(
    Action(
        ImageHandlerWaifuPics('wink', False),
        'winks at',
    ),
    name = 'wink',
    description = 'Ara-ara',
    is_global = True,
)

DANCE = SLASH_CLIENT.interactions(
    Action(
        ImageHandlerWaifuPics('dance', False),
        'dancing with',
    ),
    name = 'dance',
    description = 'Dancy, dancy.',
    is_global = True,
)

CRINGE = SLASH_CLIENT.interactions(
    Action(
        ImageHandlerWaifuPics('cringe', False),
        'cringes at',
    ),
    name = 'cringe',
    description = 'Cringe, run!',
    is_global = True,
)

KICK = SLASH_CLIENT.interactions(
    Action(
        ImageHandlerWaifuPics('kick', False),
        'kicks',
    ),
    name = 'kick',
    description = 'Kicks butt!',
    is_global = True,
)

POCKY_KISS = SLASH_CLIENT.interactions(
    Action(
        ImageHandlerStatic(TOUHOU_ACTION_POCKY_KISS),
        'pocky kisses',
        handler_self = ImageHandlerStatic(TOUHOU_ACTION_POCKY_KISS_SELF),
    ),
    name = 'pocky-kiss',
    description = 'Will they bale?',
    is_global = True,
)
