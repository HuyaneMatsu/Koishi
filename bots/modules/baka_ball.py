from hata import Client, Embed
from bot_utils.constants import GUILD__SUPPORT
from hata.ext.slash import abort
from hata.ext.extension_loader import require
from hashlib import md5

def hash_string(string):
    return int.from_bytes(md5(string.encode()).digest(), 'big') & 0xffffffffffffffff


require('Marisa')

SLASH_CLIENT: Client


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
    'Very doubtful',
    None,
]

BAKA_BALL_IMAGE = 'https://cdn.discordapp.com/attachments/568837922288173058/939974559476621352/chiruno-run.gif'

@SLASH_CLIENT.interactions(guild=GUILD__SUPPORT, name="9ball-preview")
async def baka_ball(
    event,
    question: str,
):
    if len(question.split()) < 3:
        abort('Please ask 2 and longer.')
    
    if len(question) > 2000:
        question = question[:2000]
    
    user = event.user
    response = BAKA_BALL_RESPONSES[(hash_string(question.casefold()) ^ user.id) % len(BAKA_BALL_RESPONSES)]
    
    embed = Embed(description=question).add_author(user.avatar_url, user.full_name)
    
    if response is None:
        
        embed.add_image(
            BAKA_BALL_IMAGE,
        )
    else:
        embed.add_field('⑨ Ball', response).add_thumbnail(BAKA_BALL_IMAGE)
    
    return embed
