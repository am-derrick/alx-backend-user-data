#!/usr/bin/env python3
""" Flask App
"""
from flask import Flask, jsonify, request, abort, redirect, url_for
from sqlalchemy.orm.exc import NoResultFound
from auth import Auth


app = Flask(__name__)
AUTH = Auth()


@app.route('/', methods=['GET'], strict_slashes=False)
def status() -> str:
    """ GET /status
    Return:
       - JSON payload
    """
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'], strict_slashes=False)
def new_user() -> str:
    """ POST /users
    Registers new user with email and password or finds if user
    is already registered using email
    Return:
       - JSON paylod
    """

    email = request.fomr.get("email")
    password = request.form.get("password")

    try:
        new_user = AUTH.register_user(email, password)
        if new_user is not None:
            return jsonify({
                "email": new_user.email,
                "message": "user created"
            })
    except ValueError:
        return jsonify({
            "message": "email already registered"
        }), 400


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login() -> str:
    """ POST /sessions
    Creates new user session, stores cookie, email and password
    Return:
      - JSON payload
    """
    email = request.form.get("email")
    password = request.form.get("password")
    valid_user = AUTH.valid_login(email, password)

    if not valid_user:
        abort(401)
    session_id = AUTH.create_seesion(email)
    message = {"email": email, "message": "logged in"}
    response = jsonify(message)
    response.set_cookie("session_id", session_id)
    return response


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
