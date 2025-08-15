import vampytest
from hata import Guild, GuildBadge, User

from ..guild_badge import ConditionGuildBadge


def _assert_fields_set(condition):
    """
    Asserts whether the given condition has all of its fields set.
    
    Parameters
    ----------
    condition : ``ConditionGuildBadge``
        The instance to check.
    """
    vampytest.assert_instance(condition, ConditionGuildBadge)
    vampytest.assert_instance(condition.guild, Guild)


def test__ConditionGuildBadge__new():
    """
    Tests whether ``ConditionGuildBadge.__new__`` works as intended.
    """
    guild_id = 202507120000
    guild = Guild.precreate(guild_id)
    
    condition = ConditionGuildBadge(guild)
    _assert_fields_set(condition)
    
    vampytest.assert_is(condition.guild, guild)


def test__ConditionGuildBadge__repr():
    """
    Tests whether ``ConditionGuildBadge.__repr__`` works as intended.
    """
    guild_id = 202507120001
    guild = Guild.precreate(guild_id)
    
    condition = ConditionGuildBadge(guild)
    
    output = repr(condition)
    vampytest.assert_instance(output, str)
    
    vampytest.assert_in(type(condition).__name__, output)
    vampytest.assert_in(f' guild = {guild!r}', output)


def test__ConditionGuildBadge__hash():
    """
    Tests whether ``ConditionGuildBadge.__hash__`` works as intended.
    """
    guild_id = 202507120002
    guild = Guild.precreate(guild_id)
    
    condition = ConditionGuildBadge(guild)
    
    output = hash(condition)
    vampytest.assert_instance(output, int)


def _iter_options__eq():
    guild = Guild.precreate(202507120003)
    
    keyword_parameters = {
        'guild': guild,
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
            'guild': Guild.precreate(202507120004),
        },
        False,
    )
    
    
@vampytest._(vampytest.call_from(_iter_options__eq()).returning_last())
def test__ConditionGuildBadge__eq(keyword_parameters_0, keyword_parameters_1):
    """
    Tests whether ``ConditionGuildBadge.__eq__`` works as intended.
    
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
    condition_0 = ConditionGuildBadge(**keyword_parameters_0)
    condition_1 = ConditionGuildBadge(**keyword_parameters_1)
    
    output = condition_0 == condition_1
    vampytest.assert_instance(output, bool)
    return output


def test__ConditionGuildBadge__call__passing():
    """
    Tests whether ``ConditionGuildBadge.__call__`` works as intended.
    
    Case: passing.
    """
    guild_id = 202507120007
    guild = Guild.precreate(guild_id)
    guild_badge = GuildBadge(guild_id = guild_id)
    user = User.precreate(202507120006, name = 'brain', primary_guild_badge = guild_badge)
    
    condition = ConditionGuildBadge(guild)
    
    output = condition(user)
    vampytest.assert_instance(output, bool)
    vampytest.assert_eq(output, True)


def test__ConditionGuildBadge__call__failing():
    """
    Tests whether ``ConditionGuildBadge.__call__`` works as intended.
    
    Case: failing.
    """
    guild_id = 202507120008
    guild = Guild.precreate(guild_id)
    user = User.precreate(202507120009, name = 'brain')
    
    condition = ConditionGuildBadge(guild)
    
    output = condition(user)
    vampytest.assert_instance(output, bool)
    vampytest.assert_eq(output, False)
