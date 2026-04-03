__all__ = ()

from itertools import repeat
from hata import BUILTIN_EMOJIS

from .love_option import LoveOption


LOVE_OPTIONS = (
    *repeat(
        LoveOption(
            '0-1%',
            (
                f'{BUILTIN_EMOJIS["blue_heart"]} There\'s no real connection between you two {BUILTIN_EMOJIS["blue_heart"]}',
            ),
            (
                'The chance of this relationship working out is really low. You '
                'can get it to work, but with high costs and no guarantee of '
                'working out. Do not sit back, spend as much time together as '
                'possible, talk a lot with each other to increase the chances of '
                'this relationship\'s survival.'
            ),
        ),
        2,
    ),
    *repeat(
        LoveOption(
            '2-5%',
            (
                f'{BUILTIN_EMOJIS["blue_heart"]} A small acquaintance {BUILTIN_EMOJIS["blue_heart"]}',
            ),
            (
                'There might be a chance of this relationship working out somewhat '
                'well, but it is not very high. With a lot of time and effort '
                'you\'ll get it to work eventually, however don\'t count on it. It '
                'might fall apart quicker than you\'d expect.'
            ),
        ),
        4,
    ),
    *repeat(
        LoveOption(
            '6-20%',
            (
                f'{BUILTIN_EMOJIS["purple_heart"]} You two seem like casual friends {BUILTIN_EMOJIS["purple_heart"]}',
            ),
            (
                'The chance of this relationship working is not very high. You both '
                'need to put time and effort into this relationship, if you want it '
                'to work out well for both of you. Talk with each other about '
                'everything and don\'t lock yourself up. Spend time together. This '
                'will improve the chances of this relationship\'s survival by a lot.'
            ),
        ),
        15,
    ),
    *repeat(
        LoveOption(
            '21-30%',
            (
                f'{BUILTIN_EMOJIS["heartpulse"]} You seem like you are good friends {BUILTIN_EMOJIS["heartpulse"]}',
            ),
            (
                'The chance of this relationship working is not very high, but its '
                'not that low either. If you both want this relationship to work, '
                'and put time and effort into it, meaning spending time together, '
                'talking to each other etc., then nothing shall stand in your way.'
            ),
        ),
        10,
    ),
    *repeat(
        LoveOption(
            '31-45%',
            (
                f'{BUILTIN_EMOJIS["cupid"]} You two are really close aren\'t you? {BUILTIN_EMOJIS["cupid"]}',
            ),
            (
                'Your relationship has a reasonable amount of working out. But do '
                'not overestimate yourself there. Your relationship will suffer '
                'good and bad times. Make sure to not let the bad times destroy '
                'your relationship, so do not hesitate to talk to each other, '
                'figure problems out together etc.'
            ),
        ),
        15,
    ),
    *repeat(
        LoveOption(
            '46-60%',
            (
                f'{BUILTIN_EMOJIS["heart"]} So when will you two go on a date? {BUILTIN_EMOJIS["heart"]}',
            ),
            (
                'Your relationship will most likely work out. It won\'t be perfect '
                'and you two need to spend a lot of time together, but if you keep '
                'on having contact, the good times in your relationship will '
                'outweigh the bad ones.'
            ),
        ),
        15,
    ),
    *repeat(
        LoveOption(
            '61-85%',
            (
                f'{BUILTIN_EMOJIS["two_hearts"]} Aww look you two fit so well together {BUILTIN_EMOJIS["two_hearts"]}',
            ),
            (
                'Your relationship will most likely work out well. Don\'t hesitate '
                'on making contact with each other though, as your relationship '
                'might suffer from a lack of time spent together. Talking with '
                'each other and spending time together is key.'
            ),
        ),
        25,
    ),
    *repeat(
        LoveOption(
            '86-95%',
            (
                f'{BUILTIN_EMOJIS["sparkling_heart"]} Love is in the air {BUILTIN_EMOJIS["sparkling_heart"]}',
                f'{BUILTIN_EMOJIS["sparkling_heart"]} Planned your future yet? {BUILTIN_EMOJIS["sparkling_heart"]}',
            ),
            (
                'Your relationship will most likely work out perfect. This '
                'doesn\'t mean thought that you don\'t need to put effort into it. '
                'Talk to each other, spend time together, and you two won\'t have '
                'a hard time.'
            ),
        ),
        10,
    ),
    *repeat(
        LoveOption(
            '96-100',
            (
                f'{BUILTIN_EMOJIS["sparkling_heart"]} When will you two marry? {BUILTIN_EMOJIS["sparkling_heart"]}',
                f'{BUILTIN_EMOJIS["sparkling_heart"]} Now kiss already {BUILTIN_EMOJIS["sparkling_heart"]}',
            ),
            (
                'You two will most likely have the perfect relationship. But don\'t '
                'think that this means you don\'t have to do anything for it to '
                'work. Talking to each other and spending time together is key, '
                'even in a seemingly perfect relationship.'
            ),
        ),
        5,
    ),
)
