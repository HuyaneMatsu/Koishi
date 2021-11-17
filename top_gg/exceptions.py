__all__ = ('TopGGHttpException', )

import reprlib

from .constants import JSON_KEY_EXCEPTION_MESSAGE, JSON_KEY_EXCEPTION_CODE

class TopGGHttpException(Exception):
    """
    Http exception raised by Top.gg.
    
    Attributes
    ----------
    code : `int`
        Exception code.
    message : `str`
        Exception message.
    """
    
    def __init__(self, response, response_data):
        """
        Creates a new top.gg http exception instance.
        
        Parameters
        ----------
        response : ``ClientResponse``
            Response from top.gg.
        response_data : `str` or `dict` of (`str`, `Any`) items
            Response data.
        """
        if isinstance(response_data, str):
            message = response_data
            code = 0
        elif isinstance(response_data, dict):
            message = response_data.get(JSON_KEY_EXCEPTION_MESSAGE, '')
            code = response_data.get(JSON_KEY_EXCEPTION_CODE, 0)
        else:
            message = ''
            code = 0
        
        self.message = message
        self.code = code
        self.response = response
        
        Exception.__init__(response, response_data)
    
    
    @property
    def status(self):
        """
        Returns the response's status code.
        
        Returns
        -------
        status_code : `int`
        """
        return self.response.status
    
    
    def __repr__(self):
        """Returns the exception's representation."""
        repr_parts = ['<', self.__class__.__name__, ' status=', str(self.response.status)]
        
        code = self.code
        if code:
            repr_parts.append(', code=')
            repr_parts.append(reprlib.repr(code))
        
        message = self.message
        if message:
            repr_parts.append(', message=')
            repr_parts.append(reprlib.repr(message))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
