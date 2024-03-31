__all__ = ('TOUHOU_ACTION_PAT',)

from ...image_handling_core import ImageDetail
from ...touhou_core import (
    CHEN, CHIRUNO, CLOWNPIECE, DAIYOUSEI, FUJIWARA_NO_MOKOU, FUTATSUIWA_MAMIZOU, HAKUREI_MIKO, HAKUREI_REIMU,
    HECATIA_LAPISLAZULI, HIJIRI_BYAKUREN, HIMEKAIDOU_HATATE, HOSHIGUMA_YUUGI, HOUJUU_NUE, HOURAISAN_KAGUYA, IBUKI_SUIKA,
    INUBASHIRI_MOMIJI, KAENBYOU_RIN, KAGIYAMA_HINA, KAMISHIRASAWA_KEINE, KASODANI_KYOUKO, KIRISAME_MARISA,
    KOMEIJI_KOISHI, KOMEIJI_SATORI, KONPAKU_YOUMU, MARGATROID_ALICE, MIZUHASHI_PARSEE, MORIYA_SUWAKO,
    REISEN_UDONGEIN_INABA, RUMIA, SAIGYOUJI_YUYUKO, SCARLET_FLANDRE, SHAMEIMARU_AYA, YAKUMO_RAN, YAKUMO_YUKARI
)


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


TOUHOU_ACTION_PAT = [
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/1220485700319838328/alice-reimu-pat-0000.png',
    ).with_source(MARGATROID_ALICE).with_target(HAKUREI_REIMU),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/1220478088601800714/aya-momiji-pat-0000.png',
    ).with_source(SHAMEIMARU_AYA).with_target(INUBASHIRI_MOMIJI),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/1220484187769798676/aya-momiji-pat-0001.png',
    ).with_source(SHAMEIMARU_AYA).with_target(INUBASHIRI_MOMIJI),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/1220487826039246959/chen-ran-pat-0000.png',
    ).with_source(YAKUMO_RAN).with_target(CHEN),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/1220490334103011420/chen-ran-pat-0001.png',
    ).with_source(YAKUMO_RAN).with_target(CHEN),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/1223524331145924648/chen-ran-pat-0002.png',
    ).with_source(YAKUMO_RAN).with_target(CHEN),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/1223527236238442597/chiurno-pat-0000.gif',
    ).with_target(CHIRUNO),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/1220491614573826058/clownpiece-hecatia-pat-0000.png',
    ).with_source(HECATIA_LAPISLAZULI).with_target(CLOWNPIECE),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/1220478887054540800/dai-pat-0000.png',
    ).with_target(DAIYOUSEI),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/1223307489181958335/flandre-hmiko-pat-0000.png',
    ).with_source(HAKUREI_MIKO).with_target(SCARLET_FLANDRE),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/1220484865745621012/hatate-pat-0000.png',
    ).with_target(HIMEKAIDOU_HATATE),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/1220499155844337774/hijiri-kyouko-pat-0000.png',
    ).with_source(HIJIRI_BYAKUREN).with_target(KASODANI_KYOUKO),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/1220490545772888124/hijiri-nue-pat-0000.png',
    ).with_source(HIJIRI_BYAKUREN).with_target(HOUJUU_NUE),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/1220483214452457572/hina-parsee-pat-0000.png',
    ).with_source(KAGIYAMA_HINA).with_target(MIZUHASHI_PARSEE),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/1223307488863060008/hmiko-reimu-yukari-pat-0000.png',
    ).with_source(HAKUREI_MIKO).with_source(YAKUMO_YUKARI).with_target(HAKUREI_REIMU),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/1220490850174243016/kaguya-reisen-pat-0000.png',
    ).with_source(HOURAISAN_KAGUYA).with_target(REISEN_UDONGEIN_INABA),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/1220481124992552980/keine-mokou-pat-0000.png',
    ).with_source(KAMISHIRASAWA_KEINE).with_target(FUJIWARA_NO_MOKOU),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/1223527844140027904/koishi-orin-satori-pat-0000.gif',
    ).with_source(KOMEIJI_SATORI).with_any(KOMEIJI_KOISHI).with_target(KAENBYOU_RIN),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/1223311829128839269/koishi-pat-0000.png',
    ).with_target(KOMEIJI_KOISHI),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/1223522925756416000/koishi-pat-0001.png',
    ).with_target(KOMEIJI_KOISHI),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/1223523971136356373/koishi-pat-0002.png',
    ).with_target(KOMEIJI_KOISHI),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/1220480274861785148/mamizou-nue-pat-0000.png',
    ).with_source(FUTATSUIWA_MAMIZOU).with_target(HOUJUU_NUE),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/1223311004818079867/marisa-pat-0000.png',
    ).with_target(KIRISAME_MARISA),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/1223530588611284992/orin-pat-0000.png',
    ).with_target(KAENBYOU_RIN),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/1223309868082135170/orin-satori-pat-0000.png',
    ).with_source(KOMEIJI_SATORI).with_target(KAENBYOU_RIN),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/1220498038850715779/parsee-pat-0000.png',
    ).with_target(MIZUHASHI_PARSEE),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/1223526207543443486/parsee-yuugi-pat-0000.png',
    ).with_source(HOSHIGUMA_YUUGI).with_target(MIZUHASHI_PARSEE),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/1220489732346085376/reimu-pat-0000.png',
    ).with_any(HAKUREI_REIMU),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/1220486953707765770/reimu-yukari-pat-0000.png',
    ).with_source(YAKUMO_YUKARI).with_target(HAKUREI_REIMU),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/1220492733462876270/rumia-pat-0000.png',
    ).with_target(RUMIA),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/1220479886460977182/suika-yuugi-pat-0000.png',
    ).with_source(HOSHIGUMA_YUUGI).with_target(IBUKI_SUIKA),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/1220477581795786752/suwako-pat-0000.png',
    ).with_target(MORIYA_SUWAKO),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/1220479334934904943/youmu-yuyuko-pat-0000.png',
    ).with_source(SAIGYOUJI_YUYUKO).with_target(KONPAKU_YOUMU),
]
