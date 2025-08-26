import vampytest

from ...image_handling_core import ImageHandlerSafeBooru, ImageHandlerGroup
from ...image_handling_core.constants import SOLO_REQUIRED_TAGS, TOUHOU_TAGS_BANNED

from ..character import TOUHOU_CHARACTERS
from ..characters import KOMEIJI_KOISHI, KOMEIJI_SATORI
from ..handler_key import TOUHOU_IMAGE_HANDLERS, TouhouHandlerKey


def _assert_fields_set(handler_key):
    """
    Tests whether ``TouhouHandlerKey`` works as intended.
    
    Parameters
    ----------
    handler_key : ``TouhouHandlerKey``
        The handler key to assert.
    """
    vampytest.assert_instance(handler_key, TouhouHandlerKey)
    
    vampytest.assert_instance(handler_key.characters, frozenset, nullable = True)
    vampytest.assert_instance(handler_key.hash_value, int)
    vampytest.assert_instance(handler_key.solo, bool)


def test__TouhouHandlerKey__new__no_characters():
    """
    Tests whether ``TouhouHandlerKey`` works as intended.
    
    Case: No characters.
    """
    handler_key = TouhouHandlerKey()
    _assert_fields_set(handler_key)
    
    vampytest.assert_is(handler_key.characters, None)
    vampytest.assert_eq(handler_key.solo, True)


def test__TouhouHandlerKey__new__multiple_characters():
    """
    Tests whether ``TouhouHandlerKey`` works as intended.
    
    Case: Multiple characters.
    """
    handler_key = TouhouHandlerKey(KOMEIJI_KOISHI, KOMEIJI_SATORI)
    _assert_fields_set(handler_key)
    
    vampytest.assert_eq(handler_key.characters, {KOMEIJI_KOISHI, KOMEIJI_SATORI})
    vampytest.assert_eq(handler_key.solo, False)


def test__TouhouHandlerKey__new__single_character():
    """
    Tests whether ``TouhouHandlerKey`` works as intended.
    
    Case: Single character.
    """
    handler_key = TouhouHandlerKey(KOMEIJI_KOISHI)
    _assert_fields_set(handler_key)
    
    vampytest.assert_eq(handler_key.characters, {KOMEIJI_KOISHI})
    vampytest.assert_eq(handler_key.solo, True)


def test__TouhouHandlerKey__new__single_character_non_solo():
    """
    Tests whether ``TouhouHandlerKey`` works as intended.
    
    Case: Single character, non solo.
    """
    handler_key = TouhouHandlerKey(KOMEIJI_KOISHI, solo = False)
    _assert_fields_set(handler_key)
    
    vampytest.assert_eq(handler_key.characters, {KOMEIJI_KOISHI})
    vampytest.assert_eq(handler_key.solo, False)


def test__TouhouHandlerKey__repr():
    """
    Tests whether ``TouhouHandlerKey.__repr__`` works as intended.
    """
    handler_key = TouhouHandlerKey(KOMEIJI_KOISHI, KOMEIJI_SATORI)
    
    output = repr(handler_key)
    vampytest.assert_instance(output, str)


def test__TouhouHandlerKey__hash():
    """
    Tests whether ``TouhouHandlerKey.__hash__`` works as intended.
    """
    handler_key = TouhouHandlerKey(KOMEIJI_KOISHI, KOMEIJI_SATORI)
    
    output = hash(handler_key)
    vampytest.assert_instance(output, int)


def test__TouhouHandlerKey__eq():
    """
    Tests whether ``TouhouHandlerKey.__eq__`` works as intended.
    """
    characters = [KOMEIJI_KOISHI]
    solo = False
    
    
    handler_key = TouhouHandlerKey(*characters, solo = solo)
    
    vampytest.assert_eq(handler_key, handler_key)
    vampytest.assert_ne(handler_key, object())
    
    vampytest.assert_ne(handler_key, TouhouHandlerKey(KOMEIJI_SATORI, solo = solo))
    vampytest.assert_ne(handler_key, TouhouHandlerKey(*characters, solo = True))
    

def test__TouhouHandlerKey__apply_solo_preference__no_characters():
    """
    Tests whether ``TouhouHandlerKey.apply_solo_preference`` works as intended.
    
    Case: No characters.
    """
    handler_key = TouhouHandlerKey(solo = False)
    vampytest.assert_eq(handler_key.solo, False)
    handler_key.apply_solo_preference()
    vampytest.assert_eq(handler_key.solo, False)


def test__TouhouHandlerKey__apply_solo_preference__multiple_characters():
    """
    Tests whether ``TouhouHandlerKey.apply_solo_preference`` works as intended.
    
    Case: Multiple characters.
    """
    handler_key = TouhouHandlerKey(KOMEIJI_KOISHI, KOMEIJI_SATORI, solo = False)
    vampytest.assert_eq(handler_key.solo, False)
    handler_key.apply_solo_preference()
    vampytest.assert_eq(handler_key.solo, False)


def test__TouhouHandlerKey__apply_solo_preference__single_character():
    """
    Tests whether ``TouhouHandlerKey.apply_solo_preference`` works as intended.
    
    Case: One character.
    """
    handler_key = TouhouHandlerKey(KOMEIJI_KOISHI, solo = False)
    vampytest.assert_eq(handler_key.solo, False)
    handler_key.apply_solo_preference()
    vampytest.assert_eq(handler_key.solo, True)


def _iter_options__handler_pairs():
    try:
        yield (
            TouhouHandlerKey(solo = True),
            ImageHandlerGroup(*(
                TouhouHandlerKey(character, solo = True).get_handler() for character in TOUHOU_CHARACTERS.values()
            ))
        )
        
        yield (
            TouhouHandlerKey(solo = False),
            ImageHandlerGroup(*(
                TouhouHandlerKey(character, solo = False).get_handler() for character in TOUHOU_CHARACTERS.values()
            ))
        )
        
        yield (
            TouhouHandlerKey(KOMEIJI_KOISHI, solo = True),
            ImageHandlerSafeBooru(
                SOLO_REQUIRED_TAGS,
                TOUHOU_TAGS_BANNED,
                {
                    (True, 'komeiji_koishi'),
                },
                True,
            )
        )
        
        yield (
            TouhouHandlerKey(KOMEIJI_KOISHI, solo = False),
            ImageHandlerSafeBooru(
                None,
                TOUHOU_TAGS_BANNED,
                {
                    (True, 'komeiji_koishi'),
                },
                True,
            )
        )
        
        yield (
            TouhouHandlerKey(KOMEIJI_KOISHI, KOMEIJI_SATORI),
            ImageHandlerSafeBooru(
                None,
                TOUHOU_TAGS_BANNED,
                {
                    (True, 'komeiji_koishi'),
                    (True, 'komeiji_satori'),
                },
                True,
            )
        )
    
    finally:
        TOUHOU_IMAGE_HANDLERS.clear()


@vampytest._(vampytest.call_from(_iter_options__handler_pairs()).returning_last())
def test__TouhouHandlerKey__get_handler(handler_key):
    """
    Tests whether ``TouhouHandlerKey.get_handler`` works as intended.
    
    Parameters
    ----------
    handler_key : ``TouhouHandlerKey``
        Handler key to get its image handler of.
    
    Returns
    -------
    handler_key : ``TouhouHandlerKey``
    """
    try:
        return handler_key.get_handler()
    finally:
        TOUHOU_IMAGE_HANDLERS.clear()


def test__TouhouHandlerKey__get_handler__cache():
    """
    Tests whether ``TouhouHandlerKey.get_handler`` works as intended.
    
    Case: Caching.
    """
    try:
        image_handler_0 = TouhouHandlerKey(KOMEIJI_KOISHI).get_handler()
        image_handler_1 = TouhouHandlerKey(KOMEIJI_KOISHI).get_handler()
        
        vampytest.assert_is(image_handler_0, image_handler_1)
    finally:
        TOUHOU_IMAGE_HANDLERS.clear()



@vampytest._(vampytest.call_from(_iter_options__handler_pairs()).returning_last())
def test__TouhouHandlerKey__create_handler(handler_key):
    """
    Tests whether ``TouhouHandlerKey.create_handler`` works as intended.
    
    Parameters
    ----------
    handler_key : ``TouhouHandlerKey``
        Handler key to create its image handler of.
    
    Returns
    -------
    handler_key : ``TouhouHandlerKey``
    """
    return handler_key.create_handler()
