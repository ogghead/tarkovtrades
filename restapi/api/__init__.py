from flask import Flask, redirect, render_template

# from flask_debugtoolbar import DebugToolbarExtension, request
# app.session_interface = MongoEngineSessionInterface(db)
# toolbar = DebugToolbarExtension(app)

def create_app(config_filename='config.py'):
    # create and configure the app
    app = Flask(__name__)
    
    app.config.from_pyfile(config_filename)

    from flask_mongoengine import MongoEngine
    db = MongoEngine(app, config={'db': 'test34'})

    from flask_mongoengine.wtf import model_form
    from .models.user import Post
    PostForm = model_form(Post)
    
    def add_post(request):
        form = PostForm(request)
        if request.method == 'POST' and form.validate():
            # do something
            redirect('done')
        return render_template('add_post.jinja', form=form)

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        print(db)
        # return add_post(request)
        return 'Hello, World!'

    return app