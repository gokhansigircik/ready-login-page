from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

from flask_app import DATABASE, bcrypt

# from flask_app.models.user_model import User


import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


class User:
    def __init__(self, data):
        self.id = data["id"]
        self.email = data["email"]
        self.name = data["name"]
        self.password = data["password"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

    @classmethod
    def find_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"

        results = connectToMySQL(DATABASE).query_db(query, data)

        if results and len(results) > 0:
            found_user = cls(results[0])
            return found_user
        else:
            return False

    @classmethod
    def register(cls, data):
        query = "INSERT INTO users (name, email, password) VALUES (%(name)s, %(email)s, %(password)s);"

        return connectToMySQL(DATABASE).query_db(query, data)

    @classmethod
    def validate_login(cls, data):

        found_user = cls.find_by_email(data)

        if not found_user:
            flash("Invalid login...")
            return False
        elif not bcrypt.check_password_hash(found_user.password, data['password']):
            flash("Invalid login...")
            return False

        return found_user
# ******************************************

    @staticmethod
    def validate(data):
        is_valid = True

        if len(data['name']) < 1:
            flash("Please provide a username!")
            is_valid = False

        if len(data['password']) < 1:
            flash("Please provide a user password!")
            is_valid = False

        if len(data['email']) < 1:
            flash("Please provide a email!")
            is_valid = False

        elif not EMAIL_REGEX.match(data['email']):
            flash("Please provide a VALID email...")
            is_valid = False

        return is_valid
