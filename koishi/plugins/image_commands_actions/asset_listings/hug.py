__all__ = ('TOUHOU_ACTION_HUG',)

from ...image_handling_core import ImageDetail
from ...touhou_core import (
    CHEN, FUJIWARA_NO_MOKOU, HAKUREI_REIMU, HANIYASUSHIN_KEIKI, HATA_NO_KOKORO, HIJIRI_BYAKUREN, HOUJUU_NUE,
    HOURAISAN_KAGUYA, INABA_TEWI, IZAYOI_SAKUYA, JOUTOUGUU_MAYUMI, KAENBYOU_RIN, KAMISHIRASAWA_KEINE, KAZAMI_YUUKA,
    KIRISAME_MARISA, KOMEIJI_KOISHI, KOMEIJI_SATORI, KONPAKU_YOUMU, MORIYA_SUWAKO, MURASA_MINAMITSU,
    REISEN_UDONGEIN_INABA, REIUJI_UTSUHO, SCARLET_FLANDRE, SCARLET_REMILIA, YAGOKORO_EIRIN, YAKUMO_RAN, YAKUMO_YUKARI,
    YASAKA_KANAKO
)

# Source 0:
# https://safebooru.org/index.php?page=post&s=list&tags=touhou+hug&pid=8840
# 2 page added (from behind)
#
#
# Source 1:
# From my pc actually
# :KoishiPc:


TOUHOU_ACTION_HUG = [
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/1223583582220456029/chen-ran-hug-0000.png',
    ).with_source(YAKUMO_RAN).with_target(CHEN),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/1220328524653793303/chen-ran-yukari-hug-0000.png',
    ).with_source(CHEN).with_source(YAKUMO_RAN).with_target(YAKUMO_RAN),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/1220266946021556254/eirin-kaguya-hug-0000.png',
    ).with_source(HOURAISAN_KAGUYA).with_target(YAGOKORO_EIRIN),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/1220443739642662952/eirin-reisen-hug-0000.png',
    ).with_source(YAGOKORO_EIRIN).with_target(REISEN_UDONGEIN_INABA),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/1223584864469778442/flandre-koishi-hug-0000.png',
    ).with_source(SCARLET_FLANDRE).with_target(KOMEIJI_KOISHI),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/1220448035662987264/flandre-marisa-hug-0000.png',
    ).with_source(SCARLET_FLANDRE).with_target(KIRISAME_MARISA),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/1220451292103577620/flandre-marisa-hug-0001.png',
    ).with_source(KIRISAME_MARISA).with_target(SCARLET_FLANDRE),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/1220452861675176106/flandre-marisa-hug-0002.png',
    ).with_source(KIRISAME_MARISA).with_target(SCARLET_FLANDRE),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/1220265826171617350/flandre-remilia-hug-0000.png',
    ).with_any(SCARLET_FLANDRE).with_any(SCARLET_REMILIA),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/1220449089473482762/flandre-remilia-hug-0001.png',
    ).with_source(SCARLET_FLANDRE).with_target(SCARLET_REMILIA),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/1220450482544316466/flandre-remilia-hug-0002.png',
    ).with_source(SCARLET_FLANDRE).with_target(SCARLET_REMILIA),
    
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/1223871834794102804/hijiri-nue-hug-0000.png',
    ).with_any(HIJIRI_BYAKUREN).with_any(HOUJUU_NUE),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/1220445835314204672/kaguya-mokou-hug-0000.png',
    ).with_source(HOURAISAN_KAGUYA).with_target(FUJIWARA_NO_MOKOU),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/1220331527884378162/kaguya-tewi-hug-0000.png',
    ).with_source(HOURAISAN_KAGUYA).with_target(INABA_TEWI),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/1220444261405954048/kanako-suwako-hug-0000.png',
    ).with_any(MORIYA_SUWAKO).with_any(YASAKA_KANAKO),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/1223719258941292696/keiki-mayumi-hug-0000.png',
    ).with_any(HANIYASUSHIN_KEIKI).with_any(JOUTOUGUU_MAYUMI),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/1220447468173656166/keine-mokou-hug-0000.png',
    ).with_any(KAMISHIRASAWA_KEINE).with_any(FUJIWARA_NO_MOKOU),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/1223721535311974400/koishi-hug-0000.png',
    ).with_any(KOMEIJI_KOISHI),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/1223601016079912991/koishi-kokoro-hug-0000.png',
    ).with_any(KOMEIJI_KOISHI).with_any(HATA_NO_KOKORO),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/1223602190455934976/koishi-kokoro-hug-0001.png',
    ).with_source(KOMEIJI_KOISHI).with_target(HATA_NO_KOKORO),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/1223603074053046302/koishi-kokoro-hug-0002.png',
    ).with_source(KOMEIJI_KOISHI).with_target(HATA_NO_KOKORO),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/1223710267503022131/koishi-kokoro-hug-0003.png',
    ).with_source(KOMEIJI_KOISHI).with_target(HATA_NO_KOKORO),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/1223724567067889825/koishi-okuu-hug-0000.png',
    ).with_source(REIUJI_UTSUHO).with_target(KOMEIJI_KOISHI),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/1223720362240512050/koishi-orin-hug-0000.png',
    ).with_source(KOMEIJI_KOISHI).with_target(KAENBYOU_RIN),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/1223585164102209576/koishi-reimu-hug-0000.png',
    ).with_source(KOMEIJI_KOISHI).with_target(HAKUREI_REIMU),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/1220265214897950720/koishi-satori-hug-0000.png',
    ).with_source(KOMEIJI_SATORI).with_target(KOMEIJI_KOISHI),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/1220269573971120189/koishi-satori-hug-0001.png',
    ).with_source(KOMEIJI_KOISHI).with_target(KOMEIJI_SATORI),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/1223585980855091261/koishi-satori-hug-0002.png',
    ).with_source(KOMEIJI_SATORI).with_target(KOMEIJI_KOISHI),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/1223587363779776614/koishi-satori-hug-0003.png',
    ).with_source(KOMEIJI_KOISHI).with_target(KOMEIJI_SATORI),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/1223600484682825879/koishi-satori-hug-0004.png',
    ).with_source(KOMEIJI_KOISHI).with_target(KOMEIJI_SATORI),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/1220261434416693308/marisa-reimu-hug-0000.png',
    ).with_any(KIRISAME_MARISA).with_any(HAKUREI_REIMU),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/1220446460278083604/marisa-reimu-hug-0001.png',
    ).with_source(HAKUREI_REIMU).with_target(KIRISAME_MARISA),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/1223717761398607902/marisa-reimu-hug-0002.png',
    ).with_source(HAKUREI_REIMU).with_target(KIRISAME_MARISA),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/1223717960275984384/marisa-reimu-hug-0003.png',
    ).with_source(HAKUREI_REIMU).with_target(KIRISAME_MARISA),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/1220451881143242842/marisa-yuuka-hug-0000.png',
    ).with_source(KIRISAME_MARISA).with_target(KAZAMI_YUUKA),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/1223871067202785291/murasa-nue-hug-0000.png',
    ).with_source(HOUJUU_NUE).with_target(MURASA_MINAMITSU),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/1223871067584598016/murasa-nue-hug-0001.png',
    ).with_source(MURASA_MINAMITSU).with_target(HOUJUU_NUE),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/1223571617431420969/nue-okuu-hug-0000.png',
    ).with_any(HOUJUU_NUE).with_any(REIUJI_UTSUHO),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/1223878125096538122/okuu-orin-hug-0000.png',
    ).with_source(REIUJI_UTSUHO).with_target(KAENBYOU_RIN),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/1223878125415563334/okuu-orin-hug-0001.png',
    ).with_source(REIUJI_UTSUHO).with_target(KAENBYOU_RIN),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/1223879720219840542/okuu-orin-hug-0002.png',
    ).with_source(KAENBYOU_RIN).with_target(REIUJI_UTSUHO),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/1223878126283526164/okuu-orin-hug-0003.png',
    ).with_source(REIUJI_UTSUHO).with_target(KAENBYOU_RIN),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/1223878127017787502/okuu-orin-hug-0004.png',
    ).with_source(REIUJI_UTSUHO).with_target(KAENBYOU_RIN),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/1223878127520841828/okuu-orin-hug-0005.png',
    ).with_any(REIUJI_UTSUHO).with_any(KAENBYOU_RIN),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/1223878128037003274/okuu-orin-hug-0006.png',
    ).with_source(REIUJI_UTSUHO).with_target(KAENBYOU_RIN),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/1223878128586195034/okuu-orin-hug-0007.png',
    ).with_source(KAENBYOU_RIN).with_target(REIUJI_UTSUHO),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/1220327756517212202/reimu-yukari-hug-0000.png',
    ).with_source(YAKUMO_YUKARI).with_target(HAKUREI_REIMU),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/1220330697470775296/reisen-tewi-hug-0000.png',
    ).with_source(INABA_TEWI).with_target(REISEN_UDONGEIN_INABA),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/1220329396536217600/remilia-sakuya-hug-0000.png',
    ).with_source(SCARLET_REMILIA).with_target(IZAYOI_SAKUYA),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/1223588897133695046/remilia-satori-hug-0000.png',
    ).with_any(SCARLET_REMILIA).with_any(KOMEIJI_SATORI),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/1220450004808896513/youmu-yukari-hug-0000.png',
    ).with_source(YAKUMO_YUKARI).with_target(KONPAKU_YOUMU),
]
