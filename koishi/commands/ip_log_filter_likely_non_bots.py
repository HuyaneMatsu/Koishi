__all__ = ()

import sys
from os.path import isfile as is_file

from hata.main import register

from ..bot_utils.ip_filtering import IP_TYPE_NONE, parse_ip


@register
def filter_ip_logs_likely_non_bots(
    input_file_path : str,
):
    """
    Goes through all the entries in the given file and removes the entries which are likely not from bots.
    """
    if not is_file(input_file_path):
        sys.stdout.write('Input file is not a file or does not exist.\n')
        return
    
    with open(input_file_path, 'r') as file:
        input_lines = file.read().splitlines(True)
    
    removed_count = 0
    output_lines = []
    lines_by_ips = {}
    
    for line in input_lines:
        if line == '\n':
            continue
        
        while True:
            split = line.split(maxsplit = 1)
            if len(split) < 1:
                output_lines.append(line)
                break
            
            ip_type, ip = parse_ip(split[0])
            if ip_type == IP_TYPE_NONE:
                output_lines.append(line)
                break
            
            try:
                values = lines_by_ips[ip_type, ip]
            except KeyError:
                lines_by_ips[ip_type, ip] = values = []
            
            values.append(line)
            break
    
    for values in lines_by_ips.values():
        likely_bot = True
        for value in values:
            if (
                ('.svg ' in value) or
                ('.png ' in value) or
                ('.gif ' in value) or
                ('.ico ' in value) or
                ('.css ' in value) or
                ('.js ' in value) or
                ('.jpg ' in value) or
                ('.jpeg ' in value) or
                ('Top.gg ' in value) or
                ('/guides/' in value)
            ):
                likely_bot = False
                break
            
            # No other conditions currently
            continue
        
        if likely_bot:
            output_lines.extend(values)
        else:
            removed_count += len(values)
        
    output_lines.sort()
    
    with open(input_file_path, 'w') as file:
        file.write(''.join(output_lines))
    
    sys.stdout.write(f'Removed {removed_count!s} entries.\n')
    return
