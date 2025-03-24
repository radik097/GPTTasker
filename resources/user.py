import bcrypt
from sqlalchemy.orm import scoped_session
from sqlalchemy.exc import IntegrityError
from falcon import HTTPBadRequest, HTTPConflict, HTTPCreated
from db import Session
from models import User

class UserResource:
    def __init__(self):
        self.session = scoped_session(Session)

    def on_post(self, req, resp):
        data = req.media
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            raise HTTPBadRequest('Missing fields', 'Username and password are required.')

        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        new_user = User(username=username, password_hash=password_hash)

        try:
            self.session.add(new_user)
            self.session.commit()
        except IntegrityError:
            self.session.rollback()
            raise HTTPConflict('User exists', 'Username already taken.')

        resp.status = HTTPCreated
        resp.media = {'message': 'User created successfully'}
