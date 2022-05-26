#!/usr/bin/env python3
""" Password Authentication
"""
from bcrypt import hashpw, gensalt, checkpw
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError
from uuid import uuid4
from typing import Union


def _hash_password(password: str) -> str:
    """ Takes in a password string arguments and returns
        bytes in a salted hash.
    """
    return hashpw(password.encode('utf-8'), gensalt())


def _generate_uuid() -> str:
    """ Generates UUID and returns string representation of it
    """
    return str(uuid4())


class Auth:
    """ Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """ Returns User object
        """
        try:
            self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            hashed_password = _hash_password(password)
            new_user = self._db.add_user(email, hashed_password)
            return new_user

    def valid_login(self, email: str, password: str) -> bool:
        """ Locates user by email, checks if password is valid
        """
        try:
            user_found = self._db.find_user_by(email=email)
            hashed_password = _hash_password(password)
            return checkpw(
                password.encode('utf-8'),
                user_found.hashed_password
            )
        except NoResultFound:
            return False

    def create_session(self, email: str) -> str:
        """ Finds user corresponding to email, generates a new UUID,
        stores it in database and returns session ID
        """
        try:
            user_found = self._db.find_user_by(email=email)
        except NoResultFound:
            return None

        session_id = _generate_uuid()
        self._db.update_user(user_found.id, session_id=session_id)
        return session_id

    def get_user_from_session_id(self, session_id: str) => Union[str, None]:
        """ Finds user by session_id
        """
        if session_id is None:
            return None
        try:
            user_found = self._db.find_user_by(session_id=session_id)
            return user_found
        except NoResultFound:
            return None

    def destroy_session(self, user_id: str) -> Nine:
        """ Updates user session_id to None
        """
        if user_id is None:
            return None
        try:
            user_found = self._db.find_user_by(id=user_id)
            self._db.update_user(user_found.id, session_id=None)
        except NoResultFound:
            return None

    def get_reset_password_token(self, email: str) -> str:
        """ Finds user based by email and updates reset token with UUID
        """
        try:
            user_found = self._db.find_user_by(email=email)
        except NoResultFound:
            raise ValueError

        reset_token = _generate_uuid()
        self._db.update_uset(user_found.id, reset_token=reset_token)
        return reset_token

    def update_password(self, reset_token: str, password: str) -> None:
        """ Uses reset token to find user, or raises ValueError
        """
        if reset_token is None or password is None:
            return None

        try:
            user = self._db.fins_user_by(reset_token=reset_token)
        except NoResultFound:
            raise ValueError

        hashed_password = _hash_password(password)
        self._db.update_user(user.id,
                             hashed_password=hashed_password,
                             reset_token=None)
