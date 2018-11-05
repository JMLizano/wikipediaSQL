# -*- coding: utf-8 -*-
"""Application configuration.

Most configuration is set via environment variables.

For local development, use a .env file to set
environment variables.
"""
from environs import Env

env = Env()
env.read_env()

ENV = env.str('FLASK_ENV', default='production')
DEBUG = ENV == 'development'
TESTING = True
SQLALCHEMY_DATABASE_URI = env.str('DATABASE_URL')
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = env.str('SECRET_KEY')
