from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin

TESTING = True
DEBUG = True
MONGO_DBS = ['test1', 'test2']
MONGODB_SETTINGS = [{'alias': db,
                     'db': db,
                     'host': 'mongo'} 
                    for db in MONGO_DBS]
APISPEC_SPEC = APISpec(
    title="My API",
    version='v1',
    plugins=[
        MarshmallowPlugin()
    ],
    openapi_version='2.0'
)
