import re
from math import ceil

from hata import Client, Embed, KOKORO, DATETIME_FORMAT_CODE
from hata.ext.slash import abort, Form, TextInput, TextInputStyle, InteractionResponse, Button, ButtonStyle, Row
from sqlalchemy.sql import select

from bot_utils.models import DB_ENGINE, TODO_TABLE, todo_model
from bot_utils.constants import GUILD__SUPPORT, ROLE__SUPPORT__TESTER


SLASH_CLIENT : Client

TODO_ENTRIES = {}

ENTRY_BY_ID_RP = re.compile('#(\d*)')

PARAMETER_ENTRY_NAME_ANNOTATION = ('str', 'The entry\'s name | Use # to search by id.')


class TODOEntry:
    __slots__ = ('entry_id', 'name', 'description', 'created_at', 'creator_id')
    
    def __init__(self, entry_id, name, description, created_at, creator_id):
        self.entry_id = entry_id
        self.name = name
        self.description = description
        self.created_at = created_at
        self.creator_id = creator_id
        
        TODO_ENTRIES[entry_id] = self


async def request_entries():
    async with DB_ENGINE.connect() as connector:
        response = await connector.execute(
            select(
                [
                    todo_model.id,
                    todo_model.name,
                    todo_model.description,
                    todo_model.created_at,
                    todo_model.creator_id,
                ]
            )
        )
        
        results = await response.fetchall()
        for result in results:
            TODOEntry(*result)


KOKORO.run(request_entries())


TODO_FORM_SUBMIT_CUSTOM_ID = 'todo.add.form'


TEXT_INPUT_NAME = TextInput(
    'Name',
    min_length = 2,
    max_length = 128,
    custom_id = 'name',
)

TEXT_INPUT_DESCRIPTION = TextInput(
    'Description',
    style = TextInputStyle.paragraph,
    min_length = 2,
    max_length = 1000,
    custom_id = 'description',
)


ADD_TODO_FORM = Form(
    'Add todo entry',
    [
        TEXT_INPUT_NAME,
        TEXT_INPUT_DESCRIPTION,
    ],
    custom_id = TODO_FORM_SUBMIT_CUSTOM_ID,
)


def _entry_id_sort_key(entry):
    return entry.entry_id


def _entry_sot_key_by_value(entry, value):
    index = entry.name.casefold().find(value)
    if index != -1:
        return 0, index
    
    index = entry.description.casefold().find(value)
    if index != -1:
        return 1, index
    
    return None

def _entry_by_value_sort_key(item):
    return item[0]


def _try_resolve_entries(value):
    if value is None:
        entries = sorted(TODO_ENTRIES.values(), key=_entry_id_sort_key)
    
    else:
        parsed = ENTRY_BY_ID_RP.fullmatch(value)
        if parsed is None:
            to_sort = []
            value = value.casefold()
            for entry in TODO_ENTRIES.values():
                sort_key = _entry_sot_key_by_value(entry, value)
                if sort_key is not None:
                    to_sort.append((sort_key, entry))
            
            to_sort.sort(key=_entry_by_value_sort_key)
            
            entries = [item[1] for item in to_sort]
        else:
            entry_id = parsed.group(1)
            if entry_id:
                entry_id = int(entry_id)
                try:
                    entry = TODO_ENTRIES[entry_id]
                except KeyError:
                    entries = []
                else:
                    entries = [entry]
            else:
                entries = sorted(TODO_ENTRIES.values(), key=_entry_id_sort_key)
    
    return entries


def try_resolve_entry(name):
    entries = _try_resolve_entries(name)
    if not entries:
        abort('No entry found')
    
    return entries[0]


def has_permission(event):
    return event.user.has_role(ROLE__SUPPORT__TESTER)


def check_permission(event):
    if not has_permission(event):
        abort(f'{ROLE__SUPPORT__TESTER.name} only!')


def create_entry_embed(entry, user):
    return Embed(
        f'TODO entry #{entry.entry_id}',
    ).add_field(
        'By',
        (
            f'```\n'
            f'{user.full_name}\n'
            f'```'
        ),
        inline = True,
    ).add_field(
        'At',
        (
            f'```\n'
            f'{entry.created_at:{DATETIME_FORMAT_CODE}}\n'
            f'```'
        ),
        inline = True,
    ).add_field(
        'Name',
        (
            f'```\n'
            f'{entry.name}\n'
            f'```'
        ),
    ).add_field(
        'Description',
        (
            f'```\n'
            f'{entry.description}\n'
            f'```'
        ),
    ).add_thumbnail(
        user.avatar_url,
    )


TODO = SLASH_CLIENT.interactions(
    None,
    name = 'todo',
    description = 'Todo list for koishi',
    guild = GUILD__SUPPORT,
)


def _autocomplete_format_entry(entry):
    entry_name = entry.name
    if len(entry_name) > 60:
        entry_name = entry_name[:60]
        postfix = '...'
    else:
        postfix = ''
    
    return f'#{entry.entry_id} {entry_name}{postfix}', f'#{entry.entry_id}'


@TODO.autocomplete('name')
async def autocomplete_entry_name(value):
    return [_autocomplete_format_entry(entry) for entry in _try_resolve_entries(value)]


@TODO.interactions
async def add(event):
    """Adds a new todo entry!"""
    check_permission( event)
    return ADD_TODO_FORM


@SLASH_CLIENT.interactions(custom_id=TODO_FORM_SUBMIT_CUSTOM_ID, target='form')
async def todo_add_form_submit(
    event,
    *,
    name,
    description,
):
    created_at = event.created_at
    creator_id = event.user.id
    
    description = description.replace('`', '')
    
    async with DB_ENGINE.connect() as connector:
        response = await connector.execute(
            TODO_TABLE.insert().values(
                name = name,
                description = description,
                created_at = created_at,
                creator_id = creator_id,
            ).returning(
                todo_model.id,
            )
        )
        
        result = await response.fetchone()
        entry_id = result[0]
    
    entry = TODOEntry(entry_id, name, description, created_at, creator_id)
    
    embed = create_entry_embed(entry, event.user)
    embed.add_author('Entry created')
    return embed




@TODO.interactions
async def get(
    client,
    name: PARAMETER_ENTRY_NAME_ANNOTATION,
):
    """Shows the defined entry"""
    entry = try_resolve_entry(name)
    user = await client.user_get(entry.creator_id)
    return create_entry_embed(entry, user)


ENTRY_PER_PAGE = 10

@TODO.interactions
async def list_(
    page: 'number' = 1,
    creator: ('user', 'Filter by the creator of the entry') = None,
):
    """Lists to do entries"""
    if page < 0:
        abort('Page cannot be non-positive')
    
    if creator is None:
        entries = sorted(TODO_ENTRIES.values(), key=_entry_id_sort_key)
    else:
        creator_id = creator.id
        entries = [entry for entry in TODO_ENTRIES if entry.creator_id == creator_id]
        entries.sort(key=_entry_id_sort_key)
        
    page_count = ceil(len(entries) / ENTRY_PER_PAGE)
    
    # Fast precheck
    if page > page_count:
        description = None
    
    else:
        max_entry_index = ENTRY_PER_PAGE * page
        min_entry_index = max_entry_index - ENTRY_PER_PAGE
        
        entries = entries[min_entry_index: max_entry_index]
        
        description_parts = []
        
        index = 0
        limit = len(entries)
        while True:
            entry = entries[index]
            index += 1
            
            description_parts.append('**#')
            description_parts.append(str(entry.entry_id))
            description_parts.append('** : ')
            description_parts.append(entry.name)
            
            if index == limit:
                break
            
            description_parts.append('\n')
            continue
        
        description = ''.join(description_parts)
        description_parts = None # unallocate
    
    return Embed(
        'Todo entries',
        description,
    ).add_footer(
        f'Page {page} / {page_count}',
    )


DELETE_ENTRY_BASE = 'todo.del'
DELETE_ENTRY_RP = re.compile('todo\.del\.(\d+)\.([01])')


DELETE_ENTRY_APPROVE = Button(
    'FATALITY',
    style = ButtonStyle.red,
    custom_id = DELETE_ENTRY_BASE,
)

DELETE_ENTRY_CANCEL = Button(
    'Nah.',
    style = ButtonStyle.blue,
    custom_id = DELETE_ENTRY_BASE,
)

DELETE_ENTRY_COMPONENTS = Row(DELETE_ENTRY_APPROVE, DELETE_ENTRY_CANCEL)


@TODO.interactions
async def del_(
    client,
    event,
    name: PARAMETER_ENTRY_NAME_ANNOTATION,
):
    """Removes the defined entry."""
    check_permission(event)
    entry = try_resolve_entry(name)
    
    user = await client.user_get(entry.creator_id)
    embed = create_entry_embed(entry, user)
    embed.add_author('Are you sure to delete this entry?')
    
    return InteractionResponse(
        embed = embed,
        components = Row(
            DELETE_ENTRY_APPROVE.copy_with(custom_id=f'{DELETE_ENTRY_BASE}.{entry.entry_id}.1'),
            DELETE_ENTRY_CANCEL.copy_with(custom_id=f'{DELETE_ENTRY_BASE}.{entry.entry_id}.0'),
        )
    )


@SLASH_CLIENT.interactions(custom_id=DELETE_ENTRY_RP)
async def del_approval(
    client,
    event,
    entry_id,
    state,
):
    if not has_permission(event):
        return
    
    entry_id = int(entry_id)
    
    try:
        entry = TODO_ENTRIES[entry_id]
    except KeyError:
        abort('The entry was deleted meanwhile')
        return # do return, so the linter stops crying
    
    if state == '1':
        async with DB_ENGINE.connect() as connector:
            await connector.execute(
                TODO_TABLE.delete().where(
                    todo_model.id == entry.entry_id,
                )
            )
        
        del TODO_ENTRIES[entry.entry_id]
    
    
    user = await client.user_get(entry.creator_id)
    embed = create_entry_embed(entry, user)
    
    if state == '1':
        embed.add_author('Entry deleted')
    else:
        embed.add_author('Deleting entry cancelled')
    
    return InteractionResponse(embed=embed, components=None)


CUSTOM_ID_EDIT_BASE = 'todo.edit'
CUSTOM_ID_EDIT_RP = re.compile('todo\.edit\.(\d+)\.form')


@TODO.interactions
async def edit(
    event,
    name: PARAMETER_ENTRY_NAME_ANNOTATION,
):
    """Edit the defined entry!"""
    check_permission(event)
    entry = try_resolve_entry(name)
    
    if entry.creator_id != event.user.id:
        abort('You can edit only your own entries.')
    
    
    return Form(
        f'Editing todo entry #{entry.entry_id}',
        [
            TEXT_INPUT_NAME.copy_with(value=entry.name),
            TEXT_INPUT_DESCRIPTION.copy_with(value=entry.description),
        ],
        custom_id = f'{CUSTOM_ID_EDIT_BASE}.{entry.entry_id}.form',
    )


@SLASH_CLIENT.interactions(custom_id=CUSTOM_ID_EDIT_RP, target='form')
async def edit_form_submit(
    client,
    entry_id,
    *,
    name,
    description,
):
    entry_id = int(entry_id)
    
    description = description.replace('`', '')
    
    try:
        entry = TODO_ENTRIES[entry_id]
    except KeyError:
        abort('The entry was deleted meanwhile')
        return # do return, so the linter stops crying
    
    async with DB_ENGINE.connect() as connector:
        await connector.execute(
            TODO_TABLE.update(
                todo_model.id == entry.entry_id,
            ).values(
                name = name,
                description = description,
            )
        )
    
    entry.name = name
    entry.description = description
    
    user = await client.user_get(entry.creator_id)
    embed = create_entry_embed(entry, user)
    embed.add_author('Entry edited')
    return embed
