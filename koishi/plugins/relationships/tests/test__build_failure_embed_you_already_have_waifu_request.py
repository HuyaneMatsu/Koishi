import vampytest
from hata import Embed, GuildProfile, User

from ..embed_builders import build_failure_embed_you_already_have_waifu_request


def _iter_options():
    guild_id = 202412280030
    
    waifu_subject = User.precreate(202412280031, name = 'Koishi')
    waifu_subject.guild_profiles[guild_id] = GuildProfile(nick = 'Koi')
    
    user = User.precreate(202412280032, name = 'Satori')
    user.guild_profiles[guild_id] = GuildProfile(nick = 'Sato')
    
    yield (
        waifu_subject,
        user,
        0,
        Embed(
            'You already have a waifu request',
            (
                'What would Koishi say if they would know about Satori?'
            ),
        )
    )
    
    yield (
        waifu_subject,
        user,
        guild_id,
        Embed(
            'You already have a waifu request',
            (
                'What would Koi say if they would know about Sato?'
            ),
        )
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_failure_embed_you_already_have_waifu_request(waifu_subject, user, guild_id):
    """
    Tests whether ``build_failure_embed_you_already_have_waifu_request`` works as intended.
    
    Parameters
    ----------
    waifu_subject : ``ClientUserBase``
        The already requested waifu.
    
    user : ``ClientUserBase``
        The user who is the target of the proposal.
    
    guild_id : `int`
        The respective guild's identifier.
    
    Returns
    -------
    output : ``Embed``
    """
    output = build_failure_embed_you_already_have_waifu_request(waifu_subject, user, guild_id)
    vampytest.assert_instance(output, Embed)
    return output
