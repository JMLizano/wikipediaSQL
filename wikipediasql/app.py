# -*- coding: utf-8 -*-
"""The app module, containing the app factory function."""
from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
from .public import views
from .extensions import db, bootstrap


def create_app(config_object='wikipediasql.settings'):
    """An application factory

    :param config_object: The configuration object to use.
    """
    app = Flask(__name__.split('.')[0])
    app.config.from_object(config_object)
    register_blueprints(app)
    register_errorhandlers(app)
    register_extensions(app)
    return app


def register_blueprints(app):
    """Register Flask blueprints."""
    app.register_blueprint(views.blueprint)
    return None


def register_extensions(app):
    """Register Flask extensions."""
    db.init_app(app)
    bootstrap.init_app(app)


def register_errorhandlers(app):
    """Register error handlers."""
    def render_error(error):
        """Render error template."""
        # If a HTTPException, pull the `code` attribute; default to 404
        error_code = getattr(error, 'code', 404)
        return render_template('{0}.html'.format(error_code)), error_code
    for errcode in [404]:
        app.errorhandler(errcode)(render_error)
    return None