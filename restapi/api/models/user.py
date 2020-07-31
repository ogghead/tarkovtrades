import mongoengine as me
from wtforms import validators

class User(me.Document):
    email = me.StringField(required=True)
    first_name = me.StringField(max_length=50)
    last_name = me.StringField(max_length=50)
    
class Content(me.EmbeddedDocument):
    text = me.StringField()
    lang = me.StringField(max_length=3)

class Post(me.Document):
    title = me.StringField(max_length=120, required=True, validators=[validators.InputRequired(message=u'Missing title.')])
    author = me.ReferenceField(User)
    tags = me.ListField(me.StringField(max_length=30))
    content = me.EmbeddedDocumentField(Content)