import falcon
from resources.user import UserResource
from resources.task import TaskResource
from middleware import AuthMiddleware

app = falcon.App(middleware=[AuthMiddleware()])

user_resource = UserResource()
task_resource = TaskResource()

app.add_route('/users', user_resource)
app.add_route('/tasks', task_resource)
