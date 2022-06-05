__all__ = ()

from re import compile as re_compile, I as re_ignore_case, U as re_unicode, escape as re_escape
from collections import deque
from difflib import get_close_matches

from hata import Embed, Color, BUILTIN_EMOJIS, Client
from hata.ext.slash import abort, Button, Row
from hata.ext.slash.menus import Menu

from bot_utils.tools import BeautifulSoup, choose, pop_one, choose_not_same

BOORU_COLOR = Color.from_html('#138a50')

SAFE_BOORU = 'http://safebooru.org/index.php?page=dapi&s=post&q=index&tags='
NSFW_BOORU = 'http://gelbooru.com/index.php?page=dapi&s=post&q=index&tags='

SAFE_BOORU_PROVIDER = 'safebooru'
NSFW_BOORU_PROVIDER = 'gelbooru'

TOUHOU_REQUIRED = frozenset((
    'solo',
))

TOUHOU_BANNED = frozenset((
    'underwear',
    'sideboob',
    'pov_feet',
    'underboob',
    'upskirt',
    'sexually_suggestive',
    'ass',
    'bikini',
    '6%2Bgirls',
    'comic',
    'greyscale',
    'bdsm',
    'huge_filesize',
    'lovestruck',
))

SAFE_BANNED = frozenset((
    'bdsm',
    'huge_filesize',
    'underwear',
    'sideboob',
    'pov_feet',
    'underboob',
    'upskirt',
    'sexually_suggestive',
    'ass',
    'bikini',
    'clothed_female_nude_male',
    'no_panties',
))

NSFW_BANNED = frozenset((
    'loli',
    'lolicon',
    'shota',
    'shotacon',
    'huge_filesize',
))

def make_url(base, requested_tags, required_tags, banned_tags):
    url_parts = [base]
    is_tag_first = True
    
    for tag in requested_tags:
        if tag not in banned_tags:
            if is_tag_first:
                is_tag_first = False
            else:
                url_parts.append('+')
            url_parts.append(tag)
    
    if (required_tags is not None):
        for tag in required_tags:
            if (tag not in requested_tags):
                if is_tag_first:
                    is_tag_first = False
                else:
                    url_parts.append('+')
                url_parts.append(tag)
    
    for tag in banned_tags:
        if is_tag_first:
            is_tag_first = False
        else:
            url_parts.append('+')
        url_parts.append('-')
        url_parts.append(tag)
    
    return ''.join(url_parts)

def parse_xml(xml):
    soup = BeautifulSoup(xml, 'lxml')
    
    image_url_tag_pairs = []
    
    for post in soup.find_all('post'):
        try:
            file_url = post['file_url']
        except KeyError:
            continue
        
        try:
            tags = post['tags']
        except KeyError:
            continue
        
        image_url_tag_pairs.append((file_url, tags))
    
    return image_url_tag_pairs


def make_bad_status_embed(response, provider):
    return Embed(
        'Yeet',
        f'{provider} is unavailable\n{response.status: {response.reason}}',
        color = BOORU_COLOR
    )

DEFAULT_TITLE = 'Link'

EMOJI_CYCLE = BUILTIN_EMOJIS['arrows_counterclockwise']
EMOJI_BACK = BUILTIN_EMOJIS['leftwards_arrow_with_hook']
EMOJI_TAGS = BUILTIN_EMOJIS['notepad_spiral']

def add_footer(embed, provider):
    return embed.add_footer(f'Images provided by {provider}')


def make_embed(title, image_url, provider):
    return add_footer(
        Embed(title, color=BOORU_COLOR, url=image_url).add_image(image_url),
        provider,
    )

class BooruCycler(Menu):
    BUTTON_CYCLE = Button(emoji=EMOJI_CYCLE)
    BUTTON_BACK = Button(emoji=EMOJI_BACK, enabled=False)
    BUTTON_TAGS = Button(emoji=EMOJI_TAGS)
    
    BUTTONS = Row(BUTTON_CYCLE, BUTTON_BACK)
    BUTTONS_DISPLAY_TAGS = Row(BUTTON_CYCLE, BUTTON_BACK, BUTTON_TAGS)
    
    __slots__ = ('history', 'history_step', 'pop', 'title', 'image_url_tag_pairs', 'provider', 'display_tags')
    
    def __init__(self, client, event, image_url_tag_pairs, pop, title, provider, display_tags):
        self.image_url_tag_pairs = image_url_tag_pairs
        self.pop = pop
        self.title = title
        history = deque(maxlen=100)
        self.history = history
        self.history_step = 1
        self.provider = provider
        self.display_tags = display_tags
        return
    
    async def initial_invoke(self):
        image_url_tag_pairs = self.image_url_tag_pairs
        if len(image_url_tag_pairs) == 1:
            image_url_tag_pair = image_url_tag_pairs[0]
            self.BUTTON_CYCLE.enabled = False
            self.cancel()
        else:
            if self.pop:
                image_url_tag_pair = pop_one(image_url_tag_pairs)
            else:
                image_url_tag_pair = choose(image_url_tag_pairs)
            self.history.append(image_url_tag_pair)
        
        if self.display_tags:
            components = self.BUTTONS_DISPLAY_TAGS
        else:
            components = self.BUTTONS
        self.components = components
        
        image_url = image_url_tag_pair[0]
        self.embed = make_embed(self.title, image_url, self.provider)
    

    def get_timeout(self):
        return 300.0
    
    async def invoke(self, event):
        interaction = event.interaction
        history = self.history
        history_length = len(history)
        
        if interaction == self.BUTTON_TAGS:
            if history_length == 1:
                history_step = 1
            
            else:
                history_step = self.history_step
                if history_step == 0:
                    history_step = history_length
            
            image_url_tag_pair = history[history_length - history_step]
            
            client = self.client
            await client.interaction_response_message_create(
                event,
                embed = Embed(
                    'Tags',
                    ' | '.join(image_url_tag_pair[1].replace('_', '\_').split()),
                    url = image_url_tag_pair[0],
                ).add_thumbnail(
                    image_url_tag_pair[0],
                ),
                show_for_invoking_user_only = True,
            )
            return False
        
        if event.user is not self.message.interaction.user:
            return False
        
        if interaction == self.BUTTON_CYCLE:
            image_url_tag_pairs = self.image_url_tag_pairs
            if self.pop or (not history_length):
                image_url_tag_pair = pop_one(image_url_tag_pairs)
            else:
                history_step = self.history_step
                if history_step == history_length:
                    history_step = 1
                
                image_url_tag_pair = choose_not_same(image_url_tag_pairs, history[history_length - history_step])
            
            self.history.append(image_url_tag_pair)
            self.history_step = 1
            self.BUTTON_BACK.enabled = True
            
            if not image_url_tag_pairs:
                image_url_tag_pairs.extend(self.history)
        
        elif interaction == self.BUTTON_BACK:
            if history_length == 1:
                return False
            
            history_step = self.history_step
            if history_step == history_length:
                history_step = 0
            
            history_step += 1
            self.history_step = history_step
            image_url_tag_pair = history[history_length - history_step]
        
        else:
            return False
        
        image_url = image_url_tag_pair[0]
        self.embed = make_embed(self.title, image_url, self.provider)
        return True


async def answer_booru(client, event, content, url_base, banned, provider, display_tags):
    yield
    
    tags = set(content.split())
    url = make_url(url_base, tags, None, banned)
    
    async with client.http.get(url) as response:
        if response.status != 200:
            yield make_bad_status_embed(response, provider)
            return
        
        result = await response.read()
    
    image_url_tag_pairs = parse_xml(result)
    
    if not image_url_tag_pairs:
        yield add_footer(
            Embed(
                'Error desu.',
                f'Could not find anything what matches these tags..',
                color = BOORU_COLOR,
            ),
            provider,
        )
        return
    
    await BooruCycler(client, event, image_url_tag_pairs, True, DEFAULT_TITLE, provider, display_tags)
    return


class CachedBooruCommand:
    __slots__ = ('tag', 'title', 'urls',)
    def __init__(self, title, tag):
        self.tag = tag
        self.title = title
        self.urls = None
    
    async def __call__(self, client, event):
        yield
        
        urls = self.urls
        if urls is None:
            url = make_url(SAFE_BOORU, {self.tag}, TOUHOU_REQUIRED, TOUHOU_BANNED)
            async with client.http.get(url) as response:
                if response.status != 200:
                    yield make_bad_status_embed(response, SAFE_BOORU_PROVIDER)
                    return
                
                result = await response.read()
                image_url_tag_pairs = parse_xml(result)
        
        if not image_url_tag_pairs:
            yield add_footer(
                Embed(
                    'No result',
                    'Please try again later.',
                    color = BOORU_COLOR,
                ),
                SAFE_BOORU_PROVIDER,
            )
            return
        
        await BooruCycler(client, event, image_url_tag_pairs, False, self.title, SAFE_BOORU_PROVIDER, False)
        return
    

SLASH_CLIENT: Client

@SLASH_CLIENT.interactions(is_global=True)
async def safe_booru(client, event,
    tags: ('str', 'Some tags to spice it up?') = '',
):
    """Some safe images?"""
    if not event.guild_id:
        abort(f'Guild only command.')
    
    return answer_booru(client, event, tags, SAFE_BOORU, SAFE_BANNED, SAFE_BOORU_PROVIDER, True)


@SLASH_CLIENT.interactions(is_global=True)
async def nsfw_booru(client, event,
    tags: ('str', 'Some tags to spice it up?') = '',
):
    """Some not so safe images? You perv!"""
    if not event.guild_id:
        abort(f'Guild only command.')
    
    channel = event.channel
    if (channel is None) or (not channel.nsfw):
        if 'koishi' in tags.lower():
            description = 'I love you too\~,\nbut this is not the right place to lewd.'
        else:
            description = 'Onii chaan\~,\nthis is not the right place to lewd.'
        
        abort(description)
    
    return answer_booru(client, event, tags, NSFW_BOORU, NSFW_BANNED, NSFW_BOORU_PROVIDER, True)


def generate_touhou_relations():
    touhou_name_relations = {}
    touhou_names = []
    touhou_alternative_names = {}
    
    for name, tag_name, *alternative_names in (
        ('Aki Minoriko'         , 'aki_minoriko'         , '秋 穣子', 'Minoriko',),
        ('Aki Shizuha'          , 'aki_shizuha'          , '秋 静葉', 'Shizuha',),
        ('Luna Child'           , 'luna_child'           , 'ルナチャイルド', 'Chairudo Runa', 'Luna', 'Runa',),
        ('Chen'                 , 'chen'                 , '橙',),
        ('Chiruno'              , 'cirno'                , 'チルノ', 'Cirno',),
        ('Daiyousei'            , 'daiyousei'            , '大妖精'),
        ('Ebisu Eika'           , 'ebisu_eika'           , '戎 瓔花', 'Eika Ebisu'),
        ('Elly'                 , 'elly'                 , 'エリー', 'Erii', 'Elly',),
        ('Eternity Larva'       , 'eternity_larva'       , 'エタニティラルバ', 'Eternity', 'Etanitiraruba',),
        ('Fujiwara no Mokou'    , 'fujiwara_no_mokou'    , '藤原 妹紅', 'Mokou',),
        ('Futatsuiwa Mamizou'   , 'futatsuiwa_mamizou'   , '二ッ岩 マミゾウ', 'Mamizou', 'Mamizou Futatsuiwa'),
        ('Hearn Maribel'        , 'maribel_hearn'        , 'マエリベリー ハーン', 'Maribel', 'Maeriberii', 'Haan Maeriberii', 'Maribel Hearn'),
        ('Haniyasushin Keiki'   , 'haniyasushin_keiki'   , '埴安神 袿姫', 'Keiki', 'Keiki Haniyasushin',),
        ('Hakurei Reimu'        , 'hakurei_reimu'        , '博麗 霊夢', 'Reimu', 'Reimu Hakurei'),
        ('Hata no Kokoro'       , 'hata_no_kokoro'       , '秦 こころ', 'Kokoro', 'こころ', 'Hata'),
        ('Hei Meiling'          , 'hei_meiling'          , 'Hei Meirin', 'Meiling Hei'),
        ('Hieda no Akyuu'       , 'hieda_no_akyuu'       , '稗田 阿求', 'Akyuu',),
        ('Hijiri Byakuren'      , 'hijiri_byakuren'      , '聖 白蓮', 'Byakuren', 'Hijiri Byakuren'),
        ('Himekaidou Hatate'    , 'himekaidou_hatate'    , '姫海棠 はたて', 'Hatate', 'Hatate Himekaidou'),
        ('Hinanawi Tenshi'      , 'hinanawi_tenshi'      , '比那名居 天子', 'Tenshi', 'Tenshi Hinanawi',),
        ('Hong Meiling'         , 'hong_meiling'         , '紅 美鈴', 'Meiling', 'Meirin', 'Hon Meirin', 'Meiling Hong'),
        ('Horikawa Raiko'       , 'horikawa_raiko'       , '堀川 雷鼓', 'Raiko', 'Raiko Horikawa'),
        ('Hoshiguma Yuugi'      , 'hoshiguma_yuugi'      , '星熊 勇儀', 'Yuugi', 'Yuugi Hoshiguma'),
        ('Houjuu Nue'           , 'houjuu_nue'           , '封獣 ぬえ', 'Nue', 'Nue Houjuu'),
        ('Houraisan Kaguya'     , 'houraisan_kaguya'     , '蓬莱山 輝夜', 'Kaguya', 'Kaguya Houraisan'),
        ('Lily White'           , 'lily_white'           , 'リリーホワイト', 'Lily', 'Ririi', 'Ririi Howaito'),
        ('Letty Whiterock'      , 'letty_whiterock'      , 'レティ ホワイトロック', 'Reti Howaitorokku',),
        ('Ibaraki Kasen'        , 'ibaraki_kasen'        , '茨木 華扇', 'Kasen', 'Kasen Ibaraki'),
        ('Ibuki Suika'          , 'ibuki_suika'          , '伊吹 萃香', 'Suika', 'Suika Ibuk'),
        ('Imaizumi Kagerou'     , 'imaizumi_kagerou'     , '今泉 影狼', 'Kagerou', 'Kagerou Imaizumi'),
        ('Inaba Tewi'           , 'inaba_tewi'           , '因幡 てゐ', 'Tewi', 'Tewi Inaba'),
        ('Inubashiri Momiji'    , 'inubashiri_momiji'    , '犬走 椛', 'Momiji', 'Momiji Inubashiri'),
        ('Izayoi Sakuya'        , 'izayoi_sakuya'        , '十六夜 咲夜', 'Sakuya', 'Sakuya Izayoi'),
        ('Joutouguu Mayumi'     , 'joutouguu_mayumi'     , '杖刀偶 磨弓', 'Mayumi', 'Mayumi Joutouguu'), # same as 'joutougu_mayumi'
        ('Junko'                , 'junko_(touhou)'       , '純狐', 'Junko',),
        ('Kaenbyou Rin'         , 'kaenbyou_rin'         , '火焔猫 燐', 'Orin', 'Rin', 'Rin Kaenbyou'),
        ('Kagiyama Hina'        , 'kagiyama_hina'        , '鍵山 雛', 'Hina', 'Hina Kagiyama'),
        ('Kaku Seiga'           , 'kaku_seiga'           , '霍 青娥,', 'Seiga', 'Seiga Kaku'),
        ('Kamishirasawa Keine'  , 'kamishirasawa_keine'  , '上白沢 慧音', 'Keine', 'Keine Kamishirasawa'),
        ('Kasodani Kyouko'      , 'kasodani_kyouko'      , '幽谷 響子', 'Kyouko', 'Kyouko Kasodani'),
        ('Kawashiro Nitori'     , 'kawashiro_nitori'     , '河城 にとり', 'Nitori', 'Nitori Kawashiro', 'Phoenix Kappashiro'),
        ('Kazami Yuuka'         , 'kazami_yuuka'         , '風見 幽香', 'Yuuka', 'Yuuka Kazami'), # same as 'kazami_youka'
        ('Kicchou Yachie'       , 'kitcho_yachie'        , '吉弔 八千慧', 'Yachie', 'Yachie Kicchou'), # same as 'kicchou_yachie'
        ('Kijin Seija'          , 'kijin_seija'          , '鬼人 正邪', 'Seija Kijin', 'Seija',),
        ('Kirisame Marisa'      , 'kirisame_marisa'      , '霧雨 魔理沙', 'Marisa', 'Marisa Kirisame'),
        ('Kishin Sagume'        , 'kishin_sagume'        , '稀神 サグメ', 'Sagume Kishin',),
        ('Kisume'               , 'kisume'               , 'キスメ',),
        ('Kitashirakawa Chiyuri', 'kitashirakawa_chiyuri', '北白河 ちゆり', 'Chiyuri Kitashirakawa'),
        ('Koakuma'              , 'koakuma'              , '小悪魔', 'Koakuma',),
        ('Kochiya Sanae'        , 'kochiya_sanae'        , '東風谷 早苗', 'Sanae', 'Sanae Kochiya'),
        ('Komano Aunn'          , 'komano_aun'           , '高麗野 あうん', 'Aunn', 'Aun', 'Aunn Komano'),
        ('Komeiji Koishi'       , 'komeiji_koishi'       , '古明地 こいし', 'Koishi', 'Koishi Komeiji'),
        ('Komeiji Satori'       , 'komeiji_satori'       , '古明地 さとり', 'Satori', 'Satori Komeiji'),
        ('Konngara'             , 'konngara'             , '矜羯羅', 'Konngara',),
        ('Konpaku Youmu'        , 'konpaku_youmu'        , '魂魄 妖夢', 'Youmu', 'Youmu Konpaku'),
        ('Kokuu Haruto'         , 'kokuu_haruto'         , 'Haruto Kokuu',), # no result now
        ('Kumoi Ichirin'        , 'kumoi_ichirin'        , '雲居 一輪', 'Ichirin Kumoi', 'Ichirin',),
        ('Clownpiece'           , 'clownpiece'           , 'クラウンピース', 'Kuraunpiisu', ),
        ('Kurodani Yamame'      , 'kurodani_yamame'      , '黒谷 ヤマメ', 'Yamame Kurodani',),
        ('Kurokoma Saki'        , 'kurokoma_saki'        , '驪駒 早鬼', 'Saki', 'Saki Kurokoma'),
        ('Margatroid Alice'     , 'alice_margatroid'     , 'アリス マーガトロイド', 'Arisu', 'Alice', 'Maagatoroido Arisu', 'Alice Margatroid'),
        ('Matara Okina'         , 'matara_okina'         , '摩多羅 隠岐奈', 'Okina', 'Okina Matara'),
        ('Medicine Melancholy'  , 'medicine_melancholy'  , 'メディスン メランコリー', 'Merankorii Medisun'),
        ('Mima'                 , 'mima'                 , '魅魔', 'Mima',),
        ('Sunny Milk'           , 'sunny_milk'           , 'サニーミルク', 'Sanii Miruku',),
        ('Miyako Yoshika'       , 'miyako_yoshika'       , '宮古 芳香', 'Yoshika', 'Yoshika Miyako',),
        ('Mizuhashi Parsee'     , 'mizuhashi_parsee'     , '水橋 パルスィ', 'Mizuhashi Parusi', 'Parsee Mizuhashi'),
        ('Mononobe no Futo'     , 'mononobe_no_futo'     , '物部 布都', 'Futo',),
        ('Morichika Rinnosuke'  , 'morichika_rinnosuke'  , '森近 霖之助', 'Rinnosuke', 'Rinnosuke Morichika'),
        ('Moriya Suwako'        , 'moriya_suwako'        , '洩矢 諏訪子', 'Suwako Moriya', 'Suwako',),
        ('Motoori Kosuzu'       , 'motoori_kosuzu'       , '本居 小鈴', 'Kosuzu', 'Kosuzu Motoori'),
        ('Murasa Minamitsu'     , 'murasa_minamitsu'     , '村紗 水蜜', 'Minamitsu Murasa'),
        ('Nagae Iku'            , 'nagae_iku'            , '永江 衣玖', 'Iku Nagae'),
        ('Nazrin'               , 'nazrin'               , 'ナズーリン', 'Nazuurin',),
        ('Nishida Satono'       , 'nishida_satono'       , '爾子田 里乃', 'Satono Nishida',),
        ('Niwatari Kutaka'      , 'niwatari_kutaka'      , '庭渡 久侘歌', 'Kutaka Niwatar',),
        ('Okunoda Miyoi'        , 'okunoda_miyoi'        , '奥野田 美宵', 'Miyoi Okunoda',),
        ('Onozuka Komachi'      , 'onozuka_komachi'      , '小野塚 小町', 'Komachi Onozuka',),
        ('Patchouli Knowledge'  , 'patchouli_knowledge'  , 'パチュリー ノーレッジ', 'Patchouli', 'Pachurii Noorejji'),
        ('Merlin Prismriver'    , 'merlin_prismriver'    , 'メルラン プリズムリバ', 'Merlin', 'Merlin Prismriver', 'Meruran Purizumuribaa'),
        ('Lyrica Prismriver'    , 'lyrica_prismriver'    , 'リリカ プリズムリバー', 'Lyrica', 'Ririka Purizumuribaa',),
        ('Lunasa Prismriver'    , 'lunasa_prismriver'    , 'ルナサ プリズムリバー', 'Lunasa', 'Runasa Purizumuribaa',),
        ('Hecatia Lapislazuli'  , 'hecatia_lapislazuli'  , 'ヘカーティア ラピスラズリ', 'Hecatia', 'Hekaatia', 'Hekaatia Rapisurazuri'),
        ('Reisen Udongein Inaba', 'reisen_udongein_inaba', '鈴仙 優曇華院 イナバ', 'Reisen',),
        ('Reiuji Utsuho'        , 'reiuji_utsuho'        , '霊烏路 空', 'Okuu', 'Utsuho Reiuji '),
        ('Wriggle Nightbug'     , 'wriggle_nightbug'     , 'リグル ナイトバグ', 'Wriggle', 'Riguru Naitobagu'),
        ('Ringo'                , 'ringo_(touhou)'       , '鈴瑚', 'Ringo',),
        ('Mystia Lorelei'       , 'mystia_lorelei'       , 'ミスティア ローレライ', 'Misutia Roorerai',),
        ('Rumia'                , 'rumia'                , 'ルーミア', 'Ruumia',),
        ('Star Sapphire'        , 'star_sapphire'        , 'スターサファイア', 'Safaia Sutaa',),
        ('Saigyouji Yuyuko'     , 'saigyouji_yuyuko'     , '西行寺 幽々子', 'Yuyuko', 'Yuyuko Saigyouji'),
        ('Sakata Nemuno'        , 'sakata_nemuno'        , '坂田 ネムノ', 'Nemuno', 'Nemuno Sakata'),
        ('Seiran'               , 'seiran_(touhou)'      , '清蘭', 'Seiran',),
        ('Sekibanki'            , 'sekibanki'            , '赤蛮奇', 'Sekibanki',),
        ('Shameimaru Aya'       , 'shameimaru_aya'       , '射命丸 文', 'Aya', 'Aya Shameimaru'),
        ('Shiki Eiki Yamaxanadu', 'shiki_eiki'           , '四季映姫 ヤマザナドゥ', 'Eiki', 'Shiki Eiki Yamazanadu', 'Eiki Shiki, Yamaxanadu',),
        ('Doremy Sweet'         , 'doremy_sweet'         , 'ドレミー スイート', 'Doremy', 'Doremii Suiito'),
        ('Scarlet Flandre'      , 'flandre_scarlet'      , 'スカーレット フランドール', 'Flandre', 'Flandre Scarlet', 'Flan', 'Sukaaretto Furandooru'),
        ('Scarlet Remilia'      , 'remilia_scarlet'      , 'スカーレット レミリア', 'Remilia', 'Remilia Scarlet', 'Sukaaretto Remiria'),
        ('Sukuna Shinmyoumaru'  , 'sukuna_shinmyoumaru'  , '少名 針妙丸', 'Shinmyoumaru Sukuna',),
        ('Tatara Kogasa'        , 'tatara_kogasa'        , '多々良 小傘', 'Kogasa Tatara'),
        ('Teireida Mai'         , 'teireida_mai'         , '丁礼田 舞', 'Mai Teireida', 'Mai'),
        ('Toramaru Shou'        , 'toramaru_shou'        , '寅丸 星', 'Shou Toramaru',),
        ('Toyosatomimi no Miko' , 'toyosatomimi_no_miko' , '豊聡耳 神子', 'Miko',),
        ('Usami Renko'          , 'usami_renko'          , '宇佐見 蓮子', 'Renko', 'Renko Usami'),
        ('Usami Sumireko'       , 'usami_sumireko'       , '宇佐見 菫子', 'Sumireko', 'Sumireko Usami'),
        ('Ushizaki Urumi'       , 'ushizaki_urumi'       , '牛崎 潤美', 'Urumi Ushizaki',),
        ('Wakasagihime'         , 'wakasagihime'         , 'わかさぎ姫', ),
        ('Watatsuki no Toyohime', 'watatsuki_no_toyohime', '綿月 豊姫', 'Toyohime',),
        ('Watatsuki no Yorihime', 'watatsuki_no_yorihime', '綿月 依姫', 'Yorihime',),
        ('Yagokoro Eirin'       , 'yagokoro_eirin'       , '八意 永琳', 'Eirin', 'Eirin Yagokoro'),
        ('Yakumo Ran'           , 'yakumo_ran'           , '八雲 藍', 'Ran', 'Ran Yakumo'),
        ('Yakumo Yukari'        , 'yakumo_yukari'        , '八雲 紫', 'Yukari', 'Yukari Yakumo'),
        ('Yasaka Kanako'        , 'yasaka_kanako'        , '八坂 神奈子', 'Kanako', 'Kanako Yasaka'),
        ('Yatadera Narumi'      , 'yatadera_narumi'      , '矢田寺 成美', 'Narumi', 'Narumi Yatadera'),
        ('Yorigami Joon'        , 'yorigami_jo\'on'      , '依神 女苑', 'Joon', 'Joon Yorigami',),
        ('Yorigami Shion'       , 'yorigami_shion'       , '依神 紫苑', 'Shion', 'Shion Yorigami'),
    ):
        touhou_names.append(name)
        cache = CachedBooruCommand(name, tag_name)
        touhou_name_relations[name] = cache
        touhou_names.extend(alternative_names)
        for alternative_name in alternative_names:
            touhou_name_relations[alternative_name] = cache
            touhou_alternative_names[alternative_name] = name
    
    return touhou_name_relations, touhou_names, touhou_alternative_names


TOUHOU_NAME_RELATIONS, TOUHOU_NAMES, TOUHOU_ALTERNATIVE_NAMES = generate_touhou_relations()


MOST_POPULAR_TOUHOU_CHARACTERS = [
    'Konpaku Youmu',
    'Kirisame Marisa',
    'Hakurei Reimu',
    'Komeiji Koishi',
    'Scarlet Flandre',
    'Izayoi Sakuya',
    'Scarlet Remilia',
    'Fujiwara no Mokou',
    'Komeiji Satori',
    'Saigyouji Yuyuko',
    'Shameimaru Aya',
    'Margatroid Alice',
    'Kochiya Sanae',
    'Reisen Udongein Inaba',
    'Hinanawi Tenshi',
    'Yakumo Yukari',
    'Hata no Kokoro',
    'Chiruno',
    'Patchouli Knowledge',
    'Tatara Kogasa',
]


@SLASH_CLIENT.interactions(is_global=True)
async def touhou_character(client, event,
    name: ('str', 'Who\'s?'),
):
    """Shows you the given Touhou character's portrait."""
    name_length = len(name)
    if name_length == 0:
        abort('Empty name was given.')
    
    if name_length > 10:
        name_length = 10
    
    diversity = 0.2 + (10 - name_length) * 0.02
    
    matcheds = get_close_matches(name, TOUHOU_NAMES, n=1, cutoff=1.0 - diversity)
    if matcheds:
        return TOUHOU_NAME_RELATIONS[matcheds[0]](client, event)
    
    embed = Embed('No match', color=BOORU_COLOR)
    matcheds = get_close_matches(name, TOUHOU_NAMES, n=10, cutoff=0.8 - diversity)
    if matcheds:
        field_value_parts = []
        for index, matched in enumerate(matcheds, 1):
            field_value_parts.append(str(index))
            field_value_parts.append('.: **')
            field_value_parts.append(matched)
            field_value_parts.append('**')
            name = TOUHOU_NAME_RELATIONS[matched].title
            if matched != name:
                field_value_parts.append(' [')
                field_value_parts.append(name)
                field_value_parts.append(']')
            
            field_value_parts.append('\n')
        
        del field_value_parts[-1]
        
        embed.add_field('Close matches:', ''.join(field_value_parts))
    
    return embed


@touhou_character.autocomplete('name')
async def autocomplete_touhou_character_name(value):
    if value is None:
        return MOST_POPULAR_TOUHOU_CHARACTERS
    
    matcher = re_compile(re_escape(value), re_ignore_case | re_unicode)
    
    matched_names = []
    
    for name in TOUHOU_NAMES:
        if (matcher.match(name) is not None):
            matched_names.append(name)
    
    value_length = len(value)
    if value_length >= 3:
        if len(value) > 10:
            value_length = 10
        
        diversity = 0.2 + (10 - value_length) * 0.02
        
        matched_names.extend(get_close_matches(value, TOUHOU_NAMES, n=20, cutoff=1.0 - diversity))
    
    unique = []
    system_names = set()
    
    for name in matched_names:
        system_name = TOUHOU_NAME_RELATIONS[name]
        if system_name in system_names:
            continue
        
        system_names.add(system_name)
        unique.append(name)
        continue
    
    del unique[20:]
    
    return [TOUHOU_ALTERNATIVE_NAMES.get(name, name) for name in unique]
