import vampytest
from hata import AuditLogEntry, ClientUserBase, User

from ..helpers import get_source_user_from_client_entry


def _iter_options():
    user = User.precreate(202607260011)
    
    yield None, [user], None
    yield 'nyan', [user], None
    yield f'Suwako [{user.id}]', [user], user
    yield f'nyan\nSuwako [{user.id}]', [user], user 


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
async def test__get_source_user_from_client_entry(reason, users):
    """
    Tests whether ``get_source_user_from_client_entry`` works as intended.
    
    Parameters
    ----------
    reason : `None | str`
        Reason to create entry with.
    
    users : ``list<ClientUserBase>``
        Allowed users to be requested.
    
    Returns
    -------
    output : ``None | ClientUserBase``
    """
    audit_log_entry = AuditLogEntry(reason = reason)
    
    async def get_user_mocked(user_id):
        nonlocal users
        for user in users:
            if user_id == user.id:
                return user
        
        return None
    
    mocked = vampytest.mock_globals(
        get_source_user_from_client_entry,
        get_user = get_user_mocked,
    )
    
    output = await mocked(audit_log_entry)
    vampytest.assert_instance(output, ClientUserBase, nullable = True)
    return output
