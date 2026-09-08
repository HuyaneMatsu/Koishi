import vampytest

from ...adventure_core import adventure_create

from ..content_building import produce_adventure_view_description_finalized


def _iter_options():
    adventure = adventure_create(
        202508030003,
        0,
        0,
        0,
        0,
        0,
        130,
        140,
    )
    adventure.created_at = 1463184000
    adventure.updated_at = 1463184000 + 5 * 3600 + 30 * 60
    adventure.health_exhausted = 20
    adventure.energy_exhausted = 30
    
    yield (
        adventure,
        (
            'Departed at: 2016-05-14 00:00:00 UTC\n'
            'Used health: 20 / 130\n'
            'Used energy: 30 / 140\n'
            'Total duration: 5 hours, 30 minutes\n'
            'Recovery time: 6 hours, 20 minutes'
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__produce_adventure_view_description_finalized(adventure):
    """
    Tests whether ``produce_adventure_view_description_finalized`` works as intended.
    
    Parameters
    ----------
    adventure : ``Adventure``
        Adventure to produce description for.
    
    Returns
    -------
    output : `str`
    """
    output = [*produce_adventure_view_description_finalized(adventure)]
    
    for element in output:
        vampytest.assert_instance(element, str)
    
    return ''.join(output)
