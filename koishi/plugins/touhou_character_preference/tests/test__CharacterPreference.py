import vampytest

from ...touhou_core import TOUHOU_CHARACTERS

from ..character_preference import CharacterPreference


def _assert_fields_set(character_preference):
    """
    Assets whether every field is set of the given character preference.
    
    Parameters
    ----------
    character_preference : ``CharacterPreference``
        Character preference to check.
    """
    vampytest.assert_instance(character_preference, CharacterPreference)
    
    vampytest.assert_instance(character_preference, CharacterPreference)
    vampytest.assert_instance(character_preference.entry_id, int)
    vampytest.assert_instance(character_preference.user_id, int)
    vampytest.assert_instance(character_preference.system_name, str)
    

def test__CharacterPreference__new():
    """
    Tests whether ``CharacterPreference.__new__`` works as intended.
    """
    user_id = 202309150000
    system_name = 'komeiji_koishi'
    
    character_preference = CharacterPreference(user_id, system_name)
    _assert_fields_set(character_preference)
    
    vampytest.assert_eq(character_preference.entry_id, 0)
    vampytest.assert_eq(character_preference.user_id, user_id)
    vampytest.assert_eq(character_preference.system_name, system_name)


def test__CharacterPreference__from_entry():
    """
    Tests whether ``CharacterPreference.from_entry`` works as intended.
    """
    entry_id = 69
    user_id = 202309150001
    system_name = 'komeiji_koishi'
    
    entry = {
        'id': entry_id,
        'user_id': user_id,
        'system_name': system_name,
    }
    
    character_preference = CharacterPreference.from_entry(entry)
    _assert_fields_set(character_preference)
    
    vampytest.assert_eq(character_preference.entry_id, entry_id)
    vampytest.assert_eq(character_preference.user_id, user_id)
    vampytest.assert_eq(character_preference.system_name, system_name)


def test__CharacterPreference__repr():
    """
    Tests whether ``CharacterPreference.__repr__`` works as intended.
    """
    entry_id = 69
    user_id = 202309150002
    system_name = 'komeiji_koishi'
    
    entry = {
        'id': entry_id,
        'user_id': user_id,
        'system_name': system_name,
    }
    
    character_preference = CharacterPreference.from_entry(entry)
    vampytest.assert_instance(repr(character_preference), str)


def test__CharacterPreference__get_character():
    """
    Tests whether ``CharacterPreference.get_character`` works as intended.
    
    Case: Existing.
    """
    system_name = 'komeiji_koishi'
    
    character_preference = CharacterPreference(0, system_name)
    
    character = TOUHOU_CHARACTERS[system_name]
    output = character_preference.get_character()
    vampytest.assert_is(output, character)


def test__CharacterPreference__get_character_miss():
    """
    Tests whether ``CharacterPreference.get_character`` works as intended.
    
    Case: Missing.
    """
    system_name = 'huyane'
    
    character_preference = CharacterPreference(0, system_name)
    
    output = character_preference.get_character()
    vampytest.assert_is(output, None)


def test__CharacterPreference__eq():
    """
    Tests whether ``CharacterPreference.__eq__`` works as intended.
    """
    user_id = 202309170036
    system_name = 'komeiji_koishi'
    
    character_preference = CharacterPreference(user_id, system_name)
    vampytest.assert_eq(character_preference, character_preference)
    vampytest.assert_ne(character_preference, object())
    
    vampytest.assert_ne(character_preference, CharacterPreference(user_id, 'komeiji_satori'))
    vampytest.assert_ne(character_preference, CharacterPreference(202309170037, system_name))
