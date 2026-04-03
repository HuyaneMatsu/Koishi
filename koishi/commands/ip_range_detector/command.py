__all__ = ()

import sys
from os.path import isfile as is_file

from hata.main import register

from ...bot_utils.ip_filtering import IP_TYPE_NONE, parse_ip, produce_ip_representation

from .logic import get_entry_for_ip, parse_entry_from_line


@register
def ip_range_detector(
    data_file_path : str,
):
    """
    Detects the ip ranges of the given ips. First pass a data file as a parameter and then input the ips. Line by line.
    """
    if not is_file(data_file_path):
        sys.stdout.write('Data file is not a file or does not exist.\n')
        return
    
    # Read data file
    entries = []
    string_cache = {}
    
    with open(data_file_path, 'r') as file:
        for line in file:
            entry = parse_entry_from_line(line, string_cache)
            if (entry is not None):
                entries.append(entry)
    
    # Clean up
    string_cache = None
    
    # Keep reading input
    interrupted = False
    
    while True:
        # read input while till user enters 2 line breaks
        sys.stdout.write('Enter sections:\n')
        last_line_empty = False
        
        lines = []
        
        while True:
            try:
                line = input()
            except KeyboardInterrupt:
                interrupted = True
                break
            
            if line:
                lines.append(line)
                continue
            
            if last_line_empty:
                break
            
            last_line_empty = True
            continue
        
        # Process output lines
        if lines:
            unmatched_lines = None
            matched_entries = None
            
            for line in lines:
                # Match ip in line
                while True:
                    split = line.split(maxsplit = 1)
                    if len(split) < 1:
                        matched = False
                        break
                    
                    ip_type, ip = parse_ip(split[0])
                    if ip_type == IP_TYPE_NONE:
                        matched = False
                        break
                    
                    matched = True
                    break
                
                if matched:
                    if matched_entries is None:
                        matched_entries = []
                    matched_entries.append((split[0], ip_type, ip))
                else:
                    if unmatched_lines is None:
                        unmatched_lines = []
                    unmatched_lines.append(line)
                
                continue
            
            lines = None
            output_parts = ['\n']
            
            if (unmatched_lines is not None):
                output_parts.append('Unmatched lines: \n')
                for line in unmatched_lines:
                    output_parts.append(line)
                    output_parts.append('\n')
                
                output_parts.append('\n')
            
            if (matched_entries is not None):
                output_parts.append('Matched lines: \n')
                just_rendered_entries = []
                
                for ip_raw, ip_type, ip in matched_entries:
                    # match ip to entries
                    if (get_entry_for_ip(just_rendered_entries, ip_type, ip) is not None):
                        continue
                    
                    entry = get_entry_for_ip(entries, ip_type, ip)
                    just_rendered_entries.append(entry)
                    
                    # Produce output
                    # Example:
                    # '    IPFilterRule(*parse_ip('86.57.60.0'), 10), # Tehran - Asiatech Data Transmission Co.'
                    
                    output_parts.append('    IPFilterRule(*parse_ip(\'')
                    
                    if entry is None:
                        output_parts.append(ip_raw)
                    else:
                        output_parts.extend(produce_ip_representation(entry[0], entry[1]))
                    
                    output_parts.append('\'), ')
                    
                    if entry is None:
                        absorbed = 0
                    else:
                        absorbed = entry[2]
                    
                    output_parts.append(repr(absorbed))
                    
                    output_parts.append('), # ')
                    
                    if entry is None:
                        location_name = 'unknown'
                    else:
                        location_name = entry[3]
                        if location_name is None:
                            location_name = 'unknown'
                    
                    output_parts.append(location_name)
                    output_parts.append(' - ')
                    
                    if entry is None:
                        company_name = 'unknown'
                    else:
                        company_name = entry[8]
                        if company_name is None:
                            company_name = 'unknown'
                    
                    output_parts.append(company_name)
                    output_parts.append('\n')
                    continue
                
                output_parts.append('\n')
                
                just_rendered_entries = None
            
            # Write and clean
            sys.stdout.write(''.join(output_parts))
            
            unmatched_lines = None
            matched_entries = None
            output_parts = None
        
        if interrupted:
            break
        
        continue
