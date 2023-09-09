__all__ = ()

from ....bots import SLASH_CLIENT

from .actions import (
    ACTION_BITE, ACTION_BLUSH, ACTION_BULLY, ACTION_CRINGE, ACTION_CRY, ACTION_CUDDLE, ACTION_DANCE, ACTION_GLOMP,
    ACTION_HANDHOLD, ACTION_HAPPY, ACTION_HIGHFIVE, ACTION_HUG, ACTION_KICK, ACTION_KILL, ACTION_KISS, ACTION_KON,
    ACTION_LICK, ACTION_LIKE, ACTION_NOM, ACTION_PAT, ACTION_POCKY, ACTION_POKE, ACTION_SLAP, ACTION_SMILE, ACTION_SMUG,
    ACTION_WAVE, ACTION_WINK, ACTION_YEET
)



BITE = SLASH_CLIENT.interactions(
    ACTION_BITE,
    name = 'bite',
    description = 'Vampy.',
    is_global = True,
)

BLUSH = SLASH_CLIENT.interactions(
    ACTION_BLUSH,
    name = 'blush',
    description = 'Oh.',
    is_global = True,
)

BULLY = SLASH_CLIENT.interactions(
    ACTION_BULLY,
    name = 'bully',
    description = 'No Bully!',
    is_global = True,
)

CUDDLE = SLASH_CLIENT.interactions(
    ACTION_CUDDLE,
    name = 'cuddle',
    description = 'Come here my pog champion.',
    is_global = True,
)

CRINGE = SLASH_CLIENT.interactions(
    ACTION_CRINGE,
    name = 'cringe',
    description = 'Cringe, run!',
    is_global = True,
)

CRY = SLASH_CLIENT.interactions(
    ACTION_CRY,
    name = 'cry',
    description = 'The saddest.',
    is_global = True,
)

DANCE = SLASH_CLIENT.interactions(
    ACTION_DANCE,
    name = 'dance',
    description = 'Dancy, dancy.',
    is_global = True,
)

GLOMP = SLASH_CLIENT.interactions(
    ACTION_GLOMP,
    name = 'glomp',
    description = 'You can run, but you cant hide!',
    is_global = True,
)

HANDHOLD = SLASH_CLIENT.interactions(
    ACTION_HANDHOLD,
    name = 'handhold',
    description = 'Lewd!!',
    is_global = True,
)

HAPPY = SLASH_CLIENT.interactions(
    ACTION_HAPPY,
    name = 'happy',
    description = 'If you are happy, clap your..',
    is_global = True,
)

HIGHFIVE = SLASH_CLIENT.interactions(
    ACTION_HIGHFIVE,
    name = 'highfive',
    description = 'Lets go boiz!',
    is_global = True,
)

HUG = SLASH_CLIENT.interactions(
    ACTION_HUG,
    name = 'hug',
    description = 'Huh.. Huggu? HUGG YOUUU!!!',
    is_global = True,
)

KICK = SLASH_CLIENT.interactions(
    ACTION_KICK,
    name = 'kick',
    description = 'Kicks butt!',
    is_global = True,
)

KILL = SLASH_CLIENT.interactions(
    ACTION_KILL,
    name = 'kill',
    description = 'Finally, some action.',
    is_global = True,
)

KISS = SLASH_CLIENT.interactions(
    ACTION_KISS,
    name = 'kiss',
    description = 'If you really really like your onee, give her a kiss <3',
    is_global = True,
)

KON = SLASH_CLIENT.interactions(
    ACTION_KON,
    name = 'kon',
    description = 'Kon~kon',
    is_global = True,
)

LICK = SLASH_CLIENT.interactions(
    ACTION_LICK,
    name = 'lick',
    description = 'Licking is a favored activity of neko girls.',
    is_global = True,
)

LIKE = SLASH_CLIENT.interactions(
    ACTION_LIKE,
    name = 'like',
    description = 'We like older woman.',
    is_global = True,
)

NOM = SLASH_CLIENT.interactions(
    ACTION_NOM,
    name = 'nom',
    description = 'Feed your fumo, or else',
    is_global = True,
)

PAT = SLASH_CLIENT.interactions(
    ACTION_PAT,
    name = 'pat',
    description = 'Do you like pats as well?',
    is_global = True,
)

POCKY_KISS = SLASH_CLIENT.interactions(
    ACTION_POCKY,
    name = 'pocky-kiss',
    description = 'Will they bale?',
    is_global = True,
)

POKE = SLASH_CLIENT.interactions(
    ACTION_POKE,
    name = 'poke',
    description = 'It hurts!',
    is_global = True,
)

SLAP = SLASH_CLIENT.interactions(
    ACTION_SLAP,
    name = 'slap',
    description = 'Slapping others is not nice.',
    is_global = True,
)

SMILE = SLASH_CLIENT.interactions(
    ACTION_SMILE,
    name = 'smile',
    description = 'Oh, really?',
    is_global = True,
)

SMUG = SLASH_CLIENT.interactions(
    ACTION_SMUG,
    name = 'smug',
    description = 'Smug face.',
    is_global = True,
)

WAVE = SLASH_CLIENT.interactions(
    ACTION_WAVE,
    name = 'wave',
    description = 'Flap flap',
    is_global = True,
)

WINK = SLASH_CLIENT.interactions(
    ACTION_WINK,
    name = 'wink',
    description = 'Ara-ara',
    is_global = True,
)

YEET = SLASH_CLIENT.interactions(
    ACTION_YEET,
    name = 'yeet',
    description = 'Yeet!',
    is_global = True,
)
