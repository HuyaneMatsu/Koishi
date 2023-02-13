__all__ = ()

from random import choice

from .constants import (
    ARRAY_IDENTIFIER_EMPTY, CORNERS, CORNERS_TO_EDGES, CROSSES, LINES, MIDDLE, Y_PATTERN, Y_PATTERN_CHOOSE_FROM
)


def click_ai(array, identifier_player_ai, identifier_player_other):
    """
    Does an ai click. (Yes, we are using if, so it is an ai.)
    
    Parameters
    ----------
    array : `list` of `int`
        X-O-X game array.
    identifier_player_ai : `int`
        The ai player's identifier.
    identifier_player_other : `int`
        The other user's identifier.
    """
    should_click_at = -1
    
    while True:
        # Check whether we or the enemy can do 3 next to each other
        # ? ? ?
        # ? ? ?
        # X X _
        
        for indexes in LINES:
            
            count_enemy = 0
            count_own = 0
            free_index = -1
            for index in indexes:
                element = array[index]
                if element == ARRAY_IDENTIFIER_EMPTY:
                    free_index = index
                    continue
                
                if element == identifier_player_other:
                    count_enemy += 1
                    continue
                
                count_own += 1
                continue
            
            if free_index == -1:
                continue
            
            if count_own == 2:
                should_click_at = free_index
                break
            
            if count_enemy == 2:
                should_click_at = free_index
                continue
        
        if should_click_at != -1:
            break
        
        # Check whether it is the first move for us after the enemy's
        #
        # There are 3 cases.
        #
        # 1.:
        # If the enemy selected middle
        # _ _ _
        # _ O _
        # _ _ _
        #
        # We select a corner one.
        # X _ X
        # _ O _
        # X _ X
        #
        # 2.:
        # If the enemy selected a corner
        # O _ O
        # _ _ _
        # O _ O
        #
        # We select an adjacent edge to it
        # O X _
        # X _ _
        # _ _ _
        #
        # 3.:
        # If the enemy selected and edge.
        # _ O _
        # O _ O
        # _ O _
        #
        # We select the middle
        #
        # _ O _
        # O X O
        # _ O _
        
        count_enemy = 0
        count_own = 0
        enemy_index = -1
        
        for index in range(9):
            element = array[index]
            
            if element == ARRAY_IDENTIFIER_EMPTY:
                continue
            
            if element == identifier_player_other:
                count_enemy += 1
                enemy_index = index
                continue
            
            count_own += 1
            continue
        
        if (count_enemy == 1) and (count_own == 0):
            if enemy_index == MIDDLE:
                should_click_at = choice(CORNERS)
                break
            
            try:
                edges = CORNERS_TO_EDGES[enemy_index]
            except KeyError:
                pass
            else:
                should_click_at = choice(edges)
                break
            
            should_click_at = MIDDLE
            break
        
        # Check whether the enemy or we are trying to setup a trap
        if array[4] == ARRAY_IDENTIFIER_EMPTY:
            # _ _ _
            # _ _ _
            # O X O
            #
            # If the middle is empty and the sides look like that, it is possible.
            #
            # _ ? _
            # ? O ?
            # O X O
            for index_1, index_2, index_empty_1, index_empty_2 in CROSSES:
                
                if array[index_empty_1] != ARRAY_IDENTIFIER_EMPTY:
                    continue
                
                if array[index_empty_2] != ARRAY_IDENTIFIER_EMPTY:
                    continue
                
                element = array[index_1]
                if element == ARRAY_IDENTIFIER_EMPTY:
                    continue
                
                if element != array[index_2]:
                    continue
                
                should_click_at = 4
                break
                
            if should_click_at != -1:
                break
            
            # _ _ O
            # _ X ?
            # O ? _
            #
            # Y pattern matching
            # O _ O
            # _ X ?
            # O ? _
            for index_1, index_2, empty_indexes in Y_PATTERN:
                element = array[index_1]
                if element == ARRAY_IDENTIFIER_EMPTY:
                    continue
                
                if element != array[index_2]:
                    continue
                
                for index in empty_indexes:
                    if array[index] != ARRAY_IDENTIFIER_EMPTY:
                        all_empty = False
                        break
                else:
                    all_empty = True
                
                if not all_empty:
                    break
                
                should_click_at = choice(Y_PATTERN_CHOOSE_FROM)
                break
            
            if should_click_at != -1:
                break
        
        free_indexes = []
        for index in range(len(array)):
            if array[index] == ARRAY_IDENTIFIER_EMPTY:
                free_indexes.append(index)
        
        should_click_at = choice(free_indexes)
        break
    
    array[should_click_at] = identifier_player_ai
