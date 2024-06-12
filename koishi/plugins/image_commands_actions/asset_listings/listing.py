__all__ = ('TOUHOU_ACTION_ALL',)


from ...image_handling_core import ImageHandlerStatic
from ...touhou_core import (
    CHEN, CHIRUNO, CLOWNPIECE, DAIYOUSEI, DOREMY_SWEET, FUJIWARA_NO_MOKOU, FUTATSUIWA_MAMIZOU, HAKUREI_MIKO,
    HAKUREI_REIMU, HANIYASUSHIN_KEIKI, HATA_NO_KOKORO, HEARN_MARIBEL, HECATIA_LAPISLAZULI, HIEDA_NO_AKYUU,
    HIJIRI_BYAKUREN, HIMEKAIDOU_HATATE, HINANAWI_TENSHI, HONG_MEILING, HORIKAWA_RAIKO, HOSHIGUMA_YUUGI, HOUJUU_NUE,
    HOURAISAN_KAGUYA, IBARAKI_KASEN, IBUKI_SUIKA, IIZUNAMARU_MEGUMU, IMAIZUMI_KAGEROU, INABA_TEWI, INUBASHIRI_MOMIJI,
    IZAYOI_SAKUYA, JOUTOUGUU_MAYUMI, JUNKO, KAENBYOU_RIN, KAGIYAMA_HINA, KAKU_SEIGA, KAMISHIRASAWA_KEINE,
    KASODANI_KYOUKO, KAWASHIRO_NITORI, KAZAMI_YUUKA, KIRISAME_MARISA, KICCHOU_YACHIE, KIJIN_SEIJA, KISHIN_SAGUME,
    KOAKUMA, KOCHIYA_SANAE, KOMEIJI_KOISHI, KOMEIJI_SATORI, KONPAKU_YOUMU, KUDAMAKI_TSUKASA, KUMOI_ICHIRIN,
    KUROKOMA_SAKI, LETTY_WHITEROCK, LILY_BLACK, LILY_WHITE, LUNA_CHILD, MARGATROID_ALICE, MATARA_OKINA,
    MEDICINE_MELANCHOLY, MIYAKO_YOSHIKA, MIZUHASHI_PARSEE, MONONOBE_NO_FUTO, MORICHIKA_RINNOSUKE, MORIYA_SUWAKO,
    MOTOORI_KOSUZU, MURASA_MINAMITSU, MYSTIA_LORELEI, NAGAE_IKU, NAZRIN, NISHIDA_SATONO, ONOZUKA_KOMACHI,
    PATCHOULI_KNOWLEDGE, REISEN_UDONGEIN_INABA, REIUJI_UTSUHO, RINGO, RUMIA, SAIGYOUJI_YUYUKO, SCARLET_FLANDRE,
    SCARLET_REMILIA, SEIRAN, SEKIBANKI, SHAMEIMARU_AYA, SHIKI_EIKI_YAMAXANADU, SHINKI, SOGA_NO_TOJIKO, STAR_SAPPHIRE,
    SUNNY_MILK, TATARA_KOGASA, TEIREIDA_MAI, TORAMARU_SHOU, TSUKUMO_BENBEN, TSUKUMO_YATSUHASHI, TOUTETSU_YUUMA,
    TOYOSATOMIMI_NO_MIKO, USAMI_RENKO, USAMI_SUMIREKO, WAKASAGIHIME, WRIGGLE_NIGHTBUG, YAGOKORO_EIRIN, YAKUMO_RAN,
    YAKUMO_YUKARI, KURODANI_YAMAME, YASAKA_KANAKO, YOMOTSU_HISAMI, YORIGAMI_SHION
)
from ...user_settings import PREFERRED_IMAGE_SOURCE_TOUHOU

from .constants import (
    ACTION_TAG_COSPLAY, ACTION_TAG_DANCE, ACTION_TAG_FEED, ACTION_TAG_FLUFF, ACTION_TAG_HANDHOLD, ACTION_TAG_HUG,
    ACTION_TAG_KISS, ACTION_TAG_KON, ACTION_TAG_LAP_SLEEP, ACTION_TAG_LICK, ACTION_TAG_LIKE, ACTION_TAG_NOM,
    ACTION_TAG_PAT, ACTION_TAG_POCKY_KISS, ACTION_TAG_POCKY_KISS_SELF, ACTION_TAG_POKE, ACTION_TAG_TICKLE
)


# Source of feeding:
#
# Source 0:
# https://safebooru.org/index.php?page=post&s=list&tags=touhou+feeding+
# Page 1 added from rumia + flandre till ringo + seiran

# Source of fluff:
#
# Source 0:
# From my pc actually.
# :KoishiPc:

# Source of hug:
#
# Source 0:
# https://safebooru.org/index.php?page=post&s=list&tags=touhou+hug&pid=8840
# 2 page added (from behind)

#
# Source 1:
# From my pc actually
# :KoishiPc:

# Source of kiss:
#
# Source 0:
# https://safebooru.org/index.php?page=post&s=list&tags=touhou+kiss&pid=2640
# 2 page added (from behind)

#
# Source 1:
# From my pc actually.
# :KoishiPc:

# Source of kon:
#
# Source 0:
# From my pc actually.
# :KoishiPc:

# Source of lick:
#
# Source 0:
# https://safebooru.org/index.php?page=post&s=list&tags=touhou+licking+&pid=960
# Added: 6 pages (from behind)


# Source of like:
#
# Source 0:
# From my pc actually.
# :KoishiPc:

# Source of pat:
#
# Source 0:
# https://safebooru.org/index.php?page=post&s=list&tags=touhou+pat+
# Added: all pages (first one is daiyousei solo)

#
# Source 1:
# https://safebooru.org/index.php?page=post&s=list&tags=touhou+patting
# Added: all (first one is sanae & tsukasa)

#
# Source 2:
# https://safebooru.org/index.php?page=post&s=list&tags=touhou+patting_head+
# Added: all (first one is kaguya & chen)

#
# Source 3:
# Images from my pc
# :KoishiPc:
#
# Source 4:
# https://safebooru.org/index.php?page=post&s=list&tags=touhou+headpat+&pid=120
# none added
#
# Notes: There are way more pictures on danbooru, over 100 pages, which could yield to around 500 images.

# Source of pocky-kiss:
#
# Source 0:
# https://safebooru.org/index.php?page=post&s=list&tags=2girls+pocky_kiss+touhou
# All added

# Source of pocky-kiss-self:
#
# Source 0:
# https://safebooru.org/index.php?page=post&s=list&tags=touhou+pocky+solo
# All added

# Source of tickle:
#
# Source 0:
# From my pc actually.
# :KoishiPc:

# Source of lap-sleep:
#
# Source 0:
# From meiko.
#
# Source 0:
# From my pc actually.
# :KoishiPc:

TOUHOU_ACTION_ALL = ImageHandlerStatic(PREFERRED_IMAGE_SOURCE_TOUHOU)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1219193725947871262/chiruno-feed-0000.png',
).with_action(
    ACTION_TAG_FEED, CHIRUNO, CHIRUNO,
).with_creator(
    'mikan (manmarumikan)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1219199629443203162/flandre-remilia-sakuya-feed-0000.png',
).with_action(
    ACTION_TAG_FEED, SCARLET_FLANDRE, SCARLET_REMILIA,
).with_character(
    IZAYOI_SAKUYA,
).with_creator(
    'shimotsuki aoi',
).with_editor(
    'HuyaneMatsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1219184783611920424/flandre-rumia-feed-0000.png',
).with_action(
    ACTION_TAG_FEED, SCARLET_FLANDRE, RUMIA,
).with_creator(
    'fleuriste',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1219191396397875250/flandre-yuuma-feed-0000.png',
).with_action(
    ACTION_TAG_FEED, SCARLET_FLANDRE, TOUTETSU_YUUMA,
).with_creator(
    'fifiruu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1219197486661632030/iku-tenshi-feed-0000.png',
).with_action(
    ACTION_TAG_FEED, NAGAE_IKU, HINANAWI_TENSHI,
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1219192143508410378/koishi-feed-0000.png',
).with_action(
    ACTION_TAG_FEED, None, KOMEIJI_KOISHI,
).with_creator(
    'zunusama',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1219196416442896445/koishi-feed-0001.png',
).with_action(
    ACTION_TAG_FEED, None, KOMEIJI_KOISHI,
).with_creator(
    'zunusama',
).with_editor(
    'HuyaneMatsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1219186780817850378/marisa-reimu-feed-0000.png',
).with_action(
    ACTION_TAG_FEED, KIRISAME_MARISA, HAKUREI_REIMU,
).with_creator(
    'yomogi 9392',
).with_editor(
    'HuyaneMatsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1219252027981566052/miko-remilia-feed-0000.png',
).with_action(
    ACTION_TAG_FEED, TOYOSATOMIMI_NO_MIKO, SCARLET_REMILIA,
).with_creator(
    'kochi michikaze',
).with_editor(
    'HuyaneMatsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1219259653997723749/reimu-sakuya-feed-0000.png',
).with_action(
    ACTION_TAG_FEED, IZAYOI_SAKUYA, HAKUREI_REIMU,
).with_creator(
    'himadera',
).with_editor(
    'HuyaneMatsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1232761508631547914/reisen-youmu-feed-0000.gif',
).with_action(
    ACTION_TAG_FEED, REISEN_UDONGEIN_INABA, KONPAKU_YOUMU,
).with_creator(
    'evandragon',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1219261244368883722/ringo-seiran-feed-0000.png',
).with_action(
    ACTION_TAG_FEED, SEIRAN, RINGO,
).with_creator(
    'chamaruku',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1219189215674499072/sakuya-feed-0000.png',
).with_action(
    ACTION_TAG_FEED, IZAYOI_SAKUYA, None,
).with_creator(
    'ari don',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1219183800043569203/youmu-yuyuko-feed-0000.png',
).with_action(
    ACTION_TAG_FEED, KONPAKU_YOUMU, SAIGYOUJI_YUYUKO,
).with_creator(
    'dodooo (rully ernandooo)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1207953432472985600/chen-mamizou-orin-fluff-0000.png',
).with_actions(
    (ACTION_TAG_FLUFF, CHEN, FUTATSUIWA_MAMIZOU),
    (ACTION_TAG_FLUFF, KAENBYOU_RIN, FUTATSUIWA_MAMIZOU),
).with_creator(
    'rokunen',
).with_editor(
    'HuyaneMatsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1207956050775646208/chen-ran-fluff-0000.png',
).with_action(
    ACTION_TAG_FLUFF, CHEN, YAKUMO_RAN,
).with_creator(
    'weee (raemz)',
).with_editor(
    'HuyaneMatsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1207956374655471616/chen-ran-fluff-0001.png',
).with_action(
    ACTION_TAG_FLUFF, CHEN, YAKUMO_RAN,
).with_creator(
    'hihachi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1207956871412195348/chen-ran-fluff-0002.png',
).with_action(
    ACTION_TAG_FLUFF, CHEN, YAKUMO_RAN,
).with_creator(
    'kyuubi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1207957439014641704/chen-ran-fluff-0003.png',
).with_action(
    ACTION_TAG_FLUFF, CHEN, YAKUMO_RAN,
).with_creator(
    'emia (castilla)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1207957777176334396/chen-ran-fluff-0004.png',
).with_action(
    ACTION_TAG_FLUFF, CHEN, YAKUMO_RAN,
).with_creator(
    'kamiya tomoe',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1207959805059145778/chen-ran-fluff-0005.png',
).with_actions(
    (ACTION_TAG_FLUFF, CHEN, YAKUMO_RAN),
    (ACTION_TAG_FLUFF, YAKUMO_RAN, CHEN),
).with_creator(
    'ai takurou',
).with_editor(
    'HuyaneMatsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1207966320046374932/chen-ran-fluff-0006.png',
).with_action(
    ACTION_TAG_FLUFF, CHEN, YAKUMO_RAN,
).with_creator(
    'ibarashiro natou',
).with_editor(
    'HuyaneMatsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1208512711009370182/chen-ran-fluff-0007.png',
).with_action(
    ACTION_TAG_FLUFF, CHEN, YAKUMO_RAN,
).with_creators(
    'kakao (chocolate land)', 'okoge senbei',
).with_editor(
    'HuyaneMatsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1208513375269814322/chen-ran-fluff-0008.png',
).with_action(
    ACTION_TAG_FLUFF, CHEN, YAKUMO_RAN,
).with_creator(
    'peachems (gemu)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1208514001483595776/chen-ran-fluff-0009.png',
).with_action(
    ACTION_TAG_FLUFF, CHEN, YAKUMO_RAN,
).with_creator(
    'fuuga (perv rsity)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1208514002322460732/chen-ran-fluff-0010.png',
).with_action(
    ACTION_TAG_FLUFF, CHEN, YAKUMO_RAN,
).with_creator(
    'emia',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1208514911664082964/chen-ran-fluff-0011.png',
).with_action(
    ACTION_TAG_FLUFF, CHEN, YAKUMO_RAN,
).with_creator(
    'sasakura',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1208514912012476546/chen-ran-fluff-0012.png',
).with_action(
    ACTION_TAG_FLUFF, CHEN, YAKUMO_RAN,
).with_creator(
    'ohyo',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1208515752605261844/chen-ran-fluff-0013.png',
).with_action(
    ACTION_TAG_FLUFF, CHEN, YAKUMO_RAN,
).with_creator(
    'nonaka',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1208515753079476314/chen-ran-fluff-0014.png',
).with_action(
    ACTION_TAG_FLUFF, CHEN, YAKUMO_RAN,
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1208517062495051796/chen-ran-fluff-0015.png',
).with_action(
    ACTION_TAG_FLUFF, CHEN, YAKUMO_RAN,
).with_creator(
    'kaisen',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1208517062847111268/chen-ran-fluff-0016.png',
).with_action(
    ACTION_TAG_FLUFF, CHEN, YAKUMO_RAN,
).with_creator(
    'inoe (noie)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1208517897429848074/chen-ran-fluff-0017.png',
).with_action(
    ACTION_TAG_FLUFF, CHEN, YAKUMO_RAN,
).with_creator(
    'asakura haru',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1208517898130427984/chen-ran-fluff-0018.png',
).with_action(
    ACTION_TAG_FLUFF, CHEN, YAKUMO_RAN,
).with_creator(
    'niiya',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1208518589284614214/chen-ran-fluff-0019.png',
).with_action(
    ACTION_TAG_FLUFF, CHEN, YAKUMO_RAN,
).with_creator(
    'natsuk',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1208518589645062244/chen-ran-fluff-0020.png',
).with_action(
    ACTION_TAG_FLUFF, CHEN, YAKUMO_RAN,
).with_creator(
    'takamoto akisa',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1208521042444812360/chen-ran-fluff-0021.png',
).with_action(
    ACTION_TAG_FLUFF, CHEN, YAKUMO_RAN,
).with_creator(
    'grimoire-may',
).with_editor(
    'HuyaneMatsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1208521673683378246/chen-ran-fluff-0022.png',
).with_action(
    ACTION_TAG_FLUFF, CHEN, YAKUMO_RAN,
).with_creator(
    'meeko',
).with_editor(
    'HuyaneMatsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1208521824732848168/chen-ran-fluff-0023.png',
).with_action(
    ACTION_TAG_FLUFF, CHEN, YAKUMO_RAN,
).with_creator(
    'orga (pixiv) / organ ,,'
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1208521825345347686/chen-ran-fluff-0024.png',
).with_action(
    ACTION_TAG_FLUFF, CHEN, YAKUMO_RAN,
).with_creator(
    'alu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1208521825794134016/chen-ran-fluff-0025.png',
).with_action(
    ACTION_TAG_FLUFF, CHEN, YAKUMO_RAN,
).with_creator(
    'aosaki',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1208522869303152730/chen-ran-reimu-fluff-0000.png',
).with_actions(
    (ACTION_TAG_FLUFF, CHEN, YAKUMO_RAN),
    (ACTION_TAG_FLUFF, HAKUREI_REIMU, YAKUMO_RAN),
).with_creator(
    'mumumu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1208528070341042186/chen-ran-reimu-fluff-0001.png',
).with_action(
    ACTION_TAG_FLUFF, HAKUREI_REIMU, YAKUMO_RAN,
).with_character(
    CHEN,
).with_creator(
    'yanazuki',
).with_editor(
    'HuyaneMatsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1208708292050681906/chen-ran-yukari-fluff-0000.png',
).with_actions(
    (ACTION_TAG_FLUFF, YAKUMO_YUKARI, YAKUMO_RAN),
    (ACTION_TAG_FLUFF, YAKUMO_RAN, CHEN),
).with_creator(
    'nanana (chicken union)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1236212795406553108/chen-ran-yukari-fluff-hug-0000.png',
).with_actions(
    (ACTION_TAG_FLUFF, YAKUMO_YUKARI, YAKUMO_RAN),
    (ACTION_TAG_HUG, YAKUMO_RAN, CHEN),
).with_creator(
    'nupeya',
).with_editor(
    'HuyaneMatsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1208709815145070632/chen-ran-yukari-fluff-0002.png',
).with_action(
    ACTION_TAG_FLUFF, CHEN, YAKUMO_RAN,
).with_character(
    YAKUMO_YUKARI,
).with_creator(
    'mow (momom)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1236212960125390898/chen-ran-yukari-fluff-poke-0003.png',
).with_actions(
    (ACTION_TAG_FLUFF, CHEN, YAKUMO_RAN),
    (ACTION_TAG_POKE, YAKUMO_YUKARI, CHEN),
).with_creator(
    'yuugo (atmosphere)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1208714921035038761/chen-ran-yukari-fluff-0004.png',
).with_actions(
    (ACTION_TAG_FLUFF, CHEN, YAKUMO_RAN),
    (ACTION_TAG_FLUFF, YAKUMO_YUKARI, YAKUMO_RAN),
).with_creator(
    'kani nyan',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1208715748193599558/chen-ran-yukari-fluff-0005.png',
).with_action(
    ACTION_TAG_FLUFF, YAKUMO_YUKARI, YAKUMO_RAN,
).with_character(
    CHEN,
).with_creator(
    'pudding (skymint 028)',
).with_editor(
    'HuyaneMatsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1208718306484158494/chen-ran-yukari-fluff-0006.png',
).with_actions(
    (ACTION_TAG_FLUFF, CHEN, YAKUMO_RAN),
    (ACTION_TAG_FLUFF, YAKUMO_YUKARI, YAKUMO_RAN),
).with_creator(
    'akuroporisu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1208718866419679262/chen-ran-yukari-fluff-0007.png',
).with_action(
    ACTION_TAG_FLUFF, CHEN, YAKUMO_RAN,
).with_character(
    YAKUMO_YUKARI,
).with_creator(
    'kurot',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1208719196767125564/chen-ran-yukari-fluff-0008.png',
).with_action(
    ACTION_TAG_FLUFF, YAKUMO_YUKARI, YAKUMO_RAN,
).with_character(
    CHEN,
).with_creator(
    'coco',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1208719820321857597/chen-ran-yukari-fluff-0009.png',
).with_action(
    ACTION_TAG_FLUFF, CHEN, YAKUMO_RAN,
).with_character(
    YAKUMO_YUKARI,
).with_creator(
    'poncho',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1208720609643728936/chen-ran-yukari-fluff-0010.png',
).with_action(
    ACTION_TAG_FLUFF, CHEN, YAKUMO_RAN,
).with_character(
    YAKUMO_YUKARI,
).with_creator(
    'tenpura',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1208720856487039056/chen-ran-yukari-fluff-0011.png',
).with_actions(
    (ACTION_TAG_FLUFF, CHEN, YAKUMO_RAN),
    (ACTION_TAG_FLUFF, YAKUMO_YUKARI, CHEN),
).with_creator(
    'kawanabe',
).with_editor(
    'HuyaneMatsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1208721349615423528/chen-ran-yukari-fluff-0012.png',
).with_actions(
    (ACTION_TAG_FLUFF, CHEN, YAKUMO_RAN),
    (ACTION_TAG_FLUFF, YAKUMO_YUKARI, YAKUMO_RAN),
).with_creator(
    'kirisita',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1208721705846185994/chen-ran-yukari-fluff-0013.png',
).with_action(
    ACTION_TAG_FLUFF, CHEN, YAKUMO_RAN,
).with_character(
    YAKUMO_YUKARI,
).with_creator(
    'sasuke (sasuke no sato)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1208722034687873034/chen-ran-yukari-fluff-0014.png',
).with_action(
    ACTION_TAG_FLUFF, CHEN, YAKUMO_RAN,
).with_character(
    YAKUMO_YUKARI,
).with_creator(
    'mikashimo / mikasimo',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1208722399231606784/hijiri-kyouko-mamizou-murasa-nue-fluff-0000.png',
).with_actions(
    (ACTION_TAG_FLUFF, KASODANI_KYOUKO, FUTATSUIWA_MAMIZOU),
    (ACTION_TAG_FLUFF, MURASA_MINAMITSU, FUTATSUIWA_MAMIZOU),
).with_characters(
    HOUJUU_NUE, HIJIRI_BYAKUREN,
).with_creator(
    'urin',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1208723469928235008/kagerou-momiji-fluff-0000.png',
).with_action(
    ACTION_TAG_FLUFF, IMAIZUMI_KAGEROU, INUBASHIRI_MOMIJI,
).with_creator(
    'urin',
).with_editor(
    'HuyaneMatsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1208724082846203955/kagerou-wakasagihime-fluff-0000.png',
).with_action(
    ACTION_TAG_FLUFF, WAKASAGIHIME, IMAIZUMI_KAGEROU,
).with_creator(
    'ryuuichi (f dragon)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1208725021007286362/kaguya-tewi-fluff-0000.png',
).with_action(
    ACTION_TAG_FLUFF, HOURAISAN_KAGUYA, INABA_TEWI,
).with_creator(
    'anaguma (regret party)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1208726099929075762/keine-mokou-fluff-0000.png',
).with_action(
    ACTION_TAG_FLUFF, FUJIWARA_NO_MOKOU, KAMISHIRASAWA_KEINE,
).with_creator(
    'newbokk',
).with_editor(
    'HuyaneMatsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1208727149196869652/kokoro-mamizou-fluff-0000.png',
).with_action(
    ACTION_TAG_FLUFF, HATA_NO_KOKORO, FUTATSUIWA_MAMIZOU,
).with_creator(
    'mofu mofu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1208727681626017792/kyouko-fluff-0000.png',
).with_action(
    ACTION_TAG_FLUFF, None, KASODANI_KYOUKO,
).with_creator(
    'ammer (sunset beach)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1208729217429282866/kyouko-mamizou-fluff-0000.png',
).with_action(
    ACTION_TAG_FLUFF, KASODANI_KYOUKO, FUTATSUIWA_MAMIZOU,
).with_creators(
    'doku corne', 'poikoro',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1208729874840289370/kyouko-parsee-fluff-0000.png',
).with_action(
    ACTION_TAG_FLUFF, MIZUHASHI_PARSEE, KASODANI_KYOUKO,
).with_creator(
    'cato (monocatienus)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1208730754931236885/kyouko-sanae-fluff-0000.png',
).with_action(
    ACTION_TAG_FLUFF, KOCHIYA_SANAE, KASODANI_KYOUKO,
).with_creator(
    'suzushiro yukari',
).with_editor(
    'HuyaneMatsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1208731839250964480/mai-ran-satono-fluff-0000.png',
).with_actions(
    (ACTION_TAG_FLUFF, TEIREIDA_MAI, YAKUMO_RAN),
    (ACTION_TAG_FLUFF, NISHIDA_SATONO, YAKUMO_RAN),
).with_creator(
    'itatatata',
).with_editor(
    'HuyaneMatsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1208733428623745054/mamizou-nue-fluff-0000.png',
).with_action(
    ACTION_TAG_FLUFF, HOUJUU_NUE, FUTATSUIWA_MAMIZOU,
).with_creator(
    'kiwitan',
).with_editor(
    'HuyaneMatsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1208732945750425640/mamizou-nue-fluff-0001.png',
).with_action(
    ACTION_TAG_FLUFF, HOUJUU_NUE, FUTATSUIWA_MAMIZOU,
).with_creator(
    'unime seaflower',
).with_editor(
    'HuyaneMatsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1208734747254071336/mamizou-reimu-fluff-0000.png',
).with_action(
    ACTION_TAG_FLUFF, HAKUREI_REIMU, FUTATSUIWA_MAMIZOU,
).with_creator(
    'shirane koitsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1223563583024136202/megumu-tsukasa-fluff-0000.png',
).with_action(
    ACTION_TAG_FLUFF, IIZUNAMARU_MEGUMU, KUDAMAKI_TSUKASA,
).with_creator(
    'meimaru inuchiyo',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1208735420377202759/momiji-sumireko-fluff-0000.png',
).with_action(
    ACTION_TAG_FLUFF, USAMI_SUMIREKO, INUBASHIRI_MOMIJI,
).with_creator(
    'kutsuki kai',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1208735906802962492/nazrin-reimu-fluff-0000.png',
).with_action(
    ACTION_TAG_FLUFF, HAKUREI_REIMU, NAZRIN,
).with_creator(
    'mochizuki ado',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1208736565522599956/nazrin-sanae-fluff-0000.png',
).with_action(
    ACTION_TAG_FLUFF, KOCHIYA_SANAE, NAZRIN,
).with_creator(
    'ichimi',
).with_editor(
    'HuyaneMatsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1209026357812531240/ran-yukari-fluff-0000.png',
).with_action(
    ACTION_TAG_FLUFF, YAKUMO_YUKARI, YAKUMO_RAN,
).with_creator(
    'maszom',
).with_editor(
    'HuyaneMatsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1208737577067089950/ran-yukari-fluff-0001.png',
).with_action(
    ACTION_TAG_FLUFF, YAKUMO_YUKARI, YAKUMO_RAN,
).with_creator(
    'sirousagi0414',
).with_editor(
    'HuyaneMatsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1208737577704882246/ran-yukari-fluff-0002.png',
).with_action(
    ACTION_TAG_FLUFF, YAKUMO_YUKARI, YAKUMO_RAN,
).with_creator(
    'masanaga (tsukasa)',
).with_editor(
    'HuyaneMatsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1208737578229039186/ran-yukari-fluff-0003.png',
).with_action(
    ACTION_TAG_FLUFF, YAKUMO_YUKARI, YAKUMO_RAN,
).with_creator(
    'makarori',
).with_editor(
    'HuyaneMatsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1208737578816249876/ran-yukari-fluff-0004.png',
).with_action(
    ACTION_TAG_FLUFF, YAKUMO_YUKARI, YAKUMO_RAN,
).with_creator(
    'peroponesosu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1223565656734306335/ran-yukari-fluff-0005.png',
).with_action(
    ACTION_TAG_FLUFF, YAKUMO_YUKARI, YAKUMO_RAN,
).with_creator(
    'R O T O N',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1208739850895753286/reisen-tewi-fluff-0000.png',
).with_action(
    ACTION_TAG_FLUFF, REISEN_UDONGEIN_INABA, INABA_TEWI,
).with_creator(
    'tsukimirin',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1223566216367443978/rumia-tewi-fluff-0000.png',
).with_action(
    ACTION_TAG_FLUFF, RUMIA, INABA_TEWI,
).with_creator(
    'furim',
)


TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1232754036675973281/alice-shinki-hug-0000.png',
).with_action(
    ACTION_TAG_HUG, SHINKI, MARGATROID_ALICE,
).with_creator(
    'hiyaya (kochi michikaze)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1223583582220456029/chen-ran-hug-0000.png',
).with_action(
    ACTION_TAG_HUG, YAKUMO_RAN, CHEN,
).with_creator(
    'miiko (somnolent)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1232755638321545246/chen-ran-hug-0001.png',
).with_actions(
    (ACTION_TAG_HUG, CHEN, YAKUMO_RAN),
    (ACTION_TAG_HUG, YAKUMO_RAN, CHEN),
).with_creator(
    'kalmia495',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1220328524653793303/chen-ran-yukari-hug-0000.png',
).with_actions(
    (ACTION_TAG_HUG, CHEN, YAKUMO_RAN),
    (ACTION_TAG_HUG, YAKUMO_RAN, YAKUMO_RAN),
).with_creator(
    'coco',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1220266946021556254/eirin-kaguya-hug-0000.png',
).with_action(
    ACTION_TAG_HUG, HOURAISAN_KAGUYA, YAGOKORO_EIRIN,
).with_creator(
    'mosuke',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1220443739642662952/eirin-reisen-hug-0000.png',
).with_action(
    ACTION_TAG_HUG, YAGOKORO_EIRIN, REISEN_UDONGEIN_INABA,
).with_creator(
    'rokuwata tomoe',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1223584864469778442/flandre-koishi-hug-0000.png',
).with_action(
    ACTION_TAG_HUG, SCARLET_FLANDRE, KOMEIJI_KOISHI,
).with_creator(
    'fkey',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1220448035662987264/flandre-marisa-hug-0000.png',
).with_action(
    ACTION_TAG_HUG, SCARLET_FLANDRE, KIRISAME_MARISA,
).with_creator(
    'suzuho',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1220451292103577620/flandre-marisa-hug-0001.png',
).with_action(
    ACTION_TAG_HUG, KIRISAME_MARISA, SCARLET_FLANDRE,
).with_creator(
    'mikage',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1220452861675176106/flandre-marisa-hug-0002.png',
).with_action(
    ACTION_TAG_HUG, KIRISAME_MARISA, SCARLET_FLANDRE,
).with_creator(
    'shindo',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1220265826171617350/flandre-remilia-hug-0000.png',
).with_actions(
    (ACTION_TAG_HUG, SCARLET_FLANDRE, SCARLET_REMILIA),
    (ACTION_TAG_HUG, SCARLET_REMILIA, SCARLET_FLANDRE),
).with_creator(
    'kamumiya',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1220449089473482762/flandre-remilia-hug-0001.png',
).with_action(
    ACTION_TAG_HUG, SCARLET_FLANDRE, SCARLET_REMILIA,
).with_creator(
    'nishiuri',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1220450482544316466/flandre-remilia-hug-0002.png',
).with_action(
    ACTION_TAG_HUG, SCARLET_FLANDRE, SCARLET_REMILIA,
).with_creator(
    'kou 2008',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1223871834794102804/hijiri-nue-hug-0000.png',
).with_actions(
    (ACTION_TAG_HUG, HIJIRI_BYAKUREN, HOUJUU_NUE),
    (ACTION_TAG_HUG, HOUJUU_NUE, HIJIRI_BYAKUREN),
).with_creator(
    'sheya',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1220445835314204672/kaguya-mokou-hug-0000.png',
).with_action(
    ACTION_TAG_HUG, HOURAISAN_KAGUYA, FUJIWARA_NO_MOKOU,
).with_creator(
    'ayakashi (monkeypanch)',
).with_editor(
    'HuyaneMatsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1220331527884378162/kaguya-tewi-hug-0000.png',
).with_action(
    ACTION_TAG_HUG, HOURAISAN_KAGUYA, INABA_TEWI,
).with_creator(
    'yuta (ricochetsmain)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1220444261405954048/kanako-suwako-hug-0000.png',
).with_actions(
    (ACTION_TAG_HUG, MORIYA_SUWAKO, YASAKA_KANAKO),
    (ACTION_TAG_HUG, YASAKA_KANAKO, MORIYA_SUWAKO),
).with_creators(
    'amaya enaka', 'tentani',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1223719258941292696/keiki-mayumi-hug-0000.png',
).with_actions(
    (ACTION_TAG_HUG, HANIYASUSHIN_KEIKI, JOUTOUGUU_MAYUMI),
    (ACTION_TAG_HUG, JOUTOUGUU_MAYUMI, HANIYASUSHIN_KEIKI),
).with_creator(
    'biyon',
).with_editor(
    'HuyaneMatsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1220447468173656166/keine-mokou-hug-0000.png',
).with_actions(
    (ACTION_TAG_HUG, KAMISHIRASAWA_KEINE, FUJIWARA_NO_MOKOU),
    (ACTION_TAG_HUG, FUJIWARA_NO_MOKOU, KAMISHIRASAWA_KEINE),
).with_creator(
    'shinoasa',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1223721535311974400/koishi-hug-0000.png',
).with_action(
    ACTION_TAG_HUG, KOMEIJI_KOISHI, KOMEIJI_KOISHI,
).with_editor(
    'shan',
).with_editor(
    'HuyaneMatsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1223601016079912991/koishi-kokoro-hug-0000.png',
).with_actions(
    (ACTION_TAG_HUG, KOMEIJI_KOISHI, HATA_NO_KOKORO),
    (ACTION_TAG_HUG, HATA_NO_KOKORO, KOMEIJI_KOISHI),
).with_creator(
    'tada no nasu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1223602190455934976/koishi-kokoro-hug-0001.png',
).with_action(
    ACTION_TAG_HUG, KOMEIJI_KOISHI, HATA_NO_KOKORO,
).with_creator(
    'sorani (kaeru0768)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1223603074053046302/koishi-kokoro-hug-0002.png',
).with_action(
    ACTION_TAG_HUG, KOMEIJI_KOISHI, HATA_NO_KOKORO,
).with_creator(
    'kawayabug',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1223710267503022131/koishi-kokoro-hug-0003.png',
).with_action(
    ACTION_TAG_HUG, KOMEIJI_KOISHI, HATA_NO_KOKORO,
).with_creator(
    'sekisei (superego51)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1223724567067889825/koishi-okuu-hug-0000.png',
).with_action(
    ACTION_TAG_HUG, REIUJI_UTSUHO, KOMEIJI_KOISHI,
).with_creator(
    'rakucat',
).with_editor(
    'HuyaneMatsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1223720362240512050/koishi-orin-hug-0000.png',
).with_action(
    ACTION_TAG_HUG, KOMEIJI_KOISHI, KAENBYOU_RIN,
).with_creator(
    'asameshi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1223585164102209576/koishi-reimu-hug-0000.png',
).with_action(
    ACTION_TAG_HUG, KOMEIJI_KOISHI, HAKUREI_REIMU,
).with_creator(
    'inuno rakugaki',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1220265214897950720/koishi-satori-hug-0000.png',
).with_action(
    ACTION_TAG_HUG, KOMEIJI_SATORI, KOMEIJI_KOISHI,
).with_creator(
    'shino (eefy)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1220269573971120189/koishi-satori-hug-0001.png',
).with_action(
    ACTION_TAG_HUG, KOMEIJI_KOISHI, KOMEIJI_SATORI,
).with_creator(
    'iori yakatabako',
).with_editor(
    'HuyaneMatsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1223585980855091261/koishi-satori-hug-0002.png',
).with_action(
    ACTION_TAG_HUG, KOMEIJI_SATORI, KOMEIJI_KOISHI,
).with_creator(
    'tomobe kinuko',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1223587363779776614/koishi-satori-hug-0003.png',
).with_action(
    ACTION_TAG_HUG, KOMEIJI_KOISHI, KOMEIJI_SATORI,
).with_creator(
    'tsune (tune)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1223600484682825879/koishi-satori-hug-0004.png',
).with_action(
    ACTION_TAG_HUG, KOMEIJI_KOISHI, KOMEIJI_SATORI,
).with_creator(
    '999 (hansode)',
).with_editor(
    'HuyaneMatsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1232757559597989908/koishi-satori-hug-0005.png',
).with_action(
    ACTION_TAG_HUG, KOMEIJI_KOISHI, KOMEIJI_SATORI,
).with_creator(
    'senzaicha kasukadoki',
).with_editor(
    'HuyaneMatsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1220261434416693308/marisa-reimu-hug-0000.png',
).with_actions(
    (ACTION_TAG_HUG, KIRISAME_MARISA, HAKUREI_REIMU),
    (ACTION_TAG_HUG, HAKUREI_REIMU, KIRISAME_MARISA),
).with_creator(
    'haru aki',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1220446460278083604/marisa-reimu-hug-0001.png',
).with_action(
    ACTION_TAG_HUG, HAKUREI_REIMU, KIRISAME_MARISA,
).with_creator(
    'futaba miwa',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1223717761398607902/marisa-reimu-hug-0002.png',
).with_action(
    ACTION_TAG_HUG, HAKUREI_REIMU, KIRISAME_MARISA,
).with_creator(
    'mukkushi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1223717960275984384/marisa-reimu-hug-0003.png',
).with_action(
    ACTION_TAG_HUG, HAKUREI_REIMU, KIRISAME_MARISA,
).with_creator(
    'piyokichi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1220451881143242842/marisa-yuuka-hug-0000.png',
).with_action(
    ACTION_TAG_HUG, KIRISAME_MARISA, KAZAMI_YUUKA,
).with_creator(
    'discharge cycle',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1223871067202785291/murasa-nue-hug-0000.png',
).with_action(
    ACTION_TAG_HUG, HOUJUU_NUE, MURASA_MINAMITSU,
).with_creator(
    'yuuna (yy12)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1223871067584598016/murasa-nue-hug-0001.png',
).with_action(
    ACTION_TAG_HUG, MURASA_MINAMITSU, HOUJUU_NUE,
).with_creator(
    'soiri (us)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1223571617431420969/nue-okuu-hug-0000.png',
).with_actions(
    (ACTION_TAG_HUG, HOUJUU_NUE, REIUJI_UTSUHO),
    (ACTION_TAG_HUG, REIUJI_UTSUHO, HOUJUU_NUE),
).with_creator(
    'shiny shinx',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1223878125096538122/okuu-orin-hug-0000.png',
).with_action(
    ACTION_TAG_HUG, REIUJI_UTSUHO, KAENBYOU_RIN,
).with_creator(
    'miata (miata8674)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1223878125415563334/okuu-orin-hug-0001.png',
).with_action(
    ACTION_TAG_HUG, REIUJI_UTSUHO, KAENBYOU_RIN,
).with_creator(
    'bwell',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1223879720219840542/okuu-orin-hug-0002.png',
).with_action(
    ACTION_TAG_HUG, KAENBYOU_RIN, REIUJI_UTSUHO,
).with_creator(
    'yukihiko (sky sleep)',
).with_editor(
    'HuyaneMatsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1223878126283526164/okuu-orin-hug-0003.png',
).with_action(
    ACTION_TAG_HUG, REIUJI_UTSUHO, KAENBYOU_RIN,
).with_creator(
    'toutenkou',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1223878127017787502/okuu-orin-hug-0004.png',
).with_action(
    ACTION_TAG_HUG, REIUJI_UTSUHO, KAENBYOU_RIN,
).with_creator(
    'shiromoru (yozakura_rety)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1223878127520841828/okuu-orin-hug-0005.png',
).with_actions(
    (ACTION_TAG_HUG, REIUJI_UTSUHO, KAENBYOU_RIN),
    (ACTION_TAG_HUG, KAENBYOU_RIN, REIUJI_UTSUHO),
).with_creator(
    'toutenkou',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1223878128037003274/okuu-orin-hug-0006.png',
).with_action(
    ACTION_TAG_HUG, REIUJI_UTSUHO, KAENBYOU_RIN,
).with_creator(
    'ruu (tksymkw)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1223878128586195034/okuu-orin-hug-0007.png',
).with_action(
    ACTION_TAG_HUG, KAENBYOU_RIN, REIUJI_UTSUHO,
).with_creator(
    'toutenkou',
).with_editor(
    'HuyaneMatsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1220327756517212202/reimu-yukari-hug-0000.png',
).with_action(
    ACTION_TAG_HUG, YAKUMO_YUKARI, HAKUREI_REIMU,
).with_creator(
    'murasaki kajima',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1220330697470775296/reisen-tewi-hug-0000.png',
).with_action(
    ACTION_TAG_HUG, INABA_TEWI, REISEN_UDONGEIN_INABA,
).with_creator(
    'yuuki tatsuya',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1220329396536217600/remilia-sakuya-hug-0000.png',
).with_action(
    ACTION_TAG_HUG, SCARLET_REMILIA, IZAYOI_SAKUYA,
).with_creator(
    'koto (colorcube)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1223588897133695046/remilia-satori-hug-0000.png',
).with_actions(
    (ACTION_TAG_HUG, SCARLET_REMILIA, KOMEIJI_SATORI),
    (ACTION_TAG_HUG, KOMEIJI_SATORI, SCARLET_REMILIA),
).with_creator(
    'eringi (rmrafrn)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1232756624452616335/remilia-satori-hug-0001.png',
).with_action(
    ACTION_TAG_HUG, KOMEIJI_SATORI, SCARLET_REMILIA,
).with_creator(
    'kameyan',
).with_editor(
    'HuyaneMatsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1220450004808896513/youmu-yukari-hug-0000.png',
).with_action(
    ACTION_TAG_HUG, YAKUMO_YUKARI, KONPAKU_YOUMU,
).with_creator(
    'ukyo rst',
).with_editor(
    'HuyaneMatsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1220252970327736340/alice-marisa-kiss-0000.png',
).with_action(
    ACTION_TAG_KISS, MARGATROID_ALICE, KIRISAME_MARISA,
).with_creators(
    'daken', 'jingo kajiki',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1220258995626049587/alice-marisa-kiss-0001.png',
).with_actions(
    (ACTION_TAG_KISS, MARGATROID_ALICE, KIRISAME_MARISA),
    (ACTION_TAG_KISS, KIRISAME_MARISA, MARGATROID_ALICE),
).with_creator(
    'matyinging',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1220252166154092545/aya-reisen-tewi-kiss-0000.png',
).with_action(
    ACTION_TAG_KISS, INABA_TEWI, REISEN_UDONGEIN_INABA,
).with_character(
    SHAMEIMARU_AYA,
).with_creator(
    'akagi akemi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1223888294618599465/aya-hatate-kiss-0000.png',
).with_actions(
    (ACTION_TAG_KISS, SHAMEIMARU_AYA, HIMEKAIDOU_HATATE),
    (ACTION_TAG_KISS, HIMEKAIDOU_HATATE, SHAMEIMARU_AYA),
).with_creator(
    'bmkro',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1223887385968775209/chen-nue-kiss-0000.png',
).with_action(
    ACTION_TAG_KISS, HOUJUU_NUE, CHEN,
).with_creator(
    'ishikkoro',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1220259663019376692/eirin-kaguya-kiss-0000.png',
).with_actions(
    (ACTION_TAG_KISS, YAGOKORO_EIRIN, HOURAISAN_KAGUYA),
    (ACTION_TAG_KISS, HOURAISAN_KAGUYA, YAGOKORO_EIRIN),
).with_creator(
    'aw',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1220256917948203069/eirin-reisen-youmu-yuyuko-kiss-0000.png',
).with_action(
    ACTION_TAG_KISS, KONPAKU_YOUMU, REISEN_UDONGEIN_INABA,
).with_characters(
    YAGOKORO_EIRIN, SAIGYOUJI_YUYUKO,
).with_creator(
    'Yóu yá yīn gōng / 由芽音功',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1220101427360169984/flandre-koishi-kiss-0000.png',
).with_action(
    ACTION_TAG_KISS, SCARLET_FLANDRE, KOMEIJI_KOISHI,
).with_creator(
    'calpis118 / Lpis26',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1223985953228591168/flandre-koishi-kiss-0001.png',
).with_action(
    ACTION_TAG_KISS, KOMEIJI_KOISHI, SCARLET_FLANDRE,
).with_creator(
    'dorowa (drawerslove)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1223985953857867787/flandre-koishi-kiss-0002.png',
).with_action(
    ACTION_TAG_KISS, KOMEIJI_KOISHI, SCARLET_FLANDRE,
).with_creator(
    'sorani (kaeru0768)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1232740729609261066/flandre-koishi-kiss-0003.png',
).with_action(
    ACTION_TAG_KISS, SCARLET_FLANDRE, KOMEIJI_KOISHI,
).with_creator(
    'sorani (kaeru0768)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1232740729944674345/flandre-koishi-kiss-0004.png',
).with_actions(
    (ACTION_TAG_KISS, SCARLET_FLANDRE, KOMEIJI_KOISHI),
    (ACTION_TAG_KISS, KOMEIJI_KOISHI, SCARLET_FLANDRE),
).with_creator(
    'sorani (kaeru0768)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1232740730292666368/flandre-koishi-kiss-0005.png',
).with_actions(
    (ACTION_TAG_KISS, SCARLET_FLANDRE, KOMEIJI_KOISHI),
    (ACTION_TAG_KISS, KOMEIJI_KOISHI, SCARLET_FLANDRE),
).with_creator(
    'busuneko',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1223978928780083331/flandre-meiling-remilia-sakuya-kiss-0000.png',
).with_action(
    ACTION_TAG_KISS, SCARLET_REMILIA, IZAYOI_SAKUYA,
).with_characters(
    SCARLET_FLANDRE, HONG_MEILING,
).with_creator(
    'doofuf',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1220251342149390427/kaguya-mokou-kiss-0000.png',
).with_action(
    ACTION_TAG_KISS, HOURAISAN_KAGUYA, FUJIWARA_NO_MOKOU,
).with_creator(
    'toobane',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1220255801436930078/kanako-sanae-kiss-0000.png',
).with_action(
    ACTION_TAG_KISS, YASAKA_KANAKO, KOCHIYA_SANAE,
).with_creator(
    'inaba',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1220254791570292898/kanako-sanae-sawuko-kiss-0000.png',
).with_actions(
    (ACTION_TAG_KISS, YASAKA_KANAKO, MORIYA_SUWAKO),
    (ACTION_TAG_KISS, MORIYA_SUWAKO, KOCHIYA_SANAE),
).with_creator(
    'orz (kagewaka)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1232738040825512047/kasen-komachi-kiss-0000.png',
).with_action(
    ACTION_TAG_KISS, IBARAKI_KASEN, ONOZUKA_KOMACHI,
).with_creator(
    'harusame (unmei no ikasumi)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1232735515577684079/keine-mokou-kiss-0000.png',
).with_action(
    ACTION_TAG_KISS, KAMISHIRASAWA_KEINE, FUJIWARA_NO_MOKOU,
).with_creator(
    'harusame (unmei no ikasumi)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1223989690118570044/koishi-kokoro-kiss-0000.png',
).with_action(
    ACTION_TAG_KISS, KOMEIJI_KOISHI, HATA_NO_KOKORO,
).with_creator(
    'ajia (otya3039)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1223989691016155156/koishi-kokoro-kiss-0002.png',
).with_action(
    ACTION_TAG_KISS, KOMEIJI_KOISHI, HATA_NO_KOKORO,
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1223989691334918185/koishi-kokoro-kiss-0003.png',
).with_actions(
    (ACTION_TAG_KISS, KOMEIJI_KOISHI, HATA_NO_KOKORO),
    (ACTION_TAG_KISS, HATA_NO_KOKORO, KOMEIJI_KOISHI),
).with_creator(
    'kiryuu soma',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1223989691770994718/koishi-kokoro-kiss-0004.png',
).with_actions(
    (ACTION_TAG_KISS, KOMEIJI_KOISHI, HATA_NO_KOKORO),
    (ACTION_TAG_KISS, HATA_NO_KOKORO, KOMEIJI_KOISHI),
).with_creator(
    'fub (fubimanji)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1223986286961098887/koishi-satori-kiss-0000.png',
).with_action(
    ACTION_TAG_KISS, KOMEIJI_KOISHI, KOMEIJI_SATORI,
).with_creator(
    'Narumi / 鳴海',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1223986287342653590/koishi-satori-kiss-0001.png',
).with_action(
    ACTION_TAG_KISS, KOMEIJI_KOISHI, KOMEIJI_SATORI,
).with_creator(
    'littlecloudie',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1232736399153954966/mamizou-ran-kisss-0000.png',
).with_action(
    ACTION_TAG_KISS, YAKUMO_RAN, FUTATSUIWA_MAMIZOU,
).with_creator(
    're ghotion',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1232741928832073825/maribel-renko-kiss-0000.png',
).with_action(
    ACTION_TAG_KISS, HEARN_MARIBEL, USAMI_RENKO,
).with_creator(
    'Echigo yaya / 越後やや',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1220250378562703371/marisa-patchouli-kiss-0000.png',
).with_actions(
    (ACTION_TAG_KISS, KIRISAME_MARISA, PATCHOULI_KNOWLEDGE),
    (ACTION_TAG_KISS, PATCHOULI_KNOWLEDGE, KIRISAME_MARISA),
).with_creator(
    'venusgenetrix',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1220247261976592494/marisa-reimu-kiss-0000.png',
).with_action(
    ACTION_TAG_KISS, HAKUREI_REIMU, KIRISAME_MARISA,
).with_creator(
    'sorairo porin',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1232744135073468416/marisa-reimu-kiss-0001.png',
).with_actions(
    (ACTION_TAG_KISS, HAKUREI_REIMU, KIRISAME_MARISA),
    (ACTION_TAG_KISS, KIRISAME_MARISA, HAKUREI_REIMU),
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1220255012069048320/marisa-sakuya-kiss-0000.png',
).with_action(
    ACTION_TAG_KISS, KIRISAME_MARISA, IZAYOI_SAKUYA,
).with_creator(
    'seita',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1220257838161461308/meiling-sakuya-kiss-0000.png',
).with_action(
    ACTION_TAG_KISS, HONG_MEILING, IZAYOI_SAKUYA,
).with_creator(
    'panmi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1223882100516720660/murasa-nue-kiss-0000.png',
).with_action(
    ACTION_TAG_KISS, MURASA_MINAMITSU, HOUJUU_NUE,
).with_creator(
    'soiri (us)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1223886680151298048/okuu-orin-kiss-0000.png',
).with_action(
    ACTION_TAG_KISS, REIUJI_UTSUHO, KAENBYOU_RIN,
).with_creators(
    'isaki (gomi)', 'serio (columns)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1223886681049006100/okuu-orin-kiss-0001.png',
).with_action(
    ACTION_TAG_KISS, REIUJI_UTSUHO, KAENBYOU_RIN,
).with_creator(
    'fukaiton',
).with_editor(
    'HuyaneMatsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1223889656362569728/orin-reimu-kiss-0000.png',
).with_action(
    ACTION_TAG_KISS, KAENBYOU_RIN, HAKUREI_REIMU,
).with_creator(
    'kiri futoshi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1232746386378719242/parsee-satori-kiss-0000.png',
).with_action(
    ACTION_TAG_KISS, KOMEIJI_SATORI, MIZUHASHI_PARSEE,
).with_creator(
    'ootsuki wataru',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1223976841182707762/ran-yukari-kiss-0000.png',
).with_action(
    ACTION_TAG_KISS, YAKUMO_YUKARI, YAKUMO_RAN,
).with_creator(
    'masanaga (tsukasa)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1223976842025767014/ran-yukari-kiss-0001.png',
).with_actions(
    (ACTION_TAG_KISS, YAKUMO_RAN, YAKUMO_YUKARI),
    (ACTION_TAG_KISS, YAKUMO_YUKARI, YAKUMO_RAN),
).with_creator(
    'masanaga (tsukasa)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1223978271197237308/remilia-sakuya-kiss-0000.png',
).with_action(
    ACTION_TAG_KISS, SCARLET_REMILIA, IZAYOI_SAKUYA,
).with_editor(
    'HuyaneMatsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1223982249142386719/remilia-satori-kiss-0000.png',
).with_action(
    ACTION_TAG_KISS, SCARLET_REMILIA, KOMEIJI_SATORI,
).with_editor(
    'HuyaneMatsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1220248539096027136/rinnosuke-sakuya-kiss-0000.png',
).with_action(
    ACTION_TAG_KISS, MORICHIKA_RINNOSUKE, IZAYOI_SAKUYA,
).with_creator(
    'lenahc',
).with_editor(
    'HuyaneMatsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1223980216804835360/suika-yukari-yuyuko-kiss-0000.png',
).with_actions(
    (ACTION_TAG_KISS, YAKUMO_YUKARI, SAIGYOUJI_YUYUKO),
    (ACTION_TAG_KISS, SAIGYOUJI_YUYUKO, YAKUMO_YUKARI),
).with_character(
    IBUKI_SUIKA,
).with_creator(
    'baozishark',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1223982548124831885/yukari-yuyuko-kiss-0000.png',
).with_actions(
    (ACTION_TAG_KISS, YAKUMO_YUKARI, SAIGYOUJI_YUYUKO),
    (ACTION_TAG_KISS, SAIGYOUJI_YUYUKO, YAKUMO_YUKARI),
).with_creator(
    'minust',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1149989579538038814/junko-kon-0000.png',
).with_action(
    ACTION_TAG_KON, JUNKO, None,
).with_creator(
    'moneti (daifuku) / monety / もねてぃ',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1150000049749774397/junko-kon-0001.png',
).with_action(
    ACTION_TAG_KON, JUNKO, None,
).with_creator(
    'teoi (good chaos)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1150000366818168902/junko-kon-0002.png',
).with_action(
    ACTION_TAG_KON, JUNKO, None,
).with_creator(
    'musteflott419',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1149991612550754344/kagerou-kon-0000.png',
).with_action(
    ACTION_TAG_KON, IMAIZUMI_KAGEROU, None,
).with_creator(
    'haruirokomici / もりのくろやぎ',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1149991612945010718/kagerou-kon-0001.png',
).with_action(
    ACTION_TAG_KON, IMAIZUMI_KAGEROU, None,
).with_creator(
    'misoshiru / みそしる',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1149989580406259793/momiji-kon-0000.png',
).with_action(
    ACTION_TAG_KON, INUBASHIRI_MOMIJI, None,
).with_creator(
    'hukahire0120',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1149989580792139836/momiji-kon-0001.png',
).with_action(
    ACTION_TAG_KON, INUBASHIRI_MOMIJI, None,
).with_creator(
    'risiyun',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1149989581555507320/momiji-kon-0002.png',
).with_action(
    ACTION_TAG_KON, INUBASHIRI_MOMIJI, None,
).with_creator(
    'miyabiii oekaki',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1150001216277971014/orin-tsukasa-kon-0000.png',
).with_actions(
    (ACTION_TAG_KON, KAENBYOU_RIN, None),
    (ACTION_TAG_KON, KUDAMAKI_TSUKASA, None),
).with_creator(
    'chups',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1149990026420162672/ran-kon-0000.png',
).with_action(
    ACTION_TAG_KON, YAKUMO_RAN, None,
).with_creator(
    'cube85',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1149990026868965466/ran-kon-0001.png',
).with_action(
    ACTION_TAG_KON, YAKUMO_RAN, None,
).with_creator(
    'asutoro (s--t) / あすとろ',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1149990027191931000/ran-kon-0002.png',
).with_action(
    ACTION_TAG_KON, YAKUMO_RAN, None,
).with_creator(
    'amano hagoromo / アマノ羽衣',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1149990027581984798/ran-kon-0003.png',
).with_action(
    ACTION_TAG_KON, YAKUMO_RAN, None,
).with_creator(
    'tsuru (nekopanchi)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1149990027938517075/ran-kon-0004.png',
).with_action(
    ACTION_TAG_KON, YAKUMO_RAN, None,
).with_creator(
    'raian macaroni',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1149990028253073418/ran-kon-0005.png',
).with_action(
    ACTION_TAG_KON, YAKUMO_RAN, None,
).with_creator(
    'saki (14793221)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1149990028676710440/ran-kon-0006.png',
).with_action(
    ACTION_TAG_KON, YAKUMO_RAN, None,
).with_creator(
    'gokuu (acoloredpencil) / ごくう',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1149990029196808253/ran-kon-0007.png',
).with_action(
    ACTION_TAG_KON, YAKUMO_RAN, None,
).with_creator(
    'koto (shiberia39) / 牧葉',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1149990041981042718/ran-kon-0008.png',
).with_action(
    ACTION_TAG_KON, YAKUMO_RAN, None,
).with_creator(
    'qqqrinkappp / Rinka',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1149990042358513714/ran-kon-0009.png',
).with_action(
    ACTION_TAG_KON, YAKUMO_RAN, None,
).with_creator(
    'maka (user rryf2748) / maka',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1149990042715045888/ran-kon-0010.png',
).with_action(
    ACTION_TAG_KON, YAKUMO_RAN, None,
).with_creator(
    'deal360acv',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1149990043843297320/ran-kon-0011.png',
).with_action(
    ACTION_TAG_KON, YAKUMO_RAN, None,
).with_creator(
    'sarasadou dan / 更紗灯弾',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1153368835492155532/ran-kon-0012.png',
).with_action(
    ACTION_TAG_KON, YAKUMO_RAN, None,
).with_creator(
    'rin falcon / ファルケン',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1163130820509311136/ran-kon-0013.png',
).with_action(
    ACTION_TAG_KON, YAKUMO_RAN, None,
).with_creator(
    'ashi / あ氏',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1163130820970692708/ran-kon-0014.png',
).with_action(
    ACTION_TAG_KON, YAKUMO_RAN, None,
).with_creator(
    'qqqrinkappp / Rinka',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1163130821553692773/ran-kon-0015.png',
).with_action(
    ACTION_TAG_KON, YAKUMO_RAN, None,
).with_creator(
    'safutsuguon / さふ亞おん',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1182991439857188915/ran-kon-0016.png',
).with_action(
    ACTION_TAG_KON, YAKUMO_RAN, None,
).with_creator(
    'vivo / vivoさん！',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1183495169702645810/ran-kon-0017.png',
).with_action(
    ACTION_TAG_KON, YAKUMO_RAN, None,
).with_creator(
    'ananna0031 / あんチャソ',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1183495170411466762/ran-kon-0018.png',
).with_action(
    ACTION_TAG_KON, YAKUMO_RAN, None,
).with_creator(
    'sarasadou dan / 更紗灯弾',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1183495171413913620/ran-kon-0019.png',
).with_action(
    ACTION_TAG_KON, YAKUMO_RAN, None,
).with_creator(
    'suwaneko / すわ猫',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1183495171988541470/ran-kon-0020.png',
).with_action(
    ACTION_TAG_KON, YAKUMO_RAN, None,
).with_creator(
    'deetamu / で～たむ',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1183495172286328842/ran-kon-0021.png',
).with_action(
    ACTION_TAG_KON, YAKUMO_RAN, None,
).with_creator(
    'kaiza1130 / カイザ閣下',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1183495173372661780/ran-kon-0022.png',
).with_action(
    ACTION_TAG_KON, YAKUMO_RAN, None,
).with_creator(
    'masanaga / 政長',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1183495174018568223/ran-kon-0023.png',
).with_action(
    ACTION_TAG_KON, YAKUMO_RAN, None,
).with_creator(
    'surumeri / するめり',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1183495174534475907/ran-kon-0024.png',
).with_action(
    ACTION_TAG_KON, YAKUMO_RAN, None,
).with_creator(
    'kawayabug / かわやばぐ',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1201178154455289856/ran-kon-0025.png',
).with_action(
    ACTION_TAG_KON, YAKUMO_RAN, None,
).with_creator(
    'nyong nyong',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1206154952599281734/ran-kon-0026.png',
).with_action(
    ACTION_TAG_KON, YAKUMO_RAN, None,
).with_creator(
    'alto2019',
).with_editor(
    'HuyaneMatsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1201619756164325626/ran-kon-0027.png',
).with_action(
    ACTION_TAG_KON, YAKUMO_RAN, None,
).with_creator(
    'mirufui',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1201619756873166969/ran-kon-0028.png',
).with_action(
    ACTION_TAG_KON, YAKUMO_RAN, None,
).with_creator(
    'kanaria (bocmn)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1201985356954878002/ran-kon-0029.png',
).with_action(
    ACTION_TAG_KON, YAKUMO_RAN, None,
).with_creator(
    'nekurodayo',
).with_editor(
    'HuyaneMatsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1201985357546262618/ran-kon-0030.png',
).with_action(
    ACTION_TAG_KON, YAKUMO_RAN, None,
).with_creator(
    'matsukuzu',
).with_editor(
    'HuyaneMatsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1201985358494191706/ran-kon-0031.png',
).with_action(
    ACTION_TAG_KON, YAKUMO_RAN, None,
).with_creator(
    'gokuu / ごくう',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1205981665374109816/ran-kon-0032.png',
).with_action(
    ACTION_TAG_KON, YAKUMO_RAN, None,
).with_creator(
    'kiritanpo117',
).with_editor(
    'HuyaneMatsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1213440394717691934/ran-kon-0033.png',
).with_action(
    ACTION_TAG_KON, YAKUMO_RAN, None,
).with_creator(
    'kakone',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1232772387989225522/ran-kon-0034.png',
).with_action(
    ACTION_TAG_KON, YAKUMO_RAN, None,
).with_creator(
    'neko bocchi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1149990400476598332/tsukasa-kon-0000.png',
).with_action(
    ACTION_TAG_KON, KUDAMAKI_TSUKASA, None,
).with_creator(
    'asuzemu / あすぜむ',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1149990400849887323/tsukasa-kon-0001.png',
).with_action(
    ACTION_TAG_KON, KUDAMAKI_TSUKASA, None,
).with_creator(
    'mata (matasoup)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1149990401160269884/tsukasa-kon-0002.png',
).with_action(
    ACTION_TAG_KON, KUDAMAKI_TSUKASA, None,
).with_creator(
    'formicid',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1149990401483227158/tsukasa-kon-0003.png',
).with_action(
    ACTION_TAG_KON, KUDAMAKI_TSUKASA, None,
).with_creator(
    'sen (daydream 53 / センチョリス)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1149990401902661713/tsukasa-kon-0004.png',
).with_action(
    ACTION_TAG_KON, KUDAMAKI_TSUKASA, None,
).with_creator(
    'harakune (mugennero) / ハラクネ',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1149990402405974116/tsukasa-kon-0005.png',
).with_action(
    ACTION_TAG_KON, KUDAMAKI_TSUKASA, None,
).with_creator(
    'e.o. / EO',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1149990402921865286/tsukasa-kon-0006.png',
).with_action(
    ACTION_TAG_KON, KUDAMAKI_TSUKASA, None,
).with_creator(
    'yuha (kanayuzu611) / 柚葉',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1149990403337113640/tsukasa-kon-0007.png',
).with_action(
    ACTION_TAG_KON, KUDAMAKI_TSUKASA, None,
).with_creator(
    'mizore arius / 薄氷 霙',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1149990403706208276/tsukasa-kon-0008.png',
).with_action(
    ACTION_TAG_KON, KUDAMAKI_TSUKASA, None,
).with_creator(
    'mame komari / まめ助',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1149990404117241947/tsukasa-kon-0009.png',
).with_action(
    ACTION_TAG_KON, KUDAMAKI_TSUKASA, None,
).with_creator(
    'lennonrine / レノン',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1149990425449472111/tsukasa-kon-0010.png',
).with_action(
    ACTION_TAG_KON, KUDAMAKI_TSUKASA, None,
).with_creator(
    'e sdss / 墨山スイ',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1149990425902452746/tsukasa-kon-0011.png',
).with_action(
    ACTION_TAG_KON, KUDAMAKI_TSUKASA, None,
).with_creator(
    'yoriteruru / 依神てるぽ',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1149990426296729610/tsukasa-kon-0012.png',
).with_action(
    ACTION_TAG_KON, KUDAMAKI_TSUKASA, None,
).with_creator(
    'mizore arius / 薄氷 霙',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1149990426699370639/tsukasa-kon-0013.png',
).with_action(
    ACTION_TAG_KON, KUDAMAKI_TSUKASA, None,
).with_creator(
    'qqqrinkappp / Rinka',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1149990427068481536/tsukasa-kon-0014.png',
).with_action(
    ACTION_TAG_KON, KUDAMAKI_TSUKASA, None,
).with_creator(
    'neko mata / ぢょん',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1149990427513069568/tsukasa-kon-0015.png',
).with_action(
    ACTION_TAG_KON, KUDAMAKI_TSUKASA, None,
).with_creator(
    'tantalum / タンタル',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1149990427877969960/tsukasa-kon-0016.png',
).with_action(
    ACTION_TAG_KON, KUDAMAKI_TSUKASA, None,
).with_creator(
    'toku kekakewanko / 葉鶏(ばとり)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1149990428351930409/tsukasa-kon-0017.png',
).with_action(
    ACTION_TAG_KON, KUDAMAKI_TSUKASA, None,
).with_creator(
    'nemachi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1160533157175623680/tsukasa-kon-0018.gif',
).with_action(
    ACTION_TAG_KON, KUDAMAKI_TSUKASA, None,
).with_creator(
    'furumero',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1160533130772480020/tsukasa-kon-0019.gif',
).with_action(
    ACTION_TAG_KON, KUDAMAKI_TSUKASA, None,
).with_creator(
    'gyouza',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1191083310911336520/tsukasa-kon-0020.png',
).with_action(
    ACTION_TAG_KON, KUDAMAKI_TSUKASA, None,
).with_creator(
    'makita (vector1525)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1223570385669460088/tsukasa-kon-0021.png',
).with_action(
    ACTION_TAG_KON, KUDAMAKI_TSUKASA, None,
).with_creator(
    'mizore arius',
).with_editor(
    'HuyaneMatsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1232772388421111870/tsukasa-kon-0022.png',
).with_action(
    ACTION_TAG_KON, KUDAMAKI_TSUKASA, None,
).with_creator(
    'chunjiu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1242171305176858624/ran-tsukasa-cosplay-kon-0000.png',
).with_actions(
    (ACTION_TAG_COSPLAY, KUDAMAKI_TSUKASA, YAKUMO_RAN),
    (ACTION_TAG_KON, KUDAMAKI_TSUKASA, None),
).with_creator(
    'fe (tetsu)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1242171305688825917/ran-tsukasa-cosplay-kon-0001.png',
).with_actions(
    (ACTION_TAG_COSPLAY, KUDAMAKI_TSUKASA, YAKUMO_RAN),
    (ACTION_TAG_KON, KUDAMAKI_TSUKASA, None),
).with_creator(
    'e.o.',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1149990428771356723/youmu-kon-0000.png',
).with_action(
    ACTION_TAG_KON, KONPAKU_YOUMU, None,
).with_creator(
    'momomaron / ももまろん',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1220249768958103623/alice-marisa-lick-0000.png',
).with_action(
    ACTION_TAG_LICK, KIRISAME_MARISA, MARGATROID_ALICE,
).with_creator(
    'pman',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1220456643746332732/alice-marisa-lick-0001.png',
).with_action(
    ACTION_TAG_LICK, KIRISAME_MARISA, MARGATROID_ALICE,
).with_creator(
    'alm',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1220457105983668334/alice-marisa-lick-0002.png',
).with_action(
    ACTION_TAG_LICK, KIRISAME_MARISA, MARGATROID_ALICE,
).with_creator(
    'nanase nao',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1220461916850229328/alice-marisa-lick-0003.png',
).with_action(
    ACTION_TAG_LICK, MARGATROID_ALICE, KIRISAME_MARISA,
).with_creator(
    'imokototaisi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1220465512753135636/alice-marisa-lick-0004.png',
).with_action(
    ACTION_TAG_LICK, KIRISAME_MARISA, MARGATROID_ALICE,
).with_creator(
    'yatomi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1220472322280919040/alice-marisa-lick-0005.png',
).with_action(
    ACTION_TAG_LICK, KIRISAME_MARISA, MARGATROID_ALICE,
).with_creator(
    'yoglasses',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1220454403929145384/alice-sakuya-lick-0000.png',
).with_action(
    ACTION_TAG_LICK, IZAYOI_SAKUYA, MARGATROID_ALICE,
).with_creator(
    'sen\'yuu yuuji',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1220459457910280282/aya-momiji-lick-0000.png',
).with_action(
    ACTION_TAG_LICK, SHAMEIMARU_AYA, INUBASHIRI_MOMIJI,
).with_creator(
    'arashiya',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1232771079823687680/chen-orin-lick-0000.png',
).with_action(
    ACTION_TAG_LICK, CHEN, KAENBYOU_RIN,
).with_creator(
    'masanaga (tsukasa)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1220464815160692746/chiruno-letty-lick-0000.png',
).with_action(
    ACTION_TAG_LICK, CHIRUNO, LETTY_WHITEROCK,
).with_creator(
    'hirosato',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1220466426335203470/flandre-marisa-lick-0000.png',
).with_action(
    ACTION_TAG_LICK, SCARLET_FLANDRE, KIRISAME_MARISA,
).with_creator(
    'manekinukotei',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1220455885781074060/keine-mokou-lick-0000.png',
).with_action(
    ACTION_TAG_LICK, KAMISHIRASAWA_KEINE, FUJIWARA_NO_MOKOU,
).with_creator(
    'unabara misumi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1220469241799774358/kogasa-sanae-lick-0000.png',
).with_action(
    ACTION_TAG_LICK, KOCHIYA_SANAE, TATARA_KOGASA,
).with_creator(
    'ichimi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1220457675918409738/kogasa-yuuka-wriggle-lick-0000.png',
).with_action(
    ACTION_TAG_LICK, TATARA_KOGASA, KAZAMI_YUUKA,
).with_character(
    WRIGGLE_NIGHTBUG,
).with_creator(
    'kong xian',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1220471608511303720/koishi-satori-lick-0000.png',
).with_action(
    ACTION_TAG_LICK, KOMEIJI_KOISHI, KOMEIJI_SATORI,
).with_creators(
    'eromame', 'saya26',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1220473492307316858/koishi-satori-lick-0001.png',
).with_action(
    ACTION_TAG_LICK, KOMEIJI_KOISHI, KOMEIJI_SATORI,
).with_creator(
    'kuromari (runia)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1220468448606294146/marisa-orin-reimu-lick-0000.png',
).with_action(
    ACTION_TAG_LICK, KAENBYOU_RIN, HAKUREI_REIMU,
).with_character(
    KIRISAME_MARISA,
).with_creator(
    'nakatani',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1220474336243089508/marisa-yukari-lick-0000.png',
).with_action(
    ACTION_TAG_LICK, YAKUMO_YUKARI, KIRISAME_MARISA,
).with_creator(
    'torinone',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1220463488355532881/orin-satori-lick-0000.png',
).with_action(
    ACTION_TAG_LICK, KAENBYOU_RIN, KOMEIJI_SATORI,
).with_creator(
    'toobane',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1220460308708069547/parsee-yuugi-lick-0000.png',
).with_action(
    ACTION_TAG_LICK, HOSHIGUMA_YUUGI, MIZUHASHI_PARSEE,
).with_creator(
    'atoki',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1220462891749347389/ran-yukari-lick-0000.png',
).with_action(
    ACTION_TAG_LICK, YAKUMO_RAN, YAKUMO_YUKARI,
).with_creator(
    'ayase hazuki',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1220473197837942905/reisen-tewi-lick-0000.png',
).with_action(
    ACTION_TAG_LICK, INABA_TEWI, REISEN_UDONGEIN_INABA,
).with_creator(
    'kisaragiya',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1220470441496285246/reisen-youmu-lick-0000.png',
).with_action(
    ACTION_TAG_LICK, REISEN_UDONGEIN_INABA, KONPAKU_YOUMU,
).with_creator(
    'akachuu no gema',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1220458555795050646/rumia-youmu-lick-0000.png',
).with_action(
    ACTION_TAG_LICK, RUMIA, KONPAKU_YOUMU,
).with_creator(
    'hinoryu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1220467953930342521/youmu-yuyuko-lick-0000.png',
).with_action(
    ACTION_TAG_LICK, SAIGYOUJI_YUYUKO, KONPAKU_YOUMU,
).with_creator(
    'k0n3k0',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1220475197010739260/youmu-yuyuko-lick-0001.png',
).with_action(
    ACTION_TAG_LICK, SAIGYOUJI_YUYUKO, KONPAKU_YOUMU,
).with_creator(
    'nyorumachi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1220471071661232168/yukari-yuyuko-lick-0000.png',
).with_action(
    ACTION_TAG_LICK, SAIGYOUJI_YUYUKO, YAKUMO_YUKARI,
).with_creator(
    'yoicha',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1141454561253523527/eiki-judged-0000.png',
).with_action(
    ACTION_TAG_LIKE, None, SHIKI_EIKI_YAMAXANADU,
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1119683125082062958/eirin-older-0000.png',
).with_action(
    ACTION_TAG_LIKE, None, YAGOKORO_EIRIN,
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1232790794923020411/eirin-older-0001.png',
).with_action(
    ACTION_TAG_LIKE, None, YAGOKORO_EIRIN,
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1119683125367296040/futatsuiwa-older-0000.png',
).with_action(
    ACTION_TAG_LIKE, None, FUTATSUIWA_MAMIZOU,
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1141454561891074128/hisami-grape-0000.png',
).with_action(
    ACTION_TAG_LIKE, None, YOMOTSU_HISAMI,
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1141454562260156529/hisami-older-0000.png',
).with_action(
    ACTION_TAG_LIKE, None, YOMOTSU_HISAMI,
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1213438771807264850/iku-older-0000.png',
).with_action(
    ACTION_TAG_LIKE, None, NAGAE_IKU,
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1119683125719601244/junko-older-0000.png',
).with_action(
    ACTION_TAG_LIKE, None, JUNKO,
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1119683126352937051/junko-older-0001.png',
).with_action(
    ACTION_TAG_LIKE, None, JUNKO,
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1160526086963212358/junko-older-0002.png',
).with_action(
    ACTION_TAG_LIKE, None, JUNKO,
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1119683126713667756/junko-racist-0000.png',
).with_action(
    ACTION_TAG_LIKE, None, JUNKO,
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1232733282597208174/kasen-oder-0000.png',
).with_action(
    ACTION_TAG_LIKE, None, IBARAKI_KASEN,
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1141454561563914250/kogasa-umbrella-0000.png',
).with_action(
    ACTION_TAG_LIKE, None, TATARA_KOGASA,
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1119683127049195590/koishi-happy-0000.png',
).with_action(
    ACTION_TAG_LIKE, None, KOMEIJI_KOISHI,
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1223308356111040653/miko-older-0000.png',
).with_action(
    ACTION_TAG_LIKE, None, TOYOSATOMIMI_NO_MIKO,
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1232733283100528700/nitori-smart-0000.png',
).with_action(
    ACTION_TAG_LIKE, None, KAWASHIRO_NITORI,
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1132645810635550830/nue-huge-surprises-0000.png',
).with_action(
    ACTION_TAG_LIKE, None, HOUJUU_NUE,
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1149730972707856464/rinnosuke-plain-0000.png',
).with_action(
    ACTION_TAG_LIKE, None, MORICHIKA_RINNOSUKE,
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1141454560917995611/okina-older-0000.png',
).with_action(
    ACTION_TAG_LIKE, None, MATARA_OKINA,
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1202732810818027571/okuu-nuclear-0000.png',
).with_action(
    ACTION_TAG_LIKE, None, REIUJI_UTSUHO,
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1132645810908176414/ran-fluffy-tail-0000.png',
).with_action(
    ACTION_TAG_LIKE, None, YAKUMO_RAN,
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1232790795405230202/ran-older-0000.png',
).with_action(
    ACTION_TAG_LIKE, None, YAKUMO_RAN,
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1119683127468621824/rumia-older-0000.png',
).with_action(
    ACTION_TAG_LIKE, None, RUMIA,
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1119683127825158194/seiga-evil-0000.png',
).with_action(
    ACTION_TAG_LIKE, None, KAKU_SEIGA,
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1119683128181653566/seiga-older-0000.png',
).with_action(
    ACTION_TAG_LIKE, None, KAKU_SEIGA,
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1124044845602848768/tewi-older-0000.png',
).with_action(
    ACTION_TAG_LIKE, None, INABA_TEWI,
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1119683128563355668/yukari-japanese-goblin-0000.png',
).with_action(
    ACTION_TAG_LIKE, None, YAKUMO_YUKARI,
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1119683102290231336/yukari-older-0000.png',
).with_action(
    ACTION_TAG_LIKE, None, YAKUMO_YUKARI,
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1119683102860648569/yukari-older-0001.png',
).with_action(
    ACTION_TAG_LIKE, None, YAKUMO_YUKARI,
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1119683103267500143/yukari-older-0002.png',
).with_action(
    ACTION_TAG_LIKE, None, YAKUMO_YUKARI,
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1119683103737258044/yukari-older-0003.png',
).with_action(
    ACTION_TAG_LIKE, None, YAKUMO_YUKARI,
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1119683104106360922/yukari-older-0004.png',
).with_action(
    ACTION_TAG_LIKE, None, YAKUMO_YUKARI,
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1119683104571932692/yukari-older-0005.png',
).with_action(
    ACTION_TAG_LIKE, None, YAKUMO_YUKARI,
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1119683104991354941/yukari-older-0006.png',
).with_action(
    ACTION_TAG_LIKE, None, YAKUMO_YUKARI,
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1124044846064214138/yukari-yuyuko-older-0000.png',
).with_actions(
    (ACTION_TAG_LIKE, None, YAKUMO_YUKARI),
    (ACTION_TAG_LIKE, None, SAIGYOUJI_YUYUKO),
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1141454560620195952/yuuka-cbt-0000.png',
).with_action(
    ACTION_TAG_LIKE, None, KAZAMI_YUUKA,
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1119683105435955271/yuuka-older-0000.png',
).with_action(
    ACTION_TAG_LIKE, None, KAZAMI_YUUKA,
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1119683105809244282/yuyuko-older-0000.png',
).with_action(
    ACTION_TAG_LIKE, None, SAIGYOUJI_YUYUKO,
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1119683106320957561/yuyuko-older-0001.png',
).with_action(
    ACTION_TAG_LIKE, None, SAIGYOUJI_YUYUKO,
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1232732235858182195/yuyuko-older-0002.png',
).with_action(
    ACTION_TAG_LIKE, None, SAIGYOUJI_YUYUKO,
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1232732236848173116/yuyuko-older-0003.png',
).with_action(
    ACTION_TAG_LIKE, None, SAIGYOUJI_YUYUKO,
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1220485700319838328/alice-reimu-pat-0000.png',
).with_action(
    ACTION_TAG_PAT, MARGATROID_ALICE, HAKUREI_REIMU,
).with_creator(
    'natsuk',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1220478088601800714/aya-momiji-pat-0000.png',
).with_action(
    ACTION_TAG_PAT, SHAMEIMARU_AYA, INUBASHIRI_MOMIJI,
).with_creator(
    'yurusuke',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1220484187769798676/aya-momiji-pat-0001.png',
).with_action(
    ACTION_TAG_PAT, SHAMEIMARU_AYA, INUBASHIRI_MOMIJI,
).with_creator(
    'sao (0060)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1220487826039246959/chen-ran-pat-0000.png',
).with_action(
    ACTION_TAG_PAT, YAKUMO_RAN, CHEN,
).with_creator(
    'yudofu',
).with_editor(
    'HuyaneMatsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1220490334103011420/chen-ran-pat-0001.png',
).with_action(
    ACTION_TAG_PAT, YAKUMO_RAN, CHEN,
).with_creator(
    'shirosato',
).with_editor(
    'HuyaneMatsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1223524331145924648/chen-ran-pat-0002.png',
).with_action(
    ACTION_TAG_PAT, YAKUMO_RAN, CHEN,
).with_creator(
    'Shimizu Pemu / 清水ペム',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1232760095473930290/chen-ran-pat-0003.png',
).with_action(
    ACTION_TAG_PAT, YAKUMO_RAN, CHEN,
).with_creator(
    'chahan (fried rice0614)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1223527236238442597/chiurno-pat-0000.gif',
).with_action(
    ACTION_TAG_PAT, None, CHIRUNO,
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1220491614573826058/clownpiece-hecatia-pat-0000.png',
).with_action(
    ACTION_TAG_PAT, HECATIA_LAPISLAZULI, CLOWNPIECE,
).with_creator(
    'ori (yellow duckling)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1220478887054540800/dai-pat-0000.png',
).with_action(
    ACTION_TAG_PAT, None, DAIYOUSEI,
).with_creator(
    'kenntairui / kirino souya',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1223307489181958335/flandre-hmiko-pat-0000.png',
).with_action(
    ACTION_TAG_PAT, HAKUREI_MIKO, SCARLET_FLANDRE,
).with_creator(
    'yagami (mukage)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1220484865745621012/hatate-pat-0000.png',
).with_action(
    ACTION_TAG_PAT, None, HIMEKAIDOU_HATATE,
).with_creator(
    'gaoo (frpjx283)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1220499155844337774/hijiri-kyouko-pat-0000.png',
).with_action(
    ACTION_TAG_PAT, HIJIRI_BYAKUREN, KASODANI_KYOUKO,
).with_creator(
    'mikan imo',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1220490545772888124/hijiri-nue-pat-0000.png',
).with_action(
    ACTION_TAG_PAT, HIJIRI_BYAKUREN, HOUJUU_NUE,
).with_creator(
    'e.o.',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1220483214452457572/hina-parsee-pat-0000.png',
).with_action(
    ACTION_TAG_PAT, KAGIYAMA_HINA, MIZUHASHI_PARSEE,
).with_creator(
    'enkoko',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1223307488863060008/hmiko-reimu-yukari-pat-0000.png',
).with_actions(
    (ACTION_TAG_PAT, HAKUREI_MIKO, HAKUREI_REIMU),
    (ACTION_TAG_PAT, YAKUMO_YUKARI, HAKUREI_REIMU),
).with_creator(
    'aosiro-michi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1220490850174243016/kaguya-reisen-pat-0000.png',
).with_action(
    ACTION_TAG_PAT, HOURAISAN_KAGUYA, REISEN_UDONGEIN_INABA,
).with_creator(
    'milfy oira',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1220481124992552980/keine-mokou-pat-0000.png',
).with_action(
    ACTION_TAG_PAT, KAMISHIRASAWA_KEINE, FUJIWARA_NO_MOKOU,
).with_creator(
    'rain lan',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1223527844140027904/koishi-orin-satori-pat-0000.gif',
).with_actions(
    (ACTION_TAG_PAT, KOMEIJI_SATORI, KOMEIJI_KOISHI),
    (ACTION_TAG_PAT, KOMEIJI_KOISHI, KAENBYOU_RIN),
).with_creator(
    'satori suki',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1223311829128839269/koishi-pat-0000.png',
).with_action(
    ACTION_TAG_PAT, None, KOMEIJI_KOISHI,
).with_creator(
    'Narumi / 鳴海',
).with_editor(
    'HuyaneMatsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1223522925756416000/koishi-pat-0001.png',
).with_action(
    ACTION_TAG_PAT, None, KOMEIJI_KOISHI,
).with_creator(
    'heripantomorrow',
).with_editor(
    'HuyaneMatsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1223523971136356373/koishi-pat-0002.png',
).with_action(
    ACTION_TAG_PAT, None, KOMEIJI_KOISHI,
).with_editor(
    'HuyaneMatsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1220480274861785148/mamizou-nue-pat-0000.png',
).with_action(
    ACTION_TAG_PAT, FUTATSUIWA_MAMIZOU, HOUJUU_NUE,
).with_creator(
    'verderayo',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1223311004818079867/marisa-pat-0000.png',
).with_action(
    ACTION_TAG_PAT, None, KIRISAME_MARISA,
).with_creator(
    'mukkushi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1223530588611284992/orin-pat-0000.png',
).with_action(
    ACTION_TAG_PAT, None, KAENBYOU_RIN,
).with_creator(
    'renka (sutegoma25)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1223309868082135170/orin-satori-pat-0000.png',
).with_action(
    ACTION_TAG_PAT, KOMEIJI_SATORI, KAENBYOU_RIN,
).with_creator(
    'renka (sutegoma25)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1220498038850715779/parsee-pat-0000.png',
).with_action(
    ACTION_TAG_PAT, None, MIZUHASHI_PARSEE,
).with_creator(
    'bebeneko',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1223526207543443486/parsee-yuugi-pat-0000.png',
).with_action(
    ACTION_TAG_PAT, HOSHIGUMA_YUUGI, MIZUHASHI_PARSEE,
).with_creator(
    'sanomaki',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1220489732346085376/reimu-pat-0000.png',
).with_action(
    ACTION_TAG_PAT, HAKUREI_REIMU, HAKUREI_REIMU,
).with_creator(
    'kirero',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1220486953707765770/reimu-yukari-pat-0000.png',
).with_action(
    ACTION_TAG_PAT, YAKUMO_YUKARI, HAKUREI_REIMU,
).with_creator(
    'natsuk',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1220492733462876270/rumia-pat-0000.png',
).with_action(
    ACTION_TAG_PAT, None, RUMIA,
).with_creator(
    'shinekalta',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1220479886460977182/suika-yuugi-pat-0000.png',
).with_action(
    ACTION_TAG_PAT, HOSHIGUMA_YUUGI, IBUKI_SUIKA,
).with_creator(
    'suna (sunaipu)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1220477581795786752/suwako-pat-0000.png',
).with_action(
    ACTION_TAG_PAT, None, MORIYA_SUWAKO,
).with_creator(
    'kujira-kousen',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1220479334934904943/youmu-yuyuko-pat-0000.png',
).with_action(
    ACTION_TAG_PAT, SAIGYOUJI_YUYUKO, KONPAKU_YOUMU,
).with_creator(
    'rai',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1155211020483174470/akyuu-kosuzu-pocky-0000.png',
).with_actions(
    (ACTION_TAG_POCKY_KISS, HIEDA_NO_AKYUU, MOTOORI_KOSUZU),
    (ACTION_TAG_POCKY_KISS, MOTOORI_KOSUZU, HIEDA_NO_AKYUU),
).with_creator(
    'nekolina',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1223995355973156985/alice-marisa-pocky-0000.png',
).with_actions(
    (ACTION_TAG_POCKY_KISS, KIRISAME_MARISA, MARGATROID_ALICE),
    (ACTION_TAG_POCKY_KISS, MARGATROID_ALICE, KIRISAME_MARISA),
).with_creator(
    'manjuu teishoku / 饅頭定食',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1223996169852686377/alice-mystia-pocky-0000.png',
).with_actions(
    (ACTION_TAG_POCKY_KISS, MYSTIA_LORELEI, MARGATROID_ALICE),
    (ACTION_TAG_POCKY_KISS, MARGATROID_ALICE, MYSTIA_LORELEI),
).with_creator(
    'ayagi daifuku',
).with_editor(
    'HuyaneMatsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1223993131884609596/aya-hatate-pocky-0000.png',
).with_actions(
    (ACTION_TAG_POCKY_KISS, HIMEKAIDOU_HATATE, SHAMEIMARU_AYA),
    (ACTION_TAG_POCKY_KISS, SHAMEIMARU_AYA, HIMEKAIDOU_HATATE),
).with_creator(
    'coco (r5m)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1155416757964640266/aya-remilia-pocky-0000.png',
).with_action(
    ACTION_TAG_POCKY_KISS, SCARLET_REMILIA, SHAMEIMARU_AYA,
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1155417439706824734/chen-orin-pocky-0000.png',
).with_actions(
    (ACTION_TAG_POCKY_KISS, CHEN, KAENBYOU_RIN),
    (ACTION_TAG_POCKY_KISS, KAENBYOU_RIN, CHEN),
).with_creator(
    'fujimiya kikyou / 藤見屋桔梗',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1155418080961368074/chen-ran-pocky-0000.png',
).with_action(
    ACTION_TAG_POCKY_KISS, CHEN, YAKUMO_RAN,
).with_creator(
    'gustav / ぐすたふ',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1223997595039567882/chen-ran-pocky-0001.png',
).with_actions(
    (ACTION_TAG_POCKY_KISS, YAKUMO_RAN, CHEN),
    (ACTION_TAG_POCKY_KISS, CHEN, YAKUMO_RAN),
).with_creator(
    'japa / じゃぱ',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1223997595391754260/chen-ran-pocky-0002.png',
).with_action(
    ACTION_TAG_POCKY_KISS, CHEN, YAKUMO_RAN,
).with_creator(
    'japa / じゃぱ',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1155418521304563732/chiruno-dai-pocky-0000.png',
).with_actions(
    (ACTION_TAG_POCKY_KISS, CHIRUNO, DAIYOUSEI),
    (ACTION_TAG_POCKY_KISS, DAIYOUSEI, CHIRUNO),
).with_creator(
    'mamemochi / まめもち',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1224002839488106577/chiruno-rumia-pocky-0000.png',
).with_action(
    ACTION_TAG_POCKY_KISS, CHIRUNO, RUMIA,
).with_creator(
    'torichiyo / とりちよ',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1236210240312180816/flandre-koishi-remilia-satori-pocky-0000.png',
).with_actions(
    (ACTION_TAG_POCKY_KISS, KOMEIJI_KOISHI, SCARLET_FLANDRE),
    (ACTION_TAG_POCKY_KISS, SCARLET_FLANDRE, KOMEIJI_KOISHI),
).with_characters(
    SCARLET_REMILIA, KOMEIJI_SATORI,
).with_creator(
    'minamura haruki / 皆 村',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1223993460541882378/flandre-koishi-pocky-0001.png',
).with_action(
    ACTION_TAG_POCKY_KISS, KOMEIJI_KOISHI, SCARLET_FLANDRE,
).with_creator(
    'Teeku / てぇく',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1223993460865110076/flandre-koishi-pocky-0002.png',
).with_action(
    ACTION_TAG_POCKY_KISS, KOMEIJI_KOISHI, SCARLET_FLANDRE,
).with_creator(
    'shan',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1155419036797124628/flandre-remilia-pocky-0000.png',
).with_action(
    ACTION_TAG_POCKY_KISS, SCARLET_FLANDRE, SCARLET_REMILIA,
).with_creator(
    'sakrear',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1155419380402892880/flandre-remilia-pocky-0001.png',
).with_action(
    ACTION_TAG_POCKY_KISS, SCARLET_FLANDRE, SCARLET_REMILIA,
).with_creator(
    'sakrear',
).with_editor(
    'Scarlet Flandre',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1224001610129342636/flandre-remilia-pocky-0002.png',
).with_action(
    ACTION_TAG_POCKY_KISS, SCARLET_FLANDRE, SCARLET_REMILIA,
).with_creator(
    'fumi11',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1224001610565292133/flandre-remilia-pocky-0003.png',
).with_action(
    ACTION_TAG_POCKY_KISS, SCARLET_FLANDRE, SCARLET_REMILIA,
).with_creator(
    'kusogappa',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1155420220245155850/kagerou-remilia-pocky-0000.png',
).with_actions(
    (ACTION_TAG_POCKY_KISS, IMAIZUMI_KAGEROU, SCARLET_REMILIA),
    (ACTION_TAG_POCKY_KISS, SCARLET_REMILIA, IMAIZUMI_KAGEROU),
).with_creator(
    'ziran de ph shizhi tuan / 自燃的ph试纸团',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1224000873089339552/kagerou-wakasagihime-pocky-0000.png',
).with_action(
    ACTION_TAG_POCKY_KISS, WAKASAGIHIME, IMAIZUMI_KAGEROU,
).with_creator(
    'kaginoni / かぎのに',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1224004869220728912/kanako-suwako-pocky-0000.png',
).with_action(
    ACTION_TAG_POCKY_KISS, MORIYA_SUWAKO, YASAKA_KANAKO,
).with_creator(
    'keemoringo',
).with_editor(
    'HuyaneMatsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1155420854105157742/keine-mokou-pocky-0000.png',
).with_actions(
    (ACTION_TAG_POCKY_KISS, KAMISHIRASAWA_KEINE, FUJIWARA_NO_MOKOU),
    (ACTION_TAG_POCKY_KISS, FUJIWARA_NO_MOKOU, KAMISHIRASAWA_KEINE),
).with_creator(
    'zawameki / ざわめき',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1155421417085603850/keine-mokou-pocky-0001.png',
).with_action(
    ACTION_TAG_POCKY_KISS, FUJIWARA_NO_MOKOU, KAMISHIRASAWA_KEINE,
).with_creator(
    'hijikawa arashi / 肱川 嵐',
).with_editor(
    'HuyaneMatsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1223995601637609512/keine-mokou-pocky-0002.png',
).with_action(
    ACTION_TAG_POCKY_KISS, FUJIWARA_NO_MOKOU, KAMISHIRASAWA_KEINE,
).with_creator(
    '6',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1224003250492018698/koakuma-sakuya-pocky-0000.png',
).with_action(
    ACTION_TAG_POCKY_KISS, IZAYOI_SAKUYA, KOAKUMA,
).with_creator(
    '3692materia / 浅間清正',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1223996582148571277/kogasa-nue-pocky-0000.png',
).with_actions(
    (ACTION_TAG_POCKY_KISS, HOUJUU_NUE, TATARA_KOGASA),
    (ACTION_TAG_POCKY_KISS, TATARA_KOGASA, HOUJUU_NUE),
).with_creator(
    'kitano / きたの！',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1155423779367944242/koishi-kokoro-pocky-0000.png',
).with_action(
    ACTION_TAG_POCKY_KISS, KOMEIJI_KOISHI, HATA_NO_KOKORO,
).with_creator(
    'cato',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1223992298376007750/koishi-kokoro-pocky-0001.png',
).with_actions(
    (ACTION_TAG_POCKY_KISS, KOMEIJI_KOISHI, HATA_NO_KOKORO),
    (ACTION_TAG_POCKY_KISS, HATA_NO_KOKORO, KOMEIJI_KOISHI),
).with_creator(
    'kiryuu soma',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1223994561941209089/koishi-kokoro-pocky-0002.png',
).with_actions(
    (ACTION_TAG_POCKY_KISS, HATA_NO_KOKORO, KOMEIJI_KOISHI),
    (ACTION_TAG_POCKY_KISS, KOMEIJI_KOISHI, HATA_NO_KOKORO),
).with_creator(
    'Zan / ざん',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1155424037099544632/koishi-satori-pocky-0000.png',
).with_action(
    ACTION_TAG_POCKY_KISS, KOMEIJI_KOISHI, KOMEIJI_SATORI,
).with_creator(
    'komaku juushoku / 鼓膜住職',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1155424507054530600/koishi-satori-pocky-0001.png',
).with_actions(
    (ACTION_TAG_POCKY_KISS, KOMEIJI_KOISHI, KOMEIJI_SATORI),
    (ACTION_TAG_POCKY_KISS, KOMEIJI_SATORI, KOMEIJI_KOISHI),
).with_creator(
    'gochou / 伍長',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1223534649738006641/koishi-satori-pocky-0002.gif',
).with_action(
    ACTION_TAG_POCKY_KISS, KOMEIJI_KOISHI, KOMEIJI_SATORI,
).with_creator(
    'satori suki',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1155425400323838053/lily-rumia-pocky-0000.png',
).with_actions(
    (ACTION_TAG_POCKY_KISS, LILY_WHITE, RUMIA),
    (ACTION_TAG_POCKY_KISS, RUMIA, LILY_WHITE),
).with_creator(
    'mitsubasa miu / 魅翼',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1232749283888070788/mamizou-ran-pocky-0000.png',
).with_action(
    ACTION_TAG_POCKY_KISS, YAKUMO_RAN, FUTATSUIWA_MAMIZOU,
).with_creator(
    'littlecloudie',
).with_editor(
    'HuyaneMatsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1155425812003180584/maribel-renko-pocky-0000.png',
).with_actions(
    (ACTION_TAG_POCKY_KISS, HEARN_MARIBEL, USAMI_RENKO),
    (ACTION_TAG_POCKY_KISS, USAMI_RENKO, HEARN_MARIBEL),
).with_creator(
    'senba chidori / 千羽チドリ',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1224002516287492250/maribel-renko-pocky-0001.png',
).with_action(
    ACTION_TAG_POCKY_KISS, USAMI_RENKO, HEARN_MARIBEL,
).with_creator(
    'imi_humei / フメイ',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1224002516686213120/maribel-renko-pocky-0002.png',
).with_action(
    ACTION_TAG_POCKY_KISS, USAMI_RENKO, HEARN_MARIBEL,
).with_creator(
    'tsukiori sasa / 月居咲々',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1155427814682669170/marisa-reimu-pocky-0000.png',
).with_actions(
    (ACTION_TAG_POCKY_KISS, KIRISAME_MARISA, HAKUREI_REIMU),
    (ACTION_TAG_POCKY_KISS, HAKUREI_REIMU, KIRISAME_MARISA),
).with_creator(
    'uyu-nagi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1155428193940013106/marisa-reimu-pocky-0001.png',
).with_action(
    ACTION_TAG_POCKY_KISS, KIRISAME_MARISA, HAKUREI_REIMU,
).with_creator(
    'hitte5416 / 辣酱',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1155428618940452954/marisa-reimu-pocky-0002.png',
).with_action(
    ACTION_TAG_POCKY_KISS, KIRISAME_MARISA, HAKUREI_REIMU,
).with_creator(
    'ookashippo / 大岡尻尾',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1155428858112254002/marisa-reimu-pocky-0003.png',
).with_actions(
    (ACTION_TAG_POCKY_KISS, KIRISAME_MARISA, HAKUREI_REIMU),
    (ACTION_TAG_POCKY_KISS, HAKUREI_REIMU, KIRISAME_MARISA),
).with_creator(
    'pasutel',
).with_editor(
    'HuyaneMatsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1224001376967983104/marisa-reimu-pocky-0004.png',
).with_actions(
    (ACTION_TAG_POCKY_KISS, HAKUREI_REIMU, KIRISAME_MARISA),
    (ACTION_TAG_POCKY_KISS, KIRISAME_MARISA, HAKUREI_REIMU),
).with_creator(
    'iwatobi hiro / いわとび ひろ',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1155429318013493288/meiling-sakuya-pocky-0000.png',
).with_action(
    ACTION_TAG_POCKY_KISS, HONG_MEILING, IZAYOI_SAKUYA,
).with_creator(
    'yuuta / 勇太',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1224003529597784165/meiling-sakuya-pocky-0001.png',
).with_action(
    ACTION_TAG_POCKY_KISS, HONG_MEILING, IZAYOI_SAKUYA,
).with_creator(
    'tima',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1155430157331472394/minamitsu-nue-pocky-0000.png',
).with_action(
    ACTION_TAG_POCKY_KISS, MURASA_MINAMITSU, HOUJUU_NUE,
).with_creator(
    'hisona',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1223999446355017958/mystia-rumia-pocky-0000.png',
).with_action(
    ACTION_TAG_POCKY_KISS, RUMIA, MYSTIA_LORELEI,
).with_creator(
    'earlgrey',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1223998997077954560/mystia-yuyuko-pocky-0000.png',
).with_action(
    ACTION_TAG_POCKY_KISS, SAIGYOUJI_YUYUKO, MYSTIA_LORELEI,
).with_creator(
    'nise nanatsura',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1155431623265894540/nazrin-shou-pocky-0000.png',
).with_action(
    ACTION_TAG_POCKY_KISS, TORAMARU_SHOU, NAZRIN,
).with_creator(
    'masha',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1224004228310368407/nazrin-shou-pocky-0001.png',
).with_action(
    ACTION_TAG_POCKY_KISS, NAZRIN, TORAMARU_SHOU,
).with_creator(
    'bbb',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1155432393444950046/patchouli-remilia-pocky-0000.png',
).with_actions(
    (ACTION_TAG_POCKY_KISS, PATCHOULI_KNOWLEDGE, SCARLET_REMILIA),
    (ACTION_TAG_POCKY_KISS, SCARLET_REMILIA, PATCHOULI_KNOWLEDGE),
).with_creator(
    'sakaetomoyuu / 栄智ゆう',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1224000604205092965/patchouli-youmo-pocky-0000.png',
).with_action(
    ACTION_TAG_POCKY_KISS, PATCHOULI_KNOWLEDGE, KONPAKU_YOUMU,
).with_creator(
    'nigo',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1223532027262009395/reimu-suika-pocky-kiss-0000.png',
).with_actions(
    (ACTION_TAG_POCKY_KISS, HAKUREI_REIMU, IBUKI_SUIKA),
    (ACTION_TAG_POCKY_KISS, IBUKI_SUIKA, HAKUREI_REIMU),
).with_creator(
    'shinekalta',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1224004617533132872/reimu-tenshi-pocky-0000.png',
).with_action(
    ACTION_TAG_POCKY_KISS, HINANAWI_TENSHI, HAKUREI_REIMU,
).with_creator(
    'ichiyan',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1223998031574339635/reimu-yukari-youmu-yuyuko-pocky-0000.png',
).with_actions(
    (ACTION_TAG_POCKY_KISS, SAIGYOUJI_YUYUKO, YAKUMO_YUKARI),
    (ACTION_TAG_POCKY_KISS, YAKUMO_YUKARI, SAIGYOUJI_YUYUKO),
).with_characters(
    HAKUREI_REIMU, KONPAKU_YOUMU,
).with_creator(
    'terimayo',
).with_editor(
    'HuyaneMatsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1224004000932958319/remilia-satori-pocky-0000.png',
).with_action(
    ACTION_TAG_POCKY_KISS, SCARLET_REMILIA, KOMEIJI_SATORI,
).with_creator(
    'Genbu / げんぶ',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1224005371627180032/sanae-suwako-pocky-0000.png',
).with_actions(
    (ACTION_TAG_POCKY_KISS, MORIYA_SUWAKO, KOCHIYA_SANAE),
    (ACTION_TAG_POCKY_KISS, KOCHIYA_SANAE, MORIYA_SUWAKO),
).with_creator(
    'cis',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1224000265007665192/sanae-youmu-pocky-0000.png',
).with_action(
    ACTION_TAG_POCKY_KISS, KONPAKU_YOUMU, KOCHIYA_SANAE,
).with_creator(
    'Shirota Shinobu / 白田 忍',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1208773143200661554/satori-suika-pocky-0000.png',
).with_actions(
    (ACTION_TAG_POCKY_KISS, KOMEIJI_SATORI, IBUKI_SUIKA),
    (ACTION_TAG_POCKY_KISS, IBUKI_SUIKA, KOMEIJI_SATORI),
).with_creator(
    'Scarristo',
).with_editor(
    'HuyaneMatsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1190968766524313631/aya-pocky-0000.png',
).with_action(
    ACTION_TAG_POCKY_KISS_SELF, SHAMEIMARU_AYA, SHAMEIMARU_AYA,
).with_creator(
    'futatsuki eru',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1190969247959097364/byakuren-pocky-0000.png',
).with_action(
    ACTION_TAG_POCKY_KISS_SELF, HIJIRI_BYAKUREN, HIJIRI_BYAKUREN,
).with_creator(
    'cpu (hexivision)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1190969248303042692/byakuren-pocky-0001.png',
).with_action(
    ACTION_TAG_POCKY_KISS_SELF, HIJIRI_BYAKUREN, HIJIRI_BYAKUREN,
).with_creator(
    'han (jackpot)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1190969955596914728/chiruno-pocky-0000.png',
).with_action(
    ACTION_TAG_POCKY_KISS_SELF, CHIRUNO, CHIRUNO,
).with_creator(
    'shokuyou pants',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1190970299542409277/eiki-pocky-0000.png',
).with_action(
    ACTION_TAG_POCKY_KISS_SELF, SHIKI_EIKI_YAMAXANADU, SHIKI_EIKI_YAMAXANADU,
).with_creator(
    'guard vent jun',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1190970888183623700/flandre-pocky-0000.png',
).with_action(
    ACTION_TAG_POCKY_KISS_SELF, SCARLET_FLANDRE, SCARLET_FLANDRE,
).with_creator(
    'mamemochi',
).with_editor(
    'HuyaneMatsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1190970889014104064/flandre-pocky-0001.png',
).with_action(
    ACTION_TAG_POCKY_KISS_SELF, SCARLET_FLANDRE, SCARLET_FLANDRE,
).with_creator(
    'zerocat',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1190970889550954637/flandre-pocky-0002.png',
).with_action(
    ACTION_TAG_POCKY_KISS_SELF, SCARLET_FLANDRE, SCARLET_FLANDRE,
).with_creator(
    'puuakachan',
).with_editor(
    'HuyaneMatsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1190970889991376956/flandre-pocky-0003.png',
).with_action(
    ACTION_TAG_POCKY_KISS_SELF, SCARLET_FLANDRE, SCARLET_FLANDRE,
).with_creator(
    'sasurai no kuchibuefuki',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1190970890532421632/flandre-pocky-0004.png',
).with_action(
    ACTION_TAG_POCKY_KISS_SELF, SCARLET_FLANDRE, SCARLET_FLANDRE,
).with_creator(
    'takamoto akisa',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1190970890851201054/flandre-pocky-0005.png',
).with_action(
    ACTION_TAG_POCKY_KISS_SELF, SCARLET_FLANDRE, SCARLET_FLANDRE,
).with_creator(
    'tosura-ayato',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1190970891195142264/flandre-pocky-0006.png',
).with_action(
    ACTION_TAG_POCKY_KISS_SELF, SCARLET_FLANDRE, SCARLET_FLANDRE,
).with_creator(
    'misa (kaeruhitode)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1190974008678690826/futo-pocky-0000.png',
).with_action(
    ACTION_TAG_POCKY_KISS_SELF, MONONOBE_NO_FUTO, MONONOBE_NO_FUTO,
).with_creator(
    'kuzumomo',
).with_editor(
    'HuyaneMatsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1190974887016276008/hatate-pocky-0000.png',
).with_action(
    ACTION_TAG_POCKY_KISS_SELF, HIMEKAIDOU_HATATE, HIMEKAIDOU_HATATE,
).with_creator(
    'shiranui (wasuresateraito)',
).with_editor(
    'HuyaneMatsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1190974887368601621/hatate-pocky-0001.png',
).with_action(
    ACTION_TAG_POCKY_KISS_SELF, HIMEKAIDOU_HATATE, HIMEKAIDOU_HATATE,
).with_creator(
    '*gomi (gomitin)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1190975589415395449/iku-pocky-0000.png',
).with_action(
    ACTION_TAG_POCKY_KISS_SELF, NAGAE_IKU, NAGAE_IKU,
).with_creator(
    'etosen',
).with_editor(
    'HuyaneMatsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1190976197803389019/kagerou-pocky-0000.png',
).with_action(
    ACTION_TAG_POCKY_KISS_SELF, IMAIZUMI_KAGEROU, IMAIZUMI_KAGEROU,
).with_creator(
    'rokugou daisuke',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1190976198164090990/kagerou-pocky-0001.png',
).with_action(
    ACTION_TAG_POCKY_KISS_SELF, IMAIZUMI_KAGEROU, IMAIZUMI_KAGEROU,
).with_creator(
    'tetsuhige / 鉄髭',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1190977227584712745/keine-pocky-0000.png',
).with_action(
    ACTION_TAG_POCKY_KISS_SELF, KAMISHIRASAWA_KEINE, KAMISHIRASAWA_KEINE,
).with_creator(
    'rebecca (keinelove)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1190977676173918268/kogasa-pocky-0000.png',
).with_action(
    ACTION_TAG_POCKY_KISS_SELF, TATARA_KOGASA, TATARA_KOGASA,
).with_creator(
    'muginon',
).with_editor(
    'HuyaneMatsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1190978107168010290/koishi-pocky-0000.png',
).with_action(
    ACTION_TAG_POCKY_KISS_SELF, KOMEIJI_KOISHI, KOMEIJI_KOISHI,
).with_creator(
    'oshiaki',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1190978107532902431/koishi-pocky-0001.png',
).with_action(
    ACTION_TAG_POCKY_KISS_SELF, KOMEIJI_KOISHI, KOMEIJI_KOISHI,
).with_creator(
    'sukima (crie)',
).with_editor(
    'HuyaneMatsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1190978107876843570/koishi-pocky-0002.png',
).with_action(
    ACTION_TAG_POCKY_KISS_SELF, KOMEIJI_KOISHI, KOMEIJI_KOISHI,
).with_creator(
    'ocha (ochappie)',
).with_editor(
    'HuyaneMatsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1191053128104161401/kokoro-pocky-0000.png',
).with_action(
    ACTION_TAG_POCKY_KISS_SELF, HATA_NO_KOKORO, HATA_NO_KOKORO,
).with_creator(
    'hammer (sunset beach)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1191053457856151622/komachi-pocky-0000.png',
).with_action(
    ACTION_TAG_POCKY_KISS_SELF, ONOZUKA_KOMACHI, ONOZUKA_KOMACHI,
).with_creator(
    'harakune (mugennero)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1191054222595194880/lily-black-pocky-0000.png',
).with_action(
    ACTION_TAG_POCKY_KISS_SELF, LILY_BLACK, LILY_BLACK,
).with_creator(
    'earlgrey',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1191054605249945754/lily-white-pocky-0000.png',
).with_action(
    ACTION_TAG_POCKY_KISS_SELF, LILY_WHITE, LILY_WHITE,
).with_creator(
    'nonotan',
).with_editor(
    'HuyaneMatsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1191055129093341264/marisa-pocky-0000.png',
).with_action(
    ACTION_TAG_POCKY_KISS_SELF, KIRISAME_MARISA, KIRISAME_MARISA,
).with_creator(
    'e.o.',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1191055129512775680/marisa-pocky-0001.png',
).with_action(
    ACTION_TAG_POCKY_KISS_SELF, KIRISAME_MARISA, KIRISAME_MARISA,
).with_creator(
    'sanpa',
).with_editor(
    'HuyaneMatsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1191055933057532024/medicine-melancholy-pocky-0000.png',
).with_action(
    ACTION_TAG_POCKY_KISS_SELF, MEDICINE_MELANCHOLY, MEDICINE_MELANCHOLY,
).with_creator(
    'dqn (dqnww)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1191056751898918983/miko-pocky-0000.png',
).with_action(
    ACTION_TAG_POCKY_KISS_SELF, TOYOSATOMIMI_NO_MIKO, TOYOSATOMIMI_NO_MIKO,
).with_creator(
    'makuwauri',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1191057265726333078/mokou-pocky-0000.png',
).with_action(
    ACTION_TAG_POCKY_KISS_SELF, FUJIWARA_NO_MOKOU, FUJIWARA_NO_MOKOU,
).with_creator(
    'hijikawa arashi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1191057266116415609/mokou-pocky-0001.png',
).with_action(
    ACTION_TAG_POCKY_KISS_SELF, FUJIWARA_NO_MOKOU, FUJIWARA_NO_MOKOU,
).with_creator(
    'hiyori-o',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1191059791162900561/momiji-pocky-0000.png',
).with_action(
    ACTION_TAG_POCKY_KISS_SELF, INUBASHIRI_MOMIJI, INUBASHIRI_MOMIJI,
).with_creator(
    'elu butyo',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1191059791548780654/momiji-pocky-0001.png',
).with_action(
    ACTION_TAG_POCKY_KISS_SELF, INUBASHIRI_MOMIJI, INUBASHIRI_MOMIJI,
).with_creator(
    'katsumi5o',
).with_editor(
    'HuyaneMatsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1191059791850782725/momiji-pocky-0002.png',
).with_action(
    ACTION_TAG_POCKY_KISS_SELF, INUBASHIRI_MOMIJI, INUBASHIRI_MOMIJI,
).with_creators(
    'ginzake (mizuumi)', 'shake (sakana)',
).with_editor(
    'HuyaneMatsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1191061121675837491/mystia-pocky-0000.png',
).with_action(
    ACTION_TAG_POCKY_KISS_SELF, MYSTIA_LORELEI, MYSTIA_LORELEI,
).with_creator(
    'phantom2071',
).with_editor(
    'HuyaneMatsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1191061766692671628/nazrin-pocky-0000.png',
).with_action(
    ACTION_TAG_POCKY_KISS_SELF, NAZRIN, NAZRIN,
).with_creator(
    'kibayashi kimori',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1191062294382252052/nue-pocky-0000.png',
).with_action(
    ACTION_TAG_POCKY_KISS_SELF, HOUJUU_NUE, HOUJUU_NUE,
).with_creator(
    'makita (vector1525)',
).with_editor(
    'HuyaneMatsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1191062294742970428/nue-pocky-0001.png',
).with_action(
    ACTION_TAG_POCKY_KISS_SELF, HOUJUU_NUE, HOUJUU_NUE,
).with_creator(
    'igakusei',
).with_editor(
    'HuyaneMatsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1191063521518174332/okuu-pocky-0000.png',
).with_action(
    ACTION_TAG_POCKY_KISS_SELF, REIUJI_UTSUHO, REIUJI_UTSUHO,
).with_creator(
    'sinzan',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1191064527358406826/orin-pocky-0000.png',
).with_action(
    ACTION_TAG_POCKY_KISS_SELF, KAENBYOU_RIN, KAENBYOU_RIN,
).with_creator(
    'kuromari (runia)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1191064527664595035/orin-pocky-0001.png',
).with_action(
    ACTION_TAG_POCKY_KISS_SELF, KAENBYOU_RIN, KAENBYOU_RIN,
).with_creators(
    'takasu', 'tks (chikuwa)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1191065315824652400/patchouli-pocky-0000.png',
).with_action(
    ACTION_TAG_POCKY_KISS_SELF, PATCHOULI_KNOWLEDGE, PATCHOULI_KNOWLEDGE,
).with_creator(
    'namiki (remiter00)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1191065316160184390/patchouli-pocky-0001.png',
).with_action(
    ACTION_TAG_POCKY_KISS_SELF, PATCHOULI_KNOWLEDGE, PATCHOULI_KNOWLEDGE,
).with_creator(
    'natsuki (silent selena)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1191065316470558840/patchouli-pocky-0002.png',
).with_action(
    ACTION_TAG_POCKY_KISS_SELF, PATCHOULI_KNOWLEDGE, PATCHOULI_KNOWLEDGE,
).with_creator(
    'porurin (do-desho)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1191066587424374834/ran-pocky-0000.png',
).with_action(
    ACTION_TAG_POCKY_KISS_SELF, YAKUMO_RAN, YAKUMO_RAN,
).with_creator(
    'dearmybrothers',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1191066587822821559/ran-pocky-0001.png',
).with_action(
    ACTION_TAG_POCKY_KISS_SELF, YAKUMO_RAN, YAKUMO_RAN,
).with_creator(
    'dearmybrothers',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1191067290142253187/reimu-pocky-0000.png',
).with_action(
    ACTION_TAG_POCKY_KISS_SELF, HAKUREI_REIMU, HAKUREI_REIMU,
).with_creators(
    'h sakray', 'sakurai haruto',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1191067291312459806/reimu-pocky-0001.png',
).with_action(
    ACTION_TAG_POCKY_KISS_SELF, HAKUREI_REIMU, HAKUREI_REIMU,
).with_creator(
    'aosi (wasabiranzy)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1191067291622850641/reimu-pocky-0002.png',
).with_action(
    ACTION_TAG_POCKY_KISS_SELF, HAKUREI_REIMU, HAKUREI_REIMU,
).with_creator(
    'pasutel',
).with_editor(
    'HuyaneMatsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1191068151518077049/remilia-pocky-0000.png',
).with_action(
    ACTION_TAG_POCKY_KISS_SELF, SCARLET_REMILIA, SCARLET_REMILIA,
).with_creator(
    'beni kurage',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1191068152398884924/remilia-pocky-0001.png',
).with_action(
    ACTION_TAG_POCKY_KISS_SELF, SCARLET_REMILIA, SCARLET_REMILIA,
).with_creator(
    'yamasuta',
).with_editor(
    'HuyaneMatsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1191068153199988736/remilia-pocky-0002.png',
).with_action(
    ACTION_TAG_POCKY_KISS_SELF, SCARLET_REMILIA, SCARLET_REMILIA,
).with_creator(
    'misa (kaeruhitode)',
).with_editor(
    'HuyaneMatsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1191069293698363534/rumia-pocky-0000.png',
).with_action(
    ACTION_TAG_POCKY_KISS_SELF, RUMIA, RUMIA,
).with_creator(
    'natoubee',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1191069549160845352/sakuya-pocky-0000.png',
).with_action(
    ACTION_TAG_POCKY_KISS_SELF, IZAYOI_SAKUYA, IZAYOI_SAKUYA,
).with_creator(
    'caramell0501',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1191069911582257193/sanae-pocky-0000.png',
).with_action(
    ACTION_TAG_POCKY_KISS_SELF, KOCHIYA_SANAE, KOCHIYA_SANAE,
).with_creator(
    'fueiku',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1191069912072978482/sanae-pocky-0001.png',
).with_action(
    ACTION_TAG_POCKY_KISS_SELF, KOCHIYA_SANAE, KOCHIYA_SANAE,
).with_creator(
    'osashin (osada)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1191070397135847475/satori-pocky-0000.png',
).with_action(
    ACTION_TAG_POCKY_KISS_SELF, KOMEIJI_SATORI, KOMEIJI_SATORI,
).with_creator(
    'noumin joemanyodw',
).with_editor(
    'HuyaneMatsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1191070397458813048/satori-pocky-0001.png',
).with_action(
    ACTION_TAG_POCKY_KISS_SELF, KOMEIJI_SATORI, KOMEIJI_SATORI,
).with_creator(
    'toritori (yakitoriya)',
).with_editor(
    'HuyaneMatsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1191071229663256607/suwako-pocky-0000.png',
).with_action(
    ACTION_TAG_POCKY_KISS_SELF, MORIYA_SUWAKO, MORIYA_SUWAKO,
).with_creator(
    'gamuo',
).with_editor(
    'HuyaneMatsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1191071804232585216/tenshi-pocky-0000.png',
).with_action(
    ACTION_TAG_POCKY_KISS_SELF, HINANAWI_TENSHI, HINANAWI_TENSHI,
).with_creator(
    'ruu (tksymkw)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1191072252721106964/wriggle-pocky-0000.png',
).with_action(
    ACTION_TAG_POCKY_KISS_SELF, WRIGGLE_NIGHTBUG, WRIGGLE_NIGHTBUG,
).with_creator(
    'kajiyama',
).with_editor(
    'HuyaneMatsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1191072253069242509/wriggle-pocky-0001.png',
).with_action(
    ACTION_TAG_POCKY_KISS_SELF, WRIGGLE_NIGHTBUG, WRIGGLE_NIGHTBUG,
).with_creator(
    'cato (monocatienus)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1191072816058081391/youmu-pocky-0000.png',
).with_action(
    ACTION_TAG_POCKY_KISS_SELF, KONPAKU_YOUMU, KONPAKU_YOUMU,
).with_creator(
    'shironeko yuuki',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1191072816993419314/youmu-pocky-0001.png',
).with_action(
    ACTION_TAG_POCKY_KISS_SELF, KONPAKU_YOUMU, KONPAKU_YOUMU,
).with_creator(
    'kame (kamepan44231)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1191072817496739870/youmu-pocky-0002.png',
).with_action(
    ACTION_TAG_POCKY_KISS_SELF, KONPAKU_YOUMU, KONPAKU_YOUMU,
).with_creator(
    'moni monico',
).with_editor(
    'HuyaneMatsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1191072817807106088/youmu-pocky-0003.png',
).with_action(
    ACTION_TAG_POCKY_KISS_SELF, KONPAKU_YOUMU, KONPAKU_YOUMU,
).with_creator(
    'katanakko daisuki',
).with_editor(
    'HuyaneMatsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1191072818109104200/youmu-pocky-0004.png',
).with_action(
    ACTION_TAG_POCKY_KISS_SELF, KONPAKU_YOUMU, KONPAKU_YOUMU,
).with_creator(
    'enelis',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1191074644120326276/yukari-pocky-0000.png',
).with_action(
    ACTION_TAG_POCKY_KISS_SELF, YAKUMO_YUKARI, YAKUMO_YUKARI,
).with_creator(
    'yoshihiro-m',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1191074644581683390/yuuka-pocky-0000.png',
).with_action(
    ACTION_TAG_POCKY_KISS_SELF, KAZAMI_YUUKA, KAZAMI_YUUKA,
).with_creator(
    'kanta (pixiv9296614)',
).with_editor(
    'HuyaneMatsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1191074644971757629/yuuka-pocky-0001.png',
).with_action(
    ACTION_TAG_POCKY_KISS_SELF, KAZAMI_YUUKA, KAZAMI_YUUKA,
).with_creator(
    'mokku',
).with_editor(
    'HuyaneMatsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1191074645416349706/yuuka-pocky-0002.png',
).with_action(
    ACTION_TAG_POCKY_KISS_SELF, KAZAMI_YUUKA, KAZAMI_YUUKA,
).with_creator(
    'roki (hirokix)',
).with_editor(
    'HuyaneMatsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1191074645760299049/yuyuko-pocky-0000.png',
).with_action(
    ACTION_TAG_POCKY_KISS_SELF, SAIGYOUJI_YUYUKO, SAIGYOUJI_YUYUKO,
).with_creator(
    'shiranui (wasuresateraito)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1220263200050774076/flandre-remilia-tickle-0000.png',
).with_action(
    ACTION_TAG_TICKLE, SCARLET_FLANDRE, SCARLET_REMILIA,
).with_creator(
    'yukiririn',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1220263410630004756/koishi-orin-satori-tickle-0000.png',
).with_action(
    ACTION_TAG_TICKLE, KOMEIJI_SATORI, KOMEIJI_KOISHI,
).with_character(
    KAENBYOU_RIN,
).with_creator(
    '13-gou',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1239483876095688775/doremy-sagume-lap-sleep-0000.png',
).with_action(
    ACTION_TAG_LAP_SLEEP, DOREMY_SWEET, KISHIN_SAGUME,
).with_creator(
    'muyue',
).with_editor(
    'HuyaneMatsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1239484602209533962/reisen-tewi-lap-sleep-0000.png',
).with_action(
    ACTION_TAG_LAP_SLEEP, INABA_TEWI, REISEN_UDONGEIN_INABA,
).with_creator(
    'shirosato',
).with_editor(
    'HuyaneMatsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1239483876980690995/aya-reimu-lap-sleep-0000.png',
).with_action(
    ACTION_TAG_LAP_SLEEP, HAKUREI_REIMU, SHAMEIMARU_AYA,
).with_creator(
    'chilwell seele',
).with_editor(
    'HuyaneMatsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1239483877366562816/kanako-suwako-lap-sleep-0000.png',
).with_action(
    ACTION_TAG_LAP_SLEEP, MORIYA_SUWAKO, YASAKA_KANAKO,
).with_creator(
    'ame iru',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1239485878938894346/marisa-nazrin-lap-sleep-0000.png',
).with_action(
    ACTION_TAG_LAP_SLEEP, NAZRIN, KIRISAME_MARISA,
).with_creator(
    'sznkrs',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1239483878054432799/kaguya-mokou-lap-sleep-0000.png',
).with_action(
    ACTION_TAG_LAP_SLEEP, FUJIWARA_NO_MOKOU, HOURAISAN_KAGUYA,
).with_creator(
    'jiege',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1239483878461276221/keine-mokou-lap-sleep-0000.png',
).with_action(
    ACTION_TAG_LAP_SLEEP, FUJIWARA_NO_MOKOU, KAMISHIRASAWA_KEINE,
).with_creator(
    'eichi yuu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1239483878914396200/koishi-satori-lap-sleep-0000.png',
).with_action(
    ACTION_TAG_LAP_SLEEP, KOMEIJI_KOISHI, KOMEIJI_SATORI,
).with_creator(
    'tsugetsuge',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1239483879279169566/keiki-mayumi-lap-sleep-0000.png',
).with_action(
    ACTION_TAG_LAP_SLEEP, JOUTOUGUU_MAYUMI, HANIYASUSHIN_KEIKI,
).with_creator(
    'yamase',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1239487878883704852/futo-miko-tojiko-lap-sleep-0000.png',
).with_actions(
    (ACTION_TAG_LAP_SLEEP, MONONOBE_NO_FUTO, SOGA_NO_TOJIKO),
    (ACTION_TAG_LAP_SLEEP, TOYOSATOMIMI_NO_MIKO, SOGA_NO_TOJIKO),
).with_creator(
    'ashiyu (ashu ashu)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1239483916579115018/marisa-reimu-lap-sleep-0000.png',
).with_action(
    ACTION_TAG_LAP_SLEEP, KIRISAME_MARISA, HAKUREI_REIMU,
).with_creator(
    'muzuki uruu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1239483916918849626/maribel-renko-lap-sleep-0000.png',
).with_action(
    ACTION_TAG_LAP_SLEEP, HEARN_MARIBEL, USAMI_RENKO,
).with_creator(
    'fuukadia (narcolepsy)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1239483917287952424/chen-ran-yukari-lap-sleep-0000.png',
).with_action(
    ACTION_TAG_LAP_SLEEP, CHEN, YAKUMO_RAN,
).with_character(
    YAKUMO_YUKARI,
).with_creator(
    'chanta (ayatakaoisii)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1239483917715767306/chen-ran-lap-sleep-0000.png',
).with_action(
    ACTION_TAG_LAP_SLEEP, CHEN, YAKUMO_RAN,
).with_creator(
    'namuko',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1239483918089064448/kanako-suwako-lap-sleep-0001.png',
).with_action(
    ACTION_TAG_LAP_SLEEP, MORIYA_SUWAKO, YASAKA_KANAKO,
).with_creator(
    'wataichi meko',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1239483918403506206/mamizou-nue-lap-sleep-0000.png',
).with_action(
    ACTION_TAG_LAP_SLEEP, HOUJUU_NUE, FUTATSUIWA_MAMIZOU,
).with_creator(
    'daniwae',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1239483918835646464/flandre-remilia-sakuya-lap-sleep-0000.png',
).with_action(
    ACTION_TAG_LAP_SLEEP, SCARLET_REMILIA, SCARLET_FLANDRE,
).with_character(
    IZAYOI_SAKUYA,
).with_creator(
    'satou kibi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1239483919271858187/shion-tenshi-lap-sleep-0000.png',
).with_action(
    ACTION_TAG_LAP_SLEEP, YORIGAMI_SHION, HINANAWI_TENSHI,
).with_creator(
    'piyodesu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1239496658413289492/kanako-suwako-lick-0000.png',
).with_action(
    ACTION_TAG_LICK, MORIYA_SUWAKO, YASAKA_KANAKO,
).with_creator(
    'ame iru',
).with_editor(
    'HuyaneMatsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1239496658958680074/patchouli-remilia-hug-0000.png',
).with_action(
    ACTION_TAG_HUG, PATCHOULI_KNOWLEDGE, SCARLET_REMILIA,
).with_creator(
    'eichi yuu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1239497918130556938/yuyuko-older-0004.png',
).with_action(
    ACTION_TAG_LIKE, None, SAIGYOUJI_YUYUKO,
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1239499027419103273/flandre-okina-help-0000.png',
).with_action(
    ACTION_TAG_LIKE, SCARLET_FLANDRE, MATARA_OKINA,
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1239500064355913728/aya-megumu-kiss-0000.png',
).with_action(
    ACTION_TAG_KISS, IIZUNAMARU_MEGUMU, SHAMEIMARU_AYA,
).with_creator(
    'raptor7',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1239500712560431126/chiruno-sunny-kiss-0000.png',
).with_action(
    ACTION_TAG_KISS, SUNNY_MILK, CHIRUNO,
).with_creator(
    'senmura',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1239500712560431126/chiruno-sunny-kiss-0000.png',
).with_action(
    ACTION_TAG_KISS, SUNNY_MILK, CHIRUNO,
).with_creator(
    'senmura',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1239501762780463114/koishi-satori-kiss-0002.png',
).with_action(
    ACTION_TAG_KISS, KOMEIJI_KOISHI, KOMEIJI_SATORI,
).with_creator(
    'meno~n',
).with_editor(
    'HuyaneMatsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1239502950016225310/aya-reimu-hug-0000.png',
).with_action(
    ACTION_TAG_HUG, SHAMEIMARU_AYA, HAKUREI_REIMU,
).with_creator(
    'sakic43899',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1239504389324935188/aya-reimu-hug-0001.png',
).with_action(
    ACTION_TAG_HUG, SHAMEIMARU_AYA, HAKUREI_REIMU,
).with_creator(
    'sakic43899',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1239504387974369352/aya-reimu-kiss-0000.png',
).with_action(
    ACTION_TAG_KISS, SHAMEIMARU_AYA, HAKUREI_REIMU,
).with_creator(
    'sakic43899',
).with_editor(
    'HuyaneMatsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1239504388595122247/aya-reimu-kiss-0001.png',
).with_action(
    ACTION_TAG_KISS, SHAMEIMARU_AYA, HAKUREI_REIMU,
).with_creator(
    'sakic43899',
).with_editor(
    'HuyaneMatsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1242232103517552732/marisa-reimu-kiss-0002.png',
).with_actions(
    (ACTION_TAG_KISS, KIRISAME_MARISA, HAKUREI_REIMU),
    (ACTION_TAG_KISS, HAKUREI_REIMU, KIRISAME_MARISA),
).with_creator(
    'aihara-rina',
).with_editor(
    'HuyaneMatsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1242364420462612490/sagume-seiran-kiss-0000.png',
).with_action(
    ACTION_TAG_KISS, KISHIN_SAGUME, SEIRAN,
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1242365774048530483/kagerou-tewi-hug-nom-0000.png',
).with_actions(
    (ACTION_TAG_HUG, IMAIZUMI_KAGEROU, INABA_TEWI),
    (ACTION_TAG_NOM, IMAIZUMI_KAGEROU, INABA_TEWI),
).with_creator(
    'haruwaka 064',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1242367008327335936/alice-aya-hug-0000.png',
).with_action(
    ACTION_TAG_HUG, SHAMEIMARU_AYA, MARGATROID_ALICE,
).with_creator(
    'indis',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1242368092059865161/aya-chiruno-hug-0000.png',
).with_action(
    ACTION_TAG_HUG, SHAMEIMARU_AYA, CHIRUNO,
).with_creator(
    'kototoki',
).with_editor(
    'HuyaneMatsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1242369414406344765/aya-chiruno-kiss.gif',
).with_action(
    ACTION_TAG_KISS, CHIRUNO, SHAMEIMARU_AYA,
).with_creator(
    'kototoki',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1242370408011792445/aya-chiruno-hug-0001.png',
).with_action(
    ACTION_TAG_HUG, SHAMEIMARU_AYA, CHIRUNO,
).with_creator(
    'kototoki',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1242370957926989834/alice-marisa-feed-0000.png',
).with_action(
    ACTION_TAG_FEED, MARGATROID_ALICE, KIRISAME_MARISA,
).with_creator(
    'kototoki',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1242371722322251796/seiga-miyako-hug-0000.png',
).with_action(
    ACTION_TAG_HUG, KAKU_SEIGA, MIYAKO_YOSHIKA,
).with_creator(
    'haruwaka 064',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1242372711158911056/kagerou-tewi-nom-0000.png',
).with_action(
    ACTION_TAG_NOM, IMAIZUMI_KAGEROU, INABA_TEWI,
).with_creator(
    'haruwaka 064',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1242373671050547240/kagerou-tewi-handhold-0000.png',
).with_actions(
    (ACTION_TAG_HANDHOLD, IMAIZUMI_KAGEROU, INABA_TEWI),
    (ACTION_TAG_HANDHOLD, INABA_TEWI, IMAIZUMI_KAGEROU),
).with_creator(
    'haruwaka 064',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1242374790698893343/kagerou-tewi-hug-0000.png',
).with_action(
    ACTION_TAG_HUG, IMAIZUMI_KAGEROU, INABA_TEWI,
).with_creator(
    'haruwaka 064',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1242375506507075674/kagerou-tewi-kiss-0000.png',
).with_action(
    ACTION_TAG_KISS, INABA_TEWI, IMAIZUMI_KAGEROU,
).with_creator(
    'haruwaka 064',
).with_editor(
    'HuyaneMatsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1242376905865560074/kagerou-tewi-feed-0000.png',
).with_action(
    ACTION_TAG_FEED, IMAIZUMI_KAGEROU, INABA_TEWI,
).with_creator(
    'haruwaka 064',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1242378636926128148/aya-wriggle-lick-0000.png',
).with_action(
    ACTION_TAG_LICK, SHAMEIMARU_AYA, WRIGGLE_NIGHTBUG,
).with_creator(
    'madara inosuke',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1244249925416648857/koishi-kokoro-hug-kiss-0000.png',
).with_actions(
    (ACTION_TAG_HUG, HATA_NO_KOKORO, KOMEIJI_KOISHI),
    (ACTION_TAG_KISS, HATA_NO_KOKORO, KOMEIJI_KOISHI),
).with_creator(
    'mino (minori)',
).with_editor(
    'HuyaneMatsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1244251589309501460/ran-yukari-kiss-0002.png',
).with_action(
    ACTION_TAG_KISS, YAKUMO_YUKARI, YAKUMO_RAN,
).with_creator(
    'kirisita',
).with_editor(
    'HuyaneMatsu',
)


TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1244252640007819285/mamizou-ran-kiss-0001.png',
).with_actions(
    (ACTION_TAG_KISS, FUTATSUIWA_MAMIZOU, YAKUMO_RAN),
    (ACTION_TAG_KISS, YAKUMO_RAN, FUTATSUIWA_MAMIZOU),
).with_creator(
    'littlecloudie',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1244253103910551674/flandre-koishi-kiss-0006.png',
).with_action(
    ACTION_TAG_KISS, KOMEIJI_KOISHI, SCARLET_FLANDRE,
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1244253586226155580/kogasa-sekibanki-kiss-0000.png',
).with_actions(
    (ACTION_TAG_KISS, TATARA_KOGASA, SEKIBANKI),
    (ACTION_TAG_KISS, SEKIBANKI, TATARA_KOGASA),
).with_creator(
    'puchimirin',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1244254703647330415/kanako-suwako-kiss-0000.png',
).with_action(
    ACTION_TAG_KISS, MORIYA_SUWAKO, YASAKA_KANAKO,
).with_editor(
    'HuyaneMatsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1244255837971550321/hecatia-junko-kiss-0000.png',
).with_action(
    ACTION_TAG_KISS, JUNKO, HECATIA_LAPISLAZULI,
).with_creator(
    'neold',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1244257374101831732/saki-yachie-kiss-0000.png',
).with_actions(
    (ACTION_TAG_KISS, KUROKOMA_SAKI, KICCHOU_YACHIE),
    (ACTION_TAG_KISS, KICCHOU_YACHIE, KUROKOMA_SAKI),
).with_creator(
    'inuko (ink0425)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1244257875392598066/meiling-sakuya-kiss-0001.png',
).with_actions(
    (ACTION_TAG_KISS, HONG_MEILING, IZAYOI_SAKUYA),
    (ACTION_TAG_KISS, IZAYOI_SAKUYA, HONG_MEILING),
).with_creator(
    'soubi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1244307793524166720/reimu-sanae-hug-0000.png',
).with_action(
    ACTION_TAG_HUG, HAKUREI_REIMU, KOCHIYA_SANAE,
).with_creator(
    'tsuno no hito',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1244307794501308446/reimu-sanae-kiss-0000.png',
).with_action(
    ACTION_TAG_KISS, KOCHIYA_SANAE, HAKUREI_REIMU,
).with_creator(
    'tsuno no hito',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1244307794992300152/alice-marisa-hug-kiss-0000.png',
).with_actions(
    (ACTION_TAG_HUG, KIRISAME_MARISA, MARGATROID_ALICE),
    (ACTION_TAG_KISS, KIRISAME_MARISA, MARGATROID_ALICE),
).with_creator(
    'tsuno no hito',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1244307795273322576/alice-marisa-kiss-0003.png',
).with_action(
    ACTION_TAG_KISS, KIRISAME_MARISA, MARGATROID_ALICE,
).with_creator(
    'tsuno no hito',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1244307795621314673/alice-marisa-hug-0003.png',
).with_action(
    ACTION_TAG_HUG, KIRISAME_MARISA, MARGATROID_ALICE,
).with_creator(
    'tsuno no hito',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1244307795902464081/alice-marisa-hug-0002.png',
).with_action(
    ACTION_TAG_HUG, MARGATROID_ALICE, KIRISAME_MARISA,
).with_creator(
    'tsuno no hito',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1244307796342608004/alice-marisa-hug-0001.png',
).with_action(
    ACTION_TAG_HUG, KIRISAME_MARISA, MARGATROID_ALICE,
).with_creator(
    'tsuno no hito',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1244307796703314120/alice-marisa-kiss-0002.png',
).with_action(
    ACTION_TAG_KISS, MARGATROID_ALICE, KIRISAME_MARISA,
).with_creator(
    'tsuno no hito',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1244307797093388400/alice-marisa-hug-0000.png',
).with_action(
    ACTION_TAG_HUG, KIRISAME_MARISA, MARGATROID_ALICE,
).with_creator(
    'tsuno no hito',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1244307797877719081/reimu-sanae-hug-0001.png',
).with_actions(
    (ACTION_TAG_HUG, HAKUREI_REIMU, KOCHIYA_SANAE),
    (ACTION_TAG_HUG, KOCHIYA_SANAE, HAKUREI_REIMU),
).with_creator(
    'tsuno no hito',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1244307815401787473/alice-marisa-hug-0004.png',
).with_action(
    ACTION_TAG_HUG, KIRISAME_MARISA, MARGATROID_ALICE,
).with_creator(
    'tsuno no hito',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1244307815837728849/alice-marisa-kiss-0004.png',
).with_actions(
    (ACTION_TAG_KISS, MARGATROID_ALICE, KIRISAME_MARISA),
    (ACTION_TAG_KISS, KIRISAME_MARISA, MARGATROID_ALICE),
).with_creator(
    'tsuno no hito',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1244312740592357497/akyuu-kosuzu-lap-sleep-0000.png',
).with_action(
    ACTION_TAG_LAP_SLEEP, MOTOORI_KOSUZU, HIEDA_NO_AKYUU,
).with_creator(
    'nekolina',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1244329882314473572/koishi-kokoro-kiss-0001.png',
).with_action(
    ACTION_TAG_KISS, KOMEIJI_KOISHI, HATA_NO_KOKORO,
).with_creator(
    'nekolina',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1244329883044413450/hecatia-junko-lap-sleep-0000.png',
).with_action(
    ACTION_TAG_LAP_SLEEP, JUNKO, HECATIA_LAPISLAZULI,
).with_creator(
    'nekolina',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1244329883631358052/eiki-komachi-hug-0000.png',
).with_action(
    ACTION_TAG_HUG, ONOZUKA_KOMACHI, SHIKI_EIKI_YAMAXANADU,
).with_creator(
    'nekolina',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1244329884487254027/maribel-renko-hug-kiss-0000.png',
).with_actions(
    (ACTION_TAG_HUG, HEARN_MARIBEL, USAMI_RENKO),
    (ACTION_TAG_HUG, USAMI_RENKO, HEARN_MARIBEL),
    (ACTION_TAG_KISS, HEARN_MARIBEL, USAMI_RENKO),
    (ACTION_TAG_KISS, USAMI_RENKO, HEARN_MARIBEL),
).with_creator(
    'nekolina',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1244329885133045873/alice-sakuya-kiss-0000.png',
).with_action(
    ACTION_TAG_KISS, IZAYOI_SAKUYA, MARGATROID_ALICE,
).with_creator(
    'nekolina',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1244329885518794822/kogasa-raiko-hug-0000.png',
).with_actions(
    (ACTION_TAG_HUG, TATARA_KOGASA, HORIKAWA_RAIKO),
    (ACTION_TAG_HUG, HORIKAWA_RAIKO, TATARA_KOGASA),
).with_creator(
    'nekolina',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1244329885938483321/marisa-reimu-kiss-0003.png',
).with_actions(
    (ACTION_TAG_KISS, KIRISAME_MARISA, HAKUREI_REIMU),
    (ACTION_TAG_KISS, HAKUREI_REIMU, KIRISAME_MARISA),
).with_creator(
    'nekolina',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1244329886248730654/hecatia-junko-kiss-0001.png',
).with_actions(
    (ACTION_TAG_KISS, HECATIA_LAPISLAZULI, JUNKO),
    (ACTION_TAG_KISS, JUNKO, HECATIA_LAPISLAZULI),
).with_creator(
    'nekolina',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1244329886706040933/marisa-reimu-hug-0004.png',
).with_actions(
    (ACTION_TAG_HUG, KIRISAME_MARISA, HAKUREI_REIMU),
    (ACTION_TAG_HUG, HAKUREI_REIMU, KIRISAME_MARISA),
).with_creator(
    'nekolina',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1244332524910416064/koishi-okuu-orin-satori-lap-sleep-0000.png',
).with_action(
    ACTION_TAG_LAP_SLEEP, KOMEIJI_KOISHI, KOMEIJI_SATORI,
).with_characters(
    KAENBYOU_RIN,
    REIUJI_UTSUHO,
).with_creator(
    'eru aise',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1244362795391385691/reimu-sanae-hug-0002.png',
).with_action(
    ACTION_TAG_HUG, KOCHIYA_SANAE, HAKUREI_REIMU,
).with_creator(
    'mokutan (link machine)',
).with_editor(
    'HuyaneMatsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1244362805663105167/reimu-sanae-kiss-0001.png',
).with_action(
    ACTION_TAG_KISS, KOCHIYA_SANAE, HAKUREI_REIMU,
).with_creator(
    'mokutan (link machine)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1244362806917074983/reimu-sanae-kiss-0002.png',
).with_action(
    ACTION_TAG_KISS, HAKUREI_REIMU, KOCHIYA_SANAE,
).with_creator(
    'mokutan (link machine)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1244362807969972244/reimu-sanae-kiss-0003.png',
).with_action(
    ACTION_TAG_KISS, HAKUREI_REIMU, KOCHIYA_SANAE,
).with_creator(
    'mokutan (link machine)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1244362809006096535/reimu-sanae-handhold-0000.png',
).with_actions(
    (ACTION_TAG_HANDHOLD, HAKUREI_REIMU, KOCHIYA_SANAE),
    (ACTION_TAG_HANDHOLD, KOCHIYA_SANAE, HAKUREI_REIMU),
).with_creator(
    'mokutan (link machine)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1244362810197282846/reimu-sanae-kiss-0004.png',
).with_action(
    ACTION_TAG_KISS, HAKUREI_REIMU, KOCHIYA_SANAE,
).with_creator(
    'mokutan (link machine)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1244362810738086018/reimu-sanae-hug-0005.png',
).with_actions(
    (ACTION_TAG_HUG, HAKUREI_REIMU, KOCHIYA_SANAE),
    (ACTION_TAG_HUG, KOCHIYA_SANAE, HAKUREI_REIMU),
).with_creator(
    'mokutan (link machine)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1244362811505905674/reimu-sanae-hug-kiss-0000.png',
).with_actions(
    (ACTION_TAG_HUG, HAKUREI_REIMU, KOCHIYA_SANAE),
    (ACTION_TAG_HUG, KOCHIYA_SANAE, HAKUREI_REIMU),
    (ACTION_TAG_KISS, HAKUREI_REIMU, KOCHIYA_SANAE),
    (ACTION_TAG_KISS, KOCHIYA_SANAE, HAKUREI_REIMU),
).with_creator(
    'mokutan (link machine)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1244362812692889661/reimu-sanae-hug-0004.png',
).with_actions(
    (ACTION_TAG_HUG, HAKUREI_REIMU, KOCHIYA_SANAE),
    (ACTION_TAG_HUG, KOCHIYA_SANAE, HAKUREI_REIMU),
).with_creator(
    'mokutan (link machine)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1244362813753790556/reimu-sanae-hug-0003.png',
).with_actions(
    (ACTION_TAG_HUG, HAKUREI_REIMU, KOCHIYA_SANAE),
    (ACTION_TAG_HUG, KOCHIYA_SANAE, HAKUREI_REIMU),
).with_creator(
    'mokutan (link machine)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1244362814580330636/reimu-sanae-kiss-0005.png',
).with_action(
    ACTION_TAG_KISS, HAKUREI_REIMU, KOCHIYA_SANAE,
).with_creator(
    'mokutan (link machine)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1244549231646216223/hecatia-junko-hug-0000.png',
).with_action(
    ACTION_TAG_HUG, HECATIA_LAPISLAZULI, JUNKO,
).with_creator(
    'frogsnake',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1244552423729528853/aya-hatate-kiss-0001.png',
).with_actions(
    (ACTION_TAG_KISS, SHAMEIMARU_AYA, HIMEKAIDOU_HATATE),
    (ACTION_TAG_KISS, HIMEKAIDOU_HATATE, SHAMEIMARU_AYA),
).with_creator(
    'springarashi02',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1244552424673251368/flandre-koishi-marisa-handhold-hug-0000.png',
).with_actions(
    (ACTION_TAG_HANDHOLD, SCARLET_FLANDRE, KOMEIJI_KOISHI),
    (ACTION_TAG_HANDHOLD, KOMEIJI_KOISHI, SCARLET_FLANDRE),
    (ACTION_TAG_HUG, SCARLET_FLANDRE, KIRISAME_MARISA),
    (ACTION_TAG_HUG, KOMEIJI_KOISHI, KIRISAME_MARISA),
).with_creator(
    'springarashi02',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1244552425575026728/marisa-reimu-fluff-0000.png',
).with_action(
    ACTION_TAG_FLUFF, HAKUREI_REIMU, KIRISAME_MARISA,
).with_creator(
    'springarashi02',
).with_editor(
    'HuyaneMatsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1244552426434990120/megumu-tsukasa-handhold-0000.png',
).with_actions(
    (ACTION_TAG_HANDHOLD, IIZUNAMARU_MEGUMU, KUDAMAKI_TSUKASA),
    (ACTION_TAG_HANDHOLD, KUDAMAKI_TSUKASA, IIZUNAMARU_MEGUMU),
).with_creator(
    'springarashi02',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1244552426988638299/hecatia-junko-hug-0000.png',
).with_action(
    ACTION_TAG_HUG, HECATIA_LAPISLAZULI, JUNKO,
).with_creator(
    'springarashi02',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1244655431075237938/okuu-orin-hug-0009.png',
).with_action(
    ACTION_TAG_HUG, REIUJI_UTSUHO, KAENBYOU_RIN,
).with_creator(
    'mizuga',
).with_editor(
    'HuyaneMatsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1244655431410778203/luna-star-sunny-poke-0000.png',
).with_actions(
    (ACTION_TAG_POKE, SUNNY_MILK, LUNA_CHILD),
    (ACTION_TAG_POKE, STAR_SAPPHIRE, LUNA_CHILD),
).with_creator(
    'mizuga',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1244655431985401906/momiji-ran-hug-0000.png',
).with_action(
    ACTION_TAG_HUG, YAKUMO_RAN, INUBASHIRI_MOMIJI,
).with_creator(
    'mizuga',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1244655432585445498/koishi-ran-hug-0000.png',
).with_action(
    ACTION_TAG_HUG, KOMEIJI_KOISHI, YAKUMO_RAN,
).with_creator(
    'mizuga',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1244655432925052928/hatate-momiji-hug-0000.png',
).with_action(
    ACTION_TAG_HUG, YAKUMO_RAN, INUBASHIRI_MOMIJI,
).with_creator(
    'mizuga',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1244655433344618556/okuu-orin-hug-0008.png',
).with_actions(
    (ACTION_TAG_HUG, REIUJI_UTSUHO, KAENBYOU_RIN),
    (ACTION_TAG_HUG, KAENBYOU_RIN, REIUJI_UTSUHO),
).with_creator(
    'mizuga',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1244680704705433701/orin-dance-0000.gif',
).with_action(
    ACTION_TAG_DANCE, KAENBYOU_RIN, None,
).with_creator(
    'azurereindeer',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1244680705280184452/seiga-yoshika-pat-0000.png',
).with_action(
    ACTION_TAG_PAT, KAKU_SEIGA, MIYAKO_YOSHIKA,
).with_creator(
    'azurereindeer',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1244682028130111599/reisen-youmu-hug-0000.png',
).with_action(
    ACTION_TAG_HUG, KONPAKU_YOUMU, REISEN_UDONGEIN_INABA,
).with_creator(
    'diving penguin',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1244682028130111599/reisen-youmu-hug-0000.png',
).with_action(
    ACTION_TAG_HUG, KONPAKU_YOUMU, REISEN_UDONGEIN_INABA,
).with_creator(
    'diving penguin',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1244682935966367825/youmu-hug-0000.png',
).with_action(
    ACTION_TAG_HUG, KONPAKU_YOUMU, KONPAKU_YOUMU,
).with_creator(
    'nyarocks',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1244686205132476577/wriggle-yamame-hug-0000.png',
).with_action(
    ACTION_TAG_HUG, KURODANI_YAMAME, WRIGGLE_NIGHTBUG,
).with_creator(
    'bwell',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1244686205669478461/koishi-satori-handhold-0000.png',
).with_actions(
    (ACTION_TAG_HANDHOLD, KOMEIJI_KOISHI, KOMEIJI_SATORI),
    (ACTION_TAG_HANDHOLD, KOMEIJI_SATORI, KOMEIJI_KOISHI),
).with_creator(
    'bwell',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1244686206164533338/alice-marisa-hug-0005.png',
).with_action(
    ACTION_TAG_HUG, MARGATROID_ALICE, KIRISAME_MARISA,
).with_creator(
    'bwell',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1244686206516858992/nazrin-orin-hug-0000.png',
).with_action(
    ACTION_TAG_HUG, KAENBYOU_RIN, NAZRIN,
).with_creator(
    'bwell',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1244691802963841125/flandre-remilia-handhold-0000.png',
).with_actions(
    (ACTION_TAG_HANDHOLD, SCARLET_FLANDRE, SCARLET_REMILIA),
    (ACTION_TAG_HANDHOLD, SCARLET_REMILIA, SCARLET_FLANDRE),
).with_creator(
    'bwell',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1244686207485739130/reimu-sanae-tickle-0000.png',
).with_action(
    ACTION_TAG_TICKLE, KOCHIYA_SANAE, HAKUREI_REIMU,
).with_creator(
    'bwell',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1244686207921688687/hina-nitori-lap-sleep-0000.png',
).with_action(
    ACTION_TAG_LAP_SLEEP, KAWASHIRO_NITORI, KAGIYAMA_HINA,
).with_creator(
    'bwell',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1244686208341250068/futo-ichirin-poke-0000.png',
).with_action(
    ACTION_TAG_POKE, KUMOI_ICHIRIN, MONONOBE_NO_FUTO,
).with_creator(
    'bwell',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1244695039423156244/junko-reisen-hug-0000.png',
).with_action(
    ACTION_TAG_HUG, JUNKO, REISEN_UDONGEIN_INABA,
).with_creator(
    'guming diban',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1244697424795013191/marisa-reimu-kiss-0004.png',
).with_action(
    ACTION_TAG_KISS, KIRISAME_MARISA, HAKUREI_REIMU,
).with_creator(
    'amaama',
).with_editor(
    'HuyaneMatsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1244697425097130064/marisa-reimu-hug-0005.png',
).with_actions(
    (ACTION_TAG_HUG, KIRISAME_MARISA, HAKUREI_REIMU),
    (ACTION_TAG_HUG, HAKUREI_REIMU, KIRISAME_MARISA),
).with_creator(
    'amaama',
).with_editor(
    'HuyaneMatsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1244697425478815875/chen-ran-yukari-hug-0001.png',
).with_actions(
    (ACTION_TAG_HUG, CHEN, YAKUMO_RAN),
    (ACTION_TAG_HUG, YAKUMO_YUKARI, YAKUMO_RAN),
).with_creator(
    'amaama',
).with_editor(
    'HuyaneMatsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1244697425860362321/marisa-reimu-lap-sleep-0001.png',
).with_action(
    ACTION_TAG_LAP_SLEEP, HAKUREI_REIMU, KIRISAME_MARISA,
).with_creator(
    'amaama',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1244721476775448647/flandre-remilia-pocky-kiss-0000.png',
).with_action(
    ACTION_TAG_POCKY_KISS, SCARLET_FLANDRE, SCARLET_REMILIA,
).with_creator(
    'misha (hoongju)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1244721477106925638/kogasa-nue-hug-0000.png',
).with_action(
    ACTION_TAG_HUG, TATARA_KOGASA, HOUJUU_NUE,
).with_creator(
    'misha (hoongju)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1244721477106925638/kogasa-nue-hug-0000.png',
).with_action(
    ACTION_TAG_HUG, TATARA_KOGASA, HOUJUU_NUE,
).with_creator(
    'misha (hoongju)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1244721477383618691/chiruno-wakasagihime-kiss-0000.png',
).with_action(
    ACTION_TAG_KISS, CHIRUNO, WAKASAGIHIME,
).with_creator(
    'misha (hoongju)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1244721477618765928/kagerou-sekibanki-kiss-0000.png',
).with_action(
    ACTION_TAG_KISS, SEKIBANKI, IMAIZUMI_KAGEROU,
).with_creator(
    'misha (hoongju)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1244721477937401981/kagerou-yatsuhashi-kiss-0000.png',
).with_action(
    ACTION_TAG_KISS, IMAIZUMI_KAGEROU, TSUKUMO_YATSUHASHI,
).with_creator(
    'misha (hoongju)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1244721478218285137/benben-yatsuhashi-kiss-0000.png',
).with_action(
    ACTION_TAG_KISS, TSUKUMO_YATSUHASHI, TSUKUMO_BENBEN,
).with_creator(
    'misha (hoongju)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1244721478461820959/benben-seija-kiss-0000.png',
).with_action(
    ACTION_TAG_KISS, TSUKUMO_BENBEN, KIJIN_SEIJA,
).with_creator(
    'misha (hoongju)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1244721478713217087/chiruno-raiko-kiss-0000.png',
).with_action(
    ACTION_TAG_KISS, HORIKAWA_RAIKO, CHIRUNO,
).with_creator(
    'misha (hoongju)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1244721479082578085/clownpiece-junko-hug-0000.png',
).with_action(
    ACTION_TAG_HUG, JUNKO, CLOWNPIECE,
).with_creator(
    'misha (hoongju)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1244731603305893939/kagerou-tewi-lick-0000.png',
).with_action(
    ACTION_TAG_LICK, IMAIZUMI_KAGEROU, INABA_TEWI,
).with_creator(
    'haruwaka 064',
).with_editor(
    'HuyaneMatsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1244737754735055008/kogasa-sanae-pat-0000.png',
).with_action(
    ACTION_TAG_PAT, KOCHIYA_SANAE, TATARA_KOGASA,
).with_creator(
    'piyodesu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1244738527997067485/kogasa-pat-0000.png',
).with_action(
    ACTION_TAG_PAT, None, TATARA_KOGASA,
).with_creator(
    'piyodesu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1246935653485379584/aya-momiji-pat-0001.gif',
).with_action(
    ACTION_TAG_PAT, SHAMEIMARU_AYA, INUBASHIRI_MOMIJI,
).with_creator(
    'shimouki izui',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1244742544101736498/hina-momiji-pat-0000.gif',
).with_action(
    ACTION_TAG_PAT, KAGIYAMA_HINA, INUBASHIRI_MOMIJI,
).with_creator(
    '1641 (chfhrtor94)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1244743345637560400/meiling-sakuya-pat-0000.gif',
).with_action(
    ACTION_TAG_PAT, IZAYOI_SAKUYA, HONG_MEILING,
).with_creator(
    'ayano (ayn398)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1244744486035390545/koishi-satori-pat-0000.png',
).with_action(
    ACTION_TAG_PAT, KOMEIJI_SATORI, KOMEIJI_KOISHI,
).with_creator(
    'yimudesu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1244744486794428477/alice-yuuka-kiss-0000.png',
).with_actions(
    (ACTION_TAG_KISS, MARGATROID_ALICE, KAZAMI_YUUKA),
    (ACTION_TAG_KISS, KAZAMI_YUUKA, MARGATROID_ALICE),
).with_creator(
    'yimudesu',
)
