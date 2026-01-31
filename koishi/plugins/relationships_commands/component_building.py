__all__ = ()

from hata import (
    ButtonStyle, InteractionForm, StringSelectOption, create_button, create_row, create_section, create_separator,
    create_string_select, create_text_display, create_thumbnail_media
)

from ...bot_utils.constants import EMOJI__HEART_CURRENCY

from ..relationship_divorces_core import build_component_invoke_relationship_divorces_decrement_purchase_self
from ..relationships_core import (
    CUSTOM_ID_RELATIONSHIPS_REQUEST_DETAILS_BUILDER, RELATIONSHIP_TYPE_MAMA, RELATIONSHIP_TYPE_MISTRESS,
    RELATIONSHIP_TYPE_SISTER_BIG, RELATIONSHIP_TYPE_UNSET, RELATIONSHIP_TYPE_WAIFU, calculate_relationship_value
)
from ..user_settings import USER_SETTINGS_CUSTOM_ID_NOTIFICATION_PROPOSAL_DISABLE

from .constants import (
    ACTION_NAME_UNKNOWN, EMOJI_CLOSE, EMOJI_PAGE_DECREMENT, EMOJI_PAGE_INCREMENT, PAGE_SIZE_DEFAULT,
    RELATIONSHIP_LISTING_MODE_LEGACY, RELATIONSHIP_LISTING_MODE_LONG, RELATIONSHIP_LISTING_MODE_WIDE
)
from .content_building import (
    produce_break_up_success_description, produce_relationship_listing_footer, produce_relationship_listing_header,
    produce_relationship_request_accepted_description,
    produce_relationship_request_cancellation_notification_description,
    produce_relationship_request_cancelled_description, produce_relationship_request_creation_notification_description,
    produce_relationship_request_header, produce_relationship_request_rejected_description
)
from .custom_ids import (
    CUSTOM_ID_RELATIONSHIPS_BREAK_UP_BUILDER, CUSTOM_ID_RELATIONSHIPS_CLOSE_BUILDER,
    CUSTOM_ID_RELATIONSHIPS_MODE_BUILDER, CUSTOM_ID_RELATIONSHIPS_REQUEST_CLOSE_BUILDER,
    CUSTOM_ID_RELATIONSHIPS_REQUEST_VIEW_BUILDER, CUSTOM_ID_RELATIONSHIPS_REQUEST_VIEW_DECREMENT_DISABLED,
    CUSTOM_ID_RELATIONSHIPS_REQUEST_VIEW_INCREMENT_DISABLED, CUSTOM_ID_RELATIONSHIPS_VIEW_BUILDER,
    CUSTOM_ID_RELATIONSHIPS_VIEW_DECREMENT_DISABLED, CUSTOM_ID_RELATIONSHIPS_VIEW_INCREMENT_DISABLED,
    CUSTOM_ID_RELATIONSHIP_REQUEST_ACCEPT_BUILDER, CUSTOM_ID_RELATIONSHIP_REQUEST_CANCEL_BUILDER,
    CUSTOM_ID_RELATIONSHIP_REQUEST_REJECT_BUILDER
)
from .relationship_listing_rendering_legacy import (
    create_relationship_listing_pages_legacy, produce_relationships_listing_page_legacy
)
from .relationship_listing_rendering_long import (
    create_relationship_listing_pages_long, produce_relationships_listing_page_long
)
from .relationship_listing_rendering_wide import (
    create_relationship_listing_pages_wide, produce_relationships_listing_page_wide
)


def build_break_up_confirmation_form(target_user, guild_id):
    """
    Creates a break-up confirmation form.
    
    Parameters
    ----------
    target_user : ``ClientUserBase``
        The user to be broke up with.
    
    guild_id : `int`
        The local guild's identifier.
    
    Returns
    --------
    interaction_form : ``InteractionForm``
    """
    return InteractionForm(
        'Break up confirmation',
        [
            create_text_display(
                f'Are you sure to break up with {target_user.name_at(guild_id)}?'
            ),
        ],
        custom_id = CUSTOM_ID_RELATIONSHIPS_BREAK_UP_BUILDER(target_user.id),
    )


def build_break_up_success_components(target_user, source_received, target_received, guild_id):
    """
    Builds break up success components.
    
    Parameters
    ----------
    target_user : ``ClientUserBase``
        The user to divorce.
    
    source_received : `int`
        The amount of balance the source user received.
    
    target_received : `int`
        The amount of balance the target user received.
    
    guild_id : `int`
        The respective guild's identifier.
    
    Returns
    -------
    components : ``list<Component>``
    """
    return [
        create_text_display(
            ''.join([*produce_break_up_success_description(target_user, source_received, target_received, guild_id)])
        ),
        create_row(
            build_component_invoke_relationship_divorces_decrement_purchase_self(),
        ),
    ]


def build_update_unset_success_components(relationship_type, target_user, guild_id):
    """
    Builds update unset success components.
    
    Parameters
    ----------
    relationship_type : `int`
        The relationship's type.
    
    target_user : ``ClientUserBase``
        The targeted user. May be actually the source user if the relationship is reversed.
    
    guild_id : `int`
        The respective guild's identifier.
    
    Returns
    -------
    components : ``list<Component>``
    """
    if relationship_type == RELATIONSHIP_TYPE_WAIFU:
        concept = 'waifu'
    elif relationship_type == RELATIONSHIP_TYPE_SISTER_BIG:
        concept = 'big sister'
    elif relationship_type == RELATIONSHIP_TYPE_MAMA:
        concept = 'mama'
    elif relationship_type == RELATIONSHIP_TYPE_MISTRESS:
        concept = 'mistress'
    else:
        concept = ACTION_NAME_UNKNOWN
    
    return [
        create_text_display(
            f'You have become the {concept} of {target_user.name_at(guild_id)}.'
        ),
    ]


def build_request_created_success_components(relationship_type, investment, target_user, guild_id):
    """
    Builds request created success components.
    
    Parameters
    ----------
    relationship_type : `int`
        The requested relation type.
    
    investment : `int`
        The amount of balance to propose with.
    
    target_user : ``ClientUserBase``
        The user who is the target of the proposal.
    
    guild_id : `int`
        The respective guild's identifier.
    
    Returns
    -------
    components : ``list<Component>``
    """
    if relationship_type == RELATIONSHIP_TYPE_WAIFU:
        concept = 'a marriage proposal'
    elif relationship_type == RELATIONSHIP_TYPE_SISTER_BIG:
        concept = 'a blood-pact request'
    elif relationship_type == RELATIONSHIP_TYPE_MAMA:
        concept = 'an adoption agreement'
    elif relationship_type == RELATIONSHIP_TYPE_MISTRESS:
        concept = 'an employment contract'
    else:
        concept = ACTION_NAME_UNKNOWN
    
    return [
        create_text_display(
            f'You sent {concept} to {target_user.name_at(guild_id)} '
            f'with {investment} {EMOJI__HEART_CURRENCY}'
        ),
    ]


def build_relationship_request_listing_components(
    user, outgoing, relationship_request_listing, users, guild_id, page_index
):
    """
    Builds a relationship request listing components.
    
    Parameters
    ----------
    user : ``ClientUserbase``
        The invoking user.
    
    outgoing : `bool`
        Whether redirect to outgoing requests.
    
    relationship_request_listing : ``None | list<RelationshipRequest>``
        The relationship requests. They should not be chopped before calling this function.
    
    users : ``None | list<ClientUserBase>``
        The requested user for each relationship.
    
    guild_id : `int`
        The respective guild's identifier.
    
    page_index : `int`
        The page's identifier to display.
    
    Returns
    -------
    components : ``list<Component>``
    """
    components = []
    
    # Header
    
    components.append(create_section(
        create_text_display(
            f'# {user.name_at(guild_id)}\'s {"outgoing" if outgoing else "incoming"} requests\n'
            f'\n'
            f'Page: {page_index + 1}'
        ),
        thumbnail = create_thumbnail_media(user.avatar_url_at(guild_id)),
    ))
    
    components.append(create_separator())
    
    # Listing

    if (
        (relationship_request_listing is not None) and
        (len(relationship_request_listing) > page_index * PAGE_SIZE_DEFAULT)
    ):
        # Group
        grouped_relationship_request_listing = {}
        
        for relationship_request in relationship_request_listing:
            relationship_type = relationship_request.relationship_type
            
            try:
                group = grouped_relationship_request_listing[relationship_type]
            except KeyError:
                group = []
                grouped_relationship_request_listing[relationship_type] = group
            
            if outgoing:
                user_id = relationship_request.target_user_id
            else:
                user_id = relationship_request.source_user_id
            
            try:
                target_user = next(user for user in users if user.id == user_id)
            except StopIteration as exception:
                raise RuntimeError(relationship_request_listing, users, user_id) from exception
            
            group.append(
                (target_user.name_at(guild_id), relationship_request.investment, relationship_request.entry_id)
            )
        
        # Create an ordered version
        for group in grouped_relationship_request_listing.values():
            group.sort()
        
        
        elements = []
        
        for relationship_type in (
            RELATIONSHIP_TYPE_WAIFU,
            RELATIONSHIP_TYPE_SISTER_BIG,
            RELATIONSHIP_TYPE_MAMA,
            RELATIONSHIP_TYPE_MISTRESS,
            RELATIONSHIP_TYPE_UNSET,
        ):
            try:
                group = grouped_relationship_request_listing[relationship_type]
            except KeyError:
                continue
            
            for user_name, investment, entry_id in group:
                elements.append((relationship_type, user_name, investment, entry_id))
        
        # Now we can iterate.
    
        for (
            relationship_type, user_name, investment, entry_id
        ) in (
            elements[page_index * PAGE_SIZE_DEFAULT : (page_index + 1) * PAGE_SIZE_DEFAULT]
        ):
            components.append(create_section(
                create_text_display(
                    ''.join([*produce_relationship_request_header(relationship_type, outgoing, user_name, investment)])
                ),
                thumbnail = create_button(
                    'Details',
                    custom_id = CUSTOM_ID_RELATIONSHIPS_REQUEST_DETAILS_BUILDER(user.id, outgoing, page_index, entry_id)
                )
            ))
    
        components.append(create_separator())
    
    # Control
    
    if not page_index:
        page_decrement_custom_id = CUSTOM_ID_RELATIONSHIPS_REQUEST_VIEW_DECREMENT_DISABLED
        page_decrement_enabled = False
    else:
        page_decrement_custom_id = CUSTOM_ID_RELATIONSHIPS_REQUEST_VIEW_BUILDER(user.id, outgoing, page_index - 1)
        page_decrement_enabled = True
    
    if (
        (relationship_request_listing is None) or
        (len(relationship_request_listing) <= (page_index + 1) * PAGE_SIZE_DEFAULT)
    ):
        page_increment_custom_id = CUSTOM_ID_RELATIONSHIPS_REQUEST_VIEW_INCREMENT_DISABLED
        page_increment_enabled = False
    else:
        page_increment_custom_id = CUSTOM_ID_RELATIONSHIPS_REQUEST_VIEW_BUILDER(user.id, outgoing, page_index + 1)
        page_increment_enabled = True
    
    components.append(
        create_row(
            create_button(
                f'Page {page_index}',
                EMOJI_PAGE_DECREMENT,
                custom_id = page_decrement_custom_id,
                enabled = page_decrement_enabled,
            ),
            create_button(
                f'Page {page_index + 2}',
                EMOJI_PAGE_INCREMENT,
                custom_id = page_increment_custom_id,
                enabled = page_increment_enabled,
            ),
            create_button(
                'Close',
                EMOJI_CLOSE,
                custom_id = CUSTOM_ID_RELATIONSHIPS_REQUEST_CLOSE_BUILDER(user.id),
            ),
        )
    )
    
    return components


def build_relationship_request_details_components(
    user, outgoing, relationship_request, target_user, guild_id, page_index
):
    """
    Builds a relationship request details components.
    
    Parameters
    ----------
    user : ``ClientUserbase``
        The invoking user.
    
    outgoing : `bool`
        Whether redirect to outgoing requests.
    
    relationship_request : ``RelationshipRequest``
        The relationship requests to display.
    
    target_user : ``ClientUserBase``
        The other user of the relationship request.
    
    guild_id : `int`
        The respective guild's identifier.
    
    page_index : `int`
        The page's identifier to display.
    
    Returns
    -------
    components : ``list<Component>``
    """
    components = []
    
    # Header
    
    components.append(create_text_display(
        ''.join([*produce_relationship_request_header(
            relationship_request.relationship_type,
            outgoing,
            target_user.name_at(guild_id),
            relationship_request.investment,
        )])
    ))
    components.append(create_separator())
    
    # Control
    
    if outgoing:
        action_components = (
            create_button(
                'Cancel',
                custom_id = CUSTOM_ID_RELATIONSHIP_REQUEST_CANCEL_BUILDER(
                    user.id, outgoing, page_index, relationship_request.entry_id
                ),
                style = ButtonStyle.red,
            ),
        )
    else:
        action_components = (
            create_button(
                'Accept',
                custom_id = CUSTOM_ID_RELATIONSHIP_REQUEST_ACCEPT_BUILDER(
                    user.id, outgoing, page_index, relationship_request.entry_id
                ),
                style = ButtonStyle.green,
            ),
            create_button(
                'Reject',
                custom_id = CUSTOM_ID_RELATIONSHIP_REQUEST_REJECT_BUILDER(
                    user.id, outgoing, page_index, relationship_request.entry_id
                ),
                style = ButtonStyle.red,
            ),
        )
    
    components.append(
        create_row(
            create_button(
                'Back to requests',
                custom_id = CUSTOM_ID_RELATIONSHIPS_REQUEST_VIEW_BUILDER(user.id, outgoing, page_index),
            ),
            *action_components,
            create_button(
                'Close',
                EMOJI_CLOSE,
                custom_id = CUSTOM_ID_RELATIONSHIPS_REQUEST_CLOSE_BUILDER(user.id),
            ),
        )
    )
    
    return components


def build_relationship_request_accepted_components(
    user_id, outgoing, relationship_request, source_user, guild_id, page_index
):
    """
    Builds relationship request accepted components.
    
    Parameters
    ----------
    user : ``ClientUserbase``
        The invoking user.
    
    outgoing : `bool`
        Whether redirect to outgoing requests.
    
    relationship_request : ``RelationshipRequest``
        The accepted relationship request.
    
    source_user : ``ClientUserBase``
        The user who is the source of the proposal.
    
    guild_id : `int`
        The respective guild's identifier.
    
    page_index : `int`
        The page's identifier to display.
    
    Returns
    -------
    components : ``list<Component>``
    """
    components = []
    
    # Description
    
    components.append(create_text_display(
        ''.join([*produce_relationship_request_accepted_description(
            relationship_request.relationship_type,
            relationship_request.investment,
            source_user,
            guild_id,
        )])
    ))
    components.append(create_separator())
    
    # Control
    
    components.append(
        create_row(
            create_button(
                'Back to requests',
                custom_id = CUSTOM_ID_RELATIONSHIPS_REQUEST_VIEW_BUILDER(user_id, outgoing, page_index),
            ),
            create_button(
                'Close',
                EMOJI_CLOSE,
                custom_id = CUSTOM_ID_RELATIONSHIPS_REQUEST_CLOSE_BUILDER(user_id),
            ),
        )
    )
    
    return components


def build_relationship_request_rejected_components(
    user_id, outgoing, relationship_request, source_user, guild_id, page_index
):
    """
    Builds relationship request rejected components.
    
    Parameters
    ----------
    user_id : `int`
        The invoking user's identifier.
    
    outgoing : `bool`
        Whether redirect to outgoing requests.
    
    relationship_request : ``RelationshipRequest``
        The rejected relationship request.
    
    source_user : ``ClientUserBase``
        The user who is the source of the proposal.
    
    guild_id : `int`
        The respective guild's identifier.
    
    page_index : `int`
        The page's identifier to display.
    
    Returns
    -------
    components : ``list<Component>``
    """
    components = []
    
    # Description
    
    components.append(create_text_display(
        ''.join([*produce_relationship_request_rejected_description(
            relationship_request.relationship_type,
            relationship_request.investment,
            source_user,
            guild_id,
        )])
    ))
    components.append(create_separator())
    
    # Control
    
    components.append(
        create_row(
            create_button(
                'Back to requests',
                custom_id = CUSTOM_ID_RELATIONSHIPS_REQUEST_VIEW_BUILDER(user_id, outgoing, page_index),
            ),
            create_button(
                'Close',
                EMOJI_CLOSE,
                custom_id = CUSTOM_ID_RELATIONSHIPS_REQUEST_CLOSE_BUILDER(user_id),
            ),
        )
    )
    
    return components


def build_relationship_request_creation_notification_components(
    source_user, relationship_request, target_user_id, guild_id
):
    """
    Builds relationship request creation notification components.
    
    Parameters
    ----------
    source_user : ``ClientUserbase``
        The user who created the relationship request.
    
    relationship_request : ``RelationshipRequest``
        The relationship requests to display.
    
    target_user_id : `int`
        The targeted user's identifier.
    
    guild_id : `int`
        The respective guild's identifier.
    
    Returns
    -------
    components : ``list<Component>``
    """
    components = []
    
    # Header
    
    components.append(create_text_display(
        ''.join([*produce_relationship_request_creation_notification_description(
            relationship_request.relationship_type,
            relationship_request.investment,
            source_user,
            guild_id,
        )])
    ))
    components.append(create_separator())
    
    # Control
    
    components.append(
        create_row(
            create_button(
                'Accept',
                custom_id = CUSTOM_ID_RELATIONSHIP_REQUEST_ACCEPT_BUILDER(
                    target_user_id, False, 0, relationship_request.entry_id
                ),
                style = ButtonStyle.green,
            ),
            create_button(
                'Reject',
                custom_id = CUSTOM_ID_RELATIONSHIP_REQUEST_REJECT_BUILDER(
                    target_user_id, False, 0, relationship_request.entry_id
                ),
                style = ButtonStyle.red,
            ),
            create_button(
                'I don\'t want notifs, nya!!',
                custom_id = USER_SETTINGS_CUSTOM_ID_NOTIFICATION_PROPOSAL_DISABLE,
            ),
        )
    )
    
    return components


def build_relationship_request_cancelled_components(
    user_id, outgoing, relationship_request, target_user, guild_id, page_index
):
    """
    Builds relationship request cancelled components.
    
    Parameters
    ----------
    user_id : `int`
        The invoking user's identifier.
    
    outgoing : `bool`
        Whether redirect to outgoing requests.
    
    relationship_request : ``RelationshipRequest``
        The cancelled relationship request.
    
    target_user : ``ClientUserBase``
        The user who is the target of the proposal.
    
    guild_id : `int`
        The respective guild's identifier.
    
    page_index : `int`
        The page's identifier to display.
    
    Returns
    -------
    components : ``list<Component>``
    """
    components = []
    
    # Description
    
    components.append(create_text_display(
        ''.join([*produce_relationship_request_cancelled_description(
            relationship_request.relationship_type,
            relationship_request.investment,
            target_user,
            guild_id,
        )])
    ))
    components.append(create_separator())
    
    # Control
    
    components.append(
        create_row(
            create_button(
                'Back to requests',
                custom_id = CUSTOM_ID_RELATIONSHIPS_REQUEST_VIEW_BUILDER(user_id, outgoing, page_index),
            ),
            create_button(
                'Close',
                EMOJI_CLOSE,
                custom_id = CUSTOM_ID_RELATIONSHIPS_REQUEST_CLOSE_BUILDER(user_id),
            ),
        )
    )
    
    return components


def build_relationship_request_cancellation_notification_components(
    source_user, relationship_request, guild_id
):
    """
    Builds relationship request cancellation notification components.
    
    Parameters
    ----------
    source_user : ``ClientUserBase``
        The user who is the source of the proposal.
    
    relationship_request : ``RelationshipRequest``
        The relationship requests to display.
    
    guild_id : `int`
        The respective guild's identifier.
    
    Returns
    -------
    components : ``list<Component>``
    """
    components = []
    
    # Header
    
    components.append(create_text_display(
        ''.join([*produce_relationship_request_cancellation_notification_description(
            relationship_request.relationship_type,
            relationship_request.investment,
            source_user,
            guild_id,
        )])
    ))
    components.append(create_separator())
    
    # Control
    
    components.append(
        create_row(
            create_button(
                'I don\'t want notifs, nya!!',
                custom_id = USER_SETTINGS_CUSTOM_ID_NOTIFICATION_PROPOSAL_DISABLE,
            ),
        )
    )
    
    return components


def build_relationship_listing_components(
    source_user,
    target_user,
    users,
    guild_id,
    target_user_balance,
    target_relationship_extension_traces,
    target_relationship_request_listing,
    relationship_listing_mode,
    page_index,
):
    """
    Builds components displaying the user's relationship listing.
    
    Parameters
    ----------
    source_user : ``ClientUserBase``
        The user who is listing the relationships.
    
    target_user : ``ClientUserBase``
        The user who's relationships are being listed.
    
    users : ``None | list<ClientUserBase>``
        The user entities the `target_user` has relationships with.
    
    guild_id : `int`
        The respective guild's identifier.
    
    target_user_balance : ``UserBalance``
        The targeted user's user balance.
    
    relationship_extension_traces : ``None | dict<int, RelationshipExtensionTrace>``
        Relationship extension traces to display.
    
    target_relationship_request_listing : `None | list<RelationshipProposal>`
        The outgoing relationship proposals of the targeted user.
    
    relationship_listing_mode : `int`
        The mode to render as.
    
    page_index : `int`
        The page's index to display.
    
    Returns
    -------
    components : ``list<Component>``
    """
    components = []
    
    # Pre-calculate some values we will need later.
    if target_relationship_extension_traces is None:
        direct_relationships = None
    else:
        direct_relationships = []
        for target_relationship_extension_trace in target_relationship_extension_traces.values():
            relationship_route = target_relationship_extension_trace.relationship_route
            if len(relationship_route) == 1:
                direct_relationships.append(relationship_route[0])
    
    relationship_value = calculate_relationship_value(
        target_user.id,
        target_user_balance.relationship_value,
        (None if direct_relationships is None else direct_relationships),
    )
    
    relationship_count = (0 if direct_relationships is None else len(direct_relationships))
    
    relationship_proposal_count = (
        0 if target_relationship_request_listing is None else len(target_relationship_request_listing)
    )
    
    # Header
    
    components.append(create_section(
        create_text_display(
            ''.join([*produce_relationship_listing_header(
                target_user,
                guild_id,
                relationship_value,
                target_user_balance.relationship_divorces,
                target_user_balance.relationship_slots,
                relationship_count,
                relationship_proposal_count,
                relationship_listing_mode,
                page_index,
            )])
        ),
        thumbnail = create_thumbnail_media(target_user.avatar_url_at(guild_id)),
    ))
    components.append(create_separator())
    
    # Add page content
    
    if relationship_listing_mode == RELATIONSHIP_LISTING_MODE_LEGACY:
        pager = create_relationship_listing_pages_legacy
        producer = produce_relationships_listing_page_legacy
    
    elif relationship_listing_mode == RELATIONSHIP_LISTING_MODE_LONG:
        pager = create_relationship_listing_pages_long
        producer = produce_relationships_listing_page_long
    
    elif relationship_listing_mode == RELATIONSHIP_LISTING_MODE_WIDE:
        pager = create_relationship_listing_pages_wide
        producer = produce_relationships_listing_page_wide
    
    else:
        pager = create_relationship_listing_pages_legacy
        producer = produce_relationships_listing_page_legacy
        
    
    pages = pager(target_relationship_extension_traces, users, guild_id)
    if (pages is not None) and (len(pages) > page_index):
        components.append(create_text_display(''.join([*producer(pages[page_index])])))
        components.append(create_separator())
    
    # Add footer
    
    while True:
        if (source_user is target_user):
            # Same, you cannot propose to yourself.
            break
        
        if (target_relationship_extension_traces is not None):
            try:
                relationship_extension_trace = target_relationship_extension_traces[source_user.id]
            except KeyError:
                pass
            else:
                if len(relationship_extension_trace.relationship_route) == 1:
                    # Already related, do not add footer, even if they actually can propose.
                    break
        
        components.append(create_text_display(
            ''.join([*produce_relationship_listing_footer(source_user, target_user, guild_id, relationship_value)])
        ))
        components.append(create_separator())
        break
    
    # Control
    
    if not page_index:
        page_decrement_custom_id = CUSTOM_ID_RELATIONSHIPS_VIEW_DECREMENT_DISABLED
        page_decrement_enabled = False
    else:
        page_decrement_custom_id = CUSTOM_ID_RELATIONSHIPS_VIEW_BUILDER(
            source_user.id, target_user.id, relationship_listing_mode, page_index - 1
        )
        page_decrement_enabled = True
    
    if ((pages is None) or (len(pages) <= (page_index + 1))):
        page_increment_custom_id = CUSTOM_ID_RELATIONSHIPS_VIEW_INCREMENT_DISABLED
        page_increment_enabled = False
    else:
        page_increment_custom_id = CUSTOM_ID_RELATIONSHIPS_VIEW_BUILDER(
            source_user.id, target_user.id, relationship_listing_mode, page_index + 1
        )
        page_increment_enabled = True
    
    components.append(create_row(
        create_string_select(
            [
                StringSelectOption(
                    format(RELATIONSHIP_LISTING_MODE_LEGACY, 'x'),
                    'Legacy',
                    default = (relationship_listing_mode == RELATIONSHIP_LISTING_MODE_LEGACY),
                ),
                StringSelectOption(
                    format(RELATIONSHIP_LISTING_MODE_LONG, 'x'),
                    'Long',
                    default = (relationship_listing_mode == RELATIONSHIP_LISTING_MODE_LONG),
                ),
                StringSelectOption(
                    format(RELATIONSHIP_LISTING_MODE_WIDE, 'x'),
                    'Wide',
                    default = (relationship_listing_mode == RELATIONSHIP_LISTING_MODE_WIDE),
                ),
            ],
            CUSTOM_ID_RELATIONSHIPS_MODE_BUILDER(source_user.id, target_user.id, page_index)
        )
    ))
    
    components.append(
        create_row(
            create_button(
                f'Page {page_index}',
                EMOJI_PAGE_DECREMENT,
                custom_id = page_decrement_custom_id,
                enabled = page_decrement_enabled,
            ),
            create_button(
                f'Page {page_index + 2}',
                EMOJI_PAGE_INCREMENT,
                custom_id = page_increment_custom_id,
                enabled = page_increment_enabled,
            ),
            create_button(
                'Close',
                EMOJI_CLOSE,
                custom_id = CUSTOM_ID_RELATIONSHIPS_CLOSE_BUILDER(source_user.id),
            ),
        )
    )
    
    return components
