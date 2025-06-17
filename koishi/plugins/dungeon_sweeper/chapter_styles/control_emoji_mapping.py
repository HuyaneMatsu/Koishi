__all__ = ('ControlEmojiMapping',)

from scarletio import RichAttributeErrorBaseType


class ControlEmojiMapping(RichAttributeErrorBaseType):
    """
    Represents the control emojis of a chapter used for its action.
    
    Attributes
    ----------
    end_screen_next_stage : ``Emoji``
        Shown on the end screen. Goes to the next stage.
    
    end_screen_return_to_menu : ``Emoji``
        Shown on the end screen. Used to go back ot the menu.
    
    end_screen_restart_stage : ``Emoji``
        Shown on the end screen. Restarts the current stage.
    
        
    in_game_back : ``Emoji``
        Show in game. Moves the game state back one step.
    
    in_game_east : ``Emoji``
        Shown in game. Moves the character east-wards.
    
    in_game_north : ``Emoji``
        Shown in game. Moves the character north-wards.
    
    in_game_north_east : ``Emoji``
        Shown in game. Moves the character north-east-wards.
    
    in_game_north_west : ``Emoji``
        Shown in game. Moves the character north-west-wards.
    
    in_game_restart : ``Emoji``
        Shown in game. Resets the game to the starting position.
    
    in_game_return_to_menu : ``Emoji``
        Shown in game. Cancels the current game, moving back to the main menu.
    
    in_game_south : ``Emoji``
        Shown in game. Moves the character south-wards.
    
    in_game_south_east : ``Emoji``
        Shown in game. Moves the character south-east-wards.
    
    in_game_south_west : ``Emoji``
        Shown in game. Moves the character south-west-wards.
    
    in_game_west : ``Emoji``
        Shown in game. Moves the character west-wards.
    
    
    in_menu_chapter_next : ``Emoji``
        Shown in menu. Used to increment the chapter index by one.
    
    in_menu_chapter_previous : ``Emoji``
        Shown in menu. Used to decrement the chapter index by one.
    
    in_menu_close : ``Emoji``
        Shown in menu. Closes the game.
    
    in_menu_select_stage : ``Emoji``
        Shown in menu. Selects the hovered stage.
    
    in_menu_stage_next : ``Emoji``
        Shown in menu. Used to increment the stage index by one.
    
    in_menu_stage_next_multi : ``Emoji``
        Shown in menu. Used to increment the stage index multiple times.
    
    in_menu_stage_previous : ``Emoji``
        Shown in menu. Used to decrement the stage index by one.
    
    in_menu_stage_previous_multi : ``Emoji``
        Shown in menu. Used to decrement the stage index multiple times.
    
    
    nothing : ``Emoji``
        Nothing emoji used as a placeholder where required.
    """
    __slots__ = (
        'end_screen_next_stage', 'end_screen_return_to_menu', 'end_screen_restart_stage',
        
        'in_game_back', 'in_game_east', 'in_game_north', 'in_game_north_east', 'in_game_north_west', 'in_game_restart',
        'in_game_return_to_menu', 'in_game_south', 'in_game_south_east', 'in_game_south_west', 'in_game_west',
        
        'in_menu_chapter_next', 'in_menu_chapter_previous', 'in_menu_close', 'in_menu_select_stage',
        'in_menu_stage_next', 'in_menu_stage_next_multi', 'in_menu_stage_previous', 'in_menu_stage_previous_multi', 
        
        'nothing',
    )
    
    def __new__(
        cls,
        
        end_screen_next_stage,
        end_screen_return_to_menu,
        end_screen_restart_stage,
        
        in_game_back,
        in_game_east,
        in_game_north,
        in_game_north_east,
        in_game_north_west,
        in_game_restart,
        in_game_return_to_menu,
        in_game_south,
        in_game_south_east,
        in_game_south_west,
        in_game_west,
        
        in_menu_chapter_next,
        in_menu_chapter_previous,
        in_menu_close,
        in_menu_select_stage,
        in_menu_stage_next,
        in_menu_stage_next_multi,
        in_menu_stage_previous,
        in_menu_stage_previous_multi,
        
        nothing,
    ):
        """
        Creates a new control emoji mapping.
        
        Parameters
        ----------
        end_screen_next_stage : ``Emoji``
            Shown on the end screen. Goes to the next stage.
        
        end_screen_return_to_menu : ``Emoji``
            Shown on the end screen. Used to go back ot the menu.
        
        end_screen_restart_stage : ``Emoji``
            Shown on the end screen. Restarts the current stage.
        
            
        in_game_back : ``Emoji``
            Show in game. Moves the game state back one step.
        
        in_game_east : ``Emoji``
            Shown in game. Moves the character east-wards.
        
        in_game_north : ``Emoji``
            Shown in game. Moves the character north-wards.
        
        in_game_north_east : ``Emoji``
            Shown in game. Moves the character north-east-wards.
        
        in_game_north_west : ``Emoji``
            Shown in game. Moves the character north-west-wards.
        
        in_game_restart : ``Emoji``
            Shown in game. Resets the game to the starting position.
        
        in_game_return_to_menu : ``Emoji``
            Shown in game. Cancels the current game, moving back to the main menu.
        
        in_game_south : ``Emoji``
            Shown in game. Moves the character south-wards.
        
        in_game_south_east : ``Emoji``
            Shown in game. Moves the character south-east-wards.
        
        in_game_south_west : ``Emoji``
            Shown in game. Moves the character south-west-wards.
        
        in_game_west : ``Emoji``
            Shown in game. Moves the character west-wards.
        
        
        in_menu_chapter_next : ``Emoji``
            Shown in menu. Used to increment the chapter index by one.
        
        in_menu_chapter_previous : ``Emoji``
            Shown in menu. Used to decrement the chapter index by one.
        
        in_menu_close : ``Emoji``
            Shown in menu. Closes the game.
        
        in_menu_select_stage : ``Emoji``
            Shown in menu. Selects the hovered stage.
        
        in_menu_stage_next : ``Emoji``
            Shown in menu. Used to increment the stage index by one.
        
        in_menu_stage_next_multi : ``Emoji``
            Shown in menu. Used to increment the stage index multiple times.
        
        in_menu_stage_previous : ``Emoji``
            Shown in menu. Used to decrement the stage index by one.
        
        in_menu_stage_previous_multi : ``Emoji``
            Shown in menu. Used to decrement the stage index multiple times.
        
        
        nothing : ``Emoji``
            Nothing emoji used as a placeholder where required.

        """
        self = object.__new__(cls)
        
        self.end_screen_next_stage = end_screen_next_stage
        self.end_screen_return_to_menu = end_screen_return_to_menu
        self.end_screen_restart_stage = end_screen_restart_stage
        
        self.in_game_back = in_game_back
        self.in_game_east = in_game_east
        self.in_game_north = in_game_north
        self.in_game_north_east = in_game_north_east
        self.in_game_north_west = in_game_north_west
        self.in_game_restart = in_game_restart
        self.in_game_return_to_menu = in_game_return_to_menu
        self.in_game_south = in_game_south
        self.in_game_south_east = in_game_south_east
        self.in_game_south_west = in_game_south_west
        self.in_game_west = in_game_west
        
        self.in_menu_chapter_next = in_menu_chapter_next
        self.in_menu_chapter_previous = in_menu_chapter_previous
        self.in_menu_close = in_menu_close
        self.in_menu_stage_next = in_menu_stage_next
        self.in_menu_stage_next_multi = in_menu_stage_next_multi
        self.in_menu_stage_previous = in_menu_stage_previous
        self.in_menu_stage_previous_multi = in_menu_stage_previous_multi
        self.in_menu_select_stage = in_menu_select_stage
        
        self.nothing = nothing
        
        return self
    
    
    def __repr__(self):
        """Returns repr(self)."""
        repr_parts = ['<', type(self).__name__]
        
        # Nothing here.
        
        repr_parts.append('>')
        return ''.join(repr_parts)
