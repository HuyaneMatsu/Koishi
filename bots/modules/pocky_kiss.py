__all__ = ()

from random import choice

from hata import Client, Embed
from hata.ext.slash import abort, InteractionResponse

from .waifu import build_response_and_allowed_users


SLASH_CLIENT: Client

# Images from: https://safebooru.org/index.php?page=post&s=list&tags=2girls+pocky_kiss+touhou

IMAGE_URLS = [
    'https://cdn.discordapp.com/attachments/568837922288173058/959700573081452564/akyuu-x-kosuzu-0000.png',
    'https://cdn.discordapp.com/attachments/568837922288173058/959700573706407946/aya-x-remilia-0000.png',
    'https://cdn.discordapp.com/attachments/568837922288173058/959700574033567754/chen-x-orin-0000.png',
    'https://cdn.discordapp.com/attachments/568837922288173058/959700574335537152/chen-x-ran-0000.png',
    'https://cdn.discordapp.com/attachments/568837922288173058/959700574721425428/chiruno-x-dai-0000.png',
    'https://cdn.discordapp.com/attachments/568837922288173058/959700575040184350/flandre-x-remilia-0000.png',
    'https://cdn.discordapp.com/attachments/568837922288173058/959700575291846686/hatate-x-aya-0000.png',
    'https://cdn.discordapp.com/attachments/568837922288173058/959700575585439794/kagerou-x-remilia-0000.png',
    'https://cdn.discordapp.com/attachments/568837922288173058/959700575841304597/keine-x-mokou-0000.png',
    'https://cdn.discordapp.com/attachments/568837922288173058/959700576113926154/keine-x-mokou-0001.png',
    'https://cdn.discordapp.com/attachments/568837922288173058/959701269969256488/koishi-x-flandre-0000.png',
    'https://cdn.discordapp.com/attachments/568837922288173058/959701270401257512/koishi-x-flandre-0001.png',
    'https://cdn.discordapp.com/attachments/568837922288173058/959701270820716654/koishi-x-kokoro-0000.png',
    'https://cdn.discordapp.com/attachments/568837922288173058/959701271298859068/koishi-x-satori-0000.png',
    'https://cdn.discordapp.com/attachments/568837922288173058/959701271579873321/koishi-x-satori-0001.png',
    'https://cdn.discordapp.com/attachments/568837922288173058/959701271852482570/kokoro-x-koishi-0000.png',
    'https://cdn.discordapp.com/attachments/568837922288173058/959701272150286366/lily-x-rumia-0000.png',
    # 'https://cdn.discordapp.com/attachments/568837922288173058/959701272460673024/maribel-x-renko-0000.png',
    'https://cdn.discordapp.com/attachments/568837922288173058/959701770509119498/marisa-x-alice-0000.png',
    # 'https://cdn.discordapp.com/attachments/568837922288173058/959701770773331988/marisa-x-reimu-0000.png',
    'https://cdn.discordapp.com/attachments/568837922288173058/959701771037589524/marisa-x-reimu-0001.png',
    'https://cdn.discordapp.com/attachments/568837922288173058/959701771377315880/marisa-x-reimu-0002.png',
    # 'https://cdn.discordapp.com/attachments/568837922288173058/959701771612213288/marisa-x-reimu-0003.png',
    'https://cdn.discordapp.com/attachments/568837922288173058/959701771792547871/meiling-x-sakuya-0000.png',
    'https://cdn.discordapp.com/attachments/568837922288173058/959701772140691456/minamitsu-x-nue-0000.png',
    'https://cdn.discordapp.com/attachments/568837922288173058/959701772421718026/mokou-x-keine-0000.png',
    'https://cdn.discordapp.com/attachments/568837922288173058/959701772975362118/mystia-x-rumia-0000.png',
    'https://cdn.discordapp.com/attachments/568837922288173058/959702866010968074/nazrin-x-shou-0000.png',
    'https://cdn.discordapp.com/attachments/568837922288173058/959702866392678440/nue-x-kogasa-0000.png',
    'https://cdn.discordapp.com/attachments/568837922288173058/959702866635923496/patchouli-x-remilia-0000.png',
    'https://cdn.discordapp.com/attachments/568837922288173058/959702867080515584/ran-x-chen-0000.png',
    'https://cdn.discordapp.com/attachments/568837922288173058/959702867458019358/ran-x-chen-0001.png',
    'https://cdn.discordapp.com/attachments/568837922288173058/959702867936149534/reimu-x-marisa-0000.png',
    'https://cdn.discordapp.com/attachments/568837922288173058/959702868305272832/reimu-x-sanae-0000.png',
    'https://cdn.discordapp.com/attachments/568837922288173058/959703161893965854/remilia-x-flandre-0000.png',
    'https://cdn.discordapp.com/attachments/568837922288173058/959703162195963934/remilia-x-flandre-0001.png',
    'https://cdn.discordapp.com/attachments/568837922288173058/959703162795753482/renko-x-maribel-0000.png',
    'https://cdn.discordapp.com/attachments/568837922288173058/959703163097722951/renko-x-mirabel-0000.png',
    'https://cdn.discordapp.com/attachments/568837922288173058/959703163466825748/rumia-x-chiruno-0000.png',
    # 'https://cdn.discordapp.com/attachments/568837922288173058/959703163735248936/sakuya-x-meiling-0000.gif',
    'https://cdn.discordapp.com/attachments/568837922288173058/959703164125347860/sakuya-x-meiling-0000.png',
    # 'https://cdn.discordapp.com/attachments/568837922288173058/959703164515397652/sakuya-x-meiling-0001.png',
    'https://cdn.discordapp.com/attachments/568837922288173058/959703496012222475/shou-x-nazrin-0000.png',
    'https://cdn.discordapp.com/attachments/568837922288173058/959703496444227584/suwako-x-kanako-0000.png',
    'https://cdn.discordapp.com/attachments/568837922288173058/959703496830107658/suwako-x-sanae-0000.png',
    'https://cdn.discordapp.com/attachments/568837922288173058/959703497190830080/tenshi-x-reimu-0000.png',
    'https://cdn.discordapp.com/attachments/568837922288173058/959703497501204521/wakasagihime-x-kagerou-0000.png',
    'https://cdn.discordapp.com/attachments/568837922288173058/959703497836744714/yomou-x-patchouli-0000.png',
    'https://cdn.discordapp.com/attachments/568837922288173058/959703498113581056/youmu-x-sanae-0000.png',
    'https://cdn.discordapp.com/attachments/568837922288173058/959703498939830313/yuyuki-x-yukari-0000.png',
    'https://cdn.discordapp.com/attachments/568837922288173058/959703499388616734/yuyuko-x-mystia-0000.png',
]


@SLASH_CLIENT.interactions(is_global=True)
async def pocky_kiss(client, event,
    user_00: ('user', 'Select someone.', 'user-1') = None,
    user_01: ('user', 'Select someone', 'user-2') = None,
    user_02: ('user', 'Select someone', 'user-3') = None,
    user_03: ('user', 'Select someone', 'user-4') = None,
    user_04: ('user', 'Select someone', 'user-5') = None,
    user_05: ('user', 'Select someone', 'user-6') = None,
    user_06: ('user', 'Select someone', 'user-7') = None,
    user_07: ('user', 'Select someone', 'user-8') = None,
    user_08: ('user', 'Select someone', 'user-9') = None,
    user_09: ('user', 'Select someone', 'user-10') = None,
    user_10: ('user', 'Select someone', 'user-11') = None,
    user_11: ('user', 'Select someone', 'user-12') = None,
    user_12: ('user', 'Select someone', 'user-13') = None,
    user_13: ('user', 'Select someone', 'user-14') = None,
    user_14: ('user', 'Select someone', 'user-15') = None,
    user_15: ('user', 'Select someone', 'user-16') = None,
    user_16: ('user', 'Select someone', 'user-17') = None,
    user_17: ('user', 'Select someone', 'user-18') = None,
    user_18: ('user', 'Select someone', 'user-19') = None,
    user_19: ('user', 'Select someone', 'user-20') = None,
    user_20: ('user', 'Select someone', 'user-21') = None,
    user_21: ('user', 'Select someone', 'user-22') = None,
    user_22: ('user', 'Select someone', 'user-23') = None,
    user_23: ('user', 'Select someone', 'user-24') = None,
    user_24: ('user', 'Select someone', 'user-25') = None,
):
    guild_id = event.guild_id
    if not guild_id:
        abort('Guild only command')
    
    response, allowed_mentions = build_response_and_allowed_users(
        client, event, 'pocky kisses',
        (
            user_00, user_01, user_02, user_03, user_04, user_05, user_06, user_07, user_08, user_09,
            user_10, user_11, user_12, user_13, user_14, user_15, user_16, user_17, user_18, user_19,
            user_20, user_21, user_22, user_23, user_24
        )
    )
    
    return InteractionResponse(
        response,
        embed = Embed(
            color = (event.id >> 22) & 0xffffff
        ).add_image(
            choice(IMAGE_URLS),
        ),
        allowed_mentions = allowed_mentions,
    )
