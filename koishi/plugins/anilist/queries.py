__all__ = ()

from .constants import ENTRY_PER_PAGE, SUB_ENTRY_PER_PAGE
from .keys import (
    KEY_CHARACTER, KEY_CHARACTER_AGE, KEY_CHARACTER_ARRAY, KEY_CHARACTER_BIRTH_DATE, KEY_CHARACTER_BLOOD_TYPE,
    KEY_CHARACTER_DESCRIPTION, KEY_CHARACTER_GENDER, KEY_CHARACTER_ID, KEY_CHARACTER_IMAGE, KEY_CHARACTER_IMAGE_LARGE,
    KEY_CHARACTER_MEDIA_CONNECTIONS, KEY_CHARACTER_MEDIA_CONNECTIONS_MEDIA_ARRAY, KEY_CHARACTER_NAME,
    KEY_CHARACTER_NAME_FIRST, KEY_CHARACTER_NAME_LAST, KEY_CHARACTER_NAME_MIDDLE, KEY_CHARACTER_NAME_NATIVE,
    KEY_FUZZY_DATE_DAY, KEY_FUZZY_DATE_MONTH, KEY_FUZZY_DATE_YEAR, KEY_MEDIA, KEY_MEDIA_ARRAY, KEY_MEDIA_AVERAGE_SCORE,
    KEY_MEDIA_CHAPTER_COUNT, KEY_MEDIA_DESCRIPTION, KEY_MEDIA_DESCRIPTION_MODIFIER, KEY_MEDIA_END_DATE,
    KEY_MEDIA_EPISODE_COUNT, KEY_MEDIA_EPISODE_LENGTH, KEY_MEDIA_FORMAT, KEY_MEDIA_GENRES, KEY_MEDIA_ID,
    KEY_MEDIA_IMAGE, KEY_MEDIA_IMAGE_LARGE, KEY_MEDIA_NAME, KEY_MEDIA_NAME_NATIVE, KEY_MEDIA_NAME_NATIVE_MODIFIER,
    KEY_MEDIA_NAME_ROMAJI, KEY_MEDIA_NAME_ROMAJI_MODIFIER, KEY_MEDIA_START_DATE, KEY_MEDIA_STATUS,
    KEY_MEDIA_STATUS_MODIFIER, KEY_MEDIA_TYPE, KEY_MEDIA_TYPE_ANIME, KEY_MEDIA_TYPE_MANGA, KEY_MEDIA_VOLUME_COUNT,
    KEY_PAGE, KEY_PAGE_IDENTIFIER, KEY_PAGE_INFO, KEY_PAGE_INFO_CURRENT, KEY_PAGE_INFO_ENTRIES,
    KEY_PAGE_INFO_TOTAL, KEY_PER_PAGE, KEY_QUERY, KEY_SEARCH, KEY_VARIABLE_CHARACTER_ID,
    KEY_VARIABLE_CHARACTER_QUERY, KEY_VARIABLE_MEDIA_ID, KEY_VARIABLE_MEDIA_QUERY, KEY_VARIABLE_PAGE_IDENTIFIER
)


REQUIRED_CHARACTER_FIELDS = (
    f'{KEY_CHARACTER_ID} '
    f'{KEY_CHARACTER_NAME}{{'
        f'{KEY_CHARACTER_NAME_FIRST} '
        f'{KEY_CHARACTER_NAME_MIDDLE} '
        f'{KEY_CHARACTER_NAME_LAST} '
        f'{KEY_CHARACTER_NAME_NATIVE}'
    f'}}'
    f'{KEY_CHARACTER_IMAGE}{{'
        f'{KEY_CHARACTER_IMAGE_LARGE}'
    f'}}'
    f'{KEY_CHARACTER_BIRTH_DATE}{{'
        f'{KEY_FUZZY_DATE_YEAR} '
        f'{KEY_FUZZY_DATE_MONTH} '
        f'{KEY_FUZZY_DATE_DAY} '
    f'}}'
    f'{KEY_CHARACTER_DESCRIPTION} '
    f'{KEY_CHARACTER_GENDER} '
    f'{KEY_CHARACTER_BLOOD_TYPE} '
    f'{KEY_CHARACTER_AGE} '
    f'{KEY_CHARACTER_MEDIA_CONNECTIONS}('
        f'sort:[POPULARITY_DESC],'
        f'{KEY_PER_PAGE}:{SUB_ENTRY_PER_PAGE}'
    f'){{'
        f'{KEY_CHARACTER_MEDIA_CONNECTIONS_MEDIA_ARRAY}{{'
            f'{KEY_MEDIA_ID} '
            f'{KEY_MEDIA_TYPE} '
            f'{KEY_MEDIA_NAME}{{'
                f'{KEY_MEDIA_NAME_ROMAJI}({KEY_MEDIA_NAME_ROMAJI_MODIFIER})'
                f'{KEY_MEDIA_NAME_NATIVE}({KEY_MEDIA_NAME_NATIVE_MODIFIER})'
            f'}}'
        f'}}'
    f'}}'
)


QUERY_CHARACTER = (
    f'{KEY_QUERY}(${KEY_VARIABLE_CHARACTER_QUERY}:String){{'
        f'{KEY_CHARACTER}({KEY_SEARCH}:${KEY_VARIABLE_CHARACTER_QUERY}){{'
            f'{REQUIRED_CHARACTER_FIELDS}'
        f'}}'
    f'}}'
)


QUERY_CHARACTER_BY_ID = (
    f'{KEY_QUERY}(${KEY_VARIABLE_CHARACTER_ID}:Int){{'
        f'{KEY_CHARACTER}({KEY_CHARACTER_ID}: ${KEY_VARIABLE_CHARACTER_ID}){{'
            f'{REQUIRED_CHARACTER_FIELDS}'
        f'}}'
    f'}}'
)


QUERY_CHARACTER_ARRAY = (
    f'{KEY_QUERY}('
        f'${KEY_VARIABLE_PAGE_IDENTIFIER}:Int,'
        f'${KEY_VARIABLE_CHARACTER_QUERY}:String'
    f'){{'
        f'{KEY_PAGE}({KEY_PAGE_IDENTIFIER}:${KEY_VARIABLE_PAGE_IDENTIFIER},{KEY_PER_PAGE}:{ENTRY_PER_PAGE}){{'
            f'{KEY_PAGE_INFO}{{'
                f'{KEY_PAGE_INFO_ENTRIES} '
                f'{KEY_PAGE_INFO_CURRENT} '
                f'{KEY_PAGE_INFO_TOTAL}'
            f'}}'
            f'{KEY_CHARACTER_ARRAY}({KEY_SEARCH}:${KEY_VARIABLE_CHARACTER_QUERY}){{'
                f'{KEY_CHARACTER_ID} '
                f'{KEY_CHARACTER_NAME}{{'
                    f'{KEY_CHARACTER_NAME_FIRST} '
                    f'{KEY_CHARACTER_NAME_MIDDLE} '
                    f'{KEY_CHARACTER_NAME_LAST} '
                    f'{KEY_CHARACTER_NAME_NATIVE}'
                f'}}'
            f'}}'
        f'}}'
    f'}}'
)


REQUIRED_ANIME_FIELDS = (
    f'{KEY_MEDIA_ID} '
    f'{KEY_MEDIA_NAME}{{'
        f'{KEY_MEDIA_NAME_ROMAJI}({KEY_MEDIA_NAME_ROMAJI_MODIFIER})'
        f'{KEY_MEDIA_NAME_NATIVE}({KEY_MEDIA_NAME_NATIVE_MODIFIER})'
    f'}}'
    f'{KEY_MEDIA_DESCRIPTION}({KEY_MEDIA_DESCRIPTION_MODIFIER})'
    f'{KEY_MEDIA_EPISODE_COUNT} '
    f'{KEY_MEDIA_FORMAT} '
    f'{KEY_MEDIA_STATUS}({KEY_MEDIA_STATUS_MODIFIER})'
    f'{KEY_MEDIA_EPISODE_LENGTH} '
    f'{KEY_MEDIA_START_DATE}{{'
        f'{KEY_FUZZY_DATE_YEAR} '
        f'{KEY_FUZZY_DATE_MONTH} '
        f'{KEY_FUZZY_DATE_DAY} '
    f'}}'
    f'{KEY_MEDIA_END_DATE}{{'
        f'{KEY_FUZZY_DATE_YEAR} '
        f'{KEY_FUZZY_DATE_MONTH} '
        f'{KEY_FUZZY_DATE_DAY} '
    f'}}'
    f'{KEY_MEDIA_IMAGE}{{'
        f'{KEY_MEDIA_IMAGE_LARGE}'
    f'}}'
    f'{KEY_MEDIA_GENRES} '
    f'{KEY_MEDIA_AVERAGE_SCORE}'
)


QUERY_ANIME = (
    f'{KEY_QUERY}(${KEY_VARIABLE_MEDIA_QUERY}:String){{'
        f'{KEY_MEDIA}({KEY_MEDIA_TYPE}:{KEY_MEDIA_TYPE_ANIME},{KEY_SEARCH}:${KEY_VARIABLE_MEDIA_QUERY}){{'
            f'{REQUIRED_ANIME_FIELDS}'
        f'}}'
    f'}}'
)


QUERY_ANIME_BY_ID = (
    f'{KEY_QUERY}(${KEY_VARIABLE_MEDIA_ID}:Int){{'
        f'{KEY_MEDIA}({KEY_MEDIA_TYPE}:{KEY_MEDIA_TYPE_ANIME},{KEY_MEDIA_ID}:${KEY_VARIABLE_MEDIA_ID}){{'
            f'{REQUIRED_ANIME_FIELDS}'
        f'}}'
    f'}}'
)


QUERY_ANIME_ARRAY = (
    f'{KEY_QUERY}('
        f'${KEY_VARIABLE_PAGE_IDENTIFIER}:Int,'
        f'${KEY_VARIABLE_CHARACTER_QUERY}:String'
    f'){{'
        f'{KEY_PAGE}({KEY_PAGE_IDENTIFIER}:${KEY_VARIABLE_PAGE_IDENTIFIER},{KEY_PER_PAGE}:{ENTRY_PER_PAGE}){{'
            f'{KEY_PAGE_INFO}{{'
                f'{KEY_PAGE_INFO_ENTRIES} '
                f'{KEY_PAGE_INFO_CURRENT} '
                f'{KEY_PAGE_INFO_TOTAL}'
            f'}}'
            f'{KEY_MEDIA_ARRAY}('
                f'{KEY_MEDIA_TYPE}:{KEY_MEDIA_TYPE_ANIME},'
                f'{KEY_SEARCH}:${KEY_VARIABLE_CHARACTER_QUERY}'
            f'){{'
                f'{KEY_MEDIA_ID} '
                f'{KEY_MEDIA_NAME}{{'
                    f'{KEY_MEDIA_NAME_ROMAJI}({KEY_MEDIA_NAME_ROMAJI_MODIFIER})'
                    f'{KEY_MEDIA_NAME_NATIVE}({KEY_MEDIA_NAME_NATIVE_MODIFIER})'
                f'}}'
            f'}}'
        f'}}'
    f'}}'
)


REQUIRED_MANGA_FIELDS = (
    f'{KEY_MEDIA_ID} '
    f'{KEY_MEDIA_NAME}{{'
        f'{KEY_MEDIA_NAME_ROMAJI}({KEY_MEDIA_NAME_ROMAJI_MODIFIER})'
        f'{KEY_MEDIA_NAME_NATIVE}({KEY_MEDIA_NAME_NATIVE_MODIFIER})'
    f'}}'
    f'{KEY_MEDIA_DESCRIPTION}({KEY_MEDIA_DESCRIPTION_MODIFIER})'
    f'{KEY_MEDIA_VOLUME_COUNT} '
    f'{KEY_MEDIA_FORMAT} '
    f'{KEY_MEDIA_STATUS}({KEY_MEDIA_STATUS_MODIFIER})'
    f'{KEY_MEDIA_CHAPTER_COUNT} '
    f'{KEY_MEDIA_START_DATE}{{'
        f'{KEY_FUZZY_DATE_YEAR} '
        f'{KEY_FUZZY_DATE_MONTH} '
        f'{KEY_FUZZY_DATE_DAY} '
    f'}}'
    f'{KEY_MEDIA_END_DATE}{{'
        f'{KEY_FUZZY_DATE_YEAR} '
        f'{KEY_FUZZY_DATE_MONTH} '
        f'{KEY_FUZZY_DATE_DAY} '
    f'}}'
    f'{KEY_MEDIA_IMAGE}{{'
        f'{KEY_MEDIA_IMAGE_LARGE}'
    f'}}'
    f'{KEY_MEDIA_GENRES} '
    f'{KEY_MEDIA_AVERAGE_SCORE}'
)


QUERY_MANGA = (
    f'{KEY_QUERY}(${KEY_VARIABLE_MEDIA_QUERY}:String){{'
        f'{KEY_MEDIA}({KEY_MEDIA_TYPE}:{KEY_MEDIA_TYPE_MANGA},{KEY_SEARCH}:${KEY_VARIABLE_MEDIA_QUERY}){{'
            f'{REQUIRED_MANGA_FIELDS}'
        f'}}'
    f'}}'
)


QUERY_MANGA_BY_ID = (
    f'{KEY_QUERY}(${KEY_VARIABLE_MEDIA_ID}:Int){{'
        f'{KEY_MEDIA}({KEY_MEDIA_TYPE}:{KEY_MEDIA_TYPE_MANGA},{KEY_MEDIA_ID}:${KEY_VARIABLE_MEDIA_ID}){{'
            f'{REQUIRED_MANGA_FIELDS}'
        f'}}'
    f'}}'
)


QUERY_MANGA_ARRAY = (
    f'{KEY_QUERY}('
        f'${KEY_VARIABLE_PAGE_IDENTIFIER}:Int,'
        f'${KEY_VARIABLE_CHARACTER_QUERY}:String'
    f'){{'
        f'{KEY_PAGE}({KEY_PAGE_IDENTIFIER}:${KEY_VARIABLE_PAGE_IDENTIFIER},{KEY_PER_PAGE}:{ENTRY_PER_PAGE}){{'
            f'{KEY_PAGE_INFO}{{'
                f'{KEY_PAGE_INFO_ENTRIES} '
                f'{KEY_PAGE_INFO_CURRENT} '
                f'{KEY_PAGE_INFO_TOTAL}'
            f'}}'
            f'{KEY_MEDIA_ARRAY}('
                f'{KEY_MEDIA_TYPE}:{KEY_MEDIA_TYPE_MANGA},'
                f'{KEY_SEARCH}:${KEY_VARIABLE_CHARACTER_QUERY}'
            f'){{'
                f'{KEY_MEDIA_ID} '
                f'{KEY_MEDIA_NAME}{{'
                    f'{KEY_MEDIA_NAME_ROMAJI}({KEY_MEDIA_NAME_ROMAJI_MODIFIER})'
                    f'{KEY_MEDIA_NAME_NATIVE}({KEY_MEDIA_NAME_NATIVE_MODIFIER})'
                f'}}'
            f'}}'
        f'}}'
    f'}}'
)
