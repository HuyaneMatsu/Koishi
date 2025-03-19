__all__ = ()


def build_separator_line(widths, character):
    """
    Builds a separator line.
    
    Parameters
    ----------
    widths : `list<int>`
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
    into : `list<str>`
        The container to put the table parts into.
    
    widths : `list<int>`
        Column widths.
    
    character : `str`
        Separator character.
    
    Returns
    -------
    into : `list<str>`
    """
    into.append('+')
        
    for width in widths:
        into.append(character * (width + 2))
        into.append('+')
    
    return into


def build_elements_line_into(into, widths, elements):
    """
    Builds a table element row into the given container.
    
    Parameters
    ----------
    into : `list<str>`
        The container to put the table parts into.
    
    widths : `list<int>`
        Column widths.
    
    elements : `tuple<str>`
        Column elements.
    
    Returns
    -------
    into : `list<str>`
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
    headers : `tuple<str>`
        Table headers.
    
    columns : `tuple<list<str>>`
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
    into : `list<str>`
        The container to put the table parts into.
    
    headers : `tuple<str>`
        Table headers.
    
    columns : `tuple<list<str>>`
        Table columns.
    
    Returns
    -------
    into : `list<str>`
    """
    widths = [max(len(header), max(len(word) for word in column)) for header, column in zip(headers, columns)]
    
    default_separator_line = build_separator_line(widths, '-')
    
    into.append(default_separator_line)
    into.append('\n')
    build_elements_line_into(into, widths, headers)
    into.append('\n')
    build_separator_line_into(into, widths, '=')
    
    for elements in zip(*columns):
        into.append('\n')
        build_elements_line_into(into, widths, elements)
        into.append('\n')
        into.append(default_separator_line)
    
    return into
