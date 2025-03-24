from sqlalchemy.orm import scoped_session
from falcon import HTTPBadRequest, HTTPCreated
from db import Session
from models import Task

class TaskResource:
    def __init__(self):
        self.session = scoped_session(Session)

    def on_post(self, req, resp):
        user = req.context['user']
        data = req.media
        title = data.get('title')
        description = data.get('description')

        if not title:
            raise HTTPBadRequest('Missing title', 'Task title is required.')

        new_task = Task(title=title, description=description, owner=user)
        self.session.add(new_task)
        self.session.commit()
        resp.status = HTTPCreated
        resp.media = {'message': 'Task created successfully'}
