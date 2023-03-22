__all__ = ()


def build_separator_line(widths, character):
    """
    Builds a separator line.
    
    Parameters
    ----------
    widths : `list` of `int`
        Column widths.
    character : `str`
        Separator character.
    
    Returns
    -------
    separator_line : `str`
    """
    return ''.join(build_separator_line_into([], widths, character))


def build_separator_line_into(into, widths, character):
    """
    Builds a separator line into the given container.
    
    Parameters
    ----------
    into : `list` of `str`
        The container to put the table parts into.
    widths : `list` of `int`
        Column widths.
    character : `str`
        Separator character.
    
    Returns
    -------
    into : `list` of `str`
    """
    into.append('+')
        
    for width in widths:
        into.append(character * (width + 2))
        into.append('+')
    
    return into


def build_elements_into(into, widths, elements):
    """
    Builds a table element row into the given container.
    
    Parameters
    ----------
    into : `list` of `str`
        The container to put the table parts into.
    widths : `list` of `int`
        Column widths.
    elements : `tuple` of `str`
        Column elements.
    
    Returns
    -------
    into : `list` of `str`
    """
    into.append('|')
    
    if widths:
        for width, element in zip(widths, elements):
            into.append(' ')
            into.append(element)
            into.append(' ' * (width - len(element)))
            into.append(' |')
    
    return into


def build_table(headers, columns):
    """
    Builds a table.
    
    Parameters
    ----------
    headers : `tuple` of `str`
        Table headers.
    columns : `tuple` of `list` of `str`
        Table columns.
    
    Returns
    -------
    table : `str`
    """
    return ''.join(build_table_into([], headers, columns))


def build_table_into(into, headers, columns):
    """
    Builds a table into the given container.
    
    Parameters
    ----------
    into : `list` of `str`
        The container to put the table parts into.
    headers : `tuple` of `str`
        Table headers.
    columns : `tuple` of `list` of `str`
        Table columns.
    
    Returns
    -------
    into : `list` of `str`
    """
    widths = [max(len(header), max(len(word) for word in column)) for header, column in zip(headers, columns)]
    
    default_separator_line = build_separator_line(widths, '-')
    
    into.append(default_separator_line)
    into.append('\n')
    build_elements_into(into, widths, headers)
    into.append('\n')
    build_separator_line_into(into, widths, '=')
    
    for elements in zip(*columns):
        into.append('\n')
        build_elements_into(into, widths, elements)
        into.append('\n')
        into.append(default_separator_line)
    
    return into
