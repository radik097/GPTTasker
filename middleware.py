import base64
import bcrypt
from falcon import HTTPUnauthorized
from sqlalchemy.orm import scoped_session
from db import Session
from models import User

class AuthMiddleware:
    def __init__(self):
        self.session = scoped_session(Session)

    def process_request(self, req, resp):
        auth = req.get_header('Authorization')
        if auth is None:
            raise HTTPUnauthorized('Auth token required', 'Please provide an auth token.')

        try:
            auth_type, credentials = auth.split(' ')
            if auth_type.lower() != 'basic':
                raise HTTPUnauthorized('Invalid auth type', 'Auth type must be Basic.')
            decoded = base64.b64decode(credentials).decode('utf-8')
            username, password = decoded.split(':')
        except (ValueError, AttributeError):
            raise HTTPUnauthorized('Invalid credentials', 'Unable to decode credentials.')

        user = self.session.query(User).filter_by(username=username).first()
        if user is None or not bcrypt.checkpw(password.encode('utf-8'), user.password_hash.encode('utf-8')):
            raise HTTPUnauthorized('Authentication failed', 'Invalid username or password.')

        req.context['user'] = user
