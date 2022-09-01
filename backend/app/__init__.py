#!/usr/bin/env python
# -*- coding:utf-8 -*-

from flask import Flask
from flask_cors import CORS
from pymongo import MongoClient

mongo_client = MongoClient(f'mongodb://root:mongo31415926@localhost:27017/')


def create_app():
    app = Flask(__name__)
    CORS(app, resources={r"/*": {"origins": "*"}})
    app.config['SECRET_KEY'] = 'hard to guess string'
    # app.config['JSON_AS_ASCII'] = False

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .api import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api/v1')

    @app.shell_context_processor
    def make_shell_context():
        return dict(db=mongo_client)

    return app
