__all__ = ('TOUHOU_ACTION_FEED',)

from ...image_handling_core import ImageDetail
from ...touhou_core import (
    CHIRUNO, HAKUREI_REIMU, HINANAWI_TENSHI, IZAYOI_SAKUYA, KIRISAME_MARISA, KOMEIJI_KOISHI, KONPAKU_YOUMU, NAGAE_IKU,
    RINGO, RUMIA, SAIGYOUJI_YUYUKO, SCARLET_FLANDRE, SCARLET_REMILIA, SEIRAN, TOUTETSU_YUUMA, TOYOSATOMIMI_NO_MIKO
)

# https://safebooru.org/index.php?page=post&s=list&tags=touhou+feeding+
# Page 1 added from rumia + flandre till ringo + seiran

TOUHOU_ACTION_FEED = [
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/1219193725947871262/chiruno-feed-0000.png',
    ).with_any(CHIRUNO),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/1219199629443203162/flandre-remilia-sakuya-feed-0000.png',
    ).with_source(SCARLET_FLANDRE).with_target(SCARLET_REMILIA),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/1219184783611920424/flandre-rumia-feed-0000.png',
    ).with_source(SCARLET_FLANDRE).with_target(RUMIA),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/1219191396397875250/flandre-yuuma-feed-0000.png',
    ).with_source(SCARLET_FLANDRE).with_target(TOUTETSU_YUUMA),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/1219197486661632030/iku-tenshi-feed-0000.png',
    ).with_source(NAGAE_IKU).with_target(HINANAWI_TENSHI),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/1219192143508410378/koishi-feed-0000.png',
    ).with_target(KOMEIJI_KOISHI),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/1219196416442896445/koishi-feed-0001.png',
    ).with_target(KOMEIJI_KOISHI),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/1219186780817850378/marisa-reimu-feed-0000.png',
    ).with_source(KIRISAME_MARISA).with_target(HAKUREI_REIMU),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/1219252027981566052/miko-remilia-feed-0000.png',
    ).with_source(TOYOSATOMIMI_NO_MIKO).with_target(SCARLET_REMILIA),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/1219259653997723749/reimu-sakuya-feed-0000.png',
    ).with_source(IZAYOI_SAKUYA).with_target(HAKUREI_REIMU),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/1219261244368883722/ringo-seiran-feed-0000.png',
    ).with_source(SEIRAN).with_target(RINGO),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/1219189215674499072/sakuya-feed-0000.png',
    ).with_source(IZAYOI_SAKUYA),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/1219183800043569203/youmu-yuyuko-feed-0000.png',
    ).with_source(KONPAKU_YOUMU).with_target(SAIGYOUJI_YUYUKO),
]
