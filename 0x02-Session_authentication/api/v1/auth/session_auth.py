#!/usr/bin/env python3
""" Module for API session authentication
"""
from api.v1.auth.auth import Auth
from models.user import User
import uuid


class SessionAuth(Auth):
    """ Session Authentication
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """ creates session ID for user id
        """
        if user_id is None or isinstnce(user_id, str) is False:
            return None

        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id

        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """ Returms User ID based on session ID
        """
        if session_id is None or isinstance(Session_id, str) is False:
            return None
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """ Returns user instance based on cookie value
        """
        session_id = self.session_cokie(request)
        user_id = self.user_id_for_session_id(session_id)
        return User.get(user_id)

    def destroy_session(self, request=None):
        """ Deletes user session to logout
        """
        if request is None:
            return False
        cookie = self.sesion_cookie(request)
        if cookie is None or self.user_id_for_session_id(cookie) is None:
            return False
        del self.user_id_by_session_id[cookie]
        return True
