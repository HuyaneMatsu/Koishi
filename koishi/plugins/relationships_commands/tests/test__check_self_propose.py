import vampytest
from hata import Component, User, create_text_display

from ..checks import check_self_propose


def _iter_options():
    source_user = User.precreate(202501010010)
    target_user = User.precreate(202501010011)
    
    yield (
        source_user,
        target_user,
        None,
    )
    
    yield (
        source_user,
        source_user,
        [
            create_text_display('You cannot propose to yourself.'),
        ],
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__check_self_propose(source_user, target_user):
    """
    Tests whether ``check_self_propose`` works as intended.
    
    Parameters
    ----------
    source_user : ``ClientUserBase``
        The source user.
    
    target_user : ``ClientUserBase``
        The target user.
    
    Returns
    -------
    output : ``None | list<Component>`
    """
    output = check_self_propose(source_user, target_user)
    vampytest.assert_instance(output, list, nullable = True)
    
    if (output is not None):
        for element in output:
            vampytest.assert_instance(element, Component)
    
    return output
