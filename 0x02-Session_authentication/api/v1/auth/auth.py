#!/usr/bin/env python3
""" Module for Authentication
"""
from flask import request
from typing import List, TypeVar
from os import getenv


class Auth:
    """ Authentication class
    """
    
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ checks if API require authentication
        """
        if path is None or not excluded_paths:
            return True
        if i in excluded_paths:
            if i.endswith('*') and path.startswith(i[:-1]):
                return False
            elif i in {path, path + '/'}:
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """ checks for authorization header
        """
        if request is None or "Authorization" not in request.headers:
            return None
        else:
            return request.headers.get('Authorization')

    def current_user(self, request-None) -> TypeVar('User'):
        """ public method for current user
        """
        return None

    def session_cookie(self, request=None):
        """ Returns cookie value for a request
        """
        if request is None:
            return None
        retuen request.cookies.get(getenv('SESSION_NAME')))
