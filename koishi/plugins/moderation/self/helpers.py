__all__ = ()

from hata import Embed
from hata.ext.slash import Form, TextInput, TextInputStyle, abort


def check_required_permissions(client, event, guild, required_permission, word_config):
    """
    Checks whether the permissions requirements are met.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    
    event : ``InteractionEvent``
        The received interaction event.
    
    guild : ``Guild``
        The guild where the action would be executed.
    
    required_permission : ``Permission``
        The required permissions to execute the action.
    
    word_config : ``WordConfig``
        Words to use for filling up the error messages about the action to be executed.
    """
    if guild is None:
        abort('Guild only command.')
    
    if not (guild.cached_permissions_for(client) & required_permission):
        abort(f'{client.name_at(guild)} cannot {word_config.name} in the guild.')
    
    if not client.has_higher_role_than_at(event.user, guild):
        abort(f'I must have higher role than you to {word_config.name} you.')


def check_user_remove_safety(event):
    """
    Checks whether removing the event's user would not damage the guild.
    
    Parameters
    ----------
    event : ``InteractionEvent``
        The received interaction event.
    """
    if event.user.is_boosting(event.guild_id):
        abort(f'Action forbidden for boosters.')


def build_action_completed_embed(user, embed_builder, word_config, *position_parameters):
    """
    Builds an action done embed.
    
    Parameters
    ----------
    user : ``ClientUserBase``
        The user on who the action was executed..
    embed_builder : `FunctionType``
        Base embed builder.
    word_config : ``WordConfig``
        Words to use for filling up the error messages about the action to be executed.
    *position_parameters : Positional parameters
        Additional positional parameters to pass to the embed builder.
    
    Returns
    -------
    embed : ``Embed``
    """
    return embed_builder(
        user,
        'Hecatia yeah!',
        f'**{user.full_name}** has self-{word_config.to_be} themselves.',
        *position_parameters,
    )


def create_response_form(title, reason_name, custom_id):
    """
    Creates a response form confirming the user's decision and inputting their reason why they want to suffer.
    
    Parameters
    ----------
    title : `str`
        The form's title.
    reason_name : `str`
        The reason name. Should be already capitalised.
    custom_id : `str`
        The form's custom id.
    
    Returns
    -------
    form : ``InteractionForm``
    """
    return  Form(
        title,
        [
            TextInput(
                'Reason',
                max_length = 512,
                custom_id = 'reason',
                placeholder = f'{reason_name} reason',
                style = TextInputStyle.paragraph,
            ),
        ],
        custom_id = custom_id,
    )
