from hata import Client, Embed
from collections import OrderedDict
from bot_utils.constants import GUILD__SUPPORT
from hata.ext.slash import abort
from random import choice
from difflib import SequenceMatcher
from hata.ext.extension_loader import require

require('Marisa')

SLASH_CLIENT: Client

CACHED_RESPONSES = OrderedDict()
CACHE_SIZE = 1000

BAKA_BALL_RESPONSES = [
    'It is certain',
    'It is decidedly so',
    'Without a doubt',
    'Yes definitely',
    'You may rely on it',
    'As I see it, yes',
    'Most likely',
    'Outlook good',
    'Yes',
    'Signs point to yes',
    'Reply hazy try again',
    'Ask again later',
    'Better not tell you now',
    'Cannot predict now',
    'Concentrate and ask again',
    'Don\'t count on it',
    'My reply is no',
    'My sources say no',
    'Outlook not so good',
    'Very doubtful'
]

@SLASH_CLIENT.interactions(guild=GUILD__SUPPORT, name="9ball-preview")
async def baka_ball(
    client,
    event,
    question: str,
):
    if len(question.split()) < 3:
        abort()
    
    if len(question) > 2000:
        question = question[:2000]
    
    user_id = event.user.id
    for key in CACHED_RESPONSES.keys():
        if key[0] != user_id:
            continue
        
        match = SequenceMatcher(None, question, key[1]).ratio()
        if match < 0.9:
            continue
        
        CACHED_RESPONSES.move_to_end(key)
        response = CACHED_RESPONSES[key]
        break
    
    else:
        response = choice(BAKA_BALL_RESPONSES)
        CACHED_RESPONSES[(user_id, question)] = response
        
        if len(CACHED_RESPONSES) >= 1000:
            CACHED_RESPONSES.popitem(0)
    
    return Embed(
        '⑨ Ball',
        response,
    )
