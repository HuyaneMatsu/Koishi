__all__ = (
    'AKI_MINORIKO', 'AKI_SHIZUHA', 'AKIYO', 'ANABERAL_KANA', 'ASAKURA_RIKAKO', 'CHEN', 'CHIRIZUKA_UBAME', 'CHIRUNO',
    'CLOWNPIECE',
    'DAIYOUSEI', 'DOREMY_SWEET', 'EBISU_EIKA', 'ELIS', 'ELLEN', 'ELLY', 'ETERNITY_LARVA', 'FUJIWARA_NO_MOKOU',
    'FUTATSUIWA_MAMIZOU', 'GENGETSU', 'GENJII', 'GOLIATH', 'GOUTOKUJI_MIKE', 'HAKUREI_MIKO', 'HAKUREI_REIMU', 'HARURU',
    'HANIYASUSHIN_KEIKI',
    'HATA_NO_KOKORO', 'HEARN_MARIBEL', 'HECATIA_LAPISLAZULI', 'HEI_MEILING', 'HIEDA_NO_AKYUU', 'HIJIRI_BYAKUREN',
    'HIMEKAIDOU_HATATE', 'HIMEMUSHI_MOMOYO', 'HINANAWI_TENSHI', 'HONG_MEILING', 'HORIKAWA_RAIKO', 'HOSHIGUMA_YUUGI',
    'HOUJUU_CHIMI', 'HOUJUU_NUE', 'HOURAI', 'HOURAISAN_KAGUYA', 'IBARAKI_KASEN', 'IBUKI_SUIKA', 'IIZUNAMARU_MEGUMU',
    'IMAIZUMI_KAGEROU', 'INABA_TEWI', 'INUBASHIRI_MOMIJI', 'IWANAGA_ARIYA',
    'IZAYOI_SAKUYA', 'JACKET', 'JOUTOUGUU_MAYUMI', 'JUNKO',
    'KAENBYOU_RIN', 'KAGIYAMA_HINA', 'KAKU_SEIGA', 'KAMISHIRASAWA_KEINE', 'KASODANI_KYOUKO', 'KAWASHIRO_NITORI',
    'KAZAMI_YUUKA', 'KICCHOU_YACHIE', 'KIJIN_SEIJA', 'KIKURI', 'KIRISAME_MARISA', 'KISHIN_SAGUME', 'KISUME',
    'KITASHIRAKAWA_CHIYURI', 'KOAKUMA', 'KOCHIYA_SANAE', 'KOKUU_HARUTO', 'KOMAKUSA_SANNYO', 'KOMANO_AUNN',
    'KOMEIJI_KOISHI', 'KOMEIJI_SATORI', 'KONNGARA', 'KONPAKU_YOUKI', 'KONPAKU_YOUMU', 'KUDAMAKI_TSUKASA',
    'KUMOI_ICHIRIN', 'KURODANI_YAMAME', 'KUROKOMA_SAKI', 'KURUMI', 'LABEL', 'LETTY_WHITEROCK', 'LORELEI_MYSTIA',
    'LILY_BLACK',
    'LILY_WHITE', 'LOUISE', 'LUNA_CHILD', 'MAI', 'MARGATROID_ALICE', 'MATARA_OKINA', 'MATENSHI', 'MEDICINE_MELANCHOLY',
    'MEIRA', 'MICHIGAMI_NAREKO', 'MIMA', 'MISHAGUJI', 'MITSUGASHIRA_ENOKO', 'MIYAKO_YOSHIKA', 'MIZUHASHI_PARSEE',
    'MONONOBE_NO_FUTO',
    'MORICHIKA_RINNOSUKE', 'MORIYA_SUWAKO', 'MOTOORI_KOSUZU', 'MUGETSU', 'MURASA_MINAMITSU',
    'NAGAE_IKU', 'NAZRIN', 'NIPPAKU_ZANMU', 'NISHIDA_SATONO', 'NIWATARI_KUTAKA', 'NOROIKO', 'OKAZAKI_YUMEMI',
    'OKUNODA_MIYOI', 'ONOZUKA_KOMACHI', 'ORANGE', 'PATCHOULI_KNOWLEDGE', 'PRISMRIVER_LAYLA', 'PRISMRIVER_LUNASA',
    'PRISMRIVER_LYRICA', 'PRISMRIVER_MERLIN', 'REISEN_UDONGEIN_INABA', 'REIUJI_UTSUHO', 'RENGETEKI', 'RIKA', 'RINGO',
    'RUMIA', 'SAIGYOUJI_YUYUKO', 'SAKATA_NEMUNO', 'SARA', 'SARIEL', 'SATOWA', 'SATSUKI_RIN', 'SCARLET_FLANDRE',
    'SCARLET_REMILIA', 'SEIRAN', 'SEKIBANKI', 'SHAMEIMARU_AYA', 'SHANGHAI', 'SHIKI_EIKI_YAMAXANADU', 'SHINGYOKU',
    'SHINKI', 'SOGA_NO_TOJIKO', 'SOKRATES', 'SON_BITEN', 'STAR_SAPPHIRE', 'SUKUNA_SHINMYOUMARU', 'SUNNY_MILK',
    'TAMATSUKURI_MISUMARU', 'TATARA_KOGASA', 'TEIREIDA_MAI', 'TENKAJIN_CHIYARI', 'TENKYUU_CHIMATA', 'TOKIKO', 'TOMOMI',
    'TORAMARU_SHOU', 'TOUTETSU_YUUMA', 'TOYOSATOMIMI_NO_MIKO', 'TSUBAME', 'TSUKUMO_BENBEN', 'TSUKUMO_YATSUHASHI',
    'UNNAMED_EXOTIC_GIRL_20000_HIT_GIRL', 'UNNAMED_EXOTIC_GIRL_CLEANING_MAID', 'USAMI_RENKO', 'USAMI_SUMIREKO',
    'USHIZAKI_URUMI', 'VIVIT', 'WAKASAGIHIME', 'WATARI_NINA', 'WATATSUKI_NO_TOYOHIME', 'WATATSUKI_NO_YORIHIME',
    'WAYOUSEI',
    'WRIGGLE_NIGHTBUG', 'YAGOKORO_EIRIN', 'YAKUMO_RAN', 'YAKUMO_YUKARI', 'YAMASHIRO_TAKANE', 'YASAKA_KANAKO',
    'YATADERA_NARUMI', 'YOMOTSU_HISAMI', 'YORIGAMI_JOON', 'YORIGAMI_SHION', 'YORUMI', 'YUIMAN_ASAMA',
    'YUKI', 'YUMEKO', 'YUUGEN_MAGAN'
)

from .character import TouhouCharacter


AKI_MINORIKO = TouhouCharacter(
    'aki_minoriko',
    'Aki Minoriko',
    (
        '秋 穣子',
        'Minoriko',
    ),
)

AKI_SHIZUHA = TouhouCharacter(
    'aki_shizuha',
    'Aki Shizuha',
    (
        '秋 静葉',
        'Shizuha',
    ),
)

AKIYO = TouhouCharacter(
    'akiyo',
    'Akiyo',
    (
        'Blonde Shrine Maiden from a Future Era',
    ),
)

ANABERAL_KANA = TouhouCharacter(
    'anaberal_kana',
    'Anaberal Kana',
    (
        'アナベラル カナ',
        'Kana Anaberal',
        'Kana',
    )
)

ASAKURA_RIKAKO = TouhouCharacter(
    'asakura_rikako',
    'Asakura Rikako',
    (
        '朝倉 理香子',
        'Rikako Asakura',
    ),
)

AYANA = TouhouCharacter(
    'ayana',
    'Ayana',
    (
        'あやな',
    ),
)

CHEN = TouhouCharacter(
    'chen',
    'Chen',
    (
        '橙',
    ),
)

CHIRIZUKA_UBAME = TouhouCharacter(
    'chirizuka_ubame',
    'Chirizuka Ubame',
    (
        '塵塚 ウバメ',
        'Ubame',
        'Ubame Chirizuka',
    ),
)

CHIRUNO = TouhouCharacter(
    'chiruno',
    'Chiruno',
    (
        'チルノ',
        'Cirno',
    ),
)

DAIYOUSEI = TouhouCharacter(
    'daiyousei',
    'Daiyousei',
    (
        '大妖精',
    ),
)

DOREMY_SWEET = TouhouCharacter(
    'doremy_sweet',
    'Doremy Sweet',
    (
        'ドレミー スイート',
        'Doremy',
        'Doremii Suiito',
    ),
)

EBISU_EIKA = TouhouCharacter(
    'ebisu_eika',
    'Ebisu Eika',
    (
        '戎 瓔花',
        'Eika Ebisu',
    ),
)

ELIS = TouhouCharacter(
    'elis',
    'Elis',
    (
        'エリス',
    ),
)

ELLEN = TouhouCharacter(
    'ellen',
    'Ellen',
    (
        'エレン',
        'Eren',
    )
)

ELLY = TouhouCharacter(
    'elly',
    'Elly',
    (
        'エリー',
        'Erii',
        'Elly',
    ),
)

ETERNITY_LARVA = TouhouCharacter(
    'eternity_larva',
    'Eternity Larva',
    (
        'エタニティラルバ',
        'Eternity',
        'Larva',
        'Etanitiraruba',
    ),
)

FUJIWARA_NO_MOKOU = TouhouCharacter(
    'fujiwara_no_mokou',
    'Fujiwara no Mokou',
    (
        '藤原 妹紅',
        'Mokou',
    ),
)

FUTATSUIWA_MAMIZOU = TouhouCharacter(
    'futatsuiwa_mamizou',
    'Futatsuiwa Mamizou',
    (
        '二ッ岩 マミゾウ',
        'Mamizou',
        'Mamizou Futatsuiwa',
    ),
)

GENGETSU = TouhouCharacter(
    'gengetsu',
    'Gengetsu',
    (
        '幻月',
    ),
)

GENJII = TouhouCharacter(
    'genjii',
    'Genjii',
    (
        '玄爺',
        'げんじい',
    ),
)

GOLIATH = TouhouCharacter(
    'goliath',
    'Goliath',
    (
        'Goliath doll',
        'ゴリアテ人形',
        'ごりあてにんぎょう',
        'Goriate Ningyou',
    ),
)

GOUTOKUJI_MIKE = TouhouCharacter(
    'goutokuji_mike',
    'Goutokuji Mike',
    (
        'Mike Goutokuji',
        '豪徳寺 ミケ',
        'ミケ',
    ),
)

HEARN_MARIBEL = TouhouCharacter(
    'hearn_maribel',
    'Hearn Maribel',
    (
        'マエリベリー ハーン',
        'Maribel',
        'Maeriberii',
        'Haan Maeriberii',
        'Maribel Hearn',
    ),
)

HANIYASUSHIN_KEIKI = TouhouCharacter(
    'haniyasushin_keiki',
    'Haniyasushin Keiki',
    (
        '埴安神 袿姫',
        'Keiki',
        'Keiki Haniyasushin',
    ),
)

HAKUREI_MIKO = TouhouCharacter(
    'hakurei_miko',
    'Hakurei Miko',
    (
        'Sendai Hakurei no Miko',
        '先代博麗の巫女',
        '博麗の巫女',
        'Sendai Miko',
        '先代巫女',
    )
)

HAKUREI_REIMU = TouhouCharacter(
    'hakurei_reimu',
    'Hakurei Reimu',
    (
        '博麗 霊夢',
        'Reimu',
        'Reimu Hakurei',
    ),
)

HARURU = TouhouCharacter(
    'haruru',
    'Haruru',
    (
        'Blonde Oekaki Girl',
    )
)

HATA_NO_KOKORO = TouhouCharacter(
    'hata_no_kokoro',
    'Hata no Kokoro',
    (
        '秦 こころ',
        'Kokoro',
        'こころ',
        'Hata',
    ),
)

HECATIA_LAPISLAZULI = TouhouCharacter(
    'hecatia_lapislazuli',
    'Hecatia Lapislazuli',
    (
        'ヘカーティア ラピスラズリ',
        'Hecatia',
        'Hekaatia',
        'Hekaatia Rapisurazuri',
    ),
)

HEI_MEILING = TouhouCharacter(
    'hei_meiling',
    'Hei Meiling',
    (
        'Hei Meirin',
        'Meiling Hei',
    ),
)

HIEDA_NO_AKYUU = TouhouCharacter(
    'hieda_no_akyuu',
    'Hieda no Akyuu',
    (
        '稗田 阿求',
        'Akyuu',
    ),
)

HIJIRI_BYAKUREN = TouhouCharacter(
    'hijiri_byakuren',
    'Hijiri Byakuren',
    (
        '聖 白蓮',
        'Byakuren',
        'Hijiri',
        'Byakuren Hijiri',
    ),
)

HIMEKAIDOU_HATATE = TouhouCharacter(
    'himekaidou_hatate',
    'Himekaidou Hatate',
    (
        '姫海棠 はたて',
        'Hatate',
        'Hatate Himekaidou',
    ),
)

HIMEMUSHI_MOMOYO = TouhouCharacter(
    'himemushi_momoyo',
    'Himemushi Momoyo',
    (
        '姫虫 百々世',
        'Momoyo Himemushi',
        'Momoyo',
    ),
)

HINANAWI_TENSHI = TouhouCharacter(
    'hinanawi_tenshi',
    'Hinanawi Tenshi',
    (
        '比那名居 天子',
        'Tenshi',
        'Tenshi Hinanawi',
    ),
)

HONG_MEILING = TouhouCharacter(
    'hong_meiling',
    'Hong Meiling',
    (
        '紅 美鈴',
        'Meiling',
        'Meirin',
        'Hon Meirin',
        'Meiling Hong',
    ),
)

HORIKAWA_RAIKO = TouhouCharacter(
    'horikawa_raiko',
    'Horikawa Raiko',
    (
        '堀川 雷鼓',
        'Raiko',
        'Raiko Horikawa',
    ),
)

HOSHIGUMA_YUUGI = TouhouCharacter(
    'hoshiguma_yuugi',
    'Hoshiguma Yuugi',
    (
        '星熊 勇儀',
        'Yuugi',
        'Yuugi Hoshiguma',
    ),
)

HOUJUU_CHIMI = TouhouCharacter(
    'houjuu_chimi',
    'Houjuu Chimi',
    (
        '封獣 チミ',
        'Chimi',
        'Chimi Houjuu',
    ),
)

HOUJUU_NUE = TouhouCharacter(
    'houjuu_nue',
    'Houjuu Nue',
    (
        '封獣 ぬえ',
        'Nue',
        'Nue Houjuu',
    ),
)

HOURAI = TouhouCharacter(
    'hourai',
    'Hourai',
    (
        'Hourai doll',
        '蓬莱',
        'ほうらい',
    ),
)

HOURAISAN_KAGUYA = TouhouCharacter(
    'houraisan_kaguya',
    'Houraisan Kaguya',
    (
        '蓬莱山 輝夜',
        'Kaguya',
        'Kaguya Houraisan',
    ),
)

LABEL = TouhouCharacter(
    'label',
    'Label',
    (
        'Label Girl',
    ),
)

LILY_BLACK = TouhouCharacter(
    'lily_black',
    'Lily black',
    (),
)

LILY_WHITE = TouhouCharacter(
    'lily_white',
    'Lily White',
    (
        'リリーホワイト',
        'Lily',
        'Ririi',
        'Ririi Howaito',
    ),
)

LETTY_WHITEROCK = TouhouCharacter(
    'letty_whiterock',
    'Letty Whiterock',
    (
        'レティ ホワイトロック',
        'Letty',
        'Reti Howaitorokku',
    ),
)

LORELEI_MYSTIA = TouhouCharacter(
    'lorelei_mystia',
    'Lorelei Mystia',
    (
        'ミスティア ローレライ',
        'Mystia',
        'Misutia Roorerai',
        'ローレライ ミスティア',
        'Roorerai Misutia',
    ),
)

LOUISE = TouhouCharacter(
    'louise',
    'Louise',
    (
        'ルイズ',
        'Ruizu',
    ),
)

LUNA_CHILD = TouhouCharacter(
    'luna_child',
    'Luna Child',
    (
        'ルナチャイルド',
        'Chairudo Runa',
        'Luna',
        'Runa',
    ),
)

IBARAKI_KASEN = TouhouCharacter(
    'ibaraki_kasen',
    'Ibaraki Kasen',
    (
        '茨木 華扇',
        'Kasen',
        'Kasen Ibaraki',
    ),
)

IBUKI_SUIKA = TouhouCharacter(
    'ibuki_suika',
    'Ibuki Suika',
    (
        '伊吹 萃香',
        'Suika',
        'Suika Ibuki',
    ),
)

IIZUNAMARU_MEGUMU = TouhouCharacter(
    'iizunamaru_megumu',
    'Iizunamaru Megumu',
    (
        '飯綱丸 龍',
        'Megumu Iizunamaru',
        'Megumu',
    ),
)

IMAIZUMI_KAGEROU = TouhouCharacter(
    'imaizumi_kagerou',
    'Imaizumi Kagerou',
    (
        '今泉 影狼',
        'Kagerou',
        'Kagerou Imaizumi',
    ),
)

INABA_TEWI = TouhouCharacter(
    'inaba_tewi',
    'Inaba Tewi',
    (
        '因幡 てゐ',
        'Tewi',
        'Tewi Inaba',
    ),
)

INUBASHIRI_MOMIJI = TouhouCharacter(
    'inubashiri_momiji',
    'Inubashiri Momiji',
    (
        '犬走 椛',
        'Momiji',
        'Momiji Inubashiri',
    ),
)

IWANAGA_ARIYA = TouhouCharacter(
    'iwanaga_ariya',
    'Iwanaga Ariya',
    (
        '磐永 阿梨夜',
        '阿梨夜',
        'Ariya',
        'Ariya Iwanaga',
    ),
)

IZAYOI_SAKUYA = TouhouCharacter(
    'izayoi_sakuya',
    'Izayoi Sakuya',
    (
        '十六夜 咲夜',
        'Sakuya',
        'Sakuya Izayoi',
        '咲夜',
    ),
)

JACKET = TouhouCharacter(
    'jacket',
    'Jacket',
    (
        'Jacket girl',
    ),
)

JOUTOUGUU_MAYUMI = TouhouCharacter(
    'joutouguu_mayumi',
    'Joutouguu Mayumi',
    (
        '杖刀偶 磨弓',
        'Mayumi',
        'Mayumi Joutouguu',
    ),
)

JUNKO = TouhouCharacter(
    'junko',
    'Junko',
    (
        '純狐',
        'Junko',
    ),
)

KAENBYOU_RIN = TouhouCharacter(
    'kaenbyou_rin',
    'Kaenbyou Rin',
    (
        '火焔猫 燐',
        'Orin',
        'Rin',
        'Rin Kaenbyou',
    ),
)

KAGIYAMA_HINA = TouhouCharacter(
    'kagiyama_hina',
    'Kagiyama Hina',
    (
        '鍵山 雛',
        'Hina',
        'Hina Kagiyama',
    ),
)

KAKU_SEIGA = TouhouCharacter(
    'kaku_seiga',
    'Kaku Seiga',
    (
        '霍 青娥,',
        'Seiga',
        'Seiga Kaku',
    ),
)

KAMISHIRASAWA_KEINE = TouhouCharacter(
    'kamishirasawa_keine',
    'Kamishirasawa Keine',
    (
        '上白沢 慧音',
        'Keine',
        'Keine Kamishirasawa',
    ),
)

KASODANI_KYOUKO = TouhouCharacter(
    'kasodani_kyouko',
    'Kasodani Kyouko',
    (
        '幽谷 響子',
        'Kyouko',
        'Kyouko Kasodani',
    ),
)

KAWASHIRO_NITORI = TouhouCharacter(
    'kawashiro_nitori',
    'Kawashiro Nitori',
    (
        '河城 にとり',
        'Nitori',
        'Nitori Kawashiro',
        'Phoenix Kappashiro',
    ),
)

KAZAMI_YUUKA = TouhouCharacter(
    'kazami_yuuka',
    'Kazami Yuuka',
    (
        '風見 幽香',
        'Yuuka',
        'Yuuka Kazami',
    ),
)

KICCHOU_YACHIE = TouhouCharacter(
    'kicchou_yachie',
    'Kicchou Yachie',
    (
        '吉弔 八千慧',
        'Yachie',
        'Yachie Kicchou',
    ),
)


KIKURI = TouhouCharacter(
    'kikuri',
    'Kikuri',
    (
        '菊理',
        'きくり',
    )
)

KIJIN_SEIJA = TouhouCharacter(
    'kijin_seija',
    'Kijin Seija',
    (
        '鬼人 正邪',
        'Seija Kijin',
        'Seija',
    ),
)

KIRISAME_MARISA = TouhouCharacter(
    'kirisame_marisa',
    'Kirisame Marisa',
    (
        '霧雨 魔理沙',
        'Marisa',
        'Marisa Kirisame',
    ),
)

KISHIN_SAGUME = TouhouCharacter(
    'kishin_sagume',
    'Kishin Sagume',
    (
        '稀神 サグメ',
        'Sagume',
        'Sagume Kishin',
    ),
)

KISUME = TouhouCharacter(
    'kisume',
    'Kisume',
    (
        'キスメ',
    ),
)

KITASHIRAKAWA_CHIYURI = TouhouCharacter(
    'kitashirakawa_chiyuri',
    'Kitashirakawa Chiyuri',
    (
        '北白河 ちゆり',
        'Chiyuri Kitashirakawa',
    ),
)

KOAKUMA = TouhouCharacter(
    'koakuma',
    'Koakuma',
    (
        '小悪魔',
        'Koakuma',
    ),
)

KOCHIYA_SANAE = TouhouCharacter(
    'kochiya_sanae',
    'Kochiya Sanae',
    (
        '東風谷 早苗',
        'Sanae',
        'Sanae Kochiya',
    ),
)

KOMANO_AUNN = TouhouCharacter(
    'komano_aunn',
    'Komano Aunn',
    (
        '高麗野 あうん',
        'Aunn',
        'Aun',
        'Aunn Komano',
    ),
)


KOMAKUSA_SANNYO = TouhouCharacter(
    'komakusa_sannyo',
    'Komakusa Sannyo',
    (
        '駒草 山如',
        'Sannyo',
        'Sannyo Komakusa',
    ),
)


KOMEIJI_KOISHI = TouhouCharacter(
    'komeiji_koishi',
    'Komeiji Koishi',
    (
        '古明地 こいし',
        'Koishi',
        'Koishi Komeiji',
    ),
)

KOMEIJI_SATORI = TouhouCharacter(
    'komeiji_satori',
    'Komeiji Satori',
    (
        '古明地 さとり',
        'Satori',
        'Satori Komeiji',
    ),
)

KOKUU_HARUTO = TouhouCharacter(
    'kokuu_haruto',
    'Kokuu Haruto',
    (
        'Haruto Kokuu',
    ),
)

KONNGARA = TouhouCharacter(
    'konngara',
    'Konngara',
    (
        '矜羯羅',
        'Kimkara',
        'こんがら',
    ),
)

KONPAKU_YOUKI = TouhouCharacter(
    'konpaku_youki',
    'Konpaku Youki',
    (
        'こんぱく ようき',
        '魂魄 妖忌',
        'Youki Konpaku',
    ),
)

KONPAKU_YOUMU = TouhouCharacter(
    'konpaku_youmu',
    'Konpaku Youmu',
    (
        'こんぱく ようむ',
        '魂魄 妖夢',
        'Youmu',
        'Youmu Konpaku',
    ),
)

KOTOHIME = TouhouCharacter(
    'kotohime',
    'Kotohime',
    (
        '小兎姫',
    ),
)

KUDAMAKI_TSUKASA = TouhouCharacter(
    'kudamaki_tsukasa',
    'Kudamaki Tsukasa',
    (
        '菅牧 典',
        'Tsukasa Kudamaki',
        'Tsukasa',
    ),
)

KUMOI_ICHIRIN = TouhouCharacter(
    'kumoi_ichirin',
    'Kumoi Ichirin',
    (
        '雲居 一輪',
        'Ichirin Kumoi',
        'Ichirin',
    ),
)

KURUMI = TouhouCharacter(
    'kurumi',
    'Kurumi',
    (
        'くるみ',
    ),
)

CLOWNPIECE = TouhouCharacter(
    'clownpiece',
    'Clownpiece',
    (
        'クラウンピース',
        'Kuraunpiisu',
    ),
)

KURODANI_YAMAME = TouhouCharacter(
    'kurodani_yamame',
    'Kurodani Yamame',
    (
        '黒谷 ヤマメ',
        'Yamame Kurodani',
    ),
)

KUROKOMA_SAKI = TouhouCharacter(
    'kurokoma_saki',
    'Kurokoma Saki',
    (
        '驪駒 早鬼',
        'Saki',
        'Saki Kurokoma',
    ),
)

MAI = TouhouCharacter(
    'mai',
    'Mai',
    (
        'マイ',
    ),
)

MARGATROID_ALICE = TouhouCharacter(
    'margatroid_alice',
    'Margatroid Alice',
    (
        'アリス マーガトロイド',
        'Arisu',
        'Alice',
        'Maagatoroido Arisu',
        'Alice Margatroid',
    ),
)

MATARA_OKINA = TouhouCharacter(
    'matara_okina',
    'Matara Okina',
    (
        '摩多羅 隠岐奈',
        'Okina',
        'Okina Matara',
    ),
)

MATENSHI = TouhouCharacter(
    'matenshi',
    'Matenshi',
    (
        'まてんし',
    )
)

MEDICINE_MELANCHOLY = TouhouCharacter(
    'medicine_melancholy',
    'Medicine Melancholy',
    (
        'メディスン メランコリー',
        'Merankorii Medisun',
    ),
)

MEIRA = TouhouCharacter(
    'meira',
    'Meira',
    (
        '明羅',
        'めいら',
    ),
)

MICHIGAMI_NAREKO = TouhouCharacter(
    'michigami_nareko',
    'Michigami Nareko',
    (
        '道神 馴子',
        'Nareko',
        'Nareko Michigami',
    ),
)

MIMA = TouhouCharacter(
    'mima',
    'Mima',
    (
        '魅魔',
        'Mima',
    ),
)

MISHAGUJI = TouhouCharacter(
    'mishaguji',
    'Mishaguji',
    (
        'ミシャグジ',
    ),
)

MITSUGASHIRA_ENOKO = TouhouCharacter(
    'mitsugashira_enoko',
    'Mitsugashira Enoko',
    (
        '三頭 慧ノ子',
        'Enoko Mitsugashira',
        'Enoko',
    ),
)

MIYADEGUCHI_MIZUCHI = TouhouCharacter(
    'miyadeguchi_mizuchi',
    'Miyadeguchi Mizuchi',
    (
        'みやでぐち みずち',
        '宮出口 瑞霊',
        'Mizuchi Miyadeguchi',
    ),
)

MIYAKO_YOSHIKA = TouhouCharacter(
    'miyako_yoshika',
    'Miyako Yoshika',
    (
        '宮古 芳香',
        'Yoshika',
        'Yoshika Miyako',
    ),
)

MIZUHASHI_PARSEE = TouhouCharacter(
    'mizuhashi_parsee',
    'Mizuhashi Parsee',
    (
        '水橋 パルスィ',
        'Parsee',
        'Mizuhashi Parusi',
        'Parsee Mizuhashi',
    ),
)

MONONOBE_NO_FUTO = TouhouCharacter(
    'mononobe_no_futo',
    'Mononobe no Futo',
    (
        '物部 布都',
        'Futo',
    ),
)

MORICHIKA_RINNOSUKE = TouhouCharacter(
    'morichika_rinnosuke',
    'Morichika Rinnosuke',
    (
        '森近 霖之助',
        'Rinnosuke',
        'Rinnosuke Morichika',
    ),
)

MORIYA_SUWAKO = TouhouCharacter(
    'moriya_suwako',
    'Moriya Suwako',
    (
        '洩矢 諏訪子',
        'Suwako Moriya',
        'Suwako',
    ),
)

MOTOORI_KOSUZU = TouhouCharacter(
    'motoori_kosuzu',
    'Motoori Kosuzu',
    (
        '本居 小鈴',
        'Kosuzu',
        'Kosuzu Motoori',
    ),
)

MUGETSU = TouhouCharacter(
    'mugetsu',
    'Mugetsu',
    (
        '夢月',
    )
)

MURASA_MINAMITSU = TouhouCharacter(
    'murasa_minamitsu',
    'Murasa Minamitsu',
    (
        '村紗 水蜜',
        'Murasa',
        'Minamitsu Murasa',
    ),
)

NAGAE_IKU = TouhouCharacter(
    'nagae_iku',
    'Nagae Iku',
    (
        '永江 衣玖',
        'Iku',
        'Iku Nagae',
    ),
)

NAZRIN = TouhouCharacter(
    'nazrin',
    'Nazrin',
    (
        'ナズーリン',
        'Nazuurin',
    ),
)

NIPPAKU_ZANMU = TouhouCharacter(
    'nippaku_zanmu',
    'Nippaku Zanmu',
    (
        '日白 残無',
        'Zanmu Nippaku',
        'Zanmu',
    ),
)

NISHIDA_SATONO = TouhouCharacter(
    'nishida_satono',
    'Nishida Satono',
    (
        '爾子田 里乃',
        'Satono',
        'Satono Nishida',
    ),
)

NIWATARI_KUTAKA = TouhouCharacter(
    'niwatari_kutaka',
    'Niwatari Kutaka',
    (
        '庭渡 久侘歌',
        'Kutaka',
        'Kutaka Niwatari',
    ),
)

NOROIKO = TouhouCharacter(
    'noroiko',
    'Noroiko',
    (
        'のろいこ',
    )
)

OKAZAKI_YUMEMI = TouhouCharacter(
    'okazaki_yumemi',
    'Okazaki Yumemi',
    (
        'おかざき ゆめみ',
        '岡崎 夢美',
        'Yumemi Okazaki',
    ),
)

OKUNODA_MIYOI = TouhouCharacter(
    'okunoda_miyoi',
    'Okunoda Miyoi',
    (
        '奥野田 美宵',
        'Miyoi',
        'Miyoi Okunoda',
    ),
)

ONOZUKA_KOMACHI = TouhouCharacter(
    'onozuka_komachi',
    'Onozuka Komachi',
    (
        '小野塚 小町',
        'Komachi',
        'Komachi Onozuka',
    ),
)

ORANGE = TouhouCharacter(
    'orange',
    'Orange',
    (
        'オレンジ',
        'Orenjii',
    ),
)

PATCHOULI_KNOWLEDGE = TouhouCharacter(
    'patchouli_knowledge',
    'Patchouli Knowledge',
    (
        'パチュリー ノーレッジ',
        'Patchouli',
        'Pachurii Noorejji',
    ),
)

PRISMRIVER_LUNASA = TouhouCharacter(
    'prismriver_lunasa',
    'Prismriver Lunasa',
    (
        'プリズムリバー ルナサ',
        'Lunasa',
        'Lunasa Prismriver',
        'Purizumuribaa Runasa',
    ),
)

PRISMRIVER_LYRICA = TouhouCharacter(
    'prismriver_lyrica',
    'Prismriver Lyrica',
    (
        'プリズムリバー リリカ',
        'Lyrica',
        'Lyrica Prismriver',
        'Purizumuribaa Ririka',
    ),
)

PRISMRIVER_MERLIN = TouhouCharacter(
    'prismriver_merlin',
    'Prismriver Merlin',
    (
        'プリズムリバ メルラン',
        'Merlin',
        'Merlin Prismriver',
        'Purizumuribaa Meruran',
    ),
)

PRISMRIVER_LAYLA = TouhouCharacter(
    'prismriver_layla',
    'Prismriver Layla',
    (
        'プリズムリバ レイラ',
        'Layla',
        'Layla Prismriver',
        'Purizumuribaa Reira',
    ),
)


REISEN_UDONGEIN_INABA = TouhouCharacter(
    'reisen_udongein_inaba',
    'Reisen Udongein Inaba',
    (
        '鈴仙 優曇華院 イナバ',
        'Reisen',
    ),
)

REIUJI_UTSUHO = TouhouCharacter(
    'reiuji_utsuho',
    'Reiuji Utsuho',
    (
        '霊烏路 空',
        'Okuu',
        'Utsuho Reiuji',
    ),
)

RENGETEKI = TouhouCharacter(
    'rengeteki',
    'Rengeteki',
    (
        'Hikariko',
        'れんげてき',
    ),
)

RIKA = TouhouCharacter(
    'rika',
    'Rika',
    (
        '里香',
        'りか',
    ),
)

RINGO = TouhouCharacter(
    'ringo',
    'Ringo',
    (
        '鈴瑚',
        'Ringo',
    ),
)

RUUKOTO = TouhouCharacter(
    'ruukoto',
    'Ruukoto',
    (
        'るーこと',
    ),
)

RUMIA = TouhouCharacter(
    'rumia',
    'Rumia',
    (
        'ルーミア',
        'Ruumia',
    ),
)

SATSUKI_RIN = TouhouCharacter(
    'satsuki_rin',
    'Satsuki Rin',
    (
        '冴月麟',
        'Satsuki',
        'Rin Satsuki',
    ),
)


SAIGYOUJI_YUYUKO = TouhouCharacter(
    'saigyouji_yuyuko',
    'Saigyouji Yuyuko',
    (
        '西行寺 幽々子',
        'Yuyuko',
        'Yuyuko Saigyouji',
    ),
)

SAKATA_NEMUNO = TouhouCharacter(
    'sakata_nemuno',
    'Sakata Nemuno',
    (
        '坂田 ネムノ',
        'Nemuno',
        'Nemuno Sakata',
    ),
)

SARA = TouhouCharacter(
    'sara',
    'Sara',
    (
        'サラ',
    ),
)

SARIEL = TouhouCharacter(
    'sariel',
    'Sariel',
    (
        'サリエル',
    ),
)

SATOWA = TouhouCharacter(
    'satowa',
    'Satowa',
    (
        'Girl who trained on Mount Haku',
    ),
)

SCARLET_FLANDRE = TouhouCharacter(
    'scarlet_flandre',
    'Scarlet Flandre',
    (
        'スカーレット フランドール',
        'Flandre',
        'Flandre Scarlet',
        'Flan',
        'Sukaaretto Furandooru',
    ),
)

SCARLET_REMILIA = TouhouCharacter(
    'scarlet_remilia',
    'Scarlet Remilia',
    (
        'スカーレット レミリア',
        'Remilia',
        'Remilia Scarlet',
        'Sukaaretto Remiria',
        'Remi',
    ),
)

SEIRAN = TouhouCharacter(
    'seiran',
    'Seiran',
    (
        '清蘭',
        'Seiran',
    ),
)

SEKIBANKI = TouhouCharacter(
    'sekibanki',
    'Sekibanki',
    (
        '赤蛮奇',
        'Sekibanki',
    ),
)

SHAMEIMARU_AYA = TouhouCharacter(
    'shameimaru_aya',
    'Shameimaru Aya',
    (
        '射命丸 文',
        'Aya',
        'Aya Shameimaru',
    ),
)

SHANGHAI = TouhouCharacter(
    'shanghai',
    'Shanghai',
    (
        'Shanghai doll',
        'しゃんはい',
        '上海',
    ),
)

SHIKI_EIKI_YAMAXANADU = TouhouCharacter(
    'shiki_eiki_yamaxanadu',
    'Shiki Eiki Yamaxanadu',
    (
        '四季映姫 ヤマザナドゥ',
        'Eiki',
        'Shiki Eiki Yamazanadu',
        'Eiki Shiki, Yamaxanadu',
    ),
)

SHINGYOKU = TouhouCharacter(
    'shingyoku',
    'Shingyoku',
    (
        'しんぎょく',
    ),
)

SHINKI = TouhouCharacter(
    'shinki',
    'Shinki',
    (
        '神綺',
    ),
)

SOGA_NO_TOJIKO = TouhouCharacter(
    'soga_no_tojiko',
    'Soga no Tojiko',
    (
        '蘇我 屠自古',
        'Soga',
        'Tojiko',
    ),
)

SOKRATES = TouhouCharacter(
    'sokrates',
    'Sokrates',
    (
        'ソクラテス',
        'Sokuratesu',
    )
)

SON_BITEN = TouhouCharacter(
    'son_biten',
    'Son Biten',
    (
        '孫 美天',
        'Biten Son',
        'Biten',
    )
)

STAR_SAPPHIRE = TouhouCharacter(
    'star_sapphire',
    'Star Sapphire',
    (
        'スターサファイア',
        'Safaia Sutaa',
    ),
)

SUKUNA_SHINMYOUMARU = TouhouCharacter(
    'sukuna_shinmyoumaru',
    'Sukuna Shinmyoumaru',
    (
        '少名 針妙丸',
        'Shinmyoumaru',
        'Sukuna',
        'Shinmyoumaru Sukuna',
    ),
)

SUNNY_MILK = TouhouCharacter(
    'sunny_milk',
    'Sunny Milk',
    (
        'サニーミルク',
        'Sanii Miruku',
    ),
)

TAMATSUKURI_MISUMARU = TouhouCharacter(
    'tamatsukuri_misumaru',
    'Tamatsukuri Misumaru',
    (
        '玉造 魅須丸',
        'Misumaru Tamatsukuri',
        'Misumaru',
    ),
)

TATARA_KOGASA = TouhouCharacter(
    'tatara_kogasa',
    'Tatara Kogasa',
    (
        '多々良 小傘',
        'Kogasa Tatara',
        'Kogasa',
        'Tatara',
    ),
)

TEIREIDA_MAI = TouhouCharacter(
    'teireida_mai',
    'Teireida Mai',
    (
        '丁礼田 舞',
        'tmai',
        'Mai Teireida',
    ),
)

TENKAJIN_CHIYARI = TouhouCharacter(
    'tenkajin_chiyari',
    'Tenkajin Chiyari',
    (
        '天火人 ちやり',
        'Chiyari Tenkajin',
        'Chiyari',
    ),
)

TENKYUU_CHIMATA = TouhouCharacter(
    'tenkyuu_chimata',
    'Tenkyuu Chimata',
    (
        '天弓 千亦',
        'Chimata Tenkyuu',
        'Chimata',
    ),
)

TOKIKO = TouhouCharacter(
    'tokiko',
    'Tokiko',
    (
        'ときこ',
        '朱鷺子',
    ),
)

TOMOMI = TouhouCharacter(
    'tomomi',
    'Tomomi',
    (
        'Hourai Girl',
    ),
)

TORAMARU_SHOU = TouhouCharacter(
    'toramaru_shou',
    'Toramaru Shou',
    (
        '寅丸 星',
        'Shou',
        'Shou Toramaru',
    ),
)

TOUTETSU_YUUMA = TouhouCharacter(
    'toutetsu_yuuma',
    'Toutetsu Yuuma',
    (
        '饕餮 尤魔',
        'Yuuma Toutetsu',
        'Yuuma',
    ),
)

TOYOSATOMIMI_NO_MIKO = TouhouCharacter(
    'toyosatomimi_no_miko',
    'Toyosatomimi no Miko',
    (
        '豊聡耳 神子',
        'Miko',
    ),
)

TSUBAME = TouhouCharacter(
    'tsubame',
    'Tsubame',
    (
        'Purple-haired Oekaki Girl',
    ),
)

TSUKUMO_BENBEN = TouhouCharacter(
    'tsukumo_benben',
    'Tsukumo Benben',
    (
        '九十九 弁々',
        'Benben Tsukumo',
    ),
)

TSUKUMO_YATSUHASHI = TouhouCharacter(
    'tsukumo_yatsuhashi',
    'Tsukumo Yatsuhashi',
    (
        '九十九 八橋',
        'Yatsuhashi Tsukumo',
    ),
)

UNNAMED_EXOTIC_GIRL_20000_HIT_GIRL = TouhouCharacter(
    'unnamed_exotic_girl_20000_hit_girl',
    'Unnamed Exotic Girl - 20000-hit Girl',
    (
        '20000-hit Girl',
    ),
)

UNNAMED_EXOTIC_GIRL_CLEANING_MAID = TouhouCharacter(
    'unnamed_exotic_girl_cleaning_maid',
    'Unnamed Exotic Girl - Cleaning Maid',
    (
        'Cleaning Maid',
    ),
)

USAMI_RENKO = TouhouCharacter(
    'usami_renko',
    'Usami Renko',
    (
        '宇佐見 蓮子',
        'Renko',
        'Renko Usami',
    ),
)

USAMI_SUMIREKO = TouhouCharacter(
    'usami_sumireko',
    'Usami Sumireko',
    (
        '宇佐見 菫子',
        'Sumireko',
        'Sumireko Usami',
    ),
)

USHIZAKI_URUMI = TouhouCharacter(
    'ushizaki_urumi',
    'Ushizaki Urumi',
    (
        '牛崎 潤美',
        'Urumi',
        'Urumi Ushizaki',
    ),
)

VIVIT = TouhouCharacter(
    'vivit',
    'Vivit',
    (
        'びびっと',
    ),
)

WAKASAGIHIME = TouhouCharacter(
    'wakasagihime',
    'Wakasagihime',
    (
        'わかさぎ姫',
        'Wakasagi',
    ),
)

WATARI_NINA = TouhouCharacter(
    'watari_nina',
    'Watari Nina',
    (
        '渡里 ニナ',
        'ニナ',
        'Nina Watari',
        'Nina',
    ),
)

WATATSUKI_NO_TOYOHIME = TouhouCharacter(
    'watatsuki_no_toyohime',
    'Watatsuki no Toyohime',
    (
        '綿月 豊姫',
        'Toyohime',
    ),
)

WATATSUKI_NO_YORIHIME = TouhouCharacter(
    'watatsuki_no_yorihime',
    'Watatsuki no Yorihime',
    (
        '綿月 依姫',
        'Yorihime',
    ),
)

WAYOUSEI = TouhouCharacter(
    'wayousei',
    'Wayousei',
    (
        'わようせい',
    )
)

WRIGGLE_NIGHTBUG = TouhouCharacter(
    'wriggle_nightbug',
    'Wriggle Nightbug',
    (
        'リグル ナイトバグ',
        'Wriggle',
        'Riguru Naitobagu',
        'Nightbug Wriggle',
    ),
)

YAGOKORO_EIRIN = TouhouCharacter(
    'yagokoro_eirin',
    'Yagokoro Eirin',
    (
        '八意 永琳',
        'Eirin',
        'Eirin Yagokoro',
    ),
)

YAKUMO_RAN = TouhouCharacter(
    'yakumo_ran',
    'Yakumo Ran',
    (
        '八雲 藍',
        'Ran',
        'Ran Yakumo',
    ),
)

YAKUMO_YUKARI = TouhouCharacter(
    'yakumo_yukari',
    'Yakumo Yukari',
    (
        '八雲 紫',
        'Yukari',
        'Yukari Yakumo',
    ),
)

YAMASHIRO_TAKANE = TouhouCharacter(
    'yamashiro_takane',
    'Yamashiro Takane',
    (
        '山城 たかね',
        'Takane',
        'Takane Yamashiro',
    ),
)

YASAKA_KANAKO = TouhouCharacter(
    'yasaka_kanako',
    'Yasaka Kanako',
    (
        '八坂 神奈子',
        'Kanako',
        'Kanako Yasaka',
    ),
)

YATADERA_NARUMI = TouhouCharacter(
    'yatadera_narumi',
    'Yatadera Narumi',
    (
        '矢田寺 成美',
        'Narumi',
        'Narumi Yatadera',
    ),
)

YOMOTSU_HISAMI = TouhouCharacter(
    'yomotsu_hisami',
    'Yomotsu Hisami',
    (
        '豫母都 日狭美',
        'Hisami Yomotsu',
        'Hisami',
    ),
)

YORIGAMI_JOON = TouhouCharacter(
    'yorigami_joon',
    'Yorigami Joon',
    (
        '依神 女苑',
        'Joon',
        'Joon Yorigami',
    ),
)

YORIGAMI_SHION = TouhouCharacter(
    'yorigami_shion',
    'Yorigami Shion',
    (
        '依神 紫苑',
        'Shion',
        'Shion Yorigami',
    ),
)

YORUMI = TouhouCharacter(
    'yorumi',
    'Yorumi',
    (
        'Moonlight\'s Anti-Soul',
    ),
)

YUIMAN_ASAMA = TouhouCharacter(
    'yuiman_asama',
    'Yuiman Asama',
    (
        'Asama',
        'Asama Yuiman',
        'ユイマン 浅間',
        '浅間',
    ),
)

YUMEKO = TouhouCharacter(
    'yumeko',
    'Yumeko',
    (
        'ゆめこ',
        '夢子',
    ),
)

YUUGEN_MAGAN = TouhouCharacter(
    'yuugen_magan',
    'Yuugen Magan',
    (
        'YuugenMagan',
        '幽玄魔眼',
        'ゆうげんまがん',
    ),
)

YUKI = TouhouCharacter(
    'yuki',
    'Yuki',
    (
        'ユキ',
    ),
)
