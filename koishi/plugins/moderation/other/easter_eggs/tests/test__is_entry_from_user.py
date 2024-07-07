import vampytest
from hata import AuditLogEntry, User

from ..shared import is_entry_from_user


def _iter_options():
    user_id_0 = 202407050335
    user_id_1 = 202407050336
    
    user_0 = User.precreate(user_id_0)
    
    yield (
        AuditLogEntry.precreate(
            202407050337,
            user_id = user_id_0,
            reason = None,
        ),
        user_0,
        True,
    )
    
    yield (
        AuditLogEntry.precreate(
            202407050338,
            user_id = user_id_1,
            reason = None,
        ),
        user_0,
        False,
    )
    
    yield (
        AuditLogEntry.precreate(
            202407050339,
            user_id = user_id_1,
            reason = f'Requested by: Orin [{user_id_0!s}]',
        ),
        user_0,
        True,
    )
    
    yield (
        AuditLogEntry.precreate(
            202407050340,
            user_id = user_id_1,
            reason = f'Requested by: Orin [{user_id_1!s}]',
        ),
        user_0,
        False,
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__is_entry_from_user(entry, user):
    """
    Tests whether ``is_entry_from_user`` works as intended.
    
    Parameters
    ----------
    entry : ``AuditLogEntry``
        The audit log entry to check.
    user : ``ClientUserBase``
        The respective user.
    
    Returns
    -------
    output : `bool`
    """
    output = is_entry_from_user(entry, user)
    vampytest.assert_instance(output, bool)
    return output
