import vampytest
from hata import ClientUserBase, User

from ..action import EMOJI_FLUSHED, produce_header_self


def _iter_options():
    user_id_0 = 202510080040
    
    user_0 = User.precreate(user_id_0)
    yield (
        None,
        'hugs',
        user_0,
        0.0,
        f'> {user_0.mention} hugs herself !!'
    )
    
    yield (
        'so true bestie',
        'hugs',
        user_0,
        1.0,
        f'> so true bestie; {user_0.mention} hugs themselves ?!'
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__produce_header_self(starter_text, verb, source_user, random_yield):
    """
    Tests whether ``produce_header_self`` works as intended.
    
    Parameters
    ----------
    starter_text : `None | str`
        Starter text to start the response with.
    
    verb : `str`
        The verb to use in the response.
    
    source_user : ``ClientUserBase``
        The user source user who invoked the event.
    
    random_yield : `float`
        Value to return from `random()` calls.
    
    Returns
    -------
    output : `str`
    """
    mocked = vampytest.mock_globals(
        produce_header_self,
        random = (lambda : random_yield),
    )
    output = [*mocked(starter_text, verb, source_user)]
    
    for element in output:
        vampytest.assert_instance(element, str)
    
    return ''.join(output)
