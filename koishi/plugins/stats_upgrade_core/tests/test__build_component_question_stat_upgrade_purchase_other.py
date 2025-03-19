import vampytest

from hata import Component
from hata.ext.slash import Button, Row

from ..component_builders import build_component_question_stat_upgrade_purchase_other
from ..constants import EMOJI_NO, EMOJI_YES


def _iter_options():
    user_id = 202503160000
    
    yield (
        user_id,
        2,
        Row(
            Button(
                'Yes',
                EMOJI_YES,
                custom_id = 'stats.upgrade.confirm.other.2f262100c0.2',
            ),
            Button(
                'No',
                EMOJI_NO,
                custom_id = 'stats.upgrade.cancel.other.2f262100c0.2',
            ),
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_component_question_stat_upgrade_purchase_other(user_id, stat_index):
    """
    tests whether ``build_component_question_stat_upgrade_purchase_other`` works as intended.
    
    Parameters
    ----------
    user_id : `int`
        The user's identifier.
    
    stat_index : `int`
        The stat's index.
    
    Returns
    -------
    output : ``Component``
    """
    output = build_component_question_stat_upgrade_purchase_other(user_id, stat_index)
    vampytest.assert_instance(output, Component)
    return output
