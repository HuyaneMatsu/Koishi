import vampytest
from hata import ClientUserBase, Role, User

from ..action import get_allowed_users


def _iter_options():
    user_id_0 = 202510080010
    user_id_1 = 202510080011
    user_id_2 = 202510080012
    
    role_id_0 = 202510080013
    
    user_0 = User.precreate(user_id_0)
    user_1 = User.precreate(user_id_1)
    user_2 = User.precreate(user_id_2)
    
    role_0 = Role.precreate(role_id_0)
    
    yield (
        user_0,
        user_1,
        (),
        (
            set(),
            False,
            False,
            [
                user_0,
                user_1,
            ],
        ),
    )
    
    yield (
        user_0,
        user_1,
        (
            None,
        ),
        (
            set(),
            False,
            False,
            [
                user_0,
                user_1,
            ],
        ),
    )
    
    yield (
        user_0,
        user_1,
        (
            user_0,
        ),
        (
            set(),
            True,
            False,
            [
                user_0,
                user_1,
            ],
        ),
    )
    
    yield (
        user_0,
        user_1,
        (
            user_1,
        ),
        (
            set(),
            False,
            True,
            [
                user_0,
                user_1,
            ],
        ),
    )
    
    yield (
        user_0,
        user_1,
        (
            user_2,
            role_0,
        ),
        (
            {
                user_2,
                role_0,
            },
            False,
            True,
            [
                user_0,
                user_1,
                user_2
            ],
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def get_allowed_users(client, source_user, input_targets):
    """
    Tests whether ``get_allowed_users`` works as intended.
    
    Parameters
    ----------
    client : ``ClientUserBase``
        The client who received the event.
    
    source_user : ``ClientUserBase``
        The user invoking the interaction.
    
    input_targets : ``tuple<None | Role | ClientUserBase>``
        The input users to the command.
    
    Returns
    -------
    targets : ``set<ClientUserBase | Role>``
        The mentioned users and roles by the event.
    
    client_in_users : `bool`
        Whether the client is in the mentioned users.
    
    user_in_users : `bool`
        Whether the user in in the mentioned users as well.
    
    allowed_mentions : ``list<ClientUserBase>``
        Allowed mentions.
    """
    output = get_allowed_users(client, source_user, input_targets)
    vampytest.assert_instance(output, tuple)
    vampytest.assert_eq(len(output), 4)
    
    targets, client_in_users, user_in_users, allowed_mentions = output
    
    vampytest.assert_instance(targets, set)
    for element in targets:
        vampytest.assert_instance(element, ClientUserBase, Role)
    
    vampytest.assert_instance(client_in_users, bool)
    vampytest.assert_instance(user_in_users, bool)
    
    vampytest.assert_instance(allowed_mentions, list)
    for element in targets:
        vampytest.assert_instance(element, ClientUserBase)
    
    return output
