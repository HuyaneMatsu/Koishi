__all__ = ()

from random import random, randint

from hata import Client, Embed, DiscordException, ERROR_CODES
from hata.ext.slash import P

from ..bots import FEATURE_CLIENTS



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
    n1: P('int', 'Number limit.', min_value = - 1 << 52, max_value = 1 << 52),
    n2: P('int', 'Other number limit!', min_value = - 1 << 52, max_value = 1 << 52) = 0,
):
    """Do you need some random numbers?"""
    if n1 == n2:
        result = n1
    else:
        if n2 < n1:
            n1, n2 = n2, n1
        
        result = randint(n1, n2)
    
    return str(result)
