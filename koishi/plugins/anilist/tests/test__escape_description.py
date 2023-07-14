import vampytest

from ..parsers_description import escape_description


def _iter_options():
    # Nothing to escape
    yield None, None
    yield '', None
    yield 'koishi', 'koishi'
    yield 'koishi\nsatori', 'koishi\nsatori'
    
    # Check before and after
    yield 'a __aya__', 'a **aya**'
    yield '__aya__ a', '**aya** a'
    yield 'a __aya__ a', 'a **aya** a'
    
    # Check quotes
    yield '\'pepe\'', '\'pepe\''
    yield 'a \'pepe\' a', 'a \'pepe\' a'
    yield '\"pepe\"', '\"pepe\"'
    yield 'a \"pepe\" a', 'a \"pepe\" a'
    
    # Escapes
    yield 'aya__ya', 'aya**ya'
    yield 'aya~!ya', 'aya||ya'
    yield 'aya!~ya', 'aya||ya'
    yield 'aya<br><br>ya', 'aya\nya'
    yield 'aya<br>ya', 'aya\nya'
    yield 'aya<br/>ya', 'aya\nya'
    yield 'aya&#039ya', 'aya\'ya'
    yield 'aya<i>ya', 'aya*ya'
    yield 'aya</i>ya', 'aya*ya'
    yield 'aya<i/>ya', 'aya*ya'
    yield 'aya<em>ya', 'aya`ya'
    yield 'aya</em>ya', 'aya`ya'
    yield 'aya<em/>ya', 'aya`ya'
    
    # US shit
    yield '(56\')', None
    yield ' (56\')', None
    yield '(56\') ', None
    yield ' (56\') ', ' '
    yield '(56\'56\")', None


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__escape_description(description):
    """
    Tests whether ``escape_description`` works as intended.
    
    Parameters
    ----------
    description : `None`, `str`
        Input description to escape
    
    Returns
    -------
    escaped_description : `None`, `str`
    """
    return escape_description(description)
