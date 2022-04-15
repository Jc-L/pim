import os

# local modules
import pimdata

from flask import Flask, render_template, url_for


def create_app(config):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    
    #app.config.from_mapping(
    #    SECRET_KEY='dev',
    #    DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    #)

    app.config.from_object(config)
    # app.config.from_envvar('PIM_CONFIGFILE')

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass


    # a simple page that says hello
    @app.route('/hello/')
    @app.route('/hello/<name>')
    def hello(name=None):
        return render_template('hello.html', name=name)
    
    # url_for('static', filename='style.css')

    return app