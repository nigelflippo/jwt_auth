from flask import request, make_response, jsonify, abort
from api.models import Users
from api import app, db, bcrypt


@app.route('/')
def index():
	return "JWT AUTH"

@app.route('/users/auth/register', methods=['POST'])
def register():
	email = request.json.get('email')
	password = request.json.get('password')
	if email is None or password is None:
		abort(400)
	if Users.query.filter_by(email=email).first() is not None:
		abort(400)
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
	return make_response(jsonify(responseObject)), 201

@app.route('/users/<int:id>')
def get_user(id):
	user = Users.query.get(id)
	if not user:
		abort(400)
	return jsonify({'email': user.email, 'password': user.password})

