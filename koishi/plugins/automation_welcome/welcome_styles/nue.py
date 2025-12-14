__all__ = ()

from hata import Emoji

from config import NUE_ID

from ..welcome_style_reply import WelcomeStyleReply
from ..welcome_style import WelcomeStyle


NAME = 'nue'


MESSAGE_CONTENT_BUILDERS = (
    (lambda target: f'Left wings are blue, right wings are red, {target} is the one owning them.'),
    (lambda target: f'*yawn*, {target}\'s leisurely time is over!'),
    (lambda target: f'Welcome, {target}. We hope you didn\'t forget your UFO-s.'),
    (lambda target: f'An unidentified has been identified as {target}.'),
    (lambda target: f'We have already identified you {target}.'),
    (lambda target: f'It\'s {target}! Wait, what?'),
    (lambda target: f'{target} is here to surprise us.'),
    (lambda target: f'{target} just showed up, and they got a cool UFO!'),
    (lambda target: f'{target} just joined, mind showing your UFO?'),
    (lambda target: f'A forgotten {target} showed up!'),
    (lambda target: f'{target} just arrived. Looks adoptable, please be patient with them.'),
    (lambda target: f'Out of the UFO comes {target}!'),
    (lambda target: f'Ready to start plotting, {target}?'),
    (lambda target: f'{target} just joined, Its the Seed of Unknown Form!'),
    (lambda target: f'Byakureeeeen, {target} is here!'),
    (lambda target: f'Welcome, {target} leave your trident by the door.'),
    (lambda target: f'Key! Listen!, {target} has been identified!'),
    (lambda target: f'You must be Nue here, {target}.'),
)


IMAGES = (
    'https://cdn.discordapp.com/attachments/568837922288173058/1446985114750943356/nue-welcome-0000.png',
)


IMAGE_CREATOR = 'howhow notei'

REPLY_STYLES = (
    WelcomeStyleReply(
        'Explore their true form.',
        Emoji.precreate(1029366132412522496),
        (
            lambda source, target: (
                f'{source} explores {target}\'s true form. '
                f'The head of a monkey, the body of a raccoon, the legs of a tiger, and the tail of a snake.'
            )
        ),
    ),
    WelcomeStyleReply(
        'Show them your UFO.',
        Emoji.precreate(1029366132412522496),
        (lambda source, target: f'{source} shows their UFO to {target}.'),
    ),
    WelcomeStyleReply(
        'Become their co-beneficial partner.',
        Emoji.precreate(1029366132412522496),
        (lambda source, target: f'{source} becomes {target} co-beneficial partner.'),
    ),
    WelcomeStyleReply(
        'Welcome them to the Myouren temple.',
        Emoji.precreate(1029366132412522496),
        (lambda source, target: f'{source} welcomes {target} to the Myouren temple.'),
    ),
    WelcomeStyleReply(
        'Ask them to show their UFO.',
        Emoji.precreate(1029366132412522496),
        (lambda source, target: f'{source} is eager to see {target}\'s UFO, please show!'),
    ),
)


WELCOME_STYLE = WelcomeStyle(
    NAME,
    NUE_ID,
    MESSAGE_CONTENT_BUILDERS,
    IMAGES,
    IMAGE_CREATOR,
    REPLY_STYLES,
)
