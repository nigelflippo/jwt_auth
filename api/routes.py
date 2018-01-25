from flask import request, make_response, jsonify, abort
from api.models import Users, BlacklistToken
from api import app, db, bcrypt


@app.route('/')
def index():
	return "JWT AUTH"

@app.route('/auth/register', methods=['POST'])
def register():
	email = request.json.get('email')
	password = request.json.get('password')
	if email is None or password is None:
		responseObject = {
			'status': 'error',
			'message': 'Invalid input.'
		}
		return jsonify(responseObject), 400
	if Users.query.filter_by(email=email).first() is not None:
		responseObject = {
			'status': 'error',
			'message': 'User already exists.'
		}
		return jsonify(responseObject), 400
	user = Users(
		email=email, 
		password=password
	)
	db.session.add(user)
	db.session.commit()

	auth_token = user.encode_auth_token(user.id)
	responseObject = {
		'email': user.email,
		'status': 'success',
		'message': 'Successfully registered',
		'auth_token': auth_token.decode()
	}
	return jsonify(responseObject), 201

@app.route('/auth/login', methods=['POST'])
def user_login():
	email = request.json.get('email')
	password = request.json.get('password')
	user = Users.query.filter_by(email=email).first()
	if user and bcrypt.check_password_hash(user.password, password):
		auth_token = user.encode_auth_token(user.id)
		if auth_token:
			responseObject = {
				'status': 'success',
				'message': 'Successfully logged in.',
				'auth_token': auth_token.decode()
			}
			return jsonify(responseObject), 200
	else:
		responseObject = {
			'status': 'error',
			'message': 'Invalid login.'
		}
		return jsonify(responseObject), 404

@app.route('/auth/status', methods=['GET'])
def get_auth():
	auth_header = request.headers.get('Authorization')
	auth_token = auth_header.split(' ')[0]

	if auth_token:
		decoded = Users.decode_auth_token(auth_token)
		if isinstance(decoded, str):
			responseObject = {
			'status': 'error',
			'message': decoded
			}
			return jsonify(responseObject), 401
		else:
			user = Users.query.get(decoded)
			responseObject = {
				'status': 'success',
				'data': {
					'user_id': user.id,
					'email': user.email,
					'admin': user.admin,
					'registered_on': user.registered_on
				}
			}
			return jsonify(responseObject), 200
	else:
		responseObject = {
			'status': 'error',
			'message': 'Invalid token.'
		}
		return jsonify(responseObject), 401
	
@app.route('/auth/logout', methods=['POST'])
def logout():
	auth_header = request.headers.get('Authorization')
	auth_token = auth_header.split(' ')[0]

	if auth_token:
		decoded = Users.decode_auth_token(auth_token)
		if isinstance(decoded, str):
			responseObject = {
				'status': 'error',
				'message': decoded
			}
			return jsonify(responseObject), 401
		else:
			blacklist_token = BlacklistToken(token=auth_token)
			db.session.add(blacklist_token)
			db.session.commit()
			responseObject = {
				'status': 'success',
				'message': 'Logged out.'
			}
			return jsonify(responseObject), 200
	else:
		responseObject = {
			'status': 'error',
			'message': 'Invalid token.'
		}
		return jsonify(responseObject), 403

@app.route('/users/<int:id>')
def get_user(id):
	user = Users.query.get(id)
	if not user:
		abort(400)
	return jsonify({'email': user.email, 'password': user.password})

@app.route('/tokens/blacklist/<int:id>')
def get_blacklist_token(id):
	token = BlacklistToken.query.get(id)
	if not token:
		abort(400)
	return jsonify({'token': token.token, 'blacklisted_on': token.blacklisted_on})

