import vampytest

from ..character import TouhouCharacter, remove_character


def _assert_fields_set(character):
    """
    Asserts whether the touhou character has every of its fields set.
    
    Parameters
    ----------
    character : ``TouhouCharacter``
        The character to assert.
    """
    vampytest.assert_instance(character, TouhouCharacter)
    
    vampytest.assert_instance(character.name, str)
    vampytest.assert_instance(character.nicks, tuple, nullable = True)
    vampytest.assert_instance(character.system_name, str)


def test__TouhouCharacter__new():
    """
    Tests whether ``TouhouCharacter.__new__`` works as intended.
    """
    system_name = 'huyane_matsu'
    name = 'Huyane Matsu'
    nicks = ('Huyane', 'Matsu', 'Fuyane')
    
    touhou_character_names = []
    touhou_character_lookup = {}
    touhou_characters = {}
    
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
    
    _assert_fields_set(character)
    
    vampytest.assert_eq(character.name, name)
    vampytest.assert_eq(character.nicks, nicks)
    vampytest.assert_eq(character.system_name, system_name)
    
    vampytest.assert_eq(
        {*touhou_character_names},
        {name.casefold(), *(nick.casefold() for nick in nicks)},
    )
    vampytest.assert_eq(
        touhou_character_lookup,
        {name.casefold(): character, **{nick.casefold(): character for nick in nicks}},
    )
    vampytest.assert_eq(touhou_characters, {system_name: character})


def test__TouhouCharacter__repr__with_nick():
    """
    Tests whether ``TouhouCharacter.__repr__`` works as intended.
    
    Case: with nick.
    """
    system_name = 'huyane_matsu'
    name = 'Huyane Matsu'
    nicks = ('Huyane', 'Matsu', 'Fuyane')
    
    character = TouhouCharacter(system_name, name, nicks)
    remove_character(character)
    
    output = repr(character)
    vampytest.assert_instance(output, str)
    vampytest.assert_in('nicks = ', output)


def test__TouhouCharacter__repr__without_nick():
    """
    Tests whether ``TouhouCharacter.__repr__`` works as intended.
    
    Case: without nick.
    """
    system_name = 'huyane_matsu'
    name = 'Huyane Matsu'
    nicks = None
    
    character = TouhouCharacter(system_name, name, nicks)
    remove_character(character)
    
    output = repr(character)
    vampytest.assert_instance(output, str)
    vampytest.assert_not_in('nicks = ', output)


def test__TouhouCharacter__hash():
    """
    Tests whether ``TouhouCharacter.__hash__`` works as intended.
    """
    system_name = 'huyane_matsu'
    name = 'Huyane Matsu'
    nicks = ('Huyane', 'Matsu', 'Fuyane')
    
    character = TouhouCharacter(system_name, name, nicks)
    remove_character(character)
    
    output = hash(character)
    vampytest.assert_instance(output, int)


def test__TouhouCharacter__sorting():
    """
    Tests whether ``TouhouCharacter`` sorting works as intended.
    """
    system_name_0 = 'huyane_matsu'
    name_0 = 'Huyane Matsu'
    nicks_0 = ('Huyane', 'Matsu', 'Fuyane')
    
    character_0 = TouhouCharacter(system_name_0, name_0, nicks_0)
    remove_character(character_0)
    
    system_name_1 = 'brain_dead'
    name_1 = 'Brain Dead'
    nicks_1 = ('fresh brain',)
    
    character_1 = TouhouCharacter(system_name_1, name_1, nicks_1)
    remove_character(character_1)
    
    vampytest.assert_true(character_0 > character_1)
    vampytest.assert_true(character_1 < character_0)


def _iter_options__iter_names():
    
    system_name_0 = 'huyane_matsu'
    name_0 = 'Huyane Matsu'
    nicks_0 = ('Huyane', 'Matsu', 'Fuyane')
    
    character_0 = TouhouCharacter(system_name_0, name_0, nicks_0)
    remove_character(character_0)
    
    system_name_1 = 'brain_dead'
    name_1 = 'Brain Dead'
    nicks_1 = None
    
    character_1 = TouhouCharacter(system_name_1, name_1, nicks_1)
    remove_character(character_1)
    
    yield character_0, {name_0, *nicks_0}
    yield character_1, {name_1}


@vampytest._(vampytest.call_from(_iter_options__iter_names()).returning_last())
def test__TouhouCharacter__iter_names(character):
    """
    tests whether ``TouhouCharacter.iter_names`` works as intended.
    
    Parameters
    ----------
    character : ``TouhouCharacter``
        The character to iter its name of.
    
    Returns
    -------
    names : `set<str>`
    """
    return {*character.iter_names()}
