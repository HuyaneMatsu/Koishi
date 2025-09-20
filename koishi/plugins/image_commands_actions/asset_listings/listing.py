__all__ = ('TOUHOU_ACTION_ALL',)

from ...image_handling_core import ImageHandlerStatic
from ...touhou_core import (
    AKI_MINORIKO, AKI_SHIZUHA, CHEN, CHIRUNO, CLOWNPIECE, DAIYOUSEI, DOREMY_SWEET, ELIS, ETERNITY_LARVA,
    FUJIWARA_NO_MOKOU, FUTATSUIWA_MAMIZOU, HAKUREI_MIKO, HAKUREI_REIMU, HANIYASUSHIN_KEIKI, HATA_NO_KOKORO,
    HEARN_MARIBEL, HECATIA_LAPISLAZULI, HIEDA_NO_AKYUU, HIJIRI_BYAKUREN, HIMEKAIDOU_HATATE, HINANAWI_TENSHI,
    HONG_MEILING, HORIKAWA_RAIKO, HOSHIGUMA_YUUGI, HOUJUU_NUE, HOURAISAN_KAGUYA, IBARAKI_KASEN, IBUKI_SUIKA,
    IIZUNAMARU_MEGUMU, IMAIZUMI_KAGEROU, INABA_TEWI, INUBASHIRI_MOMIJI, IWANAGA_ARIYA, IZAYOI_SAKUYA, JOUTOUGUU_MAYUMI,
    JUNKO, KAENBYOU_RIN, KAGIYAMA_HINA, KAKU_SEIGA, KAMISHIRASAWA_KEINE, KASODANI_KYOUKO, KAWASHIRO_NITORI,
    KAZAMI_YUUKA, KICCHOU_YACHIE, KIJIN_SEIJA, KIRISAME_MARISA, KISHIN_SAGUME, KOAKUMA, KOCHIYA_SANAE, KOMANO_AUNN,
    KOMEIJI_KOISHI, KOMEIJI_SATORI, KONPAKU_YOUMU, KUDAMAKI_TSUKASA, KUMOI_ICHIRIN, KURODANI_YAMAME, KUROKOMA_SAKI,
    LETTY_WHITEROCK, LILY_BLACK, LILY_WHITE, LORELEI_MYSTIA, LUNA_CHILD, MARGATROID_ALICE, MATARA_OKINA,
    MEDICINE_MELANCHOLY, MEIRA, MISHAGUJI, MITSUGASHIRA_ENOKO, MIYAKO_YOSHIKA, MIZUHASHI_PARSEE, MONONOBE_NO_FUTO,
    MORICHIKA_RINNOSUKE, MORIYA_SUWAKO, MOTOORI_KOSUZU, MURASA_MINAMITSU, NAGAE_IKU, NAZRIN, NIPPAKU_ZANMU,
    NISHIDA_SATONO, NIWATARI_KUTAKA, OKUNODA_MIYOI, ONOZUKA_KOMACHI, PATCHOULI_KNOWLEDGE, PRISMRIVER_LYRICA,
    PRISMRIVER_MERLIN, REISEN_UDONGEIN_INABA, REIUJI_UTSUHO, RINGO, RUMIA, SAIGYOUJI_YUYUKO, SARIEL, SCARLET_FLANDRE,
    SCARLET_REMILIA, SEIRAN, SEKIBANKI, SHAMEIMARU_AYA, SHIKI_EIKI_YAMAXANADU, SHINKI, SOGA_NO_TOJIKO, STAR_SAPPHIRE,
    SUKUNA_SHINMYOUMARU, SUNNY_MILK, TATARA_KOGASA, TEIREIDA_MAI, TENKAJIN_CHIYARI, TENKYUU_CHIMATA, TOKIKO,
    TORAMARU_SHOU, TOUTETSU_YUUMA, TOYOSATOMIMI_NO_MIKO, TSUKUMO_BENBEN, TSUKUMO_YATSUHASHI, USAMI_RENKO,
    USAMI_SUMIREKO, USHIZAKI_URUMI, WAKASAGIHIME, WATATSUKI_NO_TOYOHIME, WATATSUKI_NO_YORIHIME, WRIGGLE_NIGHTBUG,
    YAGOKORO_EIRIN, YAKUMO_RAN, YAKUMO_YUKARI, YAMASHIRO_TAKANE, YASAKA_KANAKO, YOMOTSU_HISAMI, YORIGAMI_JOON,
    YORIGAMI_SHION, YUIMAN_ASAMA
)
from ...user_settings import PREFERRED_IMAGE_SOURCE_TOUHOU

from .constants import (
    ACTION_TAG_BLUSH, ACTION_TAG_BULLY, ACTION_TAG_CARRY, ACTION_TAG_COSPLAY, ACTION_TAG_CRY, ACTION_TAG_DANCE,
    ACTION_TAG_FEED, ACTION_TAG_FEED_SELF, ACTION_TAG_FLUFF, ACTION_TAG_FLUFF_SELF, ACTION_TAG_HANDHOLD,
    ACTION_TAG_HAPPY, ACTION_TAG_HUG, ACTION_TAG_KISS, ACTION_TAG_KON, ACTION_TAG_LAP_SLEEP, ACTION_TAG_LICK,
    ACTION_TAG_LIKE, ACTION_TAG_MURDER, ACTION_TAG_NOM, ACTION_TAG_PAT, ACTION_TAG_PEG, ACTION_TAG_POCKY,
    ACTION_TAG_POCKY_SELF, ACTION_TAG_POKE, ACTION_TAG_RAWR, ACTION_TAG_STARE, ACTION_TAG_TICKLE, ACTION_TAG_WAVE,
    ACTION_TAG_WINK
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

# Source of lap_sleep:
#
# Source 0:
# From meiko.
#
# Source 0:
# From my pc actually.
# :KoishiPc:

# Source of stare
#
# Source 0:
# https://danbooru.donmai.us/posts?tags=touhou+staring+&z=5
# Till page 4 I think

TOUHOU_ACTION_ALL = ImageHandlerStatic(PREFERRED_IMAGE_SOURCE_TOUHOU, None)

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
).with_creator(
    'yukitarou (awamori)',
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
    'hammer (sunset beach)',
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
    'https://cdn.discordapp.com/attachments/568837922288173058/1294601987274440816/ran-satono-tmai-fluff-0000.png',
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
    'e.o.',
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
    'https://cdn.discordapp.com/attachments/568837922288173058/1294666130706665492/eiki-like-0000.png',
).with_action(
    ACTION_TAG_LIKE, None, SHIKI_EIKI_YAMAXANADU,
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294666256401829981/eirin-like-0000.png',
).with_action(
    ACTION_TAG_LIKE, None, YAGOKORO_EIRIN,
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294666256879718471/eirin-like-0001.png',
).with_action(
    ACTION_TAG_LIKE, None, YAGOKORO_EIRIN,
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294666397661794335/futatsuiwa-like-0000.png',
).with_action(
    ACTION_TAG_LIKE, None, FUTATSUIWA_MAMIZOU,
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294666583289106442/hisami-like-0000.png',
).with_action(
    ACTION_TAG_LIKE, None, YOMOTSU_HISAMI,
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294666583880368218/hisami-like-0001.png',
).with_action(
    ACTION_TAG_LIKE, None, YOMOTSU_HISAMI,
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294666824138362972/iku-like-0000.png',
).with_action(
    ACTION_TAG_LIKE, None, NAGAE_IKU,
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294667045283172486/junko-like-0000.png',
).with_action(
    ACTION_TAG_LIKE, None, JUNKO,
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294667045924769882/junko-like-0001.png',
).with_action(
    ACTION_TAG_LIKE, None, JUNKO,
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294667046335942739/junko-like-0002.png',
).with_action(
    ACTION_TAG_LIKE, None, JUNKO,
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294667286711631872/junko-like-0003.png',
).with_action(
    ACTION_TAG_LIKE, None, JUNKO,
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294667380479234069/kasen-like-0000.png',
).with_action(
    ACTION_TAG_LIKE, None, IBARAKI_KASEN,
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294667485211005038/kogasa-like-0000.png',
).with_action(
    ACTION_TAG_LIKE, None, TATARA_KOGASA,
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294667595533914234/koishi-like-0000.png',
).with_action(
    ACTION_TAG_LIKE, None, KOMEIJI_KOISHI,
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294667705722470460/miko-like-0000.png',
).with_action(
    ACTION_TAG_LIKE, None, TOYOSATOMIMI_NO_MIKO,
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294667830460940288/nitori-like-0000.png',
).with_action(
    ACTION_TAG_LIKE, None, KAWASHIRO_NITORI,
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294667943778586644/nue-like-0000.png',
).with_action(
    ACTION_TAG_LIKE, None, HOUJUU_NUE,
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294668041728295117/rinnosuke-like-0000.png',
).with_action(
    ACTION_TAG_LIKE, None, MORICHIKA_RINNOSUKE,
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294668147466436628/okina-like-0000.png',
).with_action(
    ACTION_TAG_LIKE, None, MATARA_OKINA,
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294668238575239209/okuu-like-0000.png',
).with_action(
    ACTION_TAG_LIKE, None, REIUJI_UTSUHO,
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294668366794985514/ran-like-0000.png',
).with_action(
    ACTION_TAG_LIKE, None, YAKUMO_RAN,
).with_creator(
    'terrajin',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294668488505561098/ran-like-0001.png',
).with_action(
    ACTION_TAG_LIKE, None, YAKUMO_RAN,
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294668581237424230/rumia-like-0000.png',
).with_action(
    ACTION_TAG_LIKE, None, RUMIA,
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294668686778433616/seiga-like-0000.png',
).with_action(
    ACTION_TAG_LIKE, None, KAKU_SEIGA,
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294668813371048016/seiga-like-0001.png',
).with_action(
    ACTION_TAG_LIKE, None, KAKU_SEIGA,
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294947230595158068/tewi-like-0000.png',
).with_action(
    ACTION_TAG_LIKE, None, INABA_TEWI,
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294669032347402291/yukari-like-0000.png',
).with_action(
    ACTION_TAG_LIKE, None, YAKUMO_YUKARI,
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294669356604588084/yukari-like-0001.png',
).with_action(
    ACTION_TAG_LIKE, None, YAKUMO_YUKARI,
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294669356982341642/yukari-like-0002.png',
).with_action(
    ACTION_TAG_LIKE, None, YAKUMO_YUKARI,
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294669357498236940/yukari-like-0003.png',
).with_action(
    ACTION_TAG_LIKE, None, YAKUMO_YUKARI,
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294669357997101149/yukari-like-0004.png',
).with_action(
    ACTION_TAG_LIKE, None, YAKUMO_YUKARI,
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294669358601343047/yukari-like-0005.png',
).with_action(
    ACTION_TAG_LIKE, None, YAKUMO_YUKARI,
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294669358970437734/yukari-like-0006.png',
).with_action(
    ACTION_TAG_LIKE, None, YAKUMO_YUKARI,
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294669359519629442/yukari-like-0007.png',
).with_action(
    ACTION_TAG_LIKE, None, YAKUMO_YUKARI,
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294669359851245709/yukari-yuyuko-like-0000.png',
).with_actions(
    (ACTION_TAG_LIKE, None, YAKUMO_YUKARI),
    (ACTION_TAG_LIKE, None, SAIGYOUJI_YUYUKO),
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294670912427397241/yuuka-like-0000.png',
).with_action(
    ACTION_TAG_LIKE, None, KAZAMI_YUUKA,
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294671054530150450/yuuka-like-0001.png',
).with_action(
    ACTION_TAG_LIKE, None, KAZAMI_YUUKA,
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294676825221369887/yuyuko-like-0000.png',
).with_action(
    ACTION_TAG_LIKE, None, SAIGYOUJI_YUYUKO,
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294676826064687144/yuyuko-like-0001.png',
).with_action(
    ACTION_TAG_LIKE, None, SAIGYOUJI_YUYUKO,
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294676826534314035/yuyuko-like-0002.png',
).with_action(
    ACTION_TAG_LIKE, None, SAIGYOUJI_YUYUKO,
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294676827121389568/yuyuko-like-0003.png',
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
    (ACTION_TAG_POCKY, HIEDA_NO_AKYUU, MOTOORI_KOSUZU),
    (ACTION_TAG_POCKY, MOTOORI_KOSUZU, HIEDA_NO_AKYUU),
).with_creator(
    'nekolina',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1223995355973156985/alice-marisa-pocky-0000.png',
).with_actions(
    (ACTION_TAG_POCKY, KIRISAME_MARISA, MARGATROID_ALICE),
    (ACTION_TAG_POCKY, MARGATROID_ALICE, KIRISAME_MARISA),
).with_creator(
    'manjuu teishoku / 饅頭定食',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1223996169852686377/alice-mystia-pocky-0000.png',
).with_actions(
    (ACTION_TAG_POCKY, LORELEI_MYSTIA, MARGATROID_ALICE),
    (ACTION_TAG_POCKY, MARGATROID_ALICE, LORELEI_MYSTIA),
).with_creator(
    'ayagi daifuku',
).with_editor(
    'HuyaneMatsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1223993131884609596/aya-hatate-pocky-0000.png',
).with_actions(
    (ACTION_TAG_POCKY, HIMEKAIDOU_HATATE, SHAMEIMARU_AYA),
    (ACTION_TAG_POCKY, SHAMEIMARU_AYA, HIMEKAIDOU_HATATE),
).with_creator(
    'coco (r5m)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1155416757964640266/aya-remilia-pocky-0000.png',
).with_action(
    ACTION_TAG_POCKY, SCARLET_REMILIA, SHAMEIMARU_AYA,
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1155417439706824734/chen-orin-pocky-0000.png',
).with_actions(
    (ACTION_TAG_POCKY, CHEN, KAENBYOU_RIN),
    (ACTION_TAG_POCKY, KAENBYOU_RIN, CHEN),
).with_creator(
    'fujimiya kikyou / 藤見屋桔梗',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1155418080961368074/chen-ran-pocky-0000.png',
).with_action(
    ACTION_TAG_POCKY, CHEN, YAKUMO_RAN,
).with_creator(
    'gustav / ぐすたふ',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1223997595039567882/chen-ran-pocky-0001.png',
).with_actions(
    (ACTION_TAG_POCKY, YAKUMO_RAN, CHEN),
    (ACTION_TAG_POCKY, CHEN, YAKUMO_RAN),
).with_creator(
    'japa / じゃぱ',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1223997595391754260/chen-ran-pocky-0002.png',
).with_action(
    ACTION_TAG_POCKY, CHEN, YAKUMO_RAN,
).with_creator(
    'japa / じゃぱ',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1155418521304563732/chiruno-dai-pocky-0000.png',
).with_actions(
    (ACTION_TAG_POCKY, CHIRUNO, DAIYOUSEI),
    (ACTION_TAG_POCKY, DAIYOUSEI, CHIRUNO),
).with_creator(
    'mamemochi / まめもち',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1224002839488106577/chiruno-rumia-pocky-0000.png',
).with_action(
    ACTION_TAG_POCKY, CHIRUNO, RUMIA,
).with_creator(
    'torichiyo / とりちよ',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1236210240312180816/flandre-koishi-remilia-satori-pocky-0000.png',
).with_actions(
    (ACTION_TAG_POCKY, KOMEIJI_KOISHI, SCARLET_FLANDRE),
    (ACTION_TAG_POCKY, SCARLET_FLANDRE, KOMEIJI_KOISHI),
).with_characters(
    SCARLET_REMILIA, KOMEIJI_SATORI,
).with_creator(
    'minamura haruki / 皆 村',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1223993460541882378/flandre-koishi-pocky-0001.png',
).with_action(
    ACTION_TAG_POCKY, KOMEIJI_KOISHI, SCARLET_FLANDRE,
).with_creator(
    'Teeku / てぇく',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1223993460865110076/flandre-koishi-pocky-0002.png',
).with_action(
    ACTION_TAG_POCKY, KOMEIJI_KOISHI, SCARLET_FLANDRE,
).with_creator(
    'shan',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1155419036797124628/flandre-remilia-pocky-0000.png',
).with_action(
    ACTION_TAG_POCKY, SCARLET_FLANDRE, SCARLET_REMILIA,
).with_creator(
    'sakrear',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1155419380402892880/flandre-remilia-pocky-0001.png',
).with_action(
    ACTION_TAG_POCKY, SCARLET_FLANDRE, SCARLET_REMILIA,
).with_creator(
    'sakrear',
).with_editor(
    'Scarlet Flandre',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1224001610129342636/flandre-remilia-pocky-0002.png',
).with_action(
    ACTION_TAG_POCKY, SCARLET_FLANDRE, SCARLET_REMILIA,
).with_creator(
    'fumi11',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1224001610565292133/flandre-remilia-pocky-0003.png',
).with_action(
    ACTION_TAG_POCKY, SCARLET_FLANDRE, SCARLET_REMILIA,
).with_creator(
    'kusogappa',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1155420220245155850/kagerou-remilia-pocky-0000.png',
).with_actions(
    (ACTION_TAG_POCKY, IMAIZUMI_KAGEROU, SCARLET_REMILIA),
    (ACTION_TAG_POCKY, SCARLET_REMILIA, IMAIZUMI_KAGEROU),
).with_creator(
    'ziran de ph shizhi tuan / 自燃的ph试纸团',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1224000873089339552/kagerou-wakasagihime-pocky-0000.png',
).with_action(
    ACTION_TAG_POCKY, WAKASAGIHIME, IMAIZUMI_KAGEROU,
).with_creator(
    'kaginoni / かぎのに',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1224004869220728912/kanako-suwako-pocky-0000.png',
).with_action(
    ACTION_TAG_POCKY, MORIYA_SUWAKO, YASAKA_KANAKO,
).with_creator(
    'keemoringo',
).with_editor(
    'HuyaneMatsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1155420854105157742/keine-mokou-pocky-0000.png',
).with_actions(
    (ACTION_TAG_POCKY, KAMISHIRASAWA_KEINE, FUJIWARA_NO_MOKOU),
    (ACTION_TAG_POCKY, FUJIWARA_NO_MOKOU, KAMISHIRASAWA_KEINE),
).with_creator(
    'zawameki / ざわめき',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1155421417085603850/keine-mokou-pocky-0001.png',
).with_action(
    ACTION_TAG_POCKY, FUJIWARA_NO_MOKOU, KAMISHIRASAWA_KEINE,
).with_creator(
    'hijikawa arashi / 肱川 嵐',
).with_editor(
    'HuyaneMatsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1223995601637609512/keine-mokou-pocky-0002.png',
).with_action(
    ACTION_TAG_POCKY, FUJIWARA_NO_MOKOU, KAMISHIRASAWA_KEINE,
).with_creator(
    '6',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1224003250492018698/koakuma-sakuya-pocky-0000.png',
).with_action(
    ACTION_TAG_POCKY, IZAYOI_SAKUYA, KOAKUMA,
).with_creator(
    '3692materia / 浅間清正',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1223996582148571277/kogasa-nue-pocky-0000.png',
).with_actions(
    (ACTION_TAG_POCKY, HOUJUU_NUE, TATARA_KOGASA),
    (ACTION_TAG_POCKY, TATARA_KOGASA, HOUJUU_NUE),
).with_creator(
    'kitano / きたの！',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1155423779367944242/koishi-kokoro-pocky-0000.png',
).with_action(
    ACTION_TAG_POCKY, KOMEIJI_KOISHI, HATA_NO_KOKORO,
).with_creator(
    'cato',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1223992298376007750/koishi-kokoro-pocky-0001.png',
).with_actions(
    (ACTION_TAG_POCKY, KOMEIJI_KOISHI, HATA_NO_KOKORO),
    (ACTION_TAG_POCKY, HATA_NO_KOKORO, KOMEIJI_KOISHI),
).with_creator(
    'kiryuu soma',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1223994561941209089/koishi-kokoro-pocky-0002.png',
).with_actions(
    (ACTION_TAG_POCKY, HATA_NO_KOKORO, KOMEIJI_KOISHI),
    (ACTION_TAG_POCKY, KOMEIJI_KOISHI, HATA_NO_KOKORO),
).with_creator(
    'Zan / ざん',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1155424037099544632/koishi-satori-pocky-0000.png',
).with_action(
    ACTION_TAG_POCKY, KOMEIJI_KOISHI, KOMEIJI_SATORI,
).with_creator(
    'komaku juushoku / 鼓膜住職',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1155424507054530600/koishi-satori-pocky-0001.png',
).with_actions(
    (ACTION_TAG_POCKY, KOMEIJI_KOISHI, KOMEIJI_SATORI),
    (ACTION_TAG_POCKY, KOMEIJI_SATORI, KOMEIJI_KOISHI),
).with_creator(
    'gochou / 伍長',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1223534649738006641/koishi-satori-pocky-0002.gif',
).with_action(
    ACTION_TAG_POCKY, KOMEIJI_KOISHI, KOMEIJI_SATORI,
).with_creator(
    'satori suki',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294608422272106579/lily_white-rumia-pocky-0000.png',
).with_actions(
    (ACTION_TAG_POCKY, LILY_WHITE, RUMIA),
    (ACTION_TAG_POCKY, RUMIA, LILY_WHITE),
).with_creator(
    'mitsubasa miu / 魅翼',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1232749283888070788/mamizou-ran-pocky-0000.png',
).with_action(
    ACTION_TAG_POCKY, YAKUMO_RAN, FUTATSUIWA_MAMIZOU,
).with_creator(
    'littlecloudie',
).with_editor(
    'HuyaneMatsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1155425812003180584/maribel-renko-pocky-0000.png',
).with_actions(
    (ACTION_TAG_POCKY, HEARN_MARIBEL, USAMI_RENKO),
    (ACTION_TAG_POCKY, USAMI_RENKO, HEARN_MARIBEL),
).with_creator(
    'senba chidori / 千羽チドリ',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1224002516287492250/maribel-renko-pocky-0001.png',
).with_action(
    ACTION_TAG_POCKY, USAMI_RENKO, HEARN_MARIBEL,
).with_creator(
    'imi_humei / フメイ',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1224002516686213120/maribel-renko-pocky-0002.png',
).with_action(
    ACTION_TAG_POCKY, USAMI_RENKO, HEARN_MARIBEL,
).with_creator(
    'tsukiori sasa / 月居咲々',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1155427814682669170/marisa-reimu-pocky-0000.png',
).with_actions(
    (ACTION_TAG_POCKY, KIRISAME_MARISA, HAKUREI_REIMU),
    (ACTION_TAG_POCKY, HAKUREI_REIMU, KIRISAME_MARISA),
).with_creator(
    'uyu-nagi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1155428193940013106/marisa-reimu-pocky-0001.png',
).with_action(
    ACTION_TAG_POCKY, KIRISAME_MARISA, HAKUREI_REIMU,
).with_creator(
    'hitte5416 / 辣酱',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1155428618940452954/marisa-reimu-pocky-0002.png',
).with_action(
    ACTION_TAG_POCKY, KIRISAME_MARISA, HAKUREI_REIMU,
).with_creator(
    'ookashippo / 大岡尻尾',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1155428858112254002/marisa-reimu-pocky-0003.png',
).with_actions(
    (ACTION_TAG_POCKY, KIRISAME_MARISA, HAKUREI_REIMU),
    (ACTION_TAG_POCKY, HAKUREI_REIMU, KIRISAME_MARISA),
).with_creator(
    'pasutel',
).with_editor(
    'HuyaneMatsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1224001376967983104/marisa-reimu-pocky-0004.png',
).with_actions(
    (ACTION_TAG_POCKY, HAKUREI_REIMU, KIRISAME_MARISA),
    (ACTION_TAG_POCKY, KIRISAME_MARISA, HAKUREI_REIMU),
).with_creator(
    'iwatobi hiro / いわとび ひろ',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1155429318013493288/meiling-sakuya-pocky-0000.png',
).with_action(
    ACTION_TAG_POCKY, HONG_MEILING, IZAYOI_SAKUYA,
).with_creator(
    'yuuta / 勇太',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1224003529597784165/meiling-sakuya-pocky-0001.png',
).with_action(
    ACTION_TAG_POCKY, HONG_MEILING, IZAYOI_SAKUYA,
).with_creator(
    'tima',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1155430157331472394/minamitsu-nue-pocky-0000.png',
).with_action(
    ACTION_TAG_POCKY, MURASA_MINAMITSU, HOUJUU_NUE,
).with_creator(
    'hisona',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1223999446355017958/mystia-rumia-pocky-0000.png',
).with_action(
    ACTION_TAG_POCKY, RUMIA, LORELEI_MYSTIA,
).with_creator(
    'earlgrey',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1223998997077954560/mystia-yuyuko-pocky-0000.png',
).with_action(
    ACTION_TAG_POCKY, SAIGYOUJI_YUYUKO, LORELEI_MYSTIA,
).with_creator(
    'nise nanatsura',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1155431623265894540/nazrin-shou-pocky-0000.png',
).with_action(
    ACTION_TAG_POCKY, TORAMARU_SHOU, NAZRIN,
).with_creator(
    'masha',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1224004228310368407/nazrin-shou-pocky-0001.png',
).with_action(
    ACTION_TAG_POCKY, NAZRIN, TORAMARU_SHOU,
).with_creator(
    'bbb',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1155432393444950046/patchouli-remilia-pocky-0000.png',
).with_actions(
    (ACTION_TAG_POCKY, PATCHOULI_KNOWLEDGE, SCARLET_REMILIA),
    (ACTION_TAG_POCKY, SCARLET_REMILIA, PATCHOULI_KNOWLEDGE),
).with_creator(
    'sakaetomoyuu / 栄智ゆう',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1224000604205092965/patchouli-youmo-pocky-0000.png',
).with_action(
    ACTION_TAG_POCKY, PATCHOULI_KNOWLEDGE, KONPAKU_YOUMU,
).with_creator(
    'nigo',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1259050670812561439/reimu-suika-pocky-0000.png',
).with_actions(
    (ACTION_TAG_POCKY, HAKUREI_REIMU, IBUKI_SUIKA),
    (ACTION_TAG_POCKY, IBUKI_SUIKA, HAKUREI_REIMU),
).with_creator(
    'shinekalta',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1224004617533132872/reimu-tenshi-pocky-0000.png',
).with_action(
    ACTION_TAG_POCKY, HINANAWI_TENSHI, HAKUREI_REIMU,
).with_creator(
    'ichiyan',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1223998031574339635/reimu-yukari-youmu-yuyuko-pocky-0000.png',
).with_actions(
    (ACTION_TAG_POCKY, SAIGYOUJI_YUYUKO, YAKUMO_YUKARI),
    (ACTION_TAG_POCKY, YAKUMO_YUKARI, SAIGYOUJI_YUYUKO),
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
    ACTION_TAG_POCKY, SCARLET_REMILIA, KOMEIJI_SATORI,
).with_creator(
    'Genbu / げんぶ',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1224005371627180032/sanae-suwako-pocky-0000.png',
).with_actions(
    (ACTION_TAG_POCKY, MORIYA_SUWAKO, KOCHIYA_SANAE),
    (ACTION_TAG_POCKY, KOCHIYA_SANAE, MORIYA_SUWAKO),
).with_creator(
    'cis',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1224000265007665192/sanae-youmu-pocky-0000.png',
).with_action(
    ACTION_TAG_POCKY, KONPAKU_YOUMU, KOCHIYA_SANAE,
).with_creator(
    'Shirota Shinobu / 白田 忍',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1208773143200661554/satori-suika-pocky-0000.png',
).with_actions(
    (ACTION_TAG_POCKY, KOMEIJI_SATORI, IBUKI_SUIKA),
    (ACTION_TAG_POCKY, IBUKI_SUIKA, KOMEIJI_SATORI),
).with_creator(
    'Scarristo',
).with_editor(
    'HuyaneMatsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294657520828158045/aya-pocky_self-0000.png',
).with_action(
    ACTION_TAG_POCKY_SELF, SHAMEIMARU_AYA, SHAMEIMARU_AYA,
).with_creator(
    'futatsuki eru',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294657775820869632/byakuren-pocky_self-0000.png',
).with_action(
    ACTION_TAG_POCKY_SELF, HIJIRI_BYAKUREN, HIJIRI_BYAKUREN,
).with_creator(
    'cpu (hexivision)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294657856360026113/byakuren-pocky_self-0001.png',
).with_action(
    ACTION_TAG_POCKY_SELF, HIJIRI_BYAKUREN, HIJIRI_BYAKUREN,
).with_creator(
    'han (jackpot)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294657989730631763/chiruno-pocky_self-0000.png',
).with_action(
    ACTION_TAG_POCKY_SELF, CHIRUNO, CHIRUNO,
).with_creator(
    'shokuyou pants',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294658141946118204/eiki-pocky_self-0000.png',
).with_action(
    ACTION_TAG_POCKY_SELF, SHIKI_EIKI_YAMAXANADU, SHIKI_EIKI_YAMAXANADU,
).with_creator(
    'guard vent jun',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294658451410255902/flandre-pocky_self-0000.png',
).with_action(
    ACTION_TAG_POCKY_SELF, SCARLET_FLANDRE, SCARLET_FLANDRE,
).with_creator(
    'mamemochi',
).with_editor(
    'HuyaneMatsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294658452496318506/flandre-pocky_self-0001.png',
).with_action(
    ACTION_TAG_POCKY_SELF, SCARLET_FLANDRE, SCARLET_FLANDRE,
).with_creator(
    'zerocat',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294658453159153775/flandre-pocky_self-0002.png',
).with_action(
    ACTION_TAG_POCKY_SELF, SCARLET_FLANDRE, SCARLET_FLANDRE,
).with_creator(
    'puuakachan',
).with_editor(
    'HuyaneMatsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294658453641367573/flandre-pocky_self-0003.png',
).with_action(
    ACTION_TAG_POCKY_SELF, SCARLET_FLANDRE, SCARLET_FLANDRE,
).with_creator(
    'sasurai no kuchibuefuki',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294658454161588254/flandre-pocky_self-0004.png',
).with_action(
    ACTION_TAG_POCKY_SELF, SCARLET_FLANDRE, SCARLET_FLANDRE,
).with_creator(
    'takamoto akisa',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294658454509850634/flandre-pocky_self-0005.png',
).with_action(
    ACTION_TAG_POCKY_SELF, SCARLET_FLANDRE, SCARLET_FLANDRE,
).with_creator(
    'tosura-ayato',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294658454908305438/flandre-pocky_self-0006.png',
).with_action(
    ACTION_TAG_POCKY_SELF, SCARLET_FLANDRE, SCARLET_FLANDRE,
).with_creator(
    'misa (kaeruhitode)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294659030438121623/futo-pocky_self-0000.png',
).with_action(
    ACTION_TAG_POCKY_SELF, MONONOBE_NO_FUTO, MONONOBE_NO_FUTO,
).with_creator(
    'kuzumomo',
).with_editor(
    'HuyaneMatsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294659200601034923/hatate-pocky_self-0000.png',
).with_action(
    ACTION_TAG_POCKY_SELF, HIMEKAIDOU_HATATE, HIMEKAIDOU_HATATE,
).with_creator(
    'shiranui (wasuresateraito)',
).with_editor(
    'HuyaneMatsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294659207613648957/hatate-pocky_pocky-0001.png',
).with_action(
    ACTION_TAG_POCKY_SELF, HIMEKAIDOU_HATATE, HIMEKAIDOU_HATATE,
).with_creator(
    '*gomi (gomitin)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294659412883017880/iku-pocky_self-0000.png',
).with_action(
    ACTION_TAG_POCKY_SELF, NAGAE_IKU, NAGAE_IKU,
).with_creator(
    'etosen',
).with_editor(
    'HuyaneMatsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294659576020336650/kagerou-pocky_self-0000.png',
).with_action(
    ACTION_TAG_POCKY_SELF, IMAIZUMI_KAGEROU, IMAIZUMI_KAGEROU,
).with_creator(
    'rokugou daisuke',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294659576540565616/kagerou-pocky_self-0001.png',
).with_action(
    ACTION_TAG_POCKY_SELF, IMAIZUMI_KAGEROU, IMAIZUMI_KAGEROU,
).with_creator(
    'tetsuhige / 鉄髭',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294659891746836570/keine-pocky_self-0000.png',
).with_action(
    ACTION_TAG_POCKY_SELF, KAMISHIRASAWA_KEINE, KAMISHIRASAWA_KEINE,
).with_creator(
    'rebecca (keinelove)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294659998600663051/kogasa-pocky_self-0000.png',
).with_action(
    ACTION_TAG_POCKY_SELF, TATARA_KOGASA, TATARA_KOGASA,
).with_creator(
    'muginon',
).with_editor(
    'HuyaneMatsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294660157766369401/koishi-pocky_self-0000.png',
).with_action(
    ACTION_TAG_POCKY_SELF, KOMEIJI_KOISHI, KOMEIJI_KOISHI,
).with_creator(
    'oshiaki',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294660158143594506/koishi-pocky_self-0001.png',
).with_action(
    ACTION_TAG_POCKY_SELF, KOMEIJI_KOISHI, KOMEIJI_KOISHI,
).with_creator(
    'sukima (crie)',
).with_editor(
    'HuyaneMatsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294660158554902528/koishi-pocky_self-0002.png',
).with_action(
    ACTION_TAG_POCKY_SELF, KOMEIJI_KOISHI, KOMEIJI_KOISHI,
).with_creator(
    'ocha (ochappie)',
).with_editor(
    'HuyaneMatsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294660388297904178/kokoro-pocky_self-0000.png',
).with_action(
    ACTION_TAG_POCKY_SELF, HATA_NO_KOKORO, HATA_NO_KOKORO,
).with_creator(
    'hammer (sunset beach)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294660508745465958/komachi-pocky_self-0000.png',
).with_action(
    ACTION_TAG_POCKY_SELF, ONOZUKA_KOMACHI, ONOZUKA_KOMACHI,
).with_creator(
    'harakune (mugennero)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294660817723064320/lily_black-pocky_self-0000.png',
).with_action(
    ACTION_TAG_POCKY_SELF, LILY_BLACK, LILY_BLACK,
).with_creator(
    'earlgrey',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294660818105008179/lily_white-pocky_self-0000.png',
).with_action(
    ACTION_TAG_POCKY_SELF, LILY_WHITE, LILY_WHITE,
).with_creator(
    'nonotan',
).with_editor(
    'HuyaneMatsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294660986447335505/marisa-pocky_self-0000.png',
).with_action(
    ACTION_TAG_POCKY_SELF, KIRISAME_MARISA, KIRISAME_MARISA,
).with_creator(
    'e.o.',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294660986871091342/marisa-pocky_self-0001.png',
).with_action(
    ACTION_TAG_POCKY_SELF, KIRISAME_MARISA, KIRISAME_MARISA,
).with_creator(
    'sanpa',
).with_editor(
    'HuyaneMatsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294661163086381087/medi-pocky_self-0000.png',
).with_action(
    ACTION_TAG_POCKY_SELF, MEDICINE_MELANCHOLY, MEDICINE_MELANCHOLY,
).with_creator(
    'dqn (dqnww)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294661288055537755/miko-pocky_self-0000.png',
).with_action(
    ACTION_TAG_POCKY_SELF, TOYOSATOMIMI_NO_MIKO, TOYOSATOMIMI_NO_MIKO,
).with_creator(
    'makuwauri',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294661408901828628/mokou-pocky_self-0000.png',
).with_action(
    ACTION_TAG_POCKY_SELF, FUJIWARA_NO_MOKOU, FUJIWARA_NO_MOKOU,
).with_creator(
    'hijikawa arashi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294661409313001532/mokou-pocky_self-0001.png',
).with_action(
    ACTION_TAG_POCKY_SELF, FUJIWARA_NO_MOKOU, FUJIWARA_NO_MOKOU,
).with_creator(
    'hiyori-o',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294661626657640498/momiji-pocky_self-0000.png',
).with_action(
    ACTION_TAG_POCKY_SELF, INUBASHIRI_MOMIJI, INUBASHIRI_MOMIJI,
).with_creator(
    'elu butyo',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294661627089522768/momiji-pocky_self-0001.png',
).with_action(
    ACTION_TAG_POCKY_SELF, INUBASHIRI_MOMIJI, INUBASHIRI_MOMIJI,
).with_creator(
    'katsumi5o',
).with_editor(
    'HuyaneMatsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294661627563475065/momiji-pocky_self-0002.png',
).with_action(
    ACTION_TAG_POCKY_SELF, INUBASHIRI_MOMIJI, INUBASHIRI_MOMIJI,
).with_creators(
    'ginzake (mizuumi)', 'shake (sakana)',
).with_editor(
    'HuyaneMatsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294661887946133504/mystia-pocky_self-0000.png',
).with_action(
    ACTION_TAG_POCKY_SELF, LORELEI_MYSTIA, LORELEI_MYSTIA,
).with_creator(
    'phantom2071',
).with_editor(
    'HuyaneMatsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294661999875199059/nazrin-pocky_self-0000.png',
).with_action(
    ACTION_TAG_POCKY_SELF, NAZRIN, NAZRIN,
).with_creator(
    'kibayashi kimori',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294662169304105065/nue-pocky_self-0000.png',
).with_action(
    ACTION_TAG_POCKY_SELF, HOUJUU_NUE, HOUJUU_NUE,
).with_creator(
    'makita (vector1525)',
).with_editor(
    'HuyaneMatsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294662169706762372/nue-pocky_self-0001.png',
).with_action(
    ACTION_TAG_POCKY_SELF, HOUJUU_NUE, HOUJUU_NUE,
).with_creator(
    'igakusei',
).with_editor(
    'HuyaneMatsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294662344399523860/okuu-pocky_self-0000.png',
).with_action(
    ACTION_TAG_POCKY_SELF, REIUJI_UTSUHO, REIUJI_UTSUHO,
).with_creator(
    'sinzan',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294662464507609088/orin-pocky_self-0000.png',
).with_action(
    ACTION_TAG_POCKY_SELF, KAENBYOU_RIN, KAENBYOU_RIN,
).with_creator(
    'kuromari (runia)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294662464822186024/orin-pocky_self-0001.png',
).with_action(
    ACTION_TAG_POCKY_SELF, KAENBYOU_RIN, KAENBYOU_RIN,
).with_creators(
    'takasu', 'tks (chikuwa)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294662647802757193/patchouli-pocky_self-0000.png',
).with_action(
    ACTION_TAG_POCKY_SELF, PATCHOULI_KNOWLEDGE, PATCHOULI_KNOWLEDGE,
).with_creator(
    'namiki (remiter00)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294662648092426301/patchouli-pocky_self-0001.png',
).with_action(
    ACTION_TAG_POCKY_SELF, PATCHOULI_KNOWLEDGE, PATCHOULI_KNOWLEDGE,
).with_creator(
    'natsuki (silent selena)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294662648465723434/patchouli-pocky_self-0002.png',
).with_action(
    ACTION_TAG_POCKY_SELF, PATCHOULI_KNOWLEDGE, PATCHOULI_KNOWLEDGE,
).with_creator(
    'porurin (do-desho)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294662903747579960/ran-pocky_self-0000.png',
).with_action(
    ACTION_TAG_POCKY_SELF, YAKUMO_RAN, YAKUMO_RAN,
).with_creator(
    'dearmybrothers',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294662904187977838/ran-pocky_self-0001.png',
).with_action(
    ACTION_TAG_POCKY_SELF, YAKUMO_RAN, YAKUMO_RAN,
).with_creator(
    'dearmybrothers',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294663083553456239/reimu-pocky_self-0000.png',
).with_action(
    ACTION_TAG_POCKY_SELF, HAKUREI_REIMU, HAKUREI_REIMU,
).with_creators(
    'h sakray', 'sakurai haruto',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294663083884679260/reimu-pocky_self-0001.png',
).with_action(
    ACTION_TAG_POCKY_SELF, HAKUREI_REIMU, HAKUREI_REIMU,
).with_creator(
    'aosi (wasabiranzy)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294663084194926592/reimu-pocky_self-0002.png',
).with_action(
    ACTION_TAG_POCKY_SELF, HAKUREI_REIMU, HAKUREI_REIMU,
).with_creator(
    'pasutel',
).with_editor(
    'HuyaneMatsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294663420431302728/remilia-pocky_self-0000.png',
).with_action(
    ACTION_TAG_POCKY_SELF, SCARLET_REMILIA, SCARLET_REMILIA,
).with_creator(
    'beni kurage',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294663421601644544/remilia-pocky_self-0001.png',
).with_action(
    ACTION_TAG_POCKY_SELF, SCARLET_REMILIA, SCARLET_REMILIA,
).with_creator(
    'yamasuta',
).with_editor(
    'HuyaneMatsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294663421966680198/remilia-pocky_self-0002.png',
).with_action(
    ACTION_TAG_POCKY_SELF, SCARLET_REMILIA, SCARLET_REMILIA,
).with_creator(
    'misa (kaeruhitode)',
).with_editor(
    'HuyaneMatsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294663646428921887/rumia-pocky_self-0000.png',
).with_action(
    ACTION_TAG_POCKY_SELF, RUMIA, RUMIA,
).with_creator(
    'natoubee',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294663752574308425/sakuya-pocky_self-0000.png',
).with_action(
    ACTION_TAG_POCKY_SELF, IZAYOI_SAKUYA, IZAYOI_SAKUYA,
).with_creator(
    'caramell0501',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294663895167795242/sanae-pocky_self-0000.png',
).with_action(
    ACTION_TAG_POCKY_SELF, KOCHIYA_SANAE, KOCHIYA_SANAE,
).with_creator(
    'fueiku',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294663895583162448/sanae-pocky_self-0001.png',
).with_action(
    ACTION_TAG_POCKY_SELF, KOCHIYA_SANAE, KOCHIYA_SANAE,
).with_creator(
    'osashin (osada)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294664088328208406/satori-pocky_self-0000.png',
).with_action(
    ACTION_TAG_POCKY_SELF, KOMEIJI_SATORI, KOMEIJI_SATORI,
).with_creator(
    'noumin joemanyodw',
).with_editor(
    'HuyaneMatsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294664088802299945/satori-pocky_self-0001.png',
).with_action(
    ACTION_TAG_POCKY_SELF, KOMEIJI_SATORI, KOMEIJI_SATORI,
).with_creator(
    'toritori (yakitoriya)',
).with_editor(
    'HuyaneMatsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294664313830772826/suwako-pocky_self-0000.png',
).with_action(
    ACTION_TAG_POCKY_SELF, MORIYA_SUWAKO, MORIYA_SUWAKO,
).with_creator(
    'gamuo',
).with_editor(
    'HuyaneMatsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294664433490071573/tenshi-pocky_self-0000.png',
).with_action(
    ACTION_TAG_POCKY_SELF, HINANAWI_TENSHI, HINANAWI_TENSHI,
).with_creator(
    'ruu (tksymkw)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294664580118872146/wriggle-pocky_self-0000.png',
).with_action(
    ACTION_TAG_POCKY_SELF, WRIGGLE_NIGHTBUG, WRIGGLE_NIGHTBUG,
).with_creator(
    'kajiyama',
).with_editor(
    'HuyaneMatsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294664580487843892/wriggle-pocky_self-0001.png',
).with_action(
    ACTION_TAG_POCKY_SELF, WRIGGLE_NIGHTBUG, WRIGGLE_NIGHTBUG,
).with_creator(
    'cato (monocatienus)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294664863691313182/youmu-pocky_self-0000.png',
).with_action(
    ACTION_TAG_POCKY_SELF, KONPAKU_YOUMU, KONPAKU_YOUMU,
).with_creator(
    'shironeko yuuki',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294664864731496448/youmu-pocky_self-0001.png',
).with_action(
    ACTION_TAG_POCKY_SELF, KONPAKU_YOUMU, KONPAKU_YOUMU,
).with_creator(
    'kame (kamepan44231)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294664865264435251/youmu-pocky_self-0002.png',
).with_action(
    ACTION_TAG_POCKY_SELF, KONPAKU_YOUMU, KONPAKU_YOUMU,
).with_creator(
    'moni monico',
).with_editor(
    'HuyaneMatsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294664865570361385/youmu-pocky_self-0003.png',
).with_action(
    ACTION_TAG_POCKY_SELF, KONPAKU_YOUMU, KONPAKU_YOUMU,
).with_creator(
    'katanakko daisuki',
).with_editor(
    'HuyaneMatsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294664865901969509/youmu-pocky_self-0004.png',
).with_action(
    ACTION_TAG_POCKY_SELF, KONPAKU_YOUMU, KONPAKU_YOUMU,
).with_creator(
    'enelis',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294665161990475786/yukari-pocky_self-0000.png',
).with_action(
    ACTION_TAG_POCKY_SELF, YAKUMO_YUKARI, YAKUMO_YUKARI,
).with_creator(
    'yoshihiro-m',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294665298812600330/yuuka-pocky_self-0000.png',
).with_action(
    ACTION_TAG_POCKY_SELF, KAZAMI_YUUKA, KAZAMI_YUUKA,
).with_creator(
    'kanta (pixiv9296614)',
).with_editor(
    'HuyaneMatsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294665299236356219/yuuka-pocky_self-0001.png',
).with_action(
    ACTION_TAG_POCKY_SELF, KAZAMI_YUUKA, KAZAMI_YUUKA,
).with_creator(
    'mokku',
).with_editor(
    'HuyaneMatsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294665299571769434/yuuka-pocky_self-0002.png',
).with_action(
    ACTION_TAG_POCKY_SELF, KAZAMI_YUUKA, KAZAMI_YUUKA,
).with_creator(
    'roki (hirokix)',
).with_editor(
    'HuyaneMatsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294665546159099945/yuyuko-pocky_self-0000.png',
).with_action(
    ACTION_TAG_POCKY_SELF, SAIGYOUJI_YUYUKO, SAIGYOUJI_YUYUKO,
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
    'https://cdn.discordapp.com/attachments/568837922288173058/1308909254760988773/doremy-sagume-lap_sleep-0000.png',
).with_action(
    ACTION_TAG_LAP_SLEEP, DOREMY_SWEET, KISHIN_SAGUME,
).with_creator(
    'muyue',
).with_editor(
    'HuyaneMatsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1308912673588514917/reisen-tewi-lap_sleep-0000.png',
).with_action(
    ACTION_TAG_LAP_SLEEP, INABA_TEWI, REISEN_UDONGEIN_INABA,
).with_creator(
    'shirosato',
).with_editor(
    'HuyaneMatsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1308908922207473694/kanako-suwako-lap_sleep-0000.png',
).with_action(
    ACTION_TAG_LAP_SLEEP, MORIYA_SUWAKO, YASAKA_KANAKO,
).with_creator(
    'ame iru',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1308907988391690330/marisa-nazrin-lap_sleep-0000.png',
).with_action(
    ACTION_TAG_LAP_SLEEP, NAZRIN, KIRISAME_MARISA,
).with_creator(
    'sznkrs',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1308910047421530223/kaguya-mokou-lap_sleep-0000.png',
).with_action(
    ACTION_TAG_LAP_SLEEP, FUJIWARA_NO_MOKOU, HOURAISAN_KAGUYA,
).with_creator(
    'jiege',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1308911077957828608/keine-mokou-lap_sleep-0000.png',
).with_action(
    ACTION_TAG_LAP_SLEEP, FUJIWARA_NO_MOKOU, KAMISHIRASAWA_KEINE,
).with_creator(
    'eichi yuu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1308908539950927943/koishi-satori-lap_sleep-0000.png',
).with_action(
    ACTION_TAG_LAP_SLEEP, KOMEIJI_KOISHI, KOMEIJI_SATORI,
).with_creator(
    'tsugetsuge',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1308909899631165531/keiki-mayumi-lap_sleep-0000.png',
).with_action(
    ACTION_TAG_LAP_SLEEP, JOUTOUGUU_MAYUMI, HANIYASUSHIN_KEIKI,
).with_creator(
    'yamase',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1308907461356421150/futo-miko-tojiko-lap_sleep-0000.png',
).with_actions(
    (ACTION_TAG_LAP_SLEEP, MONONOBE_NO_FUTO, SOGA_NO_TOJIKO),
    (ACTION_TAG_LAP_SLEEP, TOYOSATOMIMI_NO_MIKO, SOGA_NO_TOJIKO),
).with_creator(
    'ashiyu (ashu ashu)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1308909757817552997/marisa-reimu-lap_sleep-0000.png',
).with_action(
    ACTION_TAG_LAP_SLEEP, KIRISAME_MARISA, HAKUREI_REIMU,
).with_creator(
    'muzuki uruu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1308908137599995946/maribel-renko-lap_sleep-0000.png',
).with_action(
    ACTION_TAG_LAP_SLEEP, HEARN_MARIBEL, USAMI_RENKO,
).with_creator(
    'fuukadia (narcolepsy)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1308907790735118337/chen-ran-yukari-lap_sleep-0000.png',
).with_action(
    ACTION_TAG_LAP_SLEEP, CHEN, YAKUMO_RAN,
).with_character(
    YAKUMO_YUKARI,
).with_creator(
    'chanta (ayatakaoisii)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1308912450652995634/chen-ran-lap_sleep-0000.png',
).with_action(
    ACTION_TAG_LAP_SLEEP, CHEN, YAKUMO_RAN,
).with_creator(
    'namuko',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1308908740807757885/kanako-suwako-lap_sleep-0001.png',
).with_action(
    ACTION_TAG_LAP_SLEEP, MORIYA_SUWAKO, YASAKA_KANAKO,
).with_creator(
    'wataichi meko',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1308910941106081873/mamizou-nue-lap_sleep-0000.png',
).with_action(
    ACTION_TAG_LAP_SLEEP, HOUJUU_NUE, FUTATSUIWA_MAMIZOU,
).with_creator(
    'daniwae',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1308907044409180180/flandre-remilia-sakuya-lap_sleep-0000.png',
).with_action(
    ACTION_TAG_LAP_SLEEP, SCARLET_REMILIA, SCARLET_FLANDRE,
).with_character(
    IZAYOI_SAKUYA,
).with_creator(
    'satou kibi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1308909441260851304/shion-tenshi-lap_sleep-0000.png',
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
    'https://cdn.discordapp.com/attachments/568837922288173058/1294677109775663204/yuyuko-like-0004.png',
).with_action(
    ACTION_TAG_LIKE, None, SAIGYOUJI_YUYUKO,
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294677228377997322/flandre-okina-like-0000.png',
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
    'https://cdn.discordapp.com/attachments/568837922288173058/1294208753482334220/aya-chiruno-kiss-0000.gif',
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
    'https://cdn.discordapp.com/attachments/568837922288173058/1275115959023177798/seiga-yoshika-hug-0000.png',
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
).with_creator(
    'kirby (tiokirby)'
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
    'https://cdn.discordapp.com/attachments/568837922288173058/1308910192687190026/akyuu-kosuzu-lap_sleep-0000.png',
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
    'https://cdn.discordapp.com/attachments/568837922288173058/1308909097466200105/hecatia-junko-lap_sleep-0000.png',
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
    'https://cdn.discordapp.com/attachments/568837922288173058/1308906720730419282/koishi-okuu-orin-satori-lap_sleep-0000.png',
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
    'https://cdn.discordapp.com/attachments/568837922288173058/1308911875282571294/hina-nitori-lap_sleep-0000.png',
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
    'https://cdn.discordapp.com/attachments/568837922288173058/1308909567966445608/marisa-reimu-lap_sleep-0001.png',
).with_action(
    ACTION_TAG_LAP_SLEEP, HAKUREI_REIMU, KIRISAME_MARISA,
).with_creator(
    'amaama',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1259050462682939422/flandre-remilia-pocky-0004.png',
).with_action(
    ACTION_TAG_POCKY, SCARLET_FLANDRE, SCARLET_REMILIA,
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
    'https://cdn.discordapp.com/attachments/568837922288173058/1270701692425601086/aya-momiji-pat-0002.gif',
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

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1259041701247451167/koishi-satori-feed-0000.png',
).with_action(
    ACTION_TAG_FEED, KOMEIJI_KOISHI, KOMEIJI_SATORI,
).with_creator(
    'don9899',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1259042767678603315/flandre-yuuma-feed-0001.png',
).with_action(
    ACTION_TAG_FEED, SCARLET_FLANDRE, TOUTETSU_YUUMA,
).with_creator(
    'isu (is88)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1259049989812916336/reimu-wakasagihime-feed-0000.png',
).with_action(
    ACTION_TAG_FEED, HAKUREI_REIMU, WAKASAGIHIME,
).with_creator(
    'ferdy\'s lab',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1259047622300143696/chiruno-youmu-hug-0000.png',
).with_action(
    ACTION_TAG_HUG, KONPAKU_YOUMU, CHIRUNO,
).with_creator(
    'ferdy\'s lab',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1259047622845534258/chiruno-reimu-pat-0000.gif',
).with_action(
    ACTION_TAG_PAT, HAKUREI_REIMU, CHIRUNO,
).with_creator(
    'ferdy\'s lab',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1259047623780732948/flandre-marisa-pat-0000.png',
).with_action(
    ACTION_TAG_PAT, KIRISAME_MARISA, SCARLET_FLANDRE,
).with_creator(
    'ferdy\'s lab',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1259047624456278037/chiruno-blush-0000.png',
).with_action(
    ACTION_TAG_BLUSH, CHIRUNO, None,
).with_creator(
    'ferdy\'s lab',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1259047624841891850/chiruno-pat-0000.png',
).with_action(
    ACTION_TAG_PAT, None, CHIRUNO,
).with_creator(
    'ferdy\'s lab',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1259047638289092648/chiruno-dai-pat-0000.gif',
).with_action(
    ACTION_TAG_PAT, CHIRUNO, DAIYOUSEI,
).with_creator(
    'ferdy\'s lab',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1259047638850998302/chiruno-wave-0000.gif',
).with_action(
    ACTION_TAG_WAVE, CHIRUNO, None,
).with_creator(
    'ferdy\'s lab',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1259047639219965992/shinmyoumaru-bully-0000.gif',
).with_action(
    ACTION_TAG_BULLY, None, SUKUNA_SHINMYOUMARU,
).with_creator(
    'ferdy\'s lab',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1270672046636007435/chiruno-dai-hug-0000.png',
).with_actions(
    (ACTION_TAG_HUG, CHIRUNO, DAIYOUSEI),
    (ACTION_TAG_HUG, DAIYOUSEI, CHIRUNO),
).with_creator(
    'ferdy\'s lab',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1270672047013625916/chiruno-dai-hug-0001.png',
).with_actions(
    (ACTION_TAG_HUG, CHIRUNO, DAIYOUSEI),
    (ACTION_TAG_HUG, DAIYOUSEI, CHIRUNO),
).with_creator(
    'ferdy\'s lab',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1259051075760291850/reimu-wakasagihime-feed-0001.png',
).with_action(
    ACTION_TAG_FEED, HAKUREI_REIMU, WAKASAGIHIME,
).with_creator(
    'tierra misu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1259051900649869353/marisa-remilia-feed-0000.png',
).with_action(
    ACTION_TAG_FEED, SCARLET_REMILIA, KIRISAME_MARISA,
).with_creator(
    'a-xii',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1259051901127757924/flandre-yuuma-feed-0002.png',
).with_action(
    ACTION_TAG_FEED, SCARLET_FLANDRE, TOUTETSU_YUUMA,
).with_creator(
    'a-xii',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1259488756726108160/flandre-remilia-hug-0003.png',
).with_action(
    ACTION_TAG_HUG, SCARLET_FLANDRE, SCARLET_REMILIA,
).with_creator(
    'suwa yasai',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1259488757338345492/flandre-koishi-hug-0001.png',
).with_actions(
    (ACTION_TAG_HUG, SCARLET_FLANDRE, KOMEIJI_KOISHI),
    (ACTION_TAG_HUG, KOMEIJI_KOISHI, SCARLET_FLANDRE),
).with_creator(
    'suwa yasai',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1259488757850177576/remilia-poke-0000.png',
).with_action(
    ACTION_TAG_POKE, None, SCARLET_REMILIA,
).with_creator(
    'suwa yasai',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1308908392185724948/koishi-satori-lap_sleep-0001.png',
).with_action(
    ACTION_TAG_LAP_SLEEP, KOMEIJI_SATORI, KOMEIJI_KOISHI,
).with_creator(
    'suwa yasai',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1259488758743564378/koishi-satori-hug-0006.png',
).with_action(
    ACTION_TAG_HUG, KOMEIJI_SATORI, KOMEIJI_KOISHI,
).with_creator(
    'suwa yasai',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1259502483030409216/flandre-remilia-pocky-0005.png',
).with_action(
    ACTION_TAG_POCKY, SCARLET_FLANDRE, SCARLET_REMILIA,
).with_creator(
    'sorani (kaeru0768)',
).with_editor(
    'HuyaneMatsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1259502483420745808/meiling-sakuya-hug-0000.png',
).with_action(
    ACTION_TAG_HUG, HONG_MEILING, IZAYOI_SAKUYA,
).with_creator(
    'sorani (kaeru0768)',
).with_editor(
    'HuyaneMatsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1259502483919601746/koishi-kokoro-hug-0004.png',
).with_action(
    ACTION_TAG_HUG, KOMEIJI_KOISHI, HATA_NO_KOKORO,
).with_creator(
    'sorani (kaeru0768)',
).with_editor(
    'HuyaneMatsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1259502484435767358/flandre-remilia-youmu-pat-0000.png',
).with_actions(
    (ACTION_TAG_PAT, KONPAKU_YOUMU, SCARLET_FLANDRE),
    (ACTION_TAG_PAT, KONPAKU_YOUMU, SCARLET_REMILIA),
).with_creator(
    'sorani (kaeru0768)',
).with_editor(
    'HuyaneMatsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1259502485245001820/flandre-koishi-handhold-0001.png',
).with_actions(
    (ACTION_TAG_HANDHOLD, SCARLET_FLANDRE, KOMEIJI_KOISHI),
    (ACTION_TAG_HANDHOLD, KOMEIJI_KOISHI, SCARLET_FLANDRE),
).with_creator(
    'sorani (kaeru0768)',
).with_editor(
    'HuyaneMatsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1259502485748453417/youmu-yuyuko-hug-0000.png',
).with_action(
    ACTION_TAG_HUG, KONPAKU_YOUMU, SAIGYOUJI_YUYUKO,
).with_creator(
    'sorani (kaeru0768)',
).with_editor(
    'HuyaneMatsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1259502952037486702/flandre-koishi-kiss-0007.png',
).with_actions(
    (ACTION_TAG_KISS, SCARLET_FLANDRE, KOMEIJI_KOISHI),
    (ACTION_TAG_KISS, KOMEIJI_KOISHI, SCARLET_FLANDRE),
).with_creator(
    'sorani (kaeru0768)',
).with_editor(
    'HuyaneMatsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1259504836764766248/flandre-koishi-kiss-0008.png',
).with_action(
    ACTION_TAG_KISS, SCARLET_FLANDRE, KOMEIJI_KOISHI,
).with_creator(
    'miy 001',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1259504837184327720/flandre-koishi-hug-0002.png',
).with_action(
    ACTION_TAG_HUG, KOMEIJI_KOISHI, SCARLET_FLANDRE,
).with_creator(
    'miy 001',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1259505939220922490/flandre-koishi-hug-0003.png',
).with_action(
    ACTION_TAG_HUG, SCARLET_FLANDRE, KOMEIJI_KOISHI,
).with_creator(
    'mike (mikeneko)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1259505938218614905/flandre-koishi-kiss-0009.png',
).with_action(
    ACTION_TAG_KISS, KOMEIJI_KOISHI, SCARLET_FLANDRE,
).with_creator(
    'mike (mikeneko)',
).with_editor(
    'HuyaneMatsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1259522534643208224/koishi-satori-kiss-0004.png',
).with_action(
    ACTION_TAG_KISS, KOMEIJI_SATORI, KOMEIJI_KOISHI,
).with_creator(
    'senzaicha kasukadoki',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1259522535087673505/orin-satori-handhold-0000.png',
).with_action(
    ACTION_TAG_HANDHOLD, KAENBYOU_RIN, KOMEIJI_SATORI,
).with_creator(
    'senzaicha kasukadoki',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1259522535444316201/koishi-satori-kiss-0003.png',
).with_actions(
    (ACTION_TAG_KISS, KOMEIJI_KOISHI, KOMEIJI_SATORI),
    (ACTION_TAG_KISS, KOMEIJI_SATORI, KOMEIJI_KOISHI),
).with_creator(
    'senzaicha kasukadoki',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1259522535897432219/koishi-satori-hug-0007.png',
).with_action(
    ACTION_TAG_HUG, KOMEIJI_KOISHI, KOMEIJI_SATORI,
).with_creator(
    'senzaicha kasukadoki',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1259522536534970408/flandre-remilia-feed-0000.png',
).with_action(
    ACTION_TAG_FEED, SCARLET_FLANDRE, SCARLET_REMILIA,
).with_creator(
    'senzaicha kasukadoki',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1259523003046432789/chen-orin-handhold-0000.png',
).with_actions(
    (ACTION_TAG_HANDHOLD, CHEN, KAENBYOU_RIN),
    (ACTION_TAG_HANDHOLD, KAENBYOU_RIN, CHEN),
).with_creator(
    'senzaicha kasukadoki',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1259524953942790184/koishi-satori-hug-0008.png',
).with_action(
    ACTION_TAG_HUG, KOMEIJI_KOISHI, KOMEIJI_SATORI,
).with_creator(
    'de17a',
).with_editor(
    'HuyaneMatsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1259524954635108472/remilia-satori-kiss-0001.png',
).with_action(
    ACTION_TAG_KISS, SCARLET_REMILIA, KOMEIJI_SATORI,
).with_creator(
    'de17a',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1259524955058737223/orin-satori-pat-0001.png',
).with_action(
    ACTION_TAG_PAT, KOMEIJI_SATORI, KAENBYOU_RIN,
).with_creator(
    'de17a',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1259526415162802288/reimu-seija-kiss-0000.png',
).with_actions(
    (ACTION_TAG_KISS, HAKUREI_REIMU, KIJIN_SEIJA),
    (ACTION_TAG_KISS, KIJIN_SEIJA, HAKUREI_REIMU),
).with_creator(
    'natsu (tohotiara)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1259527700092289054/koishi-kokoro-dance-0000.png',
).with_actions(
    (ACTION_TAG_DANCE, HATA_NO_KOKORO, KOMEIJI_KOISHI),
    (ACTION_TAG_DANCE, KOMEIJI_KOISHI, HATA_NO_KOKORO),
).with_creator(
    'kumamoto (bbtonhk2)',
).with_editor(
    'HuyaneMatsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1259527700452741182/clownpiece-junko-hug-0001.png',
).with_actions(
    (ACTION_TAG_HUG, CLOWNPIECE, JUNKO),
    (ACTION_TAG_HUG, JUNKO, CLOWNPIECE),
).with_creator(
    'kumamoto (bbtonhk2)',
).with_editor(
    'HuyaneMatsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1259528648671756298/koishi-kokoro-pocky-0003.png',
).with_actions(
    (ACTION_TAG_POCKY, CLOWNPIECE, JUNKO),
    (ACTION_TAG_POCKY, JUNKO, CLOWNPIECE),
).with_creator(
    'kiryuu soma',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1259528664245076030/koishi-kokoro-nom-0000.png',
).with_action(
    ACTION_TAG_NOM, KOMEIJI_KOISHI, HATA_NO_KOKORO,
).with_creator(
    'kiryuu soma',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1259542026555363489/marisa-reimu-pocky-0005.png',
).with_actions(
    (ACTION_TAG_POCKY, KIRISAME_MARISA, HAKUREI_REIMU),
    (ACTION_TAG_POCKY, HAKUREI_REIMU, KIRISAME_MARISA),
).with_creator(
    'yomogi 9392',
).with_editor(
    'HuyaneMatsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1259542026995892414/marisa-reimu-kiss-0005.png',
).with_actions(
    (ACTION_TAG_KISS, KIRISAME_MARISA, HAKUREI_REIMU),
    (ACTION_TAG_KISS, HAKUREI_REIMU, KIRISAME_MARISA),
).with_creator(
    'yomogi 9392',
).with_editor(
    'HuyaneMatsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1259542028040273950/flandre-marisa-reimu-hug-0000.png',
).with_actions(
    (ACTION_TAG_HUG, SCARLET_FLANDRE, KIRISAME_MARISA),
    (ACTION_TAG_HUG, KIRISAME_MARISA, HAKUREI_REIMU),
    (ACTION_TAG_HUG, KIRISAME_MARISA, SCARLET_FLANDRE),
    (ACTION_TAG_HUG, HAKUREI_REIMU, KIRISAME_MARISA),
).with_creator(
    'yomogi 9392',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1259542028698648607/marisa-reimu-hug-0006.png',
).with_action(
    ACTION_TAG_HUG, HAKUREI_REIMU, KIRISAME_MARISA,
).with_creator(
    'yomogi 9392',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1259542029260816394/marisa-reimu-kiss-0006.png',
).with_actions(
    (ACTION_TAG_KISS, KIRISAME_MARISA, HAKUREI_REIMU),
    (ACTION_TAG_KISS, HAKUREI_REIMU, KIRISAME_MARISA),
).with_creator(
    'yomogi 9392',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1259542330143281255/enoko-marisa-pat-0000.png',
).with_action(
    ACTION_TAG_PAT, MITSUGASHIRA_ENOKO, KIRISAME_MARISA,
).with_creator(
    'yomogi 9392',
).with_editor(
    'HuyaneMatsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1262016689592074300/marisa-reimu-kiss-0008.png',
).with_action(
    ACTION_TAG_KISS, KIRISAME_MARISA, HAKUREI_REIMU,
).with_creator(
    'Mito / みと❁',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1262016690393317447/marisa-reimu-kiss-0007.png',
).with_actions(
    (ACTION_TAG_KISS, KIRISAME_MARISA, HAKUREI_REIMU),
    (ACTION_TAG_KISS, HAKUREI_REIMU, KIRISAME_MARISA),
).with_creator(
    'Mito / みと❁',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1262016691802603552/meiling-sakuya-hug-0001.png',
).with_action(
    ACTION_TAG_HUG, HONG_MEILING, IZAYOI_SAKUYA,
).with_creator(
    'Mito / みと❁',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1262016694302412930/marisa-reimu-pocky-0007.png',
).with_action(
    ACTION_TAG_POCKY, KIRISAME_MARISA, HAKUREI_REIMU,
).with_creator(
    'Mito / みと❁',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1262016695195668581/marisa-reimu-pocky-0006.png',
).with_actions(
    (ACTION_TAG_POCKY, KIRISAME_MARISA, HAKUREI_REIMU),
    (ACTION_TAG_POCKY, HAKUREI_REIMU, KIRISAME_MARISA),
).with_creator(
    'Mito / みと❁',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1262016696206622801/flandre-reimu-hug-0000.png',
).with_action(
    ACTION_TAG_HUG, SCARLET_FLANDRE, HAKUREI_REIMU,
).with_creator(
    'Mito / みと❁',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1262019335929729145/hijiri-ichirin-koishi-kyouko-mamizou-murasa-nue-shou-kiss-0000.png',
).with_actions(
    (ACTION_TAG_KISS, MURASA_MINAMITSU, HOUJUU_NUE),
    (ACTION_TAG_KISS, HOUJUU_NUE, MURASA_MINAMITSU),
).with_characters(
    HIJIRI_BYAKUREN, KASODANI_KYOUKO, FUTATSUIWA_MAMIZOU, TORAMARU_SHOU, KOMEIJI_KOISHI
).with_creator(
    'k0269323474256',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1262019336420458556/murasa-nue-hug-0003.png',
).with_action(
    ACTION_TAG_HUG, MURASA_MINAMITSU, HOUJUU_NUE,
).with_creator(
    'k0269323474256',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1262019336902676510/murasa-nue-hug-0002.png',
).with_action(
    ACTION_TAG_HUG, HOUJUU_NUE, MURASA_MINAMITSU,
).with_creator(
    'k0269323474256',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1262019337280290856/murasa-nue-handhold-0000.gif',
).with_actions(
    (ACTION_TAG_HANDHOLD, MURASA_MINAMITSU, HOUJUU_NUE),
    (ACTION_TAG_HANDHOLD, HOUJUU_NUE, MURASA_MINAMITSU),
).with_creator(
    'k0269323474256',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1262021560642834513/ran-yuuma-hug-0000.png',
).with_action(
    ACTION_TAG_HUG, YAKUMO_RAN, TOUTETSU_YUUMA,
).with_creator(
    'chima_q',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1262025388453007471/alice-patchouli-feed-0000.png',
).with_action(
    ACTION_TAG_FEED, MARGATROID_ALICE, PATCHOULI_KNOWLEDGE,
).with_creator(
    'arnest',
).with_editor(
    'HuyaneMatsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1262025388813582468/flandre-sakuya-hug-0000.png',
).with_action(
    ACTION_TAG_HUG, SCARLET_FLANDRE, IZAYOI_SAKUYA,
).with_creator(
    'arnest',
).with_editor(
    'HuyaneMatsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1262025389182550036/minoriko-shizuha-handhold-0000.png',
).with_actions(
    (ACTION_TAG_HANDHOLD, AKI_MINORIKO, AKI_SHIZUHA),
    (ACTION_TAG_HANDHOLD, AKI_SHIZUHA, AKI_MINORIKO),
).with_creator(
    'arnest',
).with_editor(
    'HuyaneMatsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294665727994892328/alice-pocky_self-0000.png',
).with_action(
    ACTION_TAG_POCKY_SELF, MARGATROID_ALICE, MARGATROID_ALICE,
).with_creator(
    'arnest',
).with_editor(
    'HuyaneMatsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1262025390138982481/alice-patchouli-kiss-0000.png',
).with_action(
    ACTION_TAG_KISS, MARGATROID_ALICE, PATCHOULI_KNOWLEDGE,
).with_creator(
    'arnest',
).with_editor(
    'HuyaneMatsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1262025390617002024/flandre-pat-0000.png',
).with_action(
    ACTION_TAG_PAT, None, SCARLET_FLANDRE,
).with_creator(
    'arnest',
).with_editor(
    'HuyaneMatsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1262025391313256493/alice-patchouli-hug-0000.png',
).with_action(
    ACTION_TAG_HUG, MARGATROID_ALICE, PATCHOULI_KNOWLEDGE,
).with_creator(
    'arnest',
).with_editor(
    'HuyaneMatsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1262026532097097728/minoriko-shizuha-hug-0000.png',
).with_action(
    ACTION_TAG_HUG, AKI_MINORIKO, AKI_SHIZUHA,
).with_creator(
    'arnest',
).with_editor(
    'HuyaneMatsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1262028750980251718/tewi-pat-0000.png',
).with_action(
    ACTION_TAG_PAT, None, INABA_TEWI,
).with_creator(
    'maromi gou',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1262029613383684157/remilia-satori-hug-0002.png',
).with_actions(
    (ACTION_TAG_HUG, SCARLET_REMILIA, KOMEIJI_SATORI),
    (ACTION_TAG_HUG, KOMEIJI_SATORI, SCARLET_REMILIA),
).with_creator(
    'sorani (kaeru0768)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1262030222757462077/youmu-yuyuko-hug-0001.png',
).with_action(
    ACTION_TAG_HUG, SAIGYOUJI_YUYUKO, KONPAKU_YOUMU,
).with_creator(
    'ehehe52921343',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1262031422932254832/marisa-youmu-kiss-0000.png',
).with_action(
    ACTION_TAG_KISS, KONPAKU_YOUMU, KIRISAME_MARISA,
).with_creator(
    'leon0705',
).with_editor(
    'HuyaneMatsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1262031423288643584/marisa-reimu-kiss-0010.png',
).with_action(
    ACTION_TAG_KISS, HAKUREI_REIMU, KIRISAME_MARISA,
).with_creator(
    'leon0705',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1262031423704006757/marisa-reimu-kiss-0009.png',
).with_action(
    ACTION_TAG_KISS, KIRISAME_MARISA, HAKUREI_REIMU,
).with_creator(
    'leon0705',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294677406703157309/yuuka-like-0002.png',
).with_action(
    ACTION_TAG_LIKE, None, KAZAMI_YUUKA,
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294677640539541564/junko-like-0004.png',
).with_action(
    ACTION_TAG_LIKE, None, JUNKO,
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294677920018727003/kanako-like-0000.png',
).with_action(
    ACTION_TAG_LIKE, None, YASAKA_KANAKO,
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294677641294643312/junko-like-0005.png',
).with_action(
    ACTION_TAG_LIKE, None, JUNKO,
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294677642099818526/junko-like-0006.png',
).with_action(
    ACTION_TAG_LIKE, None, JUNKO,
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294677642997403700/junko-like-0007.png',
).with_action(
    ACTION_TAG_LIKE, None, JUNKO,
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294678056790659072/okina-like-0001.png',
).with_action(
    ACTION_TAG_LIKE, None, MATARA_OKINA,
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1262046917513449564/hisami-zanmu-hug-0000.png',
).with_action(
    ACTION_TAG_HUG, YOMOTSU_HISAMI, NIPPAKU_ZANMU,
).with_creator(
    'Kureko / くれく',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1262046913566347294/maribel-renko-kiss-0002.png',
).with_action(
    ACTION_TAG_KISS, USAMI_RENKO, HEARN_MARIBEL,
).with_creator(
    'Kureko / くれく',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1262046913943961632/maribel-renko-kiss-0001.png',
).with_actions(
    (ACTION_TAG_KISS, HEARN_MARIBEL, USAMI_RENKO),
    (ACTION_TAG_KISS, USAMI_RENKO, HEARN_MARIBEL),
).with_creator(
    'Kureko / くれく',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1262046914493419540/maribel-renko-hug-0004.png',
).with_actions(
    (ACTION_TAG_HUG, HEARN_MARIBEL, USAMI_RENKO),
    (ACTION_TAG_HUG, USAMI_RENKO, HEARN_MARIBEL),
).with_creator(
    'Kureko / くれく',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1262046914938142750/maribel-renko-hug-0003.png',
).with_actions(
    (ACTION_TAG_HUG, HEARN_MARIBEL, USAMI_RENKO),
    (ACTION_TAG_HUG, USAMI_RENKO, HEARN_MARIBEL),
).with_creator(
    'Kureko / くれく',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1262046915327955096/maribel-renko-hug-0002.png',
).with_actions(
    (ACTION_TAG_HUG, HEARN_MARIBEL, USAMI_RENKO),
    (ACTION_TAG_HUG, USAMI_RENKO, HEARN_MARIBEL),
).with_creator(
    'Kureko / くれく',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1262046915831529612/maribel-renko-hug-0001.png',
).with_action(
    ACTION_TAG_HUG, HEARN_MARIBEL, USAMI_RENKO,
).with_creator(
    'Kureko / くれく',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1262046916557017249/maribel-renko-hug-0000.png',
).with_actions(
    (ACTION_TAG_HUG, HEARN_MARIBEL, USAMI_RENKO),
    (ACTION_TAG_HUG, USAMI_RENKO, HEARN_MARIBEL),
).with_creator(
    'Kureko / くれく',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1262048693566308359/maribel-renko-hug-0007.png',
).with_actions(
    (ACTION_TAG_HUG, HEARN_MARIBEL, USAMI_RENKO),
    (ACTION_TAG_HUG, USAMI_RENKO, HEARN_MARIBEL),
).with_creator(
    'Kureko / くれく',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1262048693817839698/maribel-renko-hug-0006.png',
).with_action(
    ACTION_TAG_HUG, USAMI_RENKO, HEARN_MARIBEL,
).with_creator(
    'Kureko / くれく',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1262048694082076723/maribel-renko-hug-0005.png',
).with_actions(
    (ACTION_TAG_HUG, HEARN_MARIBEL, USAMI_RENKO),
    (ACTION_TAG_HUG, USAMI_RENKO, HEARN_MARIBEL),
).with_creator(
    'Kureko / くれく',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1262048694325219338/maribel-renko-kiss-0003.png',
).with_action(
    ACTION_TAG_KISS, USAMI_RENKO, HEARN_MARIBEL,
).with_creator(
    'Kureko / くれく',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1262048694610563195/maribel-renko-handhold-0000.png',
).with_actions(
    (ACTION_TAG_HANDHOLD, HEARN_MARIBEL, USAMI_RENKO),
    (ACTION_TAG_HANDHOLD, USAMI_RENKO, HEARN_MARIBEL),
).with_creator(
    'Kureko / くれく',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1262048692299628614/joon-shion-hug-0003.png',
).with_action(
    ACTION_TAG_HUG, YORIGAMI_SHION, YORIGAMI_JOON,
).with_creator(
    'Kureko / くれく',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1262048692609876088/joon-shion-hug-0002.png',
).with_action(
    ACTION_TAG_HUG, YORIGAMI_SHION, YORIGAMI_JOON,
).with_creator(
    'Kureko / くれく',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1262048692966523004/joon-shion-hug-0001.png',
).with_action(
    ACTION_TAG_HUG, YORIGAMI_SHION, YORIGAMI_JOON,
).with_creator(
    'Kureko / くれく',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1262048693297741955/joon-shion-hug-0000.png',
).with_action(
    ACTION_TAG_HUG, YORIGAMI_SHION, YORIGAMI_JOON,
).with_creator(
    'Kureko / くれく',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1262050606454145167/ran-yuuma-fluff-0000.png',
).with_action(
    ACTION_TAG_FLUFF, TOUTETSU_YUUMA, YAKUMO_RAN,
).with_creator(
    'polpol',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1262051233653461002/flandre-yuuma-nom-0000.png',
).with_action(
    ACTION_TAG_NOM, TOUTETSU_YUUMA, SCARLET_FLANDRE,
).with_creator(
    'Pura / ぷら',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1262054241355169852/aya-chiruno-hug-0004.png',
).with_action(
    ACTION_TAG_HUG, CHIRUNO, SHAMEIMARU_AYA,
).with_creator(
    'roke (taikodon)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1262054241678262404/aya-chiruno-hug-0002.png',
).with_action(
    ACTION_TAG_HUG, SHAMEIMARU_AYA, CHIRUNO,
).with_creator(
    'roke (taikodon)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1262054242450014228/parsee-yuugi-hug-0000.png',
).with_action(
    ACTION_TAG_HUG, MIZUHASHI_PARSEE, HOSHIGUMA_YUUGI,
).with_creator(
    'roke (taikodon)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1262054243024769064/koishi-kokoro-handhold-0000.png',
).with_actions(
    (ACTION_TAG_HANDHOLD, KOMEIJI_KOISHI, HATA_NO_KOKORO),
    (ACTION_TAG_HANDHOLD, HATA_NO_KOKORO, KOMEIJI_KOISHI),
).with_creator(
    'roke (taikodon)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1262054243712368761/aya-chiruno-pat-0000.png',
).with_action(
    ACTION_TAG_PAT, SHAMEIMARU_AYA, CHIRUNO,
).with_creator(
    'roke (taikodon)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1262054244366811227/ichirin-murasa-kiss-0000.png',
).with_actions(
    (ACTION_TAG_KISS, KUMOI_ICHIRIN, MURASA_MINAMITSU),
    (ACTION_TAG_KISS, MURASA_MINAMITSU, KUMOI_ICHIRIN),
).with_creator(
    'roke (taikodon)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1308907268267577408/minoriko-shizuha-lap_sleep-0000.png',
).with_action(
    ACTION_TAG_LAP_SLEEP, AKI_MINORIKO, AKI_SHIZUHA,
).with_creator(
    'roke (taikodon)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1262054245436358738/aya-chiruno-hug-0003.png',
).with_action(
    ACTION_TAG_HUG, SHAMEIMARU_AYA, CHIRUNO,
).with_creator(
    'roke (taikodon)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1308912045277708308/aya-chiruno-lap_sleep-0000.png',
).with_action(
    ACTION_TAG_LAP_SLEEP, CHIRUNO, SHAMEIMARU_AYA,
).with_creator(
    'roke (taikodon)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1275117449578020937/ran-kon-0035.png',
).with_action(
    ACTION_TAG_KON, YAKUMO_RAN, None,
).with_creator(
    'sarasadou dan / 更紗灯弾',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1275117450266017983/ran-kon-0036.png',
).with_action(
    ACTION_TAG_KON, YAKUMO_RAN, None,
).with_creator(
    'sarasadou dan / 更紗灯弾',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1275122578926731347/hijiri-miko-poke-0000.png',
).with_action(
    ACTION_TAG_POKE, HIJIRI_BYAKUREN, TOYOSATOMIMI_NO_MIKO,
).with_creator(
    'makuwauri',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1275128043916234917/hijiri-miko-kiss-0000.png',
).with_actions(
    (ACTION_TAG_KISS, HIJIRI_BYAKUREN, TOYOSATOMIMI_NO_MIKO),
    (ACTION_TAG_KISS, TOYOSATOMIMI_NO_MIKO, HIJIRI_BYAKUREN),
).with_creator(
    'makuwauri',
).with_editor(
    'HuyaneMatsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1275122577941069834/hecatia-junko-handhold-0000.png',
).with_actions(
    (ACTION_TAG_HANDHOLD, HECATIA_LAPISLAZULI, JUNKO),
    (ACTION_TAG_HANDHOLD, JUNKO, HECATIA_LAPISLAZULI),
).with_creator(
    'makuwauri',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1275122578624876554/seiga-yoshika-pat-0001.png',
).with_action(
    ACTION_TAG_PAT, KAKU_SEIGA, MIYAKO_YOSHIKA,
).with_creator(
    'makuwauri',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1275123478315532439/flandre-yuuma-hug-0000.png',
).with_action(
    ACTION_TAG_HUG, TOUTETSU_YUUMA, SCARLET_FLANDRE,
).with_creator(
    'chokomaron',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1275124090197381250/aya-momiji-lick-0001.png',
).with_action(
    ACTION_TAG_LICK, INUBASHIRI_MOMIJI, SHAMEIMARU_AYA,
).with_creator(
    'e.o.',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1275129460768768120/ran-kon-0039.png',
).with_action(
    ACTION_TAG_KON, YAKUMO_RAN, None,
).with_creator(
    'e.o.',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1275129461381267558/ran-kon-0038.png',
).with_action(
    ACTION_TAG_KON, YAKUMO_RAN, None,
).with_creator(
    'e.o.',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1275129463683940412/ran-kon-0037.png',
).with_action(
    ACTION_TAG_KON, YAKUMO_RAN, None,
).with_creator(
    'e.o.',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1275129462140440738/marisa-reimu-poke-0000.png',
).with_action(
    ACTION_TAG_POKE, KIRISAME_MARISA, HAKUREI_REIMU,
).with_creator(
    'e.o.',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1275129462673113139/maribel-renko-tickle-0000.png',
).with_action(
    ACTION_TAG_POKE, USAMI_RENKO, HEARN_MARIBEL,
).with_creator(
    'e.o.',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1275129463193210960/maribel-renko-hug-0010.png',
).with_action(
    ACTION_TAG_HUG, USAMI_RENKO, HEARN_MARIBEL,
).with_creator(
    'e.o.',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1275129464069685300/maribel-renko-hug-0009.png',
).with_actions(
    (ACTION_TAG_HUG, USAMI_RENKO, HEARN_MARIBEL),
    (ACTION_TAG_HUG, HEARN_MARIBEL, USAMI_RENKO),
).with_creator(
    'e.o.',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1275132839733493810/aunn-marisa-reimu-kiss-0000.png',
).with_actions(
    (ACTION_TAG_KISS, KIRISAME_MARISA, HAKUREI_REIMU),
    (ACTION_TAG_KISS, HAKUREI_REIMU, KIRISAME_MARISA),
).with_character(
    KOMANO_AUNN,
).with_creator(
    'Rina / 里奈',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1275132843256975460/marisa-reimu-kiss-0011.png',
).with_actions(
    (ACTION_TAG_KISS, KIRISAME_MARISA, HAKUREI_REIMU),
    (ACTION_TAG_KISS, HAKUREI_REIMU, KIRISAME_MARISA),
).with_creator(
    'Rina / 里奈',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1275132841243705375/marisa-reimu-kiss-0013.png',
).with_action(
    ACTION_TAG_KISS, KIRISAME_MARISA, HAKUREI_REIMU,
).with_creator(
    'Rina / 里奈',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1275132842174578729/marisa-reimu-kiss-0012.png',
).with_action(
    ACTION_TAG_KISS, HAKUREI_REIMU, KIRISAME_MARISA,
).with_creator(
    'Rina / 里奈',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1284231739002064948/reimu-stare-0000.png',
).with_action(
    ACTION_TAG_STARE, HAKUREI_REIMU, None,
).with_creator(
    'mata (matasoup)',
).with_editor(
    'HuyaneMatsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1284239141520936991/reimu-stare-0001.png',
).with_action(
    ACTION_TAG_STARE, HAKUREI_REIMU, None,
).with_creator(
    'mata (matasoup)',
).with_editor(
    'HuyaneMatsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1284242869711798343/reimu-stare-0002.png',
).with_action(
    ACTION_TAG_STARE, HAKUREI_REIMU, None,
).with_creator(
    'mata (matasoup)',
).with_editor(
    'HuyaneMatsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1284231742080679977/orin-stare-0000.png',
).with_action(
    ACTION_TAG_STARE, KAENBYOU_RIN, None,
).with_creator(
    'mata (matasoup)',
).with_editor(
    'HuyaneMatsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1284231741556396164/chiruno-stare-0000.png',
).with_action(
    ACTION_TAG_STARE, CHIRUNO, None,
).with_creator(
    'mata (matasoup)',
).with_editor(
    'HuyaneMatsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1284237039499477125/yuuka-stare-0000.png',
).with_action(
    ACTION_TAG_STARE, KAZAMI_YUUKA, None,
).with_creator(
    'mata (matasoup)',
).with_editor(
    'HuyaneMatsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1284239142187962458/youmu-stare-0000.png',
).with_action(
    ACTION_TAG_STARE, KONPAKU_YOUMU, None,
).with_creator(
    'mata (matasoup)',
).with_editor(
    'HuyaneMatsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1284240065312063509/sakuya-stare-0000.png',
).with_action(
    ACTION_TAG_STARE, IZAYOI_SAKUYA, None,
).with_creator(
    'mata (matasoup)',
).with_editor(
    'HuyaneMatsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1284242870508978216/koakuma-stare-0000.png',
).with_action(
    ACTION_TAG_STARE, KOAKUMA, None,
).with_creator(
    'mata (matasoup)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1284242871200907377/reisen-stare-0000.png',
).with_action(
    ACTION_TAG_STARE, REISEN_UDONGEIN_INABA, None,
).with_creator(
    'mata (matasoup)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1284231742722412738/youmu-wave-0000.png',
).with_action(
    ACTION_TAG_WAVE, KONPAKU_YOUMU, None,
).with_creator(
    'mata (matasoup)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1284234047320756244/medi-yuuka-pat-0000.png',
).with_action(
    ACTION_TAG_PAT, KAZAMI_YUUKA, MEDICINE_MELANCHOLY,
).with_creator(
    'mata (matasoup)',
).with_editor(
    'HuyaneMatsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1284235694662881330/wriggle-yuuka-hug-0000.png',
).with_actions(
    (ACTION_TAG_HUG, KAZAMI_YUUKA, WRIGGLE_NIGHTBUG),
    (ACTION_TAG_HUG, WRIGGLE_NIGHTBUG, KAZAMI_YUUKA),
).with_creator(
    'mata (matasoup)',
).with_editor(
    'HuyaneMatsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1284231799232532593/remilia-sakuya-hug-0001.png',
).with_action(
    ACTION_TAG_HUG, IZAYOI_SAKUYA, SCARLET_REMILIA,
).with_creator(
    'mata (matasoup)',
).with_editor(
    'HuyaneMatsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1284231795897929800/meiling-sakuya-hug-0007.png',
).with_action(
    ACTION_TAG_HUG, HONG_MEILING, IZAYOI_SAKUYA,
).with_creator(
    'mata (matasoup)',
).with_editor(
    'HuyaneMatsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1284231796825002025/meiling-sakuya-hug-0006.png',
).with_action(
    ACTION_TAG_HUG, HONG_MEILING, IZAYOI_SAKUYA,
).with_creator(
    'mata (matasoup)',
).with_editor(
    'HuyaneMatsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1284231797139570830/meiling-sakuya-hug-0005.png',
).with_action(
    ACTION_TAG_HUG, HONG_MEILING, IZAYOI_SAKUYA,
).with_creator(
    'mata (matasoup)',
).with_editor(
    'HuyaneMatsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1284231798049603675/meiling-sakuya-hug-0004.png',
).with_action(
    ACTION_TAG_HUG, IZAYOI_SAKUYA, HONG_MEILING,
).with_creator(
    'mata (matasoup)',
).with_editor(
    'HuyaneMatsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1284249095657226351/megumu-stare-0000.png',
).with_action(
    ACTION_TAG_STARE, IIZUNAMARU_MEGUMU, None,
).with_creator(
    'harapan-kun',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1284249096214937701/tenshi-stare-0000.png',
).with_action(
    ACTION_TAG_STARE, HINANAWI_TENSHI, None,
).with_creator(
    'harapan-kun',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1284249096919715891/momiji-stare-0000.png',
).with_action(
    ACTION_TAG_STARE, INUBASHIRI_MOMIJI, None,
).with_creator(
    'harapan-kun',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1284249097624092704/flandre-stare-0000.png',
).with_action(
    ACTION_TAG_STARE, SCARLET_FLANDRE, None,
).with_creator(
    'harapan-kun',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1284249098278670356/alice-patchouli-stare-0000.png',
).with_actions(
    (ACTION_TAG_STARE, PATCHOULI_KNOWLEDGE, None),
    (ACTION_TAG_STARE, MARGATROID_ALICE, None),
).with_creator(
    'harapan-kun',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1284249097624092704/flandre-stare-0000.png',
).with_action(
    ACTION_TAG_STARE, SCARLET_FLANDRE, None,
).with_creator(
    'harapan-kun',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1284251464419508344/momiji-stare-0001.png',
).with_action(
    ACTION_TAG_STARE, INUBASHIRI_MOMIJI, None,
).with_creator(
    'harapan-kun',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1284252688451764317/marisa-stare-0001.png',
).with_action(
    ACTION_TAG_STARE, KIRISAME_MARISA, None,
).with_creator(
    'harapan-kun',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1284412294666780794/marisa-stare-0000.png',
).with_action(
    ACTION_TAG_STARE, KIRISAME_MARISA, None,
).with_creator(
    'nubezon',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1284412293559488593/nue-stare-0000.png',
).with_action(
    ACTION_TAG_STARE, HOUJUU_NUE, None,
).with_creator(
    'nubezon',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1284412292850782248/junko-stare-0000.png',
).with_action(
    ACTION_TAG_STARE, JUNKO, None,
).with_creator(
    'nubezon',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1284412298839986206/flandre-stare-0001.png',
).with_action(
    ACTION_TAG_STARE, SCARLET_FLANDRE, None,
).with_creator(
    'nubezon',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1284412297955246150/flandre-stare-0002.png',
).with_action(
    ACTION_TAG_STARE, SCARLET_FLANDRE, None,
).with_creator(
    'nubezon',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1284412297225441290/flandre-stare-0003.png',
).with_action(
    ACTION_TAG_STARE, SCARLET_FLANDRE, None,
).with_creator(
    'nubezon',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1284412295853637754/flandre-stare-0004.png',
).with_action(
    ACTION_TAG_STARE, SCARLET_FLANDRE, None,
).with_creator(
    'nubezon',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1284412291890020372/flandre-stare-0005.png',
).with_action(
    ACTION_TAG_STARE, SCARLET_FLANDRE, None,
).with_creator(
    'nubezon',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1284415752606322759/reimu-stare-0003.png',
).with_action(
    ACTION_TAG_STARE, HAKUREI_REIMU, None,
).with_creator(
    'hia (xonn)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1284415754241970216/kogasa-stare-0000.png',
).with_action(
    ACTION_TAG_STARE, TATARA_KOGASA, None,
).with_creator(
    'hia (xonn)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1284415753487122433/kogasa-stare-0001.png',
).with_action(
    ACTION_TAG_STARE, TATARA_KOGASA, None,
).with_creator(
    'hia (xonn)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1284415754900471839/kogasa-stare-0002.png',
).with_action(
    ACTION_TAG_STARE, TATARA_KOGASA, None,
).with_creator(
    'hia (xonn)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1284423825500672000/sakuya-stare-0001.png',
).with_action(
    ACTION_TAG_STARE, IZAYOI_SAKUYA, None,
).with_creator(
    'himuhino',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1284423826045927425/nazrin-stare-0000.png',
).with_action(
    ACTION_TAG_STARE, NAZRIN, None,
).with_creator(
    'himuhino',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1284423826683330611/orin-stare-0002.png',
).with_action(
    ACTION_TAG_STARE, KAENBYOU_RIN, None,
).with_creator(
    'himuhino',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1284423827249565716/hecatia-stare-0000.png',
).with_action(
    ACTION_TAG_STARE, HECATIA_LAPISLAZULI, None,
).with_creator(
    'himuhino',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1284423827794821140/yatsuhashi-stare-0000.png',
).with_action(
    ACTION_TAG_STARE, TSUKUMO_YATSUHASHI, None,
).with_creator(
    'himuhino',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1284423828981940267/koishi-stare-0000.png',
).with_action(
    ACTION_TAG_STARE, KOMEIJI_KOISHI, None,
).with_creator(
    'himuhino',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1284423842919612476/koishi-stare-0001.png',
).with_action(
    ACTION_TAG_STARE, KOMEIJI_KOISHI, None,
).with_creator(
    'himuhino',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1284423842583941232/koishi-stare-0002.png',
).with_action(
    ACTION_TAG_STARE, KOMEIJI_KOISHI, None,
).with_creator(
    'himuhino',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1284423830768451595/kokoro-stare-0000.png',
).with_action(
    ACTION_TAG_STARE, HATA_NO_KOKORO, None,
).with_creator(
    'himuhino',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1284423829963276288/hina-stare-0000.png',
).with_action(
    ACTION_TAG_STARE, KAGIYAMA_HINA, None,
).with_creator(
    'himuhino',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1284423829380136961/tsukasa-stare-0000.png',
).with_action(
    ACTION_TAG_STARE, KUDAMAKI_TSUKASA, None,
).with_creator(
    'himuhino',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1284423828398669885/chen-orin-hug-pat-0000.png',
).with_actions(
    (ACTION_TAG_HUG, CHEN, KAENBYOU_RIN),
    (ACTION_TAG_PAT, KAENBYOU_RIN, CHEN),
).with_creator(
    'himuhino',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1284423843317944423/chiruno-flandre-cosplay-stare-0000.png',
).with_actions(
    (ACTION_TAG_COSPLAY, CHIRUNO, SCARLET_FLANDRE),
    (ACTION_TAG_STARE, CHIRUNO, None),
).with_creator(
    'himuhino',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1284423843863334963/chiruno-flandre-cosplay-stare-0001.png',
).with_actions(
    (ACTION_TAG_COSPLAY, SCARLET_FLANDRE, CHIRUNO),
    (ACTION_TAG_STARE, SCARLET_FLANDRE, None),
).with_creator(
    'himuhino',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1284427744016470057/orin-stare-0001.png',
).with_action(
    ACTION_TAG_STARE, KAENBYOU_RIN, None,
).with_creator(
    'fuuzasa',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1284427743462817793/orin-stare-0003.png',
).with_action(
    ACTION_TAG_STARE, KAENBYOU_RIN, None,
).with_creator(
    'fuuzasa',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1284469077372309504/keine-mokou-handhold-0001.png',
).with_actions(
    (ACTION_TAG_HANDHOLD, KAMISHIRASAWA_KEINE, FUJIWARA_NO_MOKOU),
    (ACTION_TAG_HANDHOLD, FUJIWARA_NO_MOKOU, KAMISHIRASAWA_KEINE),
).with_creator(
    'itomugi-kun',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1284469077804580967/keine-mokou-fluff-0003.png',
).with_action(
    ACTION_TAG_FLUFF, FUJIWARA_NO_MOKOU, KAMISHIRASAWA_KEINE,
).with_creator(
    'itomugi-kun',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1284469078345383986/keine-mokou-handhold-0000.png',
).with_actions(
    (ACTION_TAG_HANDHOLD, KAMISHIRASAWA_KEINE, FUJIWARA_NO_MOKOU),
    (ACTION_TAG_HANDHOLD, FUJIWARA_NO_MOKOU, KAMISHIRASAWA_KEINE),
).with_creator(
    'itomugi-kun',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1284469079083847720/keine-mokou-hug-0006.png',
).with_action(
    ACTION_TAG_HUG, FUJIWARA_NO_MOKOU, KAMISHIRASAWA_KEINE,
).with_creator(
    'itomugi-kun',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1284469080509648958/keine-mokou-fluff-0002.png',
).with_action(
    ACTION_TAG_FLUFF, FUJIWARA_NO_MOKOU, KAMISHIRASAWA_KEINE,
).with_creator(
    'itomugi-kun',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1284469080509648958/keine-mokou-fluff-0002.png',
).with_action(
    ACTION_TAG_FLUFF, FUJIWARA_NO_MOKOU, KAMISHIRASAWA_KEINE,
).with_creator(
    'itomugi-kun',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1284469110637334528/koishi-satori-hug-0009.png',
).with_actions(
    (ACTION_TAG_HUG, KOMEIJI_KOISHI, KOMEIJI_SATORI),
    (ACTION_TAG_HUG, KOMEIJI_SATORI, KOMEIJI_KOISHI),
).with_creator(
    'itomugi-kun',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1284469111044313140/tsukasa-kon-stare-0000.png',
).with_actions(
    (ACTION_TAG_KON, KUDAMAKI_TSUKASA, None),
    (ACTION_TAG_STARE, KUDAMAKI_TSUKASA, None),
).with_creator(
    'itomugi-kun',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1284469111400824886/kyouko-mamizou-fluff-0001.png',
).with_action(
    ACTION_TAG_FLUFF, KASODANI_KYOUKO, FUTATSUIWA_MAMIZOU,
).with_creator(
    'itomugi-kun',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1284469111686168606/seiga-yoshika-pat-0002.png',
).with_action(
    ACTION_TAG_PAT, KAKU_SEIGA, MIYAKO_YOSHIKA,
).with_creator(
    'itomugi-kun',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1284470166004174912/keine-mokou-hug-0005.png',
).with_actions(
    (ACTION_TAG_HUG, KAMISHIRASAWA_KEINE, FUJIWARA_NO_MOKOU),
    (ACTION_TAG_HUG, FUJIWARA_NO_MOKOU, KAMISHIRASAWA_KEINE),
).with_creator(
    'itomugi-kun',
).with_editor(
    'HuyaneMatsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1284475400101298176/keine-mokou-hug-0001.png',
).with_action(
    ACTION_TAG_HUG, FUJIWARA_NO_MOKOU, KAMISHIRASAWA_KEINE,
).with_creator(
    'itomugi-kun',
).with_editor(
    'HuyaneMatsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1284475878365204492/keine-mokou-hug-0002.png',
).with_action(
    ACTION_TAG_HUG, KAMISHIRASAWA_KEINE, FUJIWARA_NO_MOKOU,
).with_creator(
    'itomugi-kun',
).with_editor(
    'HuyaneMatsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1284476440556994681/keine-mokou-fluff-0001.png',
).with_action(
    ACTION_TAG_FLUFF, FUJIWARA_NO_MOKOU, KAMISHIRASAWA_KEINE,
).with_creator(
    'itomugi-kun',
).with_editor(
    'HuyaneMatsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1284474762474688554/flandre-stare-0007.png',
).with_action(
    ACTION_TAG_STARE, SCARLET_FLANDRE, None,
).with_creator(
    'itomugi-kun',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1284474761937686601/chimata-stare-0000.png',
).with_action(
    ACTION_TAG_STARE, TENKYUU_CHIMATA, None,
).with_creator(
    'itomugi-kun',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1284474762957029407/okina-stare-0000.png',
).with_action(
    ACTION_TAG_STARE, MATARA_OKINA, None,
).with_creator(
    'itomugi-kun',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1284474793055223818/mokou-stare-0000.png',
).with_action(
    ACTION_TAG_STARE, FUJIWARA_NO_MOKOU, None,
).with_creator(
    'itomugi-kun',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1284474793843757076/yuuma-stare-0000.png',
).with_action(
    ACTION_TAG_STARE, TOUTETSU_YUUMA, None,
).with_creator(
    'itomugi-kun',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1284474794825486368/okuu-stare-0000.png',
).with_action(
    ACTION_TAG_STARE, REIUJI_UTSUHO, None,
).with_creator(
    'itomugi-kun',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1284474796230578176/sakuya-stare-0002.png',
).with_action(
    ACTION_TAG_STARE, IZAYOI_SAKUYA, None,
).with_creator(
    'itomugi-kun',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1284474795475599380/keine-mokou-stare-0000.png',
).with_actions(
    (ACTION_TAG_STARE, KAMISHIRASAWA_KEINE, None),
    (ACTION_TAG_STARE, FUJIWARA_NO_MOKOU, None),
).with_creator(
    'itomugi-kun',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1284474764404195370/keine-mokou-stare-0001.png',
).with_actions(
    (ACTION_TAG_STARE, KAMISHIRASAWA_KEINE, None),
    (ACTION_TAG_STARE, FUJIWARA_NO_MOKOU, None),
).with_creator(
    'itomugi-kun',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1284474764064194641/keine-mokou-nom-0000.png',
).with_action(
    ACTION_TAG_NOM, FUJIWARA_NO_MOKOU, KAMISHIRASAWA_KEINE,
).with_creator(
    'itomugi-kun',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1284474763472801803/keine-mokou-hug-0003.png',
).with_action(
    ACTION_TAG_HUG, KAMISHIRASAWA_KEINE, FUJIWARA_NO_MOKOU,
).with_creator(
    'itomugi-kun',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1284521693666345112/keine-blush-stare-0000.png',
).with_actions(
    (ACTION_TAG_BLUSH, KAMISHIRASAWA_KEINE, None),
    (ACTION_TAG_STARE, KAMISHIRASAWA_KEINE, None),
).with_creator(
    'itomugi-kun',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1284926692355477637/keine-stare-0000.png',
).with_action(
    ACTION_TAG_STARE, KAMISHIRASAWA_KEINE, None,
).with_creator(
    'itomugi-kun',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1284926693164847245/kaguya-stare-0000.png',
).with_action(
    ACTION_TAG_STARE, HOURAISAN_KAGUYA, None,
).with_creator(
    'itomugi-kun',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1284926693852844063/mayumi-stare-0000.png',
).with_action(
    ACTION_TAG_STARE, JOUTOUGUU_MAYUMI, None,
).with_creator(
    'itomugi-kun',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1284926694251171871/mokou-stare-0001.png',
).with_action(
    ACTION_TAG_STARE, FUJIWARA_NO_MOKOU, None,
).with_creator(
    'itomugi-kun',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1284926694586843206/keine-mokou-stare-0003.png',
).with_action(
    ACTION_TAG_STARE, FUJIWARA_NO_MOKOU, None,
).with_character(
    KAMISHIRASAWA_KEINE,
).with_creator(
    'itomugi-kun',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1284926714216185936/keine-stare-0002.png',
).with_action(
    ACTION_TAG_STARE, KAMISHIRASAWA_KEINE, None,
).with_creator(
    'itomugi-kun',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1284926713867931822/keine-mokou-stare-0004.png',
).with_actions(
    (ACTION_TAG_STARE, KAMISHIRASAWA_KEINE, None),
    (ACTION_TAG_STARE, FUJIWARA_NO_MOKOU, None),
).with_creator(
    'itomugi-kun',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1284926714794872872/keine-stare-0001.png',
).with_action(
    ACTION_TAG_STARE, KAMISHIRASAWA_KEINE, None,
).with_creator(
    'itomugi-kun',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1284926695077580942/sekibanki-stare-0000.png',
).with_action(
    ACTION_TAG_STARE, SEKIBANKI, None,
).with_creator(
    'itomugi-kun',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1284926695794802729/letty-stare-0000.png',
).with_action(
    ACTION_TAG_STARE, LETTY_WHITEROCK, None,
).with_creator(
    'itomugi-kun',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1284926712592728208/okina-stare-0001.png',
).with_action(
    ACTION_TAG_STARE, MATARA_OKINA, None,
).with_creator(
    'itomugi-kun',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1284926713138249728/star-stare-0000.png',
).with_action(
    ACTION_TAG_STARE, STAR_SAPPHIRE, None,
).with_creator(
    'itomugi-kun',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1284926713511411773/futo-stare-0000.png',
).with_action(
    ACTION_TAG_STARE, MONONOBE_NO_FUTO, None,
).with_creator(
    'itomugi-kun',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1284926714522239037/tojiko-stare-0000.png',
).with_action(
    ACTION_TAG_STARE, SOGA_NO_TOJIKO, None,
).with_creator(
    'itomugi-kun',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1288763851994824776/keine-mokou-peg-0000.png',
).with_action(
    ACTION_TAG_PEG, KAMISHIRASAWA_KEINE, FUJIWARA_NO_MOKOU,
).with_creator(
    'shirosato',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1292573211837595669/flandre-koishi-hug-0004.png',
).with_action(
    ACTION_TAG_HUG, KOMEIJI_KOISHI, SCARLET_FLANDRE,
).with_creator(
    'ranka224',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1292578376850341941/flandre-remilia-hug-0004.png',
).with_action(
    ACTION_TAG_HUG, SCARLET_FLANDRE, SCARLET_REMILIA,
).with_creator(
    'kutabireta inu',
).with_editor(
    'HuyaneMatsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1292578377584214036/aya-momiji-fluff-0000.png',
).with_action(
    ACTION_TAG_FLUFF, SHAMEIMARU_AYA, INUBASHIRI_MOMIJI,
).with_creator(
    'kutabireta inu',
).with_editor(
    'HuyaneMatsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1292578378423205970/patchouli-remilia-hug-0001.png',
).with_action(
    ACTION_TAG_HUG, SCARLET_REMILIA, PATCHOULI_KNOWLEDGE,
).with_creator(
    'kutabireta inu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1292578379589226708/flandre-remilia-kiss-0000.png',
).with_action(
    ACTION_TAG_KISS, SCARLET_REMILIA, SCARLET_FLANDRE,
).with_creator(
    'kutabireta inu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1292578380461641758/flandre-remilia-hug-0005.png',
).with_action(
    ACTION_TAG_HUG, SCARLET_FLANDRE, SCARLET_REMILIA,
).with_creator(
    'kutabireta inu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1292578381333921862/flandre-koishi-handhold-0002.png',
).with_actions(
    (ACTION_TAG_HANDHOLD, SCARLET_FLANDRE, KOMEIJI_KOISHI),
    (ACTION_TAG_HANDHOLD, KOMEIJI_KOISHI, SCARLET_FLANDRE),
).with_creator(
    'kutabireta inu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1292581216171851880/flandre-koishi-hug-0005.png',
).with_action(
    ACTION_TAG_HUG, KOMEIJI_KOISHI, SCARLET_FLANDRE,
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1292582158996607006/flandre-marisa-hug-0003.png',
).with_action(
    ACTION_TAG_HUG, SCARLET_FLANDRE, KIRISAME_MARISA,
).with_creator(
    'mata (matasoup)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1292604703489916970/keine-mokou-hug-0004.png',
).with_action(
    ACTION_TAG_HUG, FUJIWARA_NO_MOKOU, KAMISHIRASAWA_KEINE,
).with_creator(
    'terrajin',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1292604704462864384/meiling-wave-0000.png',
).with_action(
    ACTION_TAG_WAVE, HONG_MEILING, None,
).with_creator(
    'terrajin',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1292604724381749328/mystia-yuyuko-hug-nom-0000.png',
).with_actions(
    (ACTION_TAG_HUG, SAIGYOUJI_YUYUKO, LORELEI_MYSTIA),
    (ACTION_TAG_NOM, SAIGYOUJI_YUYUKO, LORELEI_MYSTIA),
).with_creator(
    'terrajin',
).with_editor(
    'HuyaneMatsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1292604724712833044/flandre-meiling-kiss-0000.png',
).with_action(
    ACTION_TAG_KISS, HONG_MEILING, SCARLET_FLANDRE,
).with_creator(
    'terrajin',
).with_editor(
    'HuyaneMatsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1292604725044449320/flandre-meiling-hug-0000.png',
).with_action(
    ACTION_TAG_HUG, HONG_MEILING, SCARLET_FLANDRE,
).with_creator(
    'terrajin',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1292604725388378195/hijiri-nue-hug-0001.png',
).with_action(
    ACTION_TAG_HUG, HOUJUU_NUE, HIJIRI_BYAKUREN,
).with_creator(
    'terrajin',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1292604703821008898/shou-stare-0000.png',
).with_action(
    ACTION_TAG_STARE, TORAMARU_SHOU, None,
).with_creator(
    'terrajin',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1292604704110678067/doremy-stare-0000.png',
).with_action(
    ACTION_TAG_STARE, DOREMY_SWEET, None,
).with_creator(
    'terrajin',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1292604704794083338/hina-stare-0001.png',
).with_action(
    ACTION_TAG_STARE, KAGIYAMA_HINA, None,
).with_creator(
    'terrajin',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1292604705234616330/kanako-stare-0000.png',
).with_action(
    ACTION_TAG_STARE, YASAKA_KANAKO, None,
).with_creator(
    'terrajin',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1292604725707018281/yuuka-stare-0001.png',
).with_action(
    ACTION_TAG_STARE, KAZAMI_YUUKA, None,
).with_creator(
    'terrajin',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1292604724088012841/kagerou-stare-0000.png',
).with_action(
    ACTION_TAG_STARE, IMAIZUMI_KAGEROU, None,
).with_creator(
    'terrajin',
).with_editor(
    'HuyaneMatsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1292606472357806090/kagerou-stare-0001.png',
).with_action(
    ACTION_TAG_STARE, IMAIZUMI_KAGEROU, None,
).with_creator(
    'terrajin',
).with_editor(
    'HuyaneMatsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1292746536450785313/flandre-okina-pat-0000.png',
).with_action(
    ACTION_TAG_PAT, MATARA_OKINA, SCARLET_FLANDRE,
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1292747961834541067/flandre-koishi-kiss-0010.png',
).with_action(
    ACTION_TAG_KISS, SCARLET_FLANDRE, KOMEIJI_KOISHI,
).with_creator(
    'Amaoto',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1292751339796959263/flandre-koishi-kiss-0011.png',
).with_action(
    ACTION_TAG_KISS, KOMEIJI_KOISHI, SCARLET_FLANDRE,
).with_creator(
    'Hanuu',
).with_editor(
    'HuyaneMatsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1292751339549491241/flandre-koishi-kiss-0012.png',
).with_action(
    ACTION_TAG_KISS, SCARLET_FLANDRE, KOMEIJI_KOISHI,
).with_creator(
    'Hanuu',
).with_editor(
    'HuyaneMatsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1292751340551798784/koishi-wave-0000.png',
).with_action(
    ACTION_TAG_WAVE, KOMEIJI_KOISHI, None,
).with_creator(
    'Hanuu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294656509841637456/keine-fluff_self-0000.png',
).with_action(
    ACTION_TAG_FLUFF_SELF, KAMISHIRASAWA_KEINE, KAMISHIRASAWA_KEINE,
).with_creator(
    'Hanuu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1292880043885723712/flandre-koishi-kiss-0013.png',
).with_action(
    ACTION_TAG_KISS, KOMEIJI_KOISHI, SCARLET_FLANDRE,
).with_creator(
    'Sekichun',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1292882604978081872/flandre-koishi-hug-0008.png',
).with_action(
    ACTION_TAG_HUG, KOMEIJI_KOISHI, SCARLET_FLANDRE,
).with_creator(
    'Nasukon',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1292882605305233409/flandre-koishi-kiss-0014.png',
).with_action(
    ACTION_TAG_KISS, SCARLET_FLANDRE, KOMEIJI_KOISHI,
).with_creator(
    'Nasukon',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1292882605825458176/flandre-koishi-hug-0006.png',
).with_action(
    ACTION_TAG_HUG, KOMEIJI_KOISHI, SCARLET_FLANDRE,
).with_creator(
    'Nasukon',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1292882909107327149/flandre-koishi-pocky-0000.png',
).with_action(
    ACTION_TAG_POCKY, KOMEIJI_KOISHI, SCARLET_FLANDRE,
).with_creator(
    'Nasukon',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1292882606538625065/flandre-koishi-handhold-0003.png',
).with_actions(
    (ACTION_TAG_HANDHOLD, SCARLET_FLANDRE, KOMEIJI_KOISHI),
    (ACTION_TAG_HANDHOLD, KOMEIJI_KOISHI, SCARLET_FLANDRE),
).with_creator(
    'Nasukon',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1292882606873903236/flandre-koishi-handhold-0000.png',
).with_actions(
    (ACTION_TAG_HANDHOLD, SCARLET_FLANDRE, KOMEIJI_KOISHI),
    (ACTION_TAG_HANDHOLD, KOMEIJI_KOISHI, SCARLET_FLANDRE),
).with_creator(
    'Nasukon',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1292885080225615953/flandre-koishi-kiss-0015.png',
).with_action(
    ACTION_TAG_KISS, KOMEIJI_KOISHI, SCARLET_FLANDRE,
).with_creator(
    'Mio/Mia',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1292885972744405092/murasa-nue-handhold-0001.png',
).with_actions(
    (ACTION_TAG_HANDHOLD, MURASA_MINAMITSU, HOUJUU_NUE),
    (ACTION_TAG_HANDHOLD, HOUJUU_NUE, MURASA_MINAMITSU),
).with_creator(
    'k0269323474256',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1292885973411037305/murasa-nue-kiss-0001.png',
).with_actions(
    (ACTION_TAG_KISS, MURASA_MINAMITSU, HOUJUU_NUE),
    (ACTION_TAG_KISS, HOUJUU_NUE, MURASA_MINAMITSU),
).with_creator(
    'k0269323474256',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294585661994827787/reisen-stare-0002.png',
).with_action(
    ACTION_TAG_STARE, REISEN_UDONGEIN_INABA, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294585666159644723/nue-stare-0055.png',
).with_action(
    ACTION_TAG_STARE, HOUJUU_NUE, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294585671389810701/koishi-stare-0018.png',
).with_action(
    ACTION_TAG_STARE, KOMEIJI_KOISHI, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294585674812362773/doremy-stare-0001.png',
).with_action(
    ACTION_TAG_STARE, DOREMY_SWEET, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294585679509983232/nue-stare-0048.png',
).with_action(
    ACTION_TAG_STARE, HOUJUU_NUE, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294585685377814558/merlin-stare-0000.png',
).with_action(
    ACTION_TAG_STARE, PRISMRIVER_MERLIN, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294585690062983209/junko-stare-0005.png',
).with_action(
    ACTION_TAG_STARE, JUNKO, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294585696870334535/shou-stare-0002.png',
).with_action(
    ACTION_TAG_STARE, TORAMARU_SHOU, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294585700402069524/aya-stare-0003.png',
).with_action(
    ACTION_TAG_STARE, SHAMEIMARU_AYA, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294585709369364510/akyuu-stare-0000.png',
).with_action(
    ACTION_TAG_STARE, HIEDA_NO_AKYUU, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294585712481669130/nue-stare-0018.png',
).with_action(
    ACTION_TAG_STARE, HOUJUU_NUE, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294585719330967552/joon-stare-0001.png',
).with_action(
    ACTION_TAG_STARE, YORIGAMI_JOON, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294585723768541205/seija-stare-0008.png',
).with_action(
    ACTION_TAG_STARE, KIJIN_SEIJA, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294585729766129674/miko-stare-0001.png',
).with_action(
    ACTION_TAG_STARE, TOYOSATOMIMI_NO_MIKO, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294585735965573140/sakuya-stare-0003.png',
).with_action(
    ACTION_TAG_STARE, IZAYOI_SAKUYA, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294585741342543892/futo-stare-0001.png',
).with_action(
    ACTION_TAG_STARE, MONONOBE_NO_FUTO, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294585744899444778/nue-stare-0011.png',
).with_action(
    ACTION_TAG_STARE, HOUJUU_NUE, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294585749072773201/youmu-stare-0002.png',
).with_action(
    ACTION_TAG_STARE, KONPAKU_YOUMU, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294585755061977098/nue-stare-0002.png',
).with_action(
    ACTION_TAG_STARE, HOUJUU_NUE, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294585759071731713/koishi-stare-0004.png',
).with_action(
    ACTION_TAG_STARE, KOMEIJI_KOISHI, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294585764310421584/kutaka-stare-0001.png',
).with_action(
    ACTION_TAG_STARE, NIWATARI_KUTAKA, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294585769284993045/chimata-stare-0002.png',
).with_action(
    ACTION_TAG_STARE, TENKYUU_CHIMATA, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294585775970586654/sagume-stare-0004.png',
).with_action(
    ACTION_TAG_STARE, KISHIN_SAGUME, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294585778479038494/sakuya-stare-0006.png',
).with_action(
    ACTION_TAG_STARE, IZAYOI_SAKUYA, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294585780702019715/satori-stare-0004.png',
).with_action(
    ACTION_TAG_STARE, KOMEIJI_SATORI, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294585786573914163/hecatia-stare-0005.png',
).with_action(
    ACTION_TAG_STARE, HECATIA_LAPISLAZULI, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294585796019617832/mokou-stare-0004.png',
).with_action(
    ACTION_TAG_STARE, FUJIWARA_NO_MOKOU, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294585802957000766/nue-stare-0001.png',
).with_action(
    ACTION_TAG_STARE, HOUJUU_NUE, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294585808543551498/nue-stare-0033.png',
).with_action(
    ACTION_TAG_STARE, HOUJUU_NUE, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294585814180827146/reimu-stare-0015.png',
).with_action(
    ACTION_TAG_STARE, HAKUREI_REIMU, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294585819717308447/tenshi-stare-0003.png',
).with_action(
    ACTION_TAG_STARE, HINANAWI_TENSHI, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294585826021478470/shinmyoumaru-stare-0000.png',
).with_action(
    ACTION_TAG_STARE, SUKUNA_SHINMYOUMARU, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294585831176142898/kanako-stare-0001.png',
).with_action(
    ACTION_TAG_STARE, YASAKA_KANAKO, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294585833776615424/nue-stare-0043.png',
).with_action(
    ACTION_TAG_STARE, HOUJUU_NUE, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294585836284809258/nue-stare-0032.png',
).with_action(
    ACTION_TAG_STARE, HOUJUU_NUE, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294585841917628447/alice-stare-0000.png',
).with_action(
    ACTION_TAG_STARE, MARGATROID_ALICE, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294585846506455051/chiruno-stare-0001.png',
).with_action(
    ACTION_TAG_STARE, CHIRUNO, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294585851954855987/letty-stare-0002.png',
).with_action(
    ACTION_TAG_STARE, LETTY_WHITEROCK, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294585857621233674/reimu-stare-0006.png',
).with_action(
    ACTION_TAG_STARE, HAKUREI_REIMU, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294585862473912363/mystia-stare-0004.png',
).with_action(
    ACTION_TAG_STARE, LORELEI_MYSTIA, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294585867201155172/rumia-stare-0000.png',
).with_action(
    ACTION_TAG_STARE, RUMIA, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294585871189807125/seija-stare-0017.png',
).with_action(
    ACTION_TAG_STARE, KIJIN_SEIJA, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294585876474761256/keine-stare-0003.png',
).with_action(
    ACTION_TAG_STARE, KAMISHIRASAWA_KEINE, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294585881138823188/suwako-stare-0002.png',
).with_action(
    ACTION_TAG_STARE, MORIYA_SUWAKO, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294585885941305364/sekibanki-stare-0002.png',
).with_action(
    ACTION_TAG_STARE, SEKIBANKI, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294585890663825449/nue-stare-0008.png',
).with_action(
    ACTION_TAG_STARE, HOUJUU_NUE, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294585895676153888/flandre-stare-0010.png',
).with_action(
    ACTION_TAG_STARE, SCARLET_FLANDRE, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294585900017254431/eiki-stare-0001.png',
).with_action(
    ACTION_TAG_STARE, SHIKI_EIKI_YAMAXANADU, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294585906648584243/nue-stare-0021.png',
).with_action(
    ACTION_TAG_STARE, HOUJUU_NUE, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294585914709901362/koishi-stare-0005.png',
).with_action(
    ACTION_TAG_STARE, KOMEIJI_KOISHI, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294585920279937115/ichirin-stare-0000.png',
).with_action(
    ACTION_TAG_STARE, KUMOI_ICHIRIN, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294585924939812915/nue-stare-0049.png',
).with_action(
    ACTION_TAG_STARE, HOUJUU_NUE, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294585930073505792/nue-stare-0026.png',
).with_action(
    ACTION_TAG_STARE, HOUJUU_NUE, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294585936151318640/okuu-stare-0002.png',
).with_action(
    ACTION_TAG_STARE, REIUJI_UTSUHO, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294585940853129216/seija-stare-0016.png',
).with_action(
    ACTION_TAG_STARE, KIJIN_SEIJA, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294585944422350849/saki-stare-0000.png',
).with_action(
    ACTION_TAG_STARE, KUROKOMA_SAKI, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294585948230647859/tokiko-stare-0000.png',
).with_action(
    ACTION_TAG_STARE, TOKIKO, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294585951636684952/nue-murder-0000.png',
).with_action(
    ACTION_TAG_MURDER, HOUJUU_NUE, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294585956128526346/nue-stare-0013.png',
).with_action(
    ACTION_TAG_STARE, HOUJUU_NUE, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294601426739400797/satono-tmai-stare-0000.png',
).with_actions(
    (ACTION_TAG_STARE, TEIREIDA_MAI, None),
    (ACTION_TAG_STARE, NISHIDA_SATONO, None),
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294585968342597674/komachi-stare-0002.png',
).with_action(
    ACTION_TAG_STARE, ONOZUKA_KOMACHI, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294585972977041408/nue-stare-0034.png',
).with_action(
    ACTION_TAG_STARE, HOUJUU_NUE, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294585977159024761/suwako-stare-0001.png',
).with_action(
    ACTION_TAG_STARE, MORIYA_SUWAKO, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294585984046071818/reimu-stare-0008.png',
).with_action(
    ACTION_TAG_STARE, HAKUREI_REIMU, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294585986206011422/seija-stare-0006.png',
).with_action(
    ACTION_TAG_STARE, KIJIN_SEIJA, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294585992312913961/ichirin-stare-0001.png',
).with_action(
    ACTION_TAG_STARE, KUMOI_ICHIRIN, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294586004300365864/parsee-stare-0002.png',
).with_action(
    ACTION_TAG_STARE, MIZUHASHI_PARSEE, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294586009949966376/reimu-stare-0011.png',
).with_action(
    ACTION_TAG_STARE, HAKUREI_REIMU, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294586013238427669/parsee-stare-0000.png',
).with_action(
    ACTION_TAG_STARE, MIZUHASHI_PARSEE, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294586025154183230/yachie-stare-0004.png',
).with_action(
    ACTION_TAG_STARE, KICCHOU_YACHIE, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294586032779563019/satori-stare-0003.png',
).with_action(
    ACTION_TAG_STARE, KOMEIJI_SATORI, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294586038672556042/nue-stare-0031.png',
).with_action(
    ACTION_TAG_STARE, HOUJUU_NUE, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294586043848458331/nue-stare-0007.png',
).with_action(
    ACTION_TAG_STARE, HOUJUU_NUE, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294586047178477588/nue-stare-0012.png',
).with_action(
    ACTION_TAG_STARE, HOUJUU_NUE, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294586052828336212/suwako-stare-0000.png',
).with_action(
    ACTION_TAG_STARE, MORIYA_SUWAKO, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294586058104766507/rumia-stare-0001.png',
).with_action(
    ACTION_TAG_STARE, RUMIA, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294586061217071136/seija-stare-0014.png',
).with_action(
    ACTION_TAG_STARE, KIJIN_SEIJA, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294586065998581820/hijiri-stare-0000.png',
).with_action(
    ACTION_TAG_STARE, HIJIRI_BYAKUREN, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294586071979393057/yuugi-stare-0000.png',
).with_action(
    ACTION_TAG_STARE, HOSHIGUMA_YUUGI, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294586077121613926/nue-stare-0054.png',
).with_action(
    ACTION_TAG_STARE, HOUJUU_NUE, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294586082842902609/wakasagihime-stare-0001.png',
).with_action(
    ACTION_TAG_STARE, WAKASAGIHIME, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294586085820731412/nue-stare-0027.png',
).with_action(
    ACTION_TAG_STARE, HOUJUU_NUE, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294586089905979472/reimu-stare-0007.png',
).with_action(
    ACTION_TAG_STARE, HAKUREI_REIMU, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294586095912095785/zanmu-stare-0000.png',
).with_action(
    ACTION_TAG_STARE, NIPPAKU_ZANMU, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294586101431799859/yuuma-stare-0001.png',
).with_action(
    ACTION_TAG_STARE, TOUTETSU_YUUMA, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294586108021182516/flandre-stare-0009.png',
).with_action(
    ACTION_TAG_STARE, SCARLET_FLANDRE, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294586114740584468/seija-stare-0020.png',
).with_action(
    ACTION_TAG_STARE, KIJIN_SEIJA, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294586119630880768/chimata-stare-0001.png',
).with_action(
    ACTION_TAG_STARE, TENKYUU_CHIMATA, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294586127763902504/koishi-stare-0016.png',
).with_action(
    ACTION_TAG_STARE, KOMEIJI_KOISHI, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294586131601555456/sagume-stare-0003.png',
).with_action(
    ACTION_TAG_STARE, KISHIN_SAGUME, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294586135405924372/tenshi-stare-0001.png',
).with_action(
    ACTION_TAG_STARE, HINANAWI_TENSHI, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294586139897892864/nue-stare-0041.png',
).with_action(
    ACTION_TAG_STARE, HOUJUU_NUE, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294586145723908147/seija-stare-0000.png',
).with_action(
    ACTION_TAG_STARE, KIJIN_SEIJA, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294586151562121216/nue-stare-0051.png',
).with_action(
    ACTION_TAG_STARE, HOUJUU_NUE, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294586154611642388/mystia-stare-0000.png',
).with_action(
    ACTION_TAG_STARE, LORELEI_MYSTIA, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294586160546320415/kogasa-stare-0009.png',
).with_action(
    ACTION_TAG_STARE, TATARA_KOGASA, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294586165114179595/seija-stare-0018.png',
).with_action(
    ACTION_TAG_STARE, KIJIN_SEIJA, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294586168457039995/koishi-satori-hug-0010.png',
).with_action(
    ACTION_TAG_HUG, KOMEIJI_SATORI, KOMEIJI_KOISHI,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294586170981879818/seija-stare-0005.png',
).with_action(
    ACTION_TAG_STARE, KIJIN_SEIJA, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294586176061046874/kagerou-stare-0003.png',
).with_action(
    ACTION_TAG_STARE, IMAIZUMI_KAGEROU, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294586180175921173/kogasa-nue-hug-0001.png',
).with_action(
    ACTION_TAG_HUG, TATARA_KOGASA, HOUJUU_NUE,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294586184676409354/shou-stare-0001.png',
).with_action(
    ACTION_TAG_STARE, TORAMARU_SHOU, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294586188241567805/kogasa-nue-handhold-0002.png',
).with_actions(
    (ACTION_TAG_HANDHOLD, HOUJUU_NUE, TATARA_KOGASA),
    (ACTION_TAG_HANDHOLD, TATARA_KOGASA, HOUJUU_NUE),
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294586195623542794/sagume-stare-0000.png',
).with_action(
    ACTION_TAG_STARE, KISHIN_SAGUME, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294586199494885459/rumia-stare-0003.png',
).with_action(
    ACTION_TAG_STARE, RUMIA, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294586204024475658/nue-stare-0040.png',
).with_action(
    ACTION_TAG_STARE, HOUJUU_NUE, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294586207547949066/nue-stare-0010.png',
).with_action(
    ACTION_TAG_STARE, HOUJUU_NUE, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294586212039786497/kogasa-stare-0003.png',
).with_action(
    ACTION_TAG_STARE, TATARA_KOGASA, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294586216737542154/seija-stare-0013.png',
).with_action(
    ACTION_TAG_STARE, KIJIN_SEIJA, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294586222639054869/aya-stare-0004.png',
).with_action(
    ACTION_TAG_STARE, SHAMEIMARU_AYA, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294586226002890783/reimu-stare-0004.png',
).with_action(
    ACTION_TAG_STARE, HAKUREI_REIMU, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294586229072855120/nue-stare-0037.png',
).with_action(
    ACTION_TAG_STARE, HOUJUU_NUE, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294586233376215061/nue-stare-0015.png',
).with_action(
    ACTION_TAG_STARE, HOUJUU_NUE, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294586238287745087/nue-stare-0019.png',
).with_action(
    ACTION_TAG_STARE, HOUJUU_NUE, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294586241379205130/ringo-stare-0000.png',
).with_action(
    ACTION_TAG_STARE, RINGO, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294586245279911936/remilia-stare-0006.png',
).with_action(
    ACTION_TAG_STARE, SCARLET_REMILIA, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294586251260989543/koishi-stare-0011.png',
).with_action(
    ACTION_TAG_STARE, KOMEIJI_KOISHI, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294586256369389569/kogasa-stare-0007.png',
).with_action(
    ACTION_TAG_STARE, TATARA_KOGASA, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294586260622544937/murasa-stare-0001.png',
).with_action(
    ACTION_TAG_STARE, MURASA_MINAMITSU, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294586263361290271/seija-stare-0015.png',
).with_action(
    ACTION_TAG_STARE, KIJIN_SEIJA, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294586266221936660/nue-stare-0053.png',
).with_action(
    ACTION_TAG_STARE, HOUJUU_NUE, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294586270479028325/nue-stare-0009.png',
).with_action(
    ACTION_TAG_STARE, HOUJUU_NUE, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294586274270941214/nue-stare-0020.png',
).with_action(
    ACTION_TAG_STARE, HOUJUU_NUE, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294586280491089991/eiki-stare-0003.png',
).with_action(
    ACTION_TAG_STARE, SHIKI_EIKI_YAMAXANADU, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294586287378141297/kagerou-stare-0002.png',
).with_action(
    ACTION_TAG_STARE, IMAIZUMI_KAGEROU, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294586293120139300/nue-stare-0005.png',
).with_action(
    ACTION_TAG_STARE, HOUJUU_NUE, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294586299910717440/rumia-stare-0002.png',
).with_action(
    ACTION_TAG_STARE, RUMIA, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294586304524455936/doremy-stare-0003.png',
).with_action(
    ACTION_TAG_STARE, DOREMY_SWEET, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294586308471164950/doremy-stare-0005.png',
).with_action(
    ACTION_TAG_STARE, DOREMY_SWEET, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294586312178798632/clownpiece-hecatia-junko-pat-0000.png',
).with_action(
    ACTION_TAG_PAT, HECATIA_LAPISLAZULI, CLOWNPIECE,
).with_characters(
    JUNKO,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294586317832720465/hina-stare-0002.png',
).with_action(
    ACTION_TAG_STARE, KAGIYAMA_HINA, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294586329480298496/koishi-stare-0010.png',
).with_action(
    ACTION_TAG_STARE, KOMEIJI_KOISHI, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294586334840619110/orin-stare-0004.png',
).with_action(
    ACTION_TAG_STARE, KAENBYOU_RIN, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294586340352069692/koishi-stare-0014.png',
).with_action(
    ACTION_TAG_STARE, KOMEIJI_KOISHI, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294586343065653258/kogasa-nue-handhold-0000.png',
).with_actions(
    (ACTION_TAG_HANDHOLD, HOUJUU_NUE, TATARA_KOGASA),
    (ACTION_TAG_HANDHOLD, TATARA_KOGASA, HOUJUU_NUE),
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294586348681822268/kanako-stare-0002.png',
).with_action(
    ACTION_TAG_STARE, YASAKA_KANAKO, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294586355212357672/clownpiece-stare-0001.png',
).with_action(
    ACTION_TAG_STARE, CLOWNPIECE, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294586362531676160/seija-stare-0023.png',
).with_action(
    ACTION_TAG_STARE, KIJIN_SEIJA, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294586367829082152/yamame-stare-0000.png',
).with_action(
    ACTION_TAG_STARE, KURODANI_YAMAME, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294603810945105994/takane-stare-0000.png',
).with_action(
    ACTION_TAG_STARE, YAMASHIRO_TAKANE, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294601576350220298/satono-tmai-hug-0000.png',
).with_actions(
    (ACTION_TAG_HUG, NISHIDA_SATONO, TEIREIDA_MAI),
    (ACTION_TAG_HUG, TEIREIDA_MAI, NISHIDA_SATONO),
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294586388192428082/flandre-stare-0006.png',
).with_action(
    ACTION_TAG_STARE, SCARLET_FLANDRE, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294586394282430504/seija-stare-0001.png',
).with_action(
    ACTION_TAG_STARE, KIJIN_SEIJA, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294586401546833941/urumi-stare-0001.png',
).with_action(
    ACTION_TAG_STARE, USHIZAKI_URUMI, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294586408329154621/parsee-stare-0004.png',
).with_action(
    ACTION_TAG_STARE, MIZUHASHI_PARSEE, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294586411877666826/nue-stare-0014.png',
).with_action(
    ACTION_TAG_STARE, HOUJUU_NUE, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294586414981320714/nue-seija-stare-0000.png',
).with_actions(
    (ACTION_TAG_STARE, HOUJUU_NUE, None),
    (ACTION_TAG_STARE, KIJIN_SEIJA, None),
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294586420677050378/nue-stare-0038.png',
).with_action(
    ACTION_TAG_STARE, HOUJUU_NUE, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294586426091900958/koishi-stare-0015.png',
).with_action(
    ACTION_TAG_STARE, KOMEIJI_KOISHI, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294586430005444649/junko-stare-0006.png',
).with_action(
    ACTION_TAG_STARE, JUNKO, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294586434761523252/doremy-stare-0006.png',
).with_action(
    ACTION_TAG_STARE, DOREMY_SWEET, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294586438666555475/seiga-stare-0000.png',
).with_action(
    ACTION_TAG_STARE, KAKU_SEIGA, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294586444475797626/miko-stare-0000.png',
).with_action(
    ACTION_TAG_STARE, TOYOSATOMIMI_NO_MIKO, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294586449210904649/wakasagihime-stare-0002.png',
).with_action(
    ACTION_TAG_STARE, WAKASAGIHIME, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294586453317128223/kokoro-mamizou-fluff-0003.png',
).with_action(
    ACTION_TAG_FLUFF, HATA_NO_KOKORO, FUTATSUIWA_MAMIZOU,
).with_creator(
    'makuwauri',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294586457960349790/nue-stare-0025.png',
).with_action(
    ACTION_TAG_STARE, HOUJUU_NUE, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294586461789884466/satori-stare-0002.png',
).with_action(
    ACTION_TAG_STARE, KOMEIJI_SATORI, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294586465350717470/keine-mokou-kiss-0001.png',
).with_action(
    ACTION_TAG_KISS, KAMISHIRASAWA_KEINE, FUJIWARA_NO_MOKOU,
).with_creator(
    'imonatsuki',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294586468265627648/nue-stare-0056.png',
).with_action(
    ACTION_TAG_STARE, HOUJUU_NUE, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294586473420689519/raiko-stare-0000.png',
).with_action(
    ACTION_TAG_STARE, HORIKAWA_RAIKO, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294586479087190119/yukari-stare-0001.png',
).with_action(
    ACTION_TAG_STARE, YAKUMO_YUKARI, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294586482870190165/sekibanki-stare-0001.png',
).with_action(
    ACTION_TAG_STARE, SEKIBANKI, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294586488973037598/yuyuko-stare-0000.png',
).with_action(
    ACTION_TAG_STARE, SAIGYOUJI_YUYUKO, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294586494220242964/remilia-stare-0000.png',
).with_action(
    ACTION_TAG_STARE, SCARLET_REMILIA, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294586499131506740/kogasa-stare-0008.png',
).with_action(
    ACTION_TAG_STARE, TATARA_KOGASA, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294586503174950942/ichirin-stare-0002.png',
).with_action(
    ACTION_TAG_STARE, KUMOI_ICHIRIN, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294586505859174460/nue-stare-0024.png',
).with_action(
    ACTION_TAG_STARE, HOUJUU_NUE, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294586510632423489/tsukasa-stare-0001.png',
).with_action(
    ACTION_TAG_STARE, KUDAMAKI_TSUKASA, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294586516592525354/shion-stare-0001.png',
).with_action(
    ACTION_TAG_STARE, YORIGAMI_SHION, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294586521835274263/mystia-stare-0006.png',
).with_action(
    ACTION_TAG_STARE, LORELEI_MYSTIA, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294586526407065620/megumu-stare-0001.png',
).with_action(
    ACTION_TAG_STARE, IIZUNAMARU_MEGUMU, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294586531872509993/youmu-stare-0001.png',
).with_action(
    ACTION_TAG_STARE, KONPAKU_YOUMU, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294586537450672179/reimu-stare-0005.png',
).with_action(
    ACTION_TAG_STARE, HAKUREI_REIMU, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294586541535920139/seija-stare-0002.png',
).with_action(
    ACTION_TAG_STARE, KIJIN_SEIJA, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294586546200117289/junko-stare-0003.png',
).with_action(
    ACTION_TAG_STARE, JUNKO, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294586552353030165/tokiko-stare-0003.png',
).with_action(
    ACTION_TAG_STARE, TOKIKO, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294586557025488967/kogasa-stare-0011.png',
).with_action(
    ACTION_TAG_STARE, TATARA_KOGASA, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294586562599714898/kutaka-stare-0003.png',
).with_action(
    ACTION_TAG_STARE, NIWATARI_KUTAKA, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294586565116559370/marisa-stare-0002.png',
).with_action(
    ACTION_TAG_STARE, KIRISAME_MARISA, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294586569403138101/nazrin-stare-0001.png',
).with_action(
    ACTION_TAG_STARE, NAZRIN, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294586573572276284/seija-stare-0019.png',
).with_action(
    ACTION_TAG_STARE, KIJIN_SEIJA, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294586577267326977/hatate-stare-0000.png',
).with_action(
    ACTION_TAG_STARE, HIMEKAIDOU_HATATE, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294586583550267482/shion-stare-0000.png',
).with_action(
    ACTION_TAG_STARE, YORIGAMI_SHION, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294586586469765251/junko-stare-0002.png',
).with_action(
    ACTION_TAG_STARE, JUNKO, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294586590961602603/rumia-stare-0004.png',
).with_action(
    ACTION_TAG_STARE, RUMIA, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294586596900737054/kutaka-stare-0000.png',
).with_action(
    ACTION_TAG_STARE, NIWATARI_KUTAKA, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294586602848522303/mokou-stare-0003.png',
).with_action(
    ACTION_TAG_STARE, FUJIWARA_NO_MOKOU, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294586607394881648/koishi-stare-0013.png',
).with_action(
    ACTION_TAG_STARE, KOMEIJI_KOISHI, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294608139034955776/lily_white-wave-0000.png',
).with_action(
    ACTION_TAG_WAVE, LILY_WHITE, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294586617071276083/junko-stare-0007.png',
).with_action(
    ACTION_TAG_STARE, JUNKO, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294586622280728586/nue-stare-0006.png',
).with_action(
    ACTION_TAG_STARE, HOUJUU_NUE, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294586627410235473/nue-stare-0003.png',
).with_action(
    ACTION_TAG_STARE, HOUJUU_NUE, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294586631919239188/seija-stare-0021.png',
).with_action(
    ACTION_TAG_STARE, KIJIN_SEIJA, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294586637895991306/satori-stare-0001.png',
).with_action(
    ACTION_TAG_STARE, KOMEIJI_SATORI, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294586644376059945/murasa-nue-handhold-0002.png',
).with_actions(
    (ACTION_TAG_HANDHOLD, HOUJUU_NUE, MURASA_MINAMITSU),
    (ACTION_TAG_HANDHOLD, MURASA_MINAMITSU, HOUJUU_NUE),
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294586647886823444/kogasa-nue-lick-0000.png',
).with_action(
    ACTION_TAG_LICK, TATARA_KOGASA, HOUJUU_NUE,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294586652576055306/komachi-stare-0001.png',
).with_action(
    ACTION_TAG_STARE, ONOZUKA_KOMACHI, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294586657319948359/remilia-stare-0007.png',
).with_action(
    ACTION_TAG_STARE, SCARLET_REMILIA, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294586660536717352/parsee-stare-0003.png',
).with_action(
    ACTION_TAG_STARE, MIZUHASHI_PARSEE, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294586665570009090/keine-stare-0004.png',
).with_action(
    ACTION_TAG_STARE, KAMISHIRASAWA_KEINE, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294586670049525823/hecatia-stare-0004.png',
).with_action(
    ACTION_TAG_STARE, HECATIA_LAPISLAZULI, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294586674533367818/hecatia-stare-0003.png',
).with_action(
    ACTION_TAG_STARE, HECATIA_LAPISLAZULI, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294586678299856948/urumi-stare-0000.png',
).with_action(
    ACTION_TAG_STARE, USHIZAKI_URUMI, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294586682196234300/seija-stare-0022.png',
).with_action(
    ACTION_TAG_STARE, KIJIN_SEIJA, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294586689410301962/mayumi-stare-0002.png',
).with_action(
    ACTION_TAG_STARE, JOUTOUGUU_MAYUMI, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294586696788217917/eiki-stare-0006.png',
).with_action(
    ACTION_TAG_STARE, SHIKI_EIKI_YAMAXANADU, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294586701804601385/reimu-stare-0016.png',
).with_action(
    ACTION_TAG_STARE, HAKUREI_REIMU, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294586708204978266/remilia-stare-0004.png',
).with_action(
    ACTION_TAG_STARE, SCARLET_REMILIA, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294586716195258491/flandre-stare-0017.png',
).with_action(
    ACTION_TAG_STARE, SCARLET_FLANDRE, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294586721106923570/nue-stare-0035.png',
).with_action(
    ACTION_TAG_STARE, HOUJUU_NUE, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294586726790074459/nue-stare-0030.png',
).with_action(
    ACTION_TAG_STARE, HOUJUU_NUE, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294586732011847680/chen-ran-hug-0002.png',
).with_action(
    ACTION_TAG_HUG, CHEN, YAKUMO_RAN,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294586735984119839/seija-stare-0003.png',
).with_action(
    ACTION_TAG_STARE, KIJIN_SEIJA, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294586741457424425/reimu-stare-0010.png',
).with_action(
    ACTION_TAG_STARE, HAKUREI_REIMU, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294586744552947782/nue-stare-0036.png',
).with_action(
    ACTION_TAG_STARE, HOUJUU_NUE, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294586749254897717/yachie-stare-0003.png',
).with_action(
    ACTION_TAG_STARE, KICCHOU_YACHIE, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294586752480051200/koishi-stare-0009.png',
).with_action(
    ACTION_TAG_STARE, KOMEIJI_KOISHI, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294586758255611905/komachi-stare-0000.png',
).with_action(
    ACTION_TAG_STARE, ONOZUKA_KOMACHI, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294586762080944240/reimu-stare-0009.png',
).with_action(
    ACTION_TAG_STARE, HAKUREI_REIMU, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294586768833908790/koishi-stare-0006.png',
).with_action(
    ACTION_TAG_STARE, KOMEIJI_KOISHI, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294586773934182483/tokiko-stare-0002.png',
).with_action(
    ACTION_TAG_STARE, TOKIKO, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294586777121718283/mokou-stare-0005.png',
).with_action(
    ACTION_TAG_STARE, FUJIWARA_NO_MOKOU, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294586781320089711/remilia-stare-0001.png',
).with_action(
    ACTION_TAG_STARE, SCARLET_REMILIA, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294586786500182088/koishi-stare-0008.png',
).with_action(
    ACTION_TAG_STARE, KOMEIJI_KOISHI, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294586795165487114/junko-stare-0008.png',
).with_action(
    ACTION_TAG_STARE, JUNKO, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294586803780718702/eiki-stare-0002.png',
).with_action(
    ACTION_TAG_STARE, SHIKI_EIKI_YAMAXANADU, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294586807442210816/clownpiece-hecatia-pat-0001.png',
).with_action(
    ACTION_TAG_PAT, HECATIA_LAPISLAZULI, CLOWNPIECE,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294586813154983988/aya-stare-0002.png',
).with_action(
    ACTION_TAG_STARE, SHAMEIMARU_AYA, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294586818435743764/mystia-stare-0003.png',
).with_action(
    ACTION_TAG_STARE, LORELEI_MYSTIA, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294586824936788061/reimu-stare-0014.png',
).with_action(
    ACTION_TAG_STARE, HAKUREI_REIMU, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294586828187373628/nue-stare-0047.png',
).with_action(
    ACTION_TAG_STARE, HOUJUU_NUE, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294586837649719318/tenshi-stare-0002.png',
).with_action(
    ACTION_TAG_STARE, HINANAWI_TENSHI, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294586845824417792/joon-stare-0000.png',
).with_action(
    ACTION_TAG_STARE, YORIGAMI_JOON, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294586851620945921/kogasa-nue-handhold-0001.png',
).with_actions(
    (ACTION_TAG_HANDHOLD, HOUJUU_NUE, TATARA_KOGASA),
    (ACTION_TAG_HANDHOLD, TATARA_KOGASA, HOUJUU_NUE),
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294586857236992041/sanae-stare-0000.png',
).with_action(
    ACTION_TAG_STARE, KOCHIYA_SANAE, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294586862513688586/nue-seija-stare-0001.png',
).with_actions(
    (ACTION_TAG_STARE, HOUJUU_NUE, None),
    (ACTION_TAG_STARE, KIJIN_SEIJA, None),
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294586868167344188/seija-stare-0009.png',
).with_action(
    ACTION_TAG_STARE, KIJIN_SEIJA, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294586874903658569/aya-stare-0000.png',
).with_action(
    ACTION_TAG_STARE, SHAMEIMARU_AYA, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294586880377225216/seija-stare-0004.png',
).with_action(
    ACTION_TAG_STARE, KIJIN_SEIJA, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294586886328946770/nazrin-stare-0003.png',
).with_action(
    ACTION_TAG_STARE, NAZRIN, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294586892389580911/letty-stare-0003.png',
).with_action(
    ACTION_TAG_STARE, LETTY_WHITEROCK, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294586899092082772/wakasagihime-stare-0000.png',
).with_action(
    ACTION_TAG_STARE, WAKASAGIHIME, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294586905760895009/seija-stare-0010.png',
).with_action(
    ACTION_TAG_STARE, KIJIN_SEIJA, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294586910911758389/parsee-stare-0001.png',
).with_action(
    ACTION_TAG_STARE, MIZUHASHI_PARSEE, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294586916485857372/flandre-stare-0011.png',
).with_action(
    ACTION_TAG_STARE, SCARLET_FLANDRE, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294586921112043610/nue-stare-0050.png',
).with_action(
    ACTION_TAG_STARE, HOUJUU_NUE, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294586927399436309/kogasa-stare-0004.png',
).with_action(
    ACTION_TAG_STARE, TATARA_KOGASA, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294586933212876800/koishi-stare-0017.png',
).with_action(
    ACTION_TAG_STARE, KOMEIJI_KOISHI, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294586938187317288/sagume-stare-0002.png',
).with_action(
    ACTION_TAG_STARE, KISHIN_SAGUME, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294586941869654017/kogasa-stare-0005.png',
).with_action(
    ACTION_TAG_STARE, TATARA_KOGASA, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294586947229978644/mystia-stare-0007.png',
).with_action(
    ACTION_TAG_STARE, LORELEI_MYSTIA, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294586951994839041/doremy-stare-0004.png',
).with_action(
    ACTION_TAG_STARE, DOREMY_SWEET, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294586956117970995/nue-stare-0017.png',
).with_action(
    ACTION_TAG_STARE, HOUJUU_NUE, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294586962585452605/flandre-stare-0012.png',
).with_action(
    ACTION_TAG_STARE, SCARLET_FLANDRE, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294586968977575957/hina-stare-0003.png',
).with_action(
    ACTION_TAG_STARE, KAGIYAMA_HINA, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294609359610974249/futo-stare-0002.png',
).with_action(
    ACTION_TAG_STARE, MONONOBE_NO_FUTO, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294586979488497698/hecatia-junko-hug-0002.png',
).with_action(
    ACTION_TAG_HUG, HECATIA_LAPISLAZULI, JUNKO,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294586984878051339/flandre-stare-0015.png',
).with_action(
    ACTION_TAG_STARE, SCARLET_FLANDRE, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294586989915541576/seija-stare-0012.png',
).with_action(
    ACTION_TAG_STARE, KIJIN_SEIJA, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294586993505734740/yuuka-stare-0003.png',
).with_action(
    ACTION_TAG_STARE, KAZAMI_YUUKA, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294586996853047296/hina-stare-0004.png',
).with_action(
    ACTION_TAG_STARE, KAGIYAMA_HINA, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294587003114881126/eiki-stare-0000.png',
).with_action(
    ACTION_TAG_STARE, SHIKI_EIKI_YAMAXANADU, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294587008500498462/larva-stare-0000.png',
).with_action(
    ACTION_TAG_STARE, ETERNITY_LARVA, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294587016272547841/satori-stare-0000.png',
).with_action(
    ACTION_TAG_STARE, KOMEIJI_SATORI, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294587022434111519/ran-stare-0000.png',
).with_action(
    ACTION_TAG_STARE, YAKUMO_RAN, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294587029765754931/letty-stare-0001.png',
).with_action(
    ACTION_TAG_STARE, LETTY_WHITEROCK, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294587038699356223/yuuka-stare-0004.png',
).with_action(
    ACTION_TAG_STARE, KAZAMI_YUUKA, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294587044789485590/kogasa-stare-0012.png',
).with_action(
    ACTION_TAG_STARE, TATARA_KOGASA, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294587048170229812/nue-stare-0004.png',
).with_action(
    ACTION_TAG_STARE, HOUJUU_NUE, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294587052708597841/reimu-stare-0013.png',
).with_action(
    ACTION_TAG_STARE, HAKUREI_REIMU, None,
).with_creator(
    'ichirugi',
)


TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294587058374971412/kutaka-urumi-pat-0000.png',
).with_action(
    ACTION_TAG_PAT, USHIZAKI_URUMI, NIWATARI_KUTAKA,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294587061839597619/yukari-stare-0000.png',
).with_action(
    ACTION_TAG_STARE, YAKUMO_YUKARI, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294587066008473661/yachie-stare-0002.png',
).with_action(
    ACTION_TAG_STARE, KICCHOU_YACHIE, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294587070848827402/clownpiece-stare-0000.png',
).with_action(
    ACTION_TAG_STARE, CLOWNPIECE, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294587074367852606/nazrin-stare-0002.png',
).with_action(
    ACTION_TAG_STARE, NAZRIN, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294587076620320778/hecatia-junko-hug-0001.png',
).with_action(
    ACTION_TAG_HUG, HECATIA_LAPISLAZULI, JUNKO,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294587081724530729/mystia-stare-0001.png',
).with_action(
    ACTION_TAG_STARE, LORELEI_MYSTIA, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294587086371815444/nue-stare-0046.png',
).with_action(
    ACTION_TAG_STARE, HOUJUU_NUE, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294587091837124679/reisen-stare-0001.png',
).with_action(
    ACTION_TAG_STARE, REISEN_UDONGEIN_INABA, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294587096773955668/nue-stare-0052.png',
).with_action(
    ACTION_TAG_STARE, HOUJUU_NUE, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294587110074089473/eiki-stare-0004.png',
).with_action(
    ACTION_TAG_STARE, SHIKI_EIKI_YAMAXANADU, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294587115002400831/nue-stare-0029.png',
).with_action(
    ACTION_TAG_STARE, HOUJUU_NUE, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294587120974827530/nue-stare-0023.png',
).with_action(
    ACTION_TAG_STARE, HOUJUU_NUE, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294587125378842664/nue-stare-0044.png',
).with_action(
    ACTION_TAG_STARE, HOUJUU_NUE, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294587130156158996/mokou-stare-0002.png',
).with_action(
    ACTION_TAG_STARE, FUJIWARA_NO_MOKOU, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294587136821166141/eiki-stare-0005.png',
).with_action(
    ACTION_TAG_STARE, SHIKI_EIKI_YAMAXANADU, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294587141250220042/yuyuko-stare-0001.png',
).with_action(
    ACTION_TAG_STARE, SAIGYOUJI_YUYUKO, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294587147004674091/yachie-stare-0000.png',
).with_action(
    ACTION_TAG_STARE, KICCHOU_YACHIE, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294587151446704179/hecatia-stare-0001.png',
).with_action(
    ACTION_TAG_STARE, HECATIA_LAPISLAZULI, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294587156865749073/seiran-stare-0000.png',
).with_action(
    ACTION_TAG_STARE, SEIRAN, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294587164058714164/sanae-stare-0001.png',
).with_action(
    ACTION_TAG_STARE, KOCHIYA_SANAE, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294587169188479078/koishi-stare-0003.png',
).with_action(
    ACTION_TAG_STARE, KOMEIJI_KOISHI, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294605494253518859/aya-chiruno-lick-0000.png',
).with_action(
    ACTION_TAG_LICK, SHAMEIMARU_AYA, CHIRUNO,
).with_creator(
    'roke (taikodon)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294587178533519442/flandre-stare-0008.png',
).with_action(
    ACTION_TAG_STARE, SCARLET_FLANDRE, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294587183235338296/remilia-stare-0003.png',
).with_action(
    ACTION_TAG_STARE, SCARLET_REMILIA, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294587188452917258/minoriko-stare-0000.png',
).with_action(
    ACTION_TAG_STARE, AKI_MINORIKO, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294587195704873062/kutaka-stare-0002.png',
).with_action(
    ACTION_TAG_STARE, NIWATARI_KUTAKA, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294587200666861578/reimu-stare-0012.png',
).with_action(
    ACTION_TAG_STARE, HAKUREI_REIMU, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294587203967651893/yuuka-stare-0005.png',
).with_action(
    ACTION_TAG_STARE, KAZAMI_YUUKA, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294587209646608404/mystia-stare-0002.png',
).with_action(
    ACTION_TAG_STARE, LORELEI_MYSTIA, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294587217267654709/tokiko-stare-0001.png',
).with_action(
    ACTION_TAG_STARE, TOKIKO, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294587227476725830/flandre-stare-0016.png',
).with_action(
    ACTION_TAG_STARE, SCARLET_FLANDRE, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294587235017949194/remilia-stare-0002.png',
).with_action(
    ACTION_TAG_STARE, SCARLET_REMILIA, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294587241594617877/okuu-stare-0001.png',
).with_action(
    ACTION_TAG_STARE, REIUJI_UTSUHO, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294587245256245288/kogasa-nue-pat-0000.png',
).with_action(
    ACTION_TAG_PAT, HOUJUU_NUE, TATARA_KOGASA,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294587249735766078/nue-stare-0045.png',
).with_action(
    ACTION_TAG_STARE, HOUJUU_NUE, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294587255306059787/yachie-stare-0001.png',
).with_action(
    ACTION_TAG_STARE, KICCHOU_YACHIE, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294587261106651169/aya-stare-0001.png',
).with_action(
    ACTION_TAG_STARE, SHAMEIMARU_AYA, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294587264080547911/rumia-stare-0005.png',
).with_action(
    ACTION_TAG_STARE, RUMIA, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294587269654773790/shizuha-stare-0000.png',
).with_action(
    ACTION_TAG_STARE, AKI_SHIZUHA, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294587274272444416/seija-stare-0007.png',
).with_action(
    ACTION_TAG_STARE, KIJIN_SEIJA, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294587279511388160/shizuha-stare-0001.png',
).with_action(
    ACTION_TAG_STARE, AKI_SHIZUHA, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294587284439437382/kogasa-stare-0010.png',
).with_action(
    ACTION_TAG_STARE, TATARA_KOGASA, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294587294539452456/yuuka-stare-0002.png',
).with_action(
    ACTION_TAG_STARE, KAZAMI_YUUKA, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294587298842673202/koishi-stare-0012.png',
).with_action(
    ACTION_TAG_STARE, KOMEIJI_KOISHI, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294587302357630998/remilia-stare-0005.png',
).with_action(
    ACTION_TAG_STARE, SCARLET_REMILIA, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294587307868950528/sanae-stare-0002.png',
).with_action(
    ACTION_TAG_STARE, KOCHIYA_SANAE, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294587310322749440/mayumi-stare-0001.png',
).with_action(
    ACTION_TAG_STARE, JOUTOUGUU_MAYUMI, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294587314026319872/keine-mokou-stare-0002.png',
).with_actions(
    (ACTION_TAG_STARE, KAMISHIRASAWA_KEINE, None),
    (ACTION_TAG_STARE, FUJIWARA_NO_MOKOU, None),
).with_creator(
    'itomugi-kun',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294587318728003645/nue-stare-0028.png',
).with_action(
    ACTION_TAG_STARE, HOUJUU_NUE, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294587324088455240/nue-stare-0022.png',
).with_action(
    ACTION_TAG_STARE, HOUJUU_NUE, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294587329658490931/doremy-stare-0002.png',
).with_action(
    ACTION_TAG_STARE, DOREMY_SWEET, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294587333630361641/patchouli-stare-0000.png',
).with_action(
    ACTION_TAG_STARE, PATCHOULI_KNOWLEDGE, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294587337883521095/chiruno-stare-0002.png',
).with_action(
    ACTION_TAG_STARE, CHIRUNO, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294587342006517770/mokou-stare-0006.png',
).with_action(
    ACTION_TAG_STARE, FUJIWARA_NO_MOKOU, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294587346133712987/seija-stare-0011.png',
).with_action(
    ACTION_TAG_STARE, KIJIN_SEIJA, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294587349925363803/sakuya-stare-0005.png',
).with_action(
    ACTION_TAG_STARE, IZAYOI_SAKUYA, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294587354572656660/mystia-stare-0005.png',
).with_action(
    ACTION_TAG_STARE, LORELEI_MYSTIA, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294587365133783050/sakuya-stare-0004.png',
).with_action(
    ACTION_TAG_STARE, IZAYOI_SAKUYA, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294587371928686624/kokoro-stare-0001.png',
).with_action(
    ACTION_TAG_STARE, HATA_NO_KOKORO, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294587377645387888/koishi-satori-stare-0000.png',
).with_actions(
    (ACTION_TAG_STARE, KOMEIJI_KOISHI, None),
    (ACTION_TAG_STARE, KOMEIJI_SATORI, None),
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294587384964317266/okina-stare-0002.png',
).with_action(
    ACTION_TAG_STARE, MATARA_OKINA, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294587389054029856/nue-stare-0039.png',
).with_action(
    ACTION_TAG_STARE, HOUJUU_NUE, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294587392526778368/koishi-stare-0007.png',
).with_action(
    ACTION_TAG_STARE, KOMEIJI_KOISHI, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294587399577407551/flandre-stare-0013.png',
).with_action(
    ACTION_TAG_STARE, SCARLET_FLANDRE, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294587403708923924/flandre-stare-0018.png',
).with_action(
    ACTION_TAG_STARE, SCARLET_FLANDRE, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294587409068986388/junko-stare-0001.png',
).with_action(
    ACTION_TAG_STARE, JUNKO, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294587413808545842/kogasa-stare-0006.png',
).with_action(
    ACTION_TAG_STARE, TATARA_KOGASA, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294595221283278930/mishagujo-suwako-stare-0000.png',
).with_action(
    ACTION_TAG_STARE, MORIYA_SUWAKO, None,
).with_character(
    MISHAGUJI,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294587425833746442/patchouli-stare-0001.png',
).with_action(
    ACTION_TAG_STARE, PATCHOULI_KNOWLEDGE, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294587431093276754/lyrica-stare-0000.png',
).with_action(
    ACTION_TAG_STARE, PRISMRIVER_LYRICA, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294587438299353149/yuuma-stare-0002.png',
).with_action(
    ACTION_TAG_STARE, TOUTETSU_YUUMA, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294587443760336896/nue-stare-0016.png',
).with_action(
    ACTION_TAG_STARE, HOUJUU_NUE, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294587448323473509/nue-stare-0042.png',
).with_action(
    ACTION_TAG_STARE, HOUJUU_NUE, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294587452358660177/junko-stare-0004.png',
).with_action(
    ACTION_TAG_STARE, JUNKO, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294587459019079680/murasa-stare-0000.png',
).with_action(
    ACTION_TAG_STARE, MURASA_MINAMITSU, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294587468963774536/hecatia-stare-0002.png',
).with_action(
    ACTION_TAG_STARE, HECATIA_LAPISLAZULI, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294587473917378641/sagume-stare-0001.png',
).with_action(
    ACTION_TAG_STARE, KISHIN_SAGUME, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294587476815515680/flandre-stare-0014.png',
).with_action(
    ACTION_TAG_STARE, SCARLET_FLANDRE, None,
).with_creator(
    'ichirugi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294946959898968075/sakuya-stare-0007.png',
).with_action(
    ACTION_TAG_STARE, IZAYOI_SAKUYA, None,
).with_creator(
    'kisamu (ksmz)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294946964068368384/koishi-happy-0000.png',
).with_action(
    ACTION_TAG_HAPPY, KOMEIJI_KOISHI, None,
).with_creator(
    'kisamu (ksmz)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294946966513385472/nue-stare-0070.png',
).with_action(
    ACTION_TAG_STARE, HOUJUU_NUE, None,
).with_creator(
    'kisamu (ksmz)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294946969982074880/nue-stare-0062.png',
).with_action(
    ACTION_TAG_STARE, HOUJUU_NUE, None,
).with_creator(
    'kisamu (ksmz)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294946973312614411/nue-stare-0071.png',
).with_action(
    ACTION_TAG_STARE, HOUJUU_NUE, None,
).with_creator(
    'kisamu (ksmz)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294946976965591091/kyouko-happy-0000.png',
).with_action(
    ACTION_TAG_HAPPY, KASODANI_KYOUKO, None,
).with_creator(
    'kisamu (ksmz)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294946981629919292/kogasa-nue-hug-0002.png',
).with_actions(
    (ACTION_TAG_HUG, HOUJUU_NUE, TATARA_KOGASA),
    (ACTION_TAG_HUG, TATARA_KOGASA, HOUJUU_NUE),
).with_creator(
    'kisamu (ksmz)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294946985639415879/kosuzu-stare-0000.png',
).with_action(
    ACTION_TAG_STARE, MOTOORI_KOSUZU, None,
).with_creator(
    'kisamu (ksmz)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294946990760787998/youmu-stare-0003.png',
).with_action(
    ACTION_TAG_STARE, KONPAKU_YOUMU, None,
).with_creator(
    'kisamu (ksmz)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294946993075916882/satori-stare-0005.png',
).with_action(
    ACTION_TAG_STARE, KOMEIJI_SATORI, None,
).with_creator(
    'kisamu (ksmz)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294946998692352021/seija-stare-0025.png',
).with_action(
    ACTION_TAG_STARE, KIJIN_SEIJA, None,
).with_creator(
    'kisamu (ksmz)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294947004128034886/nue-stare-0072.png',
).with_action(
    ACTION_TAG_STARE, HOUJUU_NUE, None,
).with_creator(
    'kisamu (ksmz)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294947007869353984/nue-feed_self-stare-0000.png',
).with_action(
    ACTION_TAG_FEED_SELF, HOUJUU_NUE, HOUJUU_NUE,
).with_creator(
    'kisamu (ksmz)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294947011266609192/koishi-stare-0021.png',
).with_action(
    ACTION_TAG_STARE, KOMEIJI_KOISHI, None,
).with_creator(
    'kisamu (ksmz)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294947017075851348/nue-stare-0059.png',
).with_action(
    ACTION_TAG_STARE, HOUJUU_NUE, None,
).with_creator(
    'kisamu (ksmz)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294947020578230332/nue-cry-0000.png',
).with_action(
    ACTION_TAG_CRY, HOUJUU_NUE, None,
).with_creator(
    'kisamu (ksmz)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294947024579334235/kutaka-stare-0004.png',
).with_action(
    ACTION_TAG_STARE, NIWATARI_KUTAKA, None,
).with_creator(
    'kisamu (ksmz)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294947028157333556/nue-stare-0068.png',
).with_action(
    ACTION_TAG_STARE, HOUJUU_NUE, None,
).with_creator(
    'kisamu (ksmz)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294947031890001991/suika-feed_self-stare-0000.png',
).with_actions(
    (ACTION_TAG_STARE, IBUKI_SUIKA, None),
    (ACTION_TAG_FEED_SELF, IBUKI_SUIKA, IBUKI_SUIKA),
).with_creator(
    'kisamu (ksmz)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294947036235567165/seija-stare-0024.png',
).with_action(
    ACTION_TAG_STARE, KIJIN_SEIJA, None,
).with_creator(
    'kisamu (ksmz)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294947041063207032/sanae-stare-0003.png',
).with_action(
    ACTION_TAG_STARE, KOCHIYA_SANAE, None,
).with_creator(
    'kisamu (ksmz)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294947044472913973/nue-wink-0000.png',
).with_action(
    ACTION_TAG_WINK, HOUJUU_NUE, None,
).with_creator(
    'kisamu (ksmz)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294947047245348906/alice-stare-0001.png',
).with_action(
    ACTION_TAG_STARE, MARGATROID_ALICE, None,
).with_creator(
    'kisamu (ksmz)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294947051821338644/nue-stare-0061.png',
).with_action(
    ACTION_TAG_STARE, HOUJUU_NUE, None,
).with_creator(
    'kisamu (ksmz)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294947057039315025/nue-stare-0057.png',
).with_action(
    ACTION_TAG_STARE, HOUJUU_NUE, None,
).with_creator(
    'kisamu (ksmz)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294947060101025874/nue-stare-0073.png',
).with_action(
    ACTION_TAG_STARE, HOUJUU_NUE, None,
).with_creator(
    'kisamu (ksmz)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294947062290448384/kogasa-wave-0000.png',
).with_action(
    ACTION_TAG_WAVE, TATARA_KOGASA, None,
).with_creator(
    'kisamu (ksmz)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294947066509922366/nue-happy-0001.png',
).with_action(
    ACTION_TAG_HAPPY, HOUJUU_NUE, None,
).with_creator(
    'kisamu (ksmz)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294947070280470608/nue-happy-0000.png',
).with_action(
    ACTION_TAG_HAPPY, HOUJUU_NUE, None,
).with_creator(
    'kisamu (ksmz)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294947074080637018/seija-stare-0026.png',
).with_action(
    ACTION_TAG_STARE, KIJIN_SEIJA, None,
).with_creator(
    'kisamu (ksmz)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294947078367084597/marisa-stare-0003.png',
).with_action(
    ACTION_TAG_STARE, KIRISAME_MARISA, None,
).with_creator(
    'kisamu (ksmz)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294947081986899968/nue-stare-0064.png',
).with_action(
    ACTION_TAG_STARE, HOUJUU_NUE, None,
).with_creator(
    'kisamu (ksmz)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294947084566396958/nue-stare-0067.png',
).with_action(
    ACTION_TAG_STARE, HOUJUU_NUE, None,
).with_creator(
    'kisamu (ksmz)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294947089758814271/flandre-stare-0019.png',
).with_action(
    ACTION_TAG_STARE, SCARLET_FLANDRE, None,
).with_creator(
    'kisamu (ksmz)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294947093810647114/nue-stare-0063.png',
).with_action(
    ACTION_TAG_STARE, HOUJUU_NUE, None,
).with_creator(
    'kisamu (ksmz)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294947099414237184/flandre-stare-0020.png',
).with_action(
    ACTION_TAG_STARE, SCARLET_FLANDRE, None,
).with_creator(
    'kisamu (ksmz)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294947103663198268/tmiko-stare-0000.png',
).with_action(
    ACTION_TAG_STARE, TOYOSATOMIMI_NO_MIKO, None,
).with_creator(
    'kisamu (ksmz)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294947107530084454/sanae-stare-0004.png',
).with_action(
    ACTION_TAG_STARE, KOCHIYA_SANAE, None,
).with_creator(
    'kisamu (ksmz)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294947109740740682/koishi-stare-0019.png',
).with_action(
    ACTION_TAG_STARE, KOMEIJI_KOISHI, None,
).with_creator(
    'kisamu (ksmz)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294947114274787358/koishi-stare-0020.png',
).with_action(
    ACTION_TAG_STARE, KOMEIJI_KOISHI, None,
).with_creator(
    'kisamu (ksmz)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294947119777583134/nue-stare-0069.png',
).with_action(
    ACTION_TAG_STARE, HOUJUU_NUE, None,
).with_creator(
    'kisamu (ksmz)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294947124039127083/iku-stare-0000.png',
).with_action(
    ACTION_TAG_STARE, NAGAE_IKU, None,
).with_creator(
    'kisamu (ksmz)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294947128204070972/kogasa-stare-0013.png',
).with_action(
    ACTION_TAG_STARE, TATARA_KOGASA, None,
).with_creator(
    'kisamu (ksmz)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294947131681148991/nue-stare-0060.png',
).with_action(
    ACTION_TAG_STARE, HOUJUU_NUE, None,
).with_creator(
    'kisamu (ksmz)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294947134722019358/flandre-stare-0021.png',
).with_action(
    ACTION_TAG_STARE, SCARLET_FLANDRE, None,
).with_creator(
    'kisamu (ksmz)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294947140681994280/sekibanki-stare-0003.png',
).with_action(
    ACTION_TAG_STARE, SEKIBANKI, None,
).with_creator(
    'kisamu (ksmz)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294947143534252123/kogasa-nue-hug-0003.png',
).with_actions(
    (ACTION_TAG_HUG, HOUJUU_NUE, TATARA_KOGASA),
    (ACTION_TAG_HUG, TATARA_KOGASA, HOUJUU_NUE),
).with_creator(
    'kisamu (ksmz)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294947149120933949/marisa-stare-0004.png',
).with_action(
    ACTION_TAG_STARE, KIRISAME_MARISA, None,
).with_creator(
    'kisamu (ksmz)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294947152379772938/remilia-stare-0008.png',
).with_action(
    ACTION_TAG_STARE, SCARLET_REMILIA, None,
).with_creator(
    'kisamu (ksmz)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294947155492081706/chiruno-stare-0005.png',
).with_action(
    ACTION_TAG_STARE, CHIRUNO, None,
).with_creator(
    'kisamu (ksmz)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1294947160181440512/nue-stare-0065.png',
).with_action(
    ACTION_TAG_STARE, HOUJUU_NUE, None,
).with_creator(
    'kisamu (ksmz)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1300132474818662450/chen-ran-hug-0003.png',
).with_action(
    ACTION_TAG_HUG, YAKUMO_RAN, CHEN,
).with_creator(
    'mizuga',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1300133856183193741/mokou-mystia-hug-0000.png',
).with_actions(
    (ACTION_TAG_HUG, FUJIWARA_NO_MOKOU, LORELEI_MYSTIA),
    (ACTION_TAG_HUG, LORELEI_MYSTIA, FUJIWARA_NO_MOKOU),
).with_creator(
    'makoto jon',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1300133857932345405/alice-mokou-hug-0000.png',
).with_actions(
    (ACTION_TAG_HUG, FUJIWARA_NO_MOKOU, MARGATROID_ALICE),
    (ACTION_TAG_HUG, MARGATROID_ALICE, FUJIWARA_NO_MOKOU),
).with_creator(
    'makoto jon',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1300188758439624839/koakuma-stare-0002.png',
).with_action(
    ACTION_TAG_STARE, KOAKUMA, None,
).with_creator(
    'risui (suzu rks)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1300188764492140564/sakuya-stare-0008.png',
).with_action(
    ACTION_TAG_STARE, IZAYOI_SAKUYA, None,
).with_creator(
    'risui (suzu rks)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1300188770330480711/kokoro-stare-0002.png',
).with_action(
    ACTION_TAG_STARE, HATA_NO_KOKORO, None,
).with_creator(
    'risui (suzu rks)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1300188773908349028/alice-stare-0002.png',
).with_action(
    ACTION_TAG_STARE, MARGATROID_ALICE, None,
).with_creator(
    'risui (suzu rks)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1300188775619493999/sekibanki-stare-0004.png',
).with_action(
    ACTION_TAG_STARE, SEKIBANKI, None,
).with_creator(
    'risui (suzu rks)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1300188785950199879/meiling-stare-0000.png',
).with_action(
    ACTION_TAG_STARE, HONG_MEILING, None,
).with_creator(
    'risui (suzu rks)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1300188791071440896/meiling-stare-0002.png',
).with_action(
    ACTION_TAG_STARE, HONG_MEILING, None,
).with_creator(
    'risui (suzu rks)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1300188797136535552/meiling-stare-0001.png',
).with_action(
    ACTION_TAG_STARE, HONG_MEILING, None,
).with_creator(
    'risui (suzu rks)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1300188805210574889/meiling-sakuya-hug-0002.png',
).with_actions(
    (ACTION_TAG_HUG, HONG_MEILING, IZAYOI_SAKUYA),
    (ACTION_TAG_HUG, IZAYOI_SAKUYA, HONG_MEILING),
).with_creator(
    'risui (suzu rks)',
).with_editor(
    'HuyaneMatsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1300188810428158032/tmiko-stare-0001.png',
).with_action(
    ACTION_TAG_STARE, TOYOSATOMIMI_NO_MIKO, None,
).with_creator(
    'risui (suzu rks)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1300188814777778316/nue-stare-0058.png',
).with_action(
    ACTION_TAG_STARE, HOUJUU_NUE, None,
).with_creator(
    'risui (suzu rks)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1300188818263117865/marisa-stare-0005.png',
).with_action(
    ACTION_TAG_STARE, KIRISAME_MARISA, None,
).with_creator(
    'risui (suzu rks)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1300188820393824397/nitori-stare-0000.png',
).with_action(
    ACTION_TAG_STARE, KAWASHIRO_NITORI, None,
).with_creator(
    'risui (suzu rks)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1300188833056292864/hina-stare-0005.png',
).with_action(
    ACTION_TAG_STARE, KAGIYAMA_HINA, None,
).with_creator(
    'risui (suzu rks)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1300188836638490756/miyoi-stare-0000.png',
).with_action(
    ACTION_TAG_STARE, OKUNODA_MIYOI, None,
).with_creator(
    'risui (suzu rks)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1300188841902211102/koakuma-stare-0001.png',
).with_action(
    ACTION_TAG_STARE, KOAKUMA, None,
).with_creator(
    'risui (suzu rks)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1300188852576583742/hina-stare-0006.png',
).with_action(
    ACTION_TAG_STARE, KAGIYAMA_HINA, None,
).with_creator(
    'risui (suzu rks)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1300188860176666824/alice-stare-0003.png',
).with_action(
    ACTION_TAG_STARE, MARGATROID_ALICE, None,
).with_creator(
    'risui (suzu rks)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1300188864647921734/meiling-stare-0003.png',
).with_action(
    ACTION_TAG_STARE, HONG_MEILING, None,
).with_creator(
    'risui (suzu rks)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1300188868410216549/meiling-sakuya-hug-0003.png',
).with_action(
    ACTION_TAG_HUG, HONG_MEILING, IZAYOI_SAKUYA,
).with_creator(
    'risui (suzu rks)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1300188872843591751/marisa-stare-0006.png',
).with_action(
    ACTION_TAG_STARE, KIRISAME_MARISA, None,
).with_creator(
    'risui (suzu rks)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1300188879827243048/flandre-remilia-hug-0006.png',
).with_actions(
    (ACTION_TAG_HUG, SCARLET_FLANDRE, SCARLET_REMILIA),
    (ACTION_TAG_HUG, SCARLET_REMILIA, SCARLET_FLANDRE),
).with_creator(
    'risui (suzu rks)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1300188886659629178/komachi-eiki-hug-0000.png',
).with_action(
    ACTION_TAG_HUG, ONOZUKA_KOMACHI, SHIKI_EIKI_YAMAXANADU,
).with_creator(
    'risui (suzu rks)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1300188891508375693/sanae-happy-0000.png',
).with_action(
    ACTION_TAG_HAPPY, KOCHIYA_SANAE, None,
).with_creator(
    'risui (suzu rks)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1300188906221736017/kagerou-stare-0004.png',
).with_action(
    ACTION_TAG_STARE, IMAIZUMI_KAGEROU, None,
).with_creator(
    'risui (suzu rks)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1300188910286147668/youmu-stare-0004.png',
).with_action(
    ACTION_TAG_STARE, KONPAKU_YOUMU, None,
).with_creator(
    'risui (suzu rks)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1300188916376277096/saki-stare-0001.png',
).with_action(
    ACTION_TAG_STARE, KUROKOMA_SAKI, None,
).with_creator(
    'risui (suzu rks)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1308902156396527719/tsukasa-kon-0023.png',
).with_action(
    ACTION_TAG_KON, KUDAMAKI_TSUKASA, None,
).with_creator(
    'kamenozoki momomo',
).with_editor(
    'HuyaneMatsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1308902162184798238/meira-reimu-hug-0000.png',
).with_action(
    ACTION_TAG_HUG, HAKUREI_REIMU, MEIRA,
).with_creator(
    'kamenozoki momomo',
).with_editor(
    'HuyaneMatsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1308903288044912750/marisa-rinnosuke-hug-0000.png',
).with_action(
    ACTION_TAG_HUG, KIRISAME_MARISA, MORICHIKA_RINNOSUKE,
).with_creator(
    'akasata',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1308903292251668602/meira-reimu-hug-0001.png',
).with_action(
    ACTION_TAG_HUG, HAKUREI_REIMU, MEIRA,
).with_creator(
    'akasata',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1308916621750042755/aya-reimu-cosplay-0000.png',
).with_actions(
    (ACTION_TAG_COSPLAY, HAKUREI_REIMU, SHAMEIMARU_AYA),
    (ACTION_TAG_COSPLAY, HAKUREI_REIMU, SHAMEIMARU_AYA),
).with_creator(
    'chilwell seele',
).with_editor(
    'HuyaneMatsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1308916626506383432/aya-reimu-hug-0002.png',
).with_action(
    ACTION_TAG_HUG, HAKUREI_REIMU, SHAMEIMARU_AYA,
).with_creator(
    'chilwell seele',
).with_editor(
    'HuyaneMatsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1308916632827199569/aya-reimu-hug-0005.png',
).with_action(
    ACTION_TAG_HUG, SHAMEIMARU_AYA, HAKUREI_REIMU,
).with_creator(
    'chilwell seele',
).with_editor(
    'HuyaneMatsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1308916637826547762/aya-reimu-kiss-0003.png',
).with_action(
    ACTION_TAG_KISS, HAKUREI_REIMU, SHAMEIMARU_AYA,
).with_creator(
    'chilwell seele',
).with_editor(
    'HuyaneMatsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1308916641840762910/aya-reimu-hug-0004.png',
).with_actions(
    (ACTION_TAG_HUG, HAKUREI_REIMU, SHAMEIMARU_AYA),
    (ACTION_TAG_HUG, SHAMEIMARU_AYA, HAKUREI_REIMU),
).with_creator(
    'chilwell seele',
).with_editor(
    'HuyaneMatsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1308916645791666268/aya-reimu-hug-0006.png',
).with_action(
    ACTION_TAG_HUG, HAKUREI_REIMU, SHAMEIMARU_AYA,
).with_creator(
    'chilwell seele',
).with_editor(
    'HuyaneMatsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1308916651420549120/aya-reimu-hug-0003.png',
).with_actions(
    (ACTION_TAG_HUG, HAKUREI_REIMU, SHAMEIMARU_AYA),
    (ACTION_TAG_HUG, SHAMEIMARU_AYA, HAKUREI_REIMU),
).with_creator(
    'chilwell seele',
).with_editor(
    'HuyaneMatsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1308916656042676316/aya-reimu-lap_sleep-0002.png',
).with_action(
    ACTION_TAG_LAP_SLEEP, HAKUREI_REIMU, SHAMEIMARU_AYA,
).with_creator(
    'chilwell seele',
).with_editor(
    'HuyaneMatsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1308916666834485361/eiki-komachi-hug-0001.png',
).with_action(
    ACTION_TAG_HUG, SHIKI_EIKI_YAMAXANADU, ONOZUKA_KOMACHI,
).with_creator(
    'chilwell seele',
).with_editor(
    'HuyaneMatsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1308916673096712192/aya-reimu-lap_sleep-0001.png',
).with_action(
    ACTION_TAG_LAP_SLEEP, HAKUREI_REIMU, SHAMEIMARU_AYA,
).with_creator(
    'chilwell seele',
).with_editor(
    'HuyaneMatsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1308916678469488731/aya-reimu-kiss-0002.png',
).with_actions(
    (ACTION_TAG_KISS, HAKUREI_REIMU, SHAMEIMARU_AYA),
    (ACTION_TAG_KISS, SHAMEIMARU_AYA, HAKUREI_REIMU),
).with_creator(
    'chilwell seele',
).with_editor(
    'HuyaneMatsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1417556539048198307/flandre-koishi-handhold-0004.png',
).with_actions(
    (ACTION_TAG_HANDHOLD, SCARLET_FLANDRE, KOMEIJI_KOISHI),
    (ACTION_TAG_HANDHOLD, KOMEIJI_KOISHI, SCARLET_FLANDRE),
).with_creator(
    'shelbop',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1417559666644488193/marisa-yuuka-carry-0000.png',
).with_action(
    ACTION_TAG_CARRY, KAZAMI_YUUKA, KIRISAME_MARISA,
).with_creator(
    'shino (mijinko)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1417559672252272803/flandre-koishi-marisa-handhold-0000.png',
).with_action(
    ACTION_TAG_HANDHOLD, KOMEIJI_KOISHI, KIRISAME_MARISA,
).with_character(
    SCARLET_FLANDRE,
).with_creator(
    'shino (mijinko)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1417559677239169114/kanako-reimu-murder-0000.png',
).with_action(
    ACTION_TAG_MURDER, YASAKA_KANAKO, HAKUREI_REIMU,
).with_creator(
    'shino (mijinko)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1417559680334696458/koishi-satori-hug-0011.png',
).with_action(
    ACTION_TAG_HUG, KOMEIJI_SATORI, KOMEIJI_KOISHI,
).with_creator(
    'shino (mijinko)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1417559685036511452/kanako-sanae-suwako-hug-0000.png',
).with_actions(
    (ACTION_TAG_HUG, MORIYA_SUWAKO, KOCHIYA_SANAE),
    (ACTION_TAG_HUG, YASAKA_KANAKO, KOCHIYA_SANAE),
).with_creator(
    'shino (mijinko)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1417560764109033512/koishi-satori-hug-0012.png',
).with_action(
    ACTION_TAG_HUG, KOMEIJI_KOISHI, KOMEIJI_SATORI,
).with_creator(
    'shino (mijinko)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1417562845091991795/flandre-koishi-handhold-0005.png',
).with_actions(
    (ACTION_TAG_HANDHOLD, SCARLET_FLANDRE, KOMEIJI_KOISHI),
    (ACTION_TAG_HANDHOLD, KOMEIJI_KOISHI, SCARLET_FLANDRE),
).with_creator(
    'nawo (peace)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1417562848833310780/meiling-remilia-lap_sleep-0000.png',
).with_action(
    ACTION_TAG_LAP_SLEEP, HONG_MEILING, SCARLET_REMILIA,
).with_creator(
    'nawo (peace)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1417562854537695273/meiling-sakuya-lap_sleep-0000.png',
).with_action(
    ACTION_TAG_LAP_SLEEP, HONG_MEILING, IZAYOI_SAKUYA,
).with_creator(
    'nawo (peace)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1417565348257071104/flandre-remilia-hug-0007.png',
).with_actions(
    (ACTION_TAG_HUG, SCARLET_FLANDRE, SCARLET_REMILIA),
    (ACTION_TAG_HUG, SCARLET_REMILIA, SCARLET_FLANDRE),
).with_creator(
    'Kurose Itsuka (黒瀬いつか)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1417565355639050402/keine-mokou-hug-0007.png',
).with_action(
    ACTION_TAG_HUG, KAMISHIRASAWA_KEINE, FUJIWARA_NO_MOKOU,
).with_creator(
    'Kurose Itsuka (黒瀬いつか)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1417565360055521370/koishi-satori-hug-0013.png',
).with_action(
    ACTION_TAG_HUG, KOMEIJI_KOISHI, KOMEIJI_SATORI,
).with_creator(
    'Kurose Itsuka (黒瀬いつか)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1417565365113979071/reimu-yukari-handhold-0000.png',
).with_actions(
    (ACTION_TAG_HANDHOLD, HAKUREI_REIMU, YAKUMO_YUKARI),
    (ACTION_TAG_HANDHOLD, YAKUMO_YUKARI, HAKUREI_REIMU),
).with_creator(
    'Kurose Itsuka (黒瀬いつか)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1417565369471733861/flandre-koishi-handhold-0006.png',
).with_actions(
    (ACTION_TAG_HANDHOLD, SCARLET_FLANDRE, KOMEIJI_KOISHI),
    (ACTION_TAG_HANDHOLD, KOMEIJI_KOISHI, SCARLET_FLANDRE),
).with_creator(
    'Kurose Itsuka (黒瀬いつか)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1417751114933211187/chen-ran-pat-0004.png',
).with_action(
    ACTION_TAG_PAT, YAKUMO_RAN, CHEN,
).with_creator(
    'Asa (麻)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1417751120943775817/flandre-remilia-hug-0008.png',
).with_actions(
    (ACTION_TAG_HUG, SCARLET_FLANDRE, SCARLET_REMILIA),
    (ACTION_TAG_HUG, SCARLET_REMILIA, SCARLET_FLANDRE),
).with_creator(
    'Asa (麻)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1417751124915781652/flandre-koishi-handhold-0007.png',
).with_actions(
    (ACTION_TAG_HANDHOLD, KOMEIJI_KOISHI, SCARLET_FLANDRE),
    (ACTION_TAG_HANDHOLD, SCARLET_FLANDRE, KOMEIJI_KOISHI),
).with_creator(
    'Asa (麻)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1417751771517943901/flandre-koishi-handhold-0008.png',
).with_actions(
    (ACTION_TAG_HANDHOLD, KOMEIJI_KOISHI, SCARLET_FLANDRE),
    (ACTION_TAG_HANDHOLD, SCARLET_FLANDRE, KOMEIJI_KOISHI),
).with_creator(
    'Zetz',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1417754577997922335/alice-marisa-handhold-0000.png',
).with_actions(
    (ACTION_TAG_HANDHOLD, KIRISAME_MARISA, MARGATROID_ALICE),
    (ACTION_TAG_HANDHOLD, MARGATROID_ALICE, KIRISAME_MARISA),
).with_creator(
    'Tsuno no hito (角人)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1417754583823941632/alice-marisa-handhold-0001.png',
).with_actions(
    (ACTION_TAG_HANDHOLD, KIRISAME_MARISA, MARGATROID_ALICE),
    (ACTION_TAG_HANDHOLD, MARGATROID_ALICE, KIRISAME_MARISA),
).with_creator(
    'Tsuno no hito (角人)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1417754590153277440/alice-reimu-hug-0000.png',
).with_action(
    ACTION_TAG_HUG, HAKUREI_REIMU, MARGATROID_ALICE,
).with_creator(
    'Tsuno no hito (角人)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1417754597023420538/alice-marisa-hug-0006.png',
).with_action(
    ACTION_TAG_HUG, KIRISAME_MARISA, MARGATROID_ALICE,
).with_creator(
    'Tsuno no hito (角人)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1417754600722927658/alice-marisa-hug-0009.png',
).with_action(
    ACTION_TAG_HUG, KIRISAME_MARISA, MARGATROID_ALICE,
).with_creator(
    'Tsuno no hito (角人)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1417754603276992605/alice-koakuma-handhold-0000.png',
).with_actions(
    (ACTION_TAG_HANDHOLD, KOAKUMA, MARGATROID_ALICE),
    (ACTION_TAG_HANDHOLD, MARGATROID_ALICE, KOAKUMA),
).with_creator(
    'Tsuno no hito (角人)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1417754605575471215/alice-marisa-hug-0008.png',
).with_action(
    ACTION_TAG_HUG, KIRISAME_MARISA, MARGATROID_ALICE,
).with_creator(
    'Tsuno no hito (角人)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1417754609790746654/alice-reimu-carry-0000.png',
).with_action(
    ACTION_TAG_CARRY, HAKUREI_REIMU, MARGATROID_ALICE,
).with_creator(
    'Tsuno no hito (角人)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1417754613712424960/alice-marisa-kiss-0005.png',
).with_action(
    ACTION_TAG_KISS, KIRISAME_MARISA, MARGATROID_ALICE,
).with_creator(
    'Tsuno no hito (角人)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1417754617621778503/alice-marisa-hug-0007.png',
).with_actions(
    (ACTION_TAG_HUG, KIRISAME_MARISA, MARGATROID_ALICE),
    (ACTION_TAG_HUG, MARGATROID_ALICE, KIRISAME_MARISA),
).with_creator(
    'Tsuno no hito (角人)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1417754619848691873/flandre-koishi-handhold-0009.png',
).with_actions(
    (ACTION_TAG_HANDHOLD, KOMEIJI_KOISHI, SCARLET_FLANDRE),
    (ACTION_TAG_HANDHOLD, SCARLET_FLANDRE, KOMEIJI_KOISHI),
).with_creator(
    'Tsuno no hito (角人)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1417754627285192774/alice-hina-handhold-0000.png',
).with_actions(
    (ACTION_TAG_HANDHOLD, KAGIYAMA_HINA, MARGATROID_ALICE),
    (ACTION_TAG_HANDHOLD, MARGATROID_ALICE, KAGIYAMA_HINA),
).with_creator(
    'Tsuno no hito (角人)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1417754632188330125/alice-mokou-handhold-0000.png',
).with_action(
    ACTION_TAG_HANDHOLD, FUJIWARA_NO_MOKOU, MARGATROID_ALICE
).with_creator(
    'Tsuno no hito (角人)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1417756734755307540/alice-flandre-hug-0000.png',
).with_actions(
    (ACTION_TAG_HUG, MARGATROID_ALICE, SCARLET_FLANDRE),
    (ACTION_TAG_HUG, SCARLET_FLANDRE, MARGATROID_ALICE),
).with_creator(
    'Mizuki (みずき)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1417756738718928977/flandre-remilia-carry-0000.png',
).with_action(
    ACTION_TAG_CARRY, SCARLET_FLANDRE, SCARLET_REMILIA,
).with_creator(
    'Mizuki (みずき)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1417756750542536785/flandre-koishi-handhold-0010.png',
).with_actions(
    (ACTION_TAG_HANDHOLD, KOMEIJI_KOISHI, SCARLET_FLANDRE),
    (ACTION_TAG_HANDHOLD, SCARLET_FLANDRE, KOMEIJI_KOISHI),
).with_creator(
    'Mizuki (みずき)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1417757567568052305/flandre-koishi-handhold-0011.png',
).with_actions(
    (ACTION_TAG_HANDHOLD, KOMEIJI_KOISHI, SCARLET_FLANDRE),
    (ACTION_TAG_HANDHOLD, SCARLET_FLANDRE, KOMEIJI_KOISHI),
).with_creator(
    'Shiran (シラン)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1417758150718918759/flandre-koishi-handhold-0012.png',
).with_actions(
    (ACTION_TAG_HANDHOLD, KOMEIJI_KOISHI, SCARLET_FLANDRE),
    (ACTION_TAG_HANDHOLD, SCARLET_FLANDRE, KOMEIJI_KOISHI),
).with_creator(
    'Robegya (ロベギャ)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1417758713636327464/flandre-koishi-handhold-0013.png',
).with_actions(
    (ACTION_TAG_HANDHOLD, KOMEIJI_KOISHI, SCARLET_FLANDRE),
    (ACTION_TAG_HANDHOLD, SCARLET_FLANDRE, KOMEIJI_KOISHI),
).with_creator(
    'Soku',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1417759473841213550/flandre-koishi-handhold-0014.png',
).with_actions(
    (ACTION_TAG_HANDHOLD, KOMEIJI_KOISHI, SCARLET_FLANDRE),
    (ACTION_TAG_HANDHOLD, SCARLET_FLANDRE, KOMEIJI_KOISHI),
).with_creator(
    'Tsuyuji Shigure (露路しぐれ)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1417760545288880158/koishi-kokoro-handhold-0001.png',
).with_action(
    ACTION_TAG_HANDHOLD, KOMEIJI_KOISHI, HATA_NO_KOKORO,
).with_creator(
    'sameduma',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1417762586052657282/maribel-renko-hug-0008.png',
).with_actions(
    (ACTION_TAG_HUG, HEARN_MARIBEL, USAMI_RENKO),
    (ACTION_TAG_HUG, USAMI_RENKO, HEARN_MARIBEL),
).with_creator(
    'Yurerugin (銀木犀)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1417762591081762846/junko-reisen-handhold-0000.png',
).with_actions(
    (ACTION_TAG_HANDHOLD, JUNKO, REISEN_UDONGEIN_INABA),
    (ACTION_TAG_HANDHOLD, REISEN_UDONGEIN_INABA, JUNKO),
).with_creator(
    'Yurerugin (銀木犀)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1417769611390091343/eirin-reisen-tewi-hug-0000.png',
).with_action(
    ACTION_TAG_HUG, INABA_TEWI, YAGOKORO_EIRIN,
).with_character(
    REISEN_UDONGEIN_INABA,
).with_creator(
    'Unya',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1417769616515534910/keine-kiss-0000.png',
).with_action(
    ACTION_TAG_KISS, KAMISHIRASAWA_KEINE, KAMISHIRASAWA_KEINE,
).with_creator(
    'Unya',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1417769620865290280/minoriki-shizuha-handhold-0000.png',
).with_actions(
    (ACTION_TAG_HANDHOLD, AKI_MINORIKO, AKI_SHIZUHA),
    (ACTION_TAG_HANDHOLD, AKI_SHIZUHA, AKI_MINORIKO),
).with_creator(
    'Unya',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1417769626179207339/momiji-nitori-rawr-0000.png',
).with_actions(
    (ACTION_TAG_RAWR, INUBASHIRI_MOMIJI, None),
    (ACTION_TAG_RAWR, KAWASHIRO_NITORI, None),
).with_creator(
    'Unya',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1417769630465785960/eiki-komachi-handhold-0000.png',
).with_action(
    ACTION_TAG_HANDHOLD, SHIKI_EIKI_YAMAXANADU, ONOZUKA_KOMACHI,
).with_creator(
    'Unya',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1417769637772267581/tenshi-yorohime-kiss-0000.png',
).with_action(
    ACTION_TAG_KISS, HINANAWI_TENSHI, WATATSUKI_NO_YORIHIME,
).with_creator(
    'Unya',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1417769641996058704/hatate-hecatia-kiss-0000.png',
).with_action(
    ACTION_TAG_KISS, HIMEKAIDOU_HATATE, HECATIA_LAPISLAZULI,
).with_creator(
    'Unya',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1417769646299414621/eirin-kaguya-hug-0001.png',
).with_action(
    ACTION_TAG_HUG, HOURAISAN_KAGUYA, YAGOKORO_EIRIN,
).with_creator(
    'Unya',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1417769652876214385/ran-youmu-hug-0000.png',
).with_action(
    ACTION_TAG_HUG, YAKUMO_RAN, KONPAKU_YOUMU,
).with_creator(
    'Unya',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1417769664888574104/yukari-yuyuko-handhold-hug-0000.png',
).with_actions(
    (ACTION_TAG_HANDHOLD, SAIGYOUJI_YUYUKO, YAKUMO_YUKARI),
    (ACTION_TAG_HUG, SAIGYOUJI_YUYUKO, YAKUMO_YUKARI),
).with_creator(
    'Unya',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1417772317312028712/eirin-tewi-kiss-0000.png',
).with_action(
    ACTION_TAG_KISS, INABA_TEWI, YAGOKORO_EIRIN,
).with_creator(
    'Unya',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1417771887014187028/yukari-yuyuko-pocky-0000.png',
).with_actions(
    (ACTION_TAG_POCKY, SAIGYOUJI_YUYUKO, YAKUMO_YUKARI),
    (ACTION_TAG_POCKY, YAKUMO_YUKARI, SAIGYOUJI_YUYUKO),
).with_creator(
    'Unya',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1417769679442808872/sanae-youmu-handhold-0000.png',
).with_actions(
    (ACTION_TAG_HANDHOLD, KOCHIYA_SANAE, KONPAKU_YOUMU),
    (ACTION_TAG_HANDHOLD, KONPAKU_YOUMU, KOCHIYA_SANAE),
).with_creator(
    'Unya',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1417769682877939773/keine-mokou-kiss-0002.png',
).with_action(
    ACTION_TAG_KISS, FUJIWARA_NO_MOKOU, KAMISHIRASAWA_KEINE,
).with_creator(
    'Unya',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1417769687206334484/toyohime-yorihime-handhold-0000.png',
).with_actions(
    (ACTION_TAG_HANDHOLD, WATATSUKI_NO_TOYOHIME, WATATSUKI_NO_YORIHIME),
    (ACTION_TAG_HANDHOLD, WATATSUKI_NO_YORIHIME, WATATSUKI_NO_TOYOHIME),
).with_creator(
    'Unya',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1417769691790704670/keine-carry-0000.png',
).with_action(
    ACTION_TAG_CARRY, KAMISHIRASAWA_KEINE, KAMISHIRASAWA_KEINE,
).with_creator(
    'Unya',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1417769694395367454/eirin-tewi-handhold-0000.png',
).with_action(
    ACTION_TAG_HANDHOLD, INABA_TEWI, YAGOKORO_EIRIN,
).with_creator(
    'Unya',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1417769698807910430/reisen-youmu-hug-0001.png',
).with_action(
    ACTION_TAG_HUG, KONPAKU_YOUMU, REISEN_UDONGEIN_INABA,
).with_creator(
    'Unya',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1417769703497269278/eirin-kaguya-hug-0002.png',
).with_action(
    ACTION_TAG_HUG, HOURAISAN_KAGUYA, YAGOKORO_EIRIN,
).with_creator(
    'Unya',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1417769707842437191/keine-mokou-hug-0008.png',
).with_action(
    ACTION_TAG_HUG, FUJIWARA_NO_MOKOU, KAMISHIRASAWA_KEINE,
).with_creator(
    'Unya',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1417769712959361034/yukari-yuuka-handhold-0000.png',
).with_action(
    ACTION_TAG_HANDHOLD, YAKUMO_YUKARI, KAZAMI_YUUKA,
).with_creator(
    'Unya',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1417769718139326525/kaguya-reisen-kiss-0000.png',
).with_action(
    ACTION_TAG_KISS, REISEN_UDONGEIN_INABA, HOURAISAN_KAGUYA,
).with_creator(
    'Unya',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1417769721780240384/youmu-yuyuko-bully-0000.png',
).with_action(
    ACTION_TAG_BULLY, SAIGYOUJI_YUYUKO, KONPAKU_YOUMU,
).with_creator(
    'Unya',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1417769724678242345/kanako-yuyuko-hug-0000.png',
).with_action(
    ACTION_TAG_HUG, SAIGYOUJI_YUYUKO, YASAKA_KANAKO,
).with_creator(
    'Unya',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1417769734304170074/eirin-medi-hug-0000.png',
).with_action(
    ACTION_TAG_HUG, YAGOKORO_EIRIN, MEDICINE_MELANCHOLY,
).with_creator(
    'Unya',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1417769740100964406/yukari-yuyuko-hug-0000.png',
).with_action(
    ACTION_TAG_HUG, YAKUMO_YUKARI, SAIGYOUJI_YUYUKO,
).with_creator(
    'Unya',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1417769746086236242/yukari-yuyuko-hug-0001.png',
).with_action(
    ACTION_TAG_HUG, SAIGYOUJI_YUYUKO, YAKUMO_YUKARI,
).with_creator(
    'Unya',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1417769751249293432/aya-sanae-hug-0000.png',
).with_actions(
    (ACTION_TAG_HUG, KOCHIYA_SANAE, SHAMEIMARU_AYA),
    (ACTION_TAG_HUG, SHAMEIMARU_AYA, KOCHIYA_SANAE),
).with_creator(
    'Unya',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1417769756622065785/keine-mokou-lick-0001.png',
).with_action(
    ACTION_TAG_LICK, FUJIWARA_NO_MOKOU, KAMISHIRASAWA_KEINE,
).with_creator(
    'Unya',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1417769762003619910/sanae-suwako-kiss-0000.png',
).with_action(
    ACTION_TAG_KISS, MORIYA_SUWAKO, KOCHIYA_SANAE,
).with_creator(
    'Unya',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1417788275661475850/reisen-tewi-carry-0000.png',
).with_action(
    ACTION_TAG_CARRY, REISEN_UDONGEIN_INABA, INABA_TEWI,
).with_creator(
    'Mata (matasoup)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1417788281646612570/medi-yuuka-feed-0000.png',
).with_action(
    ACTION_TAG_FEED, KAZAMI_YUUKA, MEDICINE_MELANCHOLY,
).with_creator(
    'Mata (matasoup)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1417788285916549150/orin-hug-0000.png',
).with_action(
    ACTION_TAG_HUG, KAENBYOU_RIN, KAENBYOU_RIN,
).with_creator(
    'Mata (matasoup)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1417788289578045481/keine-hug-0001.png',
).with_action(
    ACTION_TAG_HUG, KAMISHIRASAWA_KEINE, KAMISHIRASAWA_KEINE,
).with_creator(
    'Mata (matasoup)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1417788296351711273/momiji-handhold-0000.png',
).with_action(
    ACTION_TAG_HANDHOLD, INUBASHIRI_MOMIJI, None,
).with_creator(
    'Mata (matasoup)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1417788304006578269/aya-momiji-bully-murder-0000.png',
).with_actions(
    (ACTION_TAG_BULLY, SHAMEIMARU_AYA, INUBASHIRI_MOMIJI),
    (ACTION_TAG_MURDER, INUBASHIRI_MOMIJI, SHAMEIMARU_AYA),
).with_creator(
    'Mata (matasoup)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1417788310528589895/keine-hug-0000.png',
).with_action(
    ACTION_TAG_HUG, KAMISHIRASAWA_KEINE, KAMISHIRASAWA_KEINE,
).with_character(
    KAMISHIRASAWA_KEINE,
).with_creator(
    'Mata (matasoup)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1417789620288094358/kogasa-nue-handhold-0003.png',
).with_actions(
    (ACTION_TAG_HANDHOLD, HOUJUU_NUE, TATARA_KOGASA),
    (ACTION_TAG_HANDHOLD, TATARA_KOGASA, HOUJUU_NUE),
).with_creator(
    'Moura (kenyuugetu)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1417921806463008958/meiling-yachie-hug-0000.png',
).with_action(
    ACTION_TAG_HUG, HONG_MEILING, KICCHOU_YACHIE,
).with_creator(
    'Matsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1417921814293905578/aya-chiruno-kiss-0001.png',
).with_action(
    ACTION_TAG_KISS, SHAMEIMARU_AYA, CHIRUNO,
).with_creator(
    'Matsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1417921820551811212/aya-chiruno-handhold-0003.png',
).with_action(
    ACTION_TAG_HANDHOLD, CHIRUNO, SHAMEIMARU_AYA,
).with_creator(
    'Matsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1417923397173776494/aya-chiruno-hug-kiss-0006.png',
).with_actions(
    (ACTION_TAG_HUG, CHIRUNO, SHAMEIMARU_AYA),
    (ACTION_TAG_HUG, SHAMEIMARU_AYA, CHIRUNO),
    (ACTION_TAG_KISS, CHIRUNO, SHAMEIMARU_AYA),
    (ACTION_TAG_KISS, SHAMEIMARU_AYA, CHIRUNO),
).with_creator(
    'Matsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1417923798312685723/chiruno-happy-0001.png',
).with_action(
    ACTION_TAG_HAPPY, CHIRUNO, None,
).with_creator(
    'Matsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1417921842169254068/chiruno-remilia-feed_self-lick-0000.png',
).with_actions(
    (ACTION_TAG_FEED_SELF, CHIRUNO, CHIRUNO),
    (ACTION_TAG_LICK, SCARLET_REMILIA, CHIRUNO),
).with_creator(
    'Matsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1417921847621582878/ran-stare-0001.png',
).with_action(
    ACTION_TAG_STARE, YAKUMO_RAN, None,
).with_creator(
    'Matsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1417921853040889907/aya-chiruno-dance-0000.png',
).with_actions(
    (ACTION_TAG_DANCE, SHAMEIMARU_AYA, CHIRUNO),
    (ACTION_TAG_DANCE, CHIRUNO, SHAMEIMARU_AYA),
).with_creator(
    'Matsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1417921859801972896/aya-chiruno-handhold-0002.png',
).with_action(
    ACTION_TAG_HANDHOLD, CHIRUNO, SHAMEIMARU_AYA,
).with_creator(
    'Matsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1417921868970594334/chiruno-suwako-hug-0001.png',
).with_action(
    ACTION_TAG_HUG, MORIYA_SUWAKO, CHIRUNO,
).with_creator(
    'Matsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1417921874876436601/chiruno-suwako-hug-0002.png',
).with_action(
    ACTION_TAG_HUG, CHIRUNO, MORIYA_SUWAKO,
).with_creator(
    'Matsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1417921884145717389/aya-chiruno-handhold-0000.png',
).with_actions(
    (ACTION_TAG_HANDHOLD, CHIRUNO, SHAMEIMARU_AYA),
    (ACTION_TAG_HANDHOLD, SHAMEIMARU_AYA, CHIRUNO),
).with_creator(
    'Matsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1417921888826425435/chiruno-stare-0003.png',
).with_action(
    ACTION_TAG_STARE, CHIRUNO, None,
).with_creator(
    'Matsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1417921902978273381/chiruno-remilia-kiss-0000.png',
).with_action(
    ACTION_TAG_KISS, SCARLET_REMILIA, CHIRUNO,
).with_creator(
    'Matsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1417921909403816046/aya-chiruno-handhold-0001.png',
).with_action(
    ACTION_TAG_HANDHOLD, CHIRUNO, SHAMEIMARU_AYA,
).with_creator(
    'Matsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1417921914529120308/chiruno-komachi-orin-lap_sleep-0000.png',
).with_action(
    ACTION_TAG_LAP_SLEEP, CHIRUNO, ONOZUKA_KOMACHI,
).with_character(
    KAENBYOU_RIN,
).with_creator(
    'Matsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1417921918169907262/chiruno-stare-0004.png',
).with_action(
    ACTION_TAG_STARE, CHIRUNO, None,
).with_creator(
    'Matsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1417921923530358794/alice-wink-0000.png',
).with_action(
    ACTION_TAG_WINK, MARGATROID_ALICE, None,
).with_creator(
    'Matsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1417921926763905045/chiruno-okuu-hug-0000.png',
).with_actions(
    (ACTION_TAG_HUG, CHIRUNO, REIUJI_UTSUHO),
    (ACTION_TAG_HUG, REIUJI_UTSUHO, CHIRUNO),
).with_creator(
    'Matsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1417921930262220910/chiruno-wink-0000.png',
).with_action(
    ACTION_TAG_WINK, CHIRUNO, None,
).with_creator(
    'Matsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1417921934187827371/reimu-yukari-feed-0000.png',
).with_action(
    ACTION_TAG_FEED, HAKUREI_REIMU, YAKUMO_YUKARI,
).with_creator(
    'Matsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1417921941016412180/chiruno-yukari-poke-0000.png',
).with_action(
    ACTION_TAG_POKE, YAKUMO_YUKARI, CHIRUNO,
).with_creator(
    'Matsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1417921945550327882/aya-chiruno-hug-0005.png',
).with_action(
    ACTION_TAG_HUG, CHIRUNO, SHAMEIMARU_AYA,
).with_creator(
    'Matsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1417921949761540156/chiruno-happy-0000.png',
).with_action(
    ACTION_TAG_HAPPY, CHIRUNO, None,
).with_creator(
    'Matsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1417921952227786864/chiruno-patchouli-kiss-0000.png',
).with_action(
    ACTION_TAG_KISS, CHIRUNO, PATCHOULI_KNOWLEDGE,
).with_creator(
    'Matsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1417921956379889724/aya-chiruno-feed-0000.png',
).with_action(
    ACTION_TAG_FEED, CHIRUNO, SHAMEIMARU_AYA,
).with_creator(
    'Matsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1417921958842073338/aya-chiruno-lap_sleep-0001.png',
).with_action(
    ACTION_TAG_LAP_SLEEP, CHIRUNO, SHAMEIMARU_AYA,
).with_creator(
    'Matsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1417921962902163498/chiruno-rawr-0000.png',
).with_action(
    ACTION_TAG_RAWR, CHIRUNO, None,
).with_creator(
    'Matsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1417921974214197360/meiling-yachie-handhold-0000.png',
).with_actions(
    (ACTION_TAG_HANDHOLD, HONG_MEILING, KICCHOU_YACHIE),
    (ACTION_TAG_HANDHOLD, KICCHOU_YACHIE, HONG_MEILING),
).with_creator(
    'Matsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1417921978538659892/chiruno-dance-0000.png',
).with_action(
    ACTION_TAG_DANCE, CHIRUNO, None,
).with_creator(
    'Matsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1417921982145761470/chiruno-koishi-rawr-0000.png',
).with_actions(
    (ACTION_TAG_RAWR, CHIRUNO, None),
    (ACTION_TAG_RAWR, KOMEIJI_KOISHI, None),
).with_creator(
    'Matsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1417921994975871128/meiling-yachie-handhold-0001.png',
).with_actions(
    (ACTION_TAG_HANDHOLD, HONG_MEILING, KICCHOU_YACHIE),
    (ACTION_TAG_HANDHOLD, KICCHOU_YACHIE, HONG_MEILING),
).with_creator(
    'Matsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1417922001208873012/flandre-meiling-yachie-hug-0000.png',
).with_actions(
    (ACTION_TAG_HUG, HONG_MEILING, KICCHOU_YACHIE),
    (ACTION_TAG_HUG, SCARLET_FLANDRE, KICCHOU_YACHIE),
).with_creator(
    'Matsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1417922006279786586/aya-chiruno-kiss-0003.png',
).with_action(
    ACTION_TAG_KISS, CHIRUNO, SHAMEIMARU_AYA,
).with_creator(
    'Matsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1417922011006500914/chiruno-yuuka-kiss-lap_sleep-0000.png',
).with_actions(
    (ACTION_TAG_KISS, KAZAMI_YUUKA, CHIRUNO),
    (ACTION_TAG_LAP_SLEEP, CHIRUNO, KAZAMI_YUUKA),
).with_creator(
    'Matsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1417922015817633905/chiruno-cry-0000.png',
).with_action(
    ACTION_TAG_CRY, CHIRUNO, None,
).with_creator(
    'Matsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1417922019671933070/aya-chiruno-kiss-0005.png',
).with_actions(
    (ACTION_TAG_KISS, CHIRUNO, SHAMEIMARU_AYA),
    (ACTION_TAG_KISS, SHAMEIMARU_AYA, CHIRUNO),
).with_creator(
    'Matsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1417922023870435389/chiruno-nitori-handhold-0000.png',
).with_actions(
    (ACTION_TAG_HANDHOLD, CHIRUNO, KAWASHIRO_NITORI),
    (ACTION_TAG_HANDHOLD, KAWASHIRO_NITORI, CHIRUNO),
).with_creator(
    'Matsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1417928156005929090/aya-chiruno-hug-kiss-0007.png',
).with_actions(
    (ACTION_TAG_HUG, CHIRUNO, SHAMEIMARU_AYA),
    (ACTION_TAG_HUG, SHAMEIMARU_AYA, CHIRUNO),
    (ACTION_TAG_KISS, CHIRUNO, SHAMEIMARU_AYA),
    (ACTION_TAG_KISS, SHAMEIMARU_AYA, CHIRUNO),
).with_creator(
    'Matsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1417922031986540605/eirin-keine-handhold-0000.png',
).with_actions(
    (ACTION_TAG_HANDHOLD, KAMISHIRASAWA_KEINE, YAGOKORO_EIRIN),
    (ACTION_TAG_HANDHOLD, YAGOKORO_EIRIN, KAMISHIRASAWA_KEINE),
).with_creator(
    'Matsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1417922035140530277/aya-chiruno-kiss-0002.png',
).with_action(
    ACTION_TAG_KISS, CHIRUNO, SHAMEIMARU_AYA,
).with_creator(
    'Matsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1417922039498412132/komachi-yuuka-wave-0000.png',
).with_action(
    ACTION_TAG_WAVE, ONOZUKA_KOMACHI, KAZAMI_YUUKA,
).with_creator(
    'Matsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1417922042631688343/eirin-pat-0000.png',
).with_action(
    ACTION_TAG_PAT, YAGOKORO_EIRIN, None,
).with_creator(
    'Matsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1417922047316721664/chiruno-suwako-hug-0003.png',
).with_action(
    ACTION_TAG_HUG, CHIRUNO, MORIYA_SUWAKO,
).with_creator(
    'Matsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1417922054258425919/momiji-stare-0002.png',
).with_action(
    ACTION_TAG_STARE, INUBASHIRI_MOMIJI, None,
).with_creator(
    'Matsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1417922059505369139/aya-chiruno-kiss-0004.png',
).with_actions(
    (ACTION_TAG_KISS, CHIRUNO, SHAMEIMARU_AYA),
    (ACTION_TAG_KISS, SHAMEIMARU_AYA, CHIRUNO),
).with_creator(
    'Matsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1417922062957412452/chiruno-suwako-hug-0000.png',
).with_action(
    ACTION_TAG_HUG, CHIRUNO, MORIYA_SUWAKO,
).with_creator(
    'Matsu',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1417939797707723015/marisa-nitori-feed_self-0000.png',
).with_actions(
    (ACTION_TAG_FEED_SELF, KAWASHIRO_NITORI, KAWASHIRO_NITORI),
    (ACTION_TAG_FEED_SELF, KIRISAME_MARISA, KIRISAME_MARISA),
).with_creator(
    'Dairi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1417939803684732948/alice-happy-0000.png',
).with_action(
    ACTION_TAG_HAPPY, MARGATROID_ALICE, None,
).with_creator(
    'Dairi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1417939808025837618/futo-cry-0001.png',
).with_action(
    ACTION_TAG_CRY, MONONOBE_NO_FUTO, None,
).with_creator(
    'Dairi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1417939812404433108/koishi-happy-0001.png',
).with_action(
    ACTION_TAG_HAPPY, KOMEIJI_KOISHI, None,
).with_creator(
    'Dairi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1417939820264689807/murasa-shou-handhold-0000.png',
).with_actions(
    (ACTION_TAG_HANDHOLD, MURASA_MINAMITSU, TORAMARU_SHOU),
    (ACTION_TAG_HANDHOLD, TORAMARU_SHOU, MURASA_MINAMITSU),
).with_creator(
    'Dairi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1417939824782086316/futo-happy-0001.png',
).with_action(
    ACTION_TAG_HAPPY, MONONOBE_NO_FUTO, None,
).with_creator(
    'Dairi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1417939831484448948/junko-murasa-nom-0000.png',
).with_action(
    ACTION_TAG_NOM, JUNKO, MURASA_MINAMITSU,
).with_creator(
    'Dairi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1417939838728015882/sariel-stare-0000.png',
).with_action(
    ACTION_TAG_STARE, SARIEL, None,
).with_creator(
    'Dairi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1417939848207142912/dai-chiruno-handhold-0000.png',
).with_actions(
    (ACTION_TAG_HANDHOLD, CHIRUNO, DAIYOUSEI),
    (ACTION_TAG_HANDHOLD, DAIYOUSEI, CHIRUNO),
).with_creator(
    'Dairi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1417939854284558397/elis-wink-0000.png',
).with_action(
    ACTION_TAG_WINK, ELIS, None,
).with_creator(
    'Dairi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1417939862337749084/reisen-stare-0003.png',
).with_action(
    ACTION_TAG_STARE, REISEN_UDONGEIN_INABA, None,
).with_creator(
    'Dairi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1417939867597410354/futo-happy-0000.png',
).with_action(
    ACTION_TAG_HAPPY, MONONOBE_NO_FUTO, None,
).with_creator(
    'Dairi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1417939871942836244/chiruno-happy-0002.png',
).with_action(
    ACTION_TAG_HAPPY, CHIRUNO, None,
).with_creator(
    'Dairi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1417939878108332124/futo-cry-0000.png',
).with_action(
    ACTION_TAG_CRY, MONONOBE_NO_FUTO, None,
).with_creator(
    'Dairi',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1418497811913117766/kogasa-nue-hug-0007.png',
).with_action(
    ACTION_TAG_HUG, TATARA_KOGASA, HOUJUU_NUE,
).with_creator(
    'Blue Hawaii KGS (ぶるーはわい)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1418497816812195912/kogasa-nue-carry-0000.png',
).with_action(
    ACTION_TAG_CARRY, HOUJUU_NUE, TATARA_KOGASA,
).with_creator(
    'Blue Hawaii KGS (ぶるーはわい)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1418497822533095514/kogasa-nue-hug-0004.png',
).with_action(
    ACTION_TAG_HUG, HOUJUU_NUE, TATARA_KOGASA,
).with_creator(
    'Blue Hawaii KGS (ぶるーはわい)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1418497827952394310/kogasa-stare-0014.png',
).with_action(
    ACTION_TAG_STARE, TATARA_KOGASA, None,
).with_creator(
    'Blue Hawaii KGS (ぶるーはわい)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1418497836961628210/asama-happy-0000.png',
).with_action(
    ACTION_TAG_HAPPY, YUIMAN_ASAMA, None,
).with_creator(
    'Blue Hawaii KGS (ぶるーはわい)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1418497842116427887/kogasa-nue-kiss-0000.png',
).with_actions(
    (ACTION_TAG_KISS, HOUJUU_NUE, TATARA_KOGASA),
    (ACTION_TAG_KISS, TATARA_KOGASA, HOUJUU_NUE),
).with_creator(
    'Blue Hawaii KGS (ぶるーはわい)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1418497847359180810/kogasa-happy-0000.png',
).with_action(
    ACTION_TAG_HAPPY, TATARA_KOGASA, None,
).with_creator(
    'Blue Hawaii KGS (ぶるーはわい)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1418497851356479538/kogasa-nue-handhold-0004.png',
).with_actions(
    (ACTION_TAG_HANDHOLD, HOUJUU_NUE, TATARA_KOGASA),
    (ACTION_TAG_HANDHOLD, TATARA_KOGASA, HOUJUU_NUE),
).with_creator(
    'Blue Hawaii KGS (ぶるーはわい)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1418497857652002816/hijiri-kogasa-hug-0000.png',
).with_action(
    ACTION_TAG_HUG, HIJIRI_BYAKUREN, TATARA_KOGASA,
).with_creator(
    'Blue Hawaii KGS (ぶるーはわい)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1418497865323642950/kogasa-nue-pat-0001.png',
).with_action(
    ACTION_TAG_PAT, TATARA_KOGASA, HOUJUU_NUE,
).with_creator(
    'Blue Hawaii KGS (ぶるーはわい)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1418497871103135785/koishi-satori-hug-0014.png',
).with_action(
    ACTION_TAG_HUG, KOMEIJI_KOISHI, KOMEIJI_SATORI,
).with_creator(
    'Blue Hawaii KGS (ぶるーはわい)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1418497876291752026/kogasa-nue-hug-0005.png',
).with_actions(
    (ACTION_TAG_HUG, HOUJUU_NUE, TATARA_KOGASA),
    (ACTION_TAG_HUG, TATARA_KOGASA, HOUJUU_NUE),
).with_creator(
    'Blue Hawaii KGS (ぶるーはわい)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1418497884709584990/asama-ariya-handhold-0000.png',
).with_actions(
    (ACTION_TAG_HANDHOLD, IWANAGA_ARIYA, YUIMAN_ASAMA),
    (ACTION_TAG_HANDHOLD, YUIMAN_ASAMA, IWANAGA_ARIYA),
).with_creator(
    'Blue Hawaii KGS (ぶるーはわい)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1418497889260273715/kogasa-nue-handhold-0005.png',
).with_actions(
    (ACTION_TAG_HANDHOLD, HOUJUU_NUE, TATARA_KOGASA),
    (ACTION_TAG_HANDHOLD, TATARA_KOGASA, HOUJUU_NUE),
).with_creator(
    'Blue Hawaii KGS (ぶるーはわい)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1418497893966413885/kogasa-nue-hug-0006.png',
).with_action(
    ACTION_TAG_HUG, HOUJUU_NUE, TATARA_KOGASA,
).with_creator(
    'Blue Hawaii KGS (ぶるーはわい)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1418497899821666475/chiyari-yuuma-hug-0000.png',
).with_action(
    ACTION_TAG_HUG, TENKAJIN_CHIYARI, TOUTETSU_YUUMA,
).with_creator(
    'Blue Hawaii KGS (ぶるーはわい)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1418497909300793387/asama-ariya-handhold-0001.png',
).with_action(
    ACTION_TAG_HANDHOLD, IWANAGA_ARIYA, YUIMAN_ASAMA,
).with_creator(
    'Blue Hawaii KGS (ぶるーはわい)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1418497917269835847/kogasa-stare-0016.png',
).with_action(
    ACTION_TAG_STARE, TATARA_KOGASA, None,
).with_creator(
    'Blue Hawaii KGS (ぶるーはわい)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1418497928363773962/kogasa-nue-handhold-0007.png',
).with_action(
    ACTION_TAG_HANDHOLD, TATARA_KOGASA, HOUJUU_NUE,
).with_creator(
    'Blue Hawaii KGS (ぶるーはわい)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1418497938362994798/kogasa-nue-handhold-0006.png',
).with_actions(
    (ACTION_TAG_HANDHOLD, HOUJUU_NUE, TATARA_KOGASA),
    (ACTION_TAG_HANDHOLD, TATARA_KOGASA, HOUJUU_NUE),
).with_creator(
    'Blue Hawaii KGS (ぶるーはわい)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1418497944608575578/flandre-stare-0022.png',
).with_action(
    ACTION_TAG_STARE, SCARLET_FLANDRE, None,
).with_creator(
    'Blue Hawaii KGS (ぶるーはわい)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1418497951235575849/kogasa-nue-handhold-0008.png',
).with_actions(
    (ACTION_TAG_HANDHOLD, HOUJUU_NUE, TATARA_KOGASA),
    (ACTION_TAG_HANDHOLD, TATARA_KOGASA, HOUJUU_NUE),
).with_creator(
    'Blue Hawaii KGS (ぶるーはわい)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1418497959976243330/kogasa-stare-0017.png',
).with_action(
    ACTION_TAG_STARE, TATARA_KOGASA, None,
).with_creator(
    'Blue Hawaii KGS (ぶるーはわい)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1418497965060001833/kogasa-stare-0015.png',
).with_action(
    ACTION_TAG_STARE, TATARA_KOGASA, None,
).with_creator(
    'Blue Hawaii KGS (ぶるーはわい)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1418497970869108806/doremy-stare-0007.png',
).with_action(
    ACTION_TAG_STARE, DOREMY_SWEET, None,
).with_creator(
    'Blue Hawaii KGS (ぶるーはわい)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1418497977982648330/nue-happy-0002.png',
).with_action(
    ACTION_TAG_HAPPY, HOUJUU_NUE, None,
).with_creator(
    'Blue Hawaii KGS (ぶるーはわい)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1418497983820988416/koishi-happy-0002.png',
).with_action(
    ACTION_TAG_HAPPY, KOMEIJI_KOISHI, None,
).with_creator(
    'Blue Hawaii KGS (ぶるーはわい)',
)

TOUHOU_ACTION_ALL.add(
    'https://cdn.discordapp.com/attachments/568837922288173058/1418497990603182130/koishi-stare-0022.png',
).with_action(
    ACTION_TAG_STARE, KOMEIJI_KOISHI, None,
).with_creator(
    'Blue Hawaii KGS (ぶるーはわい)',
)
