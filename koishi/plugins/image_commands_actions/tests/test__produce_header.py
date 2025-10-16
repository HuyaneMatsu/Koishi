import vampytest
from hata import ClientUserBase, Role, User

from ..action import EMOJI_FLUSHED, produce_header


def _iter_options():
    user_id_0 = 202510080030
    user_id_1 = 202510080031
    user_id_2 = 202510080032
    user_id_3 = 202510080033
    
    role_id_0 = 202510080034
    
    user_0 = User.precreate(user_id_0)
    user_1 = User.precreate(user_id_1)
    user_2 = User.precreate(user_id_2)
    user_3 = User.precreate(user_id_3)
    
    role_0 = Role.precreate(role_id_0)
    
    yield (
        user_0,
        None,
        'hugs',
        user_1,
        [
            user_2,
            role_0,
            user_3,
        ],
        False,
        0.0,
        f'> {user_1.mention} hugs {user_2.mention}, {role_0.mention} and {user_3.mention}'
    )
    
    yield (
        user_0,
        None,
        'hugs',
        user_1,
        [],
        True,
        0.0,
        f'> {user_1.mention} hugs {user_0.mention}'
    )
    
    yield (
        user_0,
        'so true bestie',
        'hugs',
        user_1,
        [],
        True,
        1.0,
        f'> so true bestie; {user_1.mention} hugs me {EMOJI_FLUSHED}'
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__produce_header(client, starter_text, verb, source_user, targets, client_in_targets, random_yield):
    """
    Tests whether ``produce_header`` works as intended.
    
    Parameters
    ----------
    client : ``ClientUserBase``
        The client who received the event.
    
    starter_text : `None | str`
        Text to start the response with.
    
    verb : `str`
        The verb to use in the response.
    
    source_user : ``ClientUserBase``
        The user source user who invoked the event.
    
    targets : ``list<ClientUserBase | Role>``
        The mentioned users and roles by the event.
    
    client_in_targets : `bool`
        Whether the client is in the mentioned targets.
    
    random_yield : `float`
        Value to return from `random()` calls.
    
    Returns
    -------
    output : `str`
    """
    mocked = vampytest.mock_globals(
        produce_header,
        random = (lambda : random_yield),
    )
    output = [*mocked(client, starter_text, verb, source_user, targets, client_in_targets)]
    
    for element in output:
        vampytest.assert_instance(element, str)
    
    return ''.join(output)
