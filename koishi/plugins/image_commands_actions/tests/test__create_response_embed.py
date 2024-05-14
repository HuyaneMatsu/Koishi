import vampytest
from hata import Guild, User, Role, Color, GuildProfile, Embed
from ..action import create_response_embed
from ...image_handling_core import ImageDetailStatic, ImageHandlerStatic


def _iter_options():
    guild_id = 202405140000
    client_id = 202405140001
    user_id = 202405140002
    role_id = 202405140003
    color = Color(123)
    client = User.precreate(client_id)
    user = User.precreate(user_id)
    role = Role.precreate(role_id, color = color, guild_id = guild_id)
    client.guild_profiles[guild_id] = GuildProfile(role_ids = [])
    user.guild_profiles[guild_id] = GuildProfile(role_ids = [role_id])
    
    url = 'https://orindance.party/'
    image_detail = ImageDetailStatic(url).with_creator('miau')
    
    yield (
        client,
        guild_id,
        user,
        {client},
        True,
        None,
        [role],
        Embed(color = color, description = '*Could not get any images, please try again later.*'),
    )
    
    yield (
        client,
        guild_id,
        user,
        set(),
        False,
        None,
        [role],
        Embed(color = Color(0), description = '*Could not get any images, please try again later.*'),
    )
    
    yield (
        client,
        guild_id,
        user,
        {client},
        True,
        image_detail,
        [role],
        Embed(color = color).add_image(url).add_footer('By miau.'),
    )
    
    yield (
        client,
        guild_id,
        user,
        set(),
        False,
        image_detail,
        [role],
        Embed(color = Color(0)).add_image(url).add_footer('By miau.'),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__create_response_embed(client, guild_id, source_user, targets, client_in_users, image_detail, extra):
    """
    Tests whether ``create_response_embed`` works as intended.
    
    Parameters
    ----------
    client : ``ClientUserBase``
        The client who received the event.
    guild_id : `int`
        The guild's identifier where the command was called from.
    source_user : ``ClientUserBase``
        The user source user who invoked the event.
    targets : `set<Role | ClientUserBase>`
        Target entities.
    client_in_users : `bool`
        Whether the client is in the mentioned users.
    allowed_mentions : `list<ClientUserBase>`
        The allowed mentions.
    extra : `list<object>`
        Additional objects to keep in the cache.
    
    Returns
    -------
    output : ``Embed``
    """
    output = create_response_embed(client, guild_id, source_user, targets, client_in_users, image_detail)
    vampytest.assert_instance(output, Embed)
    return output
