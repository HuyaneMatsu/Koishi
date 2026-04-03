import vampytest
from hata import Embed

from ..shared_helpers import add_reason_field


def _iter_options():
    yield Embed('Scarlet'), None, Embed('Scarlet').add_field('Reason', f'```\n \n```', inline = True)
    yield Embed('Scarlet'), 'Ban reimu', Embed('Scarlet').add_field('Reason', f'```\nBan reimu\n```', inline = False)


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__add_reason_field(embed, reason):
    """
    Tests whether ``add_reason_field`` works as intended.
    
    Parameters
    ----------
    embed : ``Embed``
        Embed to test with.
    reason : `None | str`
        Reason to add.
    
    Returns
    -------
    output : ``Embed``
    """
    embed = embed.copy()
    add_reason_field(embed, reason)
    return embed
