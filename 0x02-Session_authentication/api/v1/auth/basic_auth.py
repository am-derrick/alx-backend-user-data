#!/usr/bin/env python3
""" API authentication module
"""
from api.v1.auth.auth import Auth
from base64 import b64decode
from models.user import User
from typing import TypeVar


class BasicAuth(Auth):
    """ Basic Authentication
    """

    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        """ returns Base64 part of Authorization header
        """
        if authorization_header is isinstance(
                authorization_header,
                str) and authorization_header.startswith("Basic "):
            return authorization_header[6:]

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """ returns decoded value of base64_authorization_header
        """
        if base64_auhtorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None

        try:
            return b64decode(base64_authorization_header).decode('utf-8')
        except Exception:
            return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> (str, str):
        """ retutns user credentials from decoded Base64
        """
        if decoded_base64_authorization_header is None:
            return None, None
        if not isinstance(decoded_base64_authorization_header, str):
            return None, None
        if ":" not in decoded_base64_authorization_header:
            return None, None
        email, pwd = decoded_based64_authorization_header.split(':', 1)
        return (email, pwd)

    def user_object_from_credentials(self,
                                     user_email: str,
                                     user_pwd: str) -> TypeVar('User'):
        """ returns user instance based on credentials
        """
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None
        try:
            users = User.search({'email': user_email})
        except Exception:
            return None
        for user in users:
            if user.is_valid_password(user_pwd):
                return user
            return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ overrides Auth and retrives User instance for request
        """
        auth_header = self.authorization_header(request)

        b64_header = self.extract_base54_authorization_header(auth_header)
        decoded_header = self.decode_base64_auhtorization_header(base64_header)
        user_cred = self.extract_user_credentials(decoded_header)
        return self.user_object_from_credentials(*user_creds)
