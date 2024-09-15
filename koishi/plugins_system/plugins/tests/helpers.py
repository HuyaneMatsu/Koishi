from importlib.util import spec_from_file_location


def mock_spec_from_file_location(name, location = None):
    assert location is not None
    return _bootstrap.ModuleSpec(name, SourceFileLoader(name, location), origin = location)


def wrap_mock_spec_from_file_location():
    """
    Mocks `spec_from_file_location` in a for block because its a cursed technique.
    """
    original_code = spec_from_file_location.__code__
    spec_from_file_location.__code__ = mock_spec_from_file_location.__code__
    
    try:
        yield
    finally:
        spec_from_file_location.__code__ = original_code
