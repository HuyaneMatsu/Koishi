# -*- coding: utf-8 -*-
from collections import deque
from difflib import get_close_matches

from hata import Embed, ERROR_CODES, Color, BUILTIN_EMOJIS, Task, DiscordException, KOKORO, Client
from hata.ext.commands import Timeouter, GUI_STATE_READY, GUI_STATE_SWITCHING_PAGE, \
    GUI_STATE_CANCELLING, GUI_STATE_CANCELLED, GUI_STATE_SWITCHING_CTX

from bot_utils.tools import BeautifulSoup, choose, pop_one, choose_notsame


BOORU_COLOR = Color.from_html('#138a50')

SAFE_BOORU = 'http://safebooru.org/index.php?page=dapi&s=post&q=index&tags='
NSFW_BOORU = 'http://gelbooru.com/index.php?page=dapi&s=post&q=index&tags='

DEFAULT_TITLE = 'Link'

Koishi: Client

class CachedBooruCommand(object):
    _FILTER = (
        'solo+-underwear+-sideboob+-pov_feet+-underboob+-upskirt+-sexually_suggestive+-ass+-bikini+-6%2Bgirls+-comic'
        '+-greyscale+'
            )
    
    __slots__ = ('tag_name', 'title', 'urls',)
    def __init__(self, title, tag_name):
        self.tag_name = tag_name
        self.title = title
        self.urls = None
    
    async def __call__(self, client, event):
        yield
        
        urls = self.urls
        if urls is None:
            urls = await self._request_urls(client)
            if urls is None:
                yield Embed('Error desu', 'Booru is unavailable', color=BOORU_COLOR)
                return
        
        guild = event.guild
        if (guild is None) or (client not in guild.clients):
            image_url = choose(urls)
            yield Embed(self.title, color=BOORU_COLOR, url=image_url).add_image(image_url)
            return
        
        await ShuffledShelter(client, event.channel, urls, False, self.title)
        return
    
    async def _request_urls(self, client):
        url = ''.join([SAFE_BOORU, self._FILTER, self.tag_name])
        
        async with client.http.get(url) as response:
            result = await response.read()
        
        if response.status != 200:
            return
        
        soup = BeautifulSoup(result, 'lxml')
        urls = [post['file_url'] for post in soup.find_all('post')]
        self.urls = urls
        return urls


class ShuffledShelter(object):
    CYCLE  = BUILTIN_EMOJIS['arrows_counterclockwise']
    BACK   = BUILTIN_EMOJIS['leftwards_arrow_with_hook']
    EMOJIS = (CYCLE, BACK)
    
    __slots__ = ('canceller', 'channel', 'client', 'history', 'history_step', 'message', 'pop', 'task_flag',
        'timeouter', 'title', 'urls')
    
    async def __new__(cls, client, channel, urls, pop, title=DEFAULT_TITLE):
        if not urls:
            await client.message_create(channel, embed=Embed('No result'))
            return
        
        self = object.__new__(cls)
        self.client = client
        self.channel = channel
        self.canceller = self.__class__._canceller
        self.task_flag = GUI_STATE_READY
        self.urls = urls
        self.pop = pop
        self.title = title
        self.timeouter = None
        history = deque(maxlen=100)
        self.history = history
        self.history_step = 1
        
        
        image_url = pop_one(urls) if pop else choose(urls)
        history.append(image_url)
        
        embed = Embed(title, color=BOORU_COLOR, url=image_url).add_image(image_url)
        
        message = await client.message_create(channel, embed=embed)
        self.message = message
        
        if (len(urls) == (0 if pop else 1)) or (not channel.cached_permissions_for(client).can_add_reactions):
            return
        
        for emoji in self.EMOJIS:
            await client.reaction_add(message, emoji)
        
        self.timeouter = Timeouter(self, timeout=300.)
        client.events.reaction_add.append(message, self)
        client.events.reaction_delete.append(message, self)
        
        return self
    
    async def __call__(self, client, event):
        if event.user.is_bot:
            return
        
        
        if (event.emoji not in self.EMOJIS):
            return
        
        if (event.delete_reaction_with(client) == event.DELETE_REACTION_NOT_ADDED):
            return
        
        if self.task_flag:
            return
        
        while True:
            emoji = event.emoji
            if emoji is self.CYCLE:
                image_url = pop_one(self.urls) if self.pop else choose_notsame(self.urls,
                    self.message.embeds[0].image.url)
                
                self.history.append(image_url)
                self.history_step = 1
                break
            
            if emoji is self.BACK:
                history = self.history
                history_ln = len(history)
                if history_ln < 2:
                    return
                
                history_step = self.history_step
                if history_step == history_ln:
                    history_step = 0
                
                history_step += 1
                self.history_step = history_step
                image_url = history[history_ln - history_step]
                break
            
            return
        
        embed = Embed(self.title, color=BOORU_COLOR, url=image_url).add_image(image_url)
        
        self.task_flag = GUI_STATE_SWITCHING_PAGE
        try:
            await client.message_edit(self.message, embed=embed)
        except BaseException as err:
            self.task_flag = GUI_STATE_CANCELLED
            self.cancel()
            
            if isinstance(err, ConnectionError):
                # no internet
                return
            
            if isinstance(err, DiscordException):
                if err.code in (
                        ERROR_CODES.invalid_access, # client removed
                        ERROR_CODES.unknown_message, # message already deleted
                            ):
                    return
            
            # We definitely do not want to silence `ERROR_CODES.invalid_form_body`
            await client.events.error(client, f'{self!r}.__call__', err)
            return
            
        if not self.urls:
            self.task_flag = GUI_STATE_CANCELLED
            self.cancel()
            return
        
        self.task_flag = GUI_STATE_READY
        
        self.timeouter.set_timeout(300.0)

    async def _canceller(self, exception):
        client = self.client
        message = self.message
        
        client.events.reaction_add.remove(message, self)
        client.events.reaction_delete.remove(message, self)
        
        if self.task_flag == GUI_STATE_SWITCHING_CTX:
            # the message is not our, we should not do anything with it.
            return
        
        self.task_flag = GUI_STATE_CANCELLED
        
        if exception is None:
            return
        
        if isinstance(exception, TimeoutError):
            if self.channel.cached_permissions_for(client).can_manage_messages:
                try:
                    await client.reaction_clear(message)
                except BaseException as err:
                    
                    if isinstance(err, ConnectionError):
                        # no internet
                        return
                    
                    if isinstance(err,DiscordException):
                        if err.code in (
                                ERROR_CODES.invalid_access, # client removed
                                ERROR_CODES.unknown_message, # message deleted
                                ERROR_CODES.invalid_permissions, # permissions changed meanwhile
                                    ):
                            return
                    
                    await client.events.error(client, f'{self!r}._canceller', err)
                    return
            return
        
        timeouter = self.timeouter
        if timeouter is not None:
            timeouter.cancel()
        #we do nothing
    
    def cancel(self, exception=None):
        canceller = self.canceller
        if canceller is None:
            return
        
        self.canceller = None
        
        timeouter = self.timeouter
        if timeouter is not None:
            timeouter.cancel()
        
        return Task(canceller(self, exception), KOKORO)

async def answer_booru(client, event, content, url_base):
    yield
    
    if content:
        url = '+'.join([url_base, *content.split()])
    else:
        url = url_base
    
    async with client.http.get(url) as response:
        result = await response.read()
    
    if response.status != 200:
        yield Embed('Error desu.', 'Booru is unavailable', color=BOORU_COLOR)
        return
    
    soup = BeautifulSoup(result, 'lxml')
    urls = [post['file_url'] for post in soup.find_all('post')]
    if not urls:
        yield Embed('Error desu.', f'Could not find anything what matches these tags..', color=BOORU_COLOR)
        return
    
    guild = event.guild
    if (guild is None) or (client not in guild.clients):
        image_url = choose(urls)
        yield Embed(DEFAULT_TITLE, color=BOORU_COLOR, url=image_url).add_image(image_url)
        return
    
    await ShuffledShelter(client, event.channel, urls, True)
    return
    

TOUHOU_NAME_RELATIONS = {}
TOUHOU_NAMES = []

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
        ('Hata no Kokoro'       , 'hata_no_kokoro'       , '秦 こころ', 'Kokoro',),
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
    
    TOUHOU_NAMES.append(name)
    cache = CachedBooruCommand(name, tag_name)
    TOUHOU_NAME_RELATIONS[name] = cache
    TOUHOU_NAMES.extend(alternative_names)
    for alternative_name in alternative_names:
        TOUHOU_NAME_RELATIONS[alternative_name] = cache
        

del name
del tag_name
del alternative_name
del alternative_names
del cache

@Koishi.interactions(is_global=True)
async def touhou(client, event,
        name: ('str', 'Who\'s?'),
            ):
    """Shows you the given Touhou character's portrait."""
    name_length = len(name)
    if name_length == 0:
        yield Embed('Empty content', color=BOORU_COLOR)
        return
    
    if name_length > 10:
        name_length = 10
    
    diversity = 0.2+(10-name_length)*0.02
    
    matcheds = get_close_matches(name, TOUHOU_NAMES, n=1, cutoff=1.0-diversity)
    if matcheds:
        async for response in TOUHOU_NAME_RELATIONS[matcheds[0]](client, event):
            yield response
    else:
        embed = Embed('No match', color=BOORU_COLOR)
        matcheds = get_close_matches(name, TOUHOU_NAMES, n=10, cutoff=0.8-diversity)
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
        yield embed


@Koishi.interactions(is_global=True)
async def safe_booru(client, event,
        tags: ('str', 'Some tags to spice it up?') = '',
            ):
    """Some safe images?"""
    guild = event.guild
    if (guild is None) or guild.partial:
        yield Embed('Ayaya', f'Please invite me, {client:f} first!', color=BOORU_COLOR)
        return
    
    async for response in answer_booru(client, event, tags, SAFE_BOORU):
        yield response


@Koishi.interactions(is_global=True)
async def nsfw_booru(client, event,
        tags: ('str', 'Some tags to spice it up?') = '',
            ):
    """Some not so safe images? You perv!"""
    guild = event.guild
    if (guild is None) or guild.partial:
        yield Embed('Ayaya', f'Please invite me, {client:f} first!', color=BOORU_COLOR)
        return
    
    channel = event.channel
    if not channel.nsfw:
        if 'koishi' in tags.lower():
            description = 'I love you too\~,\nbut this is not the right place to lewd.'
        else:
            description = 'Onii chaan\~,\nthis is not the right place to lewd.'
        
        yield Embed('Ayaya', description, color=BOORU_COLOR)
        return
    
    async for response in  answer_booru(client, event, tags, SAFE_BOORU):
        yield response


