__all__ = ()

from ...bots import FEATURE_CLIENTS

from .actions import (
    ACTION_BITE, ACTION_BLUSH, ACTION_BULLY, ACTION_CRINGE, ACTION_CRY, ACTION_CUDDLE, ACTION_DANCE, ACTION_FEED,
    ACTION_FLUFF, ACTION_GLOMP, ACTION_HANDHOLD, ACTION_HAPPY, ACTION_HIGHFIVE, ACTION_HUG, ACTION_KICK, ACTION_KILL,
    ACTION_KISS, ACTION_KON, ACTION_LICK, ACTION_LIKE, ACTION_NOM, ACTION_PAT, ACTION_POCKY, ACTION_POKE, ACTION_SLAP,
    ACTION_SMILE, ACTION_SMUG, ACTION_WAVE, ACTION_WINK, ACTION_YEET
)



BITE = FEATURE_CLIENTS.interactions(
    ACTION_BITE,
    name = 'bite',
    description = 'Vampy.',
    is_global = True,
)

BLUSH = FEATURE_CLIENTS.interactions(
    ACTION_BLUSH,
    name = 'blush',
    description = 'Oh.',
    is_global = True,
)

BULLY = FEATURE_CLIENTS.interactions(
    ACTION_BULLY,
    name = 'bully',
    description = 'No Bully!',
    is_global = True,
)

CUDDLE = FEATURE_CLIENTS.interactions(
    ACTION_CUDDLE,
    name = 'cuddle',
    description = 'Come here my pog champion.',
    is_global = True,
)

CRINGE = FEATURE_CLIENTS.interactions(
    ACTION_CRINGE,
    name = 'cringe',
    description = 'Cringe, run!',
    is_global = True,
)

CRY = FEATURE_CLIENTS.interactions(
    ACTION_CRY,
    name = 'cry',
    description = 'The saddest.',
    is_global = True,
)

DANCE = FEATURE_CLIENTS.interactions(
    ACTION_DANCE,
    name = 'dance',
    description = 'Dancy, dancy.',
    is_global = True,
)

FEED = FEATURE_CLIENTS.interactions(
    ACTION_FEED,
    name = 'feed',
    description = 'Just a spoonful..',
    integration_types = ['guild_install', 'user_install'],
    is_global = True,
)

FLUFF = FEATURE_CLIENTS.interactions(
    ACTION_FLUFF,
    name = 'fluff',
    description = 'Fuwa fuwa',
    integration_types = ['guild_install', 'user_install'],
    is_global = True,
)

GLOMP = FEATURE_CLIENTS.interactions(
    ACTION_GLOMP,
    name = 'glomp',
    description = 'You can run, but you cant hide!',
    is_global = True,
)

HANDHOLD = FEATURE_CLIENTS.interactions(
    ACTION_HANDHOLD,
    name = 'handhold',
    description = 'Lewd!!',
    is_global = True,
)

HAPPY = FEATURE_CLIENTS.interactions(
    ACTION_HAPPY,
    name = 'happy',
    description = 'If you are happy, clap your..',
    is_global = True,
)

HIGHFIVE = FEATURE_CLIENTS.interactions(
    ACTION_HIGHFIVE,
    name = 'highfive',
    description = 'Lets go boiz!',
    is_global = True,
)

HUG = FEATURE_CLIENTS.interactions(
    ACTION_HUG,
    name = 'hug',
    description = 'Huh.. Huggu? HUGG YOUUU!!!',
    integration_types = ['guild_install', 'user_install'],
    is_global = True,
)

KICK = FEATURE_CLIENTS.interactions(
    ACTION_KICK,
    name = 'kick',
    description = 'Kicks butt!',
    is_global = True,
)

KILL = FEATURE_CLIENTS.interactions(
    ACTION_KILL,
    name = 'kill',
    description = 'Finally, some action.',
    is_global = True,
)

KISS = FEATURE_CLIENTS.interactions(
    ACTION_KISS,
    name = 'kiss',
    description = 'If you really really like your onee, give her a kiss <3',
    integration_types = ['guild_install', 'user_install'],
    is_global = True,
)

KON = FEATURE_CLIENTS.interactions(
    ACTION_KON,
    name = 'kon',
    description = 'Kon~kon',
    integration_types = ['guild_install', 'user_install'],
    is_global = True,
)

LICK = FEATURE_CLIENTS.interactions(
    ACTION_LICK,
    name = 'lick',
    description = 'Licking is a favored activity of neko girls.',
    integration_types = ['guild_install', 'user_install'],
    is_global = True,
)

LIKE = FEATURE_CLIENTS.interactions(
    ACTION_LIKE,
    name = 'like',
    description = 'We like older woman.',
    integration_types = ['guild_install', 'user_install'],
    is_global = True,
)

NOM = FEATURE_CLIENTS.interactions(
    ACTION_NOM,
    name = 'nom',
    description = 'Feed your fumo, or else',
    is_global = True,
)

PAT = FEATURE_CLIENTS.interactions(
    ACTION_PAT,
    name = 'pat',
    description = 'Do you like pats as well?',
    integration_types = ['guild_install', 'user_install'],
    is_global = True,
)

POCKY_KISS = FEATURE_CLIENTS.interactions(
    ACTION_POCKY,
    name = 'pocky-kiss',
    description = 'Will they bale?',
    integration_types = ['guild_install', 'user_install'],
    is_global = True,
)

POKE = FEATURE_CLIENTS.interactions(
    ACTION_POKE,
    name = 'poke',
    description = 'It hurts!',
    is_global = True,
)

SLAP = FEATURE_CLIENTS.interactions(
    ACTION_SLAP,
    name = 'slap',
    description = 'Slapping others is not nice.',
    is_global = True,
)

SMILE = FEATURE_CLIENTS.interactions(
    ACTION_SMILE,
    name = 'smile',
    description = 'Oh, really?',
    is_global = True,
)

SMUG = FEATURE_CLIENTS.interactions(
    ACTION_SMUG,
    name = 'smug',
    description = 'Smug face.',
    is_global = True,
)

WAVE = FEATURE_CLIENTS.interactions(
    ACTION_WAVE,
    name = 'wave',
    description = 'Flap flap',
    is_global = True,
)

WINK = FEATURE_CLIENTS.interactions(
    ACTION_WINK,
    name = 'wink',
    description = 'Ara-ara',
    is_global = True,
)

YEET = FEATURE_CLIENTS.interactions(
    ACTION_YEET,
    name = 'yeet',
    description = 'Yeet!',
    is_global = True,
)
