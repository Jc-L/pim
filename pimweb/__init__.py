import os

# local modules
from pimdata import *

from flask import Blueprint, Flask, flash, g, redirect, render_template, request, url_for


def create_module(config):
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
    @app.route('/')
    def index(name=None):
        return render_template('index.html')
    
    @app.route('/people/')
    def people():
        return render_template('people.html', people=People.select())

    @app.route('/tasks/')
    def tasks():
        return render_template('tasks/list.html', tasks=Task.select())

    @app.route("/tasks/create", methods=("GET", "POST"))
    def create():
        """Create a new task."""
        if request.method == "POST":
            label = request.form["label"]
            description = request.form["description"]
            error = None

            if not label:
                error = "Label is required."

            if error is not None:
                flash(error)
            else:
                task = Task()
                task.label = label
                task.description = description
                task.save()
                return redirect(url_for("index"))

        return render_template("tasks/create.html")



   #  url_for('static', filename='style.css')

    return app