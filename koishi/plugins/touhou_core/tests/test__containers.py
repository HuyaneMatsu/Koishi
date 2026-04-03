import vampytest

from ..character import TOUHOU_CHARACTER_LOOKUP, TOUHOU_CHARACTER_NAMES, TOUHOU_CHARACTERS, TouhouCharacter
from ..safe_booru_tags import TOUHOU_SAFE_BOORU_TAGS
from ..tags import TAG_TO_CHARACTER

from .test__TouhouCharacter import _assert_fields_set


def test__TOUHOU_CHARACTER_NAMES():
    """
    Tests ``TOUHOU_CHARACTER_NAMES``'s structure.
    """
    for name in TOUHOU_CHARACTER_NAMES:
        vampytest.assert_instance(name, str)
        vampytest.assert_eq(name.casefold(), name)


def test__TOUHOU_CHARACTER_LOOKUP():
    """
    Tests ``TOUHOU_CHARACTER_LOOKUP``'s structure.
    """
    for name, character in TOUHOU_CHARACTER_LOOKUP.items():
        vampytest.assert_instance(name, str)
        vampytest.assert_instance(character, TouhouCharacter)
        vampytest.assert_eq(name.casefold(), name)


def test__TOUHOU_CHARACTERS():
    """
    Tests ``TOUHOU_CHARACTERS``'s structure.
    """
    for name, character in TOUHOU_CHARACTERS.items():
        vampytest.assert_instance(name, str)
        _assert_fields_set(character)
        vampytest.assert_eq(name, character.system_name)


def test__TOUHOU_SAFE_BOORU_TAGS():
    """
    Tests ``TOUHOU_SAFE_BOORU_TAGS``'s structure.
    """
    for character, tags in TOUHOU_SAFE_BOORU_TAGS.items():
        vampytest.assert_instance(character, TouhouCharacter)
        vampytest.assert_instance(tags, tuple)
        vampytest.assert_true(len(tags) > 0)
        for tag in tags:
            vampytest.assert_instance(tag, str)


def test__TAG_TO_CHARACTER():
    """
    Tests ``TAG_TO_CHARACTER``'s structure.
    """
    for tag, character in TAG_TO_CHARACTER.items():
        vampytest.assert_instance(tag, str)
        vampytest.assert_instance(character, TouhouCharacter)
