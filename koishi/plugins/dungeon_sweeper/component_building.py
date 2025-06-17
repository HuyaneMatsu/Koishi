__all__ = ()

from hata import (
    ButtonStyle, StringSelectOption, create_button, create_row, create_section, create_separator, create_string_select,
    create_text_display, create_thumbnail_media
)

from .chapter_rules import CHAPTER_RULE_DEFAULT
from .chapter_styles import EMOJI_UNKNOWN_AS_EMOJI
from .chapters import CHAPTER_DEFAULT
from .constants import (
    CHAPTER_RULES, CHAPTERS, DIFFICULTY_NAMES, DIFFICULTY_NAME_DEFAULT, EMOJI_KOISHI_WAVE, MAX_RENDER_EMOJI
)
from .custom_ids import (
    CUSTOM_ID_EMPTY_0, CUSTOM_ID_EMPTY_1, CUSTOM_ID_EMPTY_2, CUSTOM_ID_EMPTY_3, CUSTOM_ID_END_SCREEN_NEXT_STAGE,
    CUSTOM_ID_END_SCREEN_RESTART_STAGE, CUSTOM_ID_END_SCREEN_RETURN_TO_MENU, CUSTOM_ID_IN_GAME_BACK,
    CUSTOM_ID_IN_GAME_EAST, CUSTOM_ID_IN_GAME_EAST_TO_NORTH, CUSTOM_ID_IN_GAME_EAST_TO_SOUTH, CUSTOM_ID_IN_GAME_NORTH,
    CUSTOM_ID_IN_GAME_NORTH_TO_EAST, CUSTOM_ID_IN_GAME_NORTH_TO_WEST, CUSTOM_ID_IN_GAME_RESTART,
    CUSTOM_ID_IN_GAME_RETURN_TO_MENU, CUSTOM_ID_IN_GAME_SKILL, CUSTOM_ID_IN_GAME_SOUTH, CUSTOM_ID_IN_GAME_SOUTH_TO_EAST,
    CUSTOM_ID_IN_GAME_SOUTH_TO_WEST, CUSTOM_ID_IN_GAME_WEST, CUSTOM_ID_IN_GAME_WEST_TO_NORTH,
    CUSTOM_ID_IN_GAME_WEST_TO_SOUTH, CUSTOM_ID_IN_MENU_CHAPTER_NEXT, CUSTOM_ID_IN_MENU_CHAPTER_PREVIOUS,
    CUSTOM_ID_IN_MENU_CLOSE, CUSTOM_ID_IN_MENU_SELECT_STAGE, CUSTOM_ID_IN_MENU_STAGE_NEXT,
    CUSTOM_ID_IN_MENU_STAGE_NEXT_MULTI, CUSTOM_ID_IN_MENU_STAGE_PREVIOUS, CUSTOM_ID_IN_MENU_STAGE_PREVIOUS_MULTI
)
from .custom_ids import CUSTOM_ID_RULES_SELECT
from .helpers import (
    can_play_selected_stage, get_rating_for, get_selectable_stages
)
from .move_directions import (
    MOVE_DIRECTION_EAST, MOVE_DIRECTION_EAST_TO_NORTH, MOVE_DIRECTION_EAST_TO_SOUTH, MOVE_DIRECTION_NORTH,
    MOVE_DIRECTION_NORTH_TO_EAST, MOVE_DIRECTION_NORTH_TO_WEST, MOVE_DIRECTION_SOUTH, MOVE_DIRECTION_SOUTH_TO_EAST,
    MOVE_DIRECTION_SOUTH_TO_WEST, MOVE_DIRECTION_WEST, MOVE_DIRECTION_WEST_TO_NORTH, MOVE_DIRECTION_WEST_TO_SOUTH
)


def get_first_chapter():
    """
    Returns the first chapter.
    
    Returns
    -------
    chapter : ``Chapter``
    """
    for chapter in CHAPTERS.values():
        if (chapter is not CHAPTER_DEFAULT) and (not chapter.unlock_prerequisite_stage_id):
            return chapter
    
    return CHAPTER_DEFAULT


def iter_chapters_ordered():
    """
    Iterates over the chapters in order.
    
    This function is an iterable generator.
    
    Yields
    ------
    chapter : ``Chapter``
    """
    chapter = get_first_chapter()
    
    while True:
        yield chapter
        
        chapter = chapter.get_next_chapter()
        if chapter is None:
            break


def build_components_rules(chapter):
    """
    Builds role components for the given chapter.
    
    Parameters
    ----------
    chapter : ``None | Chapter``
        Chapter to build rule component for.
    
    Returns
    -------
    components : ``tuple<Component>``
    """
    if chapter is None:
        chapter = get_first_chapter()
        rule = CHAPTER_RULE_DEFAULT
    else:
        rule = CHAPTER_RULES.get(chapter.rule_id, CHAPTER_RULE_DEFAULT)
    
    style = chapter.get_style()
    
    # ---- description ----
    
    text_display_description = rule.component_builder(chapter, style)
    
    # ---- control ----
    
    select_control = create_string_select(
        (
            StringSelectOption(
                '0',
                'Rules',
                default = (rule is CHAPTER_RULE_DEFAULT),
            ),
            *(
                StringSelectOption(
                    str(chapter.id),
                    f'Chapter {chapter.display_name}',
                    default = (chapter.rule_id == rule.id),
                )
                for chapter in iter_chapters_ordered()
            ),
        ),
        custom_id = CUSTOM_ID_RULES_SELECT,
    )
    
    # ---- construct ----
    
    return (
        text_display_description,
        create_row(select_control),
    )


def build_component_tiles(style, map_, size_x):
    """
    Builds the map tiles displaying component.
    
    Parameters
    ----------
    style : ``ChapterStyle``
        Style to use for building.
    
    map_ : ``Stage``
        Stage.
    
    size_x : `int`
        The map's width.
    
    Returns
    -------
    component : ``Component``
    """
    tile_resolution_table = style.tile_resolution_table
    
    limit = len(map_)
    step = size_x
    
    if limit <= MAX_RENDER_EMOJI:
        start = 0
        shift = 0
    else:
        step_count = limit // step
        if step_count < step:
            if (step_count * (step - 2)) <= MAX_RENDER_EMOJI:
                start = 1
                step -= 2
                shift = 2
            else:
                start = step + 1
                limit -= step
                step -= 2
                shift = 2
        else:
            if ((step_count - 2) * step) <= MAX_RENDER_EMOJI:
                start = step
                limit -= step
                shift = 0
            else:
                start = step + 1
                limit -= step
                step -= 2
                shift = 2
    
    parts = []
    line_added = False
    
    while start < limit:
        end = start + step
        
        if line_added:
            parts.append('\n')
        else:
            line_added = True
        
        parts.extend(tile_resolution_table.get(element, EMOJI_UNKNOWN_AS_EMOJI) for element in map_[start : end])
        
        start = end + shift
    
    return create_text_display(''.join(parts))


def build_components_in_game(game_state):
    """
    Builds in game components for the given game state.
    
    Parameters
    ----------
    game_state : ``GameState``
        Game state to build components for.
    
    Returns
    -------
    components : ``tuple<Component>``
    """
    chapter = game_state.chapter
    style = chapter.get_style()
    control_emoji_mapping = style.control_emoji_mapping
    stage = game_state.stage
    map_ = game_state.map
    move_directions = game_state.get_directions()
    has_skill = game_state.has_skill
    next_skill = game_state.next_skill
    best = game_state.best
    steps = len(game_state.history)
    
    if has_skill and (not next_skill):
        can_activate_skill = chapter.get_skill().can_activate(game_state)
    else:
        can_activate_skill = False
    
    can_back_or_restart = game_state.can_back_or_restart()
    
    # ---- title ----
    
    text_display_title = create_text_display(
        f'Chapter {stage.chapter_id + 1} {style.emoji}, '
        f'{DIFFICULTY_NAMES.get(stage.difficulty_id, DIFFICULTY_NAME_DEFAULT)}: {stage.in_difficulty_index + 1}'
    )
    
    # ---- tiles ----
    
    text_display_tiles = build_component_tiles(style, map_, stage.size_x)
    
    # ---- footer ----
    
    text_display_footer = create_text_display(
        f'steps : {steps}' if (best == -1) else f'steps : {steps}, best : {best}'
    )
    
    #  ---- skill ----
    
    if next_skill:
        enabled = True
        button_style = ButtonStyle.green
        
    elif not has_skill:
        enabled = False
        button_style = ButtonStyle.gray
        
    elif can_activate_skill:
        enabled = True
        button_style = ButtonStyle.blue
        
    else:
        enabled = False
        button_style = ButtonStyle.blue
    
    button_skill = create_button(
        custom_id = CUSTOM_ID_IN_GAME_SKILL,
        emoji = style.emoji,
        enabled = enabled,
        style = button_style,
    )
    
    # ---- north ----
    
    if move_directions.get(MOVE_DIRECTION_NORTH):
        enabled = True
    else:
        enabled = False
    
    button_north = create_button(
        custom_id = CUSTOM_ID_IN_GAME_NORTH,
        emoji = control_emoji_mapping.in_game_north,
        enabled = enabled,
    )
    
    # ---- north-east ----
    
    if move_directions.get(MOVE_DIRECTION_NORTH_TO_EAST):
        custom_id = CUSTOM_ID_IN_GAME_NORTH_TO_EAST
        enabled = True
    elif move_directions.get(MOVE_DIRECTION_EAST_TO_NORTH):
        custom_id = CUSTOM_ID_IN_GAME_EAST_TO_NORTH
        enabled = True
    else:
        custom_id = CUSTOM_ID_EMPTY_0
        enabled = False
    
    button_north_east = create_button(
        emoji = control_emoji_mapping.in_game_north_east,
        custom_id = custom_id,
        enabled = enabled,
    )
    
    # ---- east ----
    
    if move_directions.get(MOVE_DIRECTION_EAST):
        enabled = True
    else:
        enabled = False
    
    button_east = create_button(
        custom_id = CUSTOM_ID_IN_GAME_EAST,
        emoji = control_emoji_mapping.in_game_east,
        enabled = enabled,
    )
    
    # --- south-east ----
    
    if move_directions.get(MOVE_DIRECTION_SOUTH_TO_EAST):
        custom_id = CUSTOM_ID_IN_GAME_SOUTH_TO_EAST
        enabled = True
    elif move_directions.get(MOVE_DIRECTION_EAST_TO_SOUTH):
        custom_id = CUSTOM_ID_IN_GAME_EAST_TO_SOUTH
        enabled = True
    else:
        custom_id = CUSTOM_ID_EMPTY_1
        enabled = False
    
    button_south_east = create_button(
        custom_id = custom_id,
        emoji = control_emoji_mapping.in_game_south_east,
        enabled = enabled,
    )
    
    # ---- south ----
    
    if move_directions.get(MOVE_DIRECTION_SOUTH):
        enabled = True
    else:
        enabled = False
    
    button_south = create_button(
        custom_id = CUSTOM_ID_IN_GAME_SOUTH,
        emoji = control_emoji_mapping.in_game_south,
        enabled = enabled,
    )
    
    # ---- south-west ----
    
    if move_directions.get(MOVE_DIRECTION_SOUTH_TO_WEST):
        custom_id = CUSTOM_ID_IN_GAME_SOUTH_TO_WEST
        enabled = True
    elif move_directions.get(MOVE_DIRECTION_WEST_TO_SOUTH):
        custom_id = CUSTOM_ID_IN_GAME_WEST_TO_SOUTH
        enabled = True
    else:
        custom_id = CUSTOM_ID_EMPTY_2
        enabled = False
    
    button_south_west = create_button(
        emoji = control_emoji_mapping.in_game_south_west,
        custom_id = custom_id,
        enabled = enabled,
    )
    
    # ---- west ----
    
    if move_directions.get(MOVE_DIRECTION_WEST):
        enabled = True
    else:
        enabled = False
    
    button_west = create_button(
        custom_id = CUSTOM_ID_IN_GAME_WEST,
        emoji = control_emoji_mapping.in_game_west,
        enabled = enabled,
    )
    
    
    # --- north-west ----
    
    if move_directions.get(MOVE_DIRECTION_NORTH_TO_WEST):
        custom_id = CUSTOM_ID_IN_GAME_NORTH_TO_WEST
        enabled = True
    elif move_directions.get(MOVE_DIRECTION_WEST_TO_NORTH):
        custom_id = CUSTOM_ID_IN_GAME_WEST_TO_NORTH
        enabled = True
    else:
        custom_id = CUSTOM_ID_EMPTY_3
        enabled = False
    
    button_north_west = create_button(
        custom_id = custom_id,
        emoji = control_emoji_mapping.in_game_north_west,
        enabled = enabled,
    )
    
    # ---- back ----
    
    button_back = create_button(
        custom_id = CUSTOM_ID_IN_GAME_BACK,
        emoji = control_emoji_mapping.in_game_back,
        enabled = can_back_or_restart,
        style = ButtonStyle.blue,
    )
    
    # ---- restart ----
    
    button_restart = create_button(
        custom_id = CUSTOM_ID_IN_GAME_RESTART,
        emoji = control_emoji_mapping.in_game_restart,
        enabled = can_back_or_restart,
        style = ButtonStyle.blue,
    )
    
    # ---- return-to-menu ----
    
    button_return_to_menu = create_button(
        emoji = control_emoji_mapping.in_game_return_to_menu,
        custom_id = CUSTOM_ID_IN_GAME_RETURN_TO_MENU,
        style = ButtonStyle.blue,
    )
    
    # ---- construct ----
    
    return (
        text_display_title,
        create_separator(),
        text_display_tiles,
        create_separator(),
        text_display_footer,
        create_row(
            button_north_west,
            button_north,
            button_north_east,
            button_back,
        ),
        create_row(
            button_west,
            button_skill,
            button_east,
            button_restart,
        ),
        create_row(
            button_south_west,
            button_south,
            button_south_east,
            button_return_to_menu,
        ),
    )


def build_components_end_screen(game_state):
    """
    Builds an end game components for the given game state.
    
    Parameters
    ----------
    game_state : ``GameState``
        Game state to build components for.
    
    Returns
    -------
    components : ``tuple<Component>``
    """
    chapter = game_state.chapter
    style = chapter.get_style()
    control_emoji_mapping = style.control_emoji_mapping
    stage = game_state.stage
    map_ = game_state.map
    best = game_state.best
    steps = len(game_state.history)
    
    # ---- title ----
    
    text_display_title = create_text_display(
        f'Chapter {stage.chapter_id + 1} {style.emoji} '
        f'{DIFFICULTY_NAMES.get(stage.difficulty_id, DIFFICULTY_NAME_DEFAULT)} {stage.in_difficulty_index + 1} '
        f'finished with {steps} steps with {get_rating_for(stage.best, steps)} rating!'
    )
    
    # ---- tiles ----
    
    text_display_tiles = build_component_tiles(style, map_, stage.size_x)

    # ---- footer ----
    
    text_display_footer = create_text_display(
        f'steps : {steps}, best : {best}'
    )
    
    # ---- back-to-menu ----
    
    button_return_to_menu = create_button(
        custom_id = CUSTOM_ID_END_SCREEN_RETURN_TO_MENU,
        emoji = control_emoji_mapping.end_screen_return_to_menu,
        style = ButtonStyle.blue,
    )
    
    # ---- restart-stage ----
    
    button_restart_stage = create_button(
        custom_id = CUSTOM_ID_END_SCREEN_RESTART_STAGE,
        emoji = control_emoji_mapping.end_screen_restart_stage,
        style = ButtonStyle.blue,
    )
    
    # ---- next-chapter ----
    
    button_next_chapter = create_button(
        custom_id = CUSTOM_ID_END_SCREEN_NEXT_STAGE,
        emoji = control_emoji_mapping.end_screen_next_stage,
        enabled = (stage.get_next_stage() is not None),
        style = ButtonStyle.blue,
    )
    
    # ---- construct ----
    
    return (
        text_display_title,
        create_separator(),
        text_display_tiles,
        create_separator(),
        text_display_footer,
        create_row(button_return_to_menu, button_restart_stage, button_next_chapter),
    )


def build_component_in_menu_description(chapter, selectable_stages):
    """
    Builds in menu description.
    
    Parameters
    ----------
    chapter : ``Chapter``
        The selected chapter.
    
    selectable_stages : ``None | list<(Stage, int, bool)>``
        The selectable stages in a list of tuples. Contains 3 elements: `stage` , `best`, `selected`.
    
    Returns
    -------
    component_in_menu_description : ``Component``
    """
    description_parts = []
    
    if selectable_stages is None:
        unlock_prerequisite_stage = chapter.get_unlock_prerequisite_stage()
        if unlock_prerequisite_stage is None:
            chapter = None
        else:
            chapter = unlock_prerequisite_stage.get_chapter()
        
        description_parts.append('**You must finish chapter ')
        
        if (chapter is None):
            description_parts.append('some')
        else:
            description_parts.append(chapter.display_name)
            description_parts.append(' ')
            description_parts.append(
                DIFFICULTY_NAMES.get(unlock_prerequisite_stage.difficulty_id, DIFFICULTY_NAME_DEFAULT)
            )
            description_parts.append(' ')
            description_parts.append(str(unlock_prerequisite_stage.in_difficulty_index + 1))
            description_parts.append(' first')
        
        description_parts.append('.**')
    
    else:
        field_added = False
        
        for stage, best, selected in selectable_stages:
            if field_added:
                description_parts.append('\n\n')
            else:
                field_added = True
            
            if selected:
                description_parts.append('\\> ')
            
            description_parts.append('**')
            description_parts.append(DIFFICULTY_NAMES.get(stage.difficulty_id, DIFFICULTY_NAME_DEFAULT))
            description_parts.append(' level ')
            description_parts.append(str(stage.in_difficulty_index + 1))
            description_parts.append('**')
            
            if selected:
                description_parts.append(' \\<')
            
            description_parts.append('\n')
            
            if selected:
                description_parts.append('\\> ')
            
            if best == -1:
                description_parts.append('No results recorded yet!')
            else:
                description_parts.append('rating : ')
                description_parts.append(get_rating_for(stage.best, best))
                description_parts.append('; steps : ')
                description_parts.append(str(best))
            
            if selected:
                description_parts.append(' \\<')
    
    return create_text_display(''.join(description_parts))


def build_components_in_menu(user_state):
    """
    Builds the user state's in-menu components.
    
    Parameters
    ----------
    user_state : ``UserState``
        The respective user state.
    
    Returns
    -------
    components : ``tuple<Component>``
    """
    stage = user_state.get_selected_stage()
    chapter = stage.get_chapter()
    style = chapter.get_style()
    control_emoji_mapping = style.control_emoji_mapping
    
    if can_play_selected_stage(user_state.stage_results, stage):
        selectable_stages = get_selectable_stages(user_state.stage_results, stage)
    else:
        selectable_stages = None
    
    stage_next_available = (selectable_stages is not None) and (not selectable_stages[0][2])
    stage_previous_available = (selectable_stages is not None) and (not selectable_stages[-1][2])
    
    # ---- title ----
    
    text_display_title = create_text_display(f'### Chapter {chapter.id + 1}')
    
    # ---- thumbnail ----
    
    thumbnail_media = create_thumbnail_media(style.emoji.url)
    
    # ---- description ----
    
    text_display_description = build_component_in_menu_description(chapter, selectable_stages)
    
    # ---- stage-next ----
    
    button_stage_next = create_button(
        custom_id = CUSTOM_ID_IN_MENU_STAGE_NEXT,
        emoji = control_emoji_mapping.in_menu_stage_next,
        enabled = stage_next_available,
        style = ButtonStyle.blue,
    )
    
    # ---- stage-next-multi ----
    
    button_stage_next_multi = create_button(
        custom_id = CUSTOM_ID_IN_MENU_STAGE_NEXT_MULTI,
        emoji = control_emoji_mapping.in_menu_stage_next_multi,
        enabled = stage_next_available,
        style = ButtonStyle.blue,
    )
    
    # ---- stage-previous ----
    
    button_stage_previous = create_button(
        custom_id = CUSTOM_ID_IN_MENU_STAGE_PREVIOUS,
        emoji = control_emoji_mapping.in_menu_stage_previous,
        enabled = stage_previous_available,
        style = ButtonStyle.blue,
    )
    
    # ---- stage-previous-multi ----
    
    button_stage_previous_multi = create_button(
        custom_id = CUSTOM_ID_IN_MENU_STAGE_PREVIOUS_MULTI,
        emoji = control_emoji_mapping.in_menu_stage_previous_multi,
        enabled = stage_previous_available,
        style = ButtonStyle.blue,
    )
    
    # ---- select-stage ----
    
    button_select_stage = create_button(
        custom_id = CUSTOM_ID_IN_MENU_SELECT_STAGE,
        emoji = control_emoji_mapping.in_menu_select_stage,
        enabled = (selectable_stages is not None),
        style = ButtonStyle.green,
    )
    
    # ---- chapter-previous ----
    
    button_chapter_previous = create_button(
        custom_id = CUSTOM_ID_IN_MENU_CHAPTER_PREVIOUS,
        emoji = control_emoji_mapping.in_menu_chapter_previous,
        enabled = (chapter.get_previous_chapter() is not None),
        style = ButtonStyle.blue,
    )
    
    # ---- chapter-next ----
    
    button_chapter_next = create_button(
        emoji = control_emoji_mapping.in_menu_chapter_next,
        enabled = (chapter.get_next_chapter() is not None),
        custom_id = CUSTOM_ID_IN_MENU_CHAPTER_NEXT,
        style = ButtonStyle.blue,
    )
    
    # ---- close ----
    
    button_close = create_button(
        emoji = control_emoji_mapping.in_menu_close,
        custom_id = CUSTOM_ID_IN_MENU_CLOSE,
        style = ButtonStyle.blue,
    )
    
    # ---- empty-0 ----
    
    button_empty_0 = create_button(
        emoji = control_emoji_mapping.nothing,
        custom_id = CUSTOM_ID_EMPTY_0,
        style = ButtonStyle.gray,
        enabled = False,
    )
    
    # ---- empty-1 ----
    
    button_empty_1 = create_button(
        emoji = control_emoji_mapping.nothing,
        custom_id = CUSTOM_ID_EMPTY_1,
        style = ButtonStyle.gray,
        enabled = False,
    )
    
    # ---- empty-2 ----
    
    button_empty_2 = create_button(
        emoji = control_emoji_mapping.nothing,
        custom_id = CUSTOM_ID_EMPTY_2,
        style = ButtonStyle.gray,
        enabled = False,
    )
    
    # ---- empty-3 ----
    
    button_empty_3 = create_button(
        emoji = control_emoji_mapping.nothing,
        custom_id = CUSTOM_ID_EMPTY_3,
        style = ButtonStyle.gray,
        enabled = False,
    )
    
    # ---- construct ----
    
    return (
        create_section(
            text_display_title,
            text_display_description,
            thumbnail = thumbnail_media,
        ),
        create_row(
            button_empty_0,
            button_stage_next,
            button_stage_next_multi,
            button_empty_1,
        ),
        create_row(
            button_chapter_previous,
            button_select_stage,
            button_close,
            button_chapter_next,
        ),
        create_row(
            button_empty_2,
            button_stage_previous,
            button_stage_previous_multi,
            button_empty_3,
        ),
    )


def build_components_shutdown():
    """
    Builds components when the clients are getting shut down.
    
    Returns
    -------
    components : ``tuple<Component>``
    """
    return (
        create_section(
            create_text_display(
                '### I am restarting\n'
                '\n'
                'Your progress has been saved, please try using the command again later.\n'
                '\n'
                'I am sorry for the inconvenience. See ya later qtie!'
            ),
            thumbnail = create_thumbnail_media(EMOJI_KOISHI_WAVE.url),
        ),
    )
