from hata import Client, Embed
from hata.ext.slash import abort
from hashlib import md5

def hash_string(string):
    return int.from_bytes(md5(string.encode()).digest(), 'big') & 0xffffffffffffffff


SLASH_CLIENT: Client


BAKA_BALL_RESPONSES = [
    'It\'s cool even in the summers',
    'Happy Cirno day!',
    'Dai agrees',
    'Perfect like my math class',
    'Cirno approved!',
    'You can\'t hide and seek with it',
    'They will never find the bodies',
    'Looks cool',
    '9 / 9',
    'There are many like it',
    'What\'s that?',
    'I\'m playing now, ask later',
    'You don\'t wanna know Lili',
    'Where is Dai?',
    'What? I wasn\'t listening',
    'Might have got the stupid',
    'No brain, head empty',
    'Nope, Dai says it\'s not',
    'Too tan',
    'Your score is 0%. Correct! Well done.',
    None,
]

BAKA_BALL_IMAGE = 'https://cdn.discordapp.com/attachments/568837922288173058/939974559476621352/chiruno-run.gif'

@SLASH_CLIENT.interactions(is_global=True, name='9ball')
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
