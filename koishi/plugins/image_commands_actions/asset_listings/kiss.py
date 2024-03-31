__all__ = ('TOUHOU_ACTION_KISS',)

from ...image_handling_core import ImageDetail
from ...touhou_core import (
    CHEN, FUJIWARA_NO_MOKOU, HAKUREI_REIMU, HATA_NO_KOKORO, HIMEKAIDOU_HATATE, HONG_MEILING, HOUJUU_NUE,
    HOURAISAN_KAGUYA, INABA_TEWI, IZAYOI_SAKUYA, KAENBYOU_RIN, KIRISAME_MARISA, KOCHIYA_SANAE, KOMEIJI_KOISHI,
    KOMEIJI_SATORI, KONPAKU_YOUMU, MARGATROID_ALICE, MORICHIKA_RINNOSUKE, MORIYA_SUWAKO, MURASA_MINAMITSU,
    PATCHOULI_KNOWLEDGE, REISEN_UDONGEIN_INABA, REIUJI_UTSUHO, SAIGYOUJI_YUYUKO, SCARLET_FLANDRE, SCARLET_REMILIA,
    SHAMEIMARU_AYA, YAGOKORO_EIRIN, YAKUMO_RAN, YAKUMO_YUKARI, YASAKA_KANAKO
)

# Source 0:
# https://safebooru.org/index.php?page=post&s=list&tags=touhou+kiss&pid=2640
# 2 page added (from behind)
#
#
# Source 1:
# From my pc actually.
# :KoishiPc:


TOUHOU_ACTION_KISS = [
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/1220252970327736340/alice-marisa-kiss-0000.png',
    ).with_source(MARGATROID_ALICE).with_target(KIRISAME_MARISA),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/1220258995626049587/alice-marisa-kiss-0001.png',
    ).with_any(MARGATROID_ALICE).with_any(KIRISAME_MARISA),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/1220252166154092545/aya-reisen-tewi-kiss-0000.png',
    ).with_source(INABA_TEWI).with_target(REISEN_UDONGEIN_INABA),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/1223888294618599465/aya-hatate-kiss-0000.png',
    ).with_any(SHAMEIMARU_AYA).with_any(HIMEKAIDOU_HATATE),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/1223887385968775209/chen-nue-kiss-0000.png',
    ).with_source(HOUJUU_NUE).with_target(CHEN),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/1220259663019376692/eirin-kaguya-kiss-0000.png',
    ).with_any(YAGOKORO_EIRIN).with_any(HOURAISAN_KAGUYA),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/1220256917948203069/eirin-reisen-youmu-yuyuko-kiss-0000.png',
    ).with_source(KONPAKU_YOUMU).with_target(REISEN_UDONGEIN_INABA),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/1220101427360169984/flandre-koishi-kiss-0000.png',
    ).with_source(SCARLET_FLANDRE).with_target(KOMEIJI_KOISHI),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/1223985953228591168/flandre-koishi-kiss-0001.png',
    ).with_source(KOMEIJI_KOISHI).with_target(SCARLET_FLANDRE),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/1223985953857867787/flandre-koishi-kiss-0002.png',
    ).with_source(KOMEIJI_KOISHI).with_target(SCARLET_FLANDRE),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/1223978928780083331/flandre-meiling-remilia-sakuya-kiss-0000.png',
    ).with_source(SCARLET_REMILIA).with_target(IZAYOI_SAKUYA),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/1220251342149390427/kaguya-mokou-kiss-0000.png',
    ).with_source(HOURAISAN_KAGUYA).with_target(FUJIWARA_NO_MOKOU),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/1220255801436930078/kanako-sanae-kiss-0000.png',
    ).with_source(YASAKA_KANAKO).with_target(KOCHIYA_SANAE),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/1220254791570292898/kanako-sanae-sawuko-kiss-0000.png',
    ).with_source(YASAKA_KANAKO).with_source(MORIYA_SUWAKO).with_target(KOCHIYA_SANAE),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/1223989690118570044/koishi-kokoro-kiss-0000.png',
    ).with_source(KOMEIJI_KOISHI).with_target(HATA_NO_KOKORO),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/1223989691016155156/koishi-kokoro-kiss-0002.png',
    ).with_source(KOMEIJI_KOISHI).with_target(HATA_NO_KOKORO),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/1223989691334918185/koishi-kokoro-kiss-0003.png',
    ).with_any(KOMEIJI_KOISHI).with_any(HATA_NO_KOKORO),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/1223989691770994718/koishi-kokoro-kiss-0004.png',
    ).with_any(KOMEIJI_KOISHI).with_any(HATA_NO_KOKORO),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/1223986286961098887/koishi-satori-kiss-0000.png',
    ).with_source(KOMEIJI_KOISHI).with_target(KOMEIJI_SATORI),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/1223986287342653590/koishi-satori-kiss-0001.png',
    ).with_source(KOMEIJI_KOISHI).with_target(KOMEIJI_SATORI),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/1220250378562703371/marisa-patchouli-kiss-0000.png',
    ).with_any(KIRISAME_MARISA).with_any(PATCHOULI_KNOWLEDGE),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/1220255012069048320/marisa-sakuya-kiss-0000.png',
    ).with_source(KIRISAME_MARISA).with_target(IZAYOI_SAKUYA),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/1220247261976592494/marisa-reimu-kiss-0000.png',
    ).with_source(HAKUREI_REIMU).with_target(KIRISAME_MARISA),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/1220257838161461308/meiling-sakuya-kiss-0000.png',
    ).with_source(HONG_MEILING).with_target(IZAYOI_SAKUYA),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/1223882100516720660/murasa-nue-kiss-0000.png',
    ).with_source(MURASA_MINAMITSU).with_target(HOUJUU_NUE),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/1223886680151298048/okuu-orin-kiss-0000.png',
    ).with_source(REIUJI_UTSUHO).with_target(KAENBYOU_RIN),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/1223886681049006100/okuu-orin-kiss-0001.png',
    ).with_source(REIUJI_UTSUHO).with_target(KAENBYOU_RIN),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/1223889656362569728/orin-reimu-kiss-0000.png',
    ).with_source(KAENBYOU_RIN).with_target(HAKUREI_REIMU),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/1223976841182707762/ran-yukari-kiss-0000.png',
    ).with_source(YAKUMO_YUKARI).with_target(YAKUMO_RAN),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/1223976842025767014/ran-yukari-kiss-0001.png',
    ).with_any(YAKUMO_RAN).with_any(YAKUMO_YUKARI),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/1223978271197237308/remilia-sakuya-kiss-0000.png',
    ).with_source(SCARLET_REMILIA).with_target(IZAYOI_SAKUYA),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/1223982249142386719/remilia-satori-kiss-0000.png',
    ).with_source(SCARLET_REMILIA).with_target(KOMEIJI_SATORI),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/1220248539096027136/rinnosuke-sakuya-kiss-0000.png',
    ).with_source(MORICHIKA_RINNOSUKE).with_target(IZAYOI_SAKUYA),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/1223980216804835360/suika-yukari-yuyuko-kiss-0000.png',
    ).with_any(YAKUMO_YUKARI).with_any(SAIGYOUJI_YUYUKO),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/1220246770051715143/youmu-yuyuko-kiss-0000.png',
    ).with_source(SAIGYOUJI_YUYUKO).with_target(KONPAKU_YOUMU),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/1223982548124831885/yukari-yuyuko-kiss-0000.png',
    ).with_any(YAKUMO_YUKARI).with_any(SAIGYOUJI_YUYUKO),
]
