import vampytest

from ..character import TouhouCharacter, register_character, remove_character


def test__register_character():
    """
    Tests whether ``register_character`` works as intended.
    """
    system_name = 'huyane_matsu'
    name = 'Huyane Matsu'
    nicks = ('Huyane', 'Matsu', 'Fuyane')
    
    touhou_character_names = []
    touhou_character_lookup = {}
    touhou_characters = {}
    
    register_called = False
    called_with_character = None
    
    def mocked_register_character(character):
        nonlocal register_called
        nonlocal called_with_character
        
        register_called = True
        called_with_character = character
    
    mocked = vampytest.mock_globals(
        TouhouCharacter.__new__,
        register_character = mocked_register_character,
    )
    
    character = mocked(
        TouhouCharacter,
        system_name,
        name,
        nicks,
    )
    
    vampytest.assert_true(register_called)
    vampytest.assert_is(called_with_character, character)
    
    
    mocked = vampytest.mock_globals(
        register_character,
        TOUHOU_CHARACTER_NAMES = touhou_character_names,
        TOUHOU_CHARACTER_LOOKUP = touhou_character_lookup,
        TOUHOU_CHARACTERS = touhou_characters,
    )
    
    mocked(character)
    
    vampytest.assert_eq(
        {*touhou_character_names},
        {name.casefold(), *(nick.casefold() for nick in nicks)},
    )
    vampytest.assert_eq(
        touhou_character_lookup,
        {name.casefold(): character, **{nick.casefold(): character for nick in nicks}},
    )
    vampytest.assert_eq(touhou_characters, {system_name: character})


def test__remove_character():
    """
    Tests whether ``remove_character`` works as intended.
    """
    system_name = 'huyane_matsu'
    name = 'Huyane Matsu'
    nicks = ('Huyane', 'Matsu', 'Fuyane')
    
    touhou_character_names = ['aya']
    touhou_character_lookup = {'aya': None}
    touhou_characters = {'aya': None}
    
    touhou_character_names_before = touhou_character_names.copy()
    touhou_character_lookup_before = touhou_character_lookup.copy()
    touhou_characters_before = touhou_characters.copy()
    
    mocked = vampytest.mock_globals(
        TouhouCharacter.__new__,
        2,
        TOUHOU_CHARACTER_NAMES = touhou_character_names,
        TOUHOU_CHARACTER_LOOKUP = touhou_character_lookup,
        TOUHOU_CHARACTERS = touhou_characters,
    )
    
    character = mocked(
        TouhouCharacter,
        system_name,
        name,
        nicks,
    )
    
    vampytest.assert_ne(touhou_character_names, touhou_character_names_before)
    vampytest.assert_ne(touhou_character_lookup, touhou_character_lookup_before)
    vampytest.assert_ne(touhou_characters, touhou_characters_before)
    
    
    mocked = vampytest.mock_globals(
        remove_character,
        TOUHOU_CHARACTER_NAMES = touhou_character_names,
        TOUHOU_CHARACTER_LOOKUP = touhou_character_lookup,
        TOUHOU_CHARACTERS = touhou_characters,
    )
    
    mocked(character)
    
    vampytest.assert_eq(touhou_character_names, touhou_character_names_before)
    vampytest.assert_eq(touhou_character_lookup, touhou_character_lookup_before)
    vampytest.assert_eq(touhou_characters, touhou_characters_before)
