__all__ = ()

from random import random, randint, choice

from hata import Client, Embed, BUILTIN_EMOJIS, DiscordException, ERROR_CODES, Emoji
from hata.ext.slash import abort

from ..bots import FEATURE_CLIENTS

from .relationships_core import get_affinity_percent


@FEATURE_CLIENTS.interactions(show_for_invoking_user_only = True, is_global = True)
async def message_me(client, event):
    """Messages you!"""
    yield
    
    channel = await client.channel_private_create(event.user)
    try:
        await client.message_create(channel, 'Love you!')
    except DiscordException as err:
        if err.code == ERROR_CODES.cannot_message_user:
            yield 'Pls turn on private messages from this server!'
            return
        
        raise
    
    yield ':3'


@FEATURE_CLIENTS.interactions(is_global = True)
async def roll(client, event,
    dice_count: ([(str(v), v) for v in range(1, 7)], 'With how much dice do you wanna roll?') = 1,
):
    """Rolls with dices."""
    amount = 0
    for _ in range(dice_count):
        amount += round(1.+(random() * 5.))
    
    return str(amount)


@FEATURE_CLIENTS.interactions(is_global = True)
async def rate(client, event,
    target_user: ('user', 'Do you want me to rate someone else?') = None,
):
    """Rates someone!"""
    if target_user is None:
        target_user = event.user
    
    if isinstance(target_user, Client) or client.is_owner(target_user):
        result = 10
    else:
        result = target_user.id % 11
    
    return f'I rate {target_user.name_at(event.guild)} {result}/10'


@FEATURE_CLIENTS.interactions(is_global = True)
async def yuno():
    """Your personal yandere!"""
    return Embed(
        'YUKI YUKI YUKI!',
        (
            '░░░░░░░░░░░▄▄▀▀▀▀▀▀▀▀▄▄░░░░░░░░░░░░░\n'
            '░░░░░░░░▄▀▀░░░░░░░░░░░░▀▄▄░░░░░░░░░░\n'
            '░░░░░░▄▀░░░░░░░░░░░░░░░░░░▀▄░░░░░░░░\n'
            '░░░░░▌░░░░░░░░░░░░░▀▄░░░░░░░▀▀▄░░░░░\n'
            '░░░░▌░░░░░░░░░░░░░░░░▀▌░░░░░░░░▌░░░░\n'
            '░░░▐░░░░░░░░░░░░▒░░░░░▌░░░░░░░░▐░░░░\n'
            '░░░▌▐░░░░▐░░░░▐▒▒░░░░░▌░░░░░░░░░▌░░░\n'
            '░░▐░▌░░░░▌░░▐░▌▒▒▒░░░▐░░░░░▒░▌▐░▐░░░\n'
            '░░▐░▌▒░░░▌▄▄▀▀▌▌▒▒░▒░▐▀▌▀▌▄▒░▐▒▌░▌░░\n'
            '░░░▌▌░▒░░▐▀▄▌▌▐▐▒▒▒▒▐▐▐▒▐▒▌▌░▐▒▌▄▐░░\n'
            '░▄▀▄▐▒▒▒░▌▌▄▀▄▐░▌▌▒▐░▌▄▀▄░▐▒░▐▒▌░▀▄░\n'
            '▀▄▀▒▒▌▒▒▄▀░▌█▐░░▐▐▀░░░▌█▐░▀▄▐▒▌▌░░░▀\n'
            '░▀▀▄▄▐▒▀▄▀░▀▄▀░░░░░░░░▀▄▀▄▀▒▌░▐░░░░░\n'
            '░░░░▀▐▀▄▒▀▄░░░░░░░░▐░░░░░░▀▌▐░░░░░░░\n'
            '░░░░░░▌▒▌▐▒▀░░░░░░░░░░░░░░▐▒▐░░░░░░░\n'
            '░░░░░░▐░▐▒▌░░░░▄▄▀▀▀▀▄░░░░▌▒▐░░░░░░░\n'
            '░░░░░░░▌▐▒▐▄░░░▐▒▒▒▒▒▌░░▄▀▒░▐░░░░░░░\n'
            '░░░░░░▐░░▌▐▐▀▄░░▀▄▄▄▀░▄▀▐▒░░▐░░░░░░░\n'
            '░░░░░░▌▌░▌▐░▌▒▀▄▄░░░░▄▌▐░▌▒░▐░░░░░░░\n'
            '░░░░░▐▒▐░▐▐░▌▒▒▒▒▀▀▄▀▌▐░░▌▒░▌░░░░░░░\n'
            '░░░░░▌▒▒▌▐▒▌▒▒▒▒▒▒▒▒▐▀▄▌░▐▒▒▌░░░░░░░\n'
        ),
        color = 0xffafde,
        url = 'https://www.youtube.com/watch?v=TaDAn_S_4Y8',
    )


@FEATURE_CLIENTS.interactions(is_global = True)
async def random_(
    n1: ('int', 'Number limit.'),
    n2: ('int', 'Other number limit!') = 0,
):
    """Do you need some random numbers?"""
    if n1 == n2:
        result = n1
    else:
        if n2 < n1:
            n1, n2 = n2, n1
        
        result = randint(n1, n2)
    
    return str(result)


def generate_love_level():
    value = {
        'titles': (
            f'{BUILTIN_EMOJIS["blue_heart"]} There\'s no real connection between you two {BUILTIN_EMOJIS["blue_heart"]}',
        ),
        'text': (
            'The chance of this relationship working out is really low. You '
            'can get it to work, but with high costs and no guarantee of '
            'working out. Do not sit back, spend as much time together as '
            'possible, talk a lot with each other to increase the chances of '
            'this relationship\'s survival.'
        ),
    }
    
    for x in range(0, 2):
        yield value
    
    value = {
        'titles': (
            f'{BUILTIN_EMOJIS["blue_heart"]} A small acquaintance {BUILTIN_EMOJIS["blue_heart"]}',
        ),
        'text': (
            'There might be a chance of this relationship working out somewhat '
            'well, but it is not very high. With a lot of time and effort '
            'you\'ll get it to work eventually, however don\'t count on it. It '
            'might fall apart quicker than you\'d expect.'
        ),
    }
    
    for x in range(2, 6):
        yield value
    
    value = {
        'titles': (
            f'{BUILTIN_EMOJIS["purple_heart"]} You two seem like casual friends {BUILTIN_EMOJIS["purple_heart"]}',
        ),
        'text': (
            'The chance of this relationship working is not very high. You both '
            'need to put time and effort into this relationship, if you want it '
            'to work out well for both of you. Talk with each other about '
            'everything and don\'t lock yourself up. Spend time together. This '
            'will improve the chances of this relationship\'s survival by a lot.'
        ),
    }
    
    for x in range(6, 21):
        yield value
    
    value = {
        'titles': (
            f'{BUILTIN_EMOJIS["heartpulse"]} You seem like you are good friends {BUILTIN_EMOJIS["heartpulse"]}',
        ),
        'text': (
            'The chance of this relationship working is not very high, but its '
            'not that low either. If you both want this relationship to work, '
            'and put time and effort into it, meaning spending time together, '
            'talking to each other etc., then nothing shall stand in your way.'
        ),
    }
    
    for x in range(21, 31):
        yield value
    
    value = {
        'titles':(
            f'{BUILTIN_EMOJIS["cupid"]} You two are really close aren\'t you? {BUILTIN_EMOJIS["cupid"]}',
        ),
        'text': (
            'Your relationship has a reasonable amount of working out. But do '
            'not overestimate yourself there. Your relationship will suffer '
            'good and bad times. Make sure to not let the bad times destroy '
            'your relationship, so do not hesitate to talk to each other, '
            'figure problems out together etc.'
        ),
    }
    
    for x in range(31, 46):
        yield value
    
    value = {
        'titles': (
            f'{BUILTIN_EMOJIS["heart"]} So when will you two go on a date? {BUILTIN_EMOJIS["heart"]}',
        ),
        'text': (
            'Your relationship will most likely work out. It won\'t be perfect '
            'and you two need to spend a lot of time together, but if you keep '
            'on having contact, the good times in your relationship will '
            'outweigh the bad ones.'
        ),
    }
    
    for x in range(46, 61):
        yield value
    
    value = {
        'titles': (
            f'{BUILTIN_EMOJIS["two_hearts"]} Aww look you two fit so well together {BUILTIN_EMOJIS["two_hearts"]}',
        ),
        'text': (
            'Your relationship will most likely work out well. Don\'t hesitate '
            'on making contact with each other though, as your relationship '
            'might suffer from a lack of time spent together. Talking with '
            'each other and spending time together is key.'
        ),
    }

    for x in range(61, 86):
        yield value
    
    value = {
        'titles': (
            f'{BUILTIN_EMOJIS["sparkling_heart"]} Love is in the air {BUILTIN_EMOJIS["sparkling_heart"]}',
            f'{BUILTIN_EMOJIS["sparkling_heart"]} Planned your future yet? {BUILTIN_EMOJIS["sparkling_heart"]}',
        ),
        'text': (
            'Your relationship will most likely work out perfect. This '
            'doesn\'t mean thought that you don\'t need to put effort into it. '
            'Talk to each other, spend time together, and you two won\'t have '
            'a hard time.'
        ),
    }
    
    for x in range(86, 96):
        yield value
    
    value = {
        'titles': (
            f'{BUILTIN_EMOJIS["sparkling_heart"]} When will you two marry? {BUILTIN_EMOJIS["sparkling_heart"]}',
            f'{BUILTIN_EMOJIS["sparkling_heart"]} Now kiss already {BUILTIN_EMOJIS["sparkling_heart"]}',
        ),
        'text': (
            'You two will most likely have the perfect relationship. But don\'t '
            'think that this means you don\'t have to do anything for it to '
            'work. Talking to each other and spending time together is key, '
            'even in a seemingly perfect relationship.'
        ),
    }
    
    for x in range(96, 101):
        yield value

LOVE_VALUES = tuple(generate_love_level())
del generate_love_level

@FEATURE_CLIENTS.interactions(is_global = True)
async def love(client, event,
    user_1: ('user', 'Select your heart\'s chosen one!', 'user') = None,
    user_2: ('user', 'Check some else\'s love life?', 'with') = None,
):
    """How much you two fit together?"""
    if user_2 is None:
        source_user = event.user
        
        if user_1 is None:
            target_user = client
        else:
            target_user = user_1
    else:
        target_user = user_2
        
        if user_1 is None:
            source_user = event.user
        else:
            source_user = user_1
    
    if source_user is target_user:
        abort('huh?')
    
    percent = get_affinity_percent(source_user.id, target_user.id & 0x1111111111111111111111)
    element = LOVE_VALUES[percent]
    
    return Embed(
        choice(element['titles']),
        f'{source_user:f} {BUILTIN_EMOJIS["heart"]} {target_user:f} scored {percent}%!',
        color = 0xad1457,
    ).add_field(
        'My advice:',
        element['text'],
    )
