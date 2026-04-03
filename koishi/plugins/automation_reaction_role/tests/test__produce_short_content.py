import vampytest

from hata import Embed, Message

from ..component_builders import produce_short_content


def _iter_options():
    yield (
        Message.precreate(
            202509250000,
        ),
        '',
    )
    
    yield (
        Message.precreate(
            202509250001,
            content = 'hello',
        ),
        'hello',
    )
    
    yield (
        Message.precreate(
            202509250002,
            embeds = [
                Embed(
                    'a' * 150,
                    'b' * 20,
                ).add_field(
                    'c' * 40,
                    'd' * 10,
                ),
            ],
        ),
        ''.join([
            'a' * 150,
            '\n\n',
            'b' * 20,
            '\n\n',
            'c' * 40,
        ])
    )
    
    yield (
        Message.precreate(
            202509250003,
            content = 'h' * 300,
        ),
        ''.join([
            'h' * (250 - 3),
            '...',
        ]),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__produce_short_content(message):
    """
    Tests whether ``produce_short_content`` works as intended.
    
    Parameters
    ----------
    message : ``Message``
        Message to test with.
    
    Returns
    -------
    output : `str`
    """
    output = [*produce_short_content(message)]
    
    for element in output:
        vampytest.assert_instance(element, str)
    
    return ''.join(output)
