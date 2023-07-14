__all__ = ('TOUHOU_ACTION_POCKY_KISS', 'TOUHOU_ACTION_POCKY_KISS_SELF')

from ...image_handling_core import ImageDetail
from ...touhou_core.character import freeze
from ...touhou_core.characters import (
    CHEN, CHIRUNO, DAIYOUSEI, FUJIWARA_NO_MOKOU, HAKUREI_REIMU, HATA_NO_KOKORO, HEARN_MARIBEL, HIEDA_NO_AKYUU,
    HIJIRI_BYAKUREN, HIMEKAIDOU_HATATE, HINANAWI_TENSHI, HONG_MEILING, HOUJUU_NUE, IMAIZUMI_KAGEROU, INUBASHIRI_MOMIJI,
    IZAYOI_SAKUYA, KAENBYOU_RIN, KAMISHIRASAWA_KEINE, KAZAMI_YUUKA, KIRISAME_MARISA, KOAKUMA, KOCHIYA_SANAE,
    KOMEIJI_KOISHI, KOMEIJI_SATORI, KONPAKU_YOUMU, LILY_BLACK, LILY_WHITE, MARGATROID_ALICE, MEDICINE_MELANCHOLY,
    MONONOBE_NO_FUTO, MORIYA_SUWAKO, MOTOORI_KOSUZU, MURASA_MINAMITSU, MYSTIA_LORELEI, NAGAE_IKU, NAZRIN,
    ONOZUKA_KOMACHI, PATCHOULI_KNOWLEDGE, REIUJI_UTSUHO, RUMIA, SAIGYOUJI_YUYUKO, SCARLET_FLANDRE, SCARLET_REMILIA,
    SHAMEIMARU_AYA, SHIKI_EIKI_YAMAXANADU, TATARA_KOGASA, TORAMARU_SHOU, TOYOSATOMIMI_NO_MIKO, USAMI_RENKO,
    WAKASAGIHIME, WRIGGLE_NIGHTBUG, YAKUMO_RAN, YAKUMO_YUKARI, YASAKA_KANAKO
)

# Images from: https://safebooru.org/index.php?page=post&s=list&tags=2girls+pocky_kiss+touhou


TOUHOU_ACTION_POCKY_KISS = [
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/959700573081452564/akyuu-x-kosuzu-0000.png',
        freeze(HIEDA_NO_AKYUU, MOTOORI_KOSUZU),
    ),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/959700573706407946/aya-x-remilia-0000.png',
        freeze(SHAMEIMARU_AYA, SCARLET_REMILIA),
    ),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/959700574033567754/chen-x-orin-0000.png',
        freeze(CHEN, KAENBYOU_RIN),
    ),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/1055081320570699816/chen-x-ran-0000.png',
        freeze(CHEN, YAKUMO_RAN),
    ),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/1055081499562610698/chiruno-x-dai-0000.png',
        freeze(CHIRUNO, DAIYOUSEI),
    ),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/1055082269129330739/flandre-x-remilia-0000.png',
        freeze(SCARLET_FLANDRE, SCARLET_REMILIA),
    ),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/959700575291846686/hatate-x-aya-0000.png',
        freeze(HIMEKAIDOU_HATATE, SHAMEIMARU_AYA),
    ),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/959700575585439794/kagerou-x-remilia-0000.png',
        freeze(IMAIZUMI_KAGEROU, SCARLET_REMILIA),
    ),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/1055085629358227486/keine-x-mokou-0000.png',
        freeze(KAMISHIRASAWA_KEINE, FUJIWARA_NO_MOKOU),
    ),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/1055091597567602728/keine-x-mokou-0001.png',
        freeze(KAMISHIRASAWA_KEINE, FUJIWARA_NO_MOKOU),
    ),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/959701269969256488/koishi-x-flandre-0000.png',
        freeze(KOMEIJI_KOISHI, SCARLET_FLANDRE),
    ),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/1055091921791500288/koishi-x-flandre-0001.png',
        freeze(KOMEIJI_KOISHI, SCARLET_FLANDRE),
    ),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/959701270820716654/koishi-x-kokoro-0000.png',
        freeze(KOMEIJI_KOISHI, HATA_NO_KOKORO),
    ),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/959701271298859068/koishi-x-satori-0000.png',
        freeze(KOMEIJI_KOISHI, KOMEIJI_SATORI),
    ),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/1055092416882937866/koishi-x-satori-0001.png',
        freeze(KOMEIJI_KOISHI, KOMEIJI_SATORI),
    ),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/959701271852482570/kokoro-x-koishi-0000.png',
        freeze(HATA_NO_KOKORO, KOMEIJI_KOISHI),
    ),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/959701272150286366/lily-x-rumia-0000.png',
        freeze(LILY_WHITE, LILY_WHITE),
    ),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/959701272460673024/maribel-x-renko-0000.png',
        freeze(HEARN_MARIBEL, USAMI_RENKO),
    ),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/959701770509119498/marisa-x-alice-0000.png',
        freeze(KIRISAME_MARISA, MARGATROID_ALICE),
    ),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/959701770773331988/marisa-x-reimu-0000.png',
        freeze(KIRISAME_MARISA, HAKUREI_REIMU),
    ),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/1055074351440998421/marisa-x-reimu-0001.png',
        freeze(KIRISAME_MARISA, HAKUREI_REIMU),
    ),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/959701771377315880/marisa-x-reimu-0002.png',
        freeze(KIRISAME_MARISA, HAKUREI_REIMU),
    ),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/1055074988811624488/marisa-x-reimu-0003.png',
        freeze(KIRISAME_MARISA, HAKUREI_REIMU),
    ),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/959701771792547871/meiling-x-sakuya-0000.png',
        freeze(HONG_MEILING, IZAYOI_SAKUYA),
    ),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/959701772140691456/minamitsu-x-nue-0000.png',
        freeze(MURASA_MINAMITSU, HOUJUU_NUE),
    ),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/1055075516278911056/mokou-x-keine-0000.png',
        freeze(FUJIWARA_NO_MOKOU, KAMISHIRASAWA_KEINE),
    ),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/1055076323661467748/mystia-x-alice-0000.png',
        freeze(MYSTIA_LORELEI, RUMIA),
    ),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/959702866010968074/nazrin-x-shou-0000.png',
        freeze(NAZRIN, TORAMARU_SHOU),
    ),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/959702866392678440/nue-x-kogasa-0000.png',
        freeze(HOUJUU_NUE, TATARA_KOGASA),
    ),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/959702866635923496/patchouli-x-remilia-0000.png',
        freeze(PATCHOULI_KNOWLEDGE, SCARLET_REMILIA),
    ),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/959702867080515584/ran-x-chen-0000.png',
        freeze(YAKUMO_RAN, CHEN),
    ),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/959702867458019358/ran-x-chen-0001.png',
        freeze(YAKUMO_RAN, CHEN),
    ),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/1055078160040984616/reimu-x-marisa-0000.png',
        freeze(HAKUREI_REIMU, KIRISAME_MARISA),
    ),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/959703161893965854/remilia-x-flandre-0000.png',
        freeze(SCARLET_REMILIA, SCARLET_FLANDRE),
    ),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/959703162195963934/remilia-x-flandre-0001.png',
        freeze(SCARLET_REMILIA, SCARLET_FLANDRE),
    ),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/959703162795753482/renko-x-maribel-0000.png',
        freeze(USAMI_RENKO, HEARN_MARIBEL),
    ),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/1022179444732993536/renko-x-maribel-0001.png',
        freeze(USAMI_RENKO, HEARN_MARIBEL),
    ),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/959703163466825748/rumia-x-chiruno-0000.png',
        freeze(RUMIA, CHIRUNO),
    ),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/959703164125347860/sakuya-x-meiling-0000.png',
        freeze(IZAYOI_SAKUYA, HONG_MEILING),
    ),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/1055092931578572860/sakuya-x-koakuma-0000.png',
        freeze(IZAYOI_SAKUYA, KOAKUMA),
    ),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/959703496012222475/shou-x-nazrin-0000.png',
        freeze(TORAMARU_SHOU, NAZRIN),
    ),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/1055080350700818483/suwako-x-kanako-0000.png',
        freeze(MORIYA_SUWAKO, YASAKA_KANAKO),
    ),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/959703496830107658/suwako-x-sanae-0000.png',
        freeze(MORIYA_SUWAKO, KOCHIYA_SANAE),
    ),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/959703497190830080/tenshi-x-reimu-0000.png',
        freeze(HINANAWI_TENSHI, HAKUREI_REIMU),
    ),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/959703497501204521/wakasagihime-x-kagerou-0000.png',
        freeze(WAKASAGIHIME, IMAIZUMI_KAGEROU),
    ),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/1022178973666529290/youmo-x-patchouli-0000.png',
        freeze(KONPAKU_YOUMU, PATCHOULI_KNOWLEDGE),
    ),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/959703498113581056/youmu-x-sanae-0000.png',
        freeze(KONPAKU_YOUMU, KOCHIYA_SANAE),
    ),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/1055080654225805354/yuyuko-x-yukari-0000.png',
        freeze(SAIGYOUJI_YUYUKO, YAKUMO_YUKARI),
    ),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/959703499388616734/yuyuko-x-mystia-0000.png',
        freeze(SAIGYOUJI_YUYUKO, MYSTIA_LORELEI),
    ),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/1023272988881211502/koishi-flandre-pocky-kiss-0001.png',
        freeze(KOMEIJI_KOISHI, SCARLET_FLANDRE),
    ),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/1053001373916069989/satori-x-remilia-0000.png',
        freeze(KOMEIJI_SATORI, SCARLET_REMILIA),
    ),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/1055082358203756655/flandre-x-remilia-0001.png',
        freeze(SCARLET_FLANDRE, SCARLET_REMILIA),
    ),
]

# Images from: https://safebooru.org/index.php?page=post&s=list&tags=touhou+pocky+solo

TOUHOU_ACTION_POCKY_KISS_SELF = [
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/1055026936897863711/aya-0000.png',
        freeze(SHAMEIMARU_AYA),
    ),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/1055026937388613672/byakuren-0000.png',
        freeze(HIJIRI_BYAKUREN),
    ),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/1055026937820614666/byakuren-0001.png',
        freeze(HIJIRI_BYAKUREN),
    ),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/1055026938189709362/chiruno-0000.png',
        freeze(CHIRUNO),
    ),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/1055026938634309682/eiki-0000.png',
        freeze(SHIKI_EIKI_YAMAXANADU),
    ),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/1055027767604936744/flandre-0000.png',
        freeze(SCARLET_FLANDRE),
    ),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/1055027767890169917/flandre-0001.png',
        freeze(SCARLET_FLANDRE),
    ),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/1055028120400445490/flandre-0002.png',
        freeze(SCARLET_FLANDRE),
    ),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/1055027768397660230/flandre-0003.png',
        freeze(SCARLET_FLANDRE),
    ),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/1055027768687087637/flandre-0004.png',
        freeze(SCARLET_FLANDRE),
    ),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/1055027768951312434/flandre-0005.png',
        freeze(SCARLET_FLANDRE),
    ),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/1055027769261686824/flandre-0006.png',
        freeze(SCARLET_FLANDRE),
    ),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/1055028732072575026/futo-0000.png',
        freeze(MONONOBE_NO_FUTO),
    ),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/1055028732374552616/hatate-0000.png',
        freeze(MONONOBE_NO_FUTO),
    ),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/1055028732718481419/hatate-0001.png',
        freeze(MONONOBE_NO_FUTO),
    ),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/1055034840996642836/iku-0000.png',
        freeze(NAGAE_IKU),
    ),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/1055034841353175040/kagerou-0000.png',
        freeze(IMAIZUMI_KAGEROU),
    ),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/1055034841680322603/kagerou-0001.png',
        freeze(IMAIZUMI_KAGEROU),
    ),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/1055034841948749944/keine-0000.png',
        freeze(KAMISHIRASAWA_KEINE),
    ),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/1055034842275921970/kogasa-0000.png',
        freeze(TATARA_KOGASA),
    ),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/1055035484469985330/koishi-0000.png',
        freeze(KOMEIJI_KOISHI),
    ),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/1055035484914593912/koishi-0001.png',
        freeze(KOMEIJI_KOISHI),
    ),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/1055035485224980480/koishi-0002.png',
        freeze(KOMEIJI_KOISHI),
    ),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/1055035485854105600/kokoro-0000.png',
        freeze(HATA_NO_KOKORO),
    ),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/1055035486198050836/komachi-0000.png',
        freeze(ONOZUKA_KOMACHI),
    ),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/1055035486558748762/lily_black-0000.png',
        freeze(LILY_BLACK),
    ),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/1055035486936248350/lily_white-0000.png',
        freeze(LILY_WHITE),
    ),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/1055036556135628891/marisa-0000.png',
        freeze(KIRISAME_MARISA),
    ),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/1055036556555063337/marisa-0001.png',
        freeze(KIRISAME_MARISA),
    ),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/1055036556953530378/medicine_melancholy-0000.png',
        freeze(MEDICINE_MELANCHOLY),
    ),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/1055036557423280128/miko-0000.png',
        freeze(TOYOSATOMIMI_NO_MIKO),
    ),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/1055036557712691240/mokou-0000.png',
        freeze(FUJIWARA_NO_MOKOU),
    ),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/1055036558010495057/mokou-0001.png',
        freeze(FUJIWARA_NO_MOKOU),
    ),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/1055036558459273237/momiji-0000.png',
        freeze(INUBASHIRI_MOMIJI),
    ),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/1055036558828376074/momiji-0001.png',
        freeze(INUBASHIRI_MOMIJI),
    ),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/1055036558828376074/momiji-0001.png',
        freeze(INUBASHIRI_MOMIJI),
    ),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/1055036559159734322/momiji-0002.png',
        freeze(INUBASHIRI_MOMIJI),
    ),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/1055037378269556756/mystia-0000.png',
        freeze(MYSTIA_LORELEI),
    ),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/1055037378684780574/nazrin-0000.png',
        freeze(NAZRIN),
    ),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/1055037379011944508/nue-0000.png',
        freeze(HOUJUU_NUE),
    ),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/1055037379427184660/nue-0001.png',
        freeze(HOUJUU_NUE),
    ),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/1055037379720773642/okuu-0000.png',
        freeze(REIUJI_UTSUHO),
    ),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/1055037380026966117/orin-0000.png',
        freeze(KAENBYOU_RIN),
    ),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/1055037380412846150/orin-0001.png',
        freeze(KAENBYOU_RIN),
    ),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/1055038642420187187/patchouli-0000.png',
        freeze(PATCHOULI_KNOWLEDGE),
    ),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/1055038642776707132/patchouli-0001.png',
        freeze(PATCHOULI_KNOWLEDGE),
    ),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/1055038643112247346/patchouli-0002.png',
        freeze(PATCHOULI_KNOWLEDGE),
    ),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/1055038643552669736/ran-0000.png',
        freeze(YAKUMO_RAN),
    ),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/1055038643909169182/ran-0001.png',
        freeze(YAKUMO_RAN),
    ),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/1055038643909169182/ran-0001.png',
        freeze(HAKUREI_REIMU),
    ),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/1055038644643172422/reimu-0001.png',
        freeze(HAKUREI_REIMU),
    ),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/1055038644999704636/reimu-0002.png',
        freeze(HAKUREI_REIMU),
    ),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/1055039347352666142/remilia-0000.png',
        freeze(SCARLET_REMILIA),
    ),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/1055039348061524048/remilia-0001.png',
        freeze(SCARLET_REMILIA),
    ),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/1055039348061524048/remilia-0001.png',
        freeze(SCARLET_REMILIA),
    ),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/1055039348782944266/rumia-0000.png',
        freeze(RUMIA),
    ),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/1055039349135253504/sakuya-0000.png',
        freeze(IZAYOI_SAKUYA),
    ),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/1055039349495955506/sanae-0000.png',
        freeze(KOCHIYA_SANAE),
    ),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/1055039349844103240/sanae-0001.png',
        freeze(KOCHIYA_SANAE),
    ),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/1055039746637832304/satori-0000.png',
        freeze(KOMEIJI_SATORI),
    ),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/1055039746948223017/satori-0001.png',
        freeze(KOMEIJI_SATORI),
    ),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/1055039747246002286/suwako-0000.png',
        freeze(MORIYA_SUWAKO),
    ),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/1055039747543801866/tenshi-0000.png',
        freeze(HINANAWI_TENSHI),
    ),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/1055039747858386994/wriggle-0000.png',
        freeze(WRIGGLE_NIGHTBUG),
    ),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/1055039748156166164/wriggle-0001.png',
        freeze(WRIGGLE_NIGHTBUG),
    ),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/1055040218371211325/youmu-0000.png',
        freeze(KONPAKU_YOUMU),
    ),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/1055040218769653880/youmu-0001.png',
        freeze(KONPAKU_YOUMU),
    ),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/1055040219214258186/youmu-0002.png',
        freeze(KONPAKU_YOUMU),
    ),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/1055040219512061992/youmu-0003.png',
        freeze(KONPAKU_YOUMU),
    ),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/1055040219860172800/youmu-0004.png',
        freeze(KONPAKU_YOUMU),
    ),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/1055040555186393088/yukari-0000.png',
        freeze(YAKUMO_YUKARI),
    ),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/1055040555542917140/yuuka-0000.png',
        freeze(KAZAMI_YUUKA),
    ),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/1055040555903619132/yuuka-0001.png',
        freeze(KAZAMI_YUUKA),
    ),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/1055040556276908113/yuuka-0002.png',
        freeze(KAZAMI_YUUKA),
    ),
    ImageDetail(
        'https://cdn.discordapp.com/attachments/568837922288173058/1055040557006716928/yuyuko-0000.png',
        freeze(SAIGYOUJI_YUYUKO),
    ),
]
