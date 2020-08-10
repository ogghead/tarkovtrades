import umongo as um

instance = um.PyMongoInstance()

@instance.register
class User(um.Document):
    class Meta:
        collection_name = "Users"
    email = um.fields.EmailField(required=True, unique=True)
    password = um.fields.StringField(required=True)
    is_admin = um.fields.BooleanField(default=False)
    security_level = um.fields.IntegerField(choices=[1, 2, 3], default=1)

@instance.register
class ErrorResponse(um.Document):
    error = um.fields.StringField(required=True)
