__all__ = ()

import sys
from os.path import isfile as is_file

from hata.main import register


@register
def filter_ip_logs(
    input_file_path : str,
):
    """
    Goes through all the entries in the given file and removes the ones that are already blacklisted.
    """
    from ..bot_utils.ip_filtering import IP_TYPE_NONE, match_ip_to_structure, parse_ip
    from ..web import IP_MATCHER_STRUCTURE
    
    if not is_file(input_file_path):
        sys.stdout.write('Input file is not a file or does not exist.\n')
        return
    
    with open(input_file_path, 'r') as file:
        input_lines = file.read().splitlines(True)
    
    removed_count = 0
    output_lines = []
    
    for line in input_lines:
        if line == '\n':
            continue
        
        while True:
            split = line.split(maxsplit = 1)
            if len(split) < 2:
                matched = False
                break
            
            ip_type, ip = parse_ip(split[0])
            if ip_type == IP_TYPE_NONE:
                matched = False
                break
            
            if not match_ip_to_structure(IP_MATCHER_STRUCTURE, ip_type, ip):
                matched = False
                break
            
            matched = True
            break
        
        if matched:
            removed_count += 1
        else:
            output_lines.append(line)
    
    output_lines.sort()
    
    with open(input_file_path, 'w') as file:
        file.write(''.join(output_lines))
    
    sys.stdout.write(f'Removed {removed_count!s} entries.\n')
    return
