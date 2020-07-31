from flask import Flask, render_template, redirect, request
from flask_mongoengine import MongoEngine
from flask_mongoengine.wtf import model_form
from wtforms import validators

def create_app():
    # create and configure the app
    app = Flask(__name__)
    
    app.config.from_pyfile('config.py')

    db = MongoEngine(app, config={'db': 'test34'})
    
    class User(db.Document):
        email = db.StringField(required=True)
        first_name = db.StringField(max_length=50)
        last_name = db.StringField(max_length=50)

    class Content(db.EmbeddedDocument):
        text = db.StringField()
        lang = db.StringField(max_length=3)

    class Post(db.Document):
        title = db.StringField(max_length=120, required=True, validators=[validators.InputRequired(message=u'Missing title.')])
        author = db.ReferenceField(User)
        tags = db.ListField(db.StringField(max_length=30))
        content = db.EmbeddedDocumentField(Content)

    PostForm = model_form(Post)
    
    def add_post(request):
        form = PostForm(request.get_data())
        if request.method == 'POST' and form.validate():
            # do something
            redirect('done')
        return render_template('add_post.html', form=form)
    
    

    # # ensure the instance folder exists
    # try:
    #     os.makedirs(app.instance_path)
    # except OSError:
    #     pass

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    return app