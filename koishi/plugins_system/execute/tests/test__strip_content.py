import vampytest

from ..helpers import STRIP_STATE_EMPTY, STRIP_STATE_SUCCESS, STRIP_STATE_UNCLOSED, strip_content


def _iter_options():
    yield (
        '',
        (
            STRIP_STATE_EMPTY,
            None,
        ),
    )
    
    yield (
        '    \n\t   ',
        (
            STRIP_STATE_EMPTY,
            None,
        ),
    )
    
    yield (
        '`nyan`',
        (
            STRIP_STATE_SUCCESS,
            'nyan',
        ),
    )
    
    yield (
        '`nyan\n`',
        (
            STRIP_STATE_UNCLOSED,
            None,
        ),
    )
    
    yield (
        '`nyan',
        (
            STRIP_STATE_UNCLOSED,
            None,
        ),
    )
    
    yield (
        '```nyan```',
        (
            STRIP_STATE_SUCCESS,
            'nyan',
        ),
    )
    
    yield (
        '```\nnyan```',
        (
            STRIP_STATE_SUCCESS,
            'nyan',
        ),
    )
    
    yield (
        '```nyan\n```',
        (
            STRIP_STATE_SUCCESS,
            'nyan',
        ),
    )
    
    yield (
        '```python\nnyan\n```',
        (
            STRIP_STATE_SUCCESS,
            'nyan',
        ),
    )
    
    yield (
        '```py\nnyan\n```',
        (
            STRIP_STATE_SUCCESS,
            'nyan',
        ),
    )
    
    yield (
        '```\nnyan\n```',
        (
            STRIP_STATE_SUCCESS,
            'nyan',
        ),
    )
    
    yield (
        '```nyan``',
        (
            STRIP_STATE_UNCLOSED,
            None,
        ),
    )
    
    yield (
        '```nyan`',
        (
            STRIP_STATE_UNCLOSED,
            None,
        ),
    )
    
    yield (
        '```nyan',
        (
            STRIP_STATE_UNCLOSED,
            None,
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
async def test__strip_content(content):
    return strip_content(content)
