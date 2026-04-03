__all__ = (
    'RELATIONSHIP_TYPE_AUNTIE', 'RELATIONSHIP_TYPE_CO_WORKER', 'RELATIONSHIP_TYPE_CONNECTION_MODIFIER_MASK',
    'RELATIONSHIP_TYPE_CONNECTION_MODIFIER_SHIFT_ANCESTORSHIP',
    'RELATIONSHIP_TYPE_CONNECTION_MODIFIER_SHIFT_EMPLOYMENTSHIP',
    'RELATIONSHIP_TYPE_CONNECTION_MODIFIER_SHIFT_SISTERSHIP',  'RELATIONSHIP_TYPE_CONNECTION_MODIFIER_TYPE_HALF',
    'RELATIONSHIP_TYPE_CONNECTION_MODIFIER_TYPE_IN_LAW', 'RELATIONSHIP_TYPE_CONNECTION_MODIFIER_TYPE_NONE',
    'RELATIONSHIP_TYPE_CONNECTION_MODIFIER_TYPE_STEP',  'RELATIONSHIP_TYPE_DAUGHTER', 
    'RELATIONSHIP_TYPE_GRANDDAUGHTER', 'RELATIONSHIP_TYPE_GRANNY', 'RELATIONSHIP_TYPE_MAID', 'RELATIONSHIP_TYPE_NANNY',
    'RELATIONSHIP_TYPE_MAMA', 'RELATIONSHIP_TYPE_MISTRESS', 'RELATIONSHIP_TYPE_NIECE', 'RELATIONSHIP_TYPE_NONE',
    'RELATIONSHIP_TYPE_RELATIONSHIPS', 'RELATIONSHIP_TYPE_SISTER_BIG', 'RELATIONSHIP_TYPE_SISTER_LIL',
    'RELATIONSHIP_TYPE_SISTER_RELATIVE', 'RELATIONSHIP_TYPE_TEA_FRIEND', 'RELATIONSHIP_TYPE_UNSET',
    'RELATIONSHIP_TYPE_WAIFU', 'RELATIONSHIP_TYPE_YOUNG_MISTRESS', 'determine_relative_sister',
    'get_relationship_type_name_basic', 'produce_relationship_type_name_advanced', 
)


RELATIONSHIP_TYPE_NONE = 0
RELATIONSHIP_TYPE_UNSET = 1 << 1
RELATIONSHIP_TYPE_WAIFU = 1 << 2
RELATIONSHIP_TYPE_SISTER_LIL = 1 << 3
RELATIONSHIP_TYPE_SISTER_BIG = 1 << 4
RELATIONSHIP_TYPE_MAMA = 1 << 5
RELATIONSHIP_TYPE_MISTRESS = 1 << 6
RELATIONSHIP_TYPE_MAID = 1 << 7
RELATIONSHIP_TYPE_DAUGHTER = 1 << 8

RELATIONSHIP_TYPE_SISTER_RELATIVE = 1 << 9
RELATIONSHIP_TYPE_AUNTIE = 1 << 10
RELATIONSHIP_TYPE_NIECE = 1 << 11
RELATIONSHIP_TYPE_CO_WORKER = 1 << 12
RELATIONSHIP_TYPE_GRANNY = 1 << 13
RELATIONSHIP_TYPE_GRANDDAUGHTER = 1 << 14
RELATIONSHIP_TYPE_YOUNG_MISTRESS = 1 << 15
RELATIONSHIP_TYPE_NANNY = 1 << 16
RELATIONSHIP_TYPE_TEA_FRIEND = 1 << 17


RELATIONSHIP_TYPE_CONNECTION_MODIFIER_TYPE_NONE = 0
RELATIONSHIP_TYPE_CONNECTION_MODIFIER_TYPE_HALF = 1
RELATIONSHIP_TYPE_CONNECTION_MODIFIER_TYPE_STEP = 2
RELATIONSHIP_TYPE_CONNECTION_MODIFIER_TYPE_IN_LAW = 3


RELATIONSHIP_TYPE_CONNECTION_MODIFIER_SHIFT_SISTERSHIP = 50
RELATIONSHIP_TYPE_CONNECTION_MODIFIER_SHIFT_ANCESTORSHIP = 52
RELATIONSHIP_TYPE_CONNECTION_MODIFIER_SHIFT_EMPLOYMENTSHIP = 54

RELATIONSHIP_TYPE_CONNECTION_MODIFIER_MASK = 3


RELATIONSHIP_TYPE_NAME_DEFAULT = 'pudding'

RELATIONSHIP_TYPE_NAMES = (
    (RELATIONSHIP_TYPE_UNSET, 0, 'unset'),
    (RELATIONSHIP_TYPE_WAIFU, 0, 'waifu'),
    (RELATIONSHIP_TYPE_SISTER_LIL, RELATIONSHIP_TYPE_CONNECTION_MODIFIER_SHIFT_SISTERSHIP, 'little sister'),
    (RELATIONSHIP_TYPE_SISTER_BIG, RELATIONSHIP_TYPE_CONNECTION_MODIFIER_SHIFT_SISTERSHIP, 'big sister'),
    (RELATIONSHIP_TYPE_MAMA, RELATIONSHIP_TYPE_CONNECTION_MODIFIER_SHIFT_ANCESTORSHIP, 'mama'),
    (RELATIONSHIP_TYPE_DAUGHTER, RELATIONSHIP_TYPE_CONNECTION_MODIFIER_SHIFT_ANCESTORSHIP, 'daughter'),
    (RELATIONSHIP_TYPE_MISTRESS, RELATIONSHIP_TYPE_CONNECTION_MODIFIER_SHIFT_EMPLOYMENTSHIP, 'mistress'),
    (RELATIONSHIP_TYPE_MAID, RELATIONSHIP_TYPE_CONNECTION_MODIFIER_SHIFT_EMPLOYMENTSHIP, 'maid'),
    (RELATIONSHIP_TYPE_SISTER_RELATIVE, 0, 'sister'),
    (RELATIONSHIP_TYPE_AUNTIE, 0, 'auntie'),
    (RELATIONSHIP_TYPE_NIECE, 0, 'niece'),
    (RELATIONSHIP_TYPE_CO_WORKER, 0, 'co-worker'),
    (RELATIONSHIP_TYPE_GRANNY, 0, 'granny'),
    (RELATIONSHIP_TYPE_GRANDDAUGHTER, 0, 'granddaughter'),
    (RELATIONSHIP_TYPE_YOUNG_MISTRESS, 0, 'young mistress'),
    (RELATIONSHIP_TYPE_NANNY, 0, 'nanny'),
    (RELATIONSHIP_TYPE_TEA_FRIEND, 0, 'tea friend'),
)


RELATIONSHIP_TYPE_NAMES_BASIC = {
    RELATIONSHIP_TYPE_UNSET : 'unset',
    RELATIONSHIP_TYPE_WAIFU : 'waifu',
    RELATIONSHIP_TYPE_SISTER_LIL : 'little sister',
    RELATIONSHIP_TYPE_SISTER_BIG : 'big sister',
    RELATIONSHIP_TYPE_MAMA : 'mama',
    RELATIONSHIP_TYPE_DAUGHTER : 'daughter',
    RELATIONSHIP_TYPE_MISTRESS : 'mistress',
    RELATIONSHIP_TYPE_MAID : 'maid',
}


_RELATIONSHIP_TYPE_FLIPS_BASIC = (
    (RELATIONSHIP_TYPE_SISTER_LIL, RELATIONSHIP_TYPE_SISTER_BIG),
    (RELATIONSHIP_TYPE_MAMA, RELATIONSHIP_TYPE_DAUGHTER),
    (RELATIONSHIP_TYPE_MISTRESS, RELATIONSHIP_TYPE_MAID),
)


RELATIONSHIP_TYPE_RELATIONSHIPS = {
    # unset
    RELATIONSHIP_TYPE_UNSET: RELATIONSHIP_TYPE_UNSET,
    
    # acquirable
    RELATIONSHIP_TYPE_WAIFU: RELATIONSHIP_TYPE_WAIFU,
    RELATIONSHIP_TYPE_SISTER_LIL: RELATIONSHIP_TYPE_SISTER_BIG,
    RELATIONSHIP_TYPE_SISTER_BIG: RELATIONSHIP_TYPE_SISTER_LIL,
    RELATIONSHIP_TYPE_MAMA: RELATIONSHIP_TYPE_DAUGHTER,
    RELATIONSHIP_TYPE_DAUGHTER: RELATIONSHIP_TYPE_MAMA,
    RELATIONSHIP_TYPE_MISTRESS: RELATIONSHIP_TYPE_MAID,
    RELATIONSHIP_TYPE_MAID: RELATIONSHIP_TYPE_MISTRESS,
    
    # for display
    RELATIONSHIP_TYPE_SISTER_RELATIVE: RELATIONSHIP_TYPE_SISTER_RELATIVE,
    RELATIONSHIP_TYPE_AUNTIE: RELATIONSHIP_TYPE_NIECE,
    RELATIONSHIP_TYPE_NIECE: RELATIONSHIP_TYPE_AUNTIE,
    RELATIONSHIP_TYPE_CO_WORKER: RELATIONSHIP_TYPE_CO_WORKER,
    RELATIONSHIP_TYPE_GRANNY : RELATIONSHIP_TYPE_GRANDDAUGHTER,
    RELATIONSHIP_TYPE_GRANDDAUGHTER : RELATIONSHIP_TYPE_GRANNY,
    RELATIONSHIP_TYPE_YOUNG_MISTRESS : RELATIONSHIP_TYPE_NANNY,
    RELATIONSHIP_TYPE_NANNY : RELATIONSHIP_TYPE_YOUNG_MISTRESS,
    RELATIONSHIP_TYPE_TEA_FRIEND : RELATIONSHIP_TYPE_TEA_FRIEND,
}


def do_relationship_type_flip_basic(relationship_type):
    """
    Does basic relationship type flipping.
    
    Parameters
    ----------
    relationship_type : `int`
        The relationship type to flip.
    
    Returns
    -------
    relationship_type : `int`
    """
    for source_relationship_type, target_relationship_type in _RELATIONSHIP_TYPE_FLIPS_BASIC:
        if relationship_type & source_relationship_type:
            relationship_type &=~ source_relationship_type
            relationship_type |= target_relationship_type
            continue
        
        if relationship_type & target_relationship_type:
            relationship_type &=~ target_relationship_type
            relationship_type |= source_relationship_type
            continue
    
    return relationship_type


def produce_relationship_type_name_advanced(relationship_type):
    """
    Produces the relationship type's name.
    
    This function is a generator.
    
    Parameters
    ----------
    relationship_type : `int`
        Relationship type.
    
    Returns
    -------
    part : `str`
    """
    if not relationship_type:
        yield RELATIONSHIP_TYPE_NAME_DEFAULT
        return
    
    field_added = False
    
    for mask, modifier_shift, name in RELATIONSHIP_TYPE_NAMES:
        if not (relationship_type & mask):
            continue
        
        if field_added:
            yield ' & '
        else:
            field_added = True
        
        yield name
        
        if not modifier_shift:
            continue
        
        modifier = (relationship_type >> modifier_shift) & RELATIONSHIP_TYPE_CONNECTION_MODIFIER_MASK
        if not modifier:
            continue
        
        if modifier == RELATIONSHIP_TYPE_CONNECTION_MODIFIER_TYPE_HALF:
            modifier_name = 'half'
        elif modifier == RELATIONSHIP_TYPE_CONNECTION_MODIFIER_TYPE_STEP:
            modifier_name = 'step'
        else:
            modifier_name = 'in law'
        
        yield ' ('
        yield modifier_name
        yield ')'
        continue


def get_relationship_type_name_basic(relationship_type):
    """
    Gets a basic relationship type's name.
    
    Parameters
    ----------
    relationship_type : `int`
        Relationship type.
    
    Returns
    -------
    relationship_type_name : `str`
    """
    return RELATIONSHIP_TYPE_NAMES_BASIC.get(relationship_type, RELATIONSHIP_TYPE_NAME_DEFAULT)


RELATION_TYPE_ALLOWED_EXTENDS = {
    # shared through waifu
    RELATIONSHIP_TYPE_WAIFU : (
        RELATIONSHIP_TYPE_SISTER_LIL,
        RELATIONSHIP_TYPE_SISTER_BIG,
        RELATIONSHIP_TYPE_MAMA,
        RELATIONSHIP_TYPE_MAID,
        RELATIONSHIP_TYPE_DAUGHTER,
    ),
    
    # shared through little sister
    RELATIONSHIP_TYPE_SISTER_LIL : (
        RELATIONSHIP_TYPE_SISTER_LIL,
        RELATIONSHIP_TYPE_SISTER_BIG,
        RELATIONSHIP_TYPE_MAMA,
        RELATIONSHIP_TYPE_WAIFU,
        RELATIONSHIP_TYPE_DAUGHTER,
    ),
    
    # shared through big sister
    RELATIONSHIP_TYPE_SISTER_BIG: (
        RELATIONSHIP_TYPE_SISTER_LIL,
        RELATIONSHIP_TYPE_SISTER_BIG,
        RELATIONSHIP_TYPE_MAMA,
        RELATIONSHIP_TYPE_WAIFU,
        RELATIONSHIP_TYPE_DAUGHTER,
    ),
    
    # shared through mama
    RELATIONSHIP_TYPE_MAMA : (
        RELATIONSHIP_TYPE_WAIFU,
        RELATIONSHIP_TYPE_SISTER_LIL,
        RELATIONSHIP_TYPE_SISTER_BIG,
        RELATIONSHIP_TYPE_MAMA,
        RELATIONSHIP_TYPE_DAUGHTER,
        RELATIONSHIP_TYPE_MAID,
    ),
    
    # shared through daughter
    RELATIONSHIP_TYPE_DAUGHTER : (
        RELATIONSHIP_TYPE_SISTER_LIL,
        RELATIONSHIP_TYPE_SISTER_BIG,
        RELATIONSHIP_TYPE_WAIFU,
        RELATIONSHIP_TYPE_DAUGHTER,
        RELATIONSHIP_TYPE_MISTRESS,
    ),
    
    # shared through mistress
    RELATIONSHIP_TYPE_MISTRESS : (
        RELATIONSHIP_TYPE_WAIFU,
        RELATIONSHIP_TYPE_DAUGHTER,
        RELATIONSHIP_TYPE_MAID,
    ),
    
    # shared through maid
    RELATIONSHIP_TYPE_MAID : (
        RELATIONSHIP_TYPE_MAMA,
    ),
}


def determine_relative_sister(source_user_id, target_user_id):
    """
    Determines whether the sister is big or little based on user identifiers.
    If something ends up with `RELATIONSHIP_TYPE_SISTER_RELATIVE` relationship type this function should be called.
    
    Parameters
    ----------
    source_user_id : `int`
        The identifier of the user we are calculating relationship types from.
    
    target_user_id : `int`
        The identifier of the extended user we are calculating relationship towards.
    
    Returns
    -------
    relationship_type : `int`
    """
    return RELATIONSHIP_TYPE_SISTER_BIG if source_user_id > target_user_id else RELATIONSHIP_TYPE_SISTER_LIL 



def _make_sister_lil_in_law(relationship_type):
    return _apply_relationship_parameterized(
        relationship_type,
        RELATIONSHIP_TYPE_SISTER_LIL,
        RELATIONSHIP_TYPE_SISTER_BIG,
        RELATIONSHIP_TYPE_SISTER_RELATIVE,
        RELATIONSHIP_TYPE_CONNECTION_MODIFIER_SHIFT_SISTERSHIP,
        RELATIONSHIP_TYPE_CONNECTION_MODIFIER_TYPE_IN_LAW,
    )


def _make_sister_lil_half(relationship_type):
    return _apply_relationship_parameterized(
        relationship_type,
        RELATIONSHIP_TYPE_SISTER_LIL,
        RELATIONSHIP_TYPE_SISTER_BIG,
        RELATIONSHIP_TYPE_SISTER_RELATIVE,
        RELATIONSHIP_TYPE_CONNECTION_MODIFIER_SHIFT_SISTERSHIP,
        RELATIONSHIP_TYPE_CONNECTION_MODIFIER_TYPE_HALF,
    )


def _make_sister_big_in_law(relationship_type):
    return _apply_relationship_parameterized(
        relationship_type,
        RELATIONSHIP_TYPE_SISTER_BIG,
        RELATIONSHIP_TYPE_SISTER_LIL,
        RELATIONSHIP_TYPE_SISTER_RELATIVE,
        RELATIONSHIP_TYPE_CONNECTION_MODIFIER_SHIFT_SISTERSHIP,
        RELATIONSHIP_TYPE_CONNECTION_MODIFIER_TYPE_IN_LAW,
    )


def _make_sister_big_half(relationship_type):
    return _apply_relationship_parameterized(
        relationship_type,
        RELATIONSHIP_TYPE_SISTER_BIG,
        RELATIONSHIP_TYPE_SISTER_LIL,
        RELATIONSHIP_TYPE_SISTER_RELATIVE,
        RELATIONSHIP_TYPE_CONNECTION_MODIFIER_SHIFT_SISTERSHIP,
        RELATIONSHIP_TYPE_CONNECTION_MODIFIER_TYPE_HALF,
    )


def _make_mama_in_law(relationship_type):
    return _apply_relationship_parameterized(
        relationship_type,
        RELATIONSHIP_TYPE_MAMA,
        RELATIONSHIP_TYPE_DAUGHTER,
        0,
        RELATIONSHIP_TYPE_CONNECTION_MODIFIER_SHIFT_ANCESTORSHIP,
        RELATIONSHIP_TYPE_CONNECTION_MODIFIER_TYPE_IN_LAW,
    )


def _make_mama_step(relationship_type):
    return _apply_relationship_parameterized(
        relationship_type,
        RELATIONSHIP_TYPE_MAMA,
        RELATIONSHIP_TYPE_DAUGHTER,
        0,
        RELATIONSHIP_TYPE_CONNECTION_MODIFIER_SHIFT_ANCESTORSHIP,
        RELATIONSHIP_TYPE_CONNECTION_MODIFIER_TYPE_STEP,
    )


def _make_daughter_in_law(relationship_type):
    return _apply_relationship_parameterized(
        relationship_type,
        RELATIONSHIP_TYPE_DAUGHTER,
        RELATIONSHIP_TYPE_MAMA,
        0,
        RELATIONSHIP_TYPE_CONNECTION_MODIFIER_SHIFT_ANCESTORSHIP,
        RELATIONSHIP_TYPE_CONNECTION_MODIFIER_TYPE_IN_LAW,
    )


def _make_daughter_half(relationship_type):
    return _apply_relationship_parameterized(
        relationship_type,
        RELATIONSHIP_TYPE_DAUGHTER,
        RELATIONSHIP_TYPE_MAMA,
        0,
        RELATIONSHIP_TYPE_CONNECTION_MODIFIER_SHIFT_ANCESTORSHIP,
        RELATIONSHIP_TYPE_CONNECTION_MODIFIER_TYPE_HALF,
    )


def _make_mistress_in_law(relationship_type):
    return _apply_relationship_parameterized(
        relationship_type,
        RELATIONSHIP_TYPE_MISTRESS,
        RELATIONSHIP_TYPE_MAID,
        0,
        RELATIONSHIP_TYPE_CONNECTION_MODIFIER_SHIFT_EMPLOYMENTSHIP,
        RELATIONSHIP_TYPE_CONNECTION_MODIFIER_TYPE_IN_LAW,
    )


def _make_maid_in_law(relationship_type):
    return _apply_relationship_parameterized(
        relationship_type,
        RELATIONSHIP_TYPE_MAID,
        RELATIONSHIP_TYPE_MISTRESS,
        0,
        RELATIONSHIP_TYPE_CONNECTION_MODIFIER_SHIFT_EMPLOYMENTSHIP,
        RELATIONSHIP_TYPE_CONNECTION_MODIFIER_TYPE_IN_LAW,
    )


def _apply_relationship_parameterized(
    relationship_type,
    relationship_type_applied,
    relationship_type_other,
    relationship_type_relative,
    modifier_shift,
    modifier_applied,
):
    while True:
        # Are we already relative?
        if relationship_type & relationship_type_relative:
            modifier_current = (relationship_type >> modifier_shift) & RELATIONSHIP_TYPE_CONNECTION_MODIFIER_MASK
            
            # If the current modifier is smaller or equal, we have nothing to do.
            if modifier_current <= modifier_applied:
                break
            
            relationship_type &= ~relationship_type_relative
            relationship_type |= relationship_type_applied
            relationship_type ^= (modifier_current ^ modifier_applied) << modifier_shift
            break
        
        # Are they already "little sister"??
        if relationship_type & relationship_type_applied:
            modifier_current = (relationship_type >> modifier_shift) & RELATIONSHIP_TYPE_CONNECTION_MODIFIER_MASK
            
            # If the current modifier is smaller or equal, we have nothing to do.
            if modifier_current <= modifier_applied:
                break
            
            relationship_type ^= (modifier_current ^ modifier_applied) << modifier_shift
            break
        
        # Are we "big sister"?
        if relationship_type & relationship_type_other:
            modifier_current = (relationship_type >> modifier_shift) & RELATIONSHIP_TYPE_CONNECTION_MODIFIER_MASK
            
            # If the current modifier is smaller, we have nothing to do.
            if modifier_current < modifier_applied:
                break
            
            # If we are at equal level, apply relative
            if modifier_current == modifier_applied:
                if not relationship_type_relative:
                    break
                
                relationship_type &= ~relationship_type_other
                relationship_type |= relationship_type_relative
                break
            
            relationship_type &= ~relationship_type_other
            relationship_type |= relationship_type_applied
            relationship_type ^= (modifier_current ^ modifier_applied) << modifier_shift
            break
        
        # Just apply.
        relationship_type |= relationship_type_applied
        relationship_type |= modifier_applied << modifier_shift
        break
    
    return relationship_type


def _make_sister_relative_half(relationship_type):
    return _make_relative_parametrised(
        relationship_type,
        RELATIONSHIP_TYPE_SISTER_RELATIVE,
        (RELATIONSHIP_TYPE_SISTER_LIL | RELATIONSHIP_TYPE_SISTER_BIG),
        RELATIONSHIP_TYPE_CONNECTION_MODIFIER_SHIFT_SISTERSHIP,
        RELATIONSHIP_TYPE_CONNECTION_MODIFIER_TYPE_HALF,
    )


def _make_relative_parametrised(
    relationship_type,
    relationship_type_relative,
    relationship_type_non_relative_mask,
    modifier_shift,
    modifier_applied,
):
    while True:
        
        # Are we already relative?
        if relationship_type & relationship_type_relative:
            modifier_current = (relationship_type >> modifier_shift) & RELATIONSHIP_TYPE_CONNECTION_MODIFIER_MASK
            
            # If the current modifier is smaller or equal, we have nothing to do.
            if modifier_current <= modifier_applied:
                break
            
            relationship_type ^= (modifier_current ^ modifier_applied) << modifier_shift
            break
        
        # Are we non relative?
        if relationship_type & relationship_type_non_relative_mask:
            modifier_current = (relationship_type >> modifier_shift) & RELATIONSHIP_TYPE_CONNECTION_MODIFIER_MASK
            
            # If the current modifier is smaller, we have nothing to do.
            if modifier_current <= modifier_applied:
                break
            
            relationship_type &= ~relationship_type_non_relative_mask
            relationship_type |= relationship_type_relative
            relationship_type ^= (modifier_current ^ modifier_applied) << modifier_shift
            break
        
        # Just apply.
        relationship_type |= relationship_type_relative
        relationship_type |= modifier_applied << modifier_shift
        break
    
    return relationship_type


def _make_niece(relationship_type):
    return relationship_type | RELATIONSHIP_TYPE_NIECE


def _make_auntie(relationship_type):
    return relationship_type | RELATIONSHIP_TYPE_AUNTIE


def _make_granny(relationship_type):
    return relationship_type | RELATIONSHIP_TYPE_GRANNY


def _make_nanny(relationship_type):
    return relationship_type | RELATIONSHIP_TYPE_NANNY


def _make_granddaughter(relationship_type):
    return relationship_type | RELATIONSHIP_TYPE_GRANDDAUGHTER


def _make_tea_friend(relationship_type):
    return relationship_type | RELATIONSHIP_TYPE_TEA_FRIEND
    
    
def _make_young_mistress_friend(relationship_type):
    return relationship_type | RELATIONSHIP_TYPE_YOUNG_MISTRESS


def _make_co_worker(relationship_type):
    return relationship_type | RELATIONSHIP_TYPE_CO_WORKER


RELATION_TYPE_EXTENSIONS = (
    # shared through waifu
    (
        RELATIONSHIP_TYPE_WAIFU,
        (
            (RELATIONSHIP_TYPE_SISTER_LIL, _make_sister_lil_in_law),
            (RELATIONSHIP_TYPE_SISTER_BIG, _make_sister_big_in_law),
            (RELATIONSHIP_TYPE_MAMA, _make_mama_in_law),
            (RELATIONSHIP_TYPE_MAID, _make_maid_in_law),
            (RELATIONSHIP_TYPE_DAUGHTER, _make_daughter_in_law),
        ),
    ),
    
    # shared through little sister
    (
        RELATIONSHIP_TYPE_SISTER_LIL,
        (
            (RELATIONSHIP_TYPE_WAIFU, _make_sister_lil_in_law),
            (RELATIONSHIP_TYPE_SISTER_LIL, _make_sister_lil_half),
            (RELATIONSHIP_TYPE_SISTER_BIG, _make_sister_relative_half),
            (RELATIONSHIP_TYPE_MAMA, _make_mama_step),
            (RELATIONSHIP_TYPE_DAUGHTER, _make_niece),
        ),
    ),
    
    # shared through big sister
    (
        RELATIONSHIP_TYPE_SISTER_BIG,
        (
            (RELATIONSHIP_TYPE_WAIFU, _make_sister_big_in_law),
            (RELATIONSHIP_TYPE_SISTER_LIL, _make_sister_relative_half),
            (RELATIONSHIP_TYPE_SISTER_BIG, _make_sister_big_half),
            (RELATIONSHIP_TYPE_MAMA, _make_mama_step),
            (RELATIONSHIP_TYPE_DAUGHTER, _make_niece),
        ),
    ),
    
    # shared through mama
    (
        RELATIONSHIP_TYPE_MAMA,
        (
            (RELATIONSHIP_TYPE_WAIFU, _make_mama_in_law),
            (RELATIONSHIP_TYPE_SISTER_LIL, _make_auntie),
            (RELATIONSHIP_TYPE_SISTER_BIG, _make_auntie),
            (RELATIONSHIP_TYPE_MAMA, _make_granny),
            (RELATIONSHIP_TYPE_DAUGHTER, _make_sister_relative_half),
            (RELATIONSHIP_TYPE_MAID, _make_nanny),
        ),
    ),
    
    # shared through daughter
    (
        RELATIONSHIP_TYPE_DAUGHTER,
        (
            (RELATIONSHIP_TYPE_WAIFU, _make_daughter_in_law),
            (RELATIONSHIP_TYPE_SISTER_LIL, _make_daughter_half),
            (RELATIONSHIP_TYPE_SISTER_BIG, _make_daughter_half),
            (RELATIONSHIP_TYPE_DAUGHTER, _make_granddaughter),
            (RELATIONSHIP_TYPE_MISTRESS, _make_tea_friend),
        ),
    ),
    
    # shared through mistress
    (
        RELATIONSHIP_TYPE_MISTRESS,
        (
            (RELATIONSHIP_TYPE_WAIFU, _make_mistress_in_law),
            (RELATIONSHIP_TYPE_DAUGHTER, _make_young_mistress_friend),
            (RELATIONSHIP_TYPE_MAID, _make_co_worker),
        ),
    ),
    
    # shared through maid
    (
        RELATIONSHIP_TYPE_MAID,
        (
            (RELATIONSHIP_TYPE_MAMA, _make_tea_friend),
        ),
    ),
)


RELATIONSHIP_TYPES_EXTENDABLE = (
    RELATIONSHIP_TYPE_WAIFU |
    RELATIONSHIP_TYPE_SISTER_LIL | RELATIONSHIP_TYPE_SISTER_BIG |
    RELATIONSHIP_TYPE_MAMA | RELATIONSHIP_TYPE_DAUGHTER |
    RELATIONSHIP_TYPE_MISTRESS | RELATIONSHIP_TYPE_MAID
)
