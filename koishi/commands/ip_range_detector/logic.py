__all__ = ()

from scarletio import from_json

from ...bot_utils.ip_filtering import IP_TYPE_NONE, IP_TYPE_IP_V4, IP_TYPE_IP_V6, parse_ip


def parse_entry_from_line(line, string_cache):
    """
    Reads an entry from the given line.
    
    Parameters
    ----------
    line : `str`
        Line to parse.
    
    string_cache : `dict<str, str>`
        String cache to use for deduplication.
    
    Returns
    -------
    entry : `None | (int, int, int, None | str, None | str, None | str, None | str, None | str, None | str, None | str)`
    """
    entry_raw = from_json(line)
    
    network = entry_raw['network']
    per_index = network.find('/')
    
    if per_index == -1:
        ip_raw = network
        allowed_raw = None
    else:
        ip_raw = network[: per_index]
        per_index += 1
        if per_index == len(network):
            allowed_raw = None
        else:
            allowed_raw = network[per_index :]
    
    ip_type, ip = parse_ip(ip_raw)
    if ip_type == IP_TYPE_NONE:
        return
    
    if allowed_raw is None:
        absorbed = 0
    else:
        try:
            allowed = int(allowed_raw)
        except ValueError:
            absorbed = 0
        else:
            if ip_type == IP_TYPE_IP_V4:
                absorbed = 32 - allowed
            
            elif ip_type == IP_TYPE_IP_V6:
                absorbed = 128 - allowed
            
            else:
                absorbed = 0
    
    
    country_name = entry_raw['country']
    if (country_name is not None):
        country_name = string_cache.setdefault(country_name, country_name)
    
    country_code = entry_raw['country_code']
    if (country_code is not None):
        country_code = string_cache.setdefault(country_code, country_code)
    
    continent_name = entry_raw['continent']
    if (continent_name is not None):
        continent_name = string_cache.setdefault(continent_name, continent_name)
    
    continent_code = entry_raw['continent_code']
    if (continent_code is not None):
        continent_code = string_cache.setdefault(continent_code, continent_code)
    
    autonomous_system_number = entry_raw['asn']
    if (autonomous_system_number is not None):
        autonomous_system_number = string_cache.setdefault(autonomous_system_number, autonomous_system_number)
    
    autonomous_system_name = entry_raw['as_name']
    if (autonomous_system_name is not None):
        autonomous_system_name = string_cache.setdefault(autonomous_system_name, autonomous_system_name)
    
    autonomous_system_domain = entry_raw['as_domain']
    if (autonomous_system_domain is not None):
        autonomous_system_domain = string_cache.setdefault(autonomous_system_domain, autonomous_system_domain)
    
    return (
        ip_type,
        ip,
        absorbed,
        country_name,
        country_code,
        continent_name,
        continent_code,
        autonomous_system_number,
        autonomous_system_name,
        autonomous_system_domain,
    )


def get_entry_for_ip(entries, ip_type, ip):
    """
    Gets the entry for the given ip.
    
    Parameters
    ----------
    entries : `list<(int, int, int, None | str, None | str, None | str, None | str, None | str, None | str, None | str)>`
        Entries to select from.
    
    ip_type : `int`
        The ip's type.
    
    ip : `int`
        The ip's value.
    
    Returns
    -------
    entry : `None | (int, int, int, None | str, None | str, None | str, None | str, None | str, None | str, None | str)`
    """
    for entry in entries:
        entry_ip_type = entry[0]
        if ip_type != entry_ip_type:
            continue
        
        entry_ip = entry[1]
        entry_absorbed = entry[2]
        if entry_absorbed:
            ip_to_match = ip &~ ((1 << entry_absorbed) - 1)
        else:
            ip_to_match = ip
        
        if entry_ip != ip_to_match:
            continue
        
        return entry
