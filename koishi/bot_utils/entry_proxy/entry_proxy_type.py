__all__ = ('EntryProxyType',)


class EntryProxyType(type):
    """
    The entry proxy type.
    """
    def __new__(cls, type_name, base_types, type_attributes, **keyword_parameters):
        """
        Creates a new compound component.
        
        Parameters
        ----------
        type_name : `str`
            The created component's name.
        
        base_types : `tuple` of `type`
            types from which the type inherits from.
        
        type_attributes : `dict<str, object>`
            Attributes defined in the type body.
        
        **keyword_parameters : Keyword parameters
            Additional keyword parameters.
        
        Returns
        -------
        built_type : `instance<cls>`
            The created type
        """
        aggregated_field_setters = {}
        
        # Aggregate base type field setters
        for base_type in base_types:
            if isinstance(base_type, cls):
                try:
                    base_type_field_setters = getattr(base_type, 'field_setters')
                except AttributeError:
                    pass
                else:
                    aggregated_field_setters.update(base_type_field_setters)
        
        # Aggregate custom field setters
        try:
            custom_field_setters = type_attributes['field_setters']
        except KeyError:
            custom_field_setters_present = False
        
        else:
            custom_field_setters_present = True
            aggregated_field_setters.update(custom_field_setters)
        
        type_attributes['field_setters'] = aggregated_field_setters
        
        built_type = type.__new__(cls, type_name, base_types, type_attributes, **keyword_parameters)
        
        # Aggregate new field setters
        if not custom_field_setters_present:
            try:
                slot_names = type_attributes['__slots__']
            except KeyError:
                pass
            else:
                for slot_name in slot_names:
                    try:
                        slot_descriptor = getattr(built_type, slot_name)
                    except AttributeError:
                        pass
                    else:
                        aggregated_field_setters[slot_name] = slot_descriptor.__set__
        
        return built_type
