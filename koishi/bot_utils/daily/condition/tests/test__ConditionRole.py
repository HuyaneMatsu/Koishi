import vampytest
from hata import Guild, GuildProfile, Role, User

from ..role import ConditionRole


def _assert_fields_set(condition):
    """
    Asserts whether the given condition has all of its fields set.
    
    Parameters
    ----------
    condition : ``ConditionRole``
        The instance to check.
    """
    vampytest.assert_instance(condition, ConditionRole)
    vampytest.assert_instance(condition.role, Role)


def test__ConditionRole__new():
    """
    Tests whether ``ConditionRole.__new__`` works as intended.
    """
    role = Role.precreate(202412010010)
    
    condition = ConditionRole(role)
    _assert_fields_set(condition)
    
    vampytest.assert_is(condition.role, role)


def test__ConditionRole__repr():
    """
    Tests whether ``ConditionRole.__repr__`` works as intended.
    """
    role = Role.precreate(202412010011)
    
    condition = ConditionRole(role)
    
    output = repr(condition)
    vampytest.assert_instance(output, str)
    
    vampytest.assert_in(type(condition).__name__, output)
    vampytest.assert_in(f' role = {role!r}', output)


def test__ConditionRole__hash():
    """
    Tests whether ``ConditionRole.__hash__`` works as intended.
    """
    role = Role.precreate(202412010012)
    
    condition = ConditionRole(role)
    
    output = hash(condition)
    vampytest.assert_instance(output, int)


def _iter_options__eq():
    role = Role.precreate(202412010013)
    
    keyword_parameters = {
        'role': role,
    }
    
    yield (
        keyword_parameters,
        keyword_parameters,
        True,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'role': Role.precreate(202412010014),
        },
        False,
    )
    
    
@vampytest._(vampytest.call_from(_iter_options__eq()).returning_last())
def test__ConditionRole__eq(keyword_parameters_0, keyword_parameters_1):
    """
    Tests whether ``ConditionRole.__eq__`` works as intended.
    
    Parameters
    ----------
    keyword_parameters_0 : `dict<str, object>`
        Keyword parameters to create instance with.
    
    keyword_parameters_1 : `dict<str, object>`
        Keyword parameters to create instance with.
    
    Returns
    -------
    output : `bool`
    """
    condition_0 = ConditionRole(**keyword_parameters_0)
    condition_1 = ConditionRole(**keyword_parameters_1)
    
    output = condition_0 == condition_1
    vampytest.assert_instance(output, bool)
    return output


def test__ConditionRole__call__passing():
    """
    Tests whether ``ConditionRole.__call__`` works as intended.
    
    Case: passing.
    """
    guild_id = 202412010017
    role = Role.precreate(202412010015, guild_id = guild_id)
    user = User.precreate(202412010016, name = 'brain')
    guild = Guild.precreate(guild_id, roles = [role], users = [user])
    condition = ConditionRole(role)
    user.guild_profiles[guild_id] = GuildProfile(role_ids = [role.id])
    
    output = condition(user)
    vampytest.assert_instance(output, bool)
    vampytest.assert_eq(output, True)


def test__ConditionRole__call__failing():
    """
    Tests whether ``ConditionRole.__call__`` works as intended.
    
    Case: failing.
    """
    role = Role.precreate(202412010018)
    condition = ConditionRole(role)
    user = User.precreate(202412010019, name = 'brain')
    
    output = condition(user)
    vampytest.assert_instance(output, bool)
    vampytest.assert_eq(output, False)
