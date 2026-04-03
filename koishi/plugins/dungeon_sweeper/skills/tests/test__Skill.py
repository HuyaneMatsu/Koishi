import vampytest

from types import FunctionType

from ...move_directions import MoveDirections

from ..skill import Skill


def _assert_fields_set(skill):
    """
    Asserts whether the given sill has all of its fields set.
    
    Parameters
    ----------
    skill : ``Skill``
        The skill to test.
    """
    vampytest.assert_instance(skill, Skill)
    vampytest.assert_instance(skill.can_activate, FunctionType)
    vampytest.assert_instance(skill.get_directions, FunctionType)
    vampytest.assert_instance(skill.id, int)
    vampytest.assert_instance(skill.use, FunctionType)


def test__Skill__new():
    """
    Tests whether ``Skill.__new__`` works as intended.
    """
    skill_id = 999
    
    def can_activate(game_state):
        return False
    
    def get_directions(game_state):
        return MoveDirections()
    
    def use(game_state):
        return False
    
    
    skill = Skill(
        skill_id,
        can_activate,
        get_directions,
        use,
    )
    _assert_fields_set(skill)
    
    vampytest.assert_eq(skill.id, skill_id)
    
    vampytest.assert_is(skill.can_activate, can_activate)
    vampytest.assert_is(skill.get_directions, get_directions)
    vampytest.assert_is(skill.use, use)


def test__Skill__repr():
    """
    Tests whether ``Skill.__repr__`` works as intended.
    """
    skill_id = 999
    
    def can_activate(game_state):
        return False
    
    def get_directions(game_state):
        return MoveDirections()
    
    def use(game_state):
        return False
    
    
    skill = Skill(
        skill_id,
        can_activate,
        get_directions,
        use,
    )
    
    output = repr(skill)
    vampytest.assert_instance(output, str)
