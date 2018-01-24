import os

class Config(object):
	SQLALCHEMY_DATABASE_URI = 'postgresql://localhost/jwt_auth'
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	SECRET_KEY = os.getenv('SECRET_KEY')
	BCRYPT_LOG_ROUNDS = 13
	DEBUG = True
