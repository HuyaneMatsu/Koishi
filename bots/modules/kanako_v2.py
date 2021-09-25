import os, re
from random import randint, choice
from itertools import chain

from hata import ERROR_CODES, BUILTIN_EMOJIS, CancelledError, Task, sleep, InvalidStateError, any_to_any, Color, \
    Embed, DiscordException, ReuBytesIO, LOOP_TIME, Client, KOKORO, future_or_timeout, Future, InteractionEvent, \
    Permission

from hata.ext.slash import abort, Row, Button, ButtonStyle, InteractionResponse

from bot_utils.constants import PATH__KOISHI, GUILD__STORAGE, GUILD__NEKO_DUNGEON
from bot_utils.tools import Pagination10step
from PIL import Image as PIL

SLASH_CLIENT : Client

FONT = PIL.font(os.path.join(PATH__KOISHI, 'library', 'Kozuka.otf'), 90)
FONT_COLOR = (162, 61, 229)
TIMEOUT = 300.0

PAIRS_K = ('k', 'g', 's', 'z', 'c', 't', 'd', 'f', 'h', 'b', 'p', 'n', 'm', 'y', 'r', 'w', 'j',)

PAIRS_KX = {
    'k': ('k', 'g'),
    'g': ('k', 'g'),
    's': ('s', 'z', 'c'),
    'z': ('s', 'z', 'c'),
    'c': ('s', 'z', 'c'),
    't': ('t', 'd'),
    'd': ('t', 'd'),
    'f': ('f', 'h', 'b', 'p'),
    'h': ('f', 'h', 'b', 'p'),
    'b': ('f', 'h', 'b', 'p'),
    'p': ('f', 'h', 'b', 'p')
}

PAIRS_D = ('a', 'i', 'e', 'o', 'u')

HIRAGANA = [
    ('あ', 'a'), ('い', 'i'), ('う', 'u'), ('え', 'e'), ('お', 'o'),
    ('か', 'ka'), ('き', 'ki'), ('く', 'ku'), ('け', 'ke'), ('こ', 'ko'),
    ('が', 'ga'), ('ぎ', 'gi'), ('ぐ', 'gu'), ('げ', 'ge'), ('ご', 'go'),
    ('さ', 'sa'), ('し', 'shi'), ('す', 'su'), ('せ', 'se'), ('そ', 'so'),
    ('ざ', 'za'), ('じ', 'ji'), ('ず', 'zu'), ('ぜ', 'ze'), ('ぞ', 'zo'),
    ('た', 'ta'), ('ち', 'chi'), ('つ', 'tsu'), ('て', 'te'), ('と', 'to'),
    ('だ', 'da'), ('ぢ', 'ji'), ('づ', 'zu'), ('で', 'de'), ('ど', 'do'),
    ('な', 'na'), ('に', 'ni'), ('ぬ', 'nu'), ('ね', 'ne'), ('の', 'no'),
    ('は', 'ha'), ('ひ', 'hi'), ('ふ', 'fu'), ('へ', 'he'), ('ほ', 'ho'),
    ('ば', 'ba'), ('び', 'bi'), ('ぶ', 'bu'), ('べ', 'be'), ('ぼ', 'bo'),
    ('ぱ', 'pa'), ('ぴ', 'pi'), ('ぷ', 'pu'), ('ぺ', 'pe'), ('ぽ', 'po'),
    ('ま', 'ma'), ('み', 'mi'), ('む', 'mu'), ('め', 'me'), ('も', 'mo'),
    ('ら', 'ra'), ('り', 'ri'), ('る', 'ru'), ('れ', 're'), ('ろ', 'ro'),
    ('わ', 'wa'), ('ゐ', 'wi'), ('ゔ', 'vu'), ('ゑ', 'we'), ('を', 'wo'),
    ('や', 'ya'), ('ゆ', 'yu'), ('よ', 'yo'),
    ('ん', 'n'),
    ('きゃ', 'kya'), ('きゅ', 'kyu'), ('きょ', 'kyo'),
    ('ぎゃ', 'gya'), ('ぎゅ', 'gyu'), ('ぎょ', 'gyo'),
    ('しゃ', 'sha'), ('しゅ', 'shu'), ('しょ', 'sho'),
    ('じゃ', 'ja'), ('じゅ', 'ju'), ('じょ', 'jo'),
    ('ちゃ', 'cha'), ('ちゅ', 'chu'), ('ちょ', 'cho'),
    ('ぢゃ', 'ja'), ('ぢゅ', 'ju'), ('ぢょ', 'jo'),
    ('にゃ', 'nya'), ('にゅ', 'nyu'), ('にょ', 'nyo'),
    ('ひゃ', 'hya'), ('ひゅ', 'hyu'), ('ひょ', 'hyo'),
    ('びゃ', 'bya'), ('びゅ', 'byu'), ('びょ', 'byo'),
    ('ぴゃ', 'pya'), ('ぴゅ', 'pyu'), ('ぴょ', 'pyo'),
    ('みゃ', 'mya'), ('みゅ', 'myu'), ('みょ', 'myo'),
    ('りゃ', 'rya'), ('りゅ', 'ryu'), ('りょ', 'ryo'),
]

KATAKANA = [
    ('ア', 'a'), ('イ', 'i'), ('ウ', 'u'), ('エ', 'e'), ('オ', 'o'),
    ('カ', 'ka'), ('キ', 'ki'), ('ク', 'ku'), ('ケ', 'ke'), ('コ', 'ko'),
    ('ガ', 'ga'), ('ギ', 'gi'), ('グ', 'gu'), ('ゲ', 'ge'), ('ゴ', 'go'),
    ('サ', 'sa'), ('シ', 'shi'), ('ス', 'su'), ('セ', 'se'), ('ソ', 'so'),
    ('ザ', 'za'), ('ジ', 'ji'), ('ズ', 'zu'), ('ゼ', 'ze'), ('ゾ', 'zo'),
    ('タ', 'ta'), ('チ', 'chi'), ('ツ', 'tsu'), ('テ', 'te'), ('ト', 'to'),
    ('ダ', 'da'), ('ヂ', 'ji'), ('ヅ', 'zu'), ('デ', 'de'), ('ド', 'do'),
    ('ナ', 'na'), ('ニ', 'ni'), ('ヌ', 'nu'), ('ネ', 'ne'), ('ノ', 'no'),
    ('ハ', 'ha'), ('ヒ', 'hi'), ('フ', 'fu'), ('ヘ', 'he'), ('ホ', 'ho'),
    ('バ', 'ba'), ('ビ', 'bi'), ('ブ', 'bu'), ('ベ', 'be'), ('ボ', 'bo'),
    ('パ', 'pa'), ('ピ', 'pi'), ('プ', 'pu'), ('ペ', 'pe'), ('ポ', 'po'),
    ('マ', 'ma'), ('ミ', 'mi'), ('ム', 'mu'), ('メ', 'me'), ('モ', 'mo'),
    ('ラ', 'ra'), ('リ', 'ri'), ('ル', 'ru'), ('レ', 're'), ('ロ', 'ro'),
    ('ワ', 'wa'), ('ヸ', 'wi'), ('ヴ', 'vu'), ('ヹ', 'we'), ('ヲ', 'wo'),
    ('ヤ', 'ya'), ('ュ', 'yu'), ('ョ', 'yo'),
    ('ン', 'n'),
    ('キャ', 'kya'), ('キュ', 'kyu'), ('キョ', 'kyo'),
    ('ギャ', 'gya'), ('ギュ', 'gyu'), ('ギョ', 'gyo'),
    ('シャ', 'sha'), ('シュ', 'shu'), ('ショ', 'sho'),
    ('ジャ', 'ja'), ('ジュ', 'ju'), ('ジョ', 'jo'),
    ('チャ', 'cha'), ('チュ', 'chu'), ('チョ', 'cho'),
    ('ヂャ', 'ja'), ('ヂュ', 'ju'), ('ヂョ', 'jo'),
    ('ニャ', 'nya'), ('ニュ', 'nyu'), ('ニョ', 'nyo'),
    ('ヒャ', 'hya'), ('ヒュ', 'hyu'), ('ヒョ', 'hyo'),
    ('ビャ', 'bya'), ('ビュ', 'byu'), ('ビョ', 'byo'),
    ('ピャ', 'pya'), ('ピュ', 'pyu'), ('ピョ', 'pyo'),
    ('ミャ', 'mya'), ('ミュ', 'myu'), ('ミョ', 'myo'),
    ('リャ', 'rya'), ('リュ', 'ryu'), ('リョ', 'ryo'),
]

NAME_HIRAGANA = 'hiragana'
NAME_KATAKANA = 'katakana'

MAPS = {NAME_HIRAGANA:HIRAGANA, NAME_KATAKANA:KATAKANA}


CIRCLE_TIME = 60.0
MODIFY_BEFORE = 10.0
NOTIFY_AFTER = CIRCLE_TIME-MODIFY_BEFORE

KANAKO_COLOR = Color.from_tuple(FONT_COLOR)

def draw(buffer, text):
    image = PIL.new('RGBA', FONT.getsize(text), (0, 0, 0, 0))
    image.draw().text((0,0), text, fill=FONT_COLOR, font=FONT)
    image.save(buffer, 'png')
    buffer.seek(0)
    return buffer


@SLASH_CLIENT.interactions(guild=GUILD__STORAGE)
async def create_images(client, event):
    await client.interaction_response_message_create(event, 'Starting to create images.\nIt may take some time.')
    
    relation = []
    buffer = ReuBytesIO()
    
    for relation_pair in chain.from_iterable(MAPS.values()):
        question = relation_pair[0]
        draw(buffer, question)
        
        message = await client.interaction_followup_message_create(event, file=('a.png', buffer))
        
        relation.append((question, message.attachment.url))
    
    file_parts = []
    file_parts.append('RELATIONS = {\n')
    
    for question, url in relation:
        file_parts.append('    ')
        file_parts.append(repr(question))
        file_parts.append(': ')
        file_parts.append(repr(url))
        file_parts.append(',\n')
    
    file_parts.append('}\n')
    
    file = ''.join(file_parts)
    
    await client.interaction_followup_message_create(
        event,
        'Please copy the file\'s content',
        file = ('relations.py', file),
    )

RELATIONS = {
    'あ': 'https://cdn.discordapp.com/attachments/568837922288173058/884484347007205466/a.png',
    'い': 'https://cdn.discordapp.com/attachments/568837922288173058/884484347846082560/a.png',
    'う': 'https://cdn.discordapp.com/attachments/568837922288173058/884484348651372604/a.png',
    'え': 'https://cdn.discordapp.com/attachments/568837922288173058/884484349297295460/a.png',
    'お': 'https://cdn.discordapp.com/attachments/568837922288173058/884484350572371968/a.png',
    'か': 'https://cdn.discordapp.com/attachments/568837922288173058/884484355865608232/a.png',
    'き': 'https://cdn.discordapp.com/attachments/568837922288173058/884484357329408030/a.png',
    'く': 'https://cdn.discordapp.com/attachments/568837922288173058/884484358600265809/a.png',
    'け': 'https://cdn.discordapp.com/attachments/568837922288173058/884484359388815360/a.png',
    'こ': 'https://cdn.discordapp.com/attachments/568837922288173058/884484360387035166/a.png',
    'が': 'https://cdn.discordapp.com/attachments/568837922288173058/884484364874965062/a.png',
    'ぎ': 'https://cdn.discordapp.com/attachments/568837922288173058/884484365789298688/a.png',
    'ぐ': 'https://cdn.discordapp.com/attachments/568837922288173058/884484366472974386/a.png',
    'げ': 'https://cdn.discordapp.com/attachments/568837922288173058/884484367286673478/a.png',
    'ご': 'https://cdn.discordapp.com/attachments/568837922288173058/884484368360427591/a.png',
    'さ': 'https://cdn.discordapp.com/attachments/568837922288173058/884484374005940316/a.png',
    'し': 'https://cdn.discordapp.com/attachments/568837922288173058/884484375104880710/a.png',
    'す': 'https://cdn.discordapp.com/attachments/568837922288173058/884484376270868540/a.png',
    'せ': 'https://cdn.discordapp.com/attachments/568837922288173058/884484377235558410/a.png',
    'そ': 'https://cdn.discordapp.com/attachments/568837922288173058/884484378099605524/a.png',
    'ざ': 'https://cdn.discordapp.com/attachments/568837922288173058/884484382721708082/a.png',
    'じ': 'https://cdn.discordapp.com/attachments/568837922288173058/884484385108271124/a.png',
    'ず': 'https://cdn.discordapp.com/attachments/568837922288173058/884484386739879996/a.png',
    'ぜ': 'https://cdn.discordapp.com/attachments/568837922288173058/884484387566133268/a.png',
    'ぞ': 'https://cdn.discordapp.com/attachments/568837922288173058/884484388522430464/a.png',
    'た': 'https://cdn.discordapp.com/attachments/568837922288173058/884484391806578738/a.png',
    'ち': 'https://cdn.discordapp.com/attachments/568837922288173058/884484392712552488/a.png',
    'つ': 'https://cdn.discordapp.com/attachments/568837922288173058/884484393782091836/a.png',
    'て': 'https://cdn.discordapp.com/attachments/568837922288173058/884484395183013948/a.png',
    'と': 'https://cdn.discordapp.com/attachments/568837922288173058/884484396248334396/a.png',
    'だ': 'https://cdn.discordapp.com/attachments/568837922288173058/884484599198150738/a.png',
    'ぢ': 'https://cdn.discordapp.com/attachments/568837922288173058/884484600125083688/a.png',
    'づ': 'https://cdn.discordapp.com/attachments/568837922288173058/884484601156886538/a.png',
    'で': 'https://cdn.discordapp.com/attachments/568837922288173058/884484602331295765/a.png',
    'ど': 'https://cdn.discordapp.com/attachments/568837922288173058/884484603132411954/a.png',
    'な': 'https://cdn.discordapp.com/attachments/568837922288173058/884484608249454673/a.png',
    'に': 'https://cdn.discordapp.com/attachments/568837922288173058/884484608962469929/a.png',
    'ぬ': 'https://cdn.discordapp.com/attachments/568837922288173058/884484610103324713/a.png',
    'ね': 'https://cdn.discordapp.com/attachments/568837922288173058/884484611269353532/a.png',
    'の': 'https://cdn.discordapp.com/attachments/568837922288173058/884484612246630480/a.png',
    'は': 'https://cdn.discordapp.com/attachments/568837922288173058/884484617200099348/a.png',
    'ひ': 'https://cdn.discordapp.com/attachments/568837922288173058/884484618097659984/a.png',
    'ふ': 'https://cdn.discordapp.com/attachments/568837922288173058/884484618986881055/a.png',
    'へ': 'https://cdn.discordapp.com/attachments/568837922288173058/884484619787984916/a.png',
    'ほ': 'https://cdn.discordapp.com/attachments/568837922288173058/884484620618444820/a.png',
    'ば': 'https://cdn.discordapp.com/attachments/568837922288173058/884484626465316914/a.png',
    'び': 'https://cdn.discordapp.com/attachments/568837922288173058/884484627211894794/a.png',
    'ぶ': 'https://cdn.discordapp.com/attachments/568837922288173058/884484628084326400/a.png',
    'べ': 'https://cdn.discordapp.com/attachments/568837922288173058/884484628642140230/a.png',
    'ぼ': 'https://cdn.discordapp.com/attachments/568837922288173058/884484629422301244/a.png',
    'ぱ': 'https://cdn.discordapp.com/attachments/568837922288173058/884484635239788564/a.png',
    'ぴ': 'https://cdn.discordapp.com/attachments/568837922288173058/884484636179333221/a.png',
    'ぷ': 'https://cdn.discordapp.com/attachments/568837922288173058/884484636959453214/a.png',
    'ぺ': 'https://cdn.discordapp.com/attachments/568837922288173058/884484637924130847/a.png',
    'ぽ': 'https://cdn.discordapp.com/attachments/568837922288173058/884484638763016264/a.png',
    'ま': 'https://cdn.discordapp.com/attachments/568837922288173058/884484644077174905/a.png',
    'み': 'https://cdn.discordapp.com/attachments/568837922288173058/884484645272563772/a.png',
    'む': 'https://cdn.discordapp.com/attachments/568837922288173058/884484646275010600/a.png',
    'め': 'https://cdn.discordapp.com/attachments/568837922288173058/884484647449427968/a.png',
    'も': 'https://cdn.discordapp.com/attachments/568837922288173058/884484649366196244/a.png',
    'ら': 'https://cdn.discordapp.com/attachments/568837922288173058/884484851204513882/a.png',
    'り': 'https://cdn.discordapp.com/attachments/568837922288173058/884484852169191474/a.png',
    'る': 'https://cdn.discordapp.com/attachments/568837922288173058/884484853045809262/a.png',
    'れ': 'https://cdn.discordapp.com/attachments/568837922288173058/884484853855305778/a.png',
    'ろ': 'https://cdn.discordapp.com/attachments/568837922288173058/884484855218470982/a.png',
    'わ': 'https://cdn.discordapp.com/attachments/568837922288173058/884484860448759808/a.png',
    'ゐ': 'https://cdn.discordapp.com/attachments/568837922288173058/884484861195354162/a.png',
    'ゔ': 'https://cdn.discordapp.com/attachments/568837922288173058/884484861790945321/a.png',
    'ゑ': 'https://cdn.discordapp.com/attachments/568837922288173058/884484862571085824/a.png',
    'を': 'https://cdn.discordapp.com/attachments/568837922288173058/884484863254724711/a.png',
    'や': 'https://cdn.discordapp.com/attachments/568837922288173058/884484868745093130/a.png',
    'ゆ': 'https://cdn.discordapp.com/attachments/568837922288173058/884484869659447306/a.png',
    'よ': 'https://cdn.discordapp.com/attachments/568837922288173058/884484870670258256/a.png',
    'ん': 'https://cdn.discordapp.com/attachments/568837922288173058/884484872176029826/a.png',
    'きゃ': 'https://cdn.discordapp.com/attachments/568837922288173058/884484873614655508/a.png',
    'きゅ': 'https://cdn.discordapp.com/attachments/568837922288173058/884484877804781578/a.png',
    'きょ': 'https://cdn.discordapp.com/attachments/568837922288173058/884484878782042122/a.png',
    'ぎゃ': 'https://cdn.discordapp.com/attachments/568837922288173058/884484879922917396/a.png',
    'ぎゅ': 'https://cdn.discordapp.com/attachments/568837922288173058/884484881206349905/a.png',
    'ぎょ': 'https://cdn.discordapp.com/attachments/568837922288173058/884484882317856799/a.png',
    'しゃ': 'https://cdn.discordapp.com/attachments/568837922288173058/884484887158063144/a.png',
    'しゅ': 'https://cdn.discordapp.com/attachments/568837922288173058/884484888273764352/a.png',
    'しょ': 'https://cdn.discordapp.com/attachments/568837922288173058/884484889154555974/a.png',
    'じゃ': 'https://cdn.discordapp.com/attachments/568837922288173058/884484889787924510/a.png',
    'じゅ': 'https://cdn.discordapp.com/attachments/568837922288173058/884484890672902184/a.png',
    'じょ': 'https://cdn.discordapp.com/attachments/568837922288173058/884484896041611294/a.png',
    'ちゃ': 'https://cdn.discordapp.com/attachments/568837922288173058/884484896863694868/a.png',
    'ちゅ': 'https://cdn.discordapp.com/attachments/568837922288173058/884484897996157018/a.png',
    'ちょ': 'https://cdn.discordapp.com/attachments/568837922288173058/884484898851807312/a.png',
    'ぢゃ': 'https://cdn.discordapp.com/attachments/568837922288173058/884484899753570334/a.png',
    'ぢゅ': 'https://cdn.discordapp.com/attachments/568837922288173058/884485103298953256/a.png',
    'ぢょ': 'https://cdn.discordapp.com/attachments/568837922288173058/884485104238489610/a.png',
    'にゃ': 'https://cdn.discordapp.com/attachments/568837922288173058/884485105203167262/a.png',
    'にゅ': 'https://cdn.discordapp.com/attachments/568837922288173058/884485108764147712/a.png',
    'にょ': 'https://cdn.discordapp.com/attachments/568837922288173058/884485109565227008/a.png',
    'ひゃ': 'https://cdn.discordapp.com/attachments/568837922288173058/884485112476094505/a.png',
    'ひゅ': 'https://cdn.discordapp.com/attachments/568837922288173058/884485113843425400/a.png',
    'ひょ': 'https://cdn.discordapp.com/attachments/568837922288173058/884485115235926086/a.png',
    'びゃ': 'https://cdn.discordapp.com/attachments/568837922288173058/884485116615884810/a.png',
    'びゅ': 'https://cdn.discordapp.com/attachments/568837922288173058/884485118020968488/a.png',
    'びょ': 'https://cdn.discordapp.com/attachments/568837922288173058/884485121523212398/a.png',
    'ぴゃ': 'https://cdn.discordapp.com/attachments/568837922288173058/884485122538221708/a.png',
    'ぴゅ': 'https://cdn.discordapp.com/attachments/568837922288173058/884485123259658270/a.png',
    'ぴょ': 'https://cdn.discordapp.com/attachments/568837922288173058/884485124320796735/a.png',
    'みゃ': 'https://cdn.discordapp.com/attachments/568837922288173058/884485125587472466/a.png',
    'みゅ': 'https://cdn.discordapp.com/attachments/568837922288173058/884485130222207026/a.png',
    'みょ': 'https://cdn.discordapp.com/attachments/568837922288173058/884485131488878622/a.png',
    'りゃ': 'https://cdn.discordapp.com/attachments/568837922288173058/884485132218675261/a.png',
    'りゅ': 'https://cdn.discordapp.com/attachments/568837922288173058/884485133355327548/a.png',
    'りょ': 'https://cdn.discordapp.com/attachments/568837922288173058/884485135494426644/a.png',
    'ア': 'https://cdn.discordapp.com/attachments/568837922288173058/884485139080577064/a.png',
    'イ': 'https://cdn.discordapp.com/attachments/568837922288173058/884485139965546547/a.png',
    'ウ': 'https://cdn.discordapp.com/attachments/568837922288173058/884485140829577216/a.png',
    'エ': 'https://cdn.discordapp.com/attachments/568837922288173058/884485142121439262/a.png',
    'オ': 'https://cdn.discordapp.com/attachments/568837922288173058/884485143048359956/a.png',
    'カ': 'https://cdn.discordapp.com/attachments/568837922288173058/884485148098310154/a.png',
    'キ': 'https://cdn.discordapp.com/attachments/568837922288173058/884485148849090580/a.png',
    'ク': 'https://cdn.discordapp.com/attachments/568837922288173058/884485149557919814/a.png',
    'ケ': 'https://cdn.discordapp.com/attachments/568837922288173058/884485150430330910/a.png',
    'コ': 'https://cdn.discordapp.com/attachments/568837922288173058/884485151197913158/a.png',
    'ガ': 'https://cdn.discordapp.com/attachments/568837922288173058/884485355460493352/a.png',
    'ギ': 'https://cdn.discordapp.com/attachments/568837922288173058/884485356752339035/a.png',
    'グ': 'https://cdn.discordapp.com/attachments/568837922288173058/884485357549256774/a.png',
    'ゲ': 'https://cdn.discordapp.com/attachments/568837922288173058/884485358463631481/a.png',
    'ゴ': 'https://cdn.discordapp.com/attachments/568837922288173058/884485359197618226/a.png',
    'サ': 'https://cdn.discordapp.com/attachments/568837922288173058/884485364444717086/a.png',
    'シ': 'https://cdn.discordapp.com/attachments/568837922288173058/884485365493293156/a.png',
    'ス': 'https://cdn.discordapp.com/attachments/568837922288173058/884485366512513034/a.png',
    'セ': 'https://cdn.discordapp.com/attachments/568837922288173058/884485367305232484/a.png',
    'ソ': 'https://cdn.discordapp.com/attachments/568837922288173058/884485368064376902/a.png',
    'ザ': 'https://cdn.discordapp.com/attachments/568837922288173058/884485373563138058/a.png',
    'ジ': 'https://cdn.discordapp.com/attachments/568837922288173058/884485374477484032/a.png',
    'ズ': 'https://cdn.discordapp.com/attachments/568837922288173058/884485375408631848/a.png',
    'ゼ': 'https://cdn.discordapp.com/attachments/568837922288173058/884485376742408242/a.png',
    'ゾ': 'https://cdn.discordapp.com/attachments/568837922288173058/884485377916825621/a.png',
    'タ': 'https://cdn.discordapp.com/attachments/568837922288173058/884485382694121512/a.png',
    'チ': 'https://cdn.discordapp.com/attachments/568837922288173058/884485383423930388/a.png',
    'ツ': 'https://cdn.discordapp.com/attachments/568837922288173058/884485384334110790/a.png',
    'テ': 'https://cdn.discordapp.com/attachments/568837922288173058/884485385126834236/a.png',
    'ト': 'https://cdn.discordapp.com/attachments/568837922288173058/884485386154418176/a.png',
    'ダ': 'https://cdn.discordapp.com/attachments/568837922288173058/884485392156483595/a.png',
    'ヂ': 'https://cdn.discordapp.com/attachments/568837922288173058/884485392953409586/a.png',
    'ヅ': 'https://cdn.discordapp.com/attachments/568837922288173058/884485394203303946/a.png',
    'デ': 'https://cdn.discordapp.com/attachments/568837922288173058/884485395482542120/a.png',
    'ド': 'https://cdn.discordapp.com/attachments/568837922288173058/884485396816363530/a.png',
    'ナ': 'https://cdn.discordapp.com/attachments/568837922288173058/884485400951918592/a.png',
    'ニ': 'https://cdn.discordapp.com/attachments/568837922288173058/884485402076016670/a.png',
    'ヌ': 'https://cdn.discordapp.com/attachments/568837922288173058/884485403074265119/a.png',
    'ネ': 'https://cdn.discordapp.com/attachments/568837922288173058/884485403908898836/a.png',
    'ノ': 'https://cdn.discordapp.com/attachments/568837922288173058/884485404923932722/a.png',
    'ハ': 'https://cdn.discordapp.com/attachments/568837922288173058/884485607584321646/a.png',
    'ヒ': 'https://cdn.discordapp.com/attachments/568837922288173058/884485608515436554/a.png',
    'フ': 'https://cdn.discordapp.com/attachments/568837922288173058/884485609530490951/a.png',
    'ヘ': 'https://cdn.discordapp.com/attachments/568837922288173058/884485610176401458/a.png',
    'ホ': 'https://cdn.discordapp.com/attachments/568837922288173058/884485611300483112/a.png',
    'バ': 'https://cdn.discordapp.com/attachments/568837922288173058/884485616748888084/a.png',
    'ビ': 'https://cdn.discordapp.com/attachments/568837922288173058/884485617692581958/a.png',
    'ブ': 'https://cdn.discordapp.com/attachments/568837922288173058/884485619517108234/a.png',
    'ベ': 'https://cdn.discordapp.com/attachments/568837922288173058/884485620511178803/a.png',
    'ボ': 'https://cdn.discordapp.com/attachments/568837922288173058/884485621668790322/a.png',
    'パ': 'https://cdn.discordapp.com/attachments/568837922288173058/884485625514950686/a.png',
    'ピ': 'https://cdn.discordapp.com/attachments/568837922288173058/884485626269933649/a.png',
    'プ': 'https://cdn.discordapp.com/attachments/568837922288173058/884485627507269662/a.png',
    'ペ': 'https://cdn.discordapp.com/attachments/568837922288173058/884485628396449852/a.png',
    'ポ': 'https://cdn.discordapp.com/attachments/568837922288173058/884485629407285288/a.png',
    'マ': 'https://cdn.discordapp.com/attachments/568837922288173058/884485634700501042/a.png',
    'ミ': 'https://cdn.discordapp.com/attachments/568837922288173058/884485635522564136/a.png',
    'ム': 'https://cdn.discordapp.com/attachments/568837922288173058/884485636420165652/a.png',
    'メ': 'https://cdn.discordapp.com/attachments/568837922288173058/884485637464543322/a.png',
    'モ': 'https://cdn.discordapp.com/attachments/568837922288173058/884485638722842684/a.png',
    'ラ': 'https://cdn.discordapp.com/attachments/568837922288173058/884485643214917733/a.png',
    'リ': 'https://cdn.discordapp.com/attachments/568837922288173058/884485644674560010/a.png',
    'ル': 'https://cdn.discordapp.com/attachments/568837922288173058/884485645756686406/a.png',
    'レ': 'https://cdn.discordapp.com/attachments/568837922288173058/884485646771699782/a.png',
    'ロ': 'https://cdn.discordapp.com/attachments/568837922288173058/884485647807701062/a.png',
    'ワ': 'https://cdn.discordapp.com/attachments/568837922288173058/884485652316581988/a.png',
    'ヸ': 'https://cdn.discordapp.com/attachments/568837922288173058/884485653096706068/a.png',
    'ヴ': 'https://cdn.discordapp.com/attachments/568837922288173058/884485654426308718/a.png',
    'ヹ': 'https://cdn.discordapp.com/attachments/568837922288173058/884485655692976128/a.png',
    'ヲ': 'https://cdn.discordapp.com/attachments/568837922288173058/884485656695414815/a.png',
    'ヤ': 'https://cdn.discordapp.com/attachments/568837922288173058/884485859636805662/a.png',
    'ュ': 'https://cdn.discordapp.com/attachments/568837922288173058/884485860471496764/a.png',
    'ョ': 'https://cdn.discordapp.com/attachments/568837922288173058/884485861369053274/a.png',
    'ン': 'https://cdn.discordapp.com/attachments/568837922288173058/884485862111465563/a.png',
    'キャ': 'https://cdn.discordapp.com/attachments/568837922288173058/884485863201996820/a.png',
    'キュ': 'https://cdn.discordapp.com/attachments/568837922288173058/884485868809769091/a.png',
    'キョ': 'https://cdn.discordapp.com/attachments/568837922288173058/884485869678002256/a.png',
    'ギャ': 'https://cdn.discordapp.com/attachments/568837922288173058/884485870592340039/a.png',
    'ギュ': 'https://cdn.discordapp.com/attachments/568837922288173058/884485875155755028/a.png',
    'ギョ': 'https://cdn.discordapp.com/attachments/568837922288173058/884485876049133608/a.png',
    'シャ': 'https://cdn.discordapp.com/attachments/568837922288173058/884485878259519538/a.png',
    'シュ': 'https://cdn.discordapp.com/attachments/568837922288173058/884485879622692944/a.png',
    'ショ': 'https://cdn.discordapp.com/attachments/568837922288173058/884485880901959740/a.png',
    'ジャ': 'https://cdn.discordapp.com/attachments/568837922288173058/884485882638393344/a.png',
    'ジュ': 'https://cdn.discordapp.com/attachments/568837922288173058/884485883582099516/a.png',
    'ジョ': 'https://cdn.discordapp.com/attachments/568837922288173058/884485887306637312/a.png',
    'チャ': 'https://cdn.discordapp.com/attachments/568837922288173058/884485888111951952/a.png',
    'チュ': 'https://cdn.discordapp.com/attachments/568837922288173058/884485889051488286/a.png',
    'チョ': 'https://cdn.discordapp.com/attachments/568837922288173058/884485890108456980/a.png',
    'ヂャ': 'https://cdn.discordapp.com/attachments/568837922288173058/884485891194761286/a.png',
    'ヂュ': 'https://cdn.discordapp.com/attachments/568837922288173058/884485896282460180/a.png',
    'ヂョ': 'https://cdn.discordapp.com/attachments/568837922288173058/884485897314254868/a.png',
    'ニャ': 'https://cdn.discordapp.com/attachments/568837922288173058/884485900594200678/a.png',
    'ニュ': 'https://cdn.discordapp.com/attachments/568837922288173058/884485901416292383/a.png',
    'ニョ': 'https://cdn.discordapp.com/attachments/568837922288173058/884485902330634260/a.png',
    'ヒャ': 'https://cdn.discordapp.com/attachments/568837922288173058/884485905283448912/a.png',
    'ヒュ': 'https://cdn.discordapp.com/attachments/568837922288173058/884485906109714502/a.png',
    'ヒョ': 'https://cdn.discordapp.com/attachments/568837922288173058/884485906894037022/a.png',
    'ビャ': 'https://cdn.discordapp.com/attachments/568837922288173058/884485907737116713/a.png',
    'ビュ': 'https://cdn.discordapp.com/attachments/568837922288173058/884485908689207336/a.png',
    'ビョ': 'https://cdn.discordapp.com/attachments/568837922288173058/884486111689338900/a.png',
    'ピャ': 'https://cdn.discordapp.com/attachments/568837922288173058/884486112570130532/a.png',
    'ピュ': 'https://cdn.discordapp.com/attachments/568837922288173058/884486113434140712/a.png',
    'ピョ': 'https://cdn.discordapp.com/attachments/568837922288173058/884486114482741248/a.png',
    'ミャ': 'https://cdn.discordapp.com/attachments/568837922288173058/884486115363545098/a.png',
    'ミュ': 'https://cdn.discordapp.com/attachments/568837922288173058/884486120736440320/a.png',
    'ミョ': 'https://cdn.discordapp.com/attachments/568837922288173058/884486121600458812/a.png',
    'リャ': 'https://cdn.discordapp.com/attachments/568837922288173058/884486122535788614/a.png',
    'リュ': 'https://cdn.discordapp.com/attachments/568837922288173058/884486123517272174/a.png',
    'リョ': 'https://cdn.discordapp.com/attachments/568837922288173058/884486124666511360/a.png',
}


def render_showcase(name,map_):
    result = []
    element_index = 0
    element_limit = len(map_)
    
    page_index = 1
    page_limit = (element_limit+29)//30

    field_text = []
    
    while True:
        if page_index > page_limit:
            break
        
        embed = Embed(name.capitalize(), '', KANAKO_COLOR)
        embed.add_footer(f'page {page_index} / {page_limit}')
        
        for _ in range(((element_limit%30)+9)//10 if (page_index == page_limit) else 3):
            field_index_limit = element_index+10
            if field_index_limit > element_limit:
                field_index_limit = element_limit
            
            while element_index<field_index_limit:
                element = map_[element_index]
                element_index += 1
                field_text.append(f'{element_index}.: **{element[0]} - {element[1]}**')
            
            embed.add_field(f'{element_index-9} - {element_index}', '\n'.join(field_text),inline=True)
            field_text.clear()
        
        result.append(embed)
        page_index += 1
    
    return result

MAP_SHOWCASES = {name: render_showcase(name, map_) for name, map_ in MAPS.items()}


KANAKO = SLASH_CLIENT.interactions(
    None,
    name = 'kanako',
    description = 'Start a hiragana or a katakana quiz!',
    guild = GUILD__NEKO_DUNGEON,
)


@KANAKO.interactions
async def create_(client, event,
        map_ : ([NAME_HIRAGANA, NAME_KATAKANA], 'Choose a map to play!') = NAME_HIRAGANA,
        length : ('int', 'The amount of questions.') = 20,
            ):
    """Create a new game!"""
    if not event.guild_id:
        abort('Guild only command')
    
    KanakoJoinGroup(client, event, map_, length)
    return create_kanako_join_message(event, map_, length)


@KANAKO.interactions
async def show_map(client, event,
        map_ : ([NAME_HIRAGANA, NAME_KATAKANA], 'Choose a map to display!')
            ):
    """Shows the selected map!"""
    pages = MAP_SHOWCASES[map_]
    await Pagination10step(client, event, pages)


class HistoryElement:
    __slots__ = ('answer', 'answers', 'options', 'question',)
    
    def __new__(cls, answer, answers, options, question):
        self = object.__new__(cls)
        self.answer = answer
        self.answers = answers
        self.options = options
        self.question = question
        return self


class GameStatistics:
    __slots__ = ('cache', 'history', 'users',)
    
    def __len__(self):
        return len(self.cache)
    
    def __new__(cls, source):
        self = object.__new__(cls)
        self.users = source.users
        self.history = history = source.history
        self.cache = [None for _ in range((len(history)+9)//10+1)]
        self.create_page_0()
        return self
    
    def create_page_0(self):
        user_count = len(self.users)
        win_counts = [0 for _ in range(user_count)]
        lose_counts = win_counts.copy()
        win_firsts = win_counts.copy()
        lose_firsts = win_counts.copy()
        win_times = [[] for _ in range(user_count)]
        lose_times = [[] for _ in range(user_count)]
    
        for element in self.history:
            answer = element.answer
            answers = element.answers
            first_time = CIRCLE_TIME
            first_index = 0
            first_won = True
            for index in range(user_count):
                value, time = answers[index]
                if value == answer:
                    win_counts[index] += 1
                    win_times[index].append(time)
                    if time < first_time:
                        first_time = time
                        first_index = index
                        first_won = True
                else:
                    lose_counts[index] += 1
                    lose_times[index].append(time)
                    if time < first_time:
                        first_time = time
                        first_index = index
                        first_won = False
                        
            if first_time != CIRCLE_TIME:
                if first_won:
                    win_firsts[first_index] += 1
                else:
                    lose_firsts[first_index] += 1
        
        win_medians = [value[len(value)//2] if value else CIRCLE_TIME for value in win_times]
        lose_medians = [value[len(value)//2] if value else CIRCLE_TIME for value in lose_times]
        
        embed = Embed('Statistics', color=KANAKO_COLOR)
        
        for index, user in enumerate(self.users):
            win_count = win_counts[index]
            lose_count = lose_counts[index]
            win_median = win_medians[index]
            lose_median = lose_medians[index]
            win_first = win_firsts[index]
            lose_first = lose_firsts[index]
            
            total = float(win_count)
            total += (((2**0.5)-1.0)-((((CIRCLE_TIME+win_median)/CIRCLE_TIME)**0.5)-1.0))*win_count
            total += win_first/5.
            total -= (((2**0.5)-1.0)-((((CIRCLE_TIME+lose_median)/CIRCLE_TIME)**0.5)-1.0))*lose_count*2.0
            total -= lose_first*0.4
            
            embed.add_field(f'{user:f} :',
                f'Correct answers : {win_count}\n'
                f'Bad answers : {lose_count}\n'
                f'Good answer time median : {win_median:.2f} s\n'
                f'Bad answer time median : {lose_median:.2f} s\n'
                f'Answered first: {win_first} GOOD / {lose_first} BAD\n'
                f'Rated : {total:.2f}'
            )
        
        embed.add_footer(f'Page 1 / {len(self.cache)}')
        
        self.cache[0] = embed
    
    def __getitem__(self,index):
        page = self.cache[index]
        if page is None:
            return self.create_page(index)
        
        return page
    
    def create_page(self,index):
        end = index*10
        start = end-9
        if end > len(self.history):
            end = len(self.history)
        
        embed = Embed('Statistics', f'{start} - {end}', color=KANAKO_COLOR)
        
        field_value_parts = []
        
        for question_index, history_element in enumerate(self.history[start-1:end], start):
            field_value_parts.append('```diff\n')
            
            options = history_element.options
            option_index = 0
            option_length = len(options)
            
            while True:
                option = options[option_index]
                option_index += 1
                
                field_value_parts.append(repr(option_index))
                field_value_parts.append('. : ')
                field_value_parts.append(option)
                
                if option_index == option_length:
                    break
                
                field_value_parts.append(', ')
            
            for user_index, user in enumerate(self.users):
                value, time = history_element.answers[user_index]
                field_value_parts.append('\n')
                
                if history_element.answer == value:
                    prefix = '+'
                else:
                    prefix = '-'
                
                field_value_parts.append(prefix)
                field_value_parts.append(' ')
                field_value_parts.append(user.full_name)
                field_value_parts.append(' : ')
                field_value_parts.append(value)
                field_value_parts.append(' ( ')
                field_value_parts.append(time.__format__('.2f'))
                field_value_parts.append(' s )')
            
            field_value_parts.append('\n```')
            embed.add_field(
                f'{question_index}.: {history_element.question} - {history_element.answer}',
                ''.join(field_value_parts),
            )
            field_value_parts.clear()
        
        embed.add_footer(f'Page {index+1} / {len(self.cache)}')
        
        self.cache[index] = embed
        return embed

KANAKO_JOIN_GROUPS = {}

class KanakoJoinGroup:
    __slots__ = ('users', 'event', 'handler', 'client', 'map_name', 'length')
    
    def __new__(cls, client, event, map_name, length):
        self = object.__new__(cls)
        self.client = client
        self.event = event
        self.users = {event.user}
        self.handler = KOKORO.call_later(TIMEOUT, self)
        self.map_name = map_name
        self.length = length
        
        KANAKO_JOIN_GROUPS[event.id] = self
        return self
    
    def __call__(self):
        Task(self.close(), KOKORO)
    
    async def close(self):
        self.cancel()
        
        await self.client.interaction_response_message_edit(
            self.event,
            embed = Embed(
                None,
                'Game cancelled, timeout',
            ),
            components = None,
        )
    
    def cancel(self):
        try:
            del KANAKO_JOIN_GROUPS[self.event.id]
        except KeyError:
            pass
        
        handler = self.handler
        if (handler is not None):
            self.handler = None
            handler.cancel()


CUSTOM_ID_KANAKO_JOIN_OR_LEAVE = 'kanako.join_or_leave'
CUSTOM_ID_KANAKO_START = 'kanako.start'
CUSTOM_ID_KANAKO_CANCEL = 'kanako.cancel'

BUTTON_KANAKO_JOIN_OR_LEAVE = Button(
    'Join / Leave',
    custom_id = CUSTOM_ID_KANAKO_JOIN_OR_LEAVE,
    style = ButtonStyle.violet,
)

BUTTON_KANAKO_JOIN_OR_LEAVE_DISABLED = BUTTON_KANAKO_JOIN_OR_LEAVE.copy_with(
    enabled = False,
)

BUTTON_KANAKO_START = Button(
    'Start',
    custom_id = CUSTOM_ID_KANAKO_START,
    style = ButtonStyle.green,
)

BUTTON_KANAKO_CANCEL = Button(
    'Cancel',
    custom_id = CUSTOM_ID_KANAKO_CANCEL,
    style = ButtonStyle.red,
)


COMPONENTS_KANAKO = Row(
    BUTTON_KANAKO_JOIN_OR_LEAVE,
    BUTTON_KANAKO_START,
    BUTTON_KANAKO_CANCEL,
)

COMPONENTS_KANAKO_FULL = Row(
    BUTTON_KANAKO_JOIN_OR_LEAVE_DISABLED,
    BUTTON_KANAKO_START,
    BUTTON_KANAKO_CANCEL,
)


def create_kanako_join_message(event, map_name, length):
    return InteractionResponse(
        embed = Embed(
            'Join a kanako game.',
            (
                f'Map: {map_name}\n'
                f'Game length: {length}'
            ),
            color = KANAKO_COLOR,
        ).add_field(
            'Joined users',
            event.user.full_name,
        ),
        allowed_mentions = event.user,
        components = COMPONENTS_KANAKO,
    )


@SLASH_CLIENT.interactions(custom_id=CUSTOM_ID_KANAKO_JOIN_OR_LEAVE)
async def handle_join_or_leave(event):
    try:
        join_group = KANAKO_JOIN_GROUPS[event.message.interaction.id]
    except KeyError:
        return
    
    user = event.user
    if user is join_group.event.user:
        return
    
    users = join_group.users
    try:
        users.remove(user)
    except KeyError:
        users.add(user)
    
    if len(users) >= 10:
        components = COMPONENTS_KANAKO_FULL
    else:
        components = COMPONENTS_KANAKO
    
    embed = Embed(
        'Join a kanako game.',
        (
            f'Map: {join_group.map_name}\n'
            f'Game length: {join_group.length}'
        ),
        color = KANAKO_COLOR,
    ).add_field(
        'Joined users',
        '\n'.join(user.full_name for user in sorted(users)),
    )
    
    return InteractionResponse(
        embed = embed,
        components = components,
    )


@SLASH_CLIENT.interactions(custom_id=CUSTOM_ID_KANAKO_CANCEL)
async def handle_cancel(client, event):
    interaction = event.message.interaction
    if event.user is not interaction.user:
        return
    
    try:
        join_group = KANAKO_JOIN_GROUPS[interaction.id]
    except KeyError:
        pass
    else:
        join_group.cancel()
    
    await client.interaction_component_acknowledge(event)
    await client.interaction_response_message_delete(event)


@SLASH_CLIENT.interactions(custom_id=CUSTOM_ID_KANAKO_START)
async def handle_start(client, event):
    interaction = event.message.interaction
    if event.user is not interaction.user:
        return
    
    try:
        join_group = KANAKO_JOIN_GROUPS[interaction.id]
    except KeyError:
        return
    
    join_group.cancel()
    
    await KanakoRunner(client, event, join_group.users, join_group.map_name, join_group.length)


CUSTOM_ID_OPTION_0 = 'kanako.solution.0'
CUSTOM_ID_OPTION_1 = 'kanako.solution.1'
CUSTOM_ID_OPTION_2 = 'kanako.solution.2'
CUSTOM_ID_OPTION_3 = 'kanako.solution.3'
CUSTOM_ID_OPTION_4 = 'kanako.solution.4'

CUSTOM_ID_TO_INDEX = {
    CUSTOM_ID_OPTION_0: 0,
    CUSTOM_ID_OPTION_1: 1,
    CUSTOM_ID_OPTION_2: 2,
    CUSTOM_ID_OPTION_3: 3,
    CUSTOM_ID_OPTION_4: 4,
}

class KanakoRunner:
    __slots__ = ('client', 'event', 'users', 'map_name', 'length', 'history', 'answers', 'map', 'romajis', 'options',
        'waiter', 'message', 'cancelled', 'embed')
    
    def __new__(cls, client, event, users, map_name, length):
        self = object.__new__(cls)
        self.client = client
        self.event = event
        self.users = users
        self.message = event.message
        self.map_name = map_name
        self.length = length
        
        self.cancelled = False
        self.waiter = None
        
        self.history = []
        self.answers = {}
        
        full_map = MAPS[map_name].copy()
        limit = len(full_map)-1
        
        self.map = map_ = [full_map.pop(randint(0, limit)) for limit in range(limit, limit-length, -1)]
        self.romajis = {element[1] for element in map_}
        self.options = None
        self.embed = Embed(color=KANAKO_COLOR)
        
        client.slasher.add_component_interaction_waiter(event.message, self)
        
        waiter = Future(KOKORO)
        Task(self.runner(waiter), KOKORO)
        return waiter
        
    def generate_options(self, answer):
        result = [answer]
        target = answer
        ignore = [element.answer for element in self.history[-4:]]
        ignore.append(answer)
        chances = {romaji: randint(0, 2) for romaji in self.romajis if romaji not in ignore}
        ignore = None
        
        counter = 1
        while True:
            ln = len(target)
            if ln == 3 or 'j' in target:
                for key in chances:
                    if len(key) == 3 or 'j' in target:
                        chances[key] += 2
            else:
                for key in chances:
                    if len(key) in (1, 2) and 'j' not in target:
                        chances[key] += 1
            
            if target != 'n':
                for char_d in target:
                    if char_d in PAIRS_D:
                        break
                
                for char_k in target:
                    if char_k in PAIRS_K:
                        break
                
                chars = PAIRS_KX.get(key, None)
                
                if chars is None:
                    for key in chances:
                        if len(key) != ln:
                            continue
                        if char_d in key:
                            chances[key] += 1
                        if char_k in key:
                            chances[key] += 1
                else:
                    for key in chances:
                        if len(key)!=ln:
                            continue
                        if char_d in key:
                            chances[key] += 1
                        if char_k in key:
                            chances[key] += 1
                        if any_to_any(chars, key):
                            chances[key] += 1
            
            goods = []
            maximal = 0
            for key, value in chances.items():
                if value < maximal:
                    continue
                
                if value > maximal:
                    goods.clear()
                    maximal = value
                
                goods.append(key)
            
            target = choice(goods)
            
            result.append(target)
            
            counter += 1
            if counter == 5:
                break
            
            del chances[target]
            
            for key in chances:
                chances[key] = randint(0, 2)
        
        return [result.pop(randint(0, limit)) for limit in range(4, -1, -1)]
    
    async def runner(self, waiter):
        try:
            client = self.client
            answers = self.answers
            embed = self.embed
            for index, (question, answer) in enumerate(self.map, 1):
                embed.add_footer(f'{index} / {len(self.map)}').add_image(RELATIONS[question])
                self.build_base_leftover_description()
                
                self.options = options = self.generate_options(answer)
                
                components = Row(
                    Button(
                        options[0],
                        custom_id = CUSTOM_ID_OPTION_0,
                    ),
                    Button(
                        options[1],
                        custom_id = CUSTOM_ID_OPTION_1,
                    ),
                    Button(
                        options[2],
                        custom_id = CUSTOM_ID_OPTION_2,
                    ),
                    Button(
                        options[3],
                        custom_id = CUSTOM_ID_OPTION_3,
                    ),
                    Button(
                        options[4],
                        custom_id = CUSTOM_ID_OPTION_4,
                    ),
                )
                
                try:
                    await client.interaction_component_message_edit(self.event, embed=embed, components=components)
                except BaseException as err:
                    self.cancel()
                    if isinstance(err, ConnectionError):
                        return
                    
                    raise
                finally:
                    if (waiter is not None):
                        waiter.set_result_if_pending(None)
                        waiter = None
                
                circle_start = LOOP_TIME()
                self.waiter = waiter = Future(KOKORO)
                future_or_timeout(waiter, CIRCLE_TIME)
                
                try:
                    await waiter
                except TimeoutError:
                    leavers = []
                    
                    users = self.users
                    
                    for index in reversed(range(len(users))):
                        user = users[index]
                        if user in answers:
                            continue
                        
                        leavers.append(user)
                        del users[index]
                        
                        for element in self.history:
                            del element.answers[index]
                    
                    if users:
                        continue
                    
                    self.cancel()
                    
                    embed = Embed(
                        None,
                        'No-one gave answer in time, cancelling the game.',
                        color = KANAKO_COLOR,
                    )
                    
                    try:
                        await client.interaction_response_message_edit(
                            self.event,
                            embed = embed,
                            components = None,
                        )
                    except BaseException as err:
                        self.cancel()
                        
                        if isinstance(err, ConnectionError):
                            return
                        
                        raise
                
                if self.cancelled:
                    return
                
                self.waiter = None
                
                self.history.append(HistoryElement(
                    answer,
                    [(value[0], value[1]-circle_start) for value in (answers[user] for user in self.users)],
                    self.options,
                    question,
                ))
                
                answers.clear()
                
                embed.title = f'Last answer: {answer}'
            
            await Pagination10step(client, self.event, GameStatistics(self))
        finally:
            self.cancel()
    
    def cancel(self):
        if self.cancelled:
            return
        
        self.cancelled = True
        self.client.slasher.remove_component_interaction_waiter(self.message, self)
        
        waiter = self.waiter
        if (waiter is not None):
            self.waiter = None
            waiter.set_result_if_pending(None)
    
    
    async def __call__(self, event):
        user = event.user
        if user not in self.users:
            return
        
        waiter = self.waiter
        if (waiter is None):
            return
        
        if waiter.done():
            return
        
        if user in self.answers:
            return
        
        try:
            custom_id_index = CUSTOM_ID_TO_INDEX[event.interaction.custom_id]
        except KeyError:
            return
        
        content = self.options[custom_id_index]
        
        self.answers[user] = (content, LOOP_TIME())
        self.event = event
        
        if len(self.answers) == len(self.users):
            self.waiter.set_result_if_pending(None)
        else:
            self.build_unanswered_leftover_description()
            await self.client.interaction_component_message_edit(event, embed=self.embed)
    
    
    def build_base_leftover_description(self):
        users = self.users
        if len(users) == 1:
            description = None
        else:
            description_parts = ['Waiting for:']
            for user in sorted(users):
                description_parts.append('\n')
                description_parts.append(user.full_name)
            
            description = ''.join(description_parts)
        
        self.embed.description = description
    
    
    def build_unanswered_leftover_description(self):
        unanswered = set(self.users)
        unanswered.difference_update(self.answers.keys())
        
        description_parts = ['Waiting for:']
        for user in sorted(unanswered):
            description_parts.append('\n')
            description_parts.append(user.full_name)
        
        description = ''.join(description_parts)
        
        self.embed.description = description
