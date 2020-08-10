import json
from flask_apispec import use_kwargs, marshal_with, doc, MethodResource
from umongo.exceptions import UpdateError
from marshmallow.exceptions import ValidationError
from .models import User, instance, ErrorResponse
from .helpers import with_many

@doc(tags=['Users'])
class UsersController(MethodResource):
    @marshal_with(with_many(User.schema))
    def get(self):
        return User.find()

    @use_kwargs(User.schema)
    @marshal_with(User.schema,
                  description="Success",
                  code=200)
    @marshal_with(ErrorResponse().schema,
                  description="Failure",
                  code=403)
    def put(self, **kwargs):
        user = User(**kwargs)
        try:
            user.commit()
            return user, 200
        except ValidationError as e:
            return {"error": str(e)}, 403

@doc(tags=['User'])
class UserController(MethodResource):
    @marshal_with(User.schema)
    def get(self, user_id):
        user = User.find_one({'_id': user_id})
        if user:
            return user
        return {"failed"}