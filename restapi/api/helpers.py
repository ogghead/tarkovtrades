from copy import deepcopy

def with_many(schema):
    schema_copy = deepcopy(schema)
    schema_copy.many = True
    return schema_copy

# FOR EXPLORING UMONGO
from umongo.abstract import BaseField, BaseSchema, BaseValidator
from umongo import Document, Instance
from umongo.frameworks.pymongo import PyMongoDocument