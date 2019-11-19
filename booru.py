# -*- coding: utf-8 -*-
import re

from hata.embed import Embed
from hata.parsers import eventlist
from hata.color import Color
from hata.emoji import BUILTIN_EMOJIS
from hata.events import waitfor_wrapper, Cooldown, multievent
from hata.futures import Task
from hata.exceptions import DiscordException

from tools import BeautifulSoup, choose, pop_one, CooldownHandler, mark_as_async, choose_notsame
from help_handler import KOISHI_HELP_COLOR, KOISHI_HELPER

BOORU_COLOR=Color.from_html('#138a50')

SAFE_BOORU='http://safebooru.org/index.php?page=dapi&s=post&q=index&tags='
NSFW_BOORU='http://gelbooru.com/index.php?page=dapi&s=post&q=index&tags='

class cached_booru_command(object):
    _FILTER='solo+-underwear+-sideboob+-pov_feet+-underboob+-upskirt+-sexually_suggestive+-ass+-bikini+-6%2Bgirls+-comic+-greyscale+'
    __slots__=('_tag_name', 'title', 'urls',)
    def __init__(self,title,tag_name):
        self._tag_name=tag_name
        self.title=title
        self.urls=None
        
    async def __call__(self,client,message,content):
        urls=self.urls
        if urls is None:
            await self._request_urls(client)
            urls=self.urls
            if urls is None:
                await client.message_create(message.channel,embed=Embed('Booru is unavailable',color=BOORU_COLOR))
                return

        await ShuffledShelter(client,message.channel,urls,False,self.title)

    async def _request_urls(self,client):
        url=''.join([SAFE_BOORU,self._FILTER,self._tag_name])
        async with client.http.request_get(url) as response:
            result = await response.read()
        if response.status!=200:
            return
        soup=BeautifulSoup(result,'lxml')
        self.urls=[post['file_url'] for post in soup.find_all('post')]

booru_commands=eventlist()


class ShuffledShelter(object):
    RESET = BUILTIN_EMOJIS['arrows_counterclockwise']
    
    __slots__=('cancel', 'channel','task_flag', 'urls', 'pop', 'title',)
    async def __new__(cls,client,channel,urls,pop,title='Link'):
        self=object.__new__(cls)
        self.channel=channel
        self.cancel=self._cancel
        self.task_flag=0
        self.urls=urls
        self.pop=pop
        self.title=title
        
        url=pop_one(urls) if pop else choose(urls)
        embed=Embed(title,color=BOORU_COLOR,url=url)
        embed.add_image(url)
        
        message = await client.message_create(channel,embed=embed)

        if (len(urls)==(0 if pop else 1)) or (not channel.cached_permissions_for(client).can_add_reactions):
            return
        
        message.weakrefer()
        await client.reaction_add(message,self.RESET)

        waitfor_wrapper(client,self,300.,multievent(client.events.reaction_add,client.events.reaction_delete),message,)
        
        return self
    
    async def __call__(self,wrapper,emoji,user):
        if user.is_bot or emoji is not self.RESET:
            return
        
        client=wrapper.client
        message=wrapper.target
        can_manage_messages=self.channel.cached_permissions_for(client).can_manage_messages

        if can_manage_messages:
            if not message.did_react(emoji,user):
                return
            Task(self.reaction_remove(client,message,emoji,user),client.loop)

        if self.task_flag:
            return

        url=pop_one(self.urls) if self.pop else choose_notsame(self.urls,message.embeds[0].image.url)
        embed=Embed(self.title,color=BOORU_COLOR,url=url)
        embed.add_image(url)
        
        self.task_flag=1
        try:
            await client.message_edit(message,embed=embed)
        except DiscordException:
            self.task_flag=3
            return wrapper.cancel()

        if not self.urls:
            self.task_flag=3
            return wrapper.cancel()
        
        self.task_flag=0

        if wrapper.timeout<300.:
            wrapper.timeout+=20.
            
    @staticmethod
    async def reaction_remove(client,message,emoji,user):
        try:
            await client.reaction_delete(message,emoji,user)
        except DiscordException:
            pass

    @staticmethod
    async def _cancel(self,wrapper,exception):
        self.task_flag=3
        if exception is None:
            return
        if isinstance(exception,TimeoutError):
            client=wrapper.client
            if self.channel.cached_permissions_for(client).can_manage_messages:
                try:
                    await client.reaction_clear(wrapper.target)
                except DiscordException:
                    pass
            return
        #we do nothing

async def answer_booru(client,channel,content,url_base):
    if content:
        content=content.split()
        content.insert(0,url_base)
        url='+'.join(content)
    else:
        url=url_base
    
    async with client.http.request_get(url) as response:
        result = await response.read()
    if response.status!=200:
        await client.message_create(channel,
            embed=Embed('Booru is unavailable',color=BOORU_COLOR))
        return
    
    soup=BeautifulSoup(result,'lxml')
    urls=[post['file_url'] for post in soup.find_all('post')]
    if urls:
        await ShuffledShelter(client,channel,urls,True)
        return
    
    await client.message_create(channel,embed=Embed(
        f'Sowwy, but {client.name} could not find anything what matches these tags..',
        color=BOORU_COLOR))

@booru_commands
@Cooldown('channel',20.,limit=2,handler=CooldownHandler())
@mark_as_async
def safebooru(client,message,content):
    return answer_booru(client,message.channel,content,SAFE_BOORU)

async def _help_safebooru(client,message):
    prefix=client.events.message_create.prefix(message)
    embed=Embed('safebooru',(
        'Do you want me, to request some images from safebooru?\n'
        f'Usage: `{prefix}safebooru *tags*`\n'
        'You should pass at least 1 tag.'
        ),color=KOISHI_HELP_COLOR)
    await client.message_create(message.channel,embed=embed)

KOISHI_HELPER.add('safebooru',_help_safebooru)

class nsfw_checker():
    __slots__=('command',)
    __async_call__=True
    
    def __init__(self,command):
        self.command=command
    
    def __call__(self,client,message,content):
        if getattr(message.channel,'nsfw',False):
            return self.command(client,message,content)
        
        if re.search(client.name,content,re.I) is None:
            text='Onii chaan\~,\nthis is not the right place to lewd.'
        else:
            text='I love you too\~,\nbut this is not the right place to lewd.'
        
        return client.message_create(message.channel,embed=Embed(
            text,color=BOORU_COLOR))

    @property
    def __name__(self):
        return self.command.__name__

@booru_commands
@nsfw_checker
@safebooru.shared()
@mark_as_async
def nsfwbooru(client,message,content):
    return answer_booru(client,message.channel,content,NSFW_BOORU)

async def _help_nsfwbooru(client,message):
    prefix=client.events.message_create.prefix(message)
    embed=Embed('nsfwbooru',(
        'Do you want me, to request some images from gelbooru?... You perv!\n'
        f'Usage: `{prefix}nsfwbooru *tags*`\n'
        'You should pass at least 1 tag. '
        'Passing nsfw tags is recommended as well.'
            ),color=KOISHI_HELP_COLOR).add_footer(
            'NSFW channel only!')
    await client.message_create(message.channel,embed=embed)

KOISHI_HELPER.add('nsfwbooru',_help_nsfwbooru)

for title,tag_name,command_names in (
        ('Aki Minoriko',            'aki_minoriko',         ('minoriko',),),
        ('Aki Shizuha',             'aki_shizuha',          ('shizuha',),),
        ('Chairudo Runa',           'luna_child',           ('runa','luna',),),
        ('Chen',                    'chen',                 ('chen',),),
        ('Chiruno',                 'cirno',                ('chiruno','cirno',),),
        ('Daiyousei',               'daiyousei',            ('daiyousei',),),
        ('Ebisu Eika',              'ebisu_eika',           ('eika',),),
        ('Erii',                    'elly',                 ('erii','elly',),),
        ('Etanitiraruba',           'eternity_larva',       ('eternity','Etanitiraruba',),),
        ('Fujiwara no Mokou',       'fujiwara_no_mokou',    ('mokou',),),
        ('Futatsuiwa Mamizou',      'futatsuiwa_mamizou',   ('mamizou',),),
        ('Haan Maeriberii',         'maribel_hearn',        ('maeriberii','maribel',),),
        ('Hakurei Reimu',           'hakurei_reimu',        ('reimu',),),
        ('Hata no Kokoro',          'hata_no_kokoro',       ('kokoro',),),
        ('Hieda no Akyuu',          'hieda_no_akyuu',       ('akyuu',),),
        ('Hijiri Byakuren',         'hijiri_byakuren',      ('byakuren',),),
        ('Himekaidou Hatate',       'himekaidou_hatate',    ('hatate',),),
        ('Hinanawi Tenshi',         'hinanawi_tenshi',      ('tenshi',),),
        ('Hon Meirin',              'hong_meiling',         ('meirin','meiling',),),
        ('Horikawa Raiko',          'horikawa_raiko',       ('raiko',),),
        ('Hoshiguma Yuugi',         'hoshiguma_yuugi',      ('yuugi',),),
        ('Houjuu Nue',              'houjuu_nue',           ('nue',),),
        ('Houraisan Kaguya',        'houraisan_kaguya',     ('kaguya',),),
        ('Howaito Ririi',           'lily_white',           ('ririi','lily',),),
        ('Howaitorokku Retii',      'letty_whiterock',      ('retii','letty',),),
        ('Ibaraki Kasen',           'ibaraki_kasen',        ('kasen',),),
        ('Ibuki Suika',             'ibuki_suika',          ('suika',),),
        ('Imaizumi Kagerou',        'imaizumi_kagerou',     ('kagerou',),),
        ('Inaba Tewi',              'inaba_tewi',           ('tewi',),),
        ('Inubashiri Momiji',       'inubashiri_momiji',    ('momiji',),),
        ('Izayoi Sakuya',           'izayoi_sakuya',        ('sakuya',),),
        ('Junko',                   'junko_(touhou)',       ('junko',),),
        ('Kaenbyou Rin',            'kaenbyou_rin',         ('rin',),),
        ('Kagiyama Hina',           'kagiyama_hina',        ('hina',),),
        ('Kaku Seiga',              'kaku_seiga',           ('seiga',),),
        ('Kamishirasawa Keine',     'kamishirasawa_keine',  ('keine',),),
        ('Kasodani Kyouko',         'kasodani_kyouko',      ('kyouko',),),
        ('Kawashiro Nitori',        'kawashiro_nitori',     ('nitori',),),
        ('Kazami Yuuka',            'kazami_yuuka',         ('yuuka',),),
        ('Kijin Seija',             'kijin_seija',          ('seija',),),
        ('Kirisame Marisa',         'kirisame_marisa',      ('marisa',),),
        ('Kishin Sagume',           'kishin_sagume',        ('sagume',),),
        ('Kisume',                  'kisume',               ('kisume',),),
        ('Koakuma',                 'koakuma',              ('koakuma',),),
        ('Kochiya Sanae',           'kochiya_sanae',        ('sanae',),),
        ('Komano Aunn',             'komano_aun',           ('aunn','aun',),),
        ('Komeiji Koishi',          'komeiji_koishi',       ('koishi',),),
        ('Komeiji Satori',          'komeiji_satori',       ('satori',),),
        ('Konngara',                'konngara',             ('konngara',),),
        ('Konpaku Youmu',           'konpaku_youmu',        ('youmu',),),
        ('Kuraunpiisu',             'clownpiece',           ('kuraunpiisu','clownpiece',),),
        ('Kurodani Yamame',         'kurodani_yamame',      ('yamame',),),
        ('Maagatoroido Arisu',      'alice_margatroid',     ('arisu','alice',),),
        ('Matara Okina',            'matara_okina',         ('okina',),),
        ('Merankorii Medisun',      'medicine_melancholy',  ('medisun', 'medicine',),),
        ('Mima',                    'mima',                 ('mima',),),
        ('Sanii Miruku',            'sunny_milk',           ('sanii','sunny',),),
        ('Miyako Yoshika',          'miyako_yoshika',       ('yoshika',),),
        ('Mizuhashi Parusi',        'mizuhashi_parsee',     ('parusi','parsee',),),
        ('Mononobe no Futo',        'mononobe_no_futo',     ('futo',),),
        ('Morichika Rinnosuke',     'morichika_rinnosuke',  ('rinnosuke',),),
        ('Moriya Suwako',           'moriya_suwako',        ('suwako',),),
        ('Motoori Kosuzu',          'motoori_kosuzu',       ('kosuzu',),),
        ('Murasa Minamitsu',        'murasa_minamitsu',     ('minamitsu',),),
        ('Nagae Iku',               'nagae_iku',            ('iku',),),
        ('Nazuurin',                'nazrin',               ('nazuurin','nazrin',),),
        ('Nishida Satono',          'nishida_satono',       ('satono',),),
        ('Niwatari Kutaka',         'niwatari_kutaka',      ('kutaka',),),
        ('Onozuka Komachi',         'onozuka_komachi',      ('komachi',),),
        ('Pachurii Noorejji',       'patchouli_knowledge',  ('patchouli',),),
        ('Purizumuribaa Meruran',   'merlin_prismriver',    ('meruran','merlin',),),
        ('Purizumuribaa Ririka',    'lyrica_prismriver',    ('ririka','lyrica',),),
        ('Purizumuribaa Runasa',    'lunasa_prismriver',    ('runasa','lunasa',),),
        ('Rapisurazuri Hekaatia',   'hecatia_lapislazuli',  ('hekaatia','hecatia',),),
        ('Reisen Udongein Inaba',   'reisen_udongein_inaba',('reisen',),),
        ('Reiuji Utsuho',           'reiuji_utsuho',        ('utsuho',),),
        ('Riguru Naitobagu',        'wriggle_nightbug',     ('riguru','wriggle',),),
        ('Ringo',                   'ringo_(touhou)',       ('ringo',),),
        ('Roorerai Misutia',        'mystia_lorelei',       ('misutia','mystia',),),
        ('Ruumia',                  'rumia',                ('ruumia','rumia',),),
        ('Safaia Sutaa',            'star_sapphire',        ('sutaa','star',),),
        ('Saigyouji Yuyuko',        'saigyouji_yuyuko',     ('yuyuko',),),
        ('Sakata Nemuno',           'sakata_nemuno',        ('nemuno',),),
        ('Seiran',                  'seiran_(touhou)',      ('seiran',),),
        ('Sekibanki',               'sekibanki',            ('sekibanki',),),
        ('Shameimaru Aya',          'shameimaru_aya',       ('aya',),),
        ('Shiki Eiki Yamazanadu',   'shiki_eiki',           ('eiki',),),
        ('Suiito Doremii',          'doremy_sweet',         ('doremy',),),
        ('Sukaaretto Furandooru',   'flandre_scarlet',      ('furandooru','flandre',),),
        ('Sukaaretto Remiria',      'remilia_scarlet',      ('remiria','remilia',),),
        ('Sukuna Shinmyoumaru',     'sukuna_shinmyoumaru',  ('sukuna',),),
        ('Tatara Kogasa',           'tatara_kogasa',        ('kogasa',),),
        ('Teireida Mai',            'teireida_mai',         ('mai',),),
        ('Toramaru Shou',           'toramaru_shou',        ('shou',),),
        ('Toyosatomimi no Miko',    'toyosatomimi_no_miko', ('miko',),),
        ('Usami Renko',             'usami_renko',          ('renko',),),
        ('Usami Sumireko',          'usami_sumireko',       ('sumireko',),),
        ('Ushizaki Urumi',          'ushizaki_urumi',       ('urumi',),),
        ('Wakasagihime',            'wakasagihime',         ('wakasagi','wakasagihime',),),
        ('Watatsuki no Toyohime',   'watatsuki_no_toyohime',('toyohime',),),
        ('Watatsuki no Yorihime',   'watatsuki_no_yorihime',('yorihime',),),
        ('Yagokoro Eirin',          'yagokoro_eirin',       ('eirin',),),
        ('Yakumo Ran',              'yakumo_ran',           ('ran',),),
        ('Yakumo Yukari',           'yakumo_yukari',        ('yukari',),),
        ('Yasaka Kanako',           'yasaka_kanako',        ('kanako',),),
        ('Yatadera Narumi',         'yatadera_narumi',      ('narumi',),),
        ('Yorigami Joon',           'yorigami_jo\'on',      ('joon',),),
        ('Yorigami Shion',          'yorigami_shion',       ('shion',),),
            ):
    command=cached_booru_command(title,tag_name)
    for command_name in command_names:
        booru_commands(command,case=command_name)

del title, tag_name, command_names, command, command_name
del Color, BUILTIN_EMOJIS, Cooldown, CooldownHandler, mark_as_async, eventlist
