__all__ = ()

from ...bot_utils.constants import GUILD__SUPPORT


RULES = [
    (
        'Behaviour',
        lambda: 'Listen to staff and follow their instructions.',
    ), (
        'Language',
        lambda: f'{GUILD__SUPPORT.name} is an english speaking server, please try to stick yourself to it.'
    ), (
        'Channels',
        lambda: 'Read the channel\'s topics. Make sure to keep the conversations in their respective channels.'
    ), (
        'Usernames',
        lambda: 'Invisible, offensive or noise unicode names are not allowed.',
    ), (
        'Spamming',
        lambda: 'Forbidden in any form. Spamming server members in DM-s counts as well.'
    ), (
        'NSFW',
        lambda: 'Keep explicit content in nsfw channels.',
    ), (
        'Shitposting, earrape and other cursed contents',
        lambda: (
            'Includes: tiktok cringe, ai shit, pictures taken of a screen, guro, scat '
            'and making the same joke 3 times in a row are all a big NO!!!'
        ),
    ), (
        'Advertisements',
        lambda: 'Advertising other social medias, servers, communities or services in chat or in DM-s are disallowed.',
    ), (
        'Political, Religious and Activist topics',
        lambda: (
            'Most ideals are inherently not wrong, but there are people who like to push them too far. '
            'Children should be the smith of their fate, but they are the core target of propaganda and of social '
            'pressuring. Therefore we do not allow tools used for these (neither in chat and in visible user profiles) '
            'which are: flags or idols, icons, keywords, parades, identifiable clothings, '
            'ideals that give abusive rights to a group of people over others.'
        )
    ), (
        'Alternative accounts',
        lambda: 'Unless, you have really good reason, like you were locked out from the original.',
    ), (
        'Deep frying fumos',
        lambda: 'Fumo frying and other related unethical actions are bannable offenses.',
    ), (
        'Orin abuse',
        lambda: 'You will be fed to Rumia.',
    ),
]
