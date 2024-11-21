import vampytest

from hata import Embed, ICON_TYPE_STATIC, Icon, User

from ...shared_constants import WORD_CONFIG__MUTE

from ..helpers import build_action_completed_embed
from ..mute import build_mute_embed


def _iter_options():
    user_id = 202411170001
    user_name = 'mayumi'
    user = User.precreate(user_id, avatar = Icon(ICON_TYPE_STATIC, 2), name = user_name)
    
    yield (
        user,
        build_mute_embed,
        WORD_CONFIG__MUTE,
        'hello',
        'because i said so',
        True,
        '2 weeks',
        False,
        Embed(
            'Hecatia yeah!', 
            '**mayumi** has been muted.',
        ).add_thumbnail(
            user.avatar_url,
        ).add_field(
            'Duration',
            (
                '```\n'
                '2 weeks\n'
                '```'
            ),
            inline = True
        ).add_field(
            'Notify user',
            (
                '```\n'
                'true\n'
                '```'
            ),
            inline = True
        ).add_field(
            'Reason',
            (
                '```\n'
                'because i said so\n'
                '```'
            ),
            inline = True
        ).add_footer(
            'hello',
        )
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_action_completed_embed(user, embed_builder, word_config, note, *position_parameters):
    """
    Tests whether ``build_action_completed_embed`` works as intended.
    
    Parameters
    ----------
    user : ``ClientUserBase``
        The user on who the action was executed.
    
    embed_builder : `FunctionType``
        Base embed builder.
    
    word_config : ``WordConfig``
        Words to use for filling up the error messages about the action to be executed.
    
    note : `None | str`
        Note to set to the message.
    
    *position_parameters : Positional parameters
        Additional positional parameters to pass to the embed builder.
    
    Returns
    -------
    output : ``Embed``
    """
    output = build_action_completed_embed(user, embed_builder, word_config, note, *position_parameters)
    vampytest.assert_instance(output, Embed)
    return output
