__all__ = ()

from .action import Action
from .image_handlers import (
    IMAGE_HANDLER_BITE, IMAGE_HANDLER_BLUSH, IMAGE_HANDLER_BULLY, IMAGE_HANDLER_CRINGE, IMAGE_HANDLER_CRY,
    IMAGE_HANDLER_CUDDLE, IMAGE_HANDLER_DANCE, IMAGE_HANDLER_FEED, IMAGE_HANDLER_FLUFF, IMAGE_HANDLER_GLOMP,
    IMAGE_HANDLER_HANDHOLD, IMAGE_HANDLER_HAPPY, IMAGE_HANDLER_HIGHFIVE, IMAGE_HANDLER_HUG, IMAGE_HANDLER_KICK,
    IMAGE_HANDLER_KISS, IMAGE_HANDLER_KON, IMAGE_HANDLER_LAP_SLEEP, IMAGE_HANDLER_LICK, IMAGE_HANDLER_LIKE,
    IMAGE_HANDLER_MURDER, IMAGE_HANDLER_NOM, IMAGE_HANDLER_PAT, IMAGE_HANDLER_PEG, IMAGE_HANDLER_POCKY_KISS,
    IMAGE_HANDLER_POCKY_KISS_SELF, IMAGE_HANDLER_POKE, IMAGE_HANDLER_SLAP, IMAGE_HANDLER_SMILE, IMAGE_HANDLER_SMUG,
    IMAGE_HANDLER_STARE, IMAGE_HANDLER_WAVE, IMAGE_HANDLER_WINK, IMAGE_HANDLER_YEET
)


ACTIONS = [
    Action(
        'bite',
        'Vampy.',
        IMAGE_HANDLER_BITE,
        'bites',
    ),
    Action(
        'blush',
        'Oh.',
        IMAGE_HANDLER_BLUSH,
        'blushes at',
    ),
    Action(
        'bully',
        'No Bully!',
        IMAGE_HANDLER_BULLY,
        'bullies',
    ),
    Action(
        'cringe',
        'Cringe, run!',
        IMAGE_HANDLER_CRINGE,
        'cringes at',
    ),
    Action(
        'cry',
        'The saddest.',
        IMAGE_HANDLER_CRY,
        'cries because of',
    ),
    Action(
        'cuddle',
        'Come here my pog champion.',
        IMAGE_HANDLER_CUDDLE,
        'cuddles',
    ),
    Action(
        'dance',
        'Dancy, dancy.',
        IMAGE_HANDLER_DANCE,
        'dancing for',
    ),
    Action(
        'feed',
        'Just a spoonful..',
        IMAGE_HANDLER_FEED,
        'feeds',
    ),
    Action(
        'fluff',
        'Fuwa fuwa',
        IMAGE_HANDLER_FLUFF,
        'fluffs',
    ),
    Action(
        'glomp',
        'You can run, but you can\'t hide!',
        IMAGE_HANDLER_GLOMP,
        'glomps',
    ),
    Action(
        'handhold',
        'Lewd!!',
        IMAGE_HANDLER_HANDHOLD,
        'holds hands of',
    ),
    Action(
        'happy',
        'If you are happy, clap your..',
        IMAGE_HANDLER_HAPPY,
        'is happy for',
    ),
    Action(
        'highfive',
        'Lets go boiz!',
        IMAGE_HANDLER_HIGHFIVE,
        'highfives',
    ),
    Action(
        'hug',
        'Huh.. Huggu? HUGG YOUUU!!!',
        IMAGE_HANDLER_HUG,
        'hugs',
    ),
    Action(
        'kick',
        'Kicks butt!',
        IMAGE_HANDLER_KICK,
        'kicks',
    ),
    Action(
        'murder',
        'Finally, some action.',
        IMAGE_HANDLER_MURDER,
        'murders',
        aliases = ('kill',),
    ),
    Action(
        'kiss',
        'If you really really like your onee, give her a kiss <3',
        IMAGE_HANDLER_KISS,
        'kisses',
    ),
    Action(
        'kon',
        'Kon~kon',
        IMAGE_HANDLER_KON,
        'kons at',
    ),
    Action(
        'lap-sleep',
        'Its eep time...',
        IMAGE_HANDLER_LAP_SLEEP,
        'sleeps on the lap of',
        aliases = ('sleep',),
    ),
    Action(
        'lick',
        'Licking is a favored activity of neko girls.',
        IMAGE_HANDLER_LICK,
        'licks',
    ),
    Action(
        'like',
        'We like older woman.',
        IMAGE_HANDLER_LIKE,
        'likes',
    ),
    Action(
        'nom',
        'Feed your fumo, or else',
        IMAGE_HANDLER_NOM,
        'noms',
    ),
    Action(
        'pat',
        'Do you like pats as well?',
        IMAGE_HANDLER_PAT,
        'pats',
    ),
    Action(
        'peg',
        'Cave someone!',
        IMAGE_HANDLER_PEG,
        'pegs',
        starter_text = 'So true bestie',
    ),
    Action(
        'pocky-kiss',
        'Will they bail?',
        IMAGE_HANDLER_POCKY_KISS,
        'pocky kisses',
        aliases = ('pocky',),
        handler_self = IMAGE_HANDLER_POCKY_KISS_SELF,
    ),
    Action(
        'poke',
        'It hurts!',
        IMAGE_HANDLER_POKE,
        'pokes',
    ),
    Action(
        'slap',
        'Slapping others is not nice.',
        IMAGE_HANDLER_SLAP,
        'slaps',
    ),
    Action(
        'smile',
        'Oh, really?',
        IMAGE_HANDLER_SMILE,
        'smiles at',
    ),
    Action(
        'smug',
        'Smug face.',
        IMAGE_HANDLER_SMUG,
        'smugs at',
    ),
    Action(
        'stare',
        '** stare **',
        IMAGE_HANDLER_STARE,
        'stares at',
    ),
    Action(
        'wave',
        'Flap flap',
        IMAGE_HANDLER_WAVE,
        'waves at',
    ),
    Action(
        'wink',
        'Ara-ara',
        IMAGE_HANDLER_WINK,
        'winks at',
    ),
    Action(
        'yeet',
        'Yeet!',
        IMAGE_HANDLER_YEET,
        'yeets',
    )
]
